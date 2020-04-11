
from helpers import sanitize 

class DeckImportError(Exception):
  pass
class CardValueError(Exception):
  pass


  
class Card(object):
  suites = ['H', 'D', 'S', 'C']
  heights = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
  
  def __init__(self, value):
    suite = value[0]
    height= value[1:len(value)]
    if suite not in Card.suites or height not in Card.heights:
      raise CardValueError
    
    self.value = value
  
  def __repr__(self):
    return self.value
    
  def __int__(self):
    s = self.value[1:len(self.value)]
    try:
      return int(s)
    except ValueError:
      if s == "A":
        return 11
      return 10
    
  def __str__(self):
    return repr(self)

class Deck(object):
  
  def __init__(self, deck_path=None):
    if deck_path is None:
      self.cards = []
      for suite in Card.suites:
        for height in Card.heights:
          self.cards.append(Card(suite+height))
      from random import shuffle
      shuffle(self.cards)
    else:
      with open(deck_path,'r') as f:
        self.cards = []
        l = sanitize(f.readline()).split(',')
        if len(l) != 52:
          print("Error: deck has %i cards" % len(l))
          raise DeckImportError
        from helpers import count_occurrences
        occurrences = count_occurrences(l)
        dupes = False
        for n in occurrences.values():
          if n != 1:
            dupes = True
        if dupes:
          print("Error: deck has duplicate cards")
          raise DeckImportError
        
        for c in l:
          try:
            self.cards.append(Card(c.upper()))
          except CardValueError:
            print("Error: deck contains illegal cards")
            raise DeckImportError
  
  def __len__(self):
    return len(self.cards)
  
  def pick(self, n=1):
    if len(self) == 0:
      return None
    if n == 1:
      return self.cards.pop(0)
    l = []
    for i in range(0, n):
      l.append(self.pick())
    return l
  
  def export(self, save_path):
    s = ""
    for card in self.cards:
      s+=str(card)+", "
    s = s[0:len(s)-2]
    with open(save_path, 'w+') as f:
      f.write(s)
    
    