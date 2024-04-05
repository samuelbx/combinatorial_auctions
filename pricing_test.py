from auctions.computations import _compute_price_first, solve, item_indicator
from auctions.valuation_classes import gen_rand_xos
import scipy.optimize as spo
import numpy as np
from random import random

def objective_fun(V, opt_attr, indicator):
  def _f(p, pr=False):
    quantities = []
    for i, vi in enumerate(V):
      opt_i = opt_attr[i]
      p_opt_i = _compute_price_first(p, opt_i, indicator)
      for M in range(len(vi)):
        if M != vi:
          p_M = _compute_price_first(p, M, indicator) 
          quantities.append(vi[opt_i] - p_opt_i - (vi[M] - p_M))
    if pr:
      print(np.round(quantities, 3))
      if min(quantities) >= 0:
        print("All negative!")
    return -min(quantities)
  return _f

mm = 3
VV = gen_rand_xos(3, mm)

opt_attr = solve(valuations = VV,
                 len_items = mm,
                 prices = [0]*mm,
                 order_oblivious = True)["optimal_bundles"][0][1]

ind = item_indicator(mm)
fun = objective_fun([vi[0][1] for vi in VV], opt_attr, ind)

eps = 1e-6
p = spo.brute(fun, ranges=[(eps,1-eps), (eps,1-eps), (eps,1-eps)], Ns=20)

score = solve(valuations = VV,
              len_items = mm,
              prices = p,
              order_oblivious = True)["score"]

fun(p, pr=True)
print(score, p)