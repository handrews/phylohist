I want to re-think materials a bit more broadly, and focus more on how parts of them are similar to taxa.

# Specimen identifiers

I want to re-think how we are handing material identifiers to make sure we are not over-complicating it.

The primary goal of tracking specimen identifiers and repositories are to:

* Know when two specimens are held by the same institution
    * Institutions can change names or be merged or reorganized, so the "when" matters
    * 
* Know which part of the identifier is controlled by the institution (and therefore at least theoretically stable across publications) and which is publication-specific (which may or may not be a common enough convention to be the same or similar across publications)

The most common publication-controlled portion is what we now call the "prefix", which is most often used to indicate the repository.  However, some things that look like repository prefixes ("Yjh" in the papers we've been referencing as a case study) actually serve another purpose.

"Yjh" in particular is ambiguous as to whether the 2007 paper used it to originally reference the horizon (Yanjiahe Formation), the locality (Yanjiahe, Yiching, China), or just existed to group the new specimens described in the initial paper to make it clear that they were not pre-existing specimens.  In the next paper, it was said (along with another part of the identifier) to indicate the locality, but exactly how that correlated was never entirely clear.  What _is_ clear is that it is not a repository prefix, as it is used for specimens in multiple repositories.  So we could safely designate "Yjh" as a hyphen-separated prefix of unknown semantics.

This breaks the current system, which wants prefixes to _mean_ something.  But they don't have inherent meaning, as seen by different publications using the same prefixes for different institutions.  The institutions have names, and the prefixes  are each individual publication's shorthand, which happen to align because authors tend to make acronyms of things the same way.

* No one should be globally searching on prefixes, as the meaning is not stable.
* Searching on repositories should not be tied to prefixes, at least not as a formal entity.

So I think we don't actually need to associate prefixes with repositories in `repository.yaml`.  They are associated per-paper.  The only purpose in having them inside `repository.yaml` is a referential integrity check.

Invert prefix block?  Show repositories mapping to prefixes, record IDs as written, record repository, and let code figure out the prefix splicing if any.

The `sameAs` problem: We don't want a full database of specimens, at least right now.  That feels like a pain in YAML, and is one where a real DB with automatic ids would be more suitable.

# Horizons

In modern publications, stratigraphic units have a formal hierarchy, like modern (but pre-cladistic) taxon ranks.  Like taxon ranks, historical usage was much more vague, sometimes looking like modern usage and sometimes not.  But often, stratigraphic units can be correlated even if their assigned position in the hierarchy is not consistent, just as taxa can be correlated even when the rank is changed.  Stratigraphic units are slightly more messy than taxa, as fewer aspects are standardized, and there are no equivalents of nomenclatural acts such as `nomen transl.`

# Localities

Locality prefixes are a bit weird?  Two different "prefixes" (really just institution names) for the same number in Sprinkle 1973?

```yaml
localityNumbers:
- prefix: USGS locality
  number: 55e
- prefix: USNM locality
  number: 55e
 ```

Also with
```yaml
localityNumbers:
- number: IK-2
```
This seems to be why `sprinkle-l` is in the root `localityRegister` as it allows lack of prefix?

----

Localities are a bit different.  Some aspects are relatively standardized (countries, governmental subdivisions, town names, etc., although there is considerable variation across different countries).  Then there are formal map grids and coordinate systems, as well as the concept of named sections.  Any system still also has to handle vague descriptive phrases as well.  But the formal pieces are, by definition, formal, and can be tracked.

