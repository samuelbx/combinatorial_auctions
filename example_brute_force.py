from auctions.computations import solve
from auctions.valuation_classes import gen_zero, gen_additive, gen_subadditive
from random import random

record = 1.1
def brute_test(epsilon=1e-6):
  global record

  alpha = random() * 2
  v1 = [(1, [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])]
  v2 = [(1/3, gen_additive((1, 1, 1, 0))),
        (1/3, gen_additive((1, 1, 0, 1))),
        (1/3, gen_additive((0, 1, 1, 1)))]
  v3 = [(1-epsilon, gen_zero(4)),
        (epsilon, gen_additive((alpha/epsilon, alpha/epsilon, alpha/epsilon, alpha/epsilon)))]

  score = solve(valuations = [v1, v2, v3],
                len_items = 4,
                prices = None,
                order_oblivious = False,
                silent = True)["score"]
  if score < record:
    print(score, alpha)
    record = score

while True:
  brute_test()