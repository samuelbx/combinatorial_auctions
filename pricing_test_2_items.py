from auctions.computations import solve
from auctions.valuation_classes import gen_rand_xos
from itertools import product

rnd = True
if not rnd:
  v1 = [(1, [0, 1, 1, 2])]
  v2 = [(1, [0, 1, 1, 1])]
  mm = 2
  VV = [v1, v2]
else:
  len_players, mm = 2, 2
  VV = gen_rand_xos(len_players, mm)

for i, vi in enumerate(VV):
  print(f'v{str(i+1)}', vi[0][1])

def grid_gen(m, M, N, mm):
  grid = []
  indices = product(*[list(range(N+1)) for _ in range(mm)])
  for idxes in indices:
    elem = []
    for i in idxes:
      elem.append(m+(M-m)*i/N)
    grid.append(elem)
  return grid

def thres_grid_gen(V, mm, eps=1e-4):
  lists = []
  for j in range(1, mm+1):
    sublist = [0]
    for vi in V:
      sublist.append(vi[0][1][j]+eps)
      sublist.append(vi[0][1][j]-eps)
    lists.append(sublist)
  return product(*lists)

score = solve(valuations = VV,
              len_items = mm,
              prices = 'auto',
              order_oblivious = True,
              debug = True)["score"]

print(score)