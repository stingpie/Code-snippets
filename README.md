# Code-snippets
A collection of code that I made

# bf-squared
The whole idea behind this is to make an esoteric language. Inspried by BF https://en.wikipedia.org/wiki/Esoteric_programming_language#Brainfuck and piet https://en.wikipedia.org/wiki/Esoteric_programming_language#Piet , BF² is like bf, with a few upgrades. BF² is sort of 2.5D. In bf², there are multiple layers which different actors reside in. On each layer, there are different tiles which actors can use as a program. 

ACTORS:
Each actor has a few important aspects which control how they act. The most important aspect is the "active" token. "Active" decides whether an actor takes the tiles it stands on as code. Inactive actors get their actions through linked partners. An actor can be "linked" to another actor, and then give that linked partner commands, or even take the variable from its partner. Each actor has storage for variables, which it can take from the tile it stands on, or its partners. If an actor has multiple partners, and it asks for its partner's variables, it will take all the variables, and put them into an array. 

SPECIAL TILES:
Tile ten: tile ten acts as an "if equal" statement. First, the primary actor searches for other actors who are directly next to it. Then, if the primary actor's variable equals ANY of the secondary actor's variables, the primary actor "hops" over the secondary. 
