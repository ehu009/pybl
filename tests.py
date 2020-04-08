
from helpers import map_to_list
from cards import sanitize


def test_generation(path):
  """
  verifies the following:
    -deck existence
    -deck size
    -card value correspondance
    -card uniqueness
  """
  print("Testing deck generation...")
  from helpers import generate_deck
  generate_deck(path)
  
  cards = []
  try:
    with open(path, 'r') as f:
      cards = sanitize(f.readline()).split(',')
  except FileNotFoundError:
    print("Error: could not find generated deck file \"" + path + "\"")
    return True
  
  if len(cards) is not 52:
    print("Error: generated deck has wrong number of cards: " + str(len(cards)))
    return True
  
  from cards import Card
  from cards import count_occurences
  for card in cards:
    suite = card[0].upper()
    height = card[1:len(card)].upper()
    
    if (suite not in Card.suites) or (height not in Card.heights):
      print("Error: generated deck has card with unexpected value: " + card)
      return True
  
  appears = count_occurences(cards)  
  for n in appears.values():
    if n > 1:
      print("Error: generated deck has duplicate cards")
      return True
  
  print("OK")


def test_decks(deck_path, bogus_path):
  """
  verifies the following:
    -random deck can be made
    -deck is reduced when taking cards from it
    -custom deck can be loaded from file, preserving desired order
    -importing custom decks with exotic cards raises an exception
    -importing custom decks with duplicate cards raises an exception
    -trying to obtain a card from an empty deck will yield none
  """
  print("Testing implementation of decks...")
  from cards import Deck, Card, DeckImportError
  
  d1 = Deck()
  if len(d1) != 52:
    print("Error: new deck has wrong amount of cards")
    return True
  d1.export(bogus_path)
  
  c1 = d1.pick()
  if len(d1) != 51:
    print("Error: taking a card from a deck does not reduce it's size")
    return True
  
  c2 = d1.pick()
  if c1 == c2:
    print("Error: can take the same card out of a deck twice")
    return True
  
  
  d2 = Deck(deck_path)
  test_cards = d2.pick(52)
  if d2.pick() != None:
    print("Error: trying to take a card from an empty deck does not return None")
    return True
  
  cards = []
  with open(deck_path, 'r') as f:
    cards = sanitize(f.readline()).split(',')
  
  cards = map_to_list(lambda x: Card(x), cards)
  
  for a, b in zip(cards, test_cards):
    if str(a) != str(b):
      print("Error: order is not preserved when importing a custom deck: "+str(a)+" vs. "+str(b))
      return True
  
  with open(bogus_path,'r') as f:
    cards = sanitize(f.readline()).split(',')
  cards.pop()
  cards.append("X13")
  s = ",".join(cards)
  with open(bogus_path,'w+') as f:
    f.write(s)
    
  q = True
  try:
    Deck(bogus_path)
  except DeckImportError:
    q = False
  if q:
    print("Error: a deck containing exotic cards can be imported without raising an exception")
    return True
  
  cards.pop()
  s = ",".join(cards)
  with open(bogus_path,'w+') as f:
    f.write(s)
    
  q = True
  try:
    Deck(bogus_path)
  except DeckImportError:
    q = False
  if q:
    print("Error: a deck with wrong number of cards can be imported without raising an exception")
    return True
  
  cards.append(cards[0])
  s = ",".join(cards)
  with open(bogus_path,'w+') as f:
    f.write(s)
    
  q = True
  try:
    Deck(bogus_path)
  except DeckImportError:
    q = False
  if q:
    print("Error: a deck containing duplicate cards can be imported without raising an exception")
    return True
  
  print("OK")
  

  
def test_cards():
  """
    verifies the following:
    -cannot create a card that shouldn't exist 
    -card has string representation
    -card has integer representation corresponding to blackjack score
  """
  print("Testing implementation of cards...")
  from cards import Card, CardValueError
  
  #six of hearts yields six points
  c = Card('H6')
  if str(c) != 'H6':
    print("Error: card cannot be represented as a string")
    return True
  if int(c) != 6:
    print("Error: card cannot be represented as an integer")
    return True
  
  #jack, queen and kings any suite yield 10 points
  cases = ['J', 'Q', 'K']
  for case in cases:
    c = Card('H' + case)
    if int(c) != 10:
      err_str = "Error: "
      if case == 'J':
        err_str += 'jacks'
      elif case == 'Q':
        err_str += 'queens'
      elif case == 'K':
        err_str += 'kings'
      print(err_str + " yield " + str(int(c)) + " points instead of 10")
      return True
    
  #aces of any suite yield 11 points"
  c = Card('HA')
  if int(c) != 11:
    print("Error: aces yield " + str(int(c)) + " points instead of 11")
    return True
  
  q = True
  try:
    c = Card('X13')
  except CardValueError:
    q = False
  if q:
    print("Error: a card with exotic value can be created without raising an exception: "+ c)
    return True
  
  print("OK")


def test_participants():
  """
  verifies the following:
    -participant can obtain cards
    -participant has a string representation
    -participant has an integer representation
    -participant loses if their score is above 21
  """
  print("Testing implementation of participants...")
  from roles import Participant
  from cards import Card
  
  p = Participant("Dealer")
  if p.name != "Dealer":
    print("Error: participant name cannot be specified")
    return
  
  cards = map_to_list(lambda x: p.take(Card(x)),['H3', 'H4', 'SQ'])
  
  if len(p) != 3:
    print("Error: participant can not obtain cards")
    return True
  s = repr(p)
  if s != "Dealer: H3, H4, SQ":
    print("Error: participant can not be represented as string")
    return True
  n = int(p)
  if n != 17:
    print("Error: participant can not be represented as integer")
    return True
  
  p.take(Card('DQ'))
  if int(p) > 21 and bool(p):
    print("Error: participant does not lose if score is above 21")
    return True
    
  print("OK")


def test_dealer():
  """
  verifies the following:
  -dealer can not obtain cards if current score is above 17
  -dealer does not obtain cards if dealer's score is higher than that of other players
  -dealer will not try to beat the score of a player that has lost
  -dealer will try to beat remaining players
  """
  print("Testing implementation of dealers...")
  from roles import Player, Dealer
  from cards import Card
  
  p1 = Player('Edward')
  d = Dealer()
  cards = map_to_list(lambda x: Card(x), ['H3', 'H4', 'SQ'])
  for c in cards:
    p1.take(c)
    d.take(c, [p1])
  if d.take(Card('H7'), [p1]):
    print("Error: dealer can obtain cards if current score is 17 or above")
    return True
  
  c1 = [Card('HQ'), Card('H7')]
  c2 = [Card('SQ'), Card('H6')]
  c3 = [Card('DQ'), Card('H5')]
  
  p1 = Player("alice")
  p2 = Player("bob")
  d = Dealer()
  for c in c2:
    p1.take(c)
  for c in c3:
    p2.take(c)
  for c in c1:
    d.take(c, [p1, p2])
  if d.take(Card('S2'), [p1, p2]):
    print("Error: dealer takes another card when current score exceeds players' scores")
    return True
  
  p1 = Player("alice")
  d = Dealer()
  for c in c2:
    p1.take(c)
  for c in c3:
    d.take(c, [p1])
  p1.take(Card('SQ'))
  if d.take(Card('S2'), [p1]):
    print("Error: dealer tries to beat the score of a player who has already lost")
    return True
  
  p1 = Player("alice")
  p2 = Player("bob")
  d = Dealer()
  for c in c1:
    p1.take(c)
  for c in c2:
    p2.take(c)
  for c in c3:
    d.take(c, [p1, p2])
  p2.take(Card('SQ'))
  if not d.take(Card('S2'), [p1, p2]):
    print("Error: dealer does not try to beat remaining players")
    return True
  
  print("OK")


def test_game_init():
  """
  verifies the following:
  -default number of participants is 2
  -dealer is always named 'Dealer'
  -two cards are dealt to each participant at game start
  """
  
  print("Testing implementation of card game...")
  from blackjack import Game
  from roles import Player, Dealer
  
  g = Game([Player("Player")])
  people = g.participants()
  if len(people) != 2:
    print("Error: default number of participants is not 2 (dealer + player)")
    return True
  
  ann = Player("Ann")
  peter = Player("Peter")
  simon = Player("Simon")
  g = Game([ann, peter, simon])
  
  people = g.participants()
  for p in people:
    if type(p) is Dealer and p.name() != "Dealer":
      print("Error: dealer is not automatically named \"Dealer\"")
      return True
    if len(p) != 2:
      print("Error: participants do not start with two cards each")
      return True
  
  print("OK")


def test_game_over(path):
  """
  verifies the following:
  -raises exception when deck becomes empty
  -
  """
  #-when the game is over, info about dealer and players is printed to screen
  #-when the game is over, there could be a draw
  #-when the game is over, the winners' names are printed
  print("Testing game over turnout...")
  
  from blackjack import Game, EmptyDeckError
  from roles import Player, Dealer
  from cards import Deck
  from helpers import generate_deck
  
  generate_deck(path)
  
  ann = Player("Ann")
  peter = Player("Peter")
  simon = Player("Simon")
  g = Game([ann, peter, simon], path)
  
  game.deck.pick(44)
  q = True
  try:
    game.deck.pick()
  except EmptyDeckError:
    q = False
  if q:
    print("Error: exception is not raised when trying to take a card from an empty deck")
    return True
  
  
  
  
  # implement me, stupid
  
  
  print("OK")


def run_tests():
  """
    runs all tests
  """
  path = "_test_deck.csv"
  from os import remove
  
  if test_generation(path):
    print("Error testing deck generation")
    remove(path)
    return
  
  path2 = "_bogus.csv"
  if test_decks(path, path2):
    print("Error testing deck functionality")
    remove(path)
    remove(path2)
    return
  remove(path2)
  
  if test_cards():
    print("Error testing card functionality")
    remove(path)
    return
  remove(path)
  
  if test_participants():
    print("Error testing participant functionality")
    return
  
  if test_dealer():
    print("Error testing dealer functionality")
    return
  
  if test_game_init():
    print("Error testing game initialization")
    return
  
  if test_game_over(path):
    print("Error testing game turnouts")
    remove(path)
    return
  remove(path)
  
  print("ALL OK")
  