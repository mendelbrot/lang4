# lang4

here's my folder structure so far, showing the columns for the files in the data folder

```txt
.
├── assign_sounds.py
├── data
│   ├── 01-categories.psv
│   ├── 02-grammar.psv
│   ├── 03-roots.psv
│   └── 04-compounds.psv
├── random-target-concepts.psv
├── README.md
├── sample_targets.py
├── semdom.json
└── view-groups
    ├── domain-lense.psv
    └── modifiers.psv
```

my idea is that the language is just a list of words, but to understand and shape it, i project it into views. the views arent part of the language itself, but necessary for me to understand and interact with it conceptually

there will be a desktop web application that, given a selected word, will show a grid of modified words. the view itself is just a grid of modifier word ids. for example the genders one might be a for column by two row grid of genders. the app projects a selected word into that, and it then shows a grid of text fields to view and edit the definitions of the related words (three fields per word in the case of compounds, in case a compound might mean more than one thing). changes are saved to 02-elements.csv or 03-compounds.csv depending if the edited word is an element or a compound

likewise there will be a view group with the modifiers very, not, un etc...

in random-target-concepts.psv thats where well get the list of words we want to translate to work backward from. all the words will be listed in this file but the the app will show a graph for each of the categories 

all of the categories, elements, compounds and semantic words to work backward from (target concepts) will have ids, they we be numeric and prefixed by a letter representing the file they're from
- categories: `c1.01`
- grammar: `g01.01`
- roots: `r01.01`
- compounds: `w0001`

what are the categories? every word in the language will belong to a category, for example a semantic role, a grammatical gender word, or a 'physical world, materials and weather' word category etc. every element word belongs to a category, but generally not every category has a element word that represents it (the gender modifiers by definition represent their grammatical gender category but thats a special case, but the way, im open to using an alternative name for 'grammatical gender' and in general open to improving my category names)

my goals for this conlang:
toki pona is beautifully crafted but too simple
ithkuil is very interesting philosophically and has many cool ideas i want to play with, but its too hard to learn and work with and also doesnt leverage composition like toki pona does which is very useful.
the goal is a language midway between them that is very expressive and also easy to learn. im going for something very polished and suitable for art, poetry, song, journaling, etc.
the central analogy for how i think about this language is those letter blocks that babies play with. each element word is a block. stack them in a row to make a word. these blocks are very carefully crafted so that putting them together into words is a joyful fun process that naturally supports fluent creative expression

---

# Philosophy & Design Principles

## 1. Purpose & Aesthetic Vision

This language was created out of an aesthetic dissatisfaction with the irregularities of natural languages, and as a tool for thinking about ideas from a different perspective. It is designed to be polished, expressive, and genuinely usable—especially for personal journaling, art, poetry, and song.

Its design aims for a deliberate sweet spot between two extremes:

* **Toki Pona** is beautifully crafted, easy to learn, and demonstrates the expressive power of heavy composition, but its vocabulary is too minimal for sustained precision.


* **Ithkuil** is philosophically fascinating and rich in conceptual distinctions, but it is notoriously difficult to learn and does not rely on playful word composition.

The goal is a language midway between the two: **small enough to learn and hold in your head, yet structurally expressive enough to capture nuance, emotion, and logic without friction**. Its grammatical architecture also draws on cross-linguistic typology (notably R. M. W. Dixon’s *Are Some Languages Better Than Others?*) and select ideas from predicate logic (Lojban) and stem-level semantic operators (New Ithkuil).

---

## 2. The Central Metaphor: Toy Blocks & Uncertainty Clouds

The mental model of the language is a set of **wooden letter blocks**. Every atomic element is a single, carefully crafted syllable. You build words by snapping blocks together in a row—a process meant to feel tactile, playful, and conducive to fluent creative expression.

Three lexical principles grow out of this metaphor:

* **Composition First:** Rather than coining a new root every time a translation hits a snag, the language maintains a compact inventory of ~300–700 lexical roots built outward from a broad, Toki Pona-inspired "fuzzy" core, relying extensively on compounding and derivation to build everything else.

* **Uncertainty Clouds vs. Crossroads:** An atomic root is not a narrow English definition—it is a continuous semantic field (an "uncertainty cloud") covering a cluster of conceptually linked senses. Chaining roots into a compound narrows those clouds at each crossroads, landing on specific, concrete referents (and occasionally more than one distinct meaning).

* **Multiple Valid Construals:** Because composition is flexible, a single concept does not require a single rigid formula. A concept may have a canonical everyday compound alongside poetic or alternative framings—turning word-building itself into an exercise in perspective-shifting.

---

## 3. Core Grammatical Principles

### Zero Inherent Parts of Speech

Roots have no built-in noun, verb, or adjective class. A word's grammatical function is determined strictly by its closing block—a **semantic role** makes it a noun phrase, a **valency marker** makes it a predicate, and placing a root after a head makes it a modifier. Dummy part-of-speech converters (like English *-ness* or *-ful*) are eliminated.

### A 100% Postfix Unary Pipeline

Every unary operator in the language—domain lenses, stem modifiers, semantic roles, valency, aspect, modality, evidentials, and mood—attaches **after** the stem it modifies (`X-op`).

* **Bracket-Free Precedence:** Operators apply strictly left-to-right, so block order unambiguously encodes scope without needing parentheses or closing particles.


* **High-Contrast Word Onsets:** Because lexical roots are `CVC` and modifiers are `CV`, content words always begin with a high-contrast `CVC` anchor rather than repetitive prefixes.


* **Unified Stem-Building:** Aspect and modality markers can appear inside noun stems as well as verb stems (e.g., combining with the Target-Head modifier to build compositional participles like *edible*, *beloved*, or *task*), with zero ambiguity because the closing role (`VC`) or valency (`VC`) always signals the word's clause function.

### The 8 Ontological Domain Lenses

Inspired by Bantu noun classes and philosophical thesauri, the lexicon is organized into 8 conceptual domains: **matter, biology, motion, artifact, sense, mind, society, and form**. Each domain has an optional `CV` **lens** postfix that projects any root's core image-schema into a new realm—acting as a built-in, systematic metaphor engine (e.g., shifting physical *bitter* into the `mind` lens to yield *resentment*, or shifting a concrete noun into the `form` lens to yield its abstract quality).

### Neutrality & Anti-Markedness

Deriving opposites through a single "negative" operator creates hidden **lexical markedness**—quietly declaring one pole the "default" and lumping concepts like *dark*, *black*, *cold*, or *small* into the same mental bucket as *bad* or *broken*. To avoid this:

* **Neutral Scale Roots:** Physical continua (such as *size*) are encoded as neutral parameter roots modified symmetrically by **high**, **moderate**, and **low** degree operators.


* **Precision in Negation:** Logical negation (*not*), polar reversal (*opposite*), absence (*-less*), and scalar *other-than* (*non-X*) are kept strictly distinct.

### No Copula & Fluid-S Alignment

The vague English verb *"to be"* is replaced by a 3-way core valency system—**stative/class**, **intransitive process**, and **transitive/causative action**—paired with **Fluid-S (Active-Stative)** case marking. This lets speakers cleanly distinguish classifying a thing (*"it is a run"*), describing an involuntary process (*"the river runs"*), and describing a volitional action (*"she runs"*).

### Flat, Paratactic Syntax (No Subclauses)

Rather than nesting clauses inside clauses, the language links standalone clauses using **anaphoric and cataphoric discourse pointers** (*"that prior statement"*, *"this next statement"*) combined with ordinary semantic roles (causal, purposive, conditional, concessive, temporal).

### Explicit Speaker Stance & General Number

* **Subtext Made Explicit:** Pragmatic nuances that English hides inside vague adverbs (like *"really"* or *"just"*) are surfaced cleanly through dedicated **evidentials**, **moods**, and **affective/assessive** semantic roles.

* **General Number & Base-6 Math:** Bare nouns are number-neutral; quantity is specified only when relevant using base-6 numbers, degree modifiers, or quantifiers.

# cases (c1.04)

## design goals: the middle ground

most case systems fall toward one of two extremes. european languages tend to lump many unrelated meanings into a handful of broad grammatical buckets, leaving speakers to rely on arbitrary verb conventions and prepositions. at the other end, philosophical languages like ithkuil subdivide semantic roles into dozens of hyper-specific micro-cases that are rich in precision but heavy to learn[cite: 2, 4].

this language aims for the sweet spot between them: small enough to hold in your head, yet explicit enough to make perspective and agency visible[cite: 2]. two practical principles guide what earns a case:

- **lump where the verb disambiguates for free.** broad macro-roles (like accusative) are not ad-hoc hodgepodges when their sub-meanings are mutually exclusive and automatically projected by the verb. a separate case for "thing broken," "thing transferred," and "thing perceived" would only duplicate information the verb already provides.
- **paraphrase the rare periphery.** because the language uses short, flat clauses linked by discourse pointers[cite: 2, 4], uncommon nuances do not need dedicated cases if they read naturally as a second clause. a peripheral case only earns a slot when it is high-frequency, solves a real ambiguity, or serves as a core clause-linker.

## how cases work in the clause

roots have no inherent part of speech[cite: 2]. a word becomes a noun phrase strictly by closing with a word-final VC case suffix from `c1.04`, just as a verb closes with a valency suffix from `c1.05`[cite: 2, 4].

unlike english, the language does not have fixed syntactic "subject" and "object" buckets that erase semantic differences. instead:

- **valency (`c1.05`)** sets the verb's structural frame—whether it is a 1-place state (`id`), a 1-place process (`uc`), a 2-place transitive relation (`at`), or a comparison (`ak`)[cite: 10].
- **case (`c1.04`)** specifies exactly how each noun plugs into that frame.
- **word order and the head marker** handle information structure (topic and emphasis)[cite: 4, 11]. because cases mark every noun's role explicitly, clause-level word order stays flexible, allowing the speaker to place whichever participant they want to spotlight at the front of the clause.

## the three-way core & fluid-s alignment

instead of forcing every "subject" into a single nominative case, the core of the system splits along volition and consciousness (fluid-s / active-stative alignment):

- **nominative (`es`)** is reserved for deliberate, volitional agents and actors (as well as the comparee in a comparison).
- **experiencer (`et`)** marks a conscious perceiver, feeler, or mental/sensory state holder. it can step into the first core slot of both 1-place states (*"i am cold"*) and 2-place transitive experiences (*"i saw a bird"*, *"i fear the dark"*), keeping `es` strictly volitional.
- **accusative (`om`)** is the primary undergoer macro-role. it marks patients, transferred themes, perceived stimuli, comparison standards, and non-volitional intransitive subjects (*"the water is cold"*, *"the river flows"*).
- **causal (`ot`)** handles inanimate forces and acts of nature (*"the wind broke the window"*). if a speaker wants to personify nature and imply intent, they can deliberately swap `ot` for `es`.

this design replaces the need for extra "soft agent" or "participant" cases: by choosing between `es`, `et`, `om`, `os` (recipient), or reciprocal valency, the speaker can turn a single event around to highlight agency, passive experience, or mutual participation.

## what lives outside the case system

keeping `c1.04` focused on **noun-to-verb** (and clause-framing) relationships means two major functions live elsewhere by design:

- **possession (`c1.03`)** is a noun-to-noun relationship rather than a noun-to-verb one, so the five possessive types sit with the binary stem linkers rather than competing with clause cases.
- **comparisons (`c1.05`)** are handled by a dedicated comparative valency (`ak`) on the dimension/comparison verb itself, reusing `es` (comparee) and `om` (standard) instead of spending separate case slots.

within `c1.04` itself, three cases—**vocative (`as`)**, **affective (`uv`)**, and **assessive (`ic`)**—stand outside the verb's argument structure entirely, framing the speech act or the speaker's attitude toward the whole proposition rather than participating in the event.

## cases as clause-linkers

the language avoids nested subclauses and standalone conjunction particles[cite: 2, 4]. instead, it pairs `c1.04` cases with anaphoric and cataphoric discourse pointers (*that-before* and *this-after*). attaching a case directly to a discourse pointer turns the previous or following sentence into a logical or temporal link:

- **the reason quartet** (`ot` causal, `ob` purposive, `av` conditional, `ib` concessive) generates *therefore*, *in order to*, *if so*, and *however*.
- **spatiotemporal cases** (`in` locative, `ac` ablative, `an` allative) generate *meanwhile*, *after that*, and *until then*.
- **accusative (`om`)** embeds a referenced clause as the direct object of speech or thought (*"i think this: ..."*).

## learning tiers

the 26 cases are organized into two ranks so learners do not have to absorb the entire inventory at once:

- **rank 1 (17 core cases):** the core argument roles, primary spatiotemporal cases, basic circumstantials, the reason quartet, and vocative—everything needed for fluent everyday expression.
- **rank 2 (9 precision cases):** secondary spatial/temporal spans (`ik`, `ut`), speaker-stance markers (`uv`, `ic`), and expressive framing cases (`oc` essive, `ov` perspective, `og` substitutive, `af` consumptive) that add nuance once the core is comfortable.

---

## 4. Sound, Symbolism & Script

### Self-Segregating Syllable Shapes

Every atomic morpheme is strictly one syllable, and its phonological shape immediately signals its grammatical tier:

* **`CVC`** = Lexical content roots.

* **`CV`** = Stem-level operators, verb inflections, pronouns, and numbers.

* **`VC`** = Word-final nominal roles and verbal valency.

* **Systematic `x-` Derivation:** A dedicated consonant bridge systematically turns grammatical blocks into standalone `CVC` content roots.

### Iconicity Without Taxonomic Confusion

Root spellings draw on cross-linguistic sound symbolism—such as Bouba/Kiki texture contrasts, vowel pitch/magnitude symbolism, and articulatory mimicry—so words feel intuitively tied to their meanings. At the same time, the language deliberately avoids rigid philosophical sound-templates (where every word in a category starts with the same letter), ensuring that neighboring concepts remain acoustically distinct and hard to mishear.

### The 14-Segment Featural Script

The language's 20 consonants map onto a zero-gap $5 \times 4$ featural coordinate grid—place of articulation on the outer frame, manner and voicing on the inner diagonals—paired with 5 central vowel shapes. Because closing consonants vertically mirror initial consonants, each syllable shape has an unmistakable visual silhouette: `CVC` roots fill the full glyph, `CV` modifiers weight the top, and `VC` endings weight the bottom, giving every stacked word a clear left-to-right contour.

---

## 5. Living Development Principles *(For Future Maintenance)*

* **Database-as-Code:** The language lives as plain-text, version-controlled files in Git, decoupling immutable Concept IDs from their current phonological spellings so sounds can be reassigned without breaking compounds or translations.


* **Views Over Hierarchy:** The lexicon itself is a flat list of blocks; conceptual grids (lens matrices, modifier matrices, semantic graphs) are non-destructive "views" projected over that data.


* **De-Biasing Against English:** Vocabulary design is anchored against cross-linguistic datasets (such as CLICS and SIL Semantic Domains) rather than English dictionaries alone, preventing English idioms and polysemy from quietly dictating the root inventory.