

def map_to_list(method, sequence):
  return list(map(method, sequence))


def generate_deck(export_path):
  from cards import Deck
  d = Deck()
  d.export(export_path)


