# From Gemini

That philosophy makes complete sense, and it highlights one of the biggest structural tensions in biodiversity and paleontological informatics. Most major systems do force a consensus view and struggle as a result, though a few specialized platforms share your exact "publication-first, non-consensus" design.
Because PBDB calculates a single automated "opinion" tree to power its global diversity curves, researchers frequently run into circular errors, lost historical nuance, and buried primary citations. Your YAML-based, assertion-centric architecture actually mirrors the cutting edge of taxonomic and stratigraphic data modeling.
Several notable systems take a similar publication-centric approach—and their experiences highlight the pitfalls of consensus engines:

1. Systems That Prioritize Publication Claims Over Consensus

• TreatmentBank (Plazi). Plazi is arguably the closest philosophical match to your project. Rather than building a single consensus tree, Plazi parses taxonomic literature into individual taxonomic treatments—discrete, citable blocks of text where a specific paper defines a taxon, lists its synonyms, and cites its stratigraphic/geographic occurrences. Every claim stays strictly bound to its source publication, allowing downstream users (and AI pipelines) to weigh conflicting treatments themselves.
• TaxonWorks (Species File Group). Designed explicitly to avoid the "single-tree trap," TaxonWorks models Assertions and Taxon Name Relationships as first-class objects tied to citations. A single taxon name can simultaneously hold multiple conflicting parent placements or stratigraphic assignments from different papers without the database throwing an error or forcing a winner.
• Avibase (Taxonomic Concepts). While focused on modern birds, Avibase pioneered the Taxon Concept model (Name + Author + Year + Reference). Instead of treating Parus major as one consensus bucket, it treats "Parus major sensu Linnaeus 1758" and "Parus major sensu Clements 2023" as distinct, linkable nodes, preserving exact historical meaning across centuries of literature.
• Global Biotic Interactions (GloBI). For ecological and fossil interactions (like predation or trace fossils), GloBI acts purely as an evidence aggregator. It records "Paper A claims Taxon X ate Taxon Y in Formation Z" without attempting to resolve whether Paper A's taxonomy or stratigraphy is currently considered valid.

2. Why Consensus Systems Struggle (Validating Your Design)

Major aggregators like PBDB, GBIF, and Fossilworks struggle specifically because they try to serve two incompatible masters: archiving primary literature and generating clean summary statistics.
• The " Frankenstein" Specimen Problem. When a consensus system updates a taxon's name from a 2020 paper, it often automatically re-labels a 1890s specimen record—even though the 1890s author might have been looking at a completely different species or a misidentified rock layer. Keeping data strictly per-paper prevents this retroactive distortion.
• Stratigraphic Drift. Just like taxonomy, formations get split, renamed, or re-dated. In PBDB, if someone enters a new "opinion" on a Collection's age, the consensus shifts, making it hard to see what the original paper actually claimed versus what a 2015 review paper inferred.
• Lost Provenance in Key-Value Normalization. When databases force messy 18th-century stratigraphy into rigid Formation / Member foreign keys, they have to guess. Once guessed, that guess looks identical to hard data.

3. Why Your YAML + Array Approach Fits This Architecture

Storing publication-centric assertions in flexible YAML files gives you two major advantages over rigid relational schemas:
• Zero Information Loss. Because you aren't forcing a paper's stratigraphic description into a global foreign-key table, you never have to invent consensus where none exists. Your ordered array ([Bed -> Supergroup]) faithfully captures the author's mental model of the rock column at the time of writing.
• AI-Readability and Auditability. Modern LLMs and reasoning pipelines perform much better when given structured, source-attributed claims (like YAML blocks tied to a specific citation) than when fed pre-flattened consensus tables where conflicting evidence has already been averaged out.
Are you linking stratigraphic units across papers using exact string matching or alias/synonym files, or keeping each paper's stratigraphic strings completely self-contained?

-----


Focusing on Paleozoic echinoderms changes the equation in your favor. Paleozoic invertebrate paleontology—especially for crinoids, blastoids, cystoids, and edrioasteroids—has a very specific, well-documented stratigraphic literature. While 19th-century monographs (like Wachsmuth & Springer, Hall, or Miller) are full of "3 miles down the road past the oak tree" descriptions, those classic localities and beds (e.g., the Burlington Limestone, Waldron Shale, LeGrand beds, or Trenton Group) are famous, heavily studied, and relatively finite.
Because your project uses YAML files and avoids rigid database constraints, you do not have to choose between pure free-text and a rigid foreign-key system. You can use a hybrid "soft-linking" pattern that gives you structure where units are known while letting messy, one-off descriptions pass through untouched.

1. The "Soft-Link + Verbatim" Pattern

Instead of forcing every element in your stratigraphic array to be either a strict ID or a raw string, allow an item in the array to be either a plain string or a small keyed reference (or pair a canonical ID with the verbatim text):
• When the unit is completely informal or obscure: Leave it as a plain string in your array (e.g., "crinoid bed 3 miles north of the oak tree"). Your parser/reader treats it purely as descriptive text.
• When the unit is a known Paleozoic classic: Link it to a lightweight entry in a stratigraphy.yaml lookup file (e.g., id: burlington_limestone), while still recording the paper's exact wording (verbatim: "Burlington beds").
This mirrors how TaxonWorks handles messy collecting events: it attaches structured Georeference or Repository objects only when they can be confidently resolved, while preserving the verbatim_locality string on every single record so nothing is ever lost or over-interpreted.

2. Why Paleozoic Echinoderm Literature Rewards "Light" Normalization

In Paleozoic echinoderm papers, you run into two specific patterns where a lightweight stratigraphy.yaml file pays off immediately without forcing consensus:
• Famous "Echinoderm Lagerstätten" (Obrution Deposits). Echinoderms require rapid burial to stay articulated, so the literature disproportionately revolves around specific, recurring beds (e.g., the Crawfordsville crinoid beds, the Hunsrück Slate, the Bromide Formation, or the Girvan Starfish Bed). Linking these lets you query across centuries of papers without guessing whether "Crawfordsville shales" (1880) and "Edwardsville Formation" (1980) are referring to the same general package.
• Historical Name Splits and Reassignments. Many classic 19th-century North American and European formations were later split or elevated. For example, what Hall called the "Niagara Group" or "Hudson River Group" now spans multiple modern formations. In a lightweight stratigraphy.yaml file, you don't have to pick a "winner"—you can simply record equivalent_to or part_of notes as attributed claims (e.g., "Split into X and Y by Author (1965)"), staying 100% true to your non-consensus philosophy.

3. Practical Rules for "Slight" Normalization

Since you are reading the papers manually as a learning project, you can keep the overhead low with three simple boundaries:
• Only create a canonical entry on the second sighting. Keep every stratigraphic string self-contained the first time you see it. Only promote a unit to your stratigraphy.yaml lookup file when you encounter it a second time in another paper (or when it's a major unit you immediately recognize). This keeps your lookup file small and focused on your actual dataset.
• Never normalize "Horizon" or "Bed" unless it's a named marker. Leave things like "upper 2 meters", "shaly parting", or "oak tree exposure" strictly as verbatim strings on the paper's record. Only normalize named stratigraphic units (Formations, Members, Groups, or famous named beds like the "Waldron Shale").
• Keep the hierarchy flat in the lookup file. Don't try to build a strict parent-child tree inside stratigraphy.yaml, because authors disagree on whether a unit is a Member or a Formation (and Paleozoic units frequently change rank across state lines). Just store a flat list of known unit concepts with their common historical aliases.
Would you like to look at specific examples of tricky Paleozoic echinoderm stratigraphy (such as how 19th-century North American "Groups" or European "Stages" map to modern units), or discuss how to structure alias/equivalence notes in your lookup file without creating a consensus hierarchy?

