from auctions.computations import solve
from auctions.valuation_classes import gen_zero, gen_additive

def brute_test(alpha, epsilon=1e-6):
  v1 = [(1, [0, 1, 1, 1, 1, 1, 1, 2])]
  v2 = [(1/3, gen_additive((1, 1, 0))),
        (1/3, gen_additive((0, 1, 1))),
        (1/3, gen_additive((1, 0, 1)))]
  v3 = [(1-epsilon, gen_zero(3)),
        (epsilon, gen_additive((alpha/epsilon, alpha/epsilon, alpha/epsilon)))]

  solve(valuations = [v1, v2, v3],
        len_items = 3,
        prices = None,
        order_oblivious = False)

brute_test(1)