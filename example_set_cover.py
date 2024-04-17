from auctions.utils import possible_bundles_names
from auctions.valuation_classes import gen_subadd_set_cover

def gen(k):
  m = 2**k - 1
  names = possible_bundles_names(m)
  val = gen_subadd_set_cover(m)
  print(f'{m} item(s)', list(val))

for k in range(1, 4):
  gen(k)