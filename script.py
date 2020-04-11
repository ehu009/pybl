import sys

def find_arg(needle, haystack):
  """
  returns an argument labelled by 'needle'
  
  assumes argument immediately follows it's label
  """
  for i in range(0, len(haystack)):
    if haystack[i] == needle:
      return haystack[i+1]
  return None

def arg_parse(args):
  """
  extracts command line arguments to be passed to game creation method
  
  provides default values if no arguments are given
  """
  path = find_arg('-file', args)
  names = args
  if path is not None:
    names.remove('-file')
    names.remove(path)
  if len(names) is 0:
    names = ['Player']
  return names, path


if __name__ == '__main__':
  q = sys.argv[1:]
  if len(q) > 0:
    if '-test' in q:
      from pkg.tests import run_tests
      run_tests()
      exit()      
    elif '-generate' in q:
      p = find_arg('-generate', q)
      if p is None:
        p = 'deck.csv'
      from pkg.helpers import generate_deck
      generate_deck(p)
      exit()
  from pkg.blackjack import Game
  names, deck = arg_parse(q)
  g = Game(names, deck)
  g.play()
  print("Exiting")
  