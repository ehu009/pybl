
from helpers import map_to_list

class Participant(object):
  def __init__(self, name):
    self.name = name
    self.playing = True
    self.cards = []
    self.score = 0
  
  def __bool__(self):
    return self.playing
  
  def __repr__(self):
    return self.name + ": " + ", ".join(map_to_list(lambda x: repr(x), self.cards))
  
  def __int__(self):
    return self.score
  
  def __len__(self):
    return len(self.cards)
  
  def give(self, card):
    self.cards.append(card)
    self.score += int(card)
    if self.score > 21:
      self.playing = False
    return True
    
  def take(self, card):
    return self.give(card)
    
  
  def defeat(self):
    self.playing = False
  
  
class Dealer(Participant):
  
  def __init__(self):
    super().__init__("Dealer")
  
  def take(self, card, players):
    if self.score >= 17:
      return False
    if True in map_to_list(lambda x: bool(x), players):
      for q, n in map_to_list(lambda x: (bool(x), int(x)), players):
        if q and n >= int(self):
          return super().take(card)
    return False


class Player(Participant):
  pass