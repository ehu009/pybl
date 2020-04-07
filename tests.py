
def test_generation(path):
  """
  verifies the following:
    -deck existence
    -deck size
    -card value correspondance
    -card uniqueness
  """
  print("Testing deck generation...")
  from generate import generate_deck
  generate_deck(path)
  
  cards = []
  try:
    with open(path, 'r') as f:
      l = f.readline() \
          .replace(" ", "") \
          .replace("\t", "") \
          .replace("\r", "") \
          .replace("\n", "")
      cards = l.split(',')
  except FileNotFoundError:
    print("Error: could not find generated deck file \"" + path + "\"")
    return True
  
  if len(cards) is not 52:
    print("Error: generated deck has wrong number of cards: " + str(len(cards)))
    return True
  
  appears = {}
  from cards import Card
  for card in cards:
    suite = card[0].upper()
    height = card[1:len(card)].upper()
    
    if (suite not in Card.suites) or (height not in Card.heights):
      print("Error: generated deck has card with unexpected value: " + card)
      print(suite)
      print(height)
      return True
    try:
      appears[card] += 1
    except KeyError:
      appears[card] = 1
    
  for n in appears.values():
    if n > 1:
      print("Error: generated deck has duplicate cards")
      return True
  
  print("OK")
  

def test_decks(deck_path):
  """
  verifies the following:
    -random deck can be made
    -deck is reduced when taking cards from it
    -custom deck can be loaded from file, preserving desired order
  """
  print("Testing implementation of decks...")
  from cards import Deck
  
  d1 = Deck.new()
  if len(d1) != 52:
    print("Error: new deck has wrong amount of cards")
    return True
  
  c1 = d1.pick()
  if len(d1) != 51:
    print("Error: taking a card from a deck does not reduce it's size")
    return True
  
  c2 = d1.pick()
  if c1 == c2:
    print("Error: can take the same card out of a deck twice")
    return True
  
  
  d2 = Deck.new(deck_path)
  test_cards = d2.pick(52)
  cards = []
  with open(deck_path, 'r') as f:
    l = f.readline() \
        .replace(" ", "") \
        .replace("\t", "") \
        .replace("\r", "") \
        .replace("\n", "")
    cards = l.split(',')
  if cards != test_cards:
    print("Error: order is not preserved when importing a custom deck")
    return True
  print("OK")
  

def run_tests():
  """
    runs all tests
  """
  path = "test_deck.csv"
  
  if test_generation(path):
    print("Error testing deck generation")
    return
    
  if test_decks(path):
    print("Error testing deck functionality")
    return
  
  