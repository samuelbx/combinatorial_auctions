from auctions.computations import search_prices
from random import random

x = .5
v1 = [(1, [0, 1, 1, 1, 1, 1, 1, 2])]
v2 = [(1, [0, x, x, x, x, x, x, x])]
VV = [v1, v2]

mu = .1
for v in VV:
  inner = v[0][1]
  for m in range(1, len(inner)):
    inner[m] += random()*mu

search_prices(VV, mm = 3,
              method = 'brute',
              lazy = True,
              lazy_thres = 1 - 1e-6,
              grid_points = 50)
