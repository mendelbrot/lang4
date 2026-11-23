# zir kek pe mim

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

### space free word divisions

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

## Composition

### Philosophy & Guiding Trade-Offs

Composition is the engine of the language. Rather than coining a new root every time a translation hits a gap, the language maintains a compact inventory of roughly 300–700 atomic roots and relies extensively on combining them to express everything else. The guiding mental model is a set of **wooden letter blocks**: each atomic morpheme is a single, self-contained syllable that snaps together in a row to build larger meanings.

This design aims for a deliberate middle ground between two extremes:

* **Toki Pona** demonstrates how playful, expressive, and learnable heavy composition can be, but its minimal lexicon can feel too sparse for sustained precision.


* **Ithkuil** offers extraordinary philosophical depth and conceptual precision, but its complexity makes it difficult to learn and it does not rely on playful word-building.



This system is a **work in progress**, and it is intentionally **not** designed to function like a rigid mathematical or chemical formula. While the compositional rules strive for an algebraic elegance, natural language is not a compiler. Attempting to eliminate all ambiguity—through rigid numbered place structures or mandatory closing terminators, as in Lojban—adds heavy cognitive overhead in real-time speech. Accepting a degree of natural linguistic ambiguity is a deliberate trade-off: it is the cost of keeping the root inventory small while unlocking creativity, poetic nuance, and fluent expressiveness.

Equally important is **restraint**. The compositional machinery exists to support precision when a thought genuinely demands it, not to encourage towering, over-engineered compounds. In practice, some of the most elegant words in the language will be the simplest ones—making light, sparing use of these rules and letting context do its share of the work.

---

### Uncertainty Clouds & Multiple Construals

Atomic roots are not narrow, one-to-one translations of English words; each root represents a continuous semantic field—an **"uncertainty cloud"**—covering a cluster of related senses. Stacking roots together narrows those clouds at each intersection, landing on more concrete referents.

Because composition is generative and perspective-driven, the system embraces two natural consequences:

* **Multiple Valid Construals:** A single concept does not require a single "correct" formula. A concept may settle on a **canonical** everyday compound while still allowing **alternative or poetic** framings that highlight a different facet of the idea.


* **Productive Phrases vs. Lexicalized Compounds:** Any two blocks *can* combine on the fly to form a transparent, one-off description. Only established, non-obvious, or culturally anchored combinations need to be recorded as lexicalized dictionary entries.



---

### Core Architectural Choices

#### 1. Zero Inherent Parts of Speech

Roots do not belong to fixed noun, verb, or adjective classes. A word's grammatical function is determined strictly by its position and its closing block: a **semantic role** closes a noun phrase, a **valency marker** closes a predicate, and a root placed after a head acts as a modifier. Because grammatical role is structural rather than lexical, dummy part-of-speech converters (like English *-ness* or *-ful*) are unnecessary.

#### 2. Organizing Operators by Arity and Scope

Word-building grammar is divided along two clean axes—**arity** (how many blocks an operator acts on) and **scope** (whether it builds a lexical stem or frames a clause):

* **Stem-Level Operators** build new concepts and compounds:
* **1-Place Unary Postfixes:** Ontological **domain lenses** (`c01`) and scale/polarity/state **modifiers** (`c02`).


* **2-Place Binary Connectors:** The **divider** (`OF`), symmetric **blend** (`BLEND`), **Boolean truth gates** (`AND`, `OR`, `XOR`, etc.), and **possessives** (`c03`).




* **Clause-Level Inflections** (roles, valency, aspect, modality, evidentials, mood) frame how a finished stem participates in a sentence rather than creating new dictionary words.



#### 3. A 100% Postfix Unary Pipeline (`X-op`)

Every unary operator in the language—including the 8 ontological domain lenses—attaches **after** the stem it modifies. Making domain lenses postfix rather than prefix was a key architectural trade-off with three major payoffs:

* **Left-to-Right Precedence:** Stacking unary operators strictly to the right encodes scope automatically without parentheses (e.g., `bitter-MIND-VERY` vs. `bitter-VERY-MIND`).


* **High-Contrast Word Onsets:** Because lexical roots are CVC and operators are CV, every content word begins immediately with a distinct, concrete CVC root rather than repetitive CV prefixes—improving speech clarity and mirroring how metaphor is processed (concrete image first, domain shift second).


* **Visual Silhouette:** In the 14-segment script, placing full-height CVC roots first, top-weighted CV operators in the middle, and bottom-weighted VC endings last gives every word a consistent left-to-right visual contour.



#### 4. Head-Initial Stacking vs. Symmetric Blending

By default, juxtaposing two roots (`A-B`) is strictly **head-initial**: `A` is the head, and `B` modifies it (`bird-fish` = a fish-like bird; `fish-bird` = a bird-like fish).

While head-initial stacking is fast and intuitive, it always forces the speaker to subordinate one concept to the other. The symmetric **blend** connector (`BLEND`) provides a commutative (*dvandva*) escape hatch for true hybrids, alloys, intermediate gradients (colors, tastes, emotions), and fused actions where neither root is subordinate. It stays strictly distinct from logical **`AND`**:

* **`A-B-AND`** = two distinct things grouped together (e.g., *red and white*, striped).


* **`A-B-BLEND`** = one unified concept fusing both natures (e.g., *pink*, blended).



---

### Precedence & Grouping: The Hybrid Model

Designing grouping rules for compounds presents a classic trade-off between **infix notation (`xRy`)** and **postfix / Reverse Polish notation (`xyR`)**:

* **Pure Postfix (`xyR`)** is algebraically unambiguous without brackets, but deeply nested expressions strain human working memory, pile connectors up at the end of a word, and collide with unmarked juxtaposition (`A-B`), which acts as an invisible binary operator.
* **Pure Infix (`xRy`)** is much easier to compose and parse in real time (especially for chained relations like possession), but requires explicit precedence rules or grouping particles whenever modifiers nest.

To capture the strengths of both without forcing speakers to track deep stacks or closing brackets, the language uses a **hybrid 6-rule precedence system** (from tightest binding to widest scope):

| Priority | Mechanism | Pattern | Behavior & Scope |
| --- | --- | --- | --- |
| **1 (Tightest)** | **Unary Modifiers** | `X-mod` | Binds tightly to the immediately preceding unit (a single root, or an already-closed `xyR` binary unit).
| **2** | **Tight Binary Connectors** | `X-Y-conn` | Local `xyR` pairing (`BLEND`, `AND`, `OR`, etc.) that grabs only the two immediately preceding units and fuses them into one block before juxtaposition occurs. |
| **3** | **Unmarked Juxtaposition** | `A-B` | Default head-initial modification between adjacent blocks (`B` modifies `A`).
| **4** | **The Divider (`OF`)** | `A-OF-B-C` | Works like Toki Pona *pi*: links the head on the left to a multi-block modifier group on the right.
| **5** | **Scope-Expanded Connectors & Modifiers** | `A-B-OF-conn-C-D` `A-B-OF-mod` | Placing `OF` before a connector turns it into a macro-infix acting on the full compounds before and after it. Placing `OF` before a unary modifier widens its scope to the entire preceding compound. |
| **6 (Widest)** | **Doubled Divider (`OF-OF`)** | `A-OF-B-OF-OF-C-D` | Repeating the divider creates a **wider outer cut**, allowing a speaker to divide an already-divided compound on the fly without pre-planning or closing brackets. |

#### Working Examples *(Using Conceptual Glosses)*

* **Local `xyR` pairing + Juxtaposition (Rules 2 & 3):**
> `bird-fish-BLEND-organism-machine-BLEND` $\rightarrow$ *"bio-mechanical fish-bird"*
> Each `BLEND` tightly fuses the two roots immediately before it (`[bird-fish-BLEND]` and `[organism-machine-BLEND]`), allowing the second block to modify the first without needing a divider.


* **Unary modifier on a closed `xyR` blend (Rules 1 & 2):**
> `red-white-VERY-BLEND` $\rightarrow$ *"light pink"* *(red blended with very-white)*
> `red-white-BLEND-VERY` $\rightarrow$ *"very pink"* *(`VERY` acts on the already-closed `[red-white-BLEND]` unit)*


* **Widening a unary modifier or lens with `OF` (Rule 5):**
> `wave-storm-MIND` $\rightarrow$ *"wave of [mental-storm]"* *(tight Rule 1)*
> `wave-storm-OF-MIND` $\rightarrow$ *"emotional rollercoaster / mental [storm-wave]"* *(`OF-MIND` shifts the entire preceding compound into the mind domain)*
> 
> 


* **Widening a binary connector with `OF` (Rule 5):**
> `practice-spirit-OF-BLEND-system-machine` $\rightarrow$ *"techno-spirituality"* *(blends the full compound `[practice-spirit]` with `[system-machine]`)*


* **Outer cut with the doubled divider (Rule 6):**
> `cup-OF-water-hot-OF-OF-wood-hard` $\rightarrow$ *"hardwood teacup"* *(`OF-OF` makes a wider outer cut over the already-divided `[cup-OF-water-hot]`)*


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

# evidentials (c1.08)

## design goals: optional, practical, and timeless

evidentials mark how the speaker knows what they are claiming[cite: 4]. as with the case system, the design aims for a practical middle ground: rich enough to make epistemic nuance explicit in daily speech, research, and personal writing, without forcing speakers to track hyper-granular sensory channels (like separate suffixes for seen vs. heard vs. smelled) or to mark every single sentence[cite: 3, 6].

two core architectural principles shape the category:

- **optionality over obligation.** unlike systems such as new ithkuil—where validation is obligatory on every assertion—`c1.08` markers are optional. an unmarked clause functions automatically as an unspecified default, keeping casual speech light and reserving evidentials for moments where the source of knowledge actually matters.
- **epistemic stance over shifting media.** the system avoids tying markers to specific information mediums (books, websites, videos, lectures). media technologies are constantly in flux, so anchoring grammatical categories to *how knowledge is grounded* (observation, deduction, trust, lived experience) keeps the language timeless.

## how evidentials fit into the grammar

evidentials are clause-level unary postfixes attached to the verb complex as part of the language's 100% postfix pipeline[cite: 3, 4].

- **runtime inflection, not lexical derivation.** like valency, aspect, modality, and mood, evidentials scope over the entire clause event and never create new dictionary entries[cite: 7].
- **separated from speaker attitude.** evidentials strictly encode *information source*[cite: 4]. emotional reaction and evaluative skepticism are kept orthogonal and handled by the affective (`uv`) and assessive (`ic`) cases[cite: 3, 6].

## key semantic boundaries

the 7 evidentials divide epistemic territory along three main axes, each with deliberate boundary choices:

### firsthand knowledge: observation (`ta`), memory (`ha`), and lived experience (`g08.07`)

- **clear perception vs. fallible recall (`ta` vs. `ha`).** rather than restricting direct perception (`ta`) strictly to live, present-tense narration—which is rarely needed outside play-by-play commentary—`ta` covers clear, vivid firsthand sensory observation in both the present and recent past. memory (`ha`) is reserved for older, less vivid, or potentially fallible personal recall (*"as i remember it..."*).
- **outside-in vs. inside-out (`ta` vs. `g08.07`).** where `ta` marks external sensory observation from the outside, the experiential evidential (`g08.07`) unifies two naturally linked "inside-out" sources: active personal participation (*living through an event in the thick of it*) and endophoric experience (*internal bodily or emotional sensations*).
- **complementing the experiencer case (`et`).** while `et` marks a specific participant's role inside the clause[cite: 6], the experiential evidential frames the speaker's epistemic stance across the whole proposition. this allows a speaker to mark lived-through truth even when they are not the grammatical subject—a distinction especially useful in journaling and expressive writing[cite: 3, 7].

### indirect knowledge: inference (`ci`) vs. intuition (`sa`)

- **clue-based deduction (`ci`).** `ci` is kept strictly for conclusions drawn from observable clues, physical evidence, or results.
- **narrowing `sa` to intuition.** an earlier "speculative/guessed" concept proved too broad, lumping experienced pattern recognition together with baseless guessing. `sa` is therefore narrowed to genuine intuition, felt sense, and tacit pattern recognition, while unfounded guesses are left to the possibility modality[cite: 7].

### secondhand knowledge: hearsay (`jo`) vs. authority (`yo`)

- **informal report (`jo`).** marks spoken reports, word of mouth, and informal hearsay.
- **trusted authority (`yo`).** rather than meaning "written down," `yo` emphasizes trusted expertise, reputable sources, and established common knowledge. defining `yo` around epistemic trust rather than physical medium keeps it future-proof and allows it to absorb encyclopedic facts naturally.

## what lives outside the evidential system

keeping `c1.08` compact relies on letting other parts of the grammar do the work they are already built for:

- **unspecified source:** handled by omitting an evidential altogether.
- **guessing and speculation:** handled by the possibility modality (`c1.07`)[cite: 7].
- **imaginary, fictional, or hypothetical events:** handled at the stem level by representative essence rather than spending a clause-level evidential slot[cite: 3].
- **cultural conventions (*"it is customary / they say"*):** handled by the perspective case (`ov`) (*"from the viewpoint of our customs..."*)[cite: 6].
- **mirativity (surprise) and doubt:** handled by the affective (`uv`) and assessive (`ic`) speaker-stance cases[cite: 3, 6].
- **direct quotation (quotative):** rather than adding a quotative evidential that alters the internal grammar of the quoted sentence (and becomes unwieldy in nested quotes), direct quotes use the language's flat paratactic syntax—introducing the quote with the cataphoric discourse pointer (`mu`) in the accusative (`om`) and marking the speech verb with `ta` (*"she said this [direct]: [quote]"*)[cite: 2, 3, 6].

## learning tiers

because evidentials are optional, none are assigned to rank 1 (the essential beginner core). instead, the 7 markers are split across two tiers:

- **rank 2 (4 core workhorses):** `ta` (direct), `ci` (inferential), `jo` (reportative), and `yo` (authoritative)—the high-frequency distinctions used in everyday reporting, explanation, and research.
- **rank 3 (3 personal/expressive nuances):** `ha` (memory), `sa` (intuitive), and `g08.07` (experiential)—finer-grained personal and somatic markers that add depth to journaling, storytelling, and poetry once the core four are comfortable[cite: 3, 7].

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

---

# Example Formula Translation

To keep example sentences in `data/04-examples.psv` resilient to future spelling changes, each row pairs a `zirkekpemim` text column with an ID-based `formula` column. The two columns are linked by an exact 1-to-1 token bijection derived from `data/02-grammar.psv` and `data/03-roots.psv`.

## Bijection Rules

Both `zirkekpemim` and `formula` are space-separated sequences of tokens:

* **Roots & Grammar Words:** Each word maps directly to its immutable ID (`nom` ↔ `r01.02`, `mi` ↔ `g10.01`, `es` ↔ `g04.01`).
* **Starred Grammar Words (`x`-Derivation):** Prefixing a grammar ID with `*` maps to its `x`-derived `CVC` form based on syllable shape (vowels are `a, e, i, o, u`):
  * `CV` ↔ `CVx` (e.g., `vux` ↔ `*g02.12`)
  * `VC` ↔ `xVC` (e.g., `xes` ↔ `*g04.01`)
* **Punctuation:** Special punctuation tokens map to uppercase codes (currently `.` ↔ `PRD`, defined in `PUNCT_TO_CODE` in `scripts/sync_examples.py`).

### Example

```text
zirkekpemim: nom    mi     es     vux     id     .
formula:     r01.02 g10.01 g04.01 *g02.12 g05.02 PRD
```

## Syncing with `scripts/sync_examples.py`

Write examples in `zirkekpemim`, then generate their `formula` entries; later, if spellings change in `02-grammar.psv` or `03-roots.psv`, regenerate `zirkekpemim` from `formula`:

```bash
# Overwrite formula from zirkekpemim
python3 scripts/sync_examples.py to-formula

# Overwrite zirkekpemim from formula
python3 scripts/sync_examples.py to-text
```

* Rows whose source cell is empty are skipped without modifying the target cell.
* Rows containing an unrecognized word, ID, or invalid starred form are skipped (left unchanged) and reported with their line number, row ID, and offending token(s).
