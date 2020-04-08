
from helpers import *
from cards import *
from roles import *


class EmptyDeckError(Exception):
  pass


class Game(object):
  def __init__(self, player_list, deck_path=None):
    self.users = player_list
    self.deck = Deck()
    self.current = 0
    self.users.append(Dealer())
    #grant each participant two cards
    for i in range(0, 2):
      for u in self.users:
        u.give(self.deck.pick())
  
  def participants(self):
    return self.users
  
  def conclude(self):
    pass
  
  def end(self):
    pass


def new_game(player_names, deck_path):
  pass
  