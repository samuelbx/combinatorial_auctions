from auctions.computations import search_prices

v0 = [(1, [0, 1, 0, 0, 1, 1, 1, 1])]
v1 = [(1, [0, 0, 1, 0, 1, 1, 1, 1])]
v2 = [(1, [0, 0, 0, 1, 1, 1, 1, 1])]
v3 = [(1, [0, 2, 2, 2, 2, 2, 2, 2])]

# Lazy: stops whenever finds prices such that CR >= 2/3
search_prices(VV = [v0, v1, v2, v3],
              mm = 3,
              method = 'thresholds',
              lazy = True)