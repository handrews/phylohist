# Material identifiers, registers and holders: review and proposal

Written 2026-11-14, while splitting `context` into `horizon` and `locality`.
The split is done; everything else here is a proposal set aside to come back
to. Nothing below the first section is implemented.

The question that started it: how to record the Yanjiahella specimens, which
Guo et al. print as `Yjh-HS18` (2008, 2012) and Topper et al. as `ELI-HS18`
(2019). The papers are in `example-publications/11-14`; what they print is in
the last section.

## What the review of the present model found

| today | finding | proposed change | state |
|---|---|---|---|
| `context` holds stratigraphy and geography in one record | Sprinkle 1973 has 88 contexts made of 51 distinct horizons and 81 distinct localities; 18 horizons recur across localities, 2 localities carry two horizons | split into `horizon` and `locality` records | done |
| a context's bare `inferred` object | the one use (Rievers 1961) had no basis recorded | the `editorial` block, values in the record's own fields | done |
| `context: {key, tentative}` on an entry | unused in `data/` | `tentative: [horizon, locality]` on the entry | done |
| `prefix` + per-file `prefixes` map; display is always `<prefix> <number>` | a prefix can only mean "a register"; `Yjh-HS18` cannot be displayed or looked up as printed; a site code inside a number is invisible | per-file `formats`, each a template | open |
| entry `repository` is both "where it is held" and "which register the number is in", reconciled by the `within`-chain rule in `claims._numbers_register` | no entry in `data/` uses it as an override: 2 entries carry `prefix` and `repository`, both the Walcott Collection, both inside the chain. The rule exists only to undo the conflation | `repository` is the holder the source states and never touches the key; the register comes from the format alone; the rule is deleted | open |
| registry `type: collection` covers named collections (Walcott, Springer, Caster) and numbering series (NHMUK E register, USGS locality register); `sprinkle-l` is `type: person` | the registry lists two kinds of thing, holders and registers, without saying which | add `type: register`; retype the 13 series entries | open |
| registry `prefixes` | they are printed forms, and with templates no longer prefixes | rename `forms`, each a prefix or a template | open |
| file `localityRegister`, and `register` on a locality number | two more ways to name a register, both expressible as a format | remove | open |
| `parts` parallel to `numbers`, letters inside the number string | 6 entries, all in Sprinkle 1973, all part and counterpart. Sprinkle prints "MCZ 581" and the entry keys only `mcz:581a` and `mcz:581b`, so `specimen_history` for MCZ 581 finds nothing | a number may carry `suffix` and `part`; a suffixed number also keys without the suffix | open |
| `formerIds`: strings "never split" | unused in `data/`; a former number that joins nothing defeats its purpose | items become `{format, number}` and give join keys | open |
| `localityKeys` | no tool reads them | keep: they are a locality's only identity across sources. A locality lookup tool would be their reader | open |
| `sameAs` | unused in `data/` (tests only) | keep | |

Counts are from `data/trees/` at `8d7d0ae`: 315 material entries, 160 of them
with a context, 3 with numbers and no prefix (Fay 1962, `repository: gsc`;
Sprinkle 1973, `holder: A. R. Palmer`; Sprinkle 1973, `KR-2` with
`repository: u-cincinnati-caster`).

Not proposed: splitting the registry into two files (most entries are a
holder and a register at once), renaming it, renaming the `repository`
parameter of `specimen_history`, or a global registry of localities.

## The proposal for identifiers

### Formats

A tree file declares the ways it prints an identifier, in place of `prefixes`:

```yaml
formats:
  MCZ: mcz                               # short form: template 'MCZ {number}'
  USGS locality: usgs-l                  # 'USGS locality {number}', as Sprinkle prints it
  field: {template: '{number}', register: sprinkle-l}
  Yjh-HS:
    template: 'Yjh-HS{number}{suffix}'
    register: nwu-eli
    key: 'HS{number}'
    locality: gunziao
    notes: '"Collection numbers Yjh-HS means the locality of the fossils from Yanjiahe village." (p. 793)'
```

- `template`: literal text with `{number}` and optionally `{suffix}`
  (appended after the number when the template does not place it). The
  displayed `ids` are the template filled in.
- `register`: the registry entry whose number this is. A format with none
  gives no join key (a private holder's numbers).
- `key`: the register's own number. Topper et al. 2019 would declare
  `ELI-HS{number}` with the same `key`, and both sources give
  `nwu-eli:hs18`.
- `locality`: a key of the file's `localities`, when the source says the
  format stands for a place (2012 on `Yjh-HS`; `EJ` and `JS` in the Yujingia
  paper's `ELI-EJ053`, `ELI-JS188A`).

An entry has `format:` where it has `prefix:`; a locality number is
`{format, number}`; `entryRef` and `sameAs` take `format`.

This came after a first version with an ordered list of codes per entry
(`codes: [Yjh, HS]`), each code declared with a register, a context and a
separator. Henry's suggestion of a template "like a Python f-string" replaced
the separators, and declaring the meaning per format replaced the rules that
version needed for which code names the register and which codes belong to
the number. Regular expressions with capture groups were considered and left
as more than is needed now.

**Henry's comment on `key`:** it should default to being the same as the
template, since a changing prefix is unusual. Open under that default: join
keys today are `<register>:<number>`, and with the whole printed form as the
key, two sources printing `E 23470` and `NHMUK E 23470` for one register stop
joining unless one of them states a `key`. Whether the default should be the
template, or the template is the right default only for formats whose literal
text is part of the catalogue number (`HS`), is what needs thinking through.

**Sprinkle 1973.** Under templates `USGS locality` is the printed form and
needs no apology. The field codes (`CL-1`, `SH-1`) become a format with
template `{number}`, which is what lets `localityRegister` go. Splitting off
the two-letter place code is possible (a format per code) and was left alone:
Appendix 1 has not been read for what the codes are.

### Numbers with a suffix

```yaml
- format: MCZ
  numbers: [{number: 581, suffix: A, part: part}, {number: 581, suffix: B, part: counterpart}]
```

`joinKeys` stay one per number, in order (`mcz:581a`), which the run index in
`store._index_specimen` depends on; a second field (`wholeKeys`) adds the key
without the suffix (`mcz:581`) and the store indexes both. Plain strings such
as `1010a` stay whole. In the Yanjiahella papers this is what joins 2012's
`Yjh-HS84A` and `Yjh-HS84B` to 2019's `ELI-HS84`.

### Lookup

`_typed_prefix`, `_strip_form` and the separator rules in `phylohist/store.py`
become one matcher over templates: the registry's `forms` (a bare prefix `P`
reads as `P {number}`) and the templates the sources declare, written into
`phylohist/table/repositories.json` by `scripts/claims.py`. Literal text
matches without regard to case; a run of spaces, hyphens or periods matches
any such run or none; `{number}` takes the rest; the longest literal wins and
two registers claiming it is the ambiguous result, as now. The loader's
"prefix is not a known form of its register" warning would go, since the
registry would no longer have to repeat what the sources declare.

### Registers and holders

An entry's register comes from its format. `repository` is then free to mean
only what the source says about where the specimen is: the Department of
Geology in 2008, the Early Life Institute from 2012, the Walcott Collection
for a USNM number. This replaces an earlier idea of a separate `heldAt`
field. Checks it allows, all errors: a format's register numbers the right
subject (specimens or localities); a stated `repository` is not a
`type: register` entry; a format's `locality` exists.

### Order of work, when taken up

1. Formats, registers and holders: schema, loader (`file_prefixes`,
   `number_entries`, `locality_objects`, `_prefixes_used`, `entry_identifies`,
   `same_as_matches`), claims (one helper from an entry's format and number
   to display, register and keys, replacing `_numbers_register` and
   `_numbers_fields`), migration of `prefixes`/`prefix`, the 3 unprefixed
   entries, Sprinkle's field codes, the 6 `parts` entries, the registry.
2. Lookup.
3. Tests, docs.

The check for the migration: every `joinKeys` and `localityKeys` value equal
to before; `ids` differing only where a format now prints more (Fay 1962,
"Canadian Geological Survey 752"); `wholeKeys` on exactly the 6 part and
counterpart entries.

## What the Yanjiahella papers print

Read 2026-11-14. Guo et al. 2012 has no text layer and was read from page
images at 300 dpi; the 2008 captions were read from page images too, the
text layer being garbled there. Page numbers are the printed ones.

### Guo et al. 2008, Acta Geologica Sinica 82(6): 1124–1132

- No prefix is explained anywhere, and there is no repository statement in
  the running text. Two captions name two institutions:
  - Fig. 3 (p. 1128, small shelly fossils): "specimens preserved in School of
    Earth Sciences and Resources Management, Chang'an University." All four
    panels are `Yjh-003`.
  - Fig. 5 (p. 1130, macrofossils): "Horizon and locality: Yanjiahe Formation
    of Gunzi'ao, Yanjiahe, Yichang. Specimens preserved in Department of
    Geology, Northwest University."
- Fig. 5 identifiers: `Yjh-HS36`, `Yjh-HS32`, `Yjh-HS31` (*Protoconites
  minor*); `Yjh-HS51`, `Yjh-HS16` (*Vendotaenia* sp.); `Yjh-HS81`
  (?*Yuknessia* sp.); `Yjh-HS24` (?*Konglingiphyton* sp.); `Yjh-HS18` ("a
  probable metazoan", h–j).
- The section is "the Gunzi'ao section of Yanjiahe in Yichang" (p. 1125),
  beds numbered I to V; the macrofossils are from the silty shale of Bed III.
- The PDF lacks text between the end of p. 1128 ("…more closely-spaced and
  distinct wrinkle-like") and the start of p. 1131 ("Guizhou), the Lantian
  biota…"); pp. 1129 and 1130 are figures only. The rest of section 3.2.3
  and the caption of the p. 1129 figure are not in the file.

### Guo et al. 2012, Acta Geologica Sinica 86(4): 791–798

- p. 793: "The material is deposited in ELI, Northwest University, Xi'an,
  China." and "Collection numbers Yjh-HS means the locality of the fossils
  from Yanjiahe village." "ELI" is introduced as "the Early Life Institute
  (ELI)". No identifier is printed with an `ELI` prefix.
- Type status is given only in the Fig. 2 caption (p. 794):
  - *Yanjiahella ancarpa*: `Yjh-HS7A` holotype, `Yjh-HS7B` paratype.
  - *Y. monocarpa*: `Yjh-HS18` holotype; `Yjh-HS84A`, `Yjh-HS84B`,
    `Yjh-HS734A` "general view of the paratype".
  - *Y. biscarpa*: `Yjh-HS722` holotype, `Yjh-HS998A` paratype.
- "Locality and Horizon: Bed III, a silty shale, Yanjiahe Formation, Lower
  Cambrian, Terreneuvian, Gunziao section, Sandouping, Yichang, Hubei
  province." under the genus; "As for the genus." under each species.
- `Yjh-HS18` is the specimen figured in 2008 Fig. 5h–j; the paper does not
  say so. The identifier, the caption wording and the photographs match.

### Topper et al. 2019, Nature Communications 10: 1366

- Methods, p. 7: "The fossil material studied herein is deposited at the
  Early Life Institute of Northwest University, Xi'an (Prefix: ELI)."
  Neither `Yjh` nor `HS` is mentioned.
- p. 2: "Holotype. ELI-HS722 (see Guo et al.14, Fig. 2k)." for *Yanjiahella
  biscarpa*, with *Y. ancarpa* and *Y. monocarpa* in its synonymy, the
  authors acting as First Reviser. "Material. Thirty five specimens."
- Figured: `ELI-HS18` (Fig. 1); `ELI-HS84`, `G21` (part and counterpart),
  `ELI-HS998B`, `ELI-HS999` (Fig. 2). The Fig. 2 caption's panel letters are
  inconsistent, so letters cannot be assigned to specimens from it.
- Headings are "Locality." and "Stratigraphy.".
- The only statement tying a 2019 number to a 2012 one is the holotype's
  citation of Fig. 2k. `ELI-HS18`, `ELI-HS84` and `ELI-HS998B` correspond to
  the 2012 numbers by number alone, and `84` without a letter and `998B`
  against 2012's `998A` are the part and counterpart cases above.

### Topper et al. 2020 (Reply), Nature Communications 11: 1287

- The same deposition sentence. One identifier: `ELI-HS7A` (Fig. 1, latex
  cast, *Y. biscarpa*), which is 2012's holotype of *Y. ancarpa* by number.

### The `yujingia` branch

At `76f3cd9` its data does not load, for three keys: `Yjh: nwu-geo-l` and
`ELI: eli` in two `prefixes` maps name registry keys that do not exist (the
registry there has `nwu`, `nwu-eli`, `nwu-geo`, `nwu-l`), and the 2008 tree
has the author id `xioa.z.z` for `xiao.z.z`. Its 2008 tree puts
`numbers: [HS18]` with `asPrinted: Yjh-HS81` on the ?*Yuknessia* node; the
caption gives `Yjh-HS81` to ?*Yuknessia* and `Yjh-HS18` to the probable
metazoan. The notes on `nwu-eli` point to `mwu-geo` and `mwu-l` for
`nwu-…`. Its `phylohist/table/repositories.json` predates the registry keys.
