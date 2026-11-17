"""The claim table: what the extractor derives from a tree, the manifest,
and the eval questions as a demo over the committed `phylohist/table/`.

`test_question` (marked `demo`, run with `--demo`) checks that every eval
question's expected answer still builds over `phylohist/table/`. An expected
answer is the blocks it is made of (a tool and the parameters that
matter) and the strings the rendered answer shows. Each alternative is a
plan that `phylohist.plan.execute` must build in full, every block
resting on claims or being a gap or absence statement; the rendered
composition of each alternative must contain every `shows` string, the
question's and its own. The questions hold for the data they were last
refreshed against (`eval/README.md`), so the default suite skips them.

The curated corpus's manifest is gated (marked `production`): a declared
coverage value that the derived claims contradict fails until the
declaration or the tree is corrected (`scripts/claims.py
--inconsistencies` explains each row). Everything else here runs over the
test corpus.
"""

import collections
import logging
import pathlib

import pytest
import yaml

from phylohist import plan
from phylohist.claims import (
  citation,
  corrected_node,
  derived_coverage,
  extract,
  holotype_conflicts,
  manifest,
  merge_patch,
  rank_variants,
)
from phylohist.evaluation import alternatives, normalise
from phylohist.loader import io
from phylohist.loader.taxa import Tree
from phylohist.render import render_composition
from tests import support

QUESTIONS_PATH = pathlib.Path(__file__).parent.parent / 'eval' / 'questions.yaml'

with open(QUESTIONS_PATH) as fd:
  QUESTIONS = yaml.safe_load(fd)


@pytest.fixture(scope='session')
def roots(corpus):
  return corpus.records.roots


@pytest.fixture(scope='session')
def claims(corpus):
  return corpus.claims_by_source


@pytest.mark.demo
@pytest.mark.usefixtures('demo_store')
@pytest.mark.parametrize('question', QUESTIONS, ids=[q['id'] for q in QUESTIONS])
def test_question(question):
  expected = question['expected']
  qid = question['id']
  for alternative in alternatives(expected):
    # Each alternative is a plan; it must build in full and show its
    # strings and the question's.
    outcome = plan.execute({'header': '', 'blocks': alternative['blocks']})
    if outcome['errors']:
      pytest.fail(f'{qid}: {outcome["errors"]}')
    for block in outcome['blocks']:
      if block['type'] != 'statement' and not block['claims']:
        pytest.fail(f'{qid}: {block["tool"]} {block["parameters"]} rests on no claim')
    rendered = normalise(render_composition(outcome['composition'], 'text'))
    for text in list(expected.get('shows') or ()) + alternative['shows']:
      if normalise(text) not in rendered:
        pytest.fail(f'{qid}: the expected answer does not show "{text}"')


@pytest.mark.production
def test_no_inconsistencies(production):
  if production.manifest is None:
    pytest.fail('the load logged errors; see test_no_errors')
  rows = {
    source_key: entry['inconsistencies']
    for source_key, entry in production.manifest['sources'].items()
    if entry.get('inconsistencies')
  }
  if rows:
    listing = '\n'.join(f'{source_key}: {"; ".join(found)}' for source_key, found in rows.items())
    pytest.fail(
      f'{len(rows)} sources declare coverage their claims contradict '
      f'(run scripts/claims.py --inconsistencies):\n{listing}',
    )


def test_citation_reads_the_records_own_fields(records):
  linnaeus = records.sources['1758_linnaeus']
  assert linnaeus.citation_fields == {
    'title': 'Regnum Animalia',
    'book': 'systema-naturae-10th-ed',
    'volume': 1,
  }
  assert citation(linnaeus)['title'] == 'Regnum Animalia'
  # A source with no title of its own cites none; the book is where it is.
  untitled = citation(records.sources['1741_linnaeus'])
  assert untitled['title'] is None and untitled['in']


def test_merge_patch_follows_rfc_7396():
  target = {'a': 'b', 'c': {'d': 'e', 'f': 'g'}}
  assert merge_patch(target, {'a': 'z', 'c': {'f': None}}) == {'a': 'z', 'c': {'d': 'e'}}
  assert merge_patch({'a': [1, 2]}, {'a': {'x': 1}}) == {'a': {'x': 1}}
  assert merge_patch({'a': 1}, 'text') == 'text'
  assert merge_patch(None, {'a': None, 'b': 2}) == {'b': 2}
  assert target == {'a': 'b', 'c': {'d': 'e', 'f': 'g'}}


def test_corrected_node_applies_the_editorial_corrections():
  data = {
    'taxon': 'isorophida',
    'authority': {'auth': ['bell.b.m'], 'year': 1974},
    'citedAs': 'Bell, 1974',
    'editorial': {
      'corrections': {'authority': {'auth': None, 'year': None, 'source': '1976_bell.b.m'}},
      'basis': 'cited before publication',
    },
  }
  assert corrected_node(data) == {
    'taxon': 'isorophida',
    'citedAs': 'Bell, 1974',
    'authority': {'source': '1976_bell.b.m'},
  }
  assert corrected_node({'taxon': 'x', 'editorial': {'inferred': True, 'basis': 'b'}}) is None
  # A null with nothing to put in its place: the printed field is dropped.
  dropped = corrected_node(
    {'taxon': 'x', 'pages': 12, 'editorial': {'corrections': {'pages': None}, 'basis': 'b'}}
  )
  assert dropped == {'taxon': 'x'}


def test_corrections_reach_the_claims(claims):
  # Bell 1975 cites "Bell, 1974" for the paper that appeared in 1976: the
  # usage stays as printed, names its erroneous fields, and carries the
  # attribution the editor reads instead.
  by_id = {c['id']: c for c in claims['1975_bell.b.m']}
  usage = by_id['1975_bell.b.m:0/children/0:usage']
  assert usage['printed'] == {'auth': ['bell.b.m'], 'year': 1974, 'citedAs': 'Bell, 1974'}
  assert usage['printedErrors'] == ['auth', 'year']
  assert usage['corrected'] == {
    'printed': {'citedAs': 'Bell, 1974'},
    'citesSource': '1976_bell.b.m',
  }
  assert 'erroneous' not in usage
  note = by_id['1975_bell.b.m:0/children/0:editorial']
  assert 'errors' not in note
  assert note['corrections'] == {
    'authority': {'auth': None, 'year': None, 'source': '1976_bell.b.m'}
  }


def test_manifest_carries_author_surnames(records, claims, roots):
  authors = manifest(records, claims, roots)['authors']
  assert authors['bell.b.m'] == 'Bell' and authors['bather'] == 'Bather'


def test_change_node_acts(claims):
  # A `translated` node names the taxon at the earlier rank; the node itself
  # is the earlier state as cited, so it emits its usage on its own axis.
  transl = next(
    c
    for c in claims['1994_guensburg_sprinkle']
    if c.get('actKind') == 'nomTransl' and c['subject'] == 'rhenopyrginae'
  )
  assert transl['translatedFrom'] == 'rhenopyrgidae'
  assert 'modifier' not in transl and 'altRankOf' not in transl
  earlier = next(
    c
    for c in claims['1994_guensburg_sprinkle']
    if c['kind'] == 'usage' and c['path'] == transl['path'] + '/translated'
  )
  assert earlier['axis'] == 'translated' and earlier['subject'] == 'rhenopyrgidae'
  # An act the source follows rather than performs names the work.
  parsley = next(c for c in claims['1982c_parsley'] if c.get('actKind') == 'nomTransl')
  assert parsley['by'] == '1968b_paul.c.r.c' and 'translatedFrom' not in parsley
  # A nomen nudum is an act on the synonymy entry that cites the nude usage.
  nudum = [c for c in claims['2005_frest'] if c.get('actKind') == 'nomNudum']
  assert len(nudum) == 3 and all('/synonyms/' in c['path'] for c in nudum)


def test_rank_variants_of_a_hub_are_the_records_linked_to_it(corpus):
  # Diploporita as an order and as a suborder are each `altRankOf` the class.
  assert rank_variants(corpus.records, 'diploporita-class') == [
    'diploporita-order',
    'diploporita-suborder',
  ]


@pytest.mark.parametrize('axis', ['translated', 'corrected', 'substituted', 'moved', 'removed'])
def test_earlier_state_entries_are_cited(records, caplog, axis):
  # The node under a change is the earlier state of the name as this
  # source cites it: as on a synonymy entry, the pages and illustrations in
  # its `authority` locate that earlier use, never this source's own page or
  # figure.
  illustrations = [{'page': 13, 'figures': ['1']}]
  earlier = {
    'taxon': 'rhenopyrgidae',
    'authority': {'pages': 12, 'illustrations': illustrations},
    # The cited work's own material is not this source's: none of the four
    # material fields on a cited entry emits a claim.
    'material': [{'prefix': 'GSC', 'numbers': [1]}],
    'horizons': {'somewhere': {'unit': ['Some Formation']}},
    'occurrences': [{'horizon': 'somewhere'}],
    'ranges': [{'series': 'Ordovician'}],
  }
  child = {'taxon': 'rhenopyrgus', axis: [earlier] if axis == 'removed' else earlier}
  root = Tree(
    {'taxon': 'cyathocystidae', 'pages': 100, 'children': [child]},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 99},
    corpus=records,
  )
  claims = extract(records, {'1961_dehm': [root]})['1961_dehm']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  cited = [c for c in claims if f'/{axis}' in c['path']]
  assert cited and not [c for c in cited if c['kind'] == 'material']
  for claim in cited:
    assert 'pages' not in claim
    assert claim['citedPages'] == 12 and claim['citedIllustrations'] == illustrations


def test_lapsus_is_the_slip_not_a_synonym(records, caplog):
  # The intended name stands in the tree and the name printed by a slip of
  # the pen hangs under `lapsus`: the intended name's node names the slip,
  # and the slip is used as printed here but neither accepted as a synonym
  # nor claimed as new, though its place is its protologue.
  child = {
    'taxon': 'ottawaensis_whiteaves_1897',
    'lapsus': {'taxon': 'canadensis_billings_1866', 'pages': 13},
  }
  root = Tree(
    {'taxon': 'astrocystites', 'pages': 100, 'children': [child]},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 98},
    corpus=records,
  )
  claims = extract(records, {'1961_dehm': [root]})['1961_dehm']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  by_path = collections.defaultdict(list)
  for claim in claims:
    by_path[claim['path']].append(claim)
  act = next(c for c in by_path['98/children/0'] if c['kind'] == 'act')
  assert act['actKind'] == 'lapsus' and act['lapsusAs'] == 'canadensis_billings_1866'
  [slip] = by_path['98/children/0/lapsus']
  assert slip['kind'] == 'usage' and slip['axis'] == 'lapsus'
  # The slip is printed in this source: its pages are the source's own.
  assert slip['pages'] == 13 and 'citedPages' not in slip
  protologues = support.with_documents(records, roots={'1961_dehm': [root]}).protologue_sources()
  assert '1961_dehm' in protologues.get('canadensis_billings_1866', ())


def test_lapsus_listed_in_a_synonymy(claims):
  # Bather 1914 notes Whiteaves's slip: the entry names the record the
  # slip was printed for, and is accepted under it without being a synonym.
  [entry] = [
    c
    for c in claims['1914c_bather']
    if c['kind'] == 'acceptance' and c['subject'] == 'canadensis_whiteaves_1898'
  ]
  assert entry['lapsusFor'] == 'ottawaensis_whiteaves_1897'
  assert entry['parents'] == ['steganoblastus'] and entry['citedPages'] == 395


def test_lapsus_records_stay_under_lapsus(records, caplog):
  # A lapsus record appears under `lapsus`, or as a synonymy entry marked
  # `lapsusFor`; anywhere else, and a `lapsusFor` off a synonymy entry, is
  # an error.
  from phylohist.loader.load import _report_lapsus_records

  slip = {'taxon': 'canadensis_billings_1866'}
  printed = Tree(
    {
      'taxon': 'astrocystites',
      'children': [{'taxon': 'ottawaensis_whiteaves_1897', 'lapsus': slip}],
    },
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 97},
    corpus=records,
  )
  listed = {
    'taxon': 'ottawaensis_whiteaves_1897',
    'synonyms': [dict(slip, lapsusFor={'taxon': 'ottawaensis_whiteaves_1897'})],
  }
  placed = Tree(
    {'taxon': 'astrocystites', 'children': [dict(slip), listed]},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 96},
    corpus=records,
  )
  caplog.clear()
  _report_lapsus_records(support.with_documents(records, roots={'1961_dehm': [printed, placed]}))
  errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
  assert len(errors) == 1 and '[96]/astrocystites/0/canadensis_billings_1866' in errors[0]

  caplog.clear()
  Tree(
    {'taxon': 'astrocystites', 'lapsusFor': {'taxon': 'ottawaensis_whiteaves_1897'}},
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 95},
    corpus=records,
  )
  errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
  assert len(errors) == 1 and 'is not a `synonyms` or `non` entry' in errors[0]


def test_recombined_is_the_printed_new_combination(records, caplog):
  # "comb. nov.": the act on the species, beside the move out of the genus
  # it leaves; followed from another work, it names that work.
  child = {
    'taxon': 'grayae_bather_1915',
    'recombined': True,
    'moved': {'taxon': 'pyrgocystis'},
  }
  followed = {
    'taxon': 'coronaeformis_rievers_1961',
    'recombined': {'by': {'source': '1983_holloway_jell', 'pages': 12}},
  }
  root = Tree(
    {'taxon': 'rhenopyrgus', 'children': [child, followed]},
    {'source_key': '1985_jell_burrett_banks', 'type': 'taxonomy', 'position': 94},
    corpus=records,
  )
  claims = extract(records, {'1985_jell_burrett_banks': [root]})['1985_jell_burrett_banks']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  at = collections.defaultdict(list)
  for claim in claims:
    at[claim['path']].append(claim)
  kinds = {(c['kind'], c.get('actKind')) for c in at['94/children/0']}
  assert {('act', 'combNov'), ('act', 'moved'), ('rejection', None)} <= kinds
  [act] = [c for c in at['94/children/1'] if c.get('actKind') == 'combNov']
  assert act['by'] == '1983_holloway_jell' and act['byPages'] == 12

  caplog.clear()
  Tree(
    {'taxon': 'rhenopyrgus', 'recombined': True},
    {'source_key': '1985_jell_burrett_banks', 'type': 'taxonomy', 'position': 93},
    corpus=records,
  )
  errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
  assert len(errors) == 1 and 'is not a species-group name' in errors[0]


def test_emended_by_lists_the_emendations_followed(records, caplog):
  # "Emended Paul, 1972b, and herein": each emendation the source follows
  # names its work, in printed order, before the source's own.
  root = Tree(
    {
      'taxon': 'rhenopyrgus',
      'emended': True,
      'emendedBy': [{'source': '1968b_paul.c.r.c', 'pages': 700}, {'source': '1983_holloway_jell'}],
    },
    {'source_key': '1985_jell_burrett_banks', 'type': 'taxonomy', 'position': 92},
    corpus=records,
  )
  claims = extract(records, {'1985_jell_burrett_banks': [root]})['1985_jell_burrett_banks']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  acts = [c for c in claims if c.get('actKind') == 'emended']
  assert [(a.get('by'), a.get('byPages')) for a in acts] == [
    ('1968b_paul.c.r.c', 700),
    ('1983_holloway_jell', None),
    (None, None),
  ]

  schema = support.schema()[io.TREE_DEF]
  followed = {'taxon': 'rhenopyrgus', 'emendedBy': [{'source': '1968b_paul.c.r.c'}]}
  assert schema.check({'taxonomies': [followed]})
  # The object form is gone; an emendation followed is an `emendedBy` entry.
  assert not schema.check(
    {'taxonomies': [{'taxon': 'rhenopyrgus', 'emended': {'by': {'source': '1968b_paul.c.r.c'}}}]}
  )
  assert not schema.check({'taxonomies': [{'taxon': 'rhenopyrgus', 'emendedBy': []}]})


def test_restricted_by_lists_the_restrictions_followed(records, caplog):
  # A restriction is its own act beside an emendation: each restriction
  # the source follows names its work, in printed order, before its own.
  root = Tree(
    {
      'taxon': 'rhenopyrgus',
      'emended': True,
      'restricted': True,
      'restrictedBy': [
        {'source': '1968b_paul.c.r.c', 'pages': 700},
        {'source': '1983_holloway_jell'},
      ],
    },
    {'source_key': '1985_jell_burrett_banks', 'type': 'taxonomy', 'position': 92},
    corpus=records,
  )
  claims = extract(records, {'1985_jell_burrett_banks': [root]})['1985_jell_burrett_banks']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  acts = [(c['actKind'], c.get('by'), c.get('byPages')) for c in claims if c['kind'] == 'act']
  assert acts == [
    ('emended', None, None),
    ('restricted', '1968b_paul.c.r.c', 700),
    ('restricted', '1983_holloway_jell', None),
    ('restricted', None, None),
  ]

  schema = support.schema()[io.TREE_DEF]
  followed = {'taxon': 'rhenopyrgus', 'restrictedBy': [{'source': '1968b_paul.c.r.c'}]}
  assert schema.check({'taxonomies': [followed]})
  assert not schema.check(
    {'taxonomies': [{'taxon': 'rhenopyrgus', 'restricted': {'by': {'source': '1968b_paul.c.r.c'}}}]}
  )
  assert not schema.check({'taxonomies': [{'taxon': 'rhenopyrgus', 'restrictedBy': []}]})


def test_material_adapter(records, caplog):
  # Occurrences, material, illustrations, ranges, in that fixed order, over a
  # node with a file horizon and locality, a node horizon stated as an
  # occurrence, a numbered entry, a range pair, a label-only entry, an
  # explicit repository, a prefix the file's map gives a register, an entry
  # with a tentative locality, tied and untied illustrations, and two
  # ranges.
  file_horizons = {'trenton': {'unit': ['Trenton Limestone']}}
  file_localities = {'division-st': {'location': ['Division Street, Ottawa']}}
  node_data = {
    'taxon': 'rhenopyrgus',
    'horizons': {'quarry-x': {'unit': ['Quarry X Beds']}},
    'occurrences': [{'horizon': 'quarry-x'}],
    'material': [
      {
        'prefix': 'GSC',
        'numbers': [752],
        'role': 'lectotype',
        'horizon': 'trenton',
        'locality': 'division-st',
      },
      {'prefix': 'GSC', 'numbers': [[100, 105]], 'role': 'paratype', 'formerIds': ['G 1']},
      {'label': 'the specimen lent to Hudson', 'role': 'syntype', 'status': 'lost'},
      {'numbers': ['XYZ 1'], 'repository': 'nhmuk', 'notes': 'lent'},
      {'prefix': 'PE', 'numbers': [7], 'preparation': 'latex cast', 'castOf': 752},
      {
        'prefix': 'GSC',
        'numbers': [900],
        'horizon': 'trenton',
        'locality': 'division-st',
        'tentative': ['locality'],
        'role': 'hypotype',
      },
      {
        'prefix': 'GSC',
        'numbers': [901],
        'role': 'syntype',
        'editorial': {'inferred': ['role'], 'basis': 'Only "the type" is printed.'},
      },
    ],
    'illustrations': [
      {'textFigures': [3], 'of': 752},
      {
        'plate': 1,
        'figures': [2],
        'of': [100, 'the specimen lent to Hudson'],
        'depicts': 'cast',
      },
      {'plate': 2, 'uncertain': True},
    ],
    'ranges': [
      {
        'series': 'Middle Ordovician',
        'regions': ['Ottawa', {'value': 'Quebec', 'tentative': True}],
      },
      {'period': 'Devonian', 'regions': ['Germany']},
    ],
  }
  root = Tree(
    node_data,
    {
      'source_key': '1961_dehm',
      'type': 'taxonomy',
      'position': 90,
      'file_horizons': file_horizons,
      'file_localities': file_localities,
      'file_unused': (),
      'file_prefixes': {'GSC': 'gsc', 'PE': 'fmnh-pe'},
    },
    corpus=records,
  )
  claims = extract(records, {'1961_dehm': [root]})['1961_dehm']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  material = [c for c in claims if c['kind'] == 'material']

  # The fixed order fixes the ids.
  kinds = [c['materialKind'] for c in material]
  assert kinds == ['occurrence'] * 2 + ['specimen'] * 7 + ['illustration'] * 3 + ['range'] * 2
  assert [c['id'] for c in material] == [f'1961_dehm:90:material:{n}' for n in range(len(material))]
  assert [
    c['id'] for c in extract(records, {'1961_dehm': [root]})['1961_dehm'] if c['kind'] == 'material'
  ] == [c['id'] for c in material]

  # The node's own stated occurrence first, then the pairing its entries
  # name, once for the two entries that name it: a file horizon and locality
  # each carry the scope they were read from.
  node_occ, file_occ = material[:2]
  assert node_occ['horizonKey'] == 'quarry-x' and node_occ['horizonScope'] == 'node'
  assert node_occ['occurrence'] == {'horizon': node_data['horizons']['quarry-x']}
  assert 'localityKey' not in node_occ and 'localityScope' not in node_occ
  assert file_occ['horizonKey'] == 'trenton' and file_occ['horizonScope'] == 'file'
  assert file_occ['localityKey'] == 'division-st' and file_occ['localityScope'] == 'file'
  assert file_occ['occurrence'] == {
    'horizon': file_horizons['trenton'],
    'locality': file_localities['division-st'],
  }

  numbered, pair, label_only, explicit, file_listed, tentative, inferred = material[2:9]

  assert numbered['role'] == 'lectotype' and numbered['ids'] == ['GSC 752']
  assert numbered['numbers'] == [752]
  assert numbered['horizonKey'] == 'trenton' and numbered['localityKey'] == 'division-st'
  assert 'tentativeFields' not in numbered
  assert numbered['repository'] == 'gsc' and numbered['repositoryVia'] == 'file'
  assert numbered['joinKeys'] == ['gsc:752'] and 'rangeJoin' not in numbered
  assert 'roleAct' not in numbered  # not a protologue node

  assert pair['ids'] == [['GSC 100', 'GSC 105']] and pair['formerIds'] == ['G 1']
  assert pair['joinKeys'] == ['gsc:100', 'gsc:105'] and pair['rangeJoin'] is True

  assert label_only['label'] == 'the specimen lent to Hudson' and label_only['status'] == 'lost'
  assert label_only['ids'] == [] and label_only['repository'] is None
  assert 'joinKeys' not in label_only and 'repositoryVia' not in label_only

  assert explicit['ids'] == ['XYZ 1']
  assert explicit['repository'] == 'nhmuk' and explicit['repositoryVia'] == 'explicit'
  assert explicit['joinKeys'] == ['nhmuk:xyz1'] and explicit['materialNotes'] == 'lent'
  assert 'role' not in explicit

  # `PE` belongs to two registry entries; the file's map settles it.
  assert file_listed['repository'] == 'fmnh-pe' and file_listed['repositoryVia'] == 'file'
  assert file_listed['preparation'] == 'latex cast' and file_listed['castOf'] == 752

  assert tentative['localityKey'] == 'division-st' and tentative['tentativeFields'] == ['locality']

  # The claim is about the entry: its editorial block, not the node's.
  assert inferred['editorial'] == node_data['material'][6]['editorial']
  assert inferred['inferredFields'] == ['role']

  tied, list_tied, untied = material[9:12]
  assert tied['illustration'] == {'textFigures': [3]} and tied['of'] == 752
  assert tied['ofClaim'] == [numbered['id']]
  assert list_tied['of'] == [100, 'the specimen lent to Hudson']
  assert list_tied['depicts'] == 'cast' and 'depicts' not in tied
  assert list_tied['illustration'] == {'plate': 1, 'figures': [2]}
  assert list_tied['ofClaim'] == [pair['id'], label_only['id']]
  assert numbered['illustrationClaims'] == [tied['id']]
  assert numbered['specimenIllustrations'] == [tied['illustration']]
  assert pair['illustrationClaims'] == [list_tied['id']]
  assert untied['illustration'] == {'plate': 2, 'uncertain': True}
  assert 'ofClaim' not in untied and 'illustrationClaims' not in explicit

  first, second = material[12:14]
  assert first['range'] == node_data['ranges'][0] and second['range'] == node_data['ranges'][1]

  # A protologue node: the entry's own `roleAct` wins, else a holotype,
  # paratype, syntype or cotype is this source's designation, and any
  # other role derives none. An open-nomenclature record sidesteps the
  # protologue-source check a named one would need.
  new_node = Tree(
    {
      'openTaxon': 'rhenopyrgus-sp-1_ewin_martin.m_isotalo_zamora_2020',
      'new': True,
      'material': [
        {'count': 5, 'role': 'paratype', 'roleAct': 'reported'},
        {'prefix': 'GSC', 'numbers': [1], 'role': 'holotype'},
        {'prefix': 'GSC', 'numbers': [2], 'role': 'cotype'},
        {'prefix': 'GSC', 'numbers': [3], 'role': 'hypotype'},
        {'prefix': 'GSC', 'numbers': [4]},
      ],
    },
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 91},
    corpus=records,
  )
  new_claims = [
    c for c in extract(records, {'1961_dehm': [new_node]})['1961_dehm'] if c['kind'] == 'material'
  ]
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  assert [c.get('roleAct') for c in new_claims] == [
    'reported',
    'designated',
    'designated',
    None,
    None,
  ]
  assert new_claims[0]['count'] == 5


def _numbered(records, entries, prefixes=None, locality_register=None, **node):
  """The specimen claims of a node whose tree file carries a `prefixes` map
  (and a `localityRegister`)."""
  root = Tree(
    {'taxon': 'rhenopyrgus', 'material': entries, **node},
    {
      'source_key': '1961_dehm',
      'type': 'taxonomy',
      'position': 90,
      'file_prefixes': prefixes or {},
      'file_locality_register': locality_register,
    },
    corpus=records,
  )
  claims = extract(records, {'1961_dehm': [root]})['1961_dehm']
  return [c for c in claims if c.get('materialKind') == 'specimen']


def test_a_prefix_and_numbers_entry_carries_its_fields_and_display_ids(records):
  [claim] = _numbered(
    records,
    [{'prefix': 'MCZ', 'numbers': ['581A', 581], 'asPrinted': 'MCZ 581A, 581', 'role': 'holotype'}],
    {'MCZ': 'mcz'},
  )
  assert (claim['prefix'], claim['numbers'], claim['asPrinted']) == (
    'MCZ',
    ['581A', 581],
    'MCZ 581A, 581',
  )
  assert claim['ids'] == ['MCZ 581A', 'MCZ 581']
  assert claim['repository'] == 'mcz' and claim['repositoryVia'] == 'file'
  assert claim['joinKeys'] == ['mcz:581a', 'mcz:581']
  assert 'rangeJoin' not in claim


def test_two_printed_prefixes_of_one_register_share_a_join_key(records):
  first, second = _numbered(
    records,
    [{'prefix': 'F.', 'numbers': [5404]}, {'prefix': 'UQF', 'numbers': ['5404']}],
    {'F.': 'uq-f', 'UQF': 'uq-f'},
  )
  assert first['joinKeys'] == second['joinKeys'] == ['uq-f:5404']
  assert (first['ids'], second['ids']) == (['F. 5404'], ['UQF 5404'])


def test_a_range_pair_gives_both_ends_and_stays_a_pair_in_ids(records):
  [claim] = _numbered(
    records,
    [{'prefix': 'GSC', 'numbers': [[25935, 25961], 'A-1'], 'asPrinted': 'GSC 25935–25961'}],
    {'GSC': 'gsc'},
  )
  assert claim['ids'] == [['GSC 25935', 'GSC 25961'], 'GSC A-1']
  assert claim['joinKeys'] == ['gsc:25935', 'gsc:25961', 'gsc:a1']
  assert claim['rangeJoin'] is True and claim['asPrinted'] == 'GSC 25935–25961'
  assert claim['numbers'] == [[25935, 25961], 'A-1']


def test_an_explicit_repository_within_the_prefixs_register_keys_under_the_register(records):
  [specimen] = _numbered(
    records,
    [{'prefix': 'USNM', 'numbers': [165421], 'repository': 'usnm-walcott'}],
    {'USNM': 'usnm'},
  )
  assert specimen['repository'] == 'usnm-walcott' and specimen['repositoryVia'] == 'explicit'
  assert specimen['joinKeys'] == ['usnm:165421']
  # The register itself is within itself.
  [same] = _numbered(
    records, [{'prefix': 'USNM', 'numbers': [1], 'repository': 'usnm'}], {'USNM': 'usnm'}
  )
  assert same['joinKeys'] == ['usnm:1']


def test_an_explicit_repository_outside_the_prefixs_register_wins(records):
  [specimen] = _numbered(
    records, [{'prefix': 'MCZ', 'numbers': [690], 'repository': 'usnm-walcott'}], {'MCZ': 'mcz'}
  )
  assert specimen['repository'] == 'usnm-walcott' and specimen['repositoryVia'] == 'explicit'
  assert specimen['joinKeys'] == ['usnm-walcott:690']
  # A collection above the register is not within it either.
  [above] = _numbered(
    records, [{'prefix': 'USNM', 'numbers': [1], 'repository': 'usnm'}], {'USNM': 'usnm-walcott'}
  )
  assert above['joinKeys'] == ['usnm:1']


def test_numbers_with_no_prefix_key_under_the_repository_or_not_at_all(records):
  repo, holder, nothing = _numbered(
    records,
    [
      {'repository': 'u-cincinnati-caster', 'numbers': ['KR-2']},
      {'holder': 'A. R. Palmer', 'numbers': [[500, 501]]},
      {'prefix': 'ZZ', 'numbers': [1]},
    ],
    {'MCZ': 'mcz'},
  )
  assert repo['ids'] == ['KR-2'] and repo['repository'] == 'u-cincinnati-caster'
  assert repo['repositoryVia'] == 'explicit' and repo['joinKeys'] == ['u-cincinnati-caster:kr2']
  assert holder['ids'] == [['500', '501']] and holder['holder'] == 'A. R. Palmer'
  assert holder['repository'] is None and 'repositoryVia' not in holder
  assert 'joinKeys' not in holder and holder['rangeJoin'] is True
  # A prefix the file's map lacks (an error for the loader) keys nothing.
  assert nothing['repository'] is None and 'joinKeys' not in nothing
  assert nothing['ids'] == ['ZZ 1']


def test_a_figure_names_a_prefix_and_numbers_entry_by_a_number(records):
  [claim] = _numbered(
    records,
    [{'prefix': 'MCZ', 'numbers': [581, ['600', '610']]}],
    {'MCZ': 'mcz'},
    illustrations=[{'plate': 1, 'of': 581}, {'plate': 2, 'of': 605}, {'plate': 3, 'of': 'x'}],
  )
  assert [f['plate'] for f in claim['specimenIllustrations']] == [1, 2]


def test_locality_keys_on_specimen_claims(records):
  entries = [
    {
      'prefix': 'GK',
      'numbers': [1731],
      'locality': 'miaobanpo',
      'localityNumbers': [
        {'prefix': 'GTBM', 'number': '9-1-526a'},
        {'register': 'usgs-l', 'number': '4148 CO'},
        {'number': 'FC-1'},
        {'prefix': 'ZZ', 'number': 9},
      ],
    },
    {'prefix': 'GK', 'numbers': [1732], 'locality': 'miaobanpo'},
  ]
  prefixes = {'GK': 'mcz', 'GTBM': 'usgs-l'}
  with_default, without = _numbered(
    records, entries, prefixes, 'sprinkle-l', localities={'miaobanpo': {'location': ['Kaili']}}
  )
  assert with_default['localityKeys'] == ['usgs-l:91526a', 'usgs-l:4148co', 'sprinkle-l:fc1']
  assert with_default['localityNumbers'] == entries[0]['localityNumbers']
  assert 'localityKeys' not in without and 'localityNumbers' not in without
  # Without a file `localityRegister` the bare number keys nothing.
  [claim, _] = _numbered(
    records, entries, prefixes, localities={'miaobanpo': {'location': ['Kaili']}}
  )
  assert claim['localityKeys'] == ['usgs-l:91526a', 'usgs-l:4148co']


def test_an_object_of_names_one_specimen_by_prefix_or_label(records):
  gk, gtb, slab = _numbered(
    records,
    [
      {'prefix': 'GK', 'numbers': [112]},
      {'prefix': 'GTB', 'numbers': [112]},
      {'label': 'the slab'},
    ],
    {'GK': 'mcz', 'GTB': 'gsc'},
    illustrations=[
      {'plate': 1, 'of': {'number': 112, 'prefix': 'GK'}},
      {'plate': 2, 'of': [{'number': '112', 'prefix': 'GTB'}, {'label': 'the slab'}]},
      {'plate': 3, 'of': 112},
    ],
  )
  assert [f['plate'] for f in gk['specimenIllustrations']] == [1, 3]
  assert [f['plate'] for f in gtb['specimenIllustrations']] == [2, 3]
  assert [f['plate'] for f in slab['specimenIllustrations']] == [2]
  assert (
    len(gk['illustrationClaims']) == 2
    and gk['illustrationClaims'][0] != gtb['illustrationClaims'][0]
  )


def _locality(records, locality, prefixes=None, locality_register=None):
  root = Tree(
    {'taxon': 'rhenopyrgus', 'localities': {'x': locality}, 'occurrences': [{'locality': 'x'}]},
    {
      'source_key': '1961_dehm',
      'type': 'taxonomy',
      'position': 90,
      'file_prefixes': prefixes or {},
      'file_locality_register': locality_register,
    },
    corpus=records,
  )
  claims = extract(records, {'1961_dehm': [root]})['1961_dehm']
  [claim] = [c for c in claims if c.get('materialKind') == 'occurrence']
  return claim


def test_locality_keys_of_object_numbers(records):
  locality = {
    'localityNumbers': [
      {'number': 'FC-1'},
      {'prefix': 'USGS', 'number': '4148 CO'},
      {'register': 'usnm-l', 'number': '35k'},
      {'prefix': 'Walcott', 'number': 35},
      {'register': 'usgs-l', 'number': 'D190d CO'},
      {'prefix': 'USGS', 'number': 5462},
      {'prefix': 'ZZ', 'number': 9},
    ]
  }
  prefixes = {'USGS': 'usgs-l', 'Walcott': 'usnm-l'}
  claim = _locality(records, locality, prefixes, 'sprinkle-l')
  assert claim['localityKeys'] == [
    'sprinkle-l:fc1',
    'usgs-l:4148co',
    'usnm-l:35k',
    'usnm-l:35',
    'usgs-l:d190dco',
    'usgs-l:5462',
  ]
  # With no `localityRegister` a number with neither prefix nor register is skipped;
  # a prefix the map lacks never falls to it.
  assert _locality(records, locality, prefixes)['localityKeys'] == [
    'usgs-l:4148co',
    'usnm-l:35k',
    'usnm-l:35',
    'usgs-l:d190dco',
    'usgs-l:5462',
  ]
  # Two printed forms of one number give one key.
  both = {
    'localityNumbers': [
      {'prefix': 'USGS', 'number': '4148 CO'},
      {'register': 'usgs-l', 'number': '4148 co'},
    ]
  }
  assert _locality(records, both, prefixes)['localityKeys'] == ['usgs-l:4148co']
  # A locality with no locality numbers has no field.
  assert 'localityKeys' not in _locality(
    records, {'location': ['Wheeler Quarry']}, prefixes, 'sprinkle-l'
  )
  assert 'localityKeys' not in _locality(
    records, {'localityNumbers': [{'number': 'SH-1'}]}, prefixes
  )


def test_a_specimen_is_followed_across_sources_by_its_join_key(claims):
  # Whitehouse 1941's "F. 5404" and Jell & Sprinkle 2021's "UQF5404".
  keys = {}
  for source in ('1941_whitehouse', '2021_jell_sprinkle'):
    [holotype] = [
      c
      for c in claims[source]
      if c['kind'] == 'material'
      and c['materialKind'] == 'specimen'
      and c['subject'] == 'navicula_whitehouse_1941'
      and c.get('role') == 'holotype'
    ]
    keys[source] = holotype['joinKeys']
  assert keys['1941_whitehouse'] == keys['2021_jell_sprinkle'] == ['uq-f:5404']


def test_derived_coverage(records):
  base = {'source_key': '1961_dehm', 'type': 'taxonomy'}

  def tree(data, position, file_unused=()):
    return Tree(data, {**base, 'position': position, 'file_unused': file_unused}, corpus=records)

  def derived(root, kind='material'):
    return derived_coverage({'s': [root]})['s'][kind]

  child = {'taxon': 'grayae_bather_1915'}
  other = {'taxon': 'sardesoni_bather_1915'}
  cases = [
    # `na`: the file lists the field as unused, whatever the nodes say.
    ('na', tree({'taxon': 'rhenopyrgus'}, 0, file_unused=('material',))),
    # A species null and no species lacks the field: `all`. The genus has
    # no `material` and is not counted.
    (
      'all',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'children': [{**child, 'material': [{'label': 'A'}]}, {**other, 'material': None}],
        },
        1,
      ),
    ),
    # A species null and another species lacks it: `partly`.
    (
      'partly',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'children': [{**child, 'material': None}, other],
        },
        2,
      ),
    ),
    # `all` downgraded by an entry that is not list-complete, read from
    # every named node.
    (
      'partly',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'material': [{'label': 'A', 'listComplete': False}],
          'children': [{**child, 'material': None}],
        },
        3,
      ),
    ),
    # Values alone declare nothing: a value says what the source prints,
    # not that the file was audited for the field.
    (None, tree({'taxon': 'rhenopyrgus', 'material': [{'label': 'A'}], 'children': [child]}, 4)),
    (None, tree({'taxon': 'rhenopyrgus'}, 5)),
    # A cited entry never counts, whatever it carries or lacks.
    (
      'all',
      tree(
        {
          'taxon': 'rhenopyrgus',
          'children': [{**child, 'material': None}],
          'synonyms': [other],
        },
        6,
      ),
    ),
    # A null on a genus is not counted: specimens are cited for species.
    (
      None,
      tree(
        {
          'taxon': 'rhenopyrgus',
          'material': None,
          'children': [
            {**child, 'material': [{'label': 'A'}]},
            {**other, 'material': [{'label': 'B'}]},
          ],
        },
        11,
      ),
    ),
  ]
  for expected, root in cases:
    assert derived(root) == expected, (expected, root.data)

  # `occurrences` reads `occurrences` or `ranges`; `na` needs both unused.
  occ = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'occurrences': None}],
    },
    7,
  )
  assert derived(occ, 'occurrences') == 'all'
  only_one = tree({'taxon': 'rhenopyrgus'}, 8, file_unused=('ranges',))
  assert derived(only_one, 'occurrences') is None
  both = tree({'taxon': 'rhenopyrgus'}, 9, file_unused=('ranges', 'occurrences'))
  assert derived(both, 'occurrences') == 'na'

  # `illustrations` reads the `illustrations` field.
  ill = tree({'taxon': 'rhenopyrgus', 'children': [{**child, 'illustrations': None}]}, 10)
  assert derived(ill, 'illustrations') == 'all'

  # Like `material`, `illustrations` counts species-level nodes only: a
  # genus without the field is not an uncaptured one, so a species value
  # and a species null are `all`.
  ill_genus = tree(
    {
      'taxon': 'rhenopyrgus',
      'children': [
        {**child, 'illustrations': [{'plate': 1}]},
        {**other, 'illustrations': None},
      ],
    },
    12,
  )
  assert derived(ill_genus, 'illustrations') == 'all'
  # A species lacking the field still makes it `partly`.
  ill_species = tree(
    {'taxon': 'rhenopyrgus', 'children': [{**child, 'illustrations': None}, other]}, 13
  )
  assert derived(ill_species, 'illustrations') == 'partly'
  # A figure on a genus is a value, not a null: it does not declare.
  ill_on_genus = tree({'taxon': 'rhenopyrgus', 'illustrations': [{'plate': 1}]}, 14)
  assert derived(ill_on_genus, 'illustrations') is None

  # `occurrences` is captured through a material entry's `horizon` or
  # `locality`: a species with no `occurrences`/`ranges` but a linked entry
  # counts as present, beside a species whose `ranges` is null.
  linked = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [
        {**child, 'material': [{'label': 'A', 'horizon': 'x'}]},
        {**other, 'ranges': None},
      ],
    },
    15,
  )
  assert derived(linked, 'occurrences') == 'all'
  # A locality alone links as well.
  by_locality = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [
        {**child, 'material': [{'label': 'A', 'locality': 'x'}]},
        {**other, 'ranges': None},
      ],
    },
    21,
  )
  assert derived(by_locality, 'occurrences') == 'all'
  # Without the link the same species is an uncaptured field.
  unlinked = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'material': [{'label': 'A'}]}, {**other, 'ranges': None}],
    },
    16,
  )
  assert derived(unlinked, 'occurrences') == 'partly'
  # A linked node that also writes a null is present and still declares.
  linked_null = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'material': [{'label': 'A', 'horizon': 'x'}], 'occurrences': None}],
    },
    17,
  )
  assert derived(linked_null, 'occurrences') == 'all'
  linked_only = tree(
    {
      'taxon': 'rhenopyrgus',
      'ranges': [{'series': 'Ordovician'}],
      'children': [{**child, 'material': [{'label': 'A', 'horizon': 'x'}]}],
    },
    18,
  )
  assert derived(linked_only, 'occurrences') is None

  # Only taxonomy trees are counted: a cladogram's nodes print no material,
  # so a root of that type contributes none and cannot make a kind `partly`.
  taxonomy = tree({'taxon': 'rhenopyrgus', 'children': [{**child, 'material': None}]}, 19)
  cladogram = Tree(
    {'taxon': 'rhenopyrgus', 'children': [other]},
    {**base, 'type': 'cladogram', 'position': 20},
    corpus=records,
  )
  assert derived_coverage({'s': [taxonomy, cladogram]})['s']['material'] == 'all'
  assert derived_coverage({'s': [cladogram]})['s']['material'] is None


def test_derived_synonymy_coverage(records):
  base = {'source_key': '1961_dehm', 'type': 'taxonomy'}

  def derived(data, position, file_unused=(), tree_type='taxonomy'):
    root = Tree(
      data,
      {**base, 'type': tree_type, 'position': 100 + position, 'file_unused': file_unused},
      corpus=records,
    )
    return derived_coverage({'s': [root]})['s']['synonymy']

  child = {'taxon': 'grayae_bather_1915'}
  other = {'taxon': 'sardesoni_bather_1915'}
  syn = [{'taxon': 'sardesoni_bather_1915'}]
  # `unused: [synonyms]` is `na`, whatever the nodes say.
  assert derived({'taxon': 'rhenopyrgus'}, 0, file_unused=('synonyms',)) == 'na'
  # A null and values elsewhere, no node lacking both fields: `all`.
  nulled_root = {'taxon': 'rhenopyrgus', 'synonyms': None, 'children': [{**child, 'synonyms': syn}]}
  assert derived(nulled_root, 1) == 'all'
  # A null and a node lacking both fields: `partly` (every rank counts).
  partly_child = {'taxon': 'rhenopyrgus', 'children': [{**child, 'synonyms': None}, other]}
  assert derived(partly_child, 2) == 'partly'
  assert derived({'taxon': 'rhenopyrgus', 'synonyms': None, 'children': [child]}, 3) == 'partly'
  # `non` alone counts as present.
  non_root = {'taxon': 'rhenopyrgus', 'non': syn, 'children': [{**child, 'synonyms': None}]}
  assert derived(non_root, 4) == 'all'
  # Values alone declare nothing.
  assert derived({'taxon': 'rhenopyrgus', 'synonyms': syn, 'children': [child]}, 5) is None
  assert derived({'taxon': 'rhenopyrgus', 'non': syn}, 6) is None
  # A phylogeny root contributes nothing.
  assert derived({'taxon': 'rhenopyrgus', 'synonyms': None}, 7, tree_type='cladogram') is None
  taxonomy = Tree(
    {'taxon': 'rhenopyrgus', 'synonyms': None}, {**base, 'position': 108}, corpus=records
  )
  cladogram = Tree(
    {'taxon': 'rhenopyrgus', 'children': [other]},
    {**base, 'type': 'cladogram', 'position': 109},
    corpus=records,
  )
  assert derived_coverage({'s': [taxonomy, cladogram]})['s']['synonymy'] == 'all'


def test_manifest_synonymy_keeps_the_count_check_unless_a_null_derives_it(records, monkeypatch):
  coverage = records.sources['1961_dehm']._data['audit']['coverage']
  # Declared `all`, no null: nothing derived, and no acceptance claims, so
  # the claim-count check fires.
  monkeypatch.setitem(coverage, 'synonymy', 'all')
  values = {
    '1961_dehm': [
      Tree(
        {'taxon': 'pyrgocystis', 'children': [{'taxon': 'grayae_bather_1915'}]},
        {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 30},
        corpus=records,
      )
    ]
  }
  entry = manifest(records, extract(records, values), values)['sources']['1961_dehm']
  assert entry['derivedCoverage']['synonymy'] is None
  assert entry['coverage']['synonymy'] == 'all'
  assert 'synonymy: declared all, no claims derived' in entry['inconsistencies']

  # A null derives the kind: the derived value wins, and the declaration
  # is compared with it instead of with the claim count.
  nulled = {
    '1961_dehm': [
      Tree(
        {'taxon': 'pyrgocystis', 'synonyms': None, 'children': [{'taxon': 'grayae_bather_1915'}]},
        {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 31},
        corpus=records,
      )
    ]
  }
  entry = manifest(records, extract(records, nulled), nulled)['sources']['1961_dehm']
  assert entry['derivedCoverage']['synonymy'] == 'partly'
  assert entry['coverage']['synonymy'] == 'partly'
  assert (
    'synonymy: declared all but derived from the tree (partly); remove the declaration'
  ) in entry['inconsistencies']
  assert not [r for r in entry['inconsistencies'] if r.startswith('synonymy: declared all, no')]


def test_manifest_reports_derived_disagreement(records, monkeypatch):
  # A declared value that the file's nulls contradict is an inconsistency
  # row naming both, and the effective map carries the derived label.
  audited = Tree(
    {
      'taxon': 'pyrgocystis',
      'children': [
        {'taxon': 'grayae_bather_1915', 'illustrations': None},
        {'taxon': 'sardesoni_bather_1915'},
      ],
    },
    {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 0},
    corpus=records,
  )
  synthetic = {'1961_dehm': [audited]}
  assert derived_coverage(synthetic)['1961_dehm']['illustrations'] == 'partly'
  monkeypatch.setitem(
    records.sources['1961_dehm']._data['audit']['coverage'], 'illustrations', 'none'
  )

  entry = manifest(records, extract(records, synthetic), synthetic)['sources']['1961_dehm']
  assert (
    'illustrations: declared none but derived from the tree (partly); remove the declaration'
  ) in entry['inconsistencies']
  assert entry['coverage']['illustrations'] == 'partly'
  assert entry['derivedCoverage']['illustrations'] == 'partly'

  # Agreeing values still draw the row: the tree gives the kind its
  # coverage, so the declaration is redundant.
  monkeypatch.setitem(
    records.sources['1961_dehm']._data['audit']['coverage'], 'illustrations', 'partly'
  )
  entry = manifest(records, extract(records, synthetic), synthetic)['sources']['1961_dehm']
  assert (
    'illustrations: declared partly but derived from the tree (partly); remove the declaration'
  ) in entry['inconsistencies']
  monkeypatch.setitem(
    records.sources['1961_dehm']._data['audit']['coverage'], 'illustrations', 'none'
  )

  # A value alone derives nothing, so the declaration stands and no row fires.
  values_only = {
    '1961_dehm': [
      Tree(
        {'taxon': 'pyrgocystis', 'illustrations': [{'plate': 1}]},
        {'source_key': '1961_dehm', 'type': 'taxonomy', 'position': 1},
        corpus=records,
      )
    ]
  }
  entry = manifest(records, extract(records, values_only), values_only)['sources']['1961_dehm']
  assert entry['derivedCoverage']['illustrations'] is None
  assert entry['coverage']['illustrations'] == 'none'
  assert not [r for r in entry['inconsistencies'] if r.startswith('illustrations')]


# -- absence claims and `figured: False` --------------------------------------

_BASE = {'source_key': '1961_dehm', 'type': 'taxonomy'}
_SPECIES = 'grayae_bather_1915'
_SISTER = 'sardesoni_bather_1915'


def _claims_of(records, data, position, **metadata):
  root = Tree(data, {**_BASE, 'position': position, **metadata}, corpus=records)
  return extract(records, {'1961_dehm': [root]})['1961_dehm']


def _absences(claims):
  return [(c['absenceOf'], c['fields']) for c in claims if c['kind'] == 'absence']


def test_absence_emission_by_kind(records):
  def absences(node, position, **metadata):
    return _absences(_claims_of(records, {'taxon': _SPECIES, **node}, position, **metadata))

  assert absences({'material': None}, 200) == [('material', ['material'])]
  assert absences({'illustrations': None}, 201) == [('illustrations', ['illustrations'])]
  assert absences({'synonyms': None}, 202) == [('synonymy', ['synonyms'])]
  assert absences({'occurrences': None, 'ranges': None}, 203) == [
    ('occurrences', ['occurrences', 'ranges'])
  ]
  assert absences({'ranges': None}, 204) == [('occurrences', ['ranges'])]
  # A value for either field, or a material entry linked to a horizon or a
  # locality, says the node has occurrences.
  assert absences({'occurrences': None, 'ranges': [{'series': 'Ordovician'}]}, 205) == []
  assert absences({'occurrences': [{'horizon': 'x'}], 'ranges': None}, 211) == []
  linked = {'occurrences': None, 'material': [{'label': 'A', 'horizon': 'x'}]}
  assert absences(linked, 206, file_horizons={'x': {'unit': ['a']}}) == []
  by_locality = {'occurrences': None, 'material': [{'label': 'A', 'locality': 'x'}]}
  assert absences(by_locality, 210, file_localities={'x': {'location': ['a']}}) == []
  # Absent fields and values say nothing.
  assert absences({}, 207) == []
  assert absences({'material': [{'label': 'A'}], 'synonyms': [{'taxon': _SISTER}]}, 208) == []
  # All four, in the fixed order, whatever the order written.
  everything = {
    'synonyms': None,
    'illustrations': None,
    'ranges': None,
    'material': None,
  }
  assert [kind for kind, _ in absences(everything, 209)] == [
    'material',
    'occurrences',
    'illustrations',
    'synonymy',
  ]


def test_absence_is_emitted_at_any_rank_and_never_on_a_cited_entry(records):
  genus = _claims_of(records, {'taxon': 'rhenopyrgus', 'material': None}, 210)
  assert _absences(genus) == [('material', ['material'])]
  cited = _claims_of(
    records,
    {'taxon': _SPECIES, 'synonyms': [{'taxon': _SISTER, 'synonyms': None, 'material': None}]},
    211,
  )
  assert _absences(cited) == []


def test_absence_claim_shape_and_effect_on_ids(records):
  data = {'taxon': _SPECIES, 'pages': 7, 'notes': 'n', 'material': [{'label': 'A'}]}
  plain = _claims_of(records, data, 212)
  nulled = _claims_of(records, {**data, 'ranges': None, 'synonyms': None}, 213)
  absences = [c for c in nulled if c['kind'] == 'absence']
  assert [c['id'] for c in absences] == [
    '1961_dehm:213:absence:0',
    '1961_dehm:213:absence:1',
  ]
  first = absences[0]
  assert first['absenceOf'] == 'occurrences' and first['fields'] == ['ranges']
  assert first['pages'] == 7 and first['notes'] == 'n' and first['subject'] == _SPECIES
  # No coverage kind: the claim is not counted under any.
  assert 'coverageKind' not in first['audit']

  def others(claims, position):
    return [c['id'].replace(f':{position}:', ':P:') for c in claims if c['kind'] != 'absence']

  assert others(plain, 212) == others(nulled, 213)
  entry = manifest(records, {'1961_dehm': nulled}, {'1961_dehm': []})['sources']['1961_dehm']
  assert entry['claims']['absence'] == 2
  assert 'absence' not in entry['derived']


def test_unfigured_specimens_are_derived_only_when_illustrations_are_all(records, monkeypatch):
  figured = {
    'taxon': _SPECIES,
    'material': [{'label': 'A'}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': 'A'}],
  }
  # A sister species whose figures are null makes the kind `all`.
  sister = {'taxon': _SISTER, 'illustrations': None}

  def specimens(species, position, with_sister=True, **metadata):
    children = [species, sister] if with_sister else [species]
    claims = _claims_of(
      records, {'taxon': 'rhenopyrgus', 'children': children}, position, **metadata
    )
    return {
      c['label']: c.get('figured')
      for c in claims
      if c['kind'] == 'material' and c['materialKind'] == 'specimen' and c['subject'] == _SPECIES
    }

  assert specimens(figured, 220) == {'A': None, 'B': False}
  # `figured` is never set to True: a figured specimen has illustrationClaims.
  claims = _claims_of(records, {'taxon': 'rhenopyrgus', 'children': [figured, sister]}, 221)
  by_label = {c['label']: c for c in claims if c.get('materialKind') == 'specimen'}
  assert 'illustrationClaims' in by_label['A'] and 'figured' not in by_label['A']

  # Not set when the source's figures are not entered in full.
  monkeypatch.setitem(
    records.sources['1961_dehm']._data['audit']['coverage'], 'illustrations', 'partly'
  )
  assert specimens(figured, 222, with_sister=False) == {'A': None, 'B': None}
  monkeypatch.undo()

  # Not set with an untied figure on the node: it may show the specimen.
  untied = {**figured, 'illustrations': [{'plate': 1, 'of': 'A'}, {'plate': 2}]}
  assert specimens(untied, 223) == {'A': None, 'B': None}
  # Not set when the node does not carry `illustrations` at all.
  assert specimens({k: v for k, v in figured.items() if k != 'illustrations'}, 224) == {
    'A': None,
    'B': None,
  }
  # A null on the node is a value of the field: every entry is unfigured.
  assert specimens({**figured, 'illustrations': None}, 225) == {'A': False, 'B': False}


def test_a_number_inside_a_run_names_its_entry_for_figured(records):
  node = {
    'taxon': _SPECIES,
    'material': [{'prefix': 'GSC', 'numbers': [[100, 105]]}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': 103}],
  }
  sister = {'taxon': _SISTER, 'illustrations': None}
  claims = _claims_of(records, {'taxon': 'rhenopyrgus', 'children': [node, sister]}, 226)
  specimens = [
    c for c in claims if c.get('materialKind') == 'specimen' and c['subject'] == _SPECIES
  ]
  assert [c.get('figured') for c in specimens] == [None, False]


def test_a_figured_role_or_a_figured_cast_is_never_unfigured(records):
  sister = {'taxon': _SISTER, 'illustrations': None}

  def figured(node, position):
    claims = _claims_of(records, {'taxon': 'rhenopyrgus', 'children': [node, sister]}, position)
    return {
      c['label']: c.get('figured')
      for c in claims
      if c.get('materialKind') == 'specimen' and c['subject'] == _SPECIES
    }

  # The source calls the entry a figured specimen, whatever the figures say.
  node = {
    'taxon': _SPECIES,
    'material': [{'label': 'A', 'role': 'figured'}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': 'B'}],
  }
  assert figured(node, 227) == {'A': None, 'B': None}
  assert figured({**node, 'illustrations': None}, 228) == {'A': None, 'B': False}
  # A figure of a cast shows its original; the cast's own entry is figured by it.
  cast = {
    'taxon': _SPECIES,
    'material': [{'label': 'A'}, {'label': 'B', 'castOf': 'A'}, {'label': 'C'}],
    'illustrations': [{'plate': 1, 'of': 'B'}],
  }
  assert figured(cast, 229) == {'A': None, 'B': None, 'C': False}
  # An unfigured cast leaves its original unfigured, and so does a figure
  # of another entry.
  unfigured_cast = {**cast, 'illustrations': [{'plate': 1, 'of': 'C'}]}
  assert figured(unfigured_cast, 230) == {'A': False, 'B': False, 'C': None}
  # The cast is found by a number or a run as a figure's `of` is.
  numbered = {
    'taxon': _SPECIES,
    'material': [
      {'prefix': 'GSC', 'numbers': [100]},
      {'prefix': 'GSC', 'numbers': [101], 'castOf': 100},
    ],
    'illustrations': [{'plate': 1, 'of': 101}],
  }
  claims = _claims_of(records, {'taxon': 'rhenopyrgus', 'children': [numbered, sister]}, 231)
  assert [
    c.get('figured')
    for c in claims
    if c.get('materialKind') == 'specimen' and c['subject'] == _SPECIES
  ] == [None, None]


# -- holotype_conflicts (roadmap F5) ---------------------------------------------

_TAXON = 'navicula_whitehouse_1941'


def _claim(source, role='holotype', taxon=_TAXON, **fields):
  return {
    'id': f'{source}:{taxon}:{role}:{len(fields)}',
    'kind': 'material',
    'materialKind': 'specimen',
    'source': source,
    'subject': taxon,
    'role': role,
    **fields,
  }


def _conflicts(records, *claims):
  by_source = {}
  for claim in claims:
    by_source.setdefault(claim['source'], []).append(claim)
  return holotype_conflicts(records, by_source)


def test_one_specimen_under_two_printed_forms_is_no_conflict(records):
  first = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  second = _claim('2021_jell_sprinkle', ids=['UQF5404'], joinKeys=['uq-f:5404'])
  assert _conflicts(records, first, second) == []


def test_two_different_numbers_are_a_conflict_in_year_order(records):
  later = _claim('2021_jell_sprinkle', ids=['UQF 9'], joinKeys=['uq-f:9'])
  first = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  [row] = _conflicts(records, later, first)
  assert row['taxon'] == _TAXON
  assert row['holotypes'] == [
    {
      'source': '1941_whitehouse',
      'ids': ['F. 5404'],
      'joinKeys': ['uq-f:5404'],
      'claim': first['id'],
    },
    {
      'source': '2021_jell_sprinkle',
      'ids': ['UQF 9'],
      'joinKeys': ['uq-f:9'],
      'claim': later['id'],
    },
  ]


def test_a_later_lectotype_or_neotype_is_no_conflict(records):
  holotype = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  for role in ('lectotype', 'neotype'):
    later = _claim('2021_jell_sprinkle', role=role, ids=['UQF 9'], joinKeys=['uq-f:9'])
    assert _conflicts(records, holotype, later) == []
  # A source that designates a lectotype leaves the comparison whole, even
  # when it also reports the old holotype entry.
  report = _claim('2021_jell_sprinkle', ids=['UQF 9'], joinKeys=['uq-f:9'])
  assert _conflicts(records, holotype, later, report) == []


def test_an_uncertain_holotype_is_ignored(records):
  holotype = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  doubtful = _claim('2021_jell_sprinkle', ids=['UQF 9'], joinKeys=['uq-f:9'], uncertain=True)
  assert _conflicts(records, holotype, doubtful) == []
  # An uncertain lectotype does not excuse a conflict either.
  lectotype = _claim('2021_jell_sprinkle', role='lectotype', ids=['UQF 9'], uncertain=True)
  assert _conflicts(records, holotype, lectotype) == []


def test_other_roles_and_a_single_source_are_no_conflict(records):
  holotype = _claim('1941_whitehouse', ids=['F. 5404'], joinKeys=['uq-f:5404'])
  paratype = _claim('2021_jell_sprinkle', role='paratype', ids=['UQF 9'], joinKeys=['uq-f:9'])
  assert _conflicts(records, holotype, paratype) == []
  other = _claim('1941_whitehouse', ids=['F. 5405'], joinKeys=['uq-f:5405'], count=1)
  assert _conflicts(records, holotype, other) == []


def test_unnumbered_holotypes_are_compared_by_label_then_printed_ids(records):
  first = _claim('1941_whitehouse', label='the Taf. 2 fossil')
  same = _claim('2021_jell_sprinkle', label='the Taf. 2 fossil')
  assert _conflicts(records, first, same) == []
  [row] = _conflicts(records, first, _claim('2021_jell_sprinkle', label='the Taf. 3 fossil'))
  assert row['holotypes'][0]['joinKeys'] == [] and row['holotypes'][0]['label'] == first['label']
  # No join keys and no label: the printed ids, a range pair's endpoints included.
  ids = _claim('1941_whitehouse', ids=[['XX 1', 'XX 2']])
  assert _conflicts(records, ids, _claim('2021_jell_sprinkle', ids=['XX 2'])) == []
  [row] = _conflicts(records, ids, _claim('2021_jell_sprinkle', ids=['XX 3']))
  assert row['holotypes'][0]['ids'] == [['XX 1', 'XX 2']]


def test_the_manifest_reports_holotype_conflicts(records, claims, roots):
  # The corpus: the function runs and the manifest carries what it returns.
  assert isinstance(holotype_conflicts(records, claims), list)
  assert manifest(records, claims, roots)['holotypeConflicts'] == holotype_conflicts(
    records, claims
  )


# -- `sameAs`: a link from one specimen entry to an earlier source's ------------

_EARLY, _LATE, _LATEST = '1897_whiteaves', '1914c_bather', '1962_fay'
_OTTAWA = 'ottawaensis_whiteaves_1897'


def _linked_claims(records, trees, sources=None):
  """`extract` over synthetic trees of real sources: `trees` maps a source
  key to `(position, node)`."""
  roots = {
    source: [
      Tree(node, {'source_key': source, 'type': 'taxonomy', 'position': position}, corpus=records)
    ]
    for source, (position, node) in trees.items()
  }
  return extract(records, roots, sources)


def _specimens(claims, source):
  return [c for c in claims[source] if c.get('materialKind') == 'specimen']


def test_the_linked_sources_are_in_year_order(records):
  assert [records.sources[k].year for k in (_EARLY, _LATE, _LATEST)] == [1897, 1914, 1962]


def test_same_as_is_copied_and_resolved_to_the_earlier_claim(records):
  link = {'source': _EARLY, 'label': 'First  specimen'}
  claims = _linked_claims(
    records,
    {
      _EARLY: (1300, {'taxon': _OTTAWA, 'material': [{'label': 'first specimen'}, {'label': 'x'}]}),
      _LATE: (
        1301,
        {'taxon': _OTTAWA, 'material': [{'label': 'A', 'role': 'holotype', 'sameAs': link}]},
      ),
    },
  )
  first, _ = _specimens(claims, _EARLY)
  [later] = _specimens(claims, _LATE)
  assert later['sameAs'] == link
  assert later['sameAsClaim'] == first['id']
  assert 'sameAs' not in first and 'sameAsClaim' not in first


def test_same_as_by_number_within_a_prefix(records):
  entries = [
    {'prefix': 'GSC', 'numbers': [5]},
    {'prefix': 'ROM', 'numbers': [5]},
    {'prefix': 'GSC', 'numbers': [[100, 110]]},
  ]
  trees = {_EARLY: (1302, {'taxon': _OTTAWA, 'material': entries})}

  def resolved(link, position):
    node = {'taxon': _OTTAWA, 'material': [{'label': 'A', 'sameAs': {'source': _EARLY, **link}}]}
    claims = _linked_claims(records, {**trees, _LATE: (position, node)})
    return _specimens(claims, _LATE)[0].get('sameAsClaim'), _specimens(claims, _EARLY)

  target, early = resolved({'number': 5, 'prefix': 'ROM'}, 1303)
  assert target == early[1]['id']
  # No prefix: the number names two entries, so it names none.
  assert resolved({'number': 5}, 1304)[0] is None
  # A number inside a run names the run's entry.
  target, early = resolved({'number': 105, 'prefix': 'GSC'}, 1305)
  assert target == early[2]['id']


def test_same_as_stays_unresolved_when_the_target_is_not_extracted_or_not_found(records):
  link = {'source': _EARLY, 'label': 'first specimen'}
  trees = {
    _EARLY: (1306, {'taxon': _OTTAWA, 'material': [{'label': 'first specimen'}]}),
    _LATE: (1307, {'taxon': _OTTAWA, 'material': [{'label': 'A', 'sameAs': link}]}),
  }
  [later] = _specimens(_linked_claims(records, trees, sources=[_LATE]), _LATE)
  assert later['sameAs'] == link and 'sameAsClaim' not in later
  lost = {'taxon': _OTTAWA, 'material': [{'label': 'A', 'sameAs': {**link, 'label': 'nope'}}]}
  claims = _linked_claims(records, {**trees, _LATE: (1308, lost)})
  assert 'sameAsClaim' not in _specimens(claims, _LATE)[0]


def test_an_inferred_same_as_is_listed_in_inferred_fields(records):
  editorial = {'inferred': ['role', 'sameAs'], 'basis': 'the editor reads No. 752 as the lectotype'}
  node = {
    'taxon': _OTTAWA,
    'material': [
      {
        'prefix': 'GSC',
        'numbers': [752],
        'role': 'lectotype',
        'sameAs': {'source': _LATE, 'label': 'A'},
        'editorial': editorial,
      }
    ],
  }
  [claim] = _specimens(_linked_claims(records, {_LATEST: (1309, node)}), _LATEST)
  assert claim['inferredFields'] == ['role', 'sameAs']
  assert claim['sameAs'] == {'source': _LATE, 'label': 'A'}
  # The entry is printed and only its fields are the editor's.
  assert 'inferred' not in claim


def _holotype_chain(middle_role):
  early = _claim(_EARLY, id='early', label='first specimen')
  middle = _claim(_LATE, role=middle_role, id='middle', label='A', sameAsClaim='early')
  late = _claim(
    _LATEST, id='late', ids=['GSC 752'], joinKeys=['gsc:752'], sameAsClaim='middle', role='holotype'
  )
  return early, middle, late


def test_holotypes_linked_by_same_as_are_one_specimen(records):
  early = _claim(_EARLY, id='early', label='first specimen')
  later = _claim(_LATE, id='later', label='A', sameAsClaim='early')
  assert _conflicts(records, early, later) == []
  # The link is read in either direction.
  early['sameAsClaim'], later['sameAsClaim'] = 'later', None
  assert _conflicts(records, early, later) == []
  # Unlinked, different labels are two specimens.
  [row] = _conflicts(
    records, _claim(_EARLY, id='early', label='first specimen'), _claim(_LATE, label='A')
  )
  assert [h['source'] for h in row['holotypes']] == [_EARLY, _LATE]


@pytest.mark.parametrize('middle_role', ['holotype', 'syntype'])
def test_holotypes_linked_through_a_chain_are_one_specimen(records, middle_role):
  assert _conflicts(records, *_holotype_chain(middle_role)) == []
  # Without the middle link the ends are two specimens.
  early, middle, late = _holotype_chain(middle_role)
  late['sameAsClaim'] = None
  assert len(_conflicts(records, early, middle, late)) == 1


def test_a_shared_join_key_joins_one_number_entries_but_a_batch_joins_nothing(records):
  one = _claim('1941_whitehouse', id='one', ids=['F. 1'], joinKeys=['uq-f:1'])
  two = _claim('2021_jell_sprinkle', id='two', ids=['UQF 2'], joinKeys=['uq-f:2'])
  # A paratype entry printing both numbers does not make them one specimen.
  batch = _claim(
    '1960_gill_caster', role='paratype', id='batch', joinKeys=['uq-f:1', 'uq-f:2'], rangeJoin=True
  )
  assert len(_conflicts(records, one, two, batch)) == 1
  # A one-number entry that links to the earlier label joins the two.
  early = _claim(_EARLY, id='early', label='first specimen')
  bridge = _claim(_LATE, role='paratype', id='bridge', joinKeys=['uq-f:1'], sameAsClaim='early')
  same = _claim('2021_jell_sprinkle', id='same', ids=['UQF 1'], joinKeys=['uq-f:1'])
  assert _conflicts(records, early, bridge, same) == []


def test_auctt_cites_authors_in_place_of_a_work(records, caplog):
  # "Echinozoa auctt.": the name in the sense of authors generally, cited
  # in place of a work; "auctt. veterum" qualifies the authors.
  root = Tree(
    {
      'taxon': 'rhenopyrgus',
      'authority': {'auctt': 'veterum'},
      'emendedBy': [{'auctt': True}, {'source': '1968b_paul.c.r.c'}],
    },
    {'source_key': '1985_jell_burrett_banks', 'type': 'taxonomy', 'position': 92},
    corpus=records,
  )
  claims = extract(records, {'1985_jell_burrett_banks': [root]})['1985_jell_burrett_banks']
  assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
  [usage] = [c for c in claims if c['kind'] == 'usage']
  assert usage['citesAuctt'] == 'veterum' and 'citesSource' not in usage
  assert 'printedAttribution' not in usage
  acts = [(c.get('by'), c.get('byAuctt')) for c in claims if c['kind'] == 'act']
  assert acts == [(None, True), ('1968b_paul.c.r.c', None)]

  schema = support.schema()
  tree = schema[io.TREE_DEF]
  assert tree.check({'taxonomies': [{'taxon': 'rhenopyrgus', 'authority': {'auctt': True}}]})
  assert tree.check({'taxonomies': [root.data | {'authority': {'auctt': 'veterum', 'notes': 'n'}}]})
  for authority in (
    {'auctt': True, 'source': '1968b_paul.c.r.c'},
    {'auctt': True, 'pages': 12},
    {'auctt': True, 'attributedTo': ['paul.c.r.c']},
    {'auctt': False},
    {'auctt': ''},
    {},
  ):
    assert not tree.check({'taxonomies': [{'taxon': 'rhenopyrgus', 'authority': authority}]})
  # A protologue is a particular work.
  record = {'name': 'Rhenopyrgus', 'rank': 'genus'}
  assert schema['taxa'].check(
    {'rhenopyrgus': record | {'authority': {'source': '1968b_paul.c.r.c'}}}
  )
  assert not schema['taxa'].check({'rhenopyrgus': record | {'authority': {'auctt': True}}})
  section = {'name': 'Integra', 'authority': {'source': '1968b_paul.c.r.c'}}
  assert schema['sections'].check({'integra': section})
  assert not schema['sections'].check({'integra': section | {'authority': {'auctt': True}}})


# -- occurrences: horizons and localities paired -------------------------------


def _occurrences(records, data, position, **metadata):
  claims = _claims_of(records, {'taxon': _SPECIES, **data}, position, **metadata)
  return [c for c in claims if c.get('materialKind') == 'occurrence']


def test_a_horizon_shared_by_two_localities_gives_two_claims_sharing_the_horizon(records):
  horizon = {'unit': ['Trenton Limestone'], 'series': 'Middle Ordovician'}
  data = {
    'horizons': {'trenton': horizon},
    'localities': {
      'ottawa': {'location': ['Ottawa']},
      'kingston': {'location': ['Kingston']},
    },
    'material': [
      {'label': 'A', 'horizon': 'trenton', 'locality': 'ottawa'},
      {'label': 'B', 'horizon': 'trenton', 'locality': 'kingston'},
    ],
  }
  first, second = _occurrences(records, data, 300)
  assert first['horizonKey'] == second['horizonKey'] == 'trenton'
  assert first['occurrence']['horizon'] == second['occurrence']['horizon'] == horizon
  assert (first['localityKey'], second['localityKey']) == ('ottawa', 'kingston')
  assert second['occurrence']['locality'] == {'location': ['Kingston']}
  assert first['id'] != second['id']


def test_a_locality_with_two_horizons_gives_two_claims_sharing_the_locality(records):
  data = {
    'horizons': {'lower': {'unit': ['Lower Bed']}, 'upper': {'unit': ['Upper Bed']}},
    'localities': {'quarry': {'location': ['Quarry Road']}},
    'material': [
      {'label': 'A', 'horizon': 'lower', 'locality': 'quarry'},
      {'label': 'B', 'horizon': 'upper', 'locality': 'quarry'},
    ],
  }
  first, second = _occurrences(records, data, 301)
  assert first['localityKey'] == second['localityKey'] == 'quarry'
  assert (first['horizonKey'], second['horizonKey']) == ('lower', 'upper')
  assert first['occurrence']['locality'] == second['occurrence']['locality']


def test_an_occurrence_with_no_specimen_gives_a_claim_and_counts_as_present(records, store):
  data = {
    'horizons': {'bed': {'unit': ['Wheeler Shale'], 'series': 'Cambrian Series 3'}},
    'localities': {'house-range': {'location': ['House Range, Utah']}},
    'occurrences': [{'horizon': 'bed', 'locality': 'house-range', 'notes': 'as listed'}],
  }
  claims = _claims_of(records, {'taxon': _SPECIES, **data}, 302)
  [claim] = [c for c in claims if c['kind'] == 'material']
  assert claim['materialKind'] == 'occurrence'
  assert claim['horizonKey'] == 'bed' and claim['horizonScope'] == 'node'
  assert claim['localityKey'] == 'house-range' and claim['localityScope'] == 'node'
  assert claim['occurrenceNotes'] == 'as listed'
  assert claim['occurrence']['horizon'] == data['horizons']['bed']
  assert claim['occurrence']['locality'] == data['localities']['house-range']
  assert store.words.claim_words(claim) == (
    'occurrence bed, house-range: Cambrian Series 3; Wheeler Shale; House Range, Utah'
  )
  # No specimen claim, and a node that states an occurrence says nothing absent
  # even when its `ranges` is null.
  assert not [c for c in claims if c.get('materialKind') == 'specimen']
  assert _absences(claims) == []
  with_null_ranges = _claims_of(
    records, {'taxon': _SPECIES, **data, 'ranges': None, 'occurrences': data['occurrences']}, 303
  )
  assert _absences(with_null_ranges) == []
  # `occurrences: null` alone is the declared absence.
  assert _absences(_claims_of(records, {'taxon': _SPECIES, 'occurrences': None}, 304)) == [
    ('occurrences', ['occurrences'])
  ]

  # The node counts as present for the derived coverage: a value alone
  # declares nothing, and beside a sister that says `occurrences: null` the
  # kind is `all`.
  def coverage(*children):
    root = Tree(
      {'taxon': 'rhenopyrgus', 'ranges': [{'series': 'Ordovician'}], 'children': list(children)},
      {**_BASE, 'position': 305},
      corpus=records,
    )
    return derived_coverage({'s': [root]})['s']['occurrences']

  assert coverage({'taxon': _SPECIES, **data}) is None
  assert coverage({'taxon': _SPECIES, **data}, {'taxon': _SISTER, 'occurrences': None}) == 'all'
  # Without the occurrence the same species is an uncaptured field.
  assert coverage({'taxon': _SPECIES}, {'taxon': _SISTER, 'ranges': None}) == 'partly'
  assert coverage({'taxon': _SPECIES, **data}, {'taxon': _SISTER, 'ranges': None}) == 'all'
  # An entry's `locality: null` is the audit's statement for its node: the
  # node is captured and the kind is declared.
  no_locality = {'taxon': _SISTER, 'material': [{'label': 'A', 'locality': None}]}
  assert coverage({'taxon': _SPECIES, **data}, no_locality) == 'all'
  assert coverage({'taxon': _SPECIES}, no_locality) == 'partly'


def test_a_null_locality_reaches_the_specimen_claim_and_makes_no_occurrence(records, store):
  data = {
    'horizons': {'bed': {'unit': ['Wheeler Shale']}},
    'material': [
      {'prefix': 'GSC', 'numbers': [1], 'locality': None},
      {'prefix': 'GSC', 'numbers': [2], 'horizon': 'bed', 'locality': None},
      {'prefix': 'GSC', 'numbers': [3], 'horizon': 'bed'},
    ],
  }
  claims = _claims_of(records, {'taxon': _SPECIES, **data}, 321, file_prefixes={'GSC': 'gsc'})
  neither, horizon_only, unsaid = [c for c in claims if c.get('materialKind') == 'specimen']
  # The null is kept: the source gives no locality for the specimen.
  assert neither['localityKey'] is None and 'horizonKey' not in neither
  assert horizon_only['localityKey'] is None and horizon_only['horizonKey'] == 'bed'
  assert 'localityKey' not in unsaid
  assert store.words.claim_words(neither) == 'specimens: GSC 1 (no locality given)'
  assert store.words.claim_words(horizon_only) == 'specimens: GSC 2 (no locality given)'
  assert store.words.claim_words(unsaid) == 'specimens: GSC 3'
  # A null names no locality, so the horizon stands alone in one pairing.
  [occurrence] = [c for c in claims if c.get('materialKind') == 'occurrence']
  assert occurrence['horizonKey'] == 'bed' and 'localityKey' not in occurrence
  assert occurrence['occurrence'] == {'horizon': {'unit': ['Wheeler Shale']}}
  # A node's `occurrences: null` still stands beside a null locality alone.
  alone = {'taxon': _SPECIES, 'occurrences': None, 'material': [{'label': 'A', 'locality': None}]}
  assert _absences(_claims_of(records, alone, 322)) == [('occurrences', ['occurrences'])]


def test_two_entries_naming_one_pair_give_one_claim(records):
  data = {
    'horizons': {'bed': {'unit': ['Wheeler Shale']}},
    'localities': {'quarry': {'location': ['Quarry Road']}},
    'material': [
      {'label': 'A', 'horizon': 'bed', 'locality': 'quarry'},
      {'label': 'B', 'horizon': 'bed', 'locality': 'quarry'},
      {'label': 'C'},
    ],
  }
  [claim] = _occurrences(records, data, 306)
  assert claim['horizonKey'] == 'bed' and claim['localityKey'] == 'quarry'
  # The pair is not the same as either side alone.
  data['material'].append({'label': 'D', 'horizon': 'bed'})
  assert len(_occurrences(records, data, 307)) == 2


def test_an_occurrence_item_and_an_entry_naming_the_same_pair_give_one_claim(records):
  data = {
    'horizons': {'bed': {'unit': ['Wheeler Shale']}},
    'localities': {'quarry': {'location': ['Quarry Road']}},
    'occurrences': [{'horizon': 'bed', 'locality': 'quarry', 'notes': 'stated first'}],
    'material': [{'label': 'A', 'horizon': 'bed', 'locality': 'quarry'}],
  }
  [claim] = _occurrences(records, data, 308)
  # The item came first and keeps its note.
  assert claim['occurrenceNotes'] == 'stated first'
  # Either order, one claim: the node's own statement is emitted first.
  claims = _claims_of(records, {'taxon': _SPECIES, **data}, 309)
  kinds = [c['materialKind'] for c in claims if c['kind'] == 'material']
  assert kinds == ['occurrence', 'specimen']


def test_an_entry_tentative_list_reaches_the_specimen_claim_and_renders(records, store):
  data = {
    'horizons': {'bed': {'unit': ['Wheeler Shale']}},
    'localities': {'quarry': {'location': ['Quarry Road']}},
    'material': [
      {
        'prefix': 'GSC',
        'numbers': [1],
        'horizon': 'bed',
        'locality': 'quarry',
        'tentative': ['locality'],
      },
      {
        'prefix': 'GSC',
        'numbers': [2],
        'horizon': 'bed',
        'locality': 'quarry',
        'tentative': ['horizon', 'locality'],
      },
      {'prefix': 'GSC', 'numbers': [3], 'horizon': 'bed', 'locality': 'quarry'},
    ],
  }
  claims = _claims_of(records, {'taxon': _SPECIES, **data}, 310, file_prefixes={'GSC': 'gsc'})
  one, both, plain = [c for c in claims if c.get('materialKind') == 'specimen']
  assert one['tentativeFields'] == ['locality']
  assert both['tentativeFields'] == ['horizon', 'locality']
  assert 'tentativeFields' not in plain
  assert one['horizonKey'] == 'bed' and one['localityKey'] == 'quarry'
  assert store.words.claim_words(one) == 'specimens: GSC 1 (locality quarry?)'
  assert store.words.claim_words(both) == 'specimens: GSC 2 (horizon bed?) (locality quarry?)'
  assert store.words.claim_words(plain) == 'specimens: GSC 3'
  # An entry's doubt does not make the pairing's own claim tentative.
  [occurrence] = [c for c in claims if c.get('materialKind') == 'occurrence']
  assert 'tentativeFields' not in occurrence


def test_an_occurrence_item_tentative_list_reaches_the_claim_and_renders(records, store):
  data = {
    'horizons': {'bed': {'unit': ['Wheeler Shale']}},
    'localities': {'quarry': {'location': ['Quarry Road']}},
    'occurrences': [{'horizon': 'bed', 'locality': 'quarry', 'tentative': ['locality']}],
  }
  [claim] = _occurrences(records, data, 311)
  assert claim['tentativeFields'] == ['locality']
  assert store.words.claim_words(claim) == 'occurrence bed, quarry?: Wheeler Shale; Quarry Road'


def test_an_occurrence_with_one_side_has_no_key_for_the_other(records, store):
  data = {
    'horizons': {'bed': {'unit': ['Wheeler Shale']}},
    'localities': {'quarry': {'location': ['Quarry Road']}},
    'occurrences': [{'horizon': 'bed'}, {'locality': 'quarry'}],
  }
  only_horizon, only_locality = _occurrences(records, data, 312)
  assert only_horizon['occurrence'] == {'horizon': {'unit': ['Wheeler Shale']}}
  assert 'localityKey' not in only_horizon and 'localityScope' not in only_horizon
  assert only_locality['occurrence'] == {'locality': {'location': ['Quarry Road']}}
  assert 'horizonKey' not in only_locality and 'horizonScope' not in only_locality
  assert store.words.claim_words(only_horizon) == 'occurrence bed: Wheeler Shale'
  assert store.words.claim_words(only_locality) == 'occurrence quarry: Quarry Road'
  # An entry with one side names a one-sided pairing too.
  [entry_only] = _occurrences(
    records, {**data, 'occurrences': None, 'material': [{'label': 'A', 'locality': 'quarry'}]}, 313
  )
  assert entry_only['occurrence'] == {'locality': {'location': ['Quarry Road']}}


def test_a_file_horizon_and_a_node_locality_keep_their_own_scopes(records):
  data = {
    'localities': {'quarry': {'location': ['Quarry Road']}},
    'occurrences': [{'horizon': 'bed', 'locality': 'quarry'}],
  }
  [claim] = _occurrences(records, data, 314, file_horizons={'bed': {'unit': ['Wheeler Shale']}})
  assert claim['horizonScope'] == 'file' and claim['localityScope'] == 'node'
  # A node horizon shadows the file's of the same key, and says so in its scope.
  [shadowed] = _occurrences(
    records,
    {**data, 'horizons': {'bed': {'unit': ['Marjum Formation']}}},
    315,
    file_horizons={'bed': {'unit': ['Wheeler Shale']}},
  )
  assert shadowed['horizonScope'] == 'node'
  assert shadowed['occurrence']['horizon'] == {'unit': ['Marjum Formation']}


def test_a_horizon_and_a_locality_may_share_a_key(records):
  data = {
    'horizons': {'x': {'unit': ['Wheeler Shale']}},
    'localities': {'x': {'location': ['Quarry Road']}},
    'occurrences': [{'horizon': 'x', 'locality': 'x'}],
  }
  [claim] = _occurrences(records, data, 316)
  assert claim['occurrence']['horizon'] == {'unit': ['Wheeler Shale']}
  assert claim['occurrence']['locality'] == {'location': ['Quarry Road']}


def test_locality_keys_of_an_occurrence_come_from_its_locality(records):
  data = {
    'localities': {'quarry': {'localityNumbers': [{'prefix': 'USGS', 'number': '4148 CO'}]}},
    'occurrences': [{'locality': 'quarry'}],
  }
  [claim] = _occurrences(records, data, 317, file_prefixes={'USGS': 'usgs-l'})
  assert claim['localityKeys'] == ['usgs-l:4148co']


def test_editorial_inferred_on_a_horizon_reaches_inferred_fields_and_the_words(records, store):
  data = {
    'horizons': {
      'bed': {
        'unit': ['Wheeler Shale'],
        'stage': 'Drumian',
        'editorial': {'inferred': ['stage'], 'basis': 'The formation is Drumian.'},
      }
    },
    'localities': {
      'quarry': {
        'location': ['Quarry Road'],
        'editorial': {'inferred': ['location'], 'basis': 'Named by the map sheet.'},
      }
    },
    'occurrences': [{'horizon': 'bed', 'locality': 'quarry'}],
  }
  [claim] = _occurrences(records, data, 318)
  assert claim['inferredFields'] == ['horizon.stage', 'locality.location']
  assert claim['occurrence']['horizon']['editorial'] == data['horizons']['bed']['editorial']
  assert store.words.claim_words(claim) == (
    'occurrence bed, quarry: Drumian; Wheeler Shale; Quarry Road'
    ' (stage inferred by the editor: The formation is Drumian.)'
    ' (location inferred by the editor: Named by the map sheet.)'
  )
  # A record without an editorial block adds none.
  plain = {**data, 'horizons': {'bed': {'unit': ['Wheeler Shale']}}}
  [other] = _occurrences(records, plain, 319)
  assert other['inferredFields'] == ['locality.location']


def test_a_range_with_editorial_inferred_keeps_its_own_claim_shape(records):
  rng = {'series': 'Ordovician', 'editorial': {'inferred': ['series'], 'basis': 'Dated by zone.'}}
  claims = _claims_of(records, {'taxon': _SPECIES, 'ranges': [rng]}, 320)
  [claim] = [c for c in claims if c.get('materialKind') == 'range']
  assert claim['range'] == rng
