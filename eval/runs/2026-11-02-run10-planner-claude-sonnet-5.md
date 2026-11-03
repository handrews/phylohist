# Grades for `2026-11-02-run10-planner-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 4 | 4 |
| answerable | 17 | 13 |
| as-published | 9 | 6 |
| trajectory | 17 | 14 |
| uncaptured | 9 | 8 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block is contents {"source": "1962_fay", "record": "edrioblastoidea"}
- failure: the answer does not show "Class Edrioblastoidea nov."
- failure: the answer does not show "Genus Astrocystites"
- judge contract 2: Header names only taxon, source restriction (Fay 1962), scope and year; no verdict, summary, or mechanism wording; no question asked.

Plan: {"header": "Astrocystites (genus, Whiteaves 1897); chain of higher taxa as given by Fay 1962 only; taxonomic classification; year 1962", "blocks": [{"tool": "ancestors", "parameters": {"records": ["astrocystites"], "trees": ["taxonomy"], "years": [1962, 1962]}}]}
Header: Astrocystites (genus, Whiteaves 1897); chain of higher taxa as given by Fay 1962 only; taxonomic classification; year 1962
- chains {"records": ["astrocystites"], "include_variants": true, "trees": ["taxonomy"], "years": [1962, 1962]}

> Astrocystites (genus, Whiteaves 1897); chain of higher taxa as given by Fay 1962 only; taxonomic classification; year 1962
> 
> Above Astrocystites Whiteaves 1897: 1 paper, 1 co-author set, 1962
> 
> 1962  Fay  Edrioblastoidea › Astrocystites

### q002 (answerable)

Q: Does Fay (1962) himself write that ottawaensis is the type species of Astrocystites, or is that flag the editor's own inference?

- failure: no composed block is statements {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay"}
- failure: the answer does not show "(editor)"
- failure: the answer does not show "type species"
- judge contract 1: States group and source neutrally with no verdict, but 'entered as an editorial note' is internal provenance/mechanism language rather than scientific-community phrasing.

Plan: {"header": "Statements by Fay (1962) about the genus Astrocystites, to see whether the type-species designation of ottawaensis is stated in the source or entered as an editorial note", "blocks": [{"tool": "statements", "parameters": {"record": "astrocystites", "source": "1962_fay"}}]}
Header: Statements by Fay (1962) about the genus Astrocystites, to see whether the type-species designation of ottawaensis is stated in the source or entered as an editorial note
- list {"record": "astrocystites", "source": "1962_fay", "kind": null, "act_kind": null}

> Statements by Fay (1962) about the genus Astrocystites, to see whether the type-species designation of ottawaensis is stated in the source or entered as an editorial note
> 
> Statements about Astrocystites Whiteaves 1897
>   1962  Fay  cites the name
>   1962  Fay  places it under Edrioblastoidea
>   1962  Fay  moved from Edrioasteroidea
>   1962  Fay  declines a placement in Edrioasteroidea

### q008 (answerable)

Q: In Holloway & Jell (1983), family Rhenopyrgidae is placed under a name that is not itself an order. What is that placeholder, and what does it mean?

- failure: no composed block is contents {"source": "1983_holloway_jell", "record": "edrioasteroidea"}
- judge contract 2: Header names only the taxon and the source opinion, states no verdict or summary; no follow-up question needed since parameters are unambiguous.

Plan: {"header": "Placement of family Rhenopyrgidae in Holloway & Jell (1983): the placeholder parent and its stated meaning", "blocks": [{"tool": "statements", "parameters": {"record": "Rhenopyrgidae", "source": "Holloway & Jell 1983", "kind": "placement"}}]}
Header: Placement of family Rhenopyrgidae in Holloway & Jell (1983): the placeholder parent and its stated meaning
- list {"record": "rhenopyrgidae", "source": "1983_holloway_jell", "kind": "placement", "act_kind": null}

> Placement of family Rhenopyrgidae in Holloway & Jell (1983): the placeholder parent and its stated meaning
> 
> Statements about Rhenopyrgidae Holloway & Jell 1983
>   1983  Holloway & Jell  places it under Order uncertain

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: no composed block is printed_forms {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- failure: no composed block is history {"record": "edrioblastoidina"}
- failure: the answer does not show "Suborder Edrioblastoidina Fay, 1962"
- failure: the answer does not show "class 1962–1982"
- judge contract 1: States records, rank-variant inclusion, trees, scope without verdict; but names Isorophina/Isorophinae rather than the suborder at issue (Edrioblastoidina), a parameter mismatch.

Plan: {"header": "Family Rhenopyrgidae (Holloway & Jell 1983) traced through Ewin et al. (2020)'s classification to show the suborder printed above it, and the suborder-group name Isorophina/Isorophinae (Bell 1976, taken with its subfamily-rank variant) traced across all sources to find at what rank it was first established; taxonomic classifications only.", "blocks": [{"tool": "ancestors", "parameters": {"records": ["rhenopyrgidae"], "years": [2020, 2020], "trees": ["taxonomy"]}}, {"tool": "history", "parameters": {"record": "isorophina", "include_related": true, "trees": ["taxonomy"]}}]}
Header: Family Rhenopyrgidae (Holloway & Jell 1983) traced through Ewin et al. (2020)'s classification to show the suborder printed above it, and the suborder-group name Isorophina/Isorophinae (Bell 1976, taken with its subfamily-rank variant) traced across all sources to find at what rank it was first established; taxonomic classifications only.
- chains {"records": ["rhenopyrgidae"], "include_variants": true, "trees": ["taxonomy"], "years": [2020, 2020]}
- timeline {"record": "isorophina", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Family Rhenopyrgidae (Holloway & Jell 1983) traced through Ewin et al. (2020)'s classification to show the suborder printed above it, and the suborder-group name Isorophina/Isorophinae (Bell 1976, taken with its subfamily-rank variant) traced across all sources to find at what rank it was first established; taxonomic classifications only.
> 
> Above Rhenopyrgidae Holloway & Jell 1983: 1 paper, 1 co-author set, 2020
> 
> 2020  Ewin et al.  Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 
> Isorophina Bell 1976: 15 papers, 10 co-author sets, 1976–2011
> suborder since 1976 (10 papers), unranked 2006–2010 (5 papers), subfamily 1985 (1 paper)
> in Isorophida since 1976 (14 papers, 9 co-author sets), in Edrioasteroidea 2006 (1 paper), in Agelacrinitidae 1985 (1 paper)
> 
> 1976  Bell               Isorophina, in Isorophida; named as new
> 1976  Bell & Petersen    Isorophina, in Isorophida
> 1980  Bell               Isorophina, in Isorophida (p. 165)
> 1985  Smith              Isorophina, in Isorophida
> 1985  Smith              Isorophinae, in Agelacrinitidae; nomen translatum from Isorophina
> 1987  Smith & Arbizu     Isorophinae, cited as a synonym of Agelacrinitinae
> 1992  Sumrall            Isorophina, in Isorophida
> 1996  Sumrall            Isorophina, in Isorophida
> 1996  Sumrall & Bowsher  Isorophina, in Isorophida
> 2000  Sumrall et al.     Isorophina, in Isorophida
> 2001  Sumrall            Isorophina, in Isorophida
> 2006  Sumrall et al.     Isorophina, in Edrioasteroidea (p. 190)
> 2006  Sumrall et al.     Isorophina, in Isorophida
> 2009  Sumrall            Isorophina, in Isorophida (p. 991)
> 2009  Sumrall et al.     Isorophina, in Isorophida (p. 801)
> 2010  Sumrall            Isorophina, in Isorophida (p. 789)
> 2011  Sumrall & Zamora   Isorophina, in Isorophida

### q026 (as-published)

Q: What two different words does Fay (1962) use for the same specimen, No. 752, in Astrocystites ottawaensis?

- failure: no composed block is statements {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay", "kind": "material"}
- failure: the answer does not show "752 [gsc]"
- judge contract 2: Header names only taxon, specimen, and source scope in neutral community language; no verdict, summary, or mechanism word; no question needed.

Plan: {"header": "Specimen No. 752 cited under Astrocystites ottawaensis (Whiteaves 1897), citation history across sources including Fay 1962", "blocks": [{"tool": "specimen_history", "parameters": {"number": "No. 752"}}]}
Header: Specimen No. 752 cited under Astrocystites ottawaensis (Whiteaves 1897), citation history across sources including Fay 1962
- statement {"number": "No. 752", "repository": null}

> Specimen No. 752 cited under Astrocystites ottawaensis (Whiteaves 1897), citation history across sources including Fay 1962
> 
> No source in the corpus mentions the specimen No. 752.

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- judge contract 2: Header names only the taxon, rank-variant scope, and source/year; no verdict, summary, or mechanism word; no clarifying question needed for this specific as-published request.

Plan: {"header": "Rhenopyrginae (subfamily rank, a.k.a. Rhenopyrgidae group) as printed by Guensburg & Sprinkle (1994)", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}}]}
Header: Rhenopyrginae (subfamily rank, a.k.a. Rhenopyrgidae group) as printed by Guensburg & Sprinkle (1994)
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}

> Rhenopyrginae (subfamily rank, a.k.a. Rhenopyrgidae group) as printed by Guensburg & Sprinkle (1994)
> 
> Rhenopyrginae (Subfamily)
>   1994 "Subfamily Rhenopyrginae emend. nom. transl." (the heading as entered; no verbatim form is recorded) Guensburg & Sprinkle 1994

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: no composed block is printed_forms {"record": "cambraster"}
- failure: the answer does not show "Cabibel, Termier, and Termier, 1958"
- judge contract 1: Parameters otherwise clean, but '(Jaekel 1923)' pre-judges the very disputed attribution the query investigates — one embedded verdict; no question needed otherwise.

Plan: {"header": "Authorship of the genus Cambraster (Jaekel 1923) across all sources citing it; no synonyms or variant ranks; all years", "blocks": [{"tool": "history", "parameters": {"record": "cambraster"}}]}
Header: Authorship of the genus Cambraster (Jaekel 1923) across all sources citing it; no synonyms or variant ranks; all years
- timeline {"record": "cambraster", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Authorship of the genus Cambraster (Jaekel 1923) across all sources citing it; no synonyms or variant ranks; all years
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

### q038 (absent)

Q: What does Klug et al. (2008) themselves print in their protologue for Rhenopyrgus flos?

- note: text beside the submission: The corpus has no source matching Klug et al. (2008), even though "Rhenopyrgus f
- judge contract 2: Header neutrally restates the requested item only, no verdict, summary, or mechanism language; no question asked where parameters are unambiguous.

Plan: {"header": "Requested: the protologue text Klug et al. (2008) print for Rhenopyrgus flos", "blocks": [{"tool": "gap", "parameters": {"source": "Klug et al. 2008", "kind": "newTaxa"}}]}
Header: Requested: the protologue text Klug et al. (2008) print for Rhenopyrgus flos
- statement {"source": "Klug et al. 2008", "kind": "newTaxa"}

> Requested: the protologue text Klug et al. (2008) print for Rhenopyrgus flos
> 
> No source in the corpus mentions the source Klug et al. 2008.

### q039 (absent)

Q: Which sources place the genus Rhenoblastus, and where?

- note: text beside the submission: No source in the corpus carries the name "Rhenoblastus," so I can't build a plac
- judge contract 2: Header merely scopes the search for a nonexistent name; no taxonomic verdict or mechanism language, and no spurious question for an absent-name case.

Plan: {"header": "Rhenoblastus: name not found in the corpus", "blocks": [{"tool": "gap", "parameters": {"name": "Rhenoblastus"}}]}
Header: Rhenoblastus: name not found in the corpus
- statement {"name": "Rhenoblastus"}

> Rhenoblastus: name not found in the corpus
> 
> No source in the corpus mentions the name Rhenoblastus.

### q045 (trajectory)

Q: Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

- failure: no composed block is history {"record": "rhenopyrgidae"}
- judge contract 2: Header lists only group, rank variant, placement traced, and year range; no verdict, summary, or mechanism language; no question needed.

Plan: {"header": "Rhenopyrgidae (family, including its rhenopyrginae variant) considered as placed under Cyathocystidae; all years, taxonomic placements and rejections only", "blocks": [{"tool": "placed_under", "parameters": {"record": "Rhenopyrgidae", "parent": "Cyathocystidae"}}, {"tool": "statements", "parameters": {"record": "Rhenopyrgidae", "kind": "rejection"}}]}
Header: Rhenopyrgidae (family, including its rhenopyrginae variant) considered as placed under Cyathocystidae; all years, taxonomic placements and rejections only
- chains {"record": "rhenopyrgidae", "parent": "cyathocystidae", "include_variants": true, "trees": ["taxonomy"], "years": null}
- list {"record": "rhenopyrgidae", "source": null, "kind": "rejection", "act_kind": null}

> Rhenopyrgidae (family, including its rhenopyrginae variant) considered as placed under Cyathocystidae; all years, taxonomic placements and rejections only
> 
> Rhenopyrgidae Holloway & Jell 1983 under Cyathocystidae Bather 1899: 2 papers, 2 co-author sets, 1994–2000
> first Guensburg & Sprinkle 1994, last Grigo 2000
> 
> 1994  Guensburg & Sprinkle  Rhenopyrginae
> 2000  Grigo                 Rhenopyrginae
> 
> Statements about Rhenopyrgidae Holloway & Jell 1983
>   2013  Sumrall et al.  declines a placement in Cyathocystidae

### q048 (trajectory)

Q: What did Holloway & Jell (1983) say Dehm (1961) did with Pyrgocystis octogona, and what does Dehm's own paper do?

- failure: no composed block is gap {"source": "1983_holloway_jell", "kind": "synonymy"}
- failure: the answer does not show "The synonymy printed in Holloway & Jell 1983 has not yet been entered"
- judge contract 2: Header names only the taxon and the two sources' statements; no verdict, summary, or mechanism word; no question asked, which is acceptable.

Plan: {"header": "Statements about Pyrgocystis (Rhenopyrgus) octogona Richter 1930: Holloway & Jell (1983) synonymy report of Dehm's (1961) treatment, and Dehm's (1961) own statements about the species", "blocks": [{"tool": "statements", "parameters": {"record": "coronaeformis_rievers_1961", "source": "Holloway & Jell 1983", "kind": "act"}}, {"tool": "statements", "parameters": {"record": "octogona_richter.r_1930", "source": "Dehm 1961"}}]}
Header: Statements about Pyrgocystis (Rhenopyrgus) octogona Richter 1930: Holloway & Jell (1983) synonymy report of Dehm's (1961) treatment, and Dehm's (1961) own statements about the species
- list {"record": "coronaeformis_rievers_1961", "source": "1983_holloway_jell", "kind": "act", "act_kind": null}
- list {"record": "octogona_richter.r_1930", "source": "1961_dehm", "kind": null, "act_kind": null}

> Statements about Pyrgocystis (Rhenopyrgus) octogona Richter 1930: Holloway & Jell (1983) synonymy report of Dehm's (1961) treatment, and Dehm's (1961) own statements about the species
> 
> Statements about Pyrgocystis coronaeformis Rievers 1961
>   1983  Holloway & Jell  Rhenopyrgus coronaeformis: type species
> 
> Statements about Pyrgocystis octogona Richter 1930
>   1961  Dehm  cites the name (cited p. 294)
>   1961  Dehm  places it under Pyrgocystis (cited p. 294)
>   1961  Dehm  occurrence bornich: Lower Devonian; greywacke slates; Bornich, near Weisel on the Rhine, Germany (cited p. 294)

### q053 (answerable)

Q: What is the "kalckballar" that Tilas (1740) figures, and what did later authors make of it?

- failure: the answer does not show "accepts kalckballar (Tilas 1740) as Sphaeronites aurantium"
- judge contract 2: States only record identity, authority, scope of sources, all years, no synonyms/variants; no verdict or mechanism; no question needed for answerable case.

Plan: {"header": "The record is \"kalckballar\", a mineral-type designation (a lime-ball concretion) under which Tilas (1740) figured the fossil, authority Tilas 1740; showing Tilas's own statements about it and the history of how all later sources treated the name, all years, no synonyms or variants beyond this single record.", "blocks": [{"tool": "statements", "parameters": {"record": "kalckballar_tilas_1740", "source": "Tilas 1740"}}, {"tool": "history", "parameters": {"record": "kalckballar_tilas_1740"}}]}
Header: The record is "kalckballar", a mineral-type designation (a lime-ball concretion) under which Tilas (1740) figured the fossil, authority Tilas 1740; showing Tilas's own statements about it and the history of how all later sources treated the name, all years, no synonyms or variants beyond this single record.
- list {"record": "kalckballar_tilas_1740", "source": "1740_tilas", "kind": null, "act_kind": null}
- timeline {"record": "kalckballar_tilas_1740", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> The record is "kalckballar", a mineral-type designation (a lime-ball concretion) under which Tilas (1740) figured the fossil, authority Tilas 1740; showing Tilas's own statements about it and the history of how all later sources treated the name, all years, no synonyms or variants beyond this single record.
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

### q056 (uncaptured)

Q: What classification does Vanuxem (1842) print for the fossils of New York's third district?

- failure: nothing composed: the submission names no block that could be shown
- failure: no composed block is gap {"source": "1842_vanuxem", "kind": "skeleton"}
- failure: the answer does not show "has not yet been entered (only part of it is entered so far)"
- judge contract 2: Header records only group, source tree, synonymy setting and year range; no summary, mechanism or verdict; omitted question is permissible.

Plan: {"header": "Taken as the Echinodermata; classification as printed by Vanuxem (1842) alone; no synonymy; all years.", "blocks": [{"tool": "contents", "parameters": {"source": "Vanuxem 1842", "record": "echinodermata"}}]}
Plan errors: [{"block": 1, "tool": "contents", "parameters": {"source": "Vanuxem 1842", "record": "echinodermata"}, "error": "returned no block; the corpus holds nothing for these parameters; Vanuxem 1842 declares the classification partly entered; plan gap(source=\"1842_vanuxem\", kind=\"skeleton\")"}]
Header: Taken as the Echinodermata; classification as printed by Vanuxem (1842) alone; no synonymy; all years.

> 

