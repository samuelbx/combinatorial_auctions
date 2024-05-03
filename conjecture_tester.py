from auctions.computations import solve
from tqdm import tqdm
from itertools import product

v0 = [(1, [0, 1, 0, 0, 1, 1, 1, 1])]
v1 = [(1, [0, 0, 1, 0, 1, 1, 1, 1])]
v2 = [(1, [0, 0, 0, 1, 1, 1, 1, 1])]
v3 = [(1, [0, 3, 3, 3, 3, 3, 3, 3])]
mm = 3
VV = [v0, v1, v2, v3]

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

def thres_grid_gen(V, mm, eps=1e-9):
  lists = []
  for j in range(1, mm+1):
    sublist = [0]
    for vi in V:
      sublist.append(vi[0][1][j]+eps)
      sublist.append(vi[0][1][j]-eps)
    lists.append(sublist)
  return product(*lists)

prices_grid = list(thres_grid_gen(VV, mm))
# prices_grid = grid_gen(0, 1, 40, mm)
scores, prices = [], []
for price in tqdm(prices_grid):
  score = solve(valuations = VV,
                len_items = mm,
                prices = price,
                order_oblivious = True,
                silent = True)["score"]

  scores.append(score)
  prices.append(price)


score = solve(valuations = VV,
              len_items = mm,
              prices = prices[scores.index(max(scores))],
              order_oblivious = True,
              debug = True)["score"]

print(f'{max(scores)*100:2f}% score achieved with prices {prices[scores.index(max(scores))]}')