from auctions.computations import solve
from auctions.valuation_classes import gen_rand_xos
from tqdm import tqdm


for i in tqdm(range(int(1e6))):
  len_players, mm = 3, 2
  VV = gen_rand_xos(len_players, mm)
  score = solve(valuations = VV,
                len_items = mm,
                prices = 'auto',
                order_oblivious = True,
                silent = True)["score"]
  if score < 1:
    print(score, VV)
    break