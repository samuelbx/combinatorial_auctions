from auctions.computations import solve
from auctions.valuation_classes import gen_zero, gen_xos, gen_subadditive

def counter_ex(alpha, eps=1e-9):
  v1 = [(1, gen_xos([(1,0,0), (0,1,0)]))]
  v2 = [(1, gen_xos([(0,1,0), (0,0,1)]))]
  v3 = [(1, gen_xos([(0,0,1), (1,0,0)]))]
  v4 = [(1-eps, gen_zero(3)), (eps, gen_subadditive((alpha/eps, alpha/eps, alpha/eps)))]

  solve(valuations = [v1, v2, v3, v4],
        len_items = 3,
        prices = [0.01, 0.01, 0.01],
        order_oblivious = True)

print(':: alpha = 2')
counter_ex(2)

print('\n:: alpha -> +inf')
counter_ex(1e6)