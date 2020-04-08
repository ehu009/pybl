
class Participant(object):
  def __init__(self, name):
    self.name = name
    self.playing = True
    self.cards = []
    self.score = 0
  
  def __bool__(self):
    return self.playing
  
  def __repr__(self):
    return self.name + ": " + ", ".join(list(map(lambda x: repr(x), self.cards)))
  
  def __int__(self):
    return self.score
  
  def __len__(self):
    return len(self.cards)
  
  def take(self, card):
    self.cards.append(card)
    self.score += int(card)
    if self.score > 21:
      self.playing = False
  



class Dealer(Participant):
  pass

class Player(Participant):
  pass
