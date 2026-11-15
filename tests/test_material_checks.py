"""The material checks (`phylohist.loader.material`): horizon and locality references,
figure references, material entries and the file's `prefixes` map, nulls on
a cited entry, and the file-level `unused` list. Synthetic node dicts and
documents, one test per rule; a few exercise the loader's own wiring
(`load.py`) and `scripts/check_draft.py` end to end.
"""

import logging
import subprocess
import sys
import types
from pathlib import Path

import pytest

from phylohist.loader import io, material
from phylohist.loader.taxa import Tree
from tests import support

SCRIPTS = Path(__file__).resolve().parent.parent / 'scripts'


def _entry(*prefixes, other_names=(), within=None):
  entry = {'name': 'x', 'type': 'institution', 'prefixes': list(prefixes)}
  if other_names:
    entry['otherNames'] = list(other_names)
  if within:
    entry['within'] = within
  return entry


@pytest.fixture
def repositories():
  """A synthetic registry: keys are slugs, and PE, E and UCMP are each
  claimed by two entries."""
  return {
    'fmnh': _entry('FMNH', 'PE', 'FMNH PE'),
    'north-museum-fm': _entry('PE'),
    'nhmuk': _entry('NHMUK', 'E', other_names=['BMNH', 'NHM UK']),
    'uc': _entry('UC'),
    'uc-caster': _entry('E', 'BC', within='uc'),
    'uc-museum': _entry('UCMP', within='uc'),
    'berkeley': _entry('UCMP'),
    'mcz': _entry('MCZ'),
    'gm': _entry('GM'),
    'usnm': _entry('USNM'),
    'usnm-walcott': {'name': 'x', 'type': 'collection', 'within': 'usnm'},
  }


@pytest.fixture
def registers(repositories):
  """`repositories` plus the specimen registers and locality registers the
  real registry has for the cases below."""
  return {
    **repositories,
    'uq-f': _entry('UQF', 'F'),
    'gsc': _entry('GSC', other_names=['Canadian Geological Survey']),
    'usgs-l': {**_entry('USGS'), 'subject': 'localities'},
  }


# -- registry_links -------------------------------------------------------------


def test_registry_links_real_registry_passes():
  assert material.registry_links(io.load_yaml(support.CORPUS / 'repositories.yaml')) == []


def test_registry_links_synthetic_registry_passes(repositories):
  assert material.registry_links(repositories) == []


def test_registry_links_within_a_missing_key_is_error():
  registry = {'a': _entry('A', within='nowhere')}
  assert material.registry_links(registry) == [
    ('error', 'repository "a" is within "nowhere", which is not a key'),
  ]


def test_registry_links_within_cycle_is_error_once():
  registry = {
    'a': _entry('A', within='b'),
    'b': _entry('B', within='c'),
    'c': _entry('C', within='a'),
  }
  messages = material.registry_links(registry)
  assert len(messages) == 1
  assert messages[0][0] == 'error'
  assert '`within` cycles' in messages[0][1]


def test_registry_links_self_within_is_a_cycle():
  registry = {'a': _entry('A', within='a')}
  assert material.registry_links(registry) == [('error', '`within` cycles: a -> a')]


def test_registry_links_chain_into_a_cycle_reports_the_cycle():
  registry = {
    'a': _entry('A', within='b'),
    'b': _entry('B', within='c'),
    'c': _entry('C', within='b'),
  }
  assert material.registry_links(registry) == [('error', '`within` cycles: b -> c -> b')]


# -- occurrence_refs ----------------------------------------------------------


def _records(horizons=None, localities=None):
  return {'horizons': horizons or {}, 'localities': localities or {}}


def test_occurrence_refs_missing_is_error_on_each_side():
  node = {'material': [{'label': 'A', 'horizon': 'nowhere', 'locality': 'nowhere-else'}]}
  assert material.occurrence_refs(node, _records(), _records()) == [
    ('error', 'horizon "nowhere" is not defined on the node or the file'),
    ('error', 'locality "nowhere-else" is not defined on the node or the file'),
  ]
  # A horizon key is not looked up among the localities, nor the reverse.
  node = {'material': [{'label': 'A', 'horizon': 'x'}]}
  assert material.occurrence_refs(node, _records(), _records(localities={'x': {}})) == [
    ('error', 'horizon "x" is not defined on the node or the file'),
  ]
  assert material.occurrence_refs(
    {'occurrences': [{'locality': 'x'}]}, _records(), _records(horizons={'x': {}})
  ) == [('error', 'locality "x" is not defined on the node or the file')]


def test_occurrence_refs_resolves_from_node_or_file_with_no_message():
  node_only = {'material': [{'label': 'A', 'horizon': 'here', 'locality': 'here'}]}
  assert material.occurrence_refs(node_only, _records({'here': {}}, {'here': {}}), _records()) == []
  file_only = {'material': [{'label': 'A', 'horizon': 'there', 'locality': 'there'}]}
  assert (
    material.occurrence_refs(file_only, _records(), _records({'there': {}}, {'there': {}})) == []
  )
  stated = {'occurrences': [{'horizon': 'there'}, {'locality': 'here'}]}
  assert (
    material.occurrence_refs(stated, _records(localities={'here': {}}), _records({'there': {}}))
    == []
  )


def test_occurrence_refs_node_key_shadows_file_key_is_warning_on_each_side():
  node = {'material': [{'label': 'A', 'horizon': 'here', 'locality': 'here'}]}
  records = _records({'here': {}}, {'here': {}})
  assert material.occurrence_refs(node, records, records) == [
    ('warning', 'horizon "here" on the node shadows a file-level horizon'),
    ('warning', 'locality "here" on the node shadows a file-level locality'),
  ]
  # An occurrence item shadows in the same way.
  stated = {'occurrences': [{'horizon': 'here'}]}
  assert material.occurrence_refs(stated, _records({'here': {}}), _records({'here': {}})) == [
    ('warning', 'horizon "here" on the node shadows a file-level horizon'),
  ]


def test_occurrence_refs_entries_without_a_side_are_quiet():
  node = {'material': [{'label': 'A', 'horizon': 'h', 'tentative': ['horizon']}, {'count': 1}]}
  assert material.occurrence_refs(node, _records({'h': {}}), _records()) == []
  assert material.occurrence_refs({}, _records(), _records()) == []
  assert material.occurrence_refs({'occurrences': None}, _records(), _records()) == []


def test_occurrence_refs_node_record_nothing_on_the_node_refers_to_is_error():
  node = {
    'material': [{'label': 'A', 'horizon': 'used'}],
    'occurrences': [{'locality': 'stated'}],
  }
  records = _records({'used': {}, 'stray-horizon': {}}, {'stated': {}, 'stray-locality': {}})
  assert material.occurrence_refs(node, records, _records()) == [
    ('error', 'horizon "stray-horizon" is defined on the node and referred to by nothing on it'),
    ('error', 'locality "stray-locality" is defined on the node and referred to by nothing on it'),
  ]
  # A file-level record is not held to it: the file-level check covers it.
  assert material.occurrence_refs({}, _records(), records) == []


def test_occurrence_refs_tentative_naming_a_field_the_entry_lacks_is_error():
  node = {
    'material': [
      {'label': 'A', 'horizon': 'h', 'tentative': ['horizon', 'locality']},
      {'label': 'B', 'horizon': 'h', 'locality': 'l', 'tentative': ['locality']},
    ],
    'occurrences': [{'horizon': 'h', 'tentative': ['locality']}],
  }
  records = _records({'h': {}}, {'l': {}})
  assert material.occurrence_refs(node, records, _records()) == [
    ('error', '`tentative` names `locality`, which the entry does not carry'),
    ('error', '`tentative` names `locality`, which the entry does not carry'),
  ]


# -- tentative_fields and inferred_fields -------------------------------------


def test_tentative_names_a_field_the_range_does_not_carry():
  rng = {'period': 'Ordovician', 'tentative': ['series']}
  assert material.tentative_fields(rng, 'range') == [
    ('error', '`tentative` names `series`, which the range does not carry'),
  ]
  horizon = {'unit': ['A Fm.'], 'tentative': ['unit', 'biozone']}
  assert material.tentative_fields(horizon, 'horizon') == [
    ('error', '`tentative` names `biozone`, which the horizon does not carry'),
  ]
  locality = {'location': ['A Quarry'], 'tentative': ['mapSheet']}
  assert material.tentative_fields(locality, 'locality') == [
    ('error', '`tentative` names `mapSheet`, which the locality does not carry'),
  ]


def test_tentative_cannot_name_a_key_that_is_no_printed_value():
  rng = {'series': 'Middle Ordovician', 'regions': ['Ottawa'], 'asPrinted': 'x', 'notes': 'y'}
  rng['tentative'] = ['tentative', 'notes', 'asPrinted', 'editorial', 'sources', 'regions']
  messages = material.tentative_fields(rng, 'range')
  assert [level for level, _ in messages] == ['error'] * 6
  assert [m.split('`')[3] for _, m in messages] == rng['tentative']
  # Present on the record, `editorial` is still no queriable value.
  rng['editorial'] = {'inferred': ['series']}
  rng['tentative'] = ['editorial']
  assert material.tentative_fields(rng, 'range') == [
    ('error', '`tentative` cannot name `editorial`, which is not a printed value'),
  ]


def test_tentative_true_on_a_file_level_horizon_or_locality_is_error():
  for kind in ('horizon', 'locality'):
    record = {'unit': ['A Fm.'], 'tentative': True}
    assert material.tentative_fields(record, kind, file_level=True) == [
      (
        'error',
        f'a file-level {kind} cannot be `tentative: true`; the doubt belongs to the node '
        'or the specimen that uses it',
      ),
    ]


def test_tentative_clean_cases():
  # A list on a range, a list on a node and a file-level horizon, `true`
  # on a node-level horizon and on a range, and no `tentative` at all.
  assert material.tentative_fields({'series': 'X', 'tentative': ['series']}, 'range') == []
  assert material.tentative_fields({'series': 'X', 'tentative': True}, 'range') == []
  assert material.tentative_fields({'biozone': 'X', 'tentative': ['biozone']}, 'horizon') == []
  assert (
    material.tentative_fields({'biozone': 'X', 'tentative': ['biozone']}, 'horizon', True) == []
  )
  assert material.tentative_fields({'unit': ['A']}, 'horizon', True) == []
  assert material.tentative_fields(None, 'horizon') == []
  node = {
    'ranges': [{'series': 'X', 'tentative': ['series']}, {'period': 'Y', 'tentative': True}, None],
    'horizons': {'a': {'biozone': 'X', 'tentative': ['biozone']}, 'b': {'tentative': True}},
    'localities': {'c': {'location': ['Q'], 'tentative': ['location']}, 'd': {'tentative': True}},
  }
  assert material.range_tentatives(node) == []
  assert material.record_tentatives(_records(node['horizons'], node['localities'])) == []
  assert material.range_tentatives({'ranges': None}) == []


def test_tentative_checks_name_the_record_and_run_over_the_lists():
  node = {'ranges': [{'period': 'Y', 'tentative': ['series']}]}
  assert material.range_tentatives(node) == [
    ('error', '`tentative` names `series`, which the range does not carry'),
  ]
  horizons = {'a': {'unit': ['A'], 'tentative': True}, 'b': {'tentative': ['biozone']}, 'c': None}
  localities = {'d': {'location': ['A'], 'tentative': True}, 'e': {'tentative': ['location']}}
  records = _records(horizons, localities)
  assert material.record_tentatives(records) == [
    ('error', 'horizon "b": `tentative` names `biozone`, which the horizon does not carry'),
    ('error', 'locality "e": `tentative` names `location`, which the locality does not carry'),
  ]
  assert [m for _, m in material.record_tentatives(records, file_level=True)] == [
    'horizon "a": a file-level horizon cannot be `tentative: true`; the doubt belongs to the '
    'node or the specimen that uses it',
    'horizon "b": `tentative` names `biozone`, which the horizon does not carry',
    'locality "d": a file-level locality cannot be `tentative: true`; the doubt belongs to the '
    'node or the specimen that uses it',
    'locality "e": `tentative` names `location`, which the locality does not carry',
  ]


def test_inferred_names_a_field_the_record_does_not_carry():
  horizon = {'unit': ['A'], 'editorial': {'inferred': ['unit', 'stage'], 'basis': 'x'}}
  assert material.inferred_fields(horizon, 'horizon') == [
    ('error', '`editorial.inferred` names `stage`, which the horizon does not carry'),
  ]
  assert material.inferred_fields({'unit': ['A']}, 'horizon') == []
  assert material.inferred_fields({'editorial': {'basis': 'x'}}, 'locality') == []
  assert material.inferred_fields(None, 'locality') == []
  rng = {'series': 'X', 'editorial': {'inferred': ['period']}}
  assert material.inferred_fields(rng, 'range') == [
    ('error', '`editorial.inferred` names `period`, which the range does not carry'),
  ]


def test_inferred_is_checked_on_ranges_horizons_and_localities():
  node = {'ranges': [{'series': 'X', 'editorial': {'inferred': ['period']}}]}
  assert material.range_tentatives(node) == [
    ('error', '`editorial.inferred` names `period`, which the range does not carry'),
  ]
  records = _records(
    {'h': {'unit': ['A'], 'editorial': {'inferred': ['stage']}}},
    {'l': {'location': ['A'], 'editorial': {'inferred': ['location', 'mapSheet']}}},
  )
  assert material.record_tentatives(records) == [
    (
      'error',
      'horizon "h": `editorial.inferred` names `stage`, which the horizon does not carry',
    ),
    (
      'error',
      'locality "l": `editorial.inferred` names `mapSheet`, which the locality does not carry',
    ),
  ]


# -- unreferenced_file_records ------------------------------------------------


def test_unreferenced_file_records_empty_when_none_declared():
  assert material.unreferenced_file_records({'taxonomies': []}) == []


def test_unreferenced_file_records_warns_on_the_unused_one_of_each_side():
  document = {
    'horizons': {'used': {}, 'unused-one': {}},
    'localities': {'used': {}, 'unused-two': {}},
    'taxonomies': [
      {'taxon': 'a', 'material': [{'label': 'A', 'horizon': 'used', 'locality': 'used'}]}
    ],
  }
  assert material.unreferenced_file_records(document) == [
    ('warning', 'horizon "unused-one" is defined but referred to by no entry or occurrence'),
    ('warning', 'locality "unused-two" is defined but referred to by no entry or occurrence'),
  ]


def test_unreferenced_file_records_an_occurrence_refers_too():
  document = {
    'horizons': {'h': {}},
    'localities': {'l': {}},
    'taxonomies': [{'taxon': 'a', 'occurrences': [{'horizon': 'h'}, {'locality': 'l'}]}],
  }
  assert material.unreferenced_file_records(document) == []


def test_unreferenced_file_records_all_referenced_is_quiet():
  document = {
    'horizons': {'used': {}},
    'taxonomies': [{'taxon': 'a', 'material': [{'label': 'A', 'horizon': 'used'}]}],
  }
  assert material.unreferenced_file_records(document) == []


# -- figure_refs ---------------------------------------------------------------


def test_figure_refs_label_match_is_quiet():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'A'}]}
  assert material.figure_refs(node) == []


def test_figure_refs_range_endpoint_matches():
  node = {
    'material': [{'prefix': 'GSC', 'numbers': [[1, 5]]}],
    'illustrations': [{'plate': 1, 'of': 5}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_no_match_is_error():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'B'}]}
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "B" matches 0 material entries, not 1'),
  ]


def test_figure_refs_several_matches_is_error():
  node = {
    'material': [{'label': 'A'}, {'numbers': ['A']}],
    'illustrations': [{'plate': 1, 'of': 'A'}],
  }
  assert material.figure_refs(node) == [
    (
      'error',
      'figure "of" value "A" matches 2 material entries, not 1; '
      '`{number, prefix}` or `{label}` picks one',
    ),
  ]


def test_figure_refs_list_of_and_no_of_field():
  node = {
    'material': [{'label': 'A'}, {'label': 'B'}],
    'illustrations': [{'plate': 1, 'of': ['A', 'B']}, {'plate': 2}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_cited_entry_is_not_read():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'B'}]}
  assert material.figure_refs(node, is_cited=True) == []


def test_figure_refs_number_inside_a_run_matches():
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [[582, 587]]}, {'prefix': 'MCZ', 'numbers': [600]}],
    'illustrations': [{'plate': 1, 'of': [584, '582A', 585]}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_integer_run_of_five_digits():
  node = {
    'material': [{'prefix': 'GSC', 'numbers': [[25935, 25961]]}],
    'illustrations': [{'plate': 1, 'of': 25940}],
  }
  assert material.figure_refs(node) == []


def test_figure_refs_letter_run_matches_case_sensitively():
  node = {
    'material': [{'prefix': 'GSC', 'numbers': [['10088c', '10088h']]}],
    'illustrations': [{'plate': 1, 'of': '10088d'}, {'plate': 2, 'of': '10088D'}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "10088D" matches 0 material entries, not 1'),
  ]


@pytest.mark.parametrize('value', ['581', '588', 'GM 584', '584-5', 'x584', '10088b', '10089d'])
def test_figure_refs_outside_a_run_or_of_another_stem_is_error(value):
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [[582, 587], ['10088c', '10088h']]}],
    'illustrations': [{'plate': 1, 'of': value}],
  }
  assert material.figure_refs(node) == [
    ('error', f'figure "of" value "{value}" matches 0 material entries, not 1'),
  ]


def test_figure_refs_a_run_with_a_suffixed_endpoint_is_not_an_integer_run():
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [['582A', 587]]}],
    'illustrations': [{'plate': 1, 'of': 584}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "584" matches 0 material entries, not 1'),
  ]


def test_figure_refs_exact_match_beats_a_run_containing_the_number():
  node = {
    'material': [{'prefix': 'MCZ', 'numbers': [[582, 587]]}, {'prefix': 'MCZ', 'numbers': [584]}],
    'illustrations': [{'plate': 1, 'of': 584}],
  }
  assert material.figure_refs(node) == []
  assert [e['numbers'] for e in material.entries_named(node['material'], 584)] == [[584]]


def test_figure_refs_two_runs_containing_the_number_is_error():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': [[582, 587]]},
      {'prefix': 'MCZ', 'numbers': [[584, 590]]},
    ],
    'illustrations': [{'plate': 1, 'of': 585}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "585" matches 2 material entries, not 1'),
  ]


def test_figure_refs_object_of_disambiguates_prefix():
  node = {
    'material': [
      {'prefix': 'GK', 'numbers': [112]},
      {'prefix': 'GTB', 'numbers': [112, [200, 210]]},
      {'label': 'the slab'},
    ],
    'illustrations': [{'plate': 1, 'of': 112}],
  }
  assert material.figure_refs(node) == [
    (
      'error',
      'figure "of" value "112" matches 2 material entries, not 1; '
      '`{number, prefix}` or `{label}` picks one',
    ),
  ]
  # The object form picks by prefix, by a number inside a run, or by label.
  node['illustrations'] = [
    {'plate': 1, 'of': {'number': 112, 'prefix': 'GK'}},
    {'plate': 2, 'of': [{'number': '112', 'prefix': 'GTB'}, {'number': 205, 'prefix': 'GTB'}]},
    {'plate': 3, 'of': {'label': 'the slab'}},
  ]
  assert material.figure_refs(node) == []
  assert (
    material.entries_named(node['material'], {'number': 112, 'prefix': 'GK'})
    == (node['material'][:1])
  )
  # Without a prefix the object form reads as the bare number, numbers only.
  assert material.entries_named(node['material'], {'number': 112}) == node['material'][:2]
  assert material.entries_named(node['material'], {'number': 'the slab'}) == []
  assert material.entries_named(node['material'], {'label': '112'}) == []
  # A prefix no entry of that number carries matches nothing, named as words.
  node['illustrations'] = [{'plate': 1, 'of': {'number': 112, 'prefix': 'MCZ'}}]
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "MCZ 112" matches 0 material entries, not 1'),
  ]
  # Two runs under one prefix get no hint: the object form would not help.
  node = {
    'material': [{'prefix': 'GTB', 'numbers': [[1, 5]]}, {'prefix': 'GTB', 'numbers': [[3, 9]]}],
    'illustrations': [{'plate': 1, 'of': 4}],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "4" matches 2 material entries, not 1'),
  ]


# -- cast_refs -------------------------------------------------------------------


def test_cast_refs_matches_a_number_label_or_range_endpoint():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 199},
      {'prefix': 'PE', 'numbers': [199]},
      {'prefix': 'MCZ', 'numbers': [700], 'castOf': 'the holotype'},
      {'label': 'the holotype'},
      {'prefix': 'MCZ', 'numbers': [800], 'castOf': 205},
      {'prefix': 'PE', 'numbers': [[201, 205]]},
    ],
  }
  assert material.cast_refs(node) == []


def test_cast_refs_number_inside_a_run_matches_and_exact_wins():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 203},
      {'prefix': 'PE', 'numbers': [[201, 205]]},
      {'prefix': 'MCZ', 'numbers': [800], 'castOf': 204},
      {'prefix': 'PE', 'numbers': [[204, 210]]},
    ],
  }
  assert material.cast_refs(node) == []
  node['material'].append({'prefix': 'PE', 'numbers': [[202, 206]]})
  assert material.cast_refs(node) == [
    ('error', 'castOf "203" matches 2 material entries, not 1'),
  ]


def test_cast_refs_no_match_is_error():
  node = {'material': [{'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 199}]}
  assert material.cast_refs(node) == [('error', 'castOf "199" matches 0 material entries, not 1')]


def test_cast_refs_several_matches_is_error():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': 199},
      {'prefix': 'PE', 'numbers': [199]},
      {'label': '199'},
    ],
  }
  assert material.cast_refs(node) == [
    (
      'error',
      'castOf "199" matches 2 material entries, not 1; `{number, prefix}` or `{label}` picks one',
    )
  ]


def test_cast_refs_own_entry_is_error():
  node = {'material': [{'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': '629A'}]}
  assert material.cast_refs(node) == [('error', 'castOf "629A" names the entry itself')]


def test_cast_and_fragment_refs_object_form():
  entries = [
    {'prefix': 'GK', 'numbers': [112]},
    {'prefix': 'GTB', 'numbers': [112]},
    {'prefix': 'MCZ', 'numbers': ['629A'], 'castOf': {'number': 112, 'prefix': 'GTB'}},
    {'prefix': 'MCZ', 'numbers': ['629B'], 'fragmentOf': {'number': 112, 'prefix': 'GK'}},
  ]
  assert material.cast_refs({'material': entries}) == []
  node = _node(
    {'prefix': 'GK', 'numbers': [112]},
    {'prefix': 'GTB', 'numbers': [112]},
    {'prefix': 'MCZ', 'numbers': [1], 'fragmentOf': 112},
    {'prefix': 'MCZ', 'numbers': [2], 'fragmentOf': {'number': 112, 'prefix': 'QQ'}},
    {'prefix': 'MCZ', 'numbers': [3], 'fragmentOf': {'number': 3, 'prefix': 'MCZ'}},
    {'prefix': 'MCZ', 'numbers': [4], 'castOf': {'label': 'A'}, 'fragmentOf': {'label': 'A'}},
    {'label': 'A'},
  )
  assert material.cast_refs(node) == [
    (
      'error',
      'fragmentOf "112" matches 2 material entries, not 1; '
      '`{number, prefix}` or `{label}` picks one',
    ),
    ('error', 'fragmentOf "QQ 112" matches 0 material entries, not 1'),
    ('error', 'fragmentOf "MCZ 3" names the entry itself'),
  ]


def test_cast_refs_absent_castof_and_absent_material_are_quiet():
  assert material.cast_refs({'material': [{'label': 'A'}]}) == []
  assert material.cast_refs({}) == []


# -- null_material --------------------------------------------------------------


@pytest.mark.parametrize('field', ['material', 'occurrences', 'ranges'])
def test_null_material_cited_entry_with_any_field_is_error(field):
  node = {field: None}
  assert material.null_material(node, is_cited=True) == [
    ('error', f'cited entry carries `{field}`'),
  ]


@pytest.mark.parametrize('field', ['horizons', 'localities'])
def test_null_material_cited_entry_with_a_record_map_is_error(field):
  # The cited work's own horizons and localities are not this source's.
  node = {field: {'x': {'unit': ['A']}}}
  assert material.null_material(node, is_cited=True) == [
    ('error', f'cited entry carries `{field}`'),
  ]
  assert material.null_material(node, is_cited=False) == []


def test_null_material_not_cited_is_quiet():
  node = {'material': None, 'illustrations': None, 'occurrences': None, 'ranges': None}
  assert material.null_material(node, is_cited=False) == []


def test_null_ranges_is_accepted_on_a_primary_node_and_rejected_on_a_cited_entry():
  node = {'ranges': None}
  assert material.null_material(node, is_cited=False) == []
  assert material.null_material(node, is_cited=True) == [
    ('error', 'cited entry carries `ranges`'),
  ]


LOCATORS_GO_INSIDE = "; the cited work's locators go inside `authority`"


def test_null_material_cited_entry_carries_its_locators_in_authority():
  locators = {'illustrations': [{'plate': 15, 'figures': [1, 3, 4], 'uncertain': True}]}
  assert material.null_material({'authority': locators}, is_cited=True) == []
  assert material.null_material({'authority': {**locators, 'pages': 5}}, is_cited=True) == []
  assert material.null_material(locators, is_cited=True) == [
    ('error', 'cited entry carries `illustrations`' + LOCATORS_GO_INSIDE),
  ]
  assert material.null_material({'pages': 5}, is_cited=True) == [
    ('error', 'cited entry carries `pages`' + LOCATORS_GO_INSIDE),
  ]


def test_null_material_cited_entry_with_null_illustrations_is_error():
  assert material.null_material({'illustrations': None}, is_cited=True) == [
    ('error', 'cited entry carries `illustrations`' + LOCATORS_GO_INSIDE),
  ]


def test_null_material_primary_node_authority_with_locators_alone_is_error():
  node = {'authority': {'pages': 5}}
  assert material.null_material(node, is_cited=True) == []
  assert material.null_material(node, is_cited=False) == [
    (
      'error',
      "primary node's `authority` carries locators alone; its own page and figures sit on it",
    ),
  ]
  assert material.null_material({'authority': {'source': 'x', 'pages': 5}}, is_cited=False) == []
  assert material.null_material({'authority': {}}, is_cited=False) == []


def test_null_material_cited_entry_illustration_with_of_is_error():
  node = {'authority': {'illustrations': [{'plate': 1, 'of': 'A'}, {'plate': 2}]}}
  assert material.null_material(node, is_cited=True) == [
    ('error', '`authority.illustrations` entry carries `of`'),
  ]


def test_null_material_cited_entry_illustration_with_depicts_is_error():
  node = {'authority': {'illustrations': [{'plate': 1, 'depicts': 'cast'}]}}
  assert material.null_material(node, is_cited=True) == [
    ('error', '`authority.illustrations` entry carries `depicts`'),
  ]


def test_null_material_cited_entry_reports_each_offending_entry():
  figures = [{'plate': 1, 'of': 'A', 'depicts': 'cast'}, {'plate': 2, 'of': 'B'}]
  assert len(material.null_material({'authority': {'illustrations': figures}}, is_cited=True)) == 3


@pytest.mark.parametrize('is_cited', [False, True])
def test_null_material_authority_illustration_with_of_is_error(is_cited):
  node = {'authority': {'source': 'x', 'illustrations': [{'plate': 1, 'of': 'A'}]}}
  assert material.null_material(node, is_cited=is_cited) == [
    ('error', '`authority.illustrations` entry carries `of`'),
  ]


def test_null_material_authority_illustration_with_depicts_is_error():
  node = {'authority': {'source': 'x', 'illustrations': [{'plate': 1, 'depicts': 'drawing'}]}}
  assert material.null_material(node, is_cited=False) == [
    ('error', '`authority.illustrations` entry carries `depicts`'),
  ]


def test_null_material_authority_locators_without_of_are_quiet():
  node = {'authority': {'source': 'x', 'illustrations': [{'plate': 1, 'figures': 2}]}}
  assert material.null_material(node, is_cited=False) == []


def test_null_material_null_beside_figure_of_is_error():
  node = {'material': None, 'illustrations': [{'plate': 1, 'of': 'A'}]}
  assert material.null_material(node, is_cited=False) == [
    ('error', '`material: null` beside a figure whose `of` names one'),
  ]


def test_null_material_not_null_beside_figure_of_is_quiet():
  node = {'material': [{'label': 'A'}], 'illustrations': [{'plate': 1, 'of': 'A'}]}
  assert material.null_material(node, is_cited=False) == []


def test_null_material_absent_is_quiet():
  assert material.null_material({}, is_cited=False) == []


def test_null_synonyms_on_a_cited_entry_is_error():
  assert material.null_material({'synonyms': None}, is_cited=True) == [
    ('error', 'cited entry carries `synonyms: null`'),
  ]


def test_null_synonyms_beside_a_non_list_is_error():
  node = {'synonyms': None, 'non': [{'taxon': 'a'}]}
  assert material.null_material(node, is_cited=False) == [
    ('error', '`synonyms: null` beside a `non` list'),
  ]


def test_null_synonyms_alone_is_quiet_on_a_primary_node():
  assert material.null_material({'synonyms': None}, is_cited=False) == []
  assert material.null_material({'synonyms': None, 'non': []}, is_cited=False) == []


def test_a_synonyms_list_on_a_cited_entry_is_quiet():
  # A nested synonymy exists; only the null is an error.
  node = {'synonyms': [{'taxon': 'a'}], 'non': [{'taxon': 'b'}]}
  assert material.null_material(node, is_cited=True) == []


# -- unused_fields ---------------------------------------------------------------


def test_unused_fields_none_declared_is_quiet():
  document = {'taxonomies': [{'taxon': 'a', 'ranges': None}]}
  assert material.unused_fields(document) == []


def test_unused_fields_flags_the_node_that_still_carries_it():
  document = {
    'unused': ['ranges'],
    'taxonomies': [
      {'taxon': 'a', 'ranges': None, 'children': [{'taxon': 'b'}]},
    ],
  }
  assert material.unused_fields(document) == [
    ('error', '`ranges` is listed as `unused` but appears at 0'),
  ]


def test_unused_ranges_with_a_node_carrying_ranges_is_error():
  document = {
    'unused': ['ranges'],
    'taxonomies': [{'taxon': 'a', 'ranges': [{'period': 'Ordovician'}]}],
  }
  assert material.unused_fields(document) == [
    ('error', '`ranges` is listed as `unused` but appears at 0'),
  ]


@pytest.mark.parametrize('value', [None, [{'taxon': 'b'}]])
def test_unused_synonyms_with_a_node_carrying_it_is_error(value):
  document = {'unused': ['synonyms'], 'taxonomies': [{'taxon': 'a', 'synonyms': value}]}
  assert material.unused_fields(document) == [
    ('error', '`synonyms` is listed as `unused` but appears at 0'),
  ]


def test_unused_fields_ignores_nodes_without_it():
  document = {'unused': ['ranges'], 'taxonomies': [{'taxon': 'a', 'children': [{'taxon': 'b'}]}]}
  assert material.unused_fields(document) == []


def test_unused_illustrations_tolerates_a_cited_entrys_locators():
  # A cited entry's locators sit in its `authority`, which is not the field.
  synonym = {'taxon': 'b', 'authority': {'illustrations': [{'plate': 1}]}}
  document = {'unused': ['illustrations'], 'taxonomies': [{'taxon': 'a', 'synonyms': [synonym]}]}
  assert material.unused_fields(document) == []


def test_unused_illustrations_flags_a_primary_node_even_with_null():
  document = {
    'unused': ['illustrations'],
    'taxonomies': [
      {
        'taxon': 'a',
        'synonyms': [{'taxon': 'b', 'authority': {'illustrations': [{'plate': 1}]}}],
        'children': [{'taxon': 'c', 'illustrations': None}],
      },
    ],
  }
  assert material.unused_fields(document) == [
    ('error', '`illustrations` is listed as `unused` but appears at 0/children/0'),
  ]


# -- walk_document ------------------------------------------------------------


def test_walk_document_paths_and_cited_flags():
  document = {
    'taxonomies': [
      {
        'taxon': 'a',
        'synonyms': [{'taxon': 'b', 'children': [{'taxon': 'c'}]}],
        'children': [{'taxon': 'd'}],
      },
    ],
    'phylogenies': [{'treeType': 'cladogram', 'tree': {'taxon': 'e'}}],
  }
  seen = {
    path: (node.get('taxon'), cited) for path, node, cited in material.walk_document(document)
  }
  assert seen == {
    '0': ('a', False),
    '0/synonyms/0': ('b', True),
    '0/synonyms/0/children/0': ('c', False),
    '0/children/0': ('d', False),
    '1': ('e', False),
  }


def test_walk_document_ignores_non_dict_and_absent_axes():
  assert list(material.walk_document({})) == []
  assert list(material.walk_document({'taxonomies': [None]})) == []


# -- Tree.file_horizons / file_localities / file_unused / horizons / localities -


def test_tree_file_records_and_unused_read_from_root_metadata(records):
  # No `taxon` field: only a registered source is needed (`Tree` hashes by
  # it), which the corpus provides for source key '1961_dehm'.
  metadata = {
    'source_key': '1961_dehm',
    'position': 900,
    'type': 'taxonomy',
    'file_horizons': {'loc': {}},
    'file_localities': {'site': {}},
    'file_unused': ('ranges',),
  }
  root = Tree({'children': [{}]}, metadata, corpus=records)
  assert root.file_horizons == {'loc': {}}
  assert root.file_localities == {'site': {}}
  assert root.file_unused == ('ranges',)
  child = root.children[0]
  assert child.file_horizons == {'loc': {}}
  assert child.file_localities == {'site': {}}
  assert child.file_unused == ('ranges',)


def test_tree_records_merge_node_over_file_with_scope(records):
  metadata = {
    'source_key': '1961_dehm',
    'position': 901,
    'type': 'taxonomy',
    'file_horizons': {'loc': {'unit': ['a']}, 'file-only': {}},
    'file_localities': {'loc': {'location': ['a']}, 'site': {}},
  }
  root = Tree(
    {'horizons': {'loc': {'unit': ['b']}}, 'localities': {'new': {'location': ['c']}}},
    metadata,
    corpus=records,
  )
  assert root.horizons == {'loc': {'unit': ['b']}, 'file-only': {}}
  assert root.localities == {'loc': {'location': ['a']}, 'site': {}, 'new': {'location': ['c']}}
  assert root.record_scope('horizons', 'loc') == 'node'
  assert root.record_scope('horizons', 'file-only') == 'file'
  # The same key on the other side is its own record.
  assert root.record_scope('localities', 'loc') == 'file'
  assert root.record_scope('localities', 'new') == 'node'


def test_tree_file_records_default_when_absent(records):
  metadata = {'source_key': '1961_dehm', 'position': 902, 'type': 'taxonomy'}
  root = Tree({}, metadata, corpus=records)
  assert root.file_horizons == {} and root.file_localities == {}
  assert root.file_unused == ()
  assert root.horizons == {} and root.localities == {}
  assert root.record_scope('horizons', 'x') == 'file'


def test_source_year_puts_a_work_in_preparation_last():
  # `same_as_links` orders sources by this; a work in preparation sorts
  # after every published one, and its `year` is never read.
  assert material.source_year(None) is None
  assert material.source_year(types.SimpleNamespace(in_preparation=False, year=1897)) == 1897
  assert material.source_year(types.SimpleNamespace(in_preparation=True)) == 9999


# -- loader wiring (`load.py`'s `_report_material`) ---------------------------


def test_load_reports_material_checks_at_the_right_level(records, caplog):
  from phylohist.loader.load import _report_material

  data = {
    'repositories': {'gm': _entry('GM'), 'cyc': _entry('CYC', within='cyc')},
    'trees': {
      '_synthetic_source': {
        'horizons': {'stray': {}},
        'unused': ['ranges'],
        'prefixes': {'GM': 'gm'},
        'taxonomies': [
          {
            'taxon': 'cyathocystis',
            'ranges': None,
            'material': [
              {'prefix': 'GM', 'numbers': [1], 'horizon': 'missing-ctx'},
              {'prefix': 'GM', 'numbers': [3], 'castOf': 2},
              {'numbers': [4], 'repository': 'nowhere'},
            ],
            'illustrations': [{'plate': 1, 'of': 'nope'}],
            'synonyms': [{'taxon': 'cyathocystis', 'occurrences': None}],
          },
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material(support.with_documents(records, data))
  warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert any('_synthetic_source' in m and 'horizon "stray"' in m for m in warnings)
  assert any('`ranges` is listed as `unused`' in m for m in errors)
  assert any('horizon "missing-ctx" is not defined' in m for m in errors)
  assert any('figure "of" value "nope"' in m for m in errors)
  assert any('cited entry carries `occurrences`' in m for m in errors)
  assert any('castOf "2" matches 0' in m for m in errors)
  assert any('repositories: `within` cycles: cyc -> cyc' in m for m in errors)
  assert any(
    '_synthetic_source at 0' in m and 'repository "nowhere" is not a key of the registry' in m
    for m in errors
  )
  assert sum('repository "nowhere"' in m for m in errors) == 1


def test_load_reports_tentative_on_ranges_horizons_and_localities(records, caplog):
  from phylohist.loader.load import _report_material

  data = {
    'trees': {
      '_synthetic_source': {
        'horizons': {'f': {'biozone': 'X', 'tentative': True}},
        'localities': {'g': {'location': ['Q'], 'tentative': True}},
        'taxonomies': [
          {
            'taxon': 'a',
            'horizons': {'n': {'tentative': ['biozone']}},
            'localities': {'m': {'tentative': ['location']}},
            'occurrences': [{'horizon': 'n', 'locality': 'm'}, {'horizon': 'f', 'locality': 'g'}],
            'ranges': [{'period': 'Y', 'tentative': ['series']}],
          },
        ],
      },
    },
  }
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _report_material(support.with_documents(records, data))
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert any(m.startswith('_synthetic_source: horizon "f": a file-level horizon') for m in errors)
  assert any(m.startswith('_synthetic_source: locality "g": a file-level locality') for m in errors)
  assert any(
    m.startswith('_synthetic_source at 0: horizon "n": `tentative` names `biozone`') for m in errors
  )
  assert any(
    m.startswith('_synthetic_source at 0: locality "m": `tentative` names `location`')
    for m in errors
  )
  assert any(
    m.startswith('_synthetic_source at 0: `tentative` names `series`, which the range')
    for m in errors
  )


def test_load_reports_the_occurrence_checks(records, caplog):
  from phylohist.loader.load import _report_material

  data = {
    'trees': {
      '_synthetic_source': {
        'horizons': {'shared': {'unit': ['A']}, 'file-stray': {'unit': ['B']}},
        'localities': {'shared': {'location': ['C']}},
        'taxonomies': [
          {
            'taxon': 'a',
            # Each side shadows the file's, and a node record nothing refers to.
            'horizons': {'shared': {'unit': ['A2']}, 'stray-h': {'unit': ['D']}},
            'localities': {'shared': {'location': ['C2']}, 'stray-l': {'location': ['E']}},
            'material': [
              {
                'label': 'A',
                'horizon': 'shared',
                'locality': 'shared',
                'tentative': ['horizon', 'locality'],
              },
              {'label': 'B', 'horizon': 'shared', 'tentative': ['locality']},
            ],
            'occurrences': [{'horizon': 'shared', 'tentative': ['locality']}],
          },
          {'taxon': 'b', 'occurrences': [{'locality': 'nowhere'}]},
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material(support.with_documents(records, data))
  warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert (
    '_synthetic_source at 0: horizon "shared" on the node shadows a file-level horizon' in warnings
  )
  assert (
    '_synthetic_source at 0: locality "shared" on the node shadows a file-level locality'
    in warnings
  )
  assert (
    '_synthetic_source at 0: horizon "stray-h" is defined on the node and referred to by '
    'nothing on it' in errors
  )
  assert (
    '_synthetic_source at 0: locality "stray-l" is defined on the node and referred to by '
    'nothing on it' in errors
  )
  tentative = '`tentative` names `locality`, which the entry does not carry'
  assert sum(m == f'_synthetic_source at 0: {tentative}' for m in errors) == 2
  assert (
    '_synthetic_source at 1: locality "nowhere" is not defined on the node or the file' in errors
  )
  # The file-level `file-stray` horizon nothing refers to is a warning.
  assert any('horizon "file-stray" is defined but referred to by no entry' in m for m in warnings)


def test_load_reports_editorial_inferred_naming_an_absent_field(records, caplog):
  from phylohist.loader.load import _report_material

  data = {
    'trees': {
      '_synthetic_source': {
        'horizons': {'f': {'unit': ['A'], 'editorial': {'inferred': ['stage']}}},
        'taxonomies': [
          {
            'taxon': 'a',
            'localities': {'n': {'location': ['B'], 'editorial': {'inferred': ['mapSheet']}}},
            'occurrences': [{'horizon': 'f', 'locality': 'n'}],
            'ranges': [{'period': 'Cambrian', 'editorial': {'inferred': ['series']}}],
          },
        ],
      },
    },
  }
  with caplog.at_level(logging.ERROR, logger='phylohist'):
    _report_material(support.with_documents(records, data))
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert (
    '_synthetic_source: horizon "f": `editorial.inferred` names `stage`, which the horizon '
    'does not carry' in errors
  )
  assert (
    '_synthetic_source at 0: locality "n": `editorial.inferred` names `mapSheet`, which the '
    'locality does not carry' in errors
  )
  assert (
    '_synthetic_source at 0: `editorial.inferred` names `series`, which the range does not '
    'carry' in errors
  )


# -- scripts/check_draft.py ---------------------------------------------------


def _run_check_draft(path):
  return support.run_check_draft(path)


def test_check_draft_runs_as_a_program(tmp_path):
  # The script itself, as CI runs it over `drafts/`: a draft the schema
  # rejects exits 1.
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- rnak: genus\n')
  result = subprocess.run(
    [sys.executable, str(SCRIPTS / 'check_draft.py'), str(draft)],
    capture_output=True,
    text=True,
  )
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'not valid against the tree schema' in result.stdout


def test_check_draft_exits_zero_on_a_clean_draft(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: cyathocystis\n')
  result = _run_check_draft(draft)
  assert result.returncode == 0, result.stdout + result.stderr


def test_check_draft_exits_one_on_material_null_on_a_cited_entry(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  synonyms:\n'
    '  - taxon: cyathocystidae\n'
    '    material: null\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'cited entry carries `material`' in result.stdout


def test_check_draft_exits_one_on_a_tentative_naming_an_absent_field(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'horizons:\n  f:\n    tentative: true\n'
    'localities:\n  g:\n    tentative: true\n'
    'taxonomies:\n- taxon: cyathocystis\n'
    '  occurrences:\n  - {horizon: f, locality: g}\n'
    '  ranges:\n  - period: Cambrian\n    tentative: [series]\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'a file-level horizon cannot be `tentative: true`' in result.stdout
  assert 'a file-level locality cannot be `tentative: true`' in result.stdout
  assert '`tentative` names `series`, which the range does not carry' in result.stdout


def test_check_draft_exits_one_on_illustrations_null_on_a_primary_node(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: cyathocystis\n  illustrations: null\n')
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'draft carries `illustrations: null`' in result.stdout


def test_check_draft_exits_one_on_synonyms_null_on_a_primary_node(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text('taxonomies:\n- taxon: cyathocystis\n  synonyms: null\n')
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'draft carries `synonyms: null`' in result.stdout


def test_check_draft_exits_one_on_synonyms_null_on_a_cited_entry(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  synonyms:\n'
    '  - taxon: cyathocystidae\n'
    '    synonyms: null\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'cited entry carries `synonyms: null`' in result.stdout


def test_check_draft_exits_one_on_synonyms_null_beside_non(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n- taxon: cyathocystis\n  non:\n  - taxon: cyathocystidae\n  synonyms: null\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert '`synonyms: null` beside a `non` list' in result.stdout


def test_check_draft_exits_one_on_of_in_a_cited_entrys_illustrations(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n'
    '- taxon: cyathocystis\n'
    '  synonyms:\n'
    '  - taxon: cyathocystidae\n'
    '    authority:\n'
    '      illustrations:\n'
    '      - plate: 1\n'
    '        of: A\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert '`authority.illustrations` entry carries `of`' in result.stdout


def test_check_draft_exits_one_on_a_cited_entrys_node_level_pages(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n- taxon: cyathocystis\n  synonyms:\n  - taxon: cyathocystidae\n    pages: 5\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert (
    "cited entry carries `pages`; the cited work's locators go inside `authority`" in result.stdout
  )


def test_check_draft_warns_on_a_locality_number_with_no_register_and_is_quiet_with_one(tmp_path):
  body = (
    'localities:\n  a:\n    localityNumbers: [{number: SH-1}]\n'
    'taxonomies:\n- taxon: cyathocystis\n  localities:\n    b:\n'
    '      localityNumbers: [{number: IK-3}]\n'
    '  occurrences:\n  - {locality: a}\n  - {locality: b}\n'
  )
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(body)
  result = _run_check_draft(draft)
  assert result.stdout.count('has no register') == 2, result.stdout
  assert 'warning: locality number "SH-1"' in result.stdout
  assert 'warning: 0: locality number "IK-3"' in result.stdout

  draft.write_text('localityRegister: sprinkle-l\n' + body)
  result = _run_check_draft(draft)
  assert 'has no register' not in result.stdout, result.stdout


def test_check_draft_exits_one_on_an_explicit_repository_that_is_no_registry_key(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'taxonomies:\n- taxon: cyathocystis\n  material:\n  - {numbers: [1], repository: GSC}\n',
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  assert 'repository "GSC" is not a key of the registry' in result.stdout


@pytest.mark.production
def test_roles_registry_matches_the_schema_enum():
  # Every role the schema allows is documented, and nothing else is; an
  # `equivalent` names another documented role.
  schema = io.load_yaml(io.SCHEMA_PATH)
  roles = io.load_yaml(io.DATA_DIR / 'roles.yaml')
  assert set(roles) == set(schema['$defs']['role']['enum'])
  for name, entry in roles.items():
    equivalent = entry.get('equivalent')
    assert equivalent is None or (equivalent in roles and equivalent != name), name


# -- the `prefix` + `numbers` shape --------------------------------------------


@pytest.fixture
def numbered(registers):
  """`registers` plus a register that lists its prefix, a collection that
  lists none, and an institution of the same name as one of its series."""
  return {
    **registers,
    'mcz-bare': {'name': 'x', 'type': 'collection', 'within': 'mcz', 'subject': 'specimens'},
    'nhmuk-ee': {
      'name': 'x',
      'type': 'collection',
      'within': 'nhmuk',
      'subject': 'specimens',
      'prefixes': ['EE'],
      'otherNames': ['Reg  E E'],
    },
  }


def _node(*entries, **extra):
  return {'material': list(entries), **extra}


def test_number_entries_prefix_missing_from_the_map_is_error(numbered):
  node = _node({'prefix': 'XX', 'numbers': [1]})
  assert material.number_entries(node, {'MCZ': 'mcz'}, numbered) == [
    ('error', 'prefix "XX" is not in the file\'s `prefixes` map'),
  ]
  assert material.number_entries(node, {'XX': 'mcz'}, numbered) == []
  # No map at all is the same error.
  assert material.number_entries(node, {}, numbered)[0][0] == 'error'


def test_number_entries_numbers_need_a_prefix_a_repository_or_a_holder(numbered):
  assert material.number_entries(_node({'numbers': ['5']}), {}, numbered) == [
    ('error', 'numbers with no prefix, repository or holder'),
  ]
  for entry in (
    {'numbers': ['5'], 'repository': 'gsc'},
    {'numbers': ['5'], 'holder': 'A. R. Palmer'},
    {'numbers': ['5'], 'prefix': 'GSC'},
  ):
    assert material.number_entries(_node(entry), {'GSC': 'gsc'}, numbered) == []


def test_number_entries_a_number_that_begins_with_its_registers_prefix_warns(numbered):
  prefixes = {'EE': 'nhmuk-ee', 'F.': 'uq-f'}
  node = _node(
    {'prefix': 'EE', 'numbers': ['EE16642', 'EE-1', 'EE.2', 'ee 3', 'reg e e 4', ['EE5', 7]]},
    {'prefix': 'F.', 'numbers': ['F. 5404', 'F5405', 'FE 6']},
  )
  assert material.number_entries(node, prefixes, numbered) == [
    ('warning', f'number "{n}" begins with a prefix of its register "{r}"')
    for r, n in (
      ('nhmuk-ee', 'EE16642'),
      ('nhmuk-ee', 'EE-1'),
      ('nhmuk-ee', 'EE.2'),
      ('nhmuk-ee', 'ee 3'),
      ('nhmuk-ee', 'reg e e 4'),
      ('nhmuk-ee', 'EE5'),
      ('uq-f', 'F. 5404'),
      ('uq-f', 'F5405'),
    )
  ]


def test_number_entries_a_clean_number_and_other_cases_are_quiet(numbered):
  prefixes = {'EE': 'nhmuk-ee', 'MCZ': 'mcz-bare'}
  node = _node(
    {'prefix': 'EE', 'numbers': ['16642', 16643, 'EEx1', [10, 12]]},
    # A register that lists no form has nothing to begin with.
    {'prefix': 'MCZ', 'numbers': ['MCZ 1']},
  )
  assert material.number_entries(node, prefixes, numbered) == []
  assert material.number_entries({}, prefixes, numbered) == []


def test_number_entries_reads_the_explicit_repository_register_too(numbered):
  node = _node({'prefix': 'USNM', 'numbers': ['EE 1'], 'repository': 'nhmuk-ee'})
  assert material.number_entries(node, {'USNM': 'usnm'}, numbered) == [
    ('warning', 'number "EE 1" begins with a prefix of its register "nhmuk-ee"'),
  ]


def test_number_entries_an_explicit_repository_is_a_registry_key_reported_once(numbered):
  node = _node(
    {'numbers': ['1'], 'repository': 'nope'},
    # A label entry has no numbers to check, but its repository is still read.
    {'label': 'A', 'repository': 'nowhere'},
    # `GM` is a prefix, not a key: only `gm` is.
    {'prefix': 'GM', 'numbers': [2], 'repository': 'GM'},
    {'count': 1, 'repository': 'gm'},
  )
  assert material.number_entries(node, {'GM': 'gm'}, numbered) == [
    ('error', 'repository "nope" is not a key of the registry'),
    ('error', 'repository "nowhere" is not a key of the registry'),
    ('error', 'repository "GM" is not a key of the registry'),
  ]


def _prefix_document(prefixes, *entries, **extra):
  return {'prefixes': prefixes, 'taxonomies': [{'taxon': 'a', 'material': list(entries)}], **extra}


def test_file_prefixes_clean_file_is_quiet(numbered):
  document = _prefix_document(
    {'MCZ': 'mcz', 'F.': 'uq-f', 'USGS': 'usgs-l', 'EE': 'nhmuk-ee'},
    {'prefix': 'MCZ', 'numbers': [1]},
    {'prefix': 'F.', 'numbers': [2]},
    {'prefix': 'EE', 'numbers': [3]},
    localities={'a': {'localityNumbers': [{'prefix': 'USGS', 'number': 1}]}},
    localityRegister='usgs-l',
  )
  assert material.file_prefixes(document, numbered) == []
  assert material.file_prefixes({'taxonomies': []}, numbered) == []


def test_file_prefixes_a_value_that_is_no_registry_key_is_error(numbered):
  document = _prefix_document({'MCZ': 'mcz-nowhere'}, {'prefix': 'MCZ', 'numbers': [1]})
  assert material.file_prefixes(document, numbered) == [
    ('error', 'prefix "MCZ" is mapped to "mcz-nowhere", which is not a key of the registry'),
  ]


def test_file_prefixes_a_prefix_nothing_uses_is_error(numbered):
  document = _prefix_document(
    {'MCZ': 'mcz', 'GM': 'gm', 'USGS': 'usgs-l', 'NMV': 'gm'},
    {'prefix': 'MCZ', 'numbers': [1]},
  )
  document['taxonomies'][0]['localities'] = {
    'b': {'localityNumbers': [{'prefix': 'USGS', 'number': 1}]}
  }
  assert [m for _, m in material.file_prefixes(document, numbered)] == [
    'prefix "GM" in the file\'s `prefixes` map is used by nothing',
    'prefix "NMV" is not a known form of "gm"',
    'prefix "NMV" in the file\'s `prefixes` map is used by nothing',
  ]


def test_file_prefixes_a_prefix_only_a_specimen_locality_uses_is_used(numbered):
  document = _prefix_document(
    {'MCZ': 'mcz', 'USGS': 'usgs-l'},
    {'prefix': 'MCZ', 'numbers': [1], 'localityNumbers': [{'prefix': 'USGS', 'number': 1}]},
  )
  assert material.file_prefixes(document, numbered) == []


def test_file_prefixes_a_prefix_the_register_does_not_list_is_warning(numbered):
  document = _prefix_document(
    {'MCZ': 'gm', 'U.S.N.M.': 'usnm', 'BMNH': 'nhmuk'},
    {'prefix': 'MCZ', 'numbers': [1]},
    {'prefix': 'U.S.N.M.', 'numbers': [2]},
    {'prefix': 'BMNH', 'numbers': [3]},
  )
  assert material.file_prefixes(document, numbered) == [
    ('warning', 'prefix "MCZ" is not a known form of "gm"'),
    ('warning', 'prefix "U.S.N.M." is not a known form of "usnm"'),
  ]


def test_file_prefixes_forms_compare_folded_with_a_trailing_period_ignored(numbered):
  document = _prefix_document(
    {'F.': 'uq-f', 'uqf': 'uq-f', 'Nhm  Uk': 'nhmuk', 'bmnh.': 'nhmuk'},
    *({'prefix': p, 'numbers': [1]} for p in ('F.', 'uqf', 'Nhm  Uk', 'bmnh.')),
  )
  assert material.file_prefixes(document, numbered) == []


def test_file_prefixes_a_register_with_no_forms_is_not_warned_about(numbered):
  # The registers for series a holder numbers separately list no prefix yet.
  document = _prefix_document({'PE': 'mcz-bare'}, {'prefix': 'PE', 'numbers': [1]})
  assert material.file_prefixes(document, numbered) == []


def test_file_prefixes_locality_register_must_be_a_registry_key(numbered):
  assert material.file_prefixes({'localityRegister': 'usgs-l'}, numbered) == []
  assert material.file_prefixes({'localityRegister': 'nope-l'}, numbered) == [
    ('error', 'localityRegister "nope-l" is not a key of the registry'),
  ]


def test_locality_objects(numbered):
  localities = {
    'a': {
      'localityNumbers': [
        {'number': 'FC-2'},
        {'prefix': 'USGS', 'number': '4148 CO'},
        {'prefix': 'ZZ', 'number': 1},
        {'register': 'usgs-l', 'number': 'D190d CO'},
        {'register': 'nope-l', 'number': 7},
      ]
    },
    'b': None,
  }
  prefixes = {'USGS': 'usgs-l'}
  assert material.locality_objects(localities, prefixes, None, numbered) == [
    ('warning', 'locality number "FC-2" has no register'),
    ('error', 'prefix "ZZ" is not in the file\'s `prefixes` map'),
    ('error', 'locality register "nope-l" is not a key of the registry'),
  ]
  # A file `localityRegister` gives the bare number its register.
  assert [
    m for _, m in material.locality_objects(localities, prefixes, 'sprinkle-l', numbered)
  ] == [
    'prefix "ZZ" is not in the file\'s `prefixes` map',
    'locality register "nope-l" is not a key of the registry',
  ]
  assert material.locality_objects(None, prefixes, None, numbered) == []


def test_locality_objects_reads_material_entries(numbered):
  entries = [
    {
      'prefix': 'MCZ',
      'numbers': [1],
      'localityNumbers': [
        {'number': 'FC-2'},
        {'prefix': 'ZZ', 'number': 1},
        {'register': 'nope-l', 'number': 7},
        {'prefix': 'USGS', 'number': '4148 CO'},
      ],
    },
    {'label': 'A'},
  ]
  prefixes = {'USGS': 'usgs-l', 'MCZ': 'mcz'}
  assert material.locality_objects(None, prefixes, None, numbered, entries) == [
    ('warning', 'locality number "FC-2" has no register'),
    ('error', 'prefix "ZZ" is not in the file\'s `prefixes` map'),
    ('error', 'locality register "nope-l" is not a key of the registry'),
  ]
  assert [
    m for _, m in material.locality_objects({}, prefixes, 'sprinkle-l', numbered, entries)
  ] == [
    'prefix "ZZ" is not in the file\'s `prefixes` map',
    'locality register "nope-l" is not a key of the registry',
  ]


# -- entries_named for the `prefix` + `numbers` shape ---------------------------


def test_entries_named_by_label_number_or_integer():
  entries = [
    {'prefix': 'MCZ', 'numbers': ['581A', 582, 'KR-2'], 'label': 'The Type'},
    {'prefix': 'MCZ', 'numbers': [600]},
  ]
  assert material.entries_named(entries, 'The Type') == entries[:1]
  assert material.entries_named(entries, 'the  type') == entries[:1]
  assert material.entries_named(entries, '581A') == entries[:1]
  assert material.entries_named(entries, '581a') == entries[:1]
  assert material.entries_named(entries, 582) == entries[:1]
  assert material.entries_named(entries, '582') == entries[:1]
  assert material.entries_named(entries, 'kr 2') == entries[:1]
  assert material.entries_named(entries, 600) == entries[1:]
  assert material.entries_named(entries, 601) == []
  # The prefix is no part of a number.
  assert material.entries_named(entries, 'MCZ 600') == []


def test_entries_named_inside_a_pair_and_exact_before_in_run():
  entries = [
    {'prefix': 'GSC', 'numbers': [[25935, 25961]]},
    {'prefix': 'GSC', 'numbers': [['A12', 'A20'], 25950]},
    {'prefix': 'GSC', 'numbers': [25940, ['25960', '25970']]},
  ]
  # An end of a pair counts exactly.
  assert material.entries_named(entries, 25935) == entries[:1]
  assert material.entries_named(entries, '25961') == entries[:1]
  # Inside a run only, by the run.
  assert material.entries_named(entries, 25936) == entries[:1]
  assert material.entries_named(entries, 'A15') == entries[1:2]
  assert material.entries_named(entries, 'a15') == []
  # Exact before in-run: 25940 is a number of the third and in the run of the first.
  assert material.entries_named(entries, 25940) == entries[2:]
  assert material.entries_named(entries, 25950) == entries[1:2]
  assert material.entries_named(entries, 25965) == entries[2:]
  assert material.entries_named(entries, 30000) == []


def test_figure_and_cast_refs_read_the_new_shape():
  node = {
    'material': [
      {'prefix': 'MCZ', 'numbers': [581, 'B2']},
      {'prefix': 'MCZ', 'numbers': [[600, 610]], 'castOf': 581},
      {'prefix': 'MCZ', 'numbers': [700], 'castOf': 'no-such'},
    ],
    'illustrations': [
      {'plate': 1, 'of': 581},
      {'plate': 2, 'of': [605, 'B2']},
      {'plate': 3, 'of': 999},
    ],
  }
  assert material.figure_refs(node) == [
    ('error', 'figure "of" value "999" matches 0 material entries, not 1'),
  ]
  assert material.cast_refs(node) == [
    ('error', 'castOf "no-such" matches 0 material entries, not 1'),
  ]


# -- the schema ------------------------------------------------------------------


def _schema_accepts(document):
  return support.schema()[io.TREE_DEF].check(document)


def _numbers_document(*entries, **extra):
  return {'taxonomies': [{'taxon': 'cyathocystis', 'material': list(entries)}], **extra}


def test_schema_accepts_the_new_shape():
  document = _numbers_document(
    {'prefix': 'MCZ', 'numbers': ['581A', 581, [1, 5], ['A1', 'A5']], 'parts': ['part']},
    {'prefix': 'GSC', 'numbers': [[25935, 25961]], 'asPrinted': 'GSC 25935–25961'},
    {'repository': 'u-cincinnati-caster', 'numbers': ['KR-2']},
    {'holder': 'A. R. Palmer', 'numbers': [[500, 501]]},
    {'prefix': 'USNM', 'repository': 'usnm-walcott', 'numbers': [1], 'castOf': 5, 'fragmentOf': 6},
    prefixes={'MCZ': 'mcz', 'GSC': 'gsc', 'USNM': 'usnm'},
    localityRegister='sprinkle-l',
    localities={
      'a': {
        'localityNumbers': [
          {'number': 'FC-1'},
          {'prefix': 'USGS', 'number': '4148 CO'},
          {'register': 'usgs-l', 'number': 'D190d CO'},
          {'number': 7},
        ]
      }
    },
  )
  document['taxonomies'][0]['illustrations'] = [
    {'plate': 1, 'of': 581},
    {'plate': 2, 'of': [1, 'a']},
  ]
  assert _schema_accepts(document)


@pytest.mark.parametrize(
  'entry',
  [
    # The old shape is gone.
    {'catalogNumbers': ['MCZ 1']},
    {'catalogNumbers': ['MCZ 1'], 'numbers': [1]},
    {'prefix': 'MCZ', 'numbers': [1], 'catalogNumbersAsPrinted': 'MCZ 1'},
    {'prefix': 'MCZ'},
    {'prefix': '', 'numbers': [1]},
    {'prefix': 'MCZ', 'numbers': []},
    {'prefix': 'MCZ', 'numbers': [[1, 2, 3]]},
    {'prefix': 'MCZ', 'numbers': [[1]]},
    {'prefix': 'MCZ', 'numbers': [1.5]},
    {'prefix': 'MCZ', 'numbers': [[1, [2]]]},
    {'prefix': 'MCZ', 'numbers': [1], 'asPrinted': 3},
  ],
)
def test_schema_rejects_a_malformed_or_mixed_entry(entry):
  assert not _schema_accepts(_numbers_document(entry))


@pytest.mark.parametrize(
  'extra',
  [
    {'prefixes': {'': 'mcz'}},
    {'prefixes': {'MCZ': 'Not A Key'}},
    {'prefixes': {'MCZ': 5}},
    {'prefixes': ['MCZ']},
    {'localityRegister': ['sprinkle-l']},
    {'repositories': ['mcz']},
    {'localities': {'a': {'localityNumbers': ['USGS 1']}}},
    {'localities': {'a': {'localityNumbers': [{'prefix': 'A'}]}}},
    {
      'localities': {'a': {'localityNumbers': [{'number': 1, 'prefix': 'A', 'register': 'usgs-l'}]}}
    },
    {'localities': {'a': {'localityNumbers': [{'number': 1, 'other': 'x'}]}}},
    {'localities': {'a': {'localityNumbers': [{'number': 1, 'prefix': ''}]}}},
    {'localities': {'a': {'localityNumbers': [{'number': 1, 'register': 'Not A Key'}]}}},
  ],
)
def test_schema_rejects_a_malformed_prefix_map_or_locality_number(extra):
  assert not _schema_accepts(_numbers_document({'label': 'A'}, **extra))


def _node_document(node, **extra):
  return {'taxonomies': [{'taxon': 'cyathocystis', **node}], **extra}


def test_schema_accepts_horizons_localities_occurrences_and_tentative_lists():
  document = _node_document(
    {
      'horizons': {
        'h': {
          'unit': ['Wheeler Shale'],
          'stage': 'Drumian',
          'biozone': 'X',
          'tentative': ['biozone'],
          'editorial': {'inferred': ['stage'], 'basis': 'The formation is Drumian.'},
        }
      },
      'localities': {
        'l': {
          'location': ['Quarry Road'],
          'localityNumbers': [{'number': 'SH-1'}],
          'tentative': True,
          'editorial': {'inferred': ['location'], 'basis': 'The map sheet names it.'},
        }
      },
      'occurrences': [
        {'horizon': 'h', 'locality': 'l', 'tentative': ['locality'], 'notes': 'x'},
        {'horizon': 'h'},
        {'locality': 'l'},
      ],
      'material': [
        {'label': 'A', 'horizon': 'h', 'locality': 'l', 'tentative': ['horizon', 'locality']},
        {'label': 'B', 'locality': 'l', 'tentative': ['locality']},
      ],
      'ranges': [
        {
          'series': 'Middle Cambrian',
          'editorial': {'inferred': ['series'], 'basis': 'Dated by zone.'},
        }
      ],
    },
    horizons={'fh': {'unit': ['A']}},
    localities={'fl': {'location': ['B']}},
  )
  assert _schema_accepts(document)
  assert _schema_accepts(_node_document({'occurrences': None}))
  assert _schema_accepts(_node_document({'material': [{'label': 'A'}]}, unused=['occurrences']))


@pytest.mark.parametrize(
  'document',
  [
    # The one `context` record, on an entry and on a node and a file, is gone.
    _node_document({'material': [{'label': 'A', 'context': 'x'}]}),
    _node_document({'material': [{'label': 'A', 'context': {'key': 'x', 'tentative': True}}]}),
    _node_document({'contexts': {'x': {'unit': ['A']}}}),
    _node_document({'contexts': None}),
    _node_document({}, contexts={'x': {'unit': ['A']}}),
    _node_document({}, unused=['contexts']),
    # An occurrence names a horizon, a locality or both.
    _node_document({'occurrences': [{}]}),
    _node_document({'occurrences': [{'notes': 'x'}]}),
    _node_document({'occurrences': [{'tentative': ['horizon']}]}),
    _node_document({'occurrences': [{'horizon': 'h', 'unit': ['A']}]}),
    # `tentative` on an entry or an occurrence names a side, nothing else.
    _node_document({'material': [{'label': 'A', 'horizon': 'h', 'tentative': ['role']}]}),
    _node_document({'material': [{'label': 'A', 'horizon': 'h', 'tentative': True}]}),
    _node_document({'occurrences': [{'horizon': 'h', 'tentative': ['unit']}]}),
    _node_document({'occurrences': [{'horizon': 'h', 'tentative': ['horizon', 'horizon']}]}),
    # The entry's plain keys are strings, not the old object.
    _node_document({'material': [{'label': 'A', 'horizon': {'key': 'h'}}]}),
    _node_document({'material': [{'label': 'A', 'locality': ['l']}]}),
    # The bare `inferred` object is gone from a range, a horizon and a locality.
    _node_document(
      {'ranges': [{'series': 'Middle Cambrian', 'inferred': {'series': 'Middle Cambrian'}}]}
    ),
    _node_document({'horizons': {'h': {'unit': ['A'], 'inferred': {'stage': 'Drumian'}}}}),
    _node_document({'localities': {'l': {'location': ['A'], 'inferred': {'location': ['B']}}}}),
    # A horizon has no place and a locality has no unit.
    _node_document({'horizons': {'h': {'location': ['A']}}}),
    _node_document({'localities': {'l': {'unit': ['A']}}}),
  ],
)
def test_schema_rejects_the_old_context_shape_and_a_malformed_occurrence(document):
  assert not _schema_accepts(document)


# -- Tree metadata, the loader and the draft checker ---------------------------


def test_tree_reads_the_prefix_map_and_locality_register_from_root_metadata(records):
  metadata = {
    'source_key': '1961_dehm',
    'position': 903,
    'type': 'taxonomy',
    'file_prefixes': {'MCZ': 'mcz'},
    'file_locality_register': 'sprinkle-l',
  }
  root = Tree({'children': [{}]}, metadata, corpus=records)
  child = root.children[0]
  assert (child.file_prefixes, child.file_locality_register) == ({'MCZ': 'mcz'}, 'sprinkle-l')
  bare = Tree({}, {'source_key': '1961_dehm', 'position': 904, 'type': 'taxonomy'}, corpus=records)
  assert (bare.file_prefixes, bare.file_locality_register) == ({}, None)


def test_load_reports_the_new_shape_checks(records, caplog):
  from phylohist.loader.load import _report_material

  data = {
    'repositories': {
      'mcz': _entry('MCZ'),
      'usgs-l': {**_entry('USGS'), 'subject': 'localities'},
    },
    'trees': {
      '_synthetic_source': {
        'prefixes': {'MCZ': 'mcz', 'GM': 'mcz', 'USGS': 'usgs-l'},
        'localities': {'f': {'localityNumbers': [{'prefix': 'QQ', 'number': 1}]}},
        'taxonomies': [
          {
            'taxon': 'a',
            'material': [
              {'prefix': 'MCZ', 'numbers': ['MCZ 1']},
              {'prefix': 'ZZ', 'numbers': [2]},
              {'numbers': [3]},
            ],
            'localities': {
              'n': {'localityNumbers': [{'number': 'FC-1'}, {'prefix': 'USGS', 'number': 1}]}
            },
            'occurrences': [{'locality': 'n'}, {'locality': 'f'}],
          },
        ],
      },
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material(support.with_documents(records, data))
  warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  assert '_synthetic_source: prefix "GM" is not a known form of "mcz"' in warnings
  assert (
    '_synthetic_source at 0: number "MCZ 1" begins with a prefix of its register "mcz"' in warnings
  )
  assert '_synthetic_source at 0: locality number "FC-1" has no register' in warnings
  assert '_synthetic_source: prefix "GM" in the file\'s `prefixes` map is used by nothing' in errors
  assert '_synthetic_source at 0: prefix "ZZ" is not in the file\'s `prefixes` map' in errors
  assert '_synthetic_source at 0: numbers with no prefix, repository or holder' in errors
  assert '_synthetic_source: prefix "QQ" is not in the file\'s `prefixes` map' in errors
  # The file's own localities are read as a file: no `localityRegister`, no prefix.
  assert not any('resolves to no locality register' in m for m in warnings)


def test_check_draft_reports_the_new_shape_checks(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'prefixes:\n  MCZ: mcz\n  XX: usnm\n'
    'localityRegister: sprinkle-l\n'
    'localities:\n  a:\n    localityNumbers:\n    - {number: FC-1}\n    - {prefix: ZZ, number: 1}\n'
    'taxonomies:\n- taxon: cyathocystis\n  occurrences:\n  - {locality: a}\n  material:\n'
    '  - {prefix: MCZ, numbers: [581A]}\n  - {numbers: [3]}\n  - {prefix: QQ, numbers: [4]}\n'
  )
  result = _run_check_draft(draft)
  assert result.returncode == 1, result.stdout + result.stderr
  for line in (
    'error: prefix "ZZ" is not in the file\'s `prefixes` map',
    'error: prefix "XX" in the file\'s `prefixes` map is used by nothing',
    'warning: prefix "XX" is not a known form of "usnm"',
    'error: 0: numbers with no prefix, repository or holder',
    'error: 0: prefix "QQ" is not in the file\'s `prefixes` map',
  ):
    assert line in result.stdout, line
  assert 'locality number "FC-1" has no register' not in result.stdout


def test_check_draft_is_quiet_on_a_clean_new_shape_draft(tmp_path):
  draft = tmp_path / '1898_bather.yaml'
  draft.write_text(
    'prefixes:\n  MCZ: mcz\n  USGS: usgs-l\n'
    'localities:\n  a:\n    localityNumbers:\n    - {prefix: USGS, number: 4148 CO}\n'
    'taxonomies:\n- taxon: cyathocystis\n  material:\n'
    '  - {prefix: MCZ, numbers: [581A, [1, 5]], locality: a}\n'
    '  - {holder: A. R. Palmer, numbers: [500]}\n'
  )
  result = _run_check_draft(draft)
  assert result.returncode == 0, result.stdout + result.stderr
  assert 'warning' not in result.stdout and 'error' not in result.stdout


# -- `sameAs` -------------------------------------------------------------------

YEARS = {'1897_whiteaves': 1897, '1914c_bather': 1914, '1962_fay': 1962, 'x_a': 1900, 'x_b': 1900}


def _same_as_document(*entries):
  return {'taxonomies': [{'taxon': 'a', 'children': [{'taxon': 'b', 'material': list(entries)}]}]}


def _same_as_errors(documents, years=YEARS):
  return [message for _, message in material.same_as_links(documents, years.get)]


def test_same_as_by_label_is_clean():
  documents = {
    '1897_whiteaves': _same_as_document({'label': 'first specimen'}, {'label': 'second'}),
    '1914c_bather': _same_as_document(
      {'label': 'A', 'sameAs': {'source': '1897_whiteaves', 'label': 'First  Specimen'}}
    ),
  }
  assert _same_as_errors(documents) == []
  # Every node of every taxonomy and phylogeny is read.
  link = {'source': '1897_whiteaves', 'label': 'nope'}
  documents['1914c_bather']['phylogenies'] = [
    {'treeType': 'cladogram', 'tree': {'taxon': 'a', 'material': [{'label': 'Q', 'sameAs': link}]}}
  ]
  assert _same_as_errors(documents) == [
    '1914c_bather at 1: `sameAs` matches 0 entries in "1897_whiteaves", not 1'
  ]


def test_same_as_by_number_exact_before_a_run_and_by_prefix():
  early = _same_as_document(
    {'prefix': 'GSC', 'numbers': [[100, 110]]},
    {'prefix': 'GSC', 'numbers': [105]},
    {'prefix': 'GSC', 'numbers': [5]},
    {'prefix': 'ROM', 'numbers': ['5']},
    {'label': '777'},
  )

  def check(link):
    entry = {'label': 'A', 'sameAs': {'source': '1897_whiteaves', **link}}
    return _same_as_errors({'1897_whiteaves': early, '1914c_bather': _same_as_document(entry)})

  # An exact number first: 105 is a number of the second entry and in the first's run.
  assert check({'number': 105}) == []
  assert check({'number': '102', 'prefix': 'GSC'}) == []
  assert check({'number': 5, 'prefix': 'ROM'}) == []
  # The prefix is what tells two entries with one number apart.
  assert check({'number': 5}) == [
    '1914c_bather at 0/children/0: `sameAs` matches 2 entries in "1897_whiteaves", not 1'
  ]
  assert len(check({'number': 999})) == 1
  # A number names no label; a label names no number.
  assert len(check({'number': 777})) == 1
  assert len(check({'label': '105'})) == 1
  assert check({'label': '777'}) == []


def test_same_as_label_matching_nothing_or_several_is_an_error():
  early = _same_as_document({'label': 'A'}, {'label': 'a'})
  documents = {
    '1897_whiteaves': early,
    '1914c_bather': _same_as_document(
      {'label': 'Z', 'sameAs': {'source': '1897_whiteaves', 'label': 'A'}},
      {'label': 'Y', 'sameAs': {'source': '1897_whiteaves', 'label': 'B'}},
    ),
  }
  assert _same_as_errors(documents) == [
    '1914c_bather at 0/children/0: `sameAs` matches 2 entries in "1897_whiteaves", not 1',
    '1914c_bather at 0/children/0: `sameAs` matches 0 entries in "1897_whiteaves", not 1',
  ]


def test_same_as_source_with_no_tree_or_the_entrys_own_source_is_an_error():
  def entry(source):
    return _same_as_document({'label': 'A', 'sameAs': {'source': source, 'label': 'A'}})

  documents = {'1914c_bather': entry('1897_whiteaves'), '1962_fay': entry('1962_fay')}
  assert _same_as_errors(documents) == [
    '1914c_bather at 0/children/0: `sameAs` names "1897_whiteaves", which has no tree',
    '1962_fay at 0/children/0: `sameAs` names its own source',
  ]


def test_same_as_pointing_at_a_later_source_is_an_error_but_equal_years_are_allowed():
  def entry(source):
    return _same_as_document({'label': 'A', 'sameAs': {'source': source, 'label': 'A'}})

  target = _same_as_document({'label': 'A'})
  later = {'1897_whiteaves': entry('1914c_bather'), '1914c_bather': target}
  assert _same_as_errors(later) == [
    '1897_whiteaves at 0/children/0: `sameAs` points at a later source'
  ]
  assert _same_as_errors({'x_a': entry('x_b'), 'x_b': target}) == []
  # A year that is not known is not compared.
  assert _same_as_errors(later, {}) == []


def test_the_loader_reports_same_as_links_across_the_corpus(records, caplog):
  from phylohist.loader.load import _report_material

  data = {
    'repositories': {},
    'trees': {
      '1914c_bather': _same_as_document(
        {'label': 'A', 'sameAs': {'source': '1897_whiteaves', 'label': 'nope'}}
      ),
      '1897_whiteaves': _same_as_document({'label': 'first'}),
    },
  }
  with caplog.at_level(logging.WARNING, logger='phylohist'):
    _report_material(support.with_documents(records, data))
  errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
  # The corpus's own years come from the source records, 1897 before 1914.
  assert errors == [
    '1914c_bather at 0/children/0: `sameAs` matches 0 entries in "1897_whiteaves", not 1'
  ]


def test_schema_accepts_and_rejects_same_as():
  def entry(link):
    return _numbers_document({'label': 'A', 'sameAs': link})

  assert _schema_accepts(entry({'source': '1897_whiteaves', 'label': 'first specimen'}))
  assert _schema_accepts(entry({'source': '1897_whiteaves', 'number': 752}))
  assert _schema_accepts(entry({'source': '1897_whiteaves', 'number': '752A', 'prefix': 'GSC'}))
  for bad in (
    {'label': 'first specimen'},
    {'source': '1897_whiteaves'},
    {'source': '1897_whiteaves', 'label': 'A', 'number': 1},
    {'source': '1897_whiteaves', 'label': 'A', 'prefix': 'GSC'},
    {'source': 'Not A Key', 'label': 'A'},
    {'source': '1897_whiteaves', 'label': 'A', 'other': 1},
    {'source': '1897_whiteaves', 'number': 1.5},
  ):
    assert not _schema_accepts(entry(bad)), bad


def test_schema_accepts_and_rejects_entry_refs_and_entry_locality_numbers():
  def entry(**fields):
    return _numbers_document({'prefix': 'GK', 'numbers': [112], **fields}, prefixes={'GK': 'mcz'})

  for good in (
    {'castOf': {'number': 112, 'prefix': 'GTB'}},
    {'castOf': {'number': '112'}},
    {'fragmentOf': {'label': 'the slab'}},
    {'fragmentOf': 'B'},
    {
      'localityNumbers': [
        {'prefix': 'GTBM', 'number': '9-2-12'},
        {'register': 'usgs-l', 'number': 1},
      ]
    },
  ):
    assert _schema_accepts(entry(**good)), good
  for bad in (
    {'castOf': {'prefix': 'GTB'}},
    {'castOf': {'label': 'A', 'number': 1}},
    {'castOf': {'number': 1, 'other': 1}},
    {'castOf': {'number': 1.5}},
    {'fragmentOf': {'label': 'A', 'prefix': 'GK'}},
    {'fragmentOf': {}},
    {'localityNumbers': []},
    {'localityNumbers': [{'prefix': 'GTBM'}]},
    {'localityNumbers': [{'number': 1, 'prefix': 'A', 'register': 'usgs-l'}]},
  ):
    assert not _schema_accepts(entry(**bad)), bad

  def figure(of):
    document = entry()
    document['taxonomies'][0]['illustrations'] = [{'plate': 1, 'of': of}]
    return document

  assert _schema_accepts(figure({'number': 112, 'prefix': 'GK'}))
  assert _schema_accepts(figure([112, {'label': 'A'}, {'number': '112', 'prefix': 'GTB'}]))
  assert not _schema_accepts(figure({'prefix': 'GK'}))
  assert not _schema_accepts(figure([{'number': 1, 'label': 'A'}]))
  assert not _schema_accepts(figure([]))


def test_check_draft_checks_same_as_against_the_corpus(tmp_path):
  def draft(link):
    path = tmp_path / '1914c_bather.yaml'
    path.write_text(
      f'taxonomies:\n- taxon: cyathocystis\n  material:\n  - {{label: A, sameAs: {link}}}\n'
    )
    return _run_check_draft(path)

  first = (
    'first specimen collected by John Stewart, 1886, Museum of the Geological Survey of Canada'
  )
  clean = draft(f'{{source: 1897_whiteaves, label: "{first}"}}')
  assert clean.returncode == 0, clean.stdout + clean.stderr
  assert 'error' not in clean.stdout
  for link, line in (
    (
      '{source: 1897_whiteaves, label: nope}',
      '`sameAs` matches 0 entries in "1897_whiteaves", not 1',
    ),
    ('{source: 1962_fay, label: A}', '`sameAs` points at a later source'),
    ('{source: 1914c_bather, label: A}', '`sameAs` names its own source'),
    ('{source: 1899_nobody, label: A}', '`sameAs` names "1899_nobody", which has no tree'),
  ):
    result = draft(link)
    assert result.returncode == 1, result.stdout + result.stderr
    assert f'error: 1914c_bather at 0: {line}' in result.stdout
