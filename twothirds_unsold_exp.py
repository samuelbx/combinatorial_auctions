from auctions.computations import solve, search_prices
from auctions.valuation_classes import gen_rand_xos
from auctions.utils import minimal_prices_gen

#%

players = 4
mm = 2

#%

VV = gen_rand_xos(players, mm)
result = solve(valuations = VV,
      len_items = mm,
      prices = [1e-6]*mm,
      order_oblivious = True)

opt_val = result['opt_val']

search_prices(VV, mm,
              method = minimal_prices_gen(opt_val, mm, N=200),
              lazy = True,
              lazy_thres = 2/3 - 1e-3,
              grid_points = 50)
