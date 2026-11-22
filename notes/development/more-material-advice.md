# From Gemini

You have hit on one of the biggest headaches in paleontological informatics. When researchers publish specimens before formal museum cataloging—or when research labs reorganize—field numbers, locality codes, and institutional prefixes get mashed together in ways that break strict hierarchical parsing.
To solve this, modern biodiversity databases separate the physical specimen from the strings of text used to refer to it.

How to Model This in Your Database

Instead of trying to force a single identifier string to cleanly map to Institution + Collection + Specimen, treat identifiers as a one-to-many relationship attached to a core physical specimen record.
• Create an Internal Master Specimen ID. Assign your own stable, meaningless primary key (e.g., SPEC_0001) to the actual physical fossil. This ensures you never have to change your core record when new papers rename the specimen.
• Use an "Identifiers / Aliases" Table. Create a separate table linked to your Master Specimen ID. Each row stores a published string (Yjh-HS18, ELI-HS18), the specific publication it came from, and an Identifier Type (e.g., Field Number, Informal Lab ID, Formal Catalog Number).
• Track Institutional Hierarchy Separately. Do not rely on the prefix of a specimen ID to tell you where the fossil lives. Create a Repositories table with a parent-child relationship. In your example, Early Life Institute (ELI) is a research unit nested inside the Department of Geology / Geosciences, which is inside Northwest University, Xi'an.
• Decouple Localities and Horizons. Give localities and stratigraphic units their own tables. Link SPEC_0001 to the Yanjiahe Formation (horizon) and the specific outcrop (locality), regardless of whether the specimen's label mentions them.

Decoding the Specific Example (Yjh-HS18 vs. ELI-HS18)

In Chinese early Cambrian paleontology (specifically at Northwest University, Xi'an, famous for Chengjiang and Kuanchuanpu/Yanjiahe small shelly fossils), research groups frequently use composite field-locality codes that slowly morph into catalog numbers over time.
Here is how those pieces almost certainly break down:

Component	Likely Meaning	Why It Shifted Across Papers
Yjh	Yanjiahe (Formation or Village/Section)	Used initially as a project or stratigraphic prefix while the material was being worked on in the lab.
ELI	Early Life Institute	Replaced Yjh in the third paper to standardize the specimen as a formal institutional holding of the ELI (which is housed within NWU's Department of Geology).
HS	Outcrop, Section, or Collector/Horizon Code	Often stands for a specific measured section, hill/village name (e.g., Huoshaodian or similar local site), or a bed/horizon code. Because it ties the fossil to its exact spot in the rock, it was kept as part of the base specimen number when ELI was added.
18	Sequential Specimen Number	The 18th specimen (or rock slab/sample) collected or numbered from the HS site/horizon.


Practical Tips for Ambiguous Prefixes

When you cannot prove what a sub-string like HS means without emailing the authors, handle it cleanly in your schema:
• Store the "Verbatim String" alongside "Parsed Notes". Always keep the exact published string (Yjh-HS18) untouched for searchability. Add a free-text Identifier_Notes field where you can record hypotheses (e.g., "Yjh likely Yanjiahe Fm; HS noted as locality in Paper 2").
• Map to Darwin Core's Triplet Concept Loosely. In Darwin Core, the classic identifier is the "Darwin Core Triplet" (institutionCode:collectionCode:catalogNumber). For messy literature data like yours, map the formal institutional code (ELI) to institutionCode, put the messy hybrid (HS18) in catalogNumber, and dump all older aliases (Yjh-HS18) into otherCatalogNumbers (which accepts a pipe-separated list like Yjh-HS18 | Field-04).
• Differentiate "Sample/Slab" from "Specimen". In microfossil and small shelly fossil papers (common in the Yanjiahe Formation), HS18 might actually be a rock sample or acid-maceration residue number, while individual fossils from that rock might later get sub-numbers (like ELI-HS18-01). Building a parent-child link between Bulk Samples and Individual Specimens will save you huge headaches later.
If you are actively designing this database schema, would you like help with:
• Relational table structures (e.g., SQL/table layouts for linking localities, horizons, and multi-part identifiers)
• Handling rock slabs vs. individual fossils (e.g., modeling multiple taxa found on a single numbered piece of rock)
• Specific literature conventions (e.g., decoding other regional or taxonomic numbering quirks you are encountering)

