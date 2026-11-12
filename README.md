# lang4

here's my folder structure so far, showing the columns for the files in the data folder
.
├── data
│   ├── 01-categories.csv: id,meaning
│   ├── 02-elements.csv: id,category,spelling,meaning
│   ├── 03-compounds.csv: id,elements,meaning1,meaning2,meaning3
│   └── 04-semantic-network-groups.csv: id,category,concept,compound1,compound2,compound3
├── README.md
└── view-groups
    ├── 01-gender.csv: a matrix of ids
    └── 02-modifiers.csv: a matrix of ids

my idea is that the language is just a list of words, but to understand and shape it, i project it into views. the views arent part of the language itself, but necessary for me to understand and interact with it conceptually

there will be a desktop web application that, given a selected word, will show a grid of modified words. the view itself is just a grid of modifier word ids. for example the genders one might be a for column by two row grid of genders. the app projects a selected word into that, and it then shows a grid of text fields to view and edit the definitions of the related words (three fields per word in the case of compounds, in case a compound might mean more than one thing). changes are saved to 02-elements.csv

likewise there will be a view group with the modifiers very, not, un etc...

in data/04-semantic-network-groups.csv thats where well get the list of words we want to translate to work backward from. all the words will be listed in this file but the the app will show a graph for each of the categories 

all of the categories, elements, compounds and semantic words to work backward from will have ids, i think they will just be numbered like @001, @002, @003 etc. 

what are the categories? every word in the language will belong to a category, for example a semantic role, a grammatical gender word, or a 'physical world, materials and weather' word category etc. every element word belongs to a category, but generally not every category has a element word that represents it (the gender modifiers by definition represent their grammatical gender category but thats a special case, but the way, im open to using an alternative name for 'grammatical gender' and in general open to improving my category names)

my goals for this conlang:
toki pona is beautifully crafted but too simple
ithkuil is very interesting philosophically and has many cool ideas i want to play with, but its too hard to learn and work with and also doesnt leverage composition like toki pona does which is very useful.
the goal is a language midway between them that is very expressive and also easy to learn. im going for something very polished and suitable for art, poetry, song, journaling, etc.
the central analogy for how i think about this language is those letter blocks that babies play with. each element word is a block. stack them in a row to make a word. these blocks are very carefully crafted so that putting them together into words is a joyful fun process that naturally supports fluent creative expression