from auctions.computations import solve
from auctions.valuation_classes import gen_xos, gen_rand_xos
import numpy as np
from tqdm import tqdm
from itertools import product

rnd = True
if not rnd:
  v1 = [(1, gen_xos([(1,0,0), (0,1,0)]))]
  v2 = [(1, gen_xos([(0,1,0), (0,0,1)]))]
  v3 = [(1, gen_xos([(0,0,1), (1,0,0)]))]
  mm = 3
  VV = [v1, v2, v3]
else:
  len_players = 4
  mm = 4
  VV = gen_rand_xos(len_players, mm)

for i, vi in enumerate(VV):
  print(f'v{str(i+1)}', np.round(vi[0][1], 3))

def grid_gen(m, M, N, mm):
  grid = []
  indices = product(*[list(range(N+1)) for _ in range(mm)])
  for idxes in indices:
    elem = []
    for i in idxes:
      elem.append(m+(M-m)*i/N)
    grid.append(elem)
  return grid

prices_grid = grid_gen(0, 1, 10, mm)
scores, prices = [], []
for price in tqdm(prices_grid):
  score = solve(valuations = VV,
                len_items = mm,
                prices = price,
                order_oblivious = True,
                silent = True)["score"]
  if score >= 2/3 - 1e-9:
    scores.append(score)
    prices.append(price)

print(f'{min(scores)*100:2f}% score achieved with prices {prices[scores.index(min(scores))]}')