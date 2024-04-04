from itertools import combinations

def possible_bundles(M: int):
  numbers = list(range(M))
  for i in range(0, M+1):
    for comb in combinations(numbers, i):
      yield comb

def len_possible_bundles(M: int):
  return len(list(possible_bundles(M)))

def item_indicator(M: int):
  bundles = list(possible_bundles(M))
  indicator = [[] for _ in range(M)]
  for i, bundle in enumerate(bundles):
    for item in bundle:
      indicator[item].append(i)
  return indicator