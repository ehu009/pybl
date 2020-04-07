
def generate_deck(export_path):
  from cards import Deck
  d = Deck()
  d.export(export_path)
  