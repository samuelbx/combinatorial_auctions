from auctions.computations import solve
from auctions.valuation_classes import gen_xos, gen_rand_xos
from tqdm import tqdm
from itertools import product
from random import random

rnd = True
if not rnd:
  v1 = [(1, gen_xos([(1,0,0), (0,1,0)]))]
  v2 = [(1, gen_xos([(0,1,0), (0,0,1)]))]
  v3 = [(1, gen_xos([(0,0,1), (1,0,0)]))]
  mm = 3
  VV = [v1, v2, v3]
else:
  len_players, mm = 3, 3
  VV = gen_rand_xos(len_players, mm)

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
    sublist = [0]
    for vi in V:
      sublist.append(vi[0][1][j]+eps)
      sublist.append(vi[0][1][j]-eps)
    lists.append(sublist)
  return product(*lists)

def test(VV, prices_grid):
  #prices_grid = [[d1-2*eps2, (d1+d2)/2, d2-eps2]]
  #prices_grid = thres_grid_gen(VV, mm)
  scores, prices = [], []
  for price in prices_grid:
    score = solve(valuations = VV,
                  len_items = mm,
                  prices = price,
                  order_oblivious = True,
                  silent = True)["score"]
    if score >= 2/3 - 1e-9:
      scores.append(score)
      prices.append(price)
  return scores, prices

for i in tqdm(range(int(1e6))):
  eps = 1e-6
  """
  x = [random() for _ in range(6)]
  x.sort()
  d1, d2 = 1-eps*x[5], 1-eps*x[4]
  v1 = [(1, gen_xos([(0,d1,0), (0,0,d2)]))]
  v2 = [(1, gen_xos([(d1,0,0), (0,0,d2)]))]
  v3 = [(1, gen_xos([(d1,0,0), (0,d2,0)]))]
  mm = 3
  VV = [v1, v2, v3]
  """

  mm = 3
  VV = gen_rand_xos(3, mm)

  prices_grid = thres_grid_gen(VV, mm)
  scores, prices = test(VV, prices_grid)

  if max(scores) < 0.8:
    prices_grid = grid_gen(0, 1, 20, mm)
    scores, prices = test(VV, prices_grid)
    if max(scores) < 0.8:
      prices_grid = grid_gen(0, 1, 40, mm)
      scores, prices = test(VV, prices_grid)
      if max(scores) < 0.8:
        for i, vi in enumerate(VV):
          print(f'v{str(i+1)}', vi[0][1])
        break




print(f'{min(scores)*100:2f}% score achieved with prices {prices[scores.index(min(scores))]}')
print(f'{max(scores)*100:2f}% score achieved with prices {prices[scores.index(max(scores))]}')