
from helpers import *
from cards import *
from roles import *


class EmptyDeckError(Exception):
  pass


class Game(object):
  def __init__(self, player_list, deck_path=None):
    self.users = map_to_list(lambda x: Player(x.capitalize()), player_list)
    try:
      self.deck = Deck(deck_path)
    except DeckImportError:
      exit()
    self.users.append(Dealer())
    #grant each participant two cards
    for i in range(0, 2):
      for user in self.users:
        user.give(self.deck.pick())
  
  def participants(self):
    return self.users
  
  def results(self):
    for u in self.users:
      if not bool(u):
        print("%s has busted -" % u.name)
        if type(u)==Dealer:
          return True
        else:
          print(u)
      else:
        if int(u) == 21:
          print(u.name + " has blackjack")
          return True
    
    return False
  
  def winners(self, dealer):
    scores = sorted(self.users, key=lambda x: int(x.score),reverse=True)
    win = []
    for u in scores:
      n = int(u)
      if n > 21:
        continue
      if bool(dealer):
        if n == 21:
          win.append(u)
          continue
        if len(win) > 0:
          if int(win[0]) != n:
            break
      win.append(u)
    return win
  
  def play(self):
    players = self.users.copy()
    dealer = players.pop()
    
    if not self.results():
      q_str = "Will you draw a card? Yy/Nn: "
      for u in self.users:
        if bool(u):
          print("It's " + u.name+"'s turn -")  
          try:
            while(bool(u)):
              
              if type(u)==Dealer:
                allow = False
                try:
                  allow = u.take(None, players)
                except:
                  allow = True
                if allow:
                  u.take(self.deck.pick(), players)
                else:
                  break
              else:
                print(str(u))
                r = input(q_str).upper()
                if r == "N":
                  break
                elif r == "Y":
                  u.take(self.deck.pick())
                else:
                  print("Strange input, try again")
          except EmptyDeckError:
            print("Error: ran out of cards")
            exit()
            
        if type(u) != Dealer:
          if not bool(u):
            print(u.name + " has lost, having " + str(int(u)) + " points.")
            print(u)
        else:
          print("Dealer picked %i cards" % (len(dealer)-2))
        print()
    self.game_over(dealer)
  
  def game_over(self, dealer):
    win = self.winners(dealer)
    if len(win) == 0:
      print("All have busted - house wins")
      print("Dealer's hand: %s" % ', '.join(map_to_list(lambda x: str(x), dealer.cards)))
      return
    
    if len(win) > 1:
      try:
        win.remove(dealer)
        
      except ValueError:
        pass
    
    if len(win) > 1:  
      print("Multiple winners:")
    else:
      print("Winner:")
    
    for u in win:
      print("%i points by %s - : %s" % (int(u),u.name, ', '.join(map_to_list(lambda x: str(x), u.cards)) ))
    if dealer not in win:
      print("Dealer's hand: %s" % ', '.join(map_to_list(lambda x: str(x), dealer.cards)))
   