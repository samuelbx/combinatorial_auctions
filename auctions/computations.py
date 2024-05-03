from itertools import product, permutations
from .utils import item_indicator, possible_bundles_names, grid_gen, thres_grid_gen
from math import prod
from tqdm import tqdm


BUNDLE_NAMES = None
PRICE_CACHE = []
OPT_CACHE = None
VALUATIONS_CACHE = None
PRIORITY = -1
TAG = None

def _log(priority, txt, end='\n', tag=None):
  global PRIORITY
  if priority <= PRIORITY and (tag is None or TAG is None or tag == TAG):
    print(txt, end=end)

def _possible_next_moves(list_taken: list[bool], 
                         indicator: list[list[int]]) -> list[int]:
  impossible_next = set()
  for item, taken in enumerate(list_taken):
    if taken:
      for j in indicator[item]:
        impossible_next.add(j)
  len_bundles = len(BUNDLE_NAMES)
  possible_next = []
  for i in range(len_bundles):
    if not i in impossible_next:
      possible_next.append(i)
  return possible_next


def _compute_price_first(prices: list[float], attr: int,
                         indicator: list[list[int]]) -> float:
  total_price = 0
  for i, p in enumerate(prices):
    if attr in indicator[i]:
      total_price += p
  return total_price


def _player_utility_of_move(deterministic_valuation: list[float], move: int) -> float:
  assert len(PRICE_CACHE) > 0
  return deterministic_valuation[move] - PRICE_CACHE[move]


def _update_list_taken(list_taken: list[bool], move: int,
                       indicator: list[list[int]], inplace=True) -> None:
  if not inplace:
    list_taken = list_taken.copy()
  len_items = len(indicator)
  for item in range(len_items):
    if move in indicator[item]:
      list_taken[item] = True
  return list_taken


def _utility_maximizing_moves(deterministic_valuation: list[float],
                              list_taken: list[bool], indicator: list[list[int]], tol: float=1e-12) -> tuple[int, float]:
  possible_next = _possible_next_moves(list_taken, indicator)
  max_utility = 0
  utility_maximizing_next = []
  for move in possible_next:
    player_utility = _player_utility_of_move(deterministic_valuation, move)
    if player_utility > max_utility:
      utility_maximizing_next = [move]
      max_utility = player_utility
    elif abs(player_utility - max_utility) < tol:
      utility_maximizing_next.append(move)
  return utility_maximizing_next


def _explore_opt(determ_V, list_taken, indicator):
  if len(determ_V) == 0:
    return [], 0
  
  deter_v_head, deter_tail = determ_V[0], determ_V[1:]
  possible_next = _possible_next_moves(list_taken, indicator)
  
  welfares, next_attrs = [], []
  for move in possible_next:
    list_taken_next = _update_list_taken(list_taken, move, indicator, inplace=False)
    welfare_move = deter_v_head[move]
    attr_next, welfare_next = _explore_opt(deter_tail, list_taken_next, indicator)
    welfares.append(welfare_move + welfare_next)
    next_attrs.append(attr_next)

  welfare_opt = max(welfares)
  idx = welfares.index(welfare_opt)
  attr_opt = next_attrs[idx]

  return [possible_next[idx]] + attr_opt, welfare_opt


def _compute_opt(valuations: list[tuple[float, list[float]]], indicator: list[list[int]]) -> float:
  _log(1, f'Computing OPT:')
  total_expected_val = 0
  sample_space = product(*[list(range(len(v))) for v in valuations])
  possible_attributions = []
  for possibility in sample_space:
    probability = prod(valuation[possibility[i]][0] for i, valuation in enumerate(valuations))
    _log(1, f'  Sample space {possibility} [p = {100*probability:2f}%]:')
    deterministic_valuations = [valuation[possibility[i]][1] for i, valuation in enumerate(valuations)]
    attr, welfare = _explore_opt(deterministic_valuations, [False] * len(indicator), indicator)
    attr_text = '(' + ', '.join([BUNDLE_NAMES[j] for j in attr]) + ')'
    _log(1, f'  OPT = {welfare} [attribution = {attr_text}]')
    possible_attributions.append((probability, attr))
    total_expected_val += probability * welfare
  return total_expected_val, possible_attributions


def _explore_alg(V, prices, list_taken, indicator, sig, N=1):
  if len(V) == 0:
    return 0
  
  sum = 0
  head, tail = V[0], V[1:]
  for proba, deter_v_head in head:
    if len(head) > 1:
      _log(1, _indent(f'╟ Agent {sig[N-1]+1} chooses valuation {deter_v_head} [proba = {proba*100:2f}%]', N))
    if prices is not None:
      possible_next = _utility_maximizing_moves(deter_v_head, list_taken, indicator)
    else:
      possible_next = _possible_next_moves(list_taken, indicator)
    
    extrval = 1e12 if prices is not None else 0
    for move in possible_next:
      list_taken_next = _update_list_taken(list_taken, move, indicator, inplace=False)
      welfare_move = deter_v_head[move]
      log_text = f'{sig[N-1]+1} buys {BUNDLE_NAMES[move]} ({welfare_move})'
      _log(1, _indent(f'╟ {log_text}', N), tag=sig)
      welfare_next = _explore_alg(tail, prices, list_taken_next, indicator, sig, N+1)
      welfare_branch = welfare_move + welfare_next
      extrval = min(welfare_branch, extrval) if prices is not None else max(welfare_branch, extrval)

      # EXPLANATION: if there are posted prices, agent has the choice & may provoke the worst-case scenario
      # if generic algorithm, we can choose the best option!
    if N == 1:
      _log(1, _indent(f'╙ Total: {extrval}', N), tag=sig)
    sum += extrval * proba
  
  return sum


def _compute_alg(valuations, prices: list[float],
                 order_oblivious: bool, indicator: list[list[int]]) -> tuple[list[int], float]:
  len_agents = len(valuations)
  _log(1, f'Computing ALG:')
  if not order_oblivious:
    list_taken = [False] * len(indicator)
    return _explore_alg(valuations, prices, list_taken, indicator, tuple(range(len_agents)))
  else:
    vals, perms = [], list(permutations(range(len_agents)))
    for perm in perms:
      order_text = '→'.join([str(i+1) for i in perm])
      _log(1, _indent(f'╓ Order {order_text}:', 1), tag=perm)
      list_taken = [False] * len(indicator)
      val = _explore_alg([valuations[i] for i in perm], prices, list_taken, indicator, perm)
      vals.append(val)
    worst_case_val = min(vals)
    worst_case_perm = perms[vals.index(worst_case_val)]
    order_text = '→'.join([str(i+1) for i in worst_case_perm])
    _log(1, f'ALG = {worst_case_val} [worst-case order {order_text}]')
    return worst_case_val, worst_case_perm


def _indent(str, l):
  return (l-1) * '║ ' + str


def solve(valuations: list[tuple[float, list[float]]],
          len_items: int,
          prices: list[float],
          order_oblivious: bool,
          debug: bool = False,
          silent: bool = False):
  for i, val in enumerate(valuations):
    condition = abs(sum([prob for prob, _ in val]) - 1) < 1e-12
    assert condition, f'v{i+1}\'s probabilities should sum to 1'
  
  global BUNDLE_NAMES, PRICE_CACHE, VALUATIONS_CACHE, OPT_CACHE, PRIORITY
  BUNDLE_NAMES = possible_bundles_names(len_items)

  if not silent:
    if debug:
      PRIORITY = 1
    else:
      PRIORITY = 0

  price_status = 'posted prices' if prices is not None else 'no posted prices'
  order_oblivious_status = 'order-oblivious' if order_oblivious else 'fixed order'
  _log(0, f'{len(valuations)} agents, {len_items} items, {price_status}, {order_oblivious_status}')
  indicator = item_indicator(len_items)

  if VALUATIONS_CACHE != valuations:
    OPT_CACHE = _compute_opt(valuations, indicator)
  opt_val, possible_attr = OPT_CACHE

  if prices == 'auto':
    assert len_items == 2, "auto pricing only implemented for 2 items"
    # Players reordering phase
    opt_attr = possible_attr[0][1]
    reordering = []
    if 3 in opt_attr:
      reordering.append(opt_attr.index(3))
      for i in range(len(opt_attr)):
        if i != reordering[0]:
          reordering.append(i)
    else:
      idx1, idx2 = opt_attr.index(1), opt_attr.index(2)
      reordering.append(idx1)
      reordering.append(idx2)
      for i, _ in enumerate(opt_attr):
        if i != idx1 and i != idx2:
          reordering.append(i)
    
    valuations = [valuations[i] for i in reordering]
    opt_attr = [opt_attr[i] for i in reordering]

    # Pricing phase
    eps = 1e-9
    if opt_attr[0] == 3:
      prices = [
        valuations[0][0][1][3] - valuations[0][0][1][2] - eps,
        valuations[0][0][1][3] - valuations[0][0][1][1] - eps
      ]
    elif valuations[0][0][1][1] < valuations[1][0][1][1] and valuations[0][0][1][2] < valuations[1][0][1][2]:
      max_next_b = max([valuations[i][0][1][2] for i in range(2, len(valuations))] + [0])
      prices = [valuations[0][0][1][1] - eps, max(valuations[0][0][1][2], max_next_b) + eps]
    else:
      max_next_a = max([valuations[i][0][1][1] for i in range(2, len(valuations))] + [0])
      prices = [max(valuations[1][0][1][1], max_next_a) + eps, valuations[1][0][1][2] - eps]
    
    _log(0, f'Automatic prices {prices}')

  if prices is not None:
    PRICE_CACHE = []
    len_bundles = len(BUNDLE_NAMES)
    if len(prices) == len_items:
      for b in range(len_bundles):
        PRICE_CACHE.append(_compute_price_first(prices, b, indicator))
    elif len(prices) == len_bundles:
      PRICE_CACHE = prices.copy()
    else:
      raise ValueError("wrong size for prices array")

  alg_val, worst_case_perm = _compute_alg(valuations, prices, order_oblivious, indicator)
  _log(0, f'ALG(p) = {alg_val:2f}, OPT = {opt_val:2f} [ratio = {alg_val/opt_val*100:2f}%]')

  if opt_val == 0:
    score = 1
  else:
    score = alg_val/opt_val
  
  return_dict = {
    "optimal_bundles": possible_attr,
    "alg_val": alg_val,
    "opt_val": opt_val,
    "score": score,
    "prices": prices,
    "worst_case_order": worst_case_perm
  }

  VALUATIONS_CACHE = valuations.copy()
  
  return return_dict


def search_prices(VV, mm, method, lazy = False, grid_points = 50, lazy_thres=2/3):
  global TAG
  assert method in ['brute', 'thresholds']
  if method == 'brute':
    raise ValueError('not supported yet')
    prices_grid = grid_gen(0, 1, grid_points, mm)
  elif method == 'thresholds':
    prices_grid = thres_grid_gen(VV, mm)

  max_score = 0
  argmax_prices = None
  argmax_order = None
  for price in tqdm(prices_grid):
    result = solve(valuations = VV,
                   len_items = mm,
                   prices = price,
                   order_oblivious = True,
                   silent = True)
    score = result["score"]
    
    if score > max_score:
      max_score = score
      argmax_prices = price
      argmax_order = result["worst_case_order"]

    if lazy and score > lazy_thres:
      break
  
  TAG = argmax_order
  score = solve(valuations = VV,
                len_items = mm,
                prices = argmax_prices,
                order_oblivious = True,
                debug = True)["score"]

  print(f'{max_score*100:2f}% score achieved with prices {argmax_prices}')