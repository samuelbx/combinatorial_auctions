from itertools import combinations


def possible_bundles(M: int):
  numbers = list(range(M))
  for i in range(0, M+1):
    for comb in combinations(numbers, i):
      yield comb


def possible_bundles_names(M: int) -> list[str]:
  item_names = [chr(97 + i) for i in range(M)]
  bundles = possible_bundles(M)
  bundle_names = []
  for bundle in bundles:
    bundle_elems = [item_names[elem] for elem in bundle]
    bundle_names.append('{' + ', '.join(bundle_elems) + '}')
  bundle_names[0] = 'ø'
  return bundle_names


def len_possible_bundles(M: int) -> int:
  return len(list(possible_bundles(M)))


def item_indicator(M: int) -> list[list[int]]:
  bundles = list(possible_bundles(M))
  indicator = [[] for _ in range(M)]
  for i, bundle in enumerate(bundles):
    for item in bundle:
      indicator[item].append(i)
  return indicator