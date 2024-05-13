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


def arange(m, M, N):
  for i in range(N+1):
    yield m + (M-m)*i/N


def sum_arange(max, N, no_items):
  if no_items == 0:
    yield []
  elif no_items == 1:
    yield [max]
  else:
    for val in arange(0, max, N):
      for end in sum_arange(max-val, N, no_items-1):
        yield [val] + end


def minimal_prices_gen(OPT, mm, thres=2/3-1e-2, N=20):
  bundles, indicator = list(possible_bundles(mm)), item_indicator(mm)
  for b in range(1,len(bundles)):
    p = [0]*mm
    idxes = set()
    for i, item in enumerate(indicator):
      if b in item: # item in bundle
        idxes.add(i)
    for i in range(mm):
      if not i in idxes:
        p[i] = 1e12 # infty
    
    # generate
    for vals in sum_arange(thres * OPT, N, len(idxes)):
      for idx, val in zip(idxes, vals):
        p[idx] = val
      yield p.copy()


def thres_grid_gen(V, mm, eps=1e-9, aug=False):
  lists = []
  for j in range(1, mm+1):
    sublist = set()
    for vi in V:
      if vi[0][1][j] - eps >= 0:
        sublist.add(vi[0][1][j]-eps)
      sublist.add(vi[0][1][j]+eps)
      if aug:
        assert mm == 3
        ab = vi[0][1][4]
        ac = vi[0][1][5]
        bc = vi[0][1][6]
        aa = vi[0][1][1]
        bb = vi[0][1][2]
        cc = vi[0][1][3]
        e = vi[0][1][j]
        sublist.add(e/2-eps)
        sublist.add(e/2+eps)
        if j != 1:
          sublist.add(ab - aa - eps)
          sublist.add(ab - aa + eps)
          sublist.add(ac - aa - eps)
          sublist.add(ac - aa + eps)

        if j != 2:
          sublist.add(ab - bb - eps)
          sublist.add(ab - bb + eps)
          sublist.add(bc - bb - eps)
          sublist.add(bc - bb + eps)

        if j != 3:
          sublist.add(ac - cc - eps)
          sublist.add(ac - cc + eps)
          sublist.add(bc - cc - eps)
          sublist.add(bc - cc + eps)

        # TODO: prevent negative prices from being added
        
    lists.append(sublist)
  return product(*lists)
