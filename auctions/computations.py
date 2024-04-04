from itertools import product, permutations
from .utils import len_possible_bundles, item_indicator, possible_bundles_names
from math import prod
import logging


BUNDLE_NAMES = None


def _possible_next_moves(list_taken: list[bool], 
                         indicator: list[list[int]]) -> list[int]:
  impossible_next = set()
  for item, taken in enumerate(list_taken):
    if taken:
      for j in indicator[item]:
        impossible_next.add(j)
  len_bundles = max([max(l) for l in indicator]) + 1
  possible_next = []
  for i in range(len_bundles):
    if not i in impossible_next:
      possible_next.append(i)
  return possible_next


def _compute_price(prices: list[float], attr: int,
                   indicator: list[list[int]]) -> float:
  total_price = 0
  for i, p in enumerate(prices):
    if attr in indicator[i]:
      total_price += p
  return total_price


def _player_utility_of_move(deterministic_valuation: list[float],
                     prices: list[float], move: int, indicator: list[list[int]]) -> float:
  return deterministic_valuation[move] - _compute_price(prices, move, indicator)


def _indices_of(lst, value):
  indices = [i for i, x in enumerate(lst) if x == value]
  return indices


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
                          prices: list[float],
                          list_taken: list[bool], indicator: list[list[int]]) -> tuple[int, float]:
  possible_next = _possible_next_moves(list_taken, indicator)
  player_utilities = []
  for move in possible_next:
    player_utility = _player_utility_of_move(deterministic_valuation, prices, move, indicator)
    player_utilities.append(player_utility)
  best_player_utility = max(player_utilities)
  idxes = _indices_of(player_utilities, best_player_utility)
  return [possible_next[i] for i in idxes]


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
  logging.debug(f'Computing OPT:')
  total_expected_val = 0
  sample_space = product(*[list(range(len(v))) for v in valuations])
  for possibility in sample_space:
    probability = prod(valuation[possibility[i]][0] for i, valuation in enumerate(valuations))
    logging.debug(f'  Sample space {possibility} [p = {100*probability:2f}%]:')
    deterministic_valuations = [valuation[possibility[i]][1] for i, valuation in enumerate(valuations)]
    attr, welfare = _explore_opt(deterministic_valuations, [False] * len(indicator), indicator)
    attr_text = '(' + ', '.join([BUNDLE_NAMES[j] for j in attr]) + ')'
    logging.debug(f'  OPT = {welfare} [attribution = {attr_text}]')
    total_expected_val += probability * welfare
  return total_expected_val


def _explore_alg(V, prices, list_taken, indicator, sig, N=1):
  if len(V) == 0:
    return 0
  
  sum = 0
  head, tail = V[0], V[1:]
  for proba, deter_v_head in head:
    logging.debug(_indent(f'Agent {sig[N-1]+1} chooses valuation {deter_v_head} [proba = {proba*100:2f}%]', N))
    if prices is not None:
      possible_next = _utility_maximizing_moves(deter_v_head, prices, list_taken, indicator)
    else:
      possible_next = _possible_next_moves(list_taken, indicator)
    
    extrval = 1e12 if prices is not None else 0
    for move in possible_next:
      list_taken_next = _update_list_taken(list_taken, move, indicator, inplace=False)
      welfare_move = deter_v_head[move]
      logging.debug(_indent(f'* {sig[N-1]+1} buys {BUNDLE_NAMES[move]}, added_welfare = {welfare_move}', N))
      welfare_next = _explore_alg(tail, prices, list_taken_next, indicator, sig, N+1)
      welfare_branch = welfare_move + welfare_next
      extrval = min(welfare_branch, extrval) if prices is not None else max(welfare_branch, extrval)

      # EXPLANATION: if there are posted prices, agent has the choice & may provoke the worst-case scenario
      # if generic algorithm, we can choose the best option!
    sum += extrval * proba
  
  return sum


def _compute_alg(valuations, prices: list[float],
                 order_oblivious: bool, indicator: list[list[int]]) -> tuple[list[int], float]:
  len_agents = len(valuations)
  logging.debug(f'Computing ALG:')
  if not order_oblivious:
    list_taken = [False] * len(indicator)
    return _explore_alg(valuations, prices, list_taken, indicator, tuple(range(len_agents)))
  else:
    vals, perms = [], list(permutations(range(len_agents)))
    for perm in perms:
      order_text = '→'.join([str(i+1) for i in perm])
      logging.debug(_indent(f'Testing order {order_text}:', 1))
      list_taken = [False] * len(indicator)
      val = _explore_alg([valuations[i] for i in perm], prices, list_taken, indicator, perm)
      vals.append(val)
    worst_case_val = min(vals)
    worst_case_perm = perms[vals.index(worst_case_val)]
    order_text = '→'.join([str(i+1) for i in worst_case_perm])
    logging.debug(f'ALG = {worst_case_val} [worst-case order {order_text}]')
    return worst_case_val


def _indent(str, l):
  return l * '| ' + str


def solve(valuations: list[tuple[float, list[float]]],
          len_items: int,
          prices: list[float],
          order_oblivious: bool,
          debug: bool = False,
          silent: bool = False):
  
  global BUNDLE_NAMES
  BUNDLE_NAMES = possible_bundles_names(len_items)

  if not silent:
    if debug:
      logging.basicConfig(level=logging.DEBUG)
    else:
      logging.basicConfig(level=logging.INFO)

  price_status = 'posted prices' if prices is not None else 'no posted prices'
  order_oblivious_status = 'order-oblivious' if order_oblivious else 'fixed order'
  logging.info(f'{len(valuations)} agents, {len_items} items, {price_status}, {order_oblivious_status}')
  indicator = item_indicator(len_items)
  opt_val = _compute_opt(valuations, indicator)
  alg_val = _compute_alg(valuations, prices, order_oblivious, indicator)
  logging.info(f'ALG(p) = {alg_val:2f}, OPT = {opt_val:2f} [ratio = {alg_val/opt_val*100:2f}%]')

  if opt_val == 0:
    return 1
  else:
    return alg_val/opt_val