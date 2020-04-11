

def map_to_list(method, sequence):
  """
  maps 'method' unto each item in 'sequence', returns a list
  """
  return list(map(method, sequence))


def generate_deck(export_path):
  """
  generates a shuffled deck, saves the file at 'export_path'
  """
  from pkg.cards import Deck
  d = Deck()
  d.export(export_path)

def sanitize(csv):
  """
  input: csv is a csv string
  """
  return csv.replace(" ", "") \
          .replace("\t", "") \
          .replace("\r", "") \
          .replace("\n", "")

def count_occurrences(card_list):
  """
  input: card_list is a list of strings (not a list of cards)
  """
  n = {}
  for card in card_list:
    try:
      n[card] += 1
    except KeyError:
      n[card] = 1
  return n