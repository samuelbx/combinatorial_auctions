from itertools import combinations, product


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


def item_indicator(M: int) -> list[list[int]]:
  bundles = list(possible_bundles(M))
  indicator = [[] for _ in range(M)]
  for i, bundle in enumerate(bundles):
    for item in bundle:
      indicator[item].append(i)
  return indicator


def grid_gen(m, M, N, mm):
  grid = []
  indices = product(*[list(range(N+1)) for _ in range(mm)])
  for idxes in indices:
    elem = []
    for i in idxes:
      elem.append(m+(M-m)*i/N)
    grid.append(elem)
  return grid


def thres_grid_gen(V, mm, eps=1e-9):
  lists = []
  for j in range(1, mm+1):
    sublist = set()
    for vi in V:
      if vi[0][1][j] - eps >= 0:
        sublist.add(vi[0][1][j]-eps)
      sublist.add(vi[0][1][j]+eps)
    lists.append(sublist)
  return product(*lists)