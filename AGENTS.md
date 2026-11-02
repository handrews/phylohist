# For agents

`phylohist` records published taxonomic opinions on Palaeozoic echinoderms
source by source, exactly as printed: who published what systematic
information in which paper, with the page, plate and figure numbers that
locate it. `data/` is the curated corpus, `claims/` the table generated from
it that the tools read, and `docs/claims.md` the vocabulary both are written
in. `README.md` is the overview. This file says how to answer from the
corpus and how to change it.

## Answering a question: use the tools

The tools read `claims/` and return blocks with a rendered form; a grep over
the files reproduces none of that. The CLI has one subcommand per tool:

    poetry run phylohist tools
    poetry run phylohist resolve "Rhenopyrgus"
    poetry run phylohist history rhenopyrgus --style markdown
    poetry run phylohist plan my-plan.yaml

The same tools are served over MCP by `scripts/mcp_server.py`, which
`.mcp.json` registers for Claude Code. The `plan` tool takes the blocks an
answer is made of and returns the rendered answer. `eval/planner-prompt.md`
is the full statement of how a model plans one; its rules in short:

- Resolve a printed name first. A name can resolve to several records: the
  same name at other ranks, a spelling variant, a placeholder such as "order
  uncertain". Decide which records the question is about.
- Nothing from outside the corpus enters an answer. Do not supply a name, a
  date, a placement, a specimen number or a page the tools did not return,
  and do not correct the corpus from memory.
- A name that resolves to nothing means no source in the corpus carries it.
  That is a fact about the corpus; the literature may hold more.
- Each source declares, per kind of statement, whether all, part or none of
  what the paper prints has been entered. What the corpus does not hold is
  stated with the `gap` tool, after checking that declared coverage; a source
  on record with nothing entered is a gap too.
- The blocks carry their own citations and measurements. Reproduce their
  rendered text and add no summary and no verdict.

## If all you have is a text index

An index built by `xerj autoindex` (the Corpus Hub prompt for this
repository runs one), or any grep, sees files. Read them like this:

| path | holds | read it as |
|---|---|---|
| `data/trees/<source>.yaml` | one file per paper: each classification as printed, in printed order | the source's own statements; a `taxon` key is a record in `data/taxa.yaml` |
| `claims/<source>.jsonl` | one claim per line, with `source`, `subject`, `kind`, `pages`, `printedAttribution`, `audit`, `notes` | one statement a source prints about one name; the fields are defined in `docs/claims.md`, "The record" |
| `claims/names.json` | one row per taxon record: name, rank, authority, the folded lookup forms | the way from a printed name to a record key |
| `claims/manifest.json` | one row per source: its `citation` and its `coverage` per kind (`all`, `partly`, `none`, `na`) | how a gap is told from an absence |

Cite a source as its `citation` reads ("Holloway & Jell 1983") and give the
page the claim carries. Before saying the corpus lacks something, check the
source's coverage for that kind: `none` or `partly` is a gap in the data,
and only a source with coverage `all` and no claim is an absence.

Four directories are not the corpus, and `.xerjignore` keeps them out of
the index: `drafts/` (AI-drafted trees awaiting a human audit), `notes/`
(the development record: reviews, audits, paper notes and translations,
none of it checked against the project's published goals), `eval/runs/`
(model transcripts) and `tests/corpus/` (a frozen slice of `data/` for the
tests). An answer cites a source and a page, never a note or a review.

## Changing code or data

The checks are in `README.md` under "Checks": `ruff check`, `ruff format
--check`, `pytest` with its coverage floor, `poetry run regenerate` after
any edit under `data/` or `schemas/`, and `git diff --exit-code` on
`scripts/schema-usage.md`, `claims/` and `tests/expected-warnings.txt`,
which CI fails on when stale. A draft is checked with
`scripts/check_draft.py drafts/<file>.yaml`.

- The tests run over `tests/corpus/`, a frozen slice; only tests marked
  `production` load `data/`. Improving the data cannot break a test of the
  code, and the slice is edited only to add the case a test needs.
- A new loader check that fires on committed data logs an error, and the
  data is fixed.
- The tree files keep printed order and claim ids depend on it, so
  reordering a tree is a data change.
- The data records what a paper prints: names and acts, placements, usages
  and synonymies, material with its context, and the locators. Diagnoses,
  descriptions and the paper's argument are not recorded; a reader follows
  the citation to the paper.

## Where things are

| directory | holds |
|---|---|
| `data/` | the curated corpus: the record files (`taxa.yaml`, `sources.yaml`, `authors.yaml`, ...) and one tree file per source under `trees/` |
| `claims/` | the generated claim table with `names.json` and `manifest.json`; committed, and CI fails when stale |
| `docs/` | the claims vocabulary, the tools and answer shapes, the walkthrough |
| `eval/` | the questions, the prompts, the findings, the run transcripts |
| `drafts/` | AI-drafted trees awaiting audit; the loader reads them only on request |
| `notes/` | the development record; nothing in it is needed to use phylohist |
