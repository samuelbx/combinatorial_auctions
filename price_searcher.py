from auctions.computations import search_prices

eps = 1e-6
v0 = [(1, [0, 1, 0, 0, 1, 1, 1, 1])]
v1 = [(1, [0, 0, 1, 0, 1, 1, 1, 1])]
v2 = [(1, [0, 0, 0, 1, 1, 1, 1, 1])]
v3 = [(1, [0, 1+eps, 1+eps, 1+eps, 1+eps, 1+eps, 1+eps, 1+eps])]
mm = 3
VV = [v0, v1, v2, v3]

for i, vi in enumerate(VV):
  print(f'v{str(i+1)}', vi[0][1])

search_prices(VV, mm, 'thresholds', lazy = True)