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

## update and next step

the formula for a compound word is 

`E+E+...E`

where the E can be:

* a grammar id like `g01.01`
* grammar id converted to a root like `X(g01.01)` where `X()` represents conversion by adding an initial or final 'x' depending on the category of grammar word
* a root id like `r01.01`

So an example compound formula is:

`r01.01+X(r01.02)+g01.01+g01.02`

desired features:

* static html webpage to view categories, grammar, roots, and compounds. human and machine readable

this language is more done than i think. if i just have that then i can start playing around with making up my own sentences

starting with a dictionary.

then a document outlining the rules, as i test them against translations

then add sparkle words, say 20 per category. think about what words would be really fun/interesting to play with. maybe part of the art this language can be the choice of words: instead of going toward precision and practicality, maybe instead i can find amazing, vivid words to add. maybe each word can be like a poem or painting.

This can be a metaphorical language. if i create a set of stories or parables or poems, themselves written in the language then each story will have different elements/characters

then the words can be derived from the story names. the story itself "story"+"mushroom cave" can be a word saying the lesson or theme of the story, and the different elements "agent of story cave mushroom" can be different specific items or archetypes form the story.

just an idea. or i can just try to find really cool sparkle words