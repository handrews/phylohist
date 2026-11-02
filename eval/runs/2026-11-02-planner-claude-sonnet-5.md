# Grades for `2026-11-02-planner-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 4 | 4 |
| answerable | 17 | 13 |
| as-published | 9 | 5 |
| trajectory | 17 | 14 |
| uncaptured | 9 | 7 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block is contents {"source": "1962_fay", "record": "edrioblastoidea"}
- failure: the answer does not show "Class Edrioblastoidea nov."
- failure: the answer does not show "Genus Astrocystites"
- judge contract 2: Header lists only scope (genus, higher chain, tree type, year 1962) in neutral taxonomic language; no verdict, summary, or mechanism wording.

Plan: {"header": "Astrocystites (genus); chain of taxa above it as given by Fay 1962; classification tree; year restricted to 1962", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"], "trees": ["taxonomy"], "years": [1962, 1962]}}]}
Header: Astrocystites (genus); chain of taxa above it as given by Fay 1962; classification tree; year restricted to 1962
- chains {"records": ["astrocystites"], "include_variants": true, "trees": ["taxonomy"], "years": [1962, 1962]}

> Astrocystites (genus); chain of taxa above it as given by Fay 1962; classification tree; year restricted to 1962
> 
> Above Astrocystites Whiteaves 1897: 1 paper, 1 co-author set, 1962
> 
> 1962  Fay  Edrioblastoidea › Astrocystites

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: no composed block is printed_forms {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- failure: no composed block is history {"record": "edrioblastoidina"}
- failure: the answer does not show "Suborder Edrioblastoidina Fay, 1962"
- failure: the answer does not show "class 1962–1982"
- judge contract 2: Header lists only record, source scope, tree type, year range in community language; no verdict or summary; no question needed since parameters unambiguous.

Plan: {"header": "Rhenopyrgidae taken as the family record; ancestor chains from every source shown in year order, classification (taxonomy) tree only, all years, to find both the suborder heading Ewin et al. (2020) print above it and the rank at which that name first appears in the record", "blocks": [{"tool": "ancestors", "parameters": {"records": ["Rhenopyrgidae"], "trees": ["taxonomy"]}}]}
Header: Rhenopyrgidae taken as the family record; ancestor chains from every source shown in year order, classification (taxonomy) tree only, all years, to find both the suborder heading Ewin et al. (2020) print above it and the rank at which that name first appears in the record
- chains {"records": ["rhenopyrgidae"], "include_variants": true, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae taken as the family record; ancestor chains from every source shown in year order, classification (taxonomy) tree only, all years, to find both the suborder heading Ewin et al. (2020) print above it and the rank at which that name first appears in the record
> 
> Above Rhenopyrgidae Holloway & Jell 1983: 7 papers, 7 co-author sets, 1983–2020
> 
> 1983  Holloway & Jell       Edrioasteroidea › Order uncertain › Rhenopyrgidae
> 1994  Guensburg & Sprinkle  Echinozoa › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Cyathocystidae › Rhenopyrginae
> 2000  Grigo                 Edrioasteroidea › Edrioasterida › Edrioblastoidina › Cyathocystidae › Rhenopyrginae
> 2010  Müller & Hahn         Isorophida › Rhenopyrgidae
> 2013  Sumrall et al.        Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 2017  Briggs et al.         Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 2020  Ewin et al.           Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae

### q026 (as-published)

Q: What two different words does Fay (1962) use for the same specimen, No. 752, in Astrocystites ottawaensis?

- failure: no composed block is statements {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay", "kind": "material"}
- failure: the answer does not show "752 [gsc]"
- judge contract 2: Header names only the specimen, taxon, source, and scope restriction; no verdict, summary, or mechanism; no question needed since scope is unambiguous.

Plan: {"header": "Specimen \"No. 752\" cited under Astrocystites ottawaensis by Fay 1962 — specimen citation history, this source only", "blocks": [{"tool": "specimen_history", "parameters": {"number": "No. 752", "source": "Fay 1962", "label": "No. 752"}}]}
Header: Specimen "No. 752" cited under Astrocystites ottawaensis by Fay 1962 — specimen citation history, this source only
- statement {"number": "No. 752", "repository": null}

> Specimen "No. 752" cited under Astrocystites ottawaensis by Fay 1962 — specimen citation history, this source only
> 
> No source in the corpus mentions the specimen No. 752.

### q027 (as-published)

Q: What two years does Sprinkle & Sumrall (2015) print for coordinate names from the same Bather work, Suborder Edrioasterina and Family Edrioasteridae?

- failure: no composed block is printed_forms {"record": "edrioasterina", "source": "2015_sprinkle_sumrall"}
- failure: no composed block is printed_forms {"record": "edrioasteridae", "source": "2015_sprinkle_sumrall"}
- failure: the answer does not show "Bather, 1898"
- failure: the answer does not show "Bather, 1899"
- judge contract 2: Header lists only names, ranks, source, record type and year; no verdict or mechanism; no question needed as parameters are unambiguous.

Plan: {"header": "Edrioasterina (Suborder) and Edrioasteridae (Family), both attributed to Bather, as cited by Sprinkle & Sumrall (2015); usage statements only, year 2015", "blocks": [{"tool": "statements", "parameters": {"record": "edrioasterina", "source": "Sprinkle & Sumrall 2015", "kind": "usage"}}, {"tool": "statements", "parameters": {"record": "edrioasteridae", "source": "Sprinkle & Sumrall 2015", "kind": "usage"}}]}
Header: Edrioasterina (Suborder) and Edrioasteridae (Family), both attributed to Bather, as cited by Sprinkle & Sumrall (2015); usage statements only, year 2015
- list {"record": "edrioasterina", "source": "2015_sprinkle_sumrall", "kind": "usage", "act_kind": null}
- list {"record": "edrioasteridae", "source": "2015_sprinkle_sumrall", "kind": "usage", "act_kind": null}

> Edrioasterina (Suborder) and Edrioasteridae (Family), both attributed to Bather, as cited by Sprinkle & Sumrall (2015); usage statements only, year 2015
> 
> Statements about Edrioasterina Bather 1898
>   2015  Sprinkle & Sumrall  cites the name (p. 348)
> 
> Statements about Edrioasteridae Bather 1899
>   2015  Sprinkle & Sumrall  cites the name (p. 348)

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- judge contract 2: Header names only taxon, source, year, and the requested printed heading/act; no summary or verdict; absent question is acceptable since parameters are unambiguous.

Plan: {"header": "Rhenopyrginae (subfamily rank of Rhenopyrgidae) as printed by Guensburg & Sprinkle (1994): exact heading and placement act", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrginae", "source": "Guensburg & Sprinkle 1994"}}, {"tool": "statements", "parameters": {"record": "rhenopyrginae", "source": "Guensburg & Sprinkle 1994", "kind": "placement"}}]}
Header: Rhenopyrginae (subfamily rank of Rhenopyrgidae) as printed by Guensburg & Sprinkle (1994): exact heading and placement act
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle", "kind": "placement", "act_kind": null}

> Rhenopyrginae (subfamily rank of Rhenopyrgidae) as printed by Guensburg & Sprinkle (1994): exact heading and placement act
> 
> Rhenopyrginae (Subfamily)
>   1994 "Subfamily Rhenopyrginae emend. nom. transl." (the heading as entered; no verbatim form is recorded) Guensburg & Sprinkle 1994
> 
> Statements about Rhenopyrginae Holloway & Jell 1983
>   1994  Guensburg & Sprinkle  places it under Cyathocystidae

### q032 (trajectory)

Q: What class or order has Astrocystites been placed in, across the sources that treat it?

- note: text beside the submission: Using the ancestors block for Astrocystites across all sources, showing each sou
- judge contract 2: Header lists only scope parameters (genus, all treating sources, all trees, all years) in community terms, no verdict or summary; no question needed.

Plan: {"header": "Astrocystites (genus); ancestors shown across all sources that treat it, all classification trees, all years", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"]}}]}
Header: Astrocystites (genus); ancestors shown across all sources that treat it, all classification trees, all years
- chains {"records": ["astrocystites"], "include_variants": true, "trees": ["taxonomy"], "years": null}

> Astrocystites (genus); ancestors shown across all sources that treat it, all classification trees, all years
> 
> Above Astrocystites Whiteaves 1897: 12 papers, 9 co-author sets, 1897–1994
> 
> 1897  Whiteaves             Cystoidea › Diploporitidae › Astrocystites
> 1935  Bassler               Edrioasteroidea › ? Astrocystitidae (or Blastoidea) › Astrocystites
> 1936  Bassler               Blastoidea › Protoblastoidea › ? Astrocystites
> 1962  Fay                   Edrioblastoidea › Astrocystites
> 1967  Fay                   Echinodermata › Crinozoa › Edrioblastoidea › Pentacystida › Astrocystitidae › Astrocystites
> 1968  Webby                 Pelmatozoa › Edrioblastoidea › Steganoblastidae › Astrocystites
> 1970  Mintz                 Crinozoa › Edrioblastoidea › Astrocystitidae › Astrocystites
> 1973  Sprinkle              Echinodermata › Echinozoa › Edrioblastoidea › Astrocystites
> 1980  Bell                  Edrioblastoidea › Astrocystitidae › Astrocystites
> 1982  Sprinkle              Echinodermata › Echinozoa › Edrioblastoidea › Pentacystida › Steganoblastidae › Astrocystites
> 1990  Smith & Jell          Edrioasteroidea › Edrioblastoida › Astrocystitidae › Astrocystites
> 1994  Guensburg & Sprinkle  Echinozoa › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Astrocystitidae › Astrocystites

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: no composed block is printed_forms {"record": "cambraster"}
- failure: the answer does not show "Cabibel, Termier, and Termier, 1958"
- judge contract 2: Header names only the taxon, scope of synonyms/ranks, and year range in standard terms; no verdict, summary, or mechanism; no question needed.

Plan: {"header": "Cambraster taken as the genus; authorship across all sources that make statements about it; no synonyms or variant ranks involved; all years.", "blocks": [{"tool": "history", "parameters": {"record": "cambraster", "include_related": false}}]}
Header: Cambraster taken as the genus; authorship across all sources that make statements about it; no synonyms or variant ranks involved; all years.
- timeline {"record": "cambraster", "include_related": false, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Cambraster taken as the genus; authorship across all sources that make statements about it; no synonyms or variant ranks involved; all years.
> 
> Cambraster Jaekel 1923: 5 papers, 5 co-author sets, 1985–2021
> in Stromatocystitidae since 1985 (3 papers), in Family uncertain 1994 (1 paper), in Isorophida 1985 (1 paper)
> 
> 1985  Jell et al.           Cambraster, in Stromatocystitidae
> 1985  Smith                 Cambraster, in Isorophida
> 1985  Smith                 Cambraster
> 1994  Guensburg & Sprinkle  Cambraster, in Family uncertain
> 2013  Zamora et al.         Cambraster, in Stromatocystitidae
> 2021  Jell & Sprinkle       Cambraster, in Stromatocystitidae

### q035 (trajectory)

Q: Is Isorophus (and its sibling genus Carneyella) attributed to Foerste 1916 or 1917?

- failure: no composed block is history {"record": "isorophus"}
- failure: no composed block is history {"record": "carneyella"}
- failure: the answer does not show "Isorophus Foerste 1916"
- failure: the answer does not show "Carneyella Foerste 1916"
- judge contract 2: Header lists only scope parameters: two genera, synonyms/variants excluded, all sources, all years; no summary, mechanism, or verdict; no unnecessary question.

Plan: {"header": "Isorophus and Carneyella taken as the genera (no synonyms/variants, no related taxa); printed forms across all sources, all years", "blocks": [{"tool": "printed_forms", "parameters": {"record": "Isorophus"}}, {"tool": "printed_forms", "parameters": {"record": "Carneyella"}}]}
Header: Isorophus and Carneyella taken as the genera (no synonyms/variants, no related taxa); printed forms across all sources, all years
- list {"record": "isorophus", "source": null}
- list {"record": "carneyella", "source": null}

> Isorophus and Carneyella taken as the genera (no synonyms/variants, no related taxa); printed forms across all sources, all years
> 
> Isorophus (genus)
>   1994 "Isorophus Foerste, 1917" Guensburg & Sprinkle 1994
> 
> Carneyella (genus)
>   1994 "Carneyella Foerste, 1917" Guensburg & Sprinkle 1994

### q039 (absent)

Q: Which sources place the genus Rhenoblastus, and where?

- note: text beside the submission: No source in the corpus carries the name "Rhenoblastus".
- judge contract 1: Header announces the finding ("Gap: not carried by any source") rather than stating only scope parameters — one verdict-style lapse; no question needed.

Plan: {"header": "Gap: the name \"Rhenoblastus\" is not carried by any source in the corpus", "blocks": [{"tool": "gap", "parameters": {"name": "Rhenoblastus"}}]}
Header: Gap: the name "Rhenoblastus" is not carried by any source in the corpus
- statement {"name": "Rhenoblastus"}

> Gap: the name "Rhenoblastus" is not carried by any source in the corpus
> 
> No source in the corpus mentions the name Rhenoblastus.

### q045 (trajectory)

Q: Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

- failure: no composed block is placed_under {"record": "rhenopyrgidae", "parent": "cyathocystidae"}
- failure: the answer does not show "first Guensburg & Sprinkle 1994"
- judge contract 2: Header lists only group, rank-variant inclusion, source scope, year range, and tree type; no summary, mechanism, or verdict; no spurious question.

Plan: {"header": "Rhenopyrgidae (including the subfamily rank form Rhenopyrginae) taken as the group; its history of placement under Cyathocystidae traced across all sources, all years, taxonomic trees only", "blocks": [{"tool": "history", "parameters": {"record": "rhenopyrgidae"}}]}
Header: Rhenopyrgidae (including the subfamily rank form Rhenopyrginae) taken as the group; its history of placement under Cyathocystidae traced across all sources, all years, taxonomic trees only
- timeline {"record": "rhenopyrgidae", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae (including the subfamily rank form Rhenopyrginae) taken as the group; its history of placement under Cyathocystidae traced across all sources, all years, taxonomic trees only
> 
> Rhenopyrgidae Holloway & Jell 1983: 7 papers, 7 co-author sets, 1983–2020
> family since 1983 (5 papers), subfamily 1994–2000 (2 papers)
> in Edrioblastoidina since 2013 (3 papers), in Isorophida 2010 (1 paper), in Cyathocystidae 1994–2000 (2 papers), in Order uncertain 1983 (1 paper)
> 
> 1983  Holloway & Jell       Rhenopyrgidae, in Order uncertain; named as new
> 1994  Guensburg & Sprinkle  Rhenopyrginae, in Cyathocystidae; emended; nomen translatum from Rhenopyrgidae
> 2000  Grigo                 Rhenopyrginae, in Cyathocystidae
> 2010  Müller & Hahn         Rhenopyrgidae, in Isorophida
> 2013  Sumrall et al.        Rhenopyrgidae, in Edrioblastoidina; emended; moved from Cyathocystidae; declines a placement in Cyathocystidae
> 2017  Briggs et al.         Rhenopyrgidae, in Edrioblastoidina
> 2020  Ewin et al.           Rhenopyrgidae, in Edrioblastoidina; emended (p. 118)

### q053 (answerable)

Q: What is the "kalckballar" that Tilas (1740) figures, and what did later authors make of it?

- failure: the answer does not show "accepts kalckballar (Tilas 1740) as Sphaeronites aurantium"
- judge contract 1: Parameters (record, scope, years, trees) stated plainly, no question needed; but the gloss "a mineral-form name" pre-empts answer content as a summary.

Plan: {"header": "The record \"kalckballar\" (Tilas 1740, a mineral-form name) taken alone; later treatments shown via its full history across sources; all years; classifications only", "blocks": [{"tool": "statements", "parameters": {"record": "kalckballar_tilas_1740", "source": "Tilas 1740"}}, {"tool": "history", "parameters": {"record": "kalckballar_tilas_1740"}}]}
Header: The record "kalckballar" (Tilas 1740, a mineral-form name) taken alone; later treatments shown via its full history across sources; all years; classifications only
- list {"record": "kalckballar_tilas_1740", "source": "1740_tilas", "kind": null, "act_kind": null}
- timeline {"record": "kalckballar_tilas_1740", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> The record "kalckballar" (Tilas 1740, a mineral-form name) taken alone; later treatments shown via its full history across sources; all years; classifications only
> 
> Statements about kalckballar Tilas 1740
>   1740  Tilas  cites the name (p. 196)
>   1740  Tilas  named as new (p. 196)
>   1740  Tilas  illustration: pl. II, fig. 18 (p. 196)
> 
> kalckballar Tilas 1740: 1 paper, 1 co-author set, 1740
> 
> 1740  Tilas  kalckballar; named as new (p. 196)
> 1844  Buch   kalckballar, cited as a synonym of Sphaeronites aurantium

### q055 (uncaptured)

Q: What does the Vermes part of Gmelin's thirteenth edition of the Systema Naturae (1791, part 6) place under Echinus?

- failure: nothing composed: the submission names no block that could be shown
- failure: no composed block is gap {"source": "1791a_gmelin", "kind": "skeleton"}
- failure: the answer does not show "Gmelin 1791 is on record; its content has not yet been entered"
- judge contract 1: Parameters and part cited correctly, no verdict; but Echinus is labelled an "order" with an unwarranted "(Leske, 1778)" authority — one lapse.

Plan: {"header": "Contents placed under the order Echinus (Leske, 1778) according to Gmelin 1791 (Systema Naturae, 13th ed., vol. 1, pt. 6, \"Vermes\")", "blocks": [{"tool": "contents", "parameters": {"source": "1791a_gmelin", "record": "echinus_leske_1778"}}]}
Plan errors: [{"block": 1, "tool": "contents", "parameters": {"source": "1791a_gmelin", "record": "echinus_leske_1778"}, "error": "returned no block; the corpus holds nothing for these parameters"}]
Header: Contents placed under the order Echinus (Leske, 1778) according to Gmelin 1791 (Systema Naturae, 13th ed., vol. 1, pt. 6, "Vermes")

> 

### q056 (uncaptured)

Q: What classification does Vanuxem (1842) print for the fossils of New York's third district?

- failure: nothing composed: the submission names no block that could be shown
- failure: no composed block is gap {"source": "1842_vanuxem", "kind": "skeleton"}
- failure: the answer does not show "has not yet been entered (only part of it is entered so far)"
- judge contract 1: Parameters stated plainly with no verdict, but "as printed in the report" implies complete printed coverage of a source only partly captured.

Plan: {"header": "Contents that Vanuxem (1842) places under Echinodermata, as printed in the Geology of New York's third district report", "blocks": [{"tool": "contents", "parameters": {"source": "Vanuxem 1842", "record": "echinodermata"}}]}
Plan errors: [{"block": 1, "tool": "contents", "parameters": {"source": "Vanuxem 1842", "record": "echinodermata"}, "error": "returned no block; the corpus holds nothing for these parameters"}]
Header: Contents that Vanuxem (1842) places under Echinodermata, as printed in the Geology of New York's third district report

> 

### q057 (answerable)

Q: Which papers cite the University of Queensland specimen F. 5404, and as what?

- failure: no composed block is specimen_history {"number": "UQF 5404"}
- failure: the answer does not show "Specimen UQF 5404 (University of Queensland, fossil register)"
- failure: the answer does not show "Whitehouse"
- failure: the answer does not show "Jell & Sprinkle"
- failure: the answer does not show "holotype of Peridionites navicula"
- judge contract 1: States scope and sources neutrally with no verdict, but the hybrid form "UQF F. 5404" is not community usage and presupposes the identity at issue.

Plan: {"blocks": [{"tool": "specimen_history", "parameters": {"number": "F. 5404", "repository": "UQF"}}], "header": "Citation history of the University of Queensland specimen UQF F. 5404, across all sources that cite it", "question": null}
Header: Citation history of the University of Queensland specimen UQF F. 5404, across all sources that cite it
- statement {"number": "F. 5404", "repository": "UQF"}

> Citation history of the University of Queensland specimen UQF F. 5404, across all sources that cite it
> 
> No source in the corpus mentions the specimen F. 5404.

### q059 (answerable)

Q: Which genera and species does Buch (1844) list in his new Cystideen, and which is the type genus?

- failure: nothing composed: the submission names no block that could be shown
- failure: no composed block is contents {"source": "1844_buch", "record": "cystideen"}
- failure: the answer does not show "Cystideen nov."
- failure: the answer does not show "Type genus. Sphaeronites"
- failure: the answer does not show "Genus Sycocystites gen. nov."
- failure: the answer does not show "Cryptocrinites cerasus"
- judge contract 2: Header states only scope parameters (source, taxa, ranks, type genus shown) in community language, no verdict or summary; no question needed.

Plan: {"header": "Contents of Buch 1844's \"Cystideen\" (Cystoidea), genera and species included, with the type genus marked; single source, all ranks shown", "blocks": [{"tool": "contents", "parameters": {"source": "Buch 1844", "record": "Cystoidea", "depth": 3}}]}
Plan errors: [{"block": 1, "tool": "contents", "parameters": {"source": "Buch 1844", "record": "Cystoidea", "depth": 3}, "error": "returned no block; the corpus holds nothing for these parameters"}]
Header: Contents of Buch 1844's "Cystideen" (Cystoidea), genera and species included, with the type genus marked; single source, all ranks shown

> 

