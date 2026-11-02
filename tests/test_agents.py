"""`AGENTS.md` and `.xerjignore` describe the tree to an agent and to a text
index of it; both must stay true as the tree changes.

The paths AGENTS.md names exist, the commands it quotes parse, the field
names and coverage values it lists are the code's and the schema's, and
the directories it calls not the corpus are exactly the ones `.xerjignore`
skips, as git's own matcher reads the file. The set of top-level
directories is closed, so a new one fails here until it is placed on one
side or the other. The checks that need git skip where there is no
checkout.
"""

import json
import pathlib
import re
import shlex
import subprocess

import pytest
import yaml

from phylohist import cli
from tests import support

ROOT = support.ROOT
AGENTS = (ROOT / 'AGENTS.md').read_text()
XERJIGNORE = ROOT / '.xerjignore'

# What AGENTS.md says is not the corpus, and how `.xerjignore` treats it:
# the whole directory, or everything but its README.
SKIPPED = {'drafts': 'README.md', 'notes': 'README.md', 'eval/runs': None, 'tests/corpus': None}
KEPT_WHOLE = ['data', 'claims', 'docs', 'phylohist', 'scripts', 'schemas']
TOP_LEVEL = {
  '.github',
  'claims',
  'data',
  'docs',
  'drafts',
  'eval',
  'notes',
  'phylohist',
  'schemas',
  'scripts',
  'tests',
}


def _git(*args, **kwargs):
  return subprocess.run(
    ['git', '-c', 'core.quotePath=false', *args],
    cwd=ROOT,
    capture_output=True,
    text=True,
    **kwargs,
  )


@pytest.fixture(scope='module')
def tracked():
  """Every tracked path, or a skip when this is not a git checkout."""
  try:
    run = _git('ls-files')
  except FileNotFoundError:
    pytest.skip('git is not installed')
  if run.returncode != 0:
    pytest.skip('not a git checkout')
  return run.stdout.splitlines()


def _ignored(paths):
  """``{path: pattern}`` for the tracked paths `.xerjignore` matches, by
  git's matcher with the file as the excludes file."""
  run = _git(
    '-c',
    f'core.excludesFile={XERJIGNORE}',
    'check-ignore',
    '--no-index',
    '--verbose',
    '--stdin',
    input='\n'.join(paths),
  )
  assert run.returncode in (0, 1), run.stderr
  ignored = {}
  for line in run.stdout.splitlines():
    where, path = line.split('\t', 1)
    pattern = where.split(':', 2)[2]
    if not pattern.startswith('!'):  # verbose mode also reports a path a negation keeps
      ignored[path] = pattern
  return ignored


def _named_paths():
  """The paths AGENTS.md names in backticks: anything with a slash, a
  Markdown or JSON file, or a dotfile; placeholders in angle brackets are
  left out."""
  for token in re.findall(r'`([^`]+)`', AGENTS):
    for word in token.split():
      if '<' in word:
        continue
      if '/' in word or word.endswith(('.md', '.json')) or word.startswith('.'):
        yield word


def test_every_path_named_exists():
  missing = [p for p in _named_paths() if not (ROOT / p).exists()]
  assert missing == []
  assert '## The record' in (ROOT / 'docs' / 'claims.md').read_text()
  assert '## Checks' in (ROOT / 'README.md').read_text()


def test_every_quoted_command_parses():
  commands = re.findall(r'^ {4}poetry run phylohist (.+)$', AGENTS, re.MULTILINE)
  assert len(commands) == 4
  parser = cli.build_parser()
  for command in commands:
    parser.parse_args(shlex.split(command))


def test_coverage_values_are_the_schemas():
  schema = yaml.safe_load((ROOT / 'schemas' / 'phylogeny.yaml').read_text())
  enums = []

  def walk(node):
    if isinstance(node, dict):
      if 'partly' in (node.get('enum') or []):
        enums.append(node['enum'])
      for value in node.values():
        walk(value)
    elif isinstance(node, list):
      for value in node:
        walk(value)

  walk(schema)
  assert len(enums) == 1
  listed = '(' + ', '.join(f'`{v}`' for v in enums[0]) + ')'
  assert listed in AGENTS


def test_claim_fields_are_the_tables(store):
  row = next(line for line in AGENTS.splitlines() if line.startswith('| `claims/<source>.jsonl`'))
  fields = set(re.findall(r'`(\w+)`', row.split('|')[2]))
  assert fields
  present = set()
  for claim in store.by_id.values():
    present |= set(claim)
  assert fields <= present


def test_manifest_rows_carry_what_agents_md_reads():
  manifest = json.loads((ROOT / 'claims' / 'manifest.json').read_text())
  rows = [row for row in manifest['sources'].values() if 'aliasOf' not in row]
  assert rows  # an alias row names the source it stands for and carries its citation only
  for row in rows:
    assert {'citation', 'coverage'} <= set(row)


def test_mcp_registration_is_the_server_script():
  registered = json.loads((ROOT / '.mcp.json').read_text())
  assert registered['mcpServers']['phylohist']['args'][-1] == 'scripts/mcp_server.py'


def test_ignore_file_skips_what_agents_md_says(tracked):
  ignored = _ignored(tracked)
  for directory in KEPT_WHOLE:
    assert not [p for p in ignored if p.startswith(directory + '/')], directory
  for directory, kept in SKIPPED.items():
    assert f'`{directory}/`' in AGENTS
    under = [p for p in tracked if p.startswith(directory + '/')]
    assert under, directory
    expected = {p for p in under if kept is None or p != f'{directory}/{kept}'}
    assert expected == {p for p in under if p in ignored}, directory
    if kept:
      assert f'{directory}/{kept}' in tracked
  assert 'poetry.lock' in ignored


def test_every_ignore_pattern_matches_something(tracked):
  patterns = [
    line for line in XERJIGNORE.read_text().splitlines() if line and not line.startswith(('#', '!'))
  ]
  used = set(_ignored(tracked).values())
  assert set(patterns) <= used, set(patterns) - used


def test_top_level_inventory_is_closed(tracked):
  directories = {pathlib.PurePosixPath(p).parts[0] for p in tracked if '/' in p}
  assert directories == TOP_LEVEL, (
    'a new top-level directory: say in AGENTS.md whether it is the corpus, '
    'and in .xerjignore whether an index skips it'
  )
