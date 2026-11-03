"""Plans: an answer as the blocks it is made of, executed by code.

A plan is what a planner emits instead of an answer: a one-line header
stating the parameters chosen, the blocks in order (each a tool and the
parameters that matter), and a question back when a parameter is
genuinely ambiguous. It is the same form the eval's expected answers
take. `validate` checks a plan against the tool surface without touching
the corpus; `execute` builds the composition from the corpus and reports
what could not be built.
"""

from . import blocks, tools
from .store import SPELLING_KINDS
from .words import COVERAGE_WORDS


def _specs():
  return {spec['name']: spec for spec in tools.TOOL_SPECS}


PLAN_SPEC = {
  'name': 'plan',
  'description': (
    'Answer with a plan: a one-line header stating the parameters chosen '
    '(which records the group is, whether synonyms and the same name at '
    'other ranks are included, which kinds of tree, the year range); the '
    'blocks in the order they should appear, each a tool name and its '
    'parameters; and a question back only when a parameter is genuinely '
    'ambiguous. Code builds the blocks from the corpus; you do not see '
    'them. Name records by key or as the literature prints the name, and '
    'sources by citation ("Dehm 1961"). An error names what could not be '
    'built and, when the corpus holds nothing for a block, what to plan '
    'instead: the record a source lists a spelling under, or the gap for a '
    'source with nothing or part entered.'
  ),
  'input_schema': {
    'type': 'object',
    'properties': {
      'header': {'type': 'string'},
      'blocks': {
        'type': 'array',
        'items': {
          'type': 'object',
          'properties': {
            'tool': {'type': 'string'},
            'parameters': {'type': 'object'},
          },
          'required': ['tool', 'parameters'],
        },
      },
      'question': {'type': ['string', 'null']},
    },
    'required': ['header', 'blocks'],
  },
}


def validate(plan):
  """Problems with a plan's shape: unknown tools, unknown or missing
  parameters, a tool that returns no block. Empty means well formed."""
  problems = []
  specs = _specs()
  if not isinstance(plan, dict):
    return ['a plan is an object with header, blocks and question']
  if not isinstance(plan.get('blocks'), list):
    problems.append('blocks must be a list')
    return problems
  for i, block in enumerate(plan['blocks']):
    where = f'block {i + 1}'
    if not isinstance(block, dict) or 'tool' not in block:
      problems.append(f'{where}: a block names a tool')
      continue
    spec = specs.get(block['tool'])
    if spec is None:
      problems.append(f'{where}: unknown tool {block["tool"]}')
      continue
    if block['tool'] in ('resolve_name', 'resolve_source', 'source_coverage'):
      problems.append(f'{where}: {block["tool"]} answers a lookup, not a reader; it is not a block')
      continue
    params = block.get('parameters') or {}
    if not isinstance(params, dict):
      problems.append(f'{where}: parameters must be an object')
      continue
    allowed = set(spec['input_schema']['properties'])
    for name, value in params.items():
      if name not in allowed:
        problems.append(f'{where}: {block["tool"]} has no parameter {name}')
        continue
      schema = spec['input_schema']['properties'].get(name) or {}
      if not _value_ok(value, schema):
        problems.append(
          f'{where}: {block["tool"]} {name} must be {_type_words(schema)}, '
          f'not {value!r}; leave it out for the default'
        )
    for name in spec['input_schema'].get('required', ()):
      if name not in params:
        problems.append(f'{where}: {block["tool"]} needs {name}')
  return problems


_TYPES = {
  'string': str,
  'integer': int,
  'number': (int, float),
  'boolean': bool,
  'array': list,
  'object': dict,
  'null': type(None),
}


def _value_ok(value, schema):
  """Whether `value` meets the part of JSON Schema the specs use: `type`,
  `enum`, and for a list `minItems`, `maxItems` and `items`."""
  if 'enum' in schema and value not in schema['enum']:
    return False
  kinds = schema.get('type')
  if kinds is None:
    return True
  kinds = kinds if isinstance(kinds, list) else [kinds]
  for kind in kinds:
    expected = _TYPES.get(kind)
    if expected is None:
      return True
    if isinstance(value, bool) and kind != 'boolean':
      continue
    if isinstance(value, expected):
      if kind == 'array':
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', len(value)):
          return False
        if schema.get('items'):
          return all(_value_ok(v, schema['items']) for v in value)
      return True
  return False


def _type_words(schema):
  kinds = schema.get('type')
  kinds = kinds if isinstance(kinds, list) else [kinds]
  words = {
    'string': 'a string',
    'integer': 'an integer',
    'boolean': 'true or false',
    'array': 'a list',
    'object': 'an object',
    'null': 'omitted',
  }
  said = [words.get(k, k) for k in kinds if k != 'null']
  if 'enum' in schema:
    said = ['one of ' + ', '.join(str(v) for v in schema['enum'] if v is not None)]
  elif 'array' in kinds and 'enum' in (schema.get('items') or {}):
    said = ['a list of ' + ', '.join(schema['items']['enum'])]
  if schema.get('description'):
    return (' or '.join(said) or 'omitted') + f' ({schema["description"]})'
  return ' or '.join(said) or 'omitted'


# The coverage kind a tool's block rests on, where it is not the classification.
_COVERAGE_KIND_OF_TOOL = {'synonymy': 'synonymy'}


def _nothing_hint(tool, params):
  """What to plan instead when a block builds nothing: the gap, for a
  source on record with nothing entered or with its coverage of that kind
  declared `none` or `partly`, since the contract answers such a source
  with the gap; then the related record (a spelling, the same name at
  another rank) the source does list under, when there is one, which is
  the answer for a source whose coverage is not short and a note on what
  the part entered holds for one whose coverage is. Empty when neither
  holds and the corpus simply has nothing there."""
  store = tools.store()
  source = params.get('source')
  record = params.get('record')
  source_key = store.resolver.source_key(source) if source else None
  parts, short = [], False
  if source_key:
    row = store.sources.get(source_key)
    if row is None:
      return f'the corpus has no source {source_key}; plan gap(source="{source_key}")'
    cite = store.cite(source_key)
    if not row.get('tree'):
      return f'{cite} is on record with nothing entered; plan gap(source="{source_key}")'
    kind = _COVERAGE_KIND_OF_TOOL.get(tool, 'skeleton')
    declared = (row.get('coverage') or {}).get(kind)
    if declared in ('none', 'partly'):
      short = True
      parts.append(
        f'{cite} declares {COVERAGE_WORDS[kind]} {declared} entered; '
        f'plan gap(source="{source_key}", kind="{kind}")'
      )
  if record:
    key = store.resolver.key(record)
    listed = sorted(
      k
      for k in store.resolver.related_keys(key)
      if any(
        c['kind'] == 'usage' and (source_key is None or c['source'] == source_key)
        for c in store.by_subject.get(k, ())
      )
    )
    if listed:
      row = store.names.get(key) or {}
      if row.get('kind') in SPELLING_KINDS and row.get('of') in store.names:
        parts.append(f'{row["name"]} is a spelling of {store.names[row["of"]]["name"]}')
      under = ', '.join(f'{k} ({store.names[k]["name"]})' for k in listed)
      if short:
        parts.append(f'the part entered lists under {under}')
      else:
        where = store.cite(source_key) if source_key else 'the corpus'
        parts.append(f'{where} lists under {under}: ask for that record')
  return '; '.join(parts)


def execute(plan):
  """Build a plan's composition from the corpus. Returns ``{composition,
  blocks, errors}``: the composition (None when nothing could be
  built), the blocks in order each carrying the tool and parameters
  that produced it, and one error per block that could not be built
  (an ambiguous name or citation, a bad parameter) with its message."""
  problems = validate(plan)
  if problems:
    return {
      'composition': None,
      'blocks': [],
      'errors': [{'block': None, 'error': p} for p in problems],
    }
  built, errors = [], []
  for i, spec in enumerate(plan['blocks']):
    params = dict(spec.get('parameters') or {})
    try:
      result = tools.call(spec['tool'], params, style='json')
    except ValueError as exc:
      # A bad parameter is a block that cannot be built; anything else
      # is a bug and propagates.
      errors.append({'block': i + 1, 'tool': spec['tool'], 'parameters': params, 'error': str(exc)})
      continue
    got = result if isinstance(result, list) else [result]
    got = [b for b in got if isinstance(b, dict) and 'blockId' in b]
    if not got:
      error = 'returned no block; the corpus holds nothing for these parameters'
      hint = _nothing_hint(spec['tool'], params)
      errors.append(
        {
          'block': i + 1,
          'tool': spec['tool'],
          'parameters': params,
          'error': f'{error}; {hint}' if hint else error,
        }
      )
      continue
    for b in got:
      built.append(b)
  composition = (
    blocks.compose(built, plan.get('header') or '', plan.get('question')) if built else None
  )
  return {
    'composition': composition,
    'blocks': [
      {
        'blockId': b['blockId'],
        'type': b['type'],
        'tool': b['tool'],
        'parameters': b.get('parameters'),
        'claims': b['claims'],
      }
      for b in built
    ],
    'errors': errors,
  }
