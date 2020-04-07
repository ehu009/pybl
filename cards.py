
  
  
class Card(object):
  suites = ['H', 'D', 'S', 'C']
  heights = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
  
  def __init__(self, value):
    pass
    
  def __repr__(self):
    pass
    
  def __int__(self):
    pass
    

class Deck(object):
  
  def __init__(self, deck_path=None):
    pass
  
  def __len__(self):
    pass
    
  def pick(self, n=1):
    pass
  
  def export(self, save_path):
    pass