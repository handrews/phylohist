# Phylohist Data Entry Formats

Data in Phylohist is managed as a set of YAML files that are intended to
be easy for humans to understand and use.  Or at least easier than editing
SQL or other database statements.

There are several files that more-or-less correspond to tables, with the
exception of having one tree file per publication as the original single
tree file became unwieldy.  Data in each file is related to other files
by way of human-readable keys that are constructed from the data as a basic
data integrity check.  Each key is verified to match its contents within
the file during data load.

Please note that this system grew organically.

## Files

See the schemas for the exact set of fields or object structures that
are used in each file.  This section describes the purpose of each file,
and how its keys are constructed and validated.

### The Authors file

`authors.yaml` is one of the simplest files, recording the surname,
given name(s) or initial(s), and optionally birth and death years of each
author whose identity is known.  The key for each author consists of the
lowercased surname (without any change to spaces, hyphens, diacritics, etc.)
and optionally dot-separated lower-cased given name initial(s).  The validation
does not care which form is used, and there is currently no way to force
one or the other.

Ideally, if multiple authors share last names, all of their keys use initials,
although this is notably not the case with `billings` (Elkanah Billings) vs
`billings.w.r` (Walter R. Billings, who is less well-known).  This may be
fixed and enforced in the future.

Chinese surnames are sufficiently common that initials are always included,
based on the older orthography, e.x. Zhao Yuan-Long, often written in papers
as Zhao Y.-L., producing a key of `zhao.y.l`, rather than Zhao Yuanlong
producing `zhao.y`.  An exception is Shu Degan as `shu.d` as he has made
a point of using a single initial consistently, and is particularly well-known.

Birth and death years, when available, are used in a rough check of whether
an author credit for a source is feasible, although there is padding for
posthumous work that should really be handled by an exceptions table.

See "The Authority block" below for how authors are managed, including
when the identity of an author is unclear (e.g. multiple "Clark"s have
been active in the early-mid 1900s but are not always cited clearly).

### The Publications file

`publications.yaml` was originally intended to record enough data about
a publication to print a full citation in any standard format.  In practice,
it mostly just records the publication name and provides a way to connect
publications from the same periodical or book.

There is no enforced convention for the keys in this file, and the only
field used by the code is `name`, although `editors` is validated against
`authors.yaml`.

Issue #131 was filed to track work to use the additional fields to produce
more comprehensive citations.

### The Sources file

`sources.yaml` tracks all of the publications referenced in the system.

An entry here does not necessarily mean there is or will be a tree file.
Some multi-part works have all parts added for completeness, but not all
parts publish trees.  In others, some parts are outside of the current focus
of the project but are used in authority citations when taxa they established
are referenced elsewhere.  A few very old sources are present to note fossils
initially considered to be mineral deposits.

The file is sorted by key (in theory) and the keys are underscore-separated
strings consisting of the publication year, optionally including a trailing
lowercase disambiguation letter, and then the author key of each author in
the order they are listed.  The year (but not the letter, if present) is
validated against `pubDate` and the authors against `authors`.

Disambiguation letters are only used in the keys, and are a best guess as
to which source was formally published first unless all involved sources
have clear enough dates to put them in order.

### The Taxa file

`taxa.yaml` exists to establish which taxa in various trees are truly
identical, and not just equated in some way.  Exactly what this meant
was originally somewhat vague, but for more recent entries it captures
the original nomenclatural act creating the taxon, which is validated
against the relevant tree node.  Currently, `taxa.yaml` entries with
a `pages` field are validated according to this relatively new rule.

Older entries may include some assumptions such as picking one of several
ranks associated with the name.  Higher ranks for entries without `pages`
should be considered somewhat suspect.


## Tree nodes, authority, and related structures

The fundamental structure for capturing information from a source is the
tree node.  In the most basic form, these have a parent-child relationship
with ordered children, capturing the rank used in the publication (which might
be different from the original rank captured in `taxa.yaml`).  With just that
information, Linnaeus 1758 to the Class level of the animal kingdom looks like:

```yaml
taxon: animalia
rank: Kingdom
children:
- taxon: mamallia
  rank: Class
- taxon: aves
  rank: Class
- taxon: amphibia
  rank: Class
- taxon: pisces
  rank: Class
- taxon: insecta
  rank: Class
- taxon: vermes
  rank: Class
```

These are considered to be _primary_ tree nodes, in the sense that there
is no tree without them.

The rank can be set to the special YAML value `null` when no rank is given,
which is distinct from an explicit pseudo-rank of "Unranked".

### Tree nodes and binomials

The defining feature of Linnaean taxonomy that has been carried forward into
all subsequent systems is binomial nomenclature, in which specimens are
identified by both a genus and species.  Binomials are the most common form,
but all ranks lower than genus (e.g. subgenus, subspecies, variety) are always
shown in the context of a genus, with their own typographic conventions.

Phylohist's internal system _does not_ do this.  It treats all ranks the same,
and disambiguates names below the genus level by appending additional
information to the key.  This allows the system to track recombinations
the same way it tracks any other movement
to them.  


However, many other relationships are expressed
via tree nodes, such as synonymy or translation (re-ranking).

The exact semantics of a tree node are context-sensitive.

### The Authority block




### Equating taxa across ranks, languages, and spellings

In theory, all nomenclatural statements equating taxa (_nomen transl._,
_nomen subst.,_ _nomen correct._, etc.) would be handled in the tree files.
In practice the relevant source might not be known or might not yet have
a tree file.  In older works, there might not be a formal statement, making
it hard to tell whether a given publication is where the change first occurred.

Older works are also often casual about Latin vs vulgar spellings for higher
ranks, and changed those ranks without fanfare.  Linnaeus only defined Class
and Order, so the concepts of Family and Phylum developed over time.  Family
in particular was used in a casual sense before it was formalized, and Phylum
was one of several approachs to a rank between Kingdom and Class.


With alternate ranks and Latin vs vulgar spellings, older works again 

tracked things like alter
