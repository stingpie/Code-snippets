# Code-snippets
A collection of code that I made

# bf-squared
The whole idea behind this is to make an esoteric language. Inspried by BF https://en.wikipedia.org/wiki/Esoteric_programming_language#Brainfuck and piet https://en.wikipedia.org/wiki/Esoteric_programming_language#Piet , BF² is like bf, with a few upgrades. BF² is sort of 2.5D. In bf², there are multiple layers which different actors reside in. On each layer, there are different tiles which actors can use as a program. 

ACTORS:
Each actor has a few important aspects which control how they act. The most important aspect is the "active" token. "Active" decides whether an actor takes the tiles it stands on as code. Inactive actors get their actions through linked partners. An actor can be "linked" to another actor, and then give that linked partner commands, or even take the variable from its partner. Each actor has storage for variables, which it can take from the tile it stands on, or its partners. If an actor has multiple partners, and it asks for its partner's variables, it will take all the variables, and put them into an array. 

If all the tiles they pass over are zero, actors will continue to move in the direction self.dir

TILES:
Tile zero: does nothing

Tile one to five: changes the direction of the actor. (right, up, left, down, none)

Tile six to nine: shifts the actors, but sets their direction to none. (right, up, left, down)

Tile ten: tile ten acts as an "if equal" statement. First, the primary actor searches for other actors who are directly next to it. Then, if the primary actor's variable equals ANY of the secondary actor's variables, the primary actor "hops" over the secondary. 

Tile eleven: This tile tells the actor to store the tile number into self.variables. It is completely useless on an active actors, it is intended to be used on linked partners. 

Tile twelve: Twelve makes the actor aggregate all the data from its partner's self.variables into an array.

Tiles thirteen to sixteen: these tiles order the actor to change the tile it's standing on. Once again, this is intended for inactive partners. 

Tile seventeen: toggles whether the actor is active

Tile eighteen: links the primary actor with another actor of the index self.variables[0]

Tile nineteen: removes the nth actor from the linked list, where n is self.variables[0]

Tile twenty: uses the first six variables from self.variables to create a new actor. 
