from auctions.computations import solve
from auctions.valuation_classes import gen_rand_xos
from tqdm import tqdm
from itertools import product

rnd = False
if not rnd:
  v1 = [(1, [0, .798, .994, 1.575])]
  v2 = [(1, [0, .624, .334, .958])]
  mm = 2
  VV = [v1, v2]
else:
  len_players, mm = 3, 3
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

def thres_grid_gen(V, mm, eps=1e-9):
  lists = []
  for j in range(1, mm+1):
    sublist = [0]
    for vi in V:
      sublist.append(vi[0][1][j]+eps)
      sublist.append(vi[0][1][j]-eps)
    lists.append(sublist)
  return product(*lists)

# prices_grid = grid_gen(0, 1, 10, mm)
prices_grid = list(thres_grid_gen(VV, mm))
scores, prices = [], []
for price in tqdm(prices_grid):
  score = solve(valuations = VV,
                len_items = mm,
                prices = price,
                order_oblivious = True,
                silent = True)["score"]
  print(price, score)
  if score >= 2/3 - 1e-9:
    scores.append(score)
    prices.append(price)

print(f'{min(scores)*100:2f}% score achieved with prices {prices[scores.index(min(scores))]}')
print(f'{max(scores)*100:2f}% score achieved with prices {prices[scores.index(max(scores))]}')