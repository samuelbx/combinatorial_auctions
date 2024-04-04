from auctions.computations import solve
from auctions.valuation_classes import gen_xos

v1 = [(1, gen_xos([(0,1,0), (0,0,1)]))]
v2 = [(1, gen_xos([(1,0,0), (0,0,1)]))]
v3 = [(1, gen_xos([(1,0,0), (0,1,0)]))]

solve(valuations = [v1, v2, v3],
      len_items = 3,
      prices = [1e-6, 1e-6, 1e-6],
      order_oblivious = True,
      debug = True)