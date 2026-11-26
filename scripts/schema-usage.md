# Schema usage census

**Generated** by `scripts/schema_audit.py` -- do not edit by hand.
Narrative analysis of these numbers is in `notes/audits/schema-audit.md`.

Counts are *distinct instance locations* that reached a given schema
location, measured from the `json-schema-engine` verbose output tree.

## 1. Unreached schema locations

Schema locations no data anywhere reaches. A nested location is listed
even when its parent is also unreached, so read parents first.

| `$defs` | unreached locations |
|---|---|
| `actAndModifierFields` | `phylogeny#/$defs/actAndModifierFields/properties/recombined/oneOf/1`<br>`phylogeny#/$defs/actAndModifierFields/properties/restrictedBy`<br>`phylogeny#/$defs/actAndModifierFields/properties/restrictedBy/items` |
| `article` | `phylogeny#/$defs/article/oneOf/2`<br>`phylogeny#/$defs/article/properties/reading` |
| `authority` | `phylogeny#/$defs/authority/oneOf/3/not`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/0`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/1`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/2`<br>`phylogeny#/$defs/authority/oneOf/3/not/anyOf/3`<br>`phylogeny#/$defs/authority/properties/auctt/oneOf/1` |
| `catalogNumber` | `phylogeny#/$defs/catalogNumber`<br>`phylogeny#/$defs/catalogNumber/oneOf/0`<br>`phylogeny#/$defs/catalogNumber/oneOf/1`<br>`phylogeny#/$defs/catalogNumber/oneOf/1/items` |
| `citedAct` | `phylogeny#/$defs/citedAct`<br>`phylogeny#/$defs/citedAct/properties/by` |
| `citedWork` | `phylogeny#/$defs/citedWork/anyOf/1` |
| `cladisticFields` | `phylogeny#/$defs/cladisticFields/properties/data`<br>`phylogeny#/$defs/cladisticFields/properties/data/additionalProperties` |
| `editorialObject` | `phylogeny#/$defs/editorialObject/properties/corrections/not`<br>`phylogeny#/$defs/editorialObject/properties/corrections/not/anyOf/0`<br>`phylogeny#/$defs/editorialObject/properties/corrections/not/anyOf/1`<br>`phylogeny#/$defs/editorialObject/properties/corrections/not/anyOf/2`<br>`phylogeny#/$defs/editorialObject/properties/corrections/properties/authority/properties/in`<br>`phylogeny#/$defs/editorialObject/properties/corrections/properties/authority/properties/in/items` |
| `entryRef` | `phylogeny#/$defs/entryRef`<br>`phylogeny#/$defs/entryRef/oneOf/0`<br>`phylogeny#/$defs/entryRef/oneOf/1`<br>`phylogeny#/$defs/entryRef/properties/label`<br>`phylogeny#/$defs/entryRef/properties/number`<br>`phylogeny#/$defs/entryRef/properties/prefix` |
| `entryRefOrNumber` | `phylogeny#/$defs/entryRefOrNumber/oneOf/1` |
| `eon` | `phylogeny#/$defs/eon` |
| `era` | `phylogeny#/$defs/era` |
| `figureLocatorFields` | `phylogeny#/$defs/figureLocatorFields/properties/non` |
| `horizon` | `phylogeny#/$defs/horizon/properties/biozones`<br>`phylogeny#/$defs/horizon/properties/biozones/items`<br>`phylogeny#/$defs/horizon/properties/sources`<br>`phylogeny#/$defs/horizon/properties/sources/items`<br>`phylogeny#/$defs/horizon/properties/tentative/oneOf/0` |
| `labels` | `phylogeny#/$defs/labels/oneOf/1`<br>`phylogeny#/$defs/labels/oneOf/1/items` |
| `localTimeFields` | `phylogeny#/$defs/localTimeFields/properties/localStageBoundary` |
| `locality` | `phylogeny#/$defs/locality/properties/collectedDate`<br>`phylogeny#/$defs/locality/properties/sources`<br>`phylogeny#/$defs/locality/properties/sources/items`<br>`phylogeny#/$defs/locality/properties/tentative`<br>`phylogeny#/$defs/locality/properties/tentative/oneOf/0`<br>`phylogeny#/$defs/locality/properties/tentative/oneOf/1`<br>`phylogeny#/$defs/locality/properties/tentative/oneOf/1/items` |
| `localityNumber` | `phylogeny#/$defs/localityNumber/not`<br>`phylogeny#/$defs/localityNumber/properties/register` |
| `materialEntry` | `phylogeny#/$defs/materialEntry/not`<br>`phylogeny#/$defs/materialEntry/properties/formerIds`<br>`phylogeny#/$defs/materialEntry/properties/formerIds/items`<br>`phylogeny#/$defs/materialEntry/properties/fragmentOf`<br>`phylogeny#/$defs/materialEntry/properties/horizon/oneOf/1`<br>`phylogeny#/$defs/materialEntry/properties/roleUncertain`<br>`phylogeny#/$defs/materialEntry/properties/sameAs`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/oneOf/0`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/oneOf/1`<br>`phylogeny#/$defs/materialEntry/properties/sameAs/oneOf/1/items`<br>`phylogeny#/$defs/materialEntry/properties/tentative` |
| `occurrence` | `phylogeny#/$defs/occurrence/properties/notes`<br>`phylogeny#/$defs/occurrence/properties/tentative` |
| `occurrenceTentative` | `phylogeny#/$defs/occurrenceTentative`<br>`phylogeny#/$defs/occurrenceTentative/items` |
| `person` | `phylogeny#/$defs/person/properties/suffix` |
| `publication` | `phylogeny#/$defs/publication/properties/type` |
| `range` | `phylogeny#/$defs/range/properties/editorial` |
| `relationalFields` | `phylogeny#/$defs/relationalFields/properties/type/oneOf/1` |
| `sameAsLink` | `phylogeny#/$defs/sameAsLink`<br>`phylogeny#/$defs/sameAsLink/oneOf/0`<br>`phylogeny#/$defs/sameAsLink/oneOf/1`<br>`phylogeny#/$defs/sameAsLink/properties/labels`<br>`phylogeny#/$defs/sameAsLink/properties/numbers`<br>`phylogeny#/$defs/sameAsLink/properties/numbers/items`<br>`phylogeny#/$defs/sameAsLink/properties/of`<br>`phylogeny#/$defs/sameAsLink/properties/prefix`<br>`phylogeny#/$defs/sameAsLink/properties/source` |
| `sectionRecord` | `phylogeny#/$defs/sectionRecord/properties/authority/not` |
| `stageRange` | `phylogeny#/$defs/stageRange`<br>`phylogeny#/$defs/stageRange/items` |
| `taxonRecord` | `phylogeny#/$defs/taxonRecord/else/oneOf/3`<br>`phylogeny#/$defs/taxonRecord/else/oneOf/4`<br>`phylogeny#/$defs/taxonRecord/properties/altGenderOf`<br>`phylogeny#/$defs/taxonRecord/properties/authority/not`<br>`phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items/items`<br>`phylogeny#/$defs/taxonRecord/properties/latinSpellingOf` |
| `timeFields` | `phylogeny#/$defs/timeFields/properties/eon`<br>`phylogeny#/$defs/timeFields/properties/era`<br>`phylogeny#/$defs/timeFields/properties/seriesBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageBoundary`<br>`phylogeny#/$defs/timeFields/properties/stageRange` |
| `typeNode` | `phylogeny#/$defs/typeNode/properties/fixedBy` |

## 2. Property frequency by `$defs`

`data %` is the share of that container's instances carrying the
property.

### `actAndModifierFields` -- 5975 instances in `data/`

| property | data | data % |
|---|---|---|
| `new` | 1653 | 27.7% |
| `isType` | 364 | 6.1% |
| `emended` | 57 | 1.0% |
| `pars` | 21 | 0.4% |
| `translated` | 19 | 0.3% |
| `emendedBy` | 9 | 0.2% |
| `nudum` | 7 | 0.1% |
| `recombined` | 3 | 0.1% |
| `term` | 3 | 0.1% |
| `group` | 2 | 0.0% |
| `restricted` | 1 | 0.0% |
| `restrictedBy` | 0 | 0.0% |

### `article` -- 406 instances in `data/`

| property | data | data % |
|---|---|---|
| `authors` | 406 | 100.0% |
| `pubDate` | 405 | 99.8% |
| `volume` | 318 | 78.3% |
| `title` | 290 | 71.4% |
| `identifiers` | 287 | 70.7% |
| `pages` | 260 | 64.0% |
| `journal` | 248 | 61.1% |
| `number` | 203 | 50.0% |
| `identifiers.url` | 200 | 69.7% |
| `book` | 157 | 38.7% |
| `processDates` | 101 | 24.9% |
| `notes` | 71 | 17.5% |
| `identifiers.doi` | 66 | 23.0% |
| `processDates.accepted` | 63 | 62.4% |
| `processDates.received` | 53 | 52.5% |
| `audit` | 48 | 11.8% |
| `audit.notes` | 48 | 100.0% |
| `audit.state` | 48 | 100.0% |
| `audit.coverage` | 30 | 62.5% |
| `processDates.online` | 28 | 27.7% |
| `plates` | 25 | 6.2% |
| `identifiers.jstor` | 24 | 8.4% |
| `processDates.revised` | 18 | 17.8% |
| `series` | 14 | 3.4% |
| `processDates.read` | 11 | 10.9% |
| `articleNumber` | 8 | 2.0% |
| `seen` | 5 | 1.2% |
| `processDates.transmitted` | 4 | 4.0% |
| `processDates.conferenceEnd` | 3 | 3.0% |
| `processDates.conferenceStart` | 3 | 3.0% |
| `processDates.issued` | 3 | 3.0% |
| `processDates.submitted` | 3 | 3.0% |
| `chapter` | 2 | 0.5% |
| `translationOf` | 2 | 0.5% |
| `translations` | 2 | 0.5% |
| `/oneOf/3.inPrep` | 1 | 100.0% |
| `editors` | 1 | 0.2% |
| `inPrep` | 1 | 0.2% |
| `processDates.printed` | 1 | 1.0% |
| `processDates.published` | 1 | 1.0% |
| `processDates.unknown` | 1 | 1.0% |
| `quotes` | 1 | 0.2% |
| `reading` | 0 | 0.0% |

### `authority` -- 2984 instances in `data/`

| property | data | data % |
|---|---|---|
| `source` | 2104 | 70.5% |
| `auth` | 856 | 28.7% |
| `year` | 853 | 28.6% |
| `pages` | 426 | 14.3% |
| `illustrations` | 94 | 3.2% |
| `in` | 27 | 0.9% |
| `attributedTo` | 25 | 0.8% |
| `ex` | 15 | 0.5% |
| `notes` | 4 | 0.1% |
| `auctt` | 2 | 0.1% |

### `citationFields` -- 9668 instances in `data/`

| property | data | data % |
|---|---|---|
| `citedAs` | 1094 | 11.3% |

### `cladisticFields` -- 793 instances in `data/`

| property | data | data % |
|---|---|---|
| `outgroup` | 19 | 2.4% |
| `matrix` | 8 | 1.0% |
| `bootstrap` | 6 | 0.8% |
| `data` | 0 | 0.0% |

### `editorialObject` -- 91 instances in `data/`

| property | data | data % |
|---|---|---|
| `basis` | 91 | 100.0% |
| `inferred` | 76 | 83.5% |
| `corrections` | 15 | 16.5% |
| `corrections.authority` | 11 | 73.3% |
| `corrections.authority.source` | 9 | 81.8% |
| `corrections.authority.auth` | 8 | 72.7% |
| `corrections.authority.year` | 8 | 72.7% |
| `corrections.authority.in` | 0 | 0.0% |

### `figureLocatorFields` -- 613 instances in `data/`

| property | data | data % |
|---|---|---|
| `figures` | 538 | 87.8% |
| `plate` | 413 | 67.4% |
| `page` | 184 | 30.0% |
| `textFigures` | 69 | 11.3% |
| `notes` | 28 | 4.6% |
| `non` | 0 | 0.0% |

### `horizon` -- 92 instances in `data/`

| property | data | data % |
|---|---|---|
| `unit` | 89 | 96.7% |
| `biozone` | 35 | 38.0% |
| `notes` | 11 | 12.0% |
| `biozoneRange` | 6 | 6.5% |
| `biota` | 5 | 5.4% |
| `tentative` | 2 | 2.2% |
| `editorial` | 1 | 1.1% |
| `fauna` | 1 | 1.1% |
| `biozones` | 0 | 0.0% |
| `sources` | 0 | 0.0% |

### `identificationFields` -- 6768 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxon` | 6115 | 90.4% |
| `openTaxon` | 285 | 4.2% |
| `cf` | 16 | 0.2% |
| `aff` | 14 | 0.2% |
| `designation` | 2 | 0.0% |
| `mineralTaxon` | 2 | 0.0% |

### `illustration` -- 613 instances in `data/`

| property | data | data % |
|---|---|---|
| `of` | 302 | 49.3% |
| `depicts` | 226 | 36.9% |
| `uncertain` | 2 | 0.3% |

### `localTimeFields` -- 169 instances in `data/`

| property | data | data % |
|---|---|---|
| `localSeries` | 53 | 31.4% |
| `localSeriesModifier` | 19 | 11.2% |
| `localSeriesRange` | 9 | 5.3% |
| `localStage` | 7 | 4.1% |
| `localPeriod` | 3 | 1.8% |
| `localStageRange` | 2 | 1.2% |
| `localSeriesBoundary` | 1 | 0.6% |
| `localStageModifier` | 1 | 0.6% |
| `localStageBoundary` | 0 | 0.0% |

### `locality` -- 120 instances in `data/`

| property | data | data % |
|---|---|---|
| `location` | 120 | 100.0% |
| `localityNumbers` | 46 | 38.3% |
| `mapSheet` | 30 | 25.0% |
| `landSurvey` | 11 | 9.2% |
| `notes` | 7 | 5.8% |
| `collectedBy` | 2 | 1.7% |
| `coordinatesAsPrinted` | 1 | 0.8% |
| `editorial` | 1 | 0.8% |
| `paleocontinent` | 1 | 0.8% |
| `collectedDate` | 0 | 0.0% |
| `sources` | 0 | 0.0% |
| `tentative` | 0 | 0.0% |

### `localityNumber` -- 59 instances in `data/`

| property | data | data % |
|---|---|---|
| `number` | 59 | 100.0% |
| `prefix` | 28 | 47.5% |
| `register` | 0 | 0.0% |

### `locationFields` -- 6768 instances in `data/`

| property | data | data % |
|---|---|---|
| `illustrations` | 210 | 3.1% |

### `materialEntry` -- 312 instances in `data/`

| property | data | data % |
|---|---|---|
| `numbers` | 291 | 93.3% |
| `prefix` | 288 | 92.3% |
| `role` | 226 | 72.4% |
| `locality` | 163 | 52.2% |
| `horizon` | 160 | 51.3% |
| `asPrinted` | 85 | 27.2% |
| `notes` | 69 | 22.1% |
| `labels` | 18 | 5.8% |
| `preparation` | 17 | 5.4% |
| `repository` | 12 | 3.8% |
| `count` | 11 | 3.5% |
| `collectedBy` | 10 | 3.2% |
| `collectedDate` | 7 | 2.2% |
| `localityNumbers` | 7 | 2.2% |
| `parts` | 6 | 1.9% |
| `holder` | 5 | 1.6% |
| `castOf` | 3 | 1.0% |
| `uncertain` | 2 | 0.6% |
| `editorial` | 1 | 0.3% |
| `examined` | 1 | 0.3% |
| `listComplete` | 1 | 0.3% |
| `roleAct` | 1 | 0.3% |
| `status` | 1 | 0.3% |
| `formerIds` | 0 | 0.0% |
| `fragmentOf` | 0 | 0.0% |
| `roleUncertain` | 0 | 0.0% |
| `sameAs` | 0 | 0.0% |
| `tentative` | 0 | 0.0% |

### `materialsFields` -- 5975 instances in `data/`

| property | data | data % |
|---|---|---|
| `material` | 133 | 2.2% |
| `ranges` | 113 | 1.9% |
| `occurrences` | 69 | 1.2% |
| `localities` | 58 | 1.0% |
| `horizons` | 56 | 0.9% |

### `metaFields` -- 6768 instances in `data/`

| property | data | data % |
|---|---|---|
| `notes` | 526 | 7.8% |
| `editorial` | 87 | 1.3% |

### `modularDate` -- 405 instances in `data/`

| property | data | data % |
|---|---|---|
| `year` | 405 | 100.0% |
| `month` | 94 | 23.2% |
| `day` | 37 | 9.1% |
| `/then/oneOf/2.day` | 22 | 100.0% |
| `/then/oneOf/2.month` | 22 | 100.0% |
| `/then/oneOf/1.day` | 13 | 100.0% |
| `/then/oneOf/1.month` | 13 | 100.0% |
| `months` | 6 | 1.5% |
| `/then/oneOf/0.day` | 2 | 100.0% |
| `/then/oneOf/0.month` | 2 | 100.0% |
| `season` | 1 | 0.2% |

### `occurrence` -- 30 instances in `data/`

| property | data | data % |
|---|---|---|
| `locality` | 30 | 100.0% |
| `horizon` | 27 | 90.0% |
| `notes` | 0 | 0.0% |
| `tentative` | 0 | 0.0% |

### `person` -- 335 instances in `data/`

| property | data | data % |
|---|---|---|
| `given` | 335 | 100.0% |
| `surname` | 335 | 100.0% |
| `birth` | 113 | 33.7% |
| `death` | 111 | 33.1% |
| `suffix` | 0 | 0.0% |

### `phylogeny` -- 36 instances in `data/`

| property | data | data % |
|---|---|---|
| `tree` | 36 | 100.0% |
| `treeType` | 36 | 100.0% |
| `methodology` | 18 | 50.0% |
| `notes` | 7 | 19.4% |
| `characteristics` | 1 | 2.8% |

### `publication` -- 180 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 180 | 100.0% |
| `editors` | 10 | 5.6% |
| `place` | 8 | 4.4% |
| `publisher` | 8 | 4.4% |
| `notes` | 5 | 2.8% |
| `type` | 0 | 0.0% |

### `range` -- 77 instances in `data/`

| property | data | data % |
|---|---|---|
| `regions` | 37 | 48.1% |
| `asPrinted` | 35 | 45.5% |
| `notes` | 10 | 13.0% |
| `tentative` | 7 | 9.1% |
| `regions/items/oneOf/1.tentative` | 2 | 100.0% |
| `regions/items/oneOf/1.value` | 2 | 100.0% |
| `editorial` | 0 | 0.0% |

### `ranks` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `ranks/items.name` | 32 | 100.0% |
| `ranks/items.informal` | 9 | 28.1% |
| `exceptions/items.name` | 7 | 100.0% |
| `exceptions/items.note` | 7 | 100.0% |
| `exceptions/items.rank` | 7 | 100.0% |
| `suffixes/items.ranks` | 6 | 100.0% |
| `suffixes/items.suffix` | 6 | 100.0% |
| `ranks/items.group` | 5 | 15.6% |
| `ranks/items.endings/items.suffix` | 4 | 100.0% |
| `ranks/items.endings` | 3 | 9.4% |
| `checkedFrom` | 1 | 100.0% |
| `exceptions` | 1 | 100.0% |
| `ranks` | 1 | 100.0% |
| `ranks/items.endings/items.before` | 1 | 25.0% |
| `suffixes` | 1 | 100.0% |

### `relationalFields` -- 5975 instances in `data/`

| property | data | data % |
|---|---|---|
| `synonyms` | 377 | 6.3% |
| `moved` | 81 | 1.4% |
| `type` | 9 | 0.2% |
| `corrected` | 5 | 0.1% |
| `non` | 5 | 0.1% |
| `or` | 5 | 0.1% |
| `lapsus` | 4 | 0.1% |
| `removed` | 2 | 0.0% |
| `substituted` | 2 | 0.0% |
| `lapsusFor` | 1 | 0.0% |

### `repositories` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.name` | 63 | 100.0% |
| `/additionalProperties.type` | 63 | 100.0% |
| `/additionalProperties.prefixes` | 55 | 87.3% |
| `/additionalProperties.place` | 38 | 60.3% |
| `/additionalProperties.within` | 17 | 27.0% |
| `/additionalProperties.subject` | 15 | 23.8% |
| `/additionalProperties.notes` | 11 | 17.5% |
| `/additionalProperties.otherNames` | 3 | 4.8% |

### `roles` -- 1 instances in `data/`

| property | data | data % |
|---|---|---|
| `/additionalProperties.meaning` | 12 | 100.0% |
| `/additionalProperties.regulated` | 12 | 100.0% |
| `/additionalProperties.article` | 6 | 50.0% |
| `/additionalProperties.notes` | 6 | 50.0% |
| `/additionalProperties.equivalent` | 2 | 16.7% |

### `sectionFields` -- 5975 instances in `data/`

| property | data | data % |
|---|---|---|
| `sectionEnd` | 25 | 0.4% |
| `sectionStart` | 25 | 0.4% |
| `sectionStart.section` | 25 | 100.0% |
| `sectionStart.new` | 14 | 56.0% |
| `sectionStart.pages` | 14 | 56.0% |
| `sectionStart.citedAs` | 12 | 48.0% |
| `sectionStart.notes` | 5 | 20.0% |
| `sectionStart.designation` | 3 | 12.0% |
| `sectionStart.editorial` | 1 | 4.0% |

### `sectionRecord` -- 14 instances in `data/`

| property | data | data % |
|---|---|---|
| `authority` | 14 | 100.0% |
| `citedAs` | 14 | 100.0% |
| `name` | 14 | 100.0% |
| `notes` | 5 | 35.7% |
| `/if.name` | 3 | 100.0% |
| `designation` | 3 | 21.4% |
| `needsQualification` | 1 | 7.1% |

### `sourceAlias` -- 4 instances in `data/`

| property | data | data % |
|---|---|---|
| `aliasOf` | 4 | 100.0% |

### `taxonRecord` -- 2900 instances in `data/`

| property | data | data % |
|---|---|---|
| `name` | 2870 | 99.0% |
| `authority` | 2677 | 92.3% |
| `/if.authority` | 2676 | 100.0% |
| `rank` | 1046 | 36.1% |
| `notes` | 252 | 8.7% |
| `altSpellingOf` | 149 | 5.1% |
| `lang` | 76 | 2.6% |
| `originalParent` | 71 | 2.4% |
| `altRankOf` | 51 | 1.8% |
| `vulgarSpellingOf` | 45 | 1.6% |
| `homonym` | 18 | 0.6% |
| `needsQualification` | 17 | 0.6% |
| `bracket` | 9 | 0.3% |
| `designation` | 4 | 0.1% |
| `holotype` | 1 | 0.0% |
| `mineral` | 1 | 0.0% |
| `status` | 1 | 0.0% |
| `altGenderOf` | 0 | 0.0% |
| `latinSpellingOf` | 0 | 0.0% |

### `timeFields` -- 169 instances in `data/`

| property | data | data % |
|---|---|---|
| `period` | 91 | 53.8% |
| `series` | 49 | 29.0% |
| `seriesRange` | 24 | 14.2% |
| `stage` | 20 | 11.8% |
| `seriesModifier` | 7 | 4.1% |
| `stageModifier` | 4 | 2.4% |
| `eon` | 0 | 0.0% |
| `era` | 0 | 0.0% |
| `seriesBoundary` | 0 | 0.0% |
| `stageBoundary` | 0 | 0.0% |
| `stageRange` | 0 | 0.0% |

### `translatedNode` -- 16 instances in `data/`

| property | data | data % |
|---|---|---|
| `by` | 1 | 6.2% |

### `tree` -- 6768 instances in `data/`

| property | data | data % |
|---|---|---|
| `children` | 2260 | 33.4% |
| `pages` | 1247 | 18.4% |
| `rank` | 657 | 9.7% |
| `authority` | 347 | 5.1% |
| `parents` | 335 | 4.9% |
| `bracketEnd` | 28 | 0.4% |
| `bracketStart` | 28 | 0.4% |
| `mergeInto` | 14 | 0.2% |
| `altPlacements` | 6 | 0.1% |

### `treeDocument` -- 232 instances in `data/`

| property | data | data % |
|---|---|---|
| `taxonomies` | 228 | 98.3% |
| `prefixes` | 35 | 15.1% |
| `phylogenies` | 25 | 10.8% |
| `notes` | 20 | 8.6% |
| `horizons` | 5 | 2.2% |
| `localities` | 5 | 2.2% |
| `unused` | 5 | 2.2% |
| `assumptions` | 1 | 0.4% |
| `localityRegister` | 1 | 0.4% |

### `typeNode` -- 9 instances in `data/`

| property | data | data % |
|---|---|---|
| `fixation` | 2 | 22.2% |
| `fixedBy` | 0 | 0.0% |

### `uncertaintyFields` -- 6768 instances in `data/`

| property | data | data % |
|---|---|---|
| `provisional` | 142 | 2.1% |
| `tentative` | 17 | 0.3% |
| `questionable` | 14 | 0.2% |
| `quotedParent` | 14 | 0.2% |
| `sensu` | 8 | 0.1% |
| `mutable` | 3 | 0.0% |
| `quoted` | 2 | 0.0% |
| `monophyly` | 1 | 0.0% |

## 3. Enum member usage

### `phylogeny#/$defs/actAndModifierFields/properties/group`

2 of 3 members used, 2 occurrences.

| value | count |
|---|---|
| `'stem'` | 1 |
| `'total'` | 1 |

**Never used (1):** `'crown'`

### `phylogeny#/$defs/actAndModifierFields/properties/term`

1 of 3 members used, 3 occurrences.

| value | count |
|---|---|
| `'plesion'` | 3 |

**Never used (2):** `'scion'`, `'clade'`

### `phylogeny#/$defs/article/properties/audit/properties/coverage/additionalProperties`

4 of 4 members used, 239 occurrences.

| value | count |
|---|---|
| `'none'` | 75 |
| `'all'` | 70 |
| `'partly'` | 49 |
| `'na'` | 45 |

### `phylogeny#/$defs/article/properties/audit/properties/coverage/propertyNames`

8 of 8 members used, 239 occurrences.

| value | count |
|---|---|
| `'phylogeny'` | 30 |
| `'illustrations'` | 30 |
| `'material'` | 30 |
| `'synonymy'` | 30 |
| `'types'` | 30 |
| `'newTaxa'` | 30 |
| `'skeleton'` | 30 |
| `'occurrences'` | 29 |

### `phylogeny#/$defs/article/properties/audit/properties/state`

1 of 5 members used, 48 occurrences.

| value | count |
|---|---|
| `'partial'` | 48 |

**Never used (4):** `'complete'`, `'unaudited'`, `'unauditable'`, `'unobtainable'`

### `phylogeny#/$defs/eon`

0 of 4 members used, 0 occurrences.

**Never used (4):** `'Hadean'`, `'Archean'`, `'Proterozoic'`, `'Phanerozoic'`

### `phylogeny#/$defs/era`

0 of 10 members used, 0 occurrences.

**Never used (10):** `'Eoarchean'`, `'Paleoarchean'`, `'Mesoarchean'`, `'Neoarchean'`, `'Paleoproterozoic'`, `'Mesoproterozoic'`, `'Neoproterozoic'`, `'Paleozoic'`, `'Mesozoic'`, `'Cenozoic'`

### `phylogeny#/$defs/illustration/properties/depicts`

4 of 4 members used, 226 occurrences.

| value | count |
|---|---|
| `'cast'` | 132 |
| `'drawing'` | 50 |
| `'specimen'` | 39 |
| `'reconstruction'` | 5 |

### `phylogeny#/$defs/materialEntry/properties/roleAct`

1 of 2 members used, 1 occurrences.

| value | count |
|---|---|
| `'designated'` | 1 |

**Never used (1):** `'reported'`

### `phylogeny#/$defs/materialEntry/properties/status`

1 of 2 members used, 1 occurrences.

| value | count |
|---|---|
| `'lost'` | 1 |

**Never used (1):** `'untraced'`

### `phylogeny#/$defs/modularDate/properties/season`

1 of 5 members used, 1 occurrences.

| value | count |
|---|---|
| `'summer'` | 1 |

**Never used (4):** `'spring'`, `'fall'`, `'autumn'`, `'winter'`

### `phylogeny#/$defs/occurrenceTentative/items`

0 of 2 members used, 0 occurrences.

**Never used (2):** `'horizon'`, `'locality'`

### `phylogeny#/$defs/period`

3 of 22 members used, 91 occurrences.

| value | count |
|---|---|
| `'Cambrian'` | 50 |
| `'Ordovician'` | 38 |
| `'Silurian'` | 3 |

**Never used (19):** `'Siderian'`, `'Rhyacian'`, `'Orosirian'`, `'Statherian'`, `'Calymmian'`, `'Ectasian'`, `'Stenian'`, `'Tonian'`, `'Cryogenian'`, `'Ediacaran'`, `'Devonian'`, `'Carboniferous'`, `'Permian'`, `'Triassic'`, `'Jurassic'`, `'Cretaceous'`, `'Paleogene'`, `'Neogene'`, `'Quaternary'`

### `phylogeny#/$defs/phylogeny/properties/treeType`

3 of 4 members used, 36 occurrences.

| value | count |
|---|---|
| `'cladogram'` | 27 |
| `'diagram'` | 8 |
| `'other'` | 1 |

**Never used (1):** `'taxonomy'`

### `phylogeny#/$defs/publication/properties/type`

0 of 2 members used, 0 occurrences.

**Never used (2):** `'journal'`, `'book'`

### `phylogeny#/$defs/rank`

25 of 32 members used, 1642 occurrences.

| value | count |
|---|---|
| `'Order'` | 312 |
| `'Class'` | 292 |
| `'species'` | 280 |
| `'Family'` | 228 |
| `'genus'` | 152 |
| `'variety'` | 65 |
| `'Phylum'` | 63 |
| `'Subphylum'` | 52 |
| `'Superfamily'` | 33 |
| `'Subfamily'` | 26 |
| `'Subclass'` | 24 |
| `'Suborder'` | 23 |
| `'subgenus'` | 17 |
| `'Grade'` | 16 |
| `'section'` | 14 |
| `'Group'` | 12 |
| `'Division'` | 9 |
| `'Kingdom'` | 6 |
| `'Subtypus'` | 5 |
| `'Superorder'` | 4 |
| `'Subkingdom'` | 3 |
| `'Typus'` | 2 |
| `'Branch'` | 2 |
| `'Parvclass'` | 1 |
| `'Superphylum'` | 1 |

**Never used (7):** `'Domain'`, `'Infraphylum'`, `'Superclass'`, `'Infraclass'`, `'subspecies'`, `'Embranchement'`, `'Unranked'`

### `phylogeny#/$defs/ranks/properties/ranks/items/properties/group`

2 of 2 members used, 5 occurrences.

| value | count |
|---|---|
| `'species'` | 3 |
| `'genus'` | 2 |

### `phylogeny#/$defs/repositories/additionalProperties/properties/subject`

2 of 4 members used, 15 occurrences.

| value | count |
|---|---|
| `'specimens'` | 8 |
| `'localities'` | 7 |

**Never used (2):** `'samples'`, `'unknown'`

### `phylogeny#/$defs/repositories/additionalProperties/properties/type`

3 of 4 members used, 63 occurrences.

| value | count |
|---|---|
| `'institution'` | 42 |
| `'collection'` | 17 |
| `'person'` | 4 |

**Never used (1):** `'unknown'`

### `phylogeny#/$defs/role`

12 of 12 members used, 240 occurrences.

| value | count |
|---|---|
| `'paratype'` | 99 |
| `'holotype'` | 84 |
| `'plesiotype'` | 32 |
| `'syntype'` | 8 |
| `'lectotype'` | 4 |
| `'figured'` | 3 |
| `'hypotype'` | 3 |
| `'topotype'` | 3 |
| `'chirotype'` | 1 |
| `'cotype'` | 1 |
| `'neotype'` | 1 |
| `'paralectotype'` | 1 |

### `phylogeny#/$defs/series`

19 of 47 members used, 97 occurrences.

| value | count |
|---|---|
| `'Middle Ordovician'` | 35 |
| `'Lower Ordovician'` | 21 |
| `'Lower Devonian'` | 8 |
| `'Middle Cambrian'` | 5 |
| `'Middle Devonian'` | 5 |
| `'Holocene'` | 5 |
| `'Lower Cambrian'` | 3 |
| `'Upper Devonian'` | 2 |
| `'Upper Ordovician'` | 2 |
| `'Terrenuevian'` | 2 |
| `'Upper Cambrian'` | 1 |
| `'Lower Mississippian'` | 1 |
| `'Middle Permian'` | 1 |
| `'Upper Permian'` | 1 |
| `'Middle Silurian'` | 1 |
| `'Upper Silurian'` | 1 |
| `'Lower Silurian'` | 1 |
| `'Llandovery'` | 1 |
| `'Cambrian Series 2'` | 1 |

**Never used (28):** `'Miaolingian'`, `'Furongian'`, `'Wenlock'`, `'Ludlow'`, `'Přídolí'`, `'Middle Mississippian'`, `'Upper Mississippian'`, `'Lower Pennsylvanian'`, `'Middle Pennsylvanian'`, `'Upper Pennsylvanian'`, `'Lower Permian'`, `'Cisuralian'`, `'Guadalupian'`, `'Lopingian'`, `'Lower Triassic'`, `'Middle Triassic'`, `'Upper Triassic'`, `'Lower Jurassic'`, `'Middle Jurassic'`, `'Upper Jurassic'`, `'Lower Cretaceous'`, `'Upper Cretaceous'`, `'Paleocene'`, `'Eocene'`, `'Oligocene'`, `'Miocene'`, `'Pliocene'`, `'Pleistocene'`

### `phylogeny#/$defs/stage`

11 of 100 members used, 20 occurrences.

| value | count |
|---|---|
| `'Wuliuan'` | 3 |
| `'Emsian'` | 2 |
| `'Tremadocian'` | 2 |
| `'Eifelian'` | 2 |
| `'Floian'` | 2 |
| `'Katian'` | 2 |
| `'Telychian'` | 2 |
| `'Cambrian Stage 3'` | 2 |
| `'Givetian'` | 1 |
| `'Jiangshanian'` | 1 |
| `'Fortunian'` | 1 |

**Never used (89):** `'Cambrian Stage 2'`, `'Cambrian Stage 4'`, `'Drumian'`, `'Guzhangian'`, `'Paibian'`, `'Cambrian Stage 10'`, `'Dapingian'`, `'Darriwilian'`, `'Sandbian'`, `'Hirnantian'`, `'Rhuddanian'`, `'Aeronian'`, `'Sheinwoodian'`, `'Homerian'`, `'Gorstian'`, `'Ludfordian'`, `'Lochkovian'`, `'Pragian'`, `'Frasnian'`, `'Famennian'`, `'Touraisian'`, `'Viséan'`, `'Serpukhovian'`, `'Baskirian'`, `'Moscovian'`, `'Kasimovian'`, `'Gzhelian'`, `'Asselian'`, `'Sakmarian'`, `'Artinskian'`, `'Kungurian'`, `'Roadian'`, `'Wordian'`, `'Capitanian'`, `'Wuchiapingian'`, `'Changhsingian'`, `'Induan'`, `'Olenekian'`, `'Anisian'`, `'Ladinian'`, `'Carnian'`, `'Norian'`, `'Rhaetian'`, `'Hettangian'`, `'Sinemurian'`, `'Toarcian'`, `'Aalenian'`, `'Bajocian'`, `'Bathonian'`, `'Callovian'`, `'Oxfordian'`, `'Kimmeridgian'`, `'Tithonian'`, `'Berriasian'`, `'Valanginian'`, `'Hauterivian'`, `'Barremian'`, `'Aptian'`, `'Albian'`, `'Cenomanian'`, `'Turonian'`, `'Coniacian'`, `'Santonian'`, `'Campanian'`, `'Maastrichtian'`, `'Danian'`, `'Selanian'`, `'Thanetian'`, `'Ypresian'`, `'Lutetian'`, `'Bartonian'`, `'Priabonian'`, `'Rupelian'`, `'Chattian'`, `'Aquitanian'`, `'Burdigalian'`, `'Langhian'`, `'Serravallian'`, `'Tortonian'`, `'Messinian'`, `'Zanclean'`, `'Piacenzian'`, `'Gelasian'`, `'Calabrian'`, `'Chibanian'`, `'Upper Pleistocene'`, `'Greenlandian'`, `'Northgrippian'`, `'Meghalayan'`

### `phylogeny#/$defs/stageModifier`

3 of 3 members used, 31 occurrences.

| value | count |
|---|---|
| `'upper'` | 15 |
| `'lower'` | 13 |
| `'middle'` | 3 |

### `phylogeny#/$defs/treeDocument/properties/unused/items`

2 of 6 members used, 9 occurrences.

| value | count |
|---|---|
| `'type'` | 5 |
| `'illustrations'` | 4 |

**Never used (4):** `'material'`, `'occurrences'`, `'ranges'`, `'synonyms'`

### `phylogeny#/$defs/typeNode/properties/fixation`

1 of 8 members used, 2 occurrences.

| value | count |
|---|---|
| `'originalDesignation'` | 2 |

**Never used (7):** `'monotypy'`, `'subsequentDesignation'`, `'subsequentMonotypy'`, `'objectiveSynonymy'`, `'tautonymy'`, `'typus'`, `'iczn'`

### `phylogeny#/$defs/uncertaintyFields/properties/monophyly`

1 of 4 members used, 1 occurrences.

| value | count |
|---|---|
| `'nonMonophyletic'` | 1 |

**Never used (3):** `'monophyletic'`, `'paraphyletic'`, `'polyphyletic'`

### `phylogeny#/$defs/uncertaintyFields/properties/sensu`

3 of 4 members used, 8 occurrences.

| value | count |
|---|---|
| `'lato'` | 4 |
| `'stricto'` | 3 |
| `'extenso'` | 1 |

**Never used (1):** `'emendato'`

## 4. Observed value types where the schema allows a union

Tests whether each multi-type declaration is actually needed.

| location | declared | observed | string examples | declared but unseen |
|---|---|---|---|---|
| `phylogeny#/$defs/article/properties/articleNumber` | integer/string | intx6, strx2 | `e1465`, `e38296` | - |
| `phylogeny#/$defs/article/properties/chapter` | integer/string | strx2 | `III. Stamm. Echinodermat...`, `Report of E. Billings, E...` | integer |
| `phylogeny#/$defs/article/properties/number` | integer/string | intx190, strx13 | `Supplement`, `1/2`, `Part 4, No. 220`, `Adv. Pr.` | - |
| `phylogeny#/$defs/article/properties/pages/items` | integer/string | intx486, strx48 | `supplementary 17`, `supplementary 1`, `S637`, `S634` | - |
| `phylogeny#/$defs/article/properties/plates/items` | integer/string | intx31, strx17 | `II`, `I`, `XXXVII`, `VI` | - |
| `phylogeny#/$defs/article/properties/series` | integer/string | intx10, strx4 | `A`, `New Series` | - |
| `phylogeny#/$defs/article/properties/volume` | integer/string | intx292, strx26 | `New Series`, `3: Echinoderms: Notes fo...`, `Report of the 68th Meeti...`, `Eighty-Three Plates to A...` | - |
| `phylogeny#/$defs/citationNumber` | integer/string | intx2875, strx406 | `5f`, `IV`, `X`, `VII` | - |
| `phylogeny#/$defs/cladisticFields/properties/matrix/items` | integer/string | intx139, strx5 | `?` | - |
| `phylogeny#/$defs/editorialObject/properties/corrections/properties/authority/properties/auth` | array/null | nullx7, listx1 | - | - |
| `phylogeny#/$defs/editorialObject/properties/inferred` | boolean/array | boolx42, listx34 | - | - |
| `phylogeny#/$defs/locationFields/properties/illustrations` | array/null | listx197, nullx13 | - | - |
| `phylogeny#/$defs/materialsFields/properties/material` | array/null | listx124, nullx9 | - | - |
| `phylogeny#/$defs/materialsFields/properties/occurrences` | array/null | nullx41, listx28 | - | - |
| `phylogeny#/$defs/materialsFields/properties/ranges` | array/null | listx72, nullx41 | - | - |
| `phylogeny#/$defs/person/properties/death` | integer/null | intx110, nullx1 | - | - |
| `phylogeny#/$defs/phylogeny/properties/characteristics/items/additionalProperties/additionalProperties` | integer/string | intx40 | - | string |
| `phylogeny#/$defs/printedNumber` | string/integer | intx668, strx433 | `HS81`, `HS18`, `HS734A`, `HS84B` | - |
| `phylogeny#/$defs/relationalFields/properties/synonyms` | array/null | listx377 | - | null |
| `phylogeny#/$defs/sectionRecord/properties/name` | string/null | strx11, nullx3 | `Stellatae`, `Radiatae`, `Multivalvia`, `Lunatae` | - |
| `phylogeny#/$defs/taxonRecord/properties/holotype/additionalProperties/items` | array/string/integer | strx1 | `E23470` | array, integer |
| `phylogeny#/$defs/taxonRecord/properties/name` | string/null | strx2617, nullx253 | `Zoophytes`, `Zoophyta`, `Zoophites`, `Zoanthida` | - |
| `tree#/properties/children` | array/null | listx2252, nullx8 | - | - |

