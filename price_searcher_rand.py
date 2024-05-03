from auctions.computations import search_prices
from auctions.valuation_classes import gen_rand_xos
from tqdm import tqdm

# Lazy: stops whenever finds prices such that CR >= 2/3
for i in tqdm(range(int(1e6))):
  VV = gen_rand_xos(3, 3)
  score = search_prices(VV,
                        mm = 3,
                        method = 'thresholds_aug',
                        lazy = True,
                        silent = True,
                        lazy_thres = 1 - 1e-9,
                        grid_points = 20)
  if score < 1 - 1e-9:
    print(score)
    for i, vi in enumerate(VV):
      print(f'v{str(i+1)} {vi[0][1]}')
    score = search_prices(VV,
                          mm = 3,
                          method = 'brute',
                          lazy = True,
                          lazy_thres = 1 - 1e-9,
                          silent = False,
                          grid_points = 50)