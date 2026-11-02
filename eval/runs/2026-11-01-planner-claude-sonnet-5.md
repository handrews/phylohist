# Grades for `2026-11-01-planner-claude-sonnet-5.jsonl`

| class | questions | mechanical pass |
|---|---|---|
| absent | 4 | 4 |
| answerable | 17 | 14 |
| as-published | 9 | 5 |
| trajectory | 17 | 15 |
| uncaptured | 9 | 7 |

## Failures and notes

### q001 (answerable)

Q: What new class does Fay (1962) erect for the genus Astrocystites, and what family/order sit between the genus and the class?

- failure: no composed block is contents {"source": "1962_fay", "record": "edrioblastoidea"}
- failure: the answer does not show "Class Edrioblastoidea nov."
- failure: the answer does not show "Genus Astrocystites"
- judge contract 2: Header lists only scope parameters—taxon, source, classification-only, year—in community language, with no summary, mechanism, or verdict; no question asked.

Plan: {"header": "Astrocystites (genus); chain of taxa above it as given by Fay 1962; classification scheme only; year restricted to 1962", "blocks": [{"tool": "ancestors", "parameters": {"records": ["Astrocystites"], "trees": ["taxonomy"], "years": [1962, 1962]}}]}
Header: Astrocystites (genus); chain of taxa above it as given by Fay 1962; classification scheme only; year restricted to 1962
- chains {"records": ["astrocystites"], "include_variants": true, "trees": ["taxonomy"], "years": [1962, 1962]}

> Astrocystites (genus); chain of taxa above it as given by Fay 1962; classification scheme only; year restricted to 1962
> 
> Above Astrocystites Whiteaves 1897: 1 paper, 1 co-author set, 1962
> 
> 1962  Fay  Edrioblastoidea › Astrocystites

### q009 (answerable)

Q: What new species of Rhenopyrgus does Grigo (2000) describe, and from where?

- failure: no composed block is gap {"source": "2000_grigo", "kind": "occurrences"}
- judge contract 2: Header names only the genus, the single source and its year, scope limited to that source; no summary, mechanism, or verdict; no clarifying question needed.

Plan: {"header": "Rhenopyrgus (genus) as placed by Grigo (2000): systematic contents of that source only", "blocks": [{"tool": "contents", "parameters": {"source": "Grigo 2000", "record": "Rhenopyrgus"}}]}
Header: Rhenopyrgus (genus) as placed by Grigo (2000): systematic contents of that source only
- classification {"source": "2000_grigo", "record": "rhenopyrgus", "depth": null, "synonymy": false, "path": "0/children/1/children/0/children/0/children/0/children/0"}

> Rhenopyrgus (genus) as placed by Grigo (2000): systematic contents of that source only
> 
> Grigo 2000, p. 95
>   Genus Rhenopyrgus
>     Type species. Rhenopyrgus coronaeformis
>     Rhenopyrgus coronaeformis
>     Rhenopyrgus sp. nov.

### q011 (answerable)

Q: What is the holotype specimen number for Rhenopyrgus grayae, per Ewin et al. (2020)?

- note: text beside the submission: This asks for the holotype specimen number recorded under a species by a source 
- judge contract 2: Header names taxon, basionym inclusion, source authority, and record scope only; no verdict or summary; no question needed for answerable case.

Plan: {"header": "Holotype of Rhenopyrgus grayae (= grayae Bather, 1915) as given by Ewin et al. 2020; material statements only", "blocks": [{"tool": "statements", "parameters": {"record": "grayae_bather_1915", "source": "2020_ewin_martin.m_isotalo_zamora", "kind": "material"}}]}
Header: Holotype of Rhenopyrgus grayae (= grayae Bather, 1915) as given by Ewin et al. 2020; material statements only
- list {"record": "grayae_bather_1915", "source": "2020_ewin_martin.m_isotalo_zamora", "kind": "material", "act_kind": null}

> Holotype of Rhenopyrgus grayae (= grayae Bather, 1915) as given by Ewin et al. 2020; material statements only
> 
> Statements about Pyrgocystis grayae Bather 1915
>   2020  Ewin et al.  Rhenopyrgus grayae: occurrence lady-burn-starfish-bed: Katian; Upper Ordovician; Farden Member, South Threave Formation, Drummuck Group; Lady Burn Starfish Bed, part of the Craighead inlier., Lady Burn, near Girvan, Scotland, UK; Ardmillan
>   2020  Ewin et al.  Rhenopyrgus grayae: holotype: NHMUK E 23470
>   2020  Ewin et al.  Rhenopyrgus grayae: specimens: NHMUK E 23674, 29570

### q021 (as-published)

Q: What exact suborder heading do Ewin et al. (2020) print above family Rhenopyrgidae, and at what rank was that name first established?

- failure: no composed block is printed_forms {"record": "edrioblastoidina", "source": "2020_ewin_martin.m_isotalo_zamora"}
- failure: no composed block is history {"record": "edrioblastoidina"}
- failure: the answer does not show "Suborder Edrioblastoidina Fay, 1962"
- failure: the answer does not show "class 1962–1982"
- judge contract 1: Parameters and year range stated without verdict, but Rhenopyrginae is a subfamily-rank variant, not "suborder-rank" — one mislabelled parameter.

Plan: {"header": "Rhenopyrgidae (family) and its suborder-rank variant Rhenopyrginae; Ewin et al. 2020's classification of the family's placement shown via its ancestor chain, and the full history of the suborder name across all sources to establish its original rank; all years", "blocks": [{"tool": "ancestors", "parameters": {"records": ["rhenopyrgidae"], "trees": ["taxonomy"], "years": [2020, 2020]}}, {"tool": "history", "parameters": {"record": "rhenopyrginae"}}]}
Header: Rhenopyrgidae (family) and its suborder-rank variant Rhenopyrginae; Ewin et al. 2020's classification of the family's placement shown via its ancestor chain, and the full history of the suborder name across all sources to establish its original rank; all years
- chains {"records": ["rhenopyrgidae"], "include_variants": true, "trees": ["taxonomy"], "years": [2020, 2020]}
- timeline {"record": "rhenopyrginae", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae (family) and its suborder-rank variant Rhenopyrginae; Ewin et al. 2020's classification of the family's placement shown via its ancestor chain, and the full history of the suborder name across all sources to establish its original rank; all years
> 
> Above Rhenopyrgidae Holloway & Jell 1983: 1 paper, 1 co-author set, 2020
> 
> 2020  Ewin et al.  Echinodermata › Edrioasteroidea › Edrioasterida › Edrioblastoidina › Rhenopyrgidae
> 
> Rhenopyrginae Holloway & Jell 1983: 7 papers, 7 co-author sets, 1983–2020
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

### q026 (as-published)

Q: What two different words does Fay (1962) use for the same specimen, No. 752, in Astrocystites ottawaensis?

- failure: no composed block is statements {"record": "ottawaensis_whiteaves_1897", "source": "1962_fay", "kind": "material"}
- failure: the answer does not show "752 [gsc]"
- judge contract 2: Header names only taxon, specimen, source scope, and the Fay 1962 restriction; no verdict, summary, or mechanism wording; no question needed.

Plan: {"header": "Specimen No. 752 cited under Astrocystites ottawaensis: citation history across sources, isolating Fay 1962's usage", "blocks": [{"tool": "specimen_history", "parameters": {"number": "752"}}]}
Header: Specimen No. 752 cited under Astrocystites ottawaensis: citation history across sources, isolating Fay 1962's usage
- statement {"number": "752", "repository": null}

> Specimen No. 752 cited under Astrocystites ottawaensis: citation history across sources, isolating Fay 1962's usage
> 
> No source in the corpus mentions the specimen 752.

### q028 (as-published)

Q: What exact heading and parenthetical act does Guensburg & Sprinkle (1994) print for the Rhenopyrgus subfamily?

- failure: no composed block is contents {"source": "1994_guensburg_sprinkle", "record": "rhenopyrginae"}
- judge contract 1: Parameters and scope stated plainly, but the parenthetical "a nomen translatum of Rhenopyrgidae" pre-states the answer rather than merely naming the group.

Plan: {"header": "Rhenopyrgus subfamily (Rhenopyrginae, a nomen translatum of Rhenopyrgidae) as printed by Guensburg & Sprinkle 1994; no synonyms or other ranks beyond this one included; single source", "blocks": [{"tool": "printed_forms", "parameters": {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}}, {"tool": "statements", "parameters": {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle", "kind": "act"}}]}
Header: Rhenopyrgus subfamily (Rhenopyrginae, a nomen translatum of Rhenopyrgidae) as printed by Guensburg & Sprinkle 1994; no synonyms or other ranks beyond this one included; single source
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle"}
- list {"record": "rhenopyrginae", "source": "1994_guensburg_sprinkle", "kind": "act", "act_kind": null}

> Rhenopyrgus subfamily (Rhenopyrginae, a nomen translatum of Rhenopyrgidae) as printed by Guensburg & Sprinkle 1994; no synonyms or other ranks beyond this one included; single source
> 
> Rhenopyrginae (Subfamily)
>   1994 "Subfamily Rhenopyrginae emend. nom. transl." (the heading as entered; no verbatim form is recorded) Guensburg & Sprinkle 1994
> 
> Statements about Rhenopyrginae Holloway & Jell 1983
>   1994  Guensburg & Sprinkle  emended
>   1994  Guensburg & Sprinkle  nomen translatum from Rhenopyrgidae

### q034 (trajectory)

Q: Who does the corpus credit as the author of Cambraster, and does every source agree?

- failure: no composed block is printed_forms {"record": "cambraster"}
- failure: the answer does not show "Cabibel, Termier, and Termier, 1958"
- judge contract 2: Lists only group, synonym/variant scope, tree type, and year range in neutral taxonomic language; no summary, mechanism, or verdict; omitted question acceptable.

Plan: {"header": "Cambraster (genus); authorship as credited across sources; no synonyms or variants beyond the primary record; classifications only; all years", "blocks": [{"tool": "history", "parameters": {"record": "cambraster"}}]}
Header: Cambraster (genus); authorship as credited across sources; no synonyms or variants beyond the primary record; classifications only; all years
- timeline {"record": "cambraster", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Cambraster (genus); authorship as credited across sources; no synonyms or variants beyond the primary record; classifications only; all years
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

- note: text beside the submission: The corpus does not contain this paper.
- judge contract 1: Header is scope-only but pre-states the finding (source absent from corpus), i.e. a summary verdict; no spurious question asked.

Plan: {"header": "No plan built: the source \"Klug et al. 2008\" is not present in the corpus", "blocks": [{"tool": "gap", "parameters": {"source": "Klug et al. 2008", "kind": "newTaxa"}}]}
Header: No plan built: the source "Klug et al. 2008" is not present in the corpus
- statement {"source": "Klug et al. 2008", "kind": "newTaxa"}

> No plan built: the source "Klug et al. 2008" is not present in the corpus
> 
> No source in the corpus mentions the source Klug et al. 2008.

### q039 (absent)

Q: Which sources place the genus Rhenoblastus, and where?

- note: text beside the submission: No source in the corpus carries the name "Rhenoblastus" at any rank, so there is
- judge contract 1: Header states no parameters and instead delivers the finding of absence — a summary/verdict rather than scope; otherwise brief, no question needed.

Plan: {"header": "Rhenoblastus is not a name carried by any source in the corpus; reporting the gap.", "blocks": [{"tool": "gap", "parameters": {"name": "Rhenoblastus"}}]}
Header: Rhenoblastus is not a name carried by any source in the corpus; reporting the gap.
- statement {"name": "Rhenoblastus"}

> Rhenoblastus is not a name carried by any source in the corpus; reporting the gap.
> 
> No source in the corpus mentions the name Rhenoblastus.

### q045 (trajectory)

Q: Who proposed placing rhenopyrgids inside Cyathocystidae, who followed, and who rejected it?

- failure: no composed block is placed_under {"record": "rhenopyrgidae", "parent": "cyathocystidae"}
- failure: the answer does not show "first Guensburg & Sprinkle 1994"
- judge contract 2: States group, rank-variant inclusion, year range, and source type only; no verdict, summary, or mechanism language; no question needed.

Plan: {"header": "Rhenopyrgidae (including its subfamily-rank variant Rhenopyrginae) placement under Cyathocystidae; all years, taxonomic classifications", "blocks": [{"tool": "history", "parameters": {"record": "rhenopyrgidae", "include_related": true}}]}
Header: Rhenopyrgidae (including its subfamily-rank variant Rhenopyrginae) placement under Cyathocystidae; all years, taxonomic classifications
- timeline {"record": "rhenopyrgidae", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> Rhenopyrgidae (including its subfamily-rank variant Rhenopyrginae) placement under Cyathocystidae; all years, taxonomic classifications
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
- judge contract 2: Header names only the specimen, scope, ordering and columns; no verdict, count or mechanism wording. No question needed since parameters are unambiguous.

Plan: {"header": "\"Kalckballar\" taken as the single record named by Tilas (1740); its original statement plus how later authors treated it, traced through all sources in year order; classifications only; all years.", "blocks": [{"tool": "statements", "parameters": {"record": "kalckballar_tilas_1740", "source": "Tilas 1740"}}, {"tool": "history", "parameters": {"record": "kalckballar_tilas_1740"}}]}
Header: "Kalckballar" taken as the single record named by Tilas (1740); its original statement plus how later authors treated it, traced through all sources in year order; classifications only; all years.
- list {"record": "kalckballar_tilas_1740", "source": "1740_tilas", "kind": null, "act_kind": null}
- timeline {"record": "kalckballar_tilas_1740", "include_related": true, "synonymy": false, "trees": ["taxonomy"], "years": null}

> "Kalckballar" taken as the single record named by Tilas (1740); its original statement plus how later authors treated it, traced through all sources in year order; classifications only; all years.
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

### q054 (as-published)

Q: Under what spelling do the papers in the corpus cite Meyer's (1826) genus Echinoencrinites?

- failure: no composed block is history {"record": "echinoencrinites"}
- failure: the answer does not show "Echino-encrinites; named as new"
- failure: the answer does not show "Echino-encrinites, in Cystidea"
- failure: the answer does not show "cited as a synonym of Echino-encrinus"
- judge contract 1: No question needed, no mechanism or judgement language, but the header announces the finding (gap) rather than merely stating scope parameters — one summary lapse.

Plan: {"header": "Echinoencrinites Meyer, 1826 (genus), including its alternate spelling Echino-encrinites; printed forms across all sources; all years", "blocks": [{"tool": "printed_forms", "parameters": {"record": "echinoencrinites"}}, {"tool": "printed_forms", "parameters": {"record": "echino-encrinites"}}]}
Header: Echinoencrinites Meyer, 1826 (genus), including its alternate spelling Echino-encrinites; printed forms across all sources; all years
- list {"record": "echinoencrinites", "source": null}
- list {"record": "echino-encrinites", "source": null}

> Echinoencrinites Meyer, 1826 (genus), including its alternate spelling Echino-encrinites; printed forms across all sources; all years
> 
> Echinoencrinites (genus)
> 
> Echino-encrinites (genus)
>   1847 "['von Meyer'] 1826 ['Karstner']" Hall 1847

### q056 (uncaptured)

Q: What classification does Vanuxem (1842) print for the fossils of New York's third district?

- failure: nothing composed: the submission names no block that could be shown
- failure: no composed block is gap {"source": "1842_vanuxem", "kind": "skeleton"}
- failure: the answer does not show "has not yet been entered (only part of it is entered so far)"
- judge contract 2: Header names only the work, taxon, and synonymy scope; no summary, mechanism, or verdict; no unnecessary clarifying question.

Plan: {"header": "Classification of Echinodermata as printed by Vanuxem (1842); full hierarchy below Echinodermata; taxonomic trees only; no year restriction", "blocks": [{"tool": "contents", "parameters": {"source": "Vanuxem 1842", "record": "Echinodermata"}}]}
Plan errors: [{"block": 1, "tool": "contents", "parameters": {"source": "Vanuxem 1842", "record": "Echinodermata"}, "error": "returned no block; the corpus holds nothing for these parameters"}]
Header: Classification of Echinodermata as printed by Vanuxem (1842); full hierarchy below Echinodermata; taxonomic trees only; no year restriction

> 

### q058 (absent)

Q: How does Breyn (1732) arrange the echinoids in his Schediasma?

- note: text beside the submission: The corpus does not contain this source.
- judge contract 2: Header states only corpus coverage (Breyn 1732 absent as a source), no verdict or mechanism; no question needed since no parameter is ambiguous.

Plan: {"header": "Gap: Breyn (1732) is not a source in this corpus", "blocks": [{"tool": "gap", "parameters": {"source": "Breyn 1732", "kind": "skeleton"}}]}
Header: Gap: Breyn (1732) is not a source in this corpus
- statement {"source": "Breyn 1732", "kind": "skeleton"}

> Gap: Breyn (1732) is not a source in this corpus
> 
> No source in the corpus mentions the source Breyn 1732.

### q055 (uncaptured)

Q: What does the Vermes part of Gmelin's thirteenth edition of the Systema Naturae (1791, part 6) place under Echinus?

- failure: no composition (the model answered in prose or not at all)
- judge contract 2: Header names only the source, taxon, and what is listed (genera, species, type genus) as printed; no verdict or summary; no question needed.

Header: 

> 

