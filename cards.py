
def sanitize(csv):
  return csv.replace(" ", "") \
          .replace("\t", "") \
          .replace("\r", "") \
          .replace("\n", "")

  
class Card(object):
  suites = ['H', 'D', 'S', 'C']
  heights = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
  
  def __init__(self, value):
    suite = value[0]
    height= value[1:len(value)]
    if suite not in Card.suites or height not in Card.heights:
      raise CardValueError
      return None
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
    pass
    
  def __len__(self):
    pass
    
  def pick(self, n=1):
    pass
  
  def export(self, save_path):
    pass