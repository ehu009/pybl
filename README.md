# pybl
A Python3 implementation of Blackjack

##Requirements
Requires python3 installed on your system.

##Usage
Run *script.py* using these input parametres:
`[-test] || [-generate 'save path'] || ['player name'] ['player names ...'] [-file 'path to deck']`
The game will not be started if `-test` or `-generate` are provided.
If player names are not provided, one will be known as "Player".

Examples:
* `python3 ./script.py -test`
* `python3 ./script.py alf bella carmen`
* `python3 ./script.py alf bella -file ./my_exotic_cards.csv`
* `python3 ./script.py -generate ./fresh_deck.csv`
