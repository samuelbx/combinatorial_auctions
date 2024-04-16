from auctions.valuation_classes import gen_subadd_set_cover

print('1 item', gen_subadd_set_cover(2**1-1))
print('3 items', gen_subadd_set_cover(2**2-1))
print('7 items', gen_subadd_set_cover(2**3-1))
