# pybl
A Python3 implementation of Blackjack

## Requirements
Requires python3 installed on your system.

## Usage
Run *script.py* using one of these modes:
#### -generate
Generates a deck of cards.
If no export path is provided, default path is `./deck.csv`
Optional input parametres: export path
###### examples
`python3 ./script.py -generate my_cards.txt`
`python3 ./script.py -generate`

#### -test
Tests the implementation, not including game over turnout nor game state after dealing initial cards.
Takes no parametres.
###### examples
`python3 ./script.py -test asdf`
`python3 ./script.py -test`

#### default
Plays blackjack. The game will not be started if `-test` or `-generate` are provided.
Optional parameters: custom deck path, player names.
Path to custom deck is specified using `-file`.
If player name(s) are not provided, one will be known as "Player".
###### examples
`python3 ./script.py albert lance`
`python3 ./script.py -file my_deck.txt`
`python3 ./script.py albert -file another_deck.txt lance terrence`
`python3 ./script.py`

## Custom deck files
This file can have *any extension*, but it's card values **must** be written in a single line, and **must** be separated by commas.
Whitespace in the deck file will be ignored, and card values can be *either* lower or upper case.
On import, custom decks **must not** contain duplicates, and **must** contain exactly 52 cards.

## Game rules
Players are shuffled at game start, dealer is always last.
Cards from custom decks are picked from front to back.
After dealing two cards each, players who have not made a bust can pick cards.
###### Player win scenarios
* If score is higher than or same as dealer's score
* Dealer makes a bust and player does not
###### Dealer win scenarios
* If all players make a bust
* Dealer's score exceeds all players' scores
