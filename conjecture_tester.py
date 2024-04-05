from auctions.computations import solve
from auctions.valuation_classes import gen_xos
from random import random
import numpy as np

rnd = True
if not rnd:
  v1 = [(1, gen_xos([(1,0,0), (0,1,0)]))]
  v2 = [(1, gen_xos([(0,1,0), (0,0,1)]))]
  v3 = [(1, gen_xos([(0,0,1), (1,0,0)]))]
else:
  v1 = [(1, gen_xos([(random(), random(), random()), (random(), random(), random())]))]
  v2 = [(1, gen_xos([(random(), random(), random()), (random(), random(), random())]))]
  v3 = [(1, gen_xos([(random(), random(), random()), (random(), random(), random())]))]

print('v1', np.round(v1[0][1], 3))
print('v2', np.round(v2[0][1], 3))
print('v3', np.round(v3[0][1], 3))

def grid_gen(m1, M1, m2, M2, m3, M3, N):
  grid = []
  for i in range(N+1):
    for j in range(N+1):
      for k in range(N+1):
        #if not (i==0 and j==0 and k==0):
        grid.append([m1+(M1-m1)*i/N, m2+(M2-m2)*j/N, m3+(M3-m3)*k/N])
  return grid

prices_grid = grid_gen(0, 1, 0, 1, 0, 1, 20)
scores, prices = [], []
for price in prices_grid:
  score = solve(valuations = [v1, v2, v3],
                len_items = 3,
                prices = price,
                order_oblivious = True,
                silent = True)["score"]
  if score >= 2/3 - 1e-9:
    scores.append(score)
    prices.append(price)

print(f'{min(scores)*100:2f}% score achieved with prices {prices[scores.index(min(scores))]}')