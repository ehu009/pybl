
def generate_deck(export_path):
  from cards import Deck
  d = Deck.new()
  d.export(export_path)