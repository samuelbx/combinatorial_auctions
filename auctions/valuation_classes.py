from .utils import possible_bundles
from random import random
from math import log2

def gen_additive(objvals: tuple[float]):
  v = []
  for bundle in possible_bundles(len(objvals)):
    v.append(sum([objvals[idx] for idx in bundle]))
  return v

def gen_zero(M: float):
  return gen_additive([0]*M)

def gen_subadditive(objvals: tuple[float]):
  assert len(objvals) == 3
  va, vb, vc = objvals
  return [0, va, vb, vc, max(va, vb), max(va, vc), max(vb, vc), max(va+vb, va+vc, vb+vc)]

def gen_xos(list_additive_objvals: tuple[tuple[float]]):
  additive_vals = [gen_additive(objvals) for objvals in list_additive_objvals]
  return [max([additive_vals[i][j] for i in range(len(list_additive_objvals))]) for j in range(len(additive_vals[0]))]

def gen_rand_xos(len_players, len_items):
  VV = []
  for i in range(len_players):
    base_funs = []
    for k in range(2):
      base_funs.append([random() for _ in range(len_items)])
    VV.append([(1, gen_xos(base_funs))])
  return VV

def _dot(x: list[int], y: list[int]):
  S = 0
  for a, b in zip(x, y):
    S += a * b
  return S

def _included(X: set, S: list[set], list_taken: list[int]):
  s = set()
  return X.issubset(s.union(*[S[x] for x in list_taken]))

def _min_union_search(X, S, list_taken):
  m = len(S)
  if _included(X, S, list_taken):
    return len(list_taken)
  minval = 1e12
  start = 0
  if len(list_taken) != 0:
    start = list_taken[-1] + 1
  for x in range(start, m):
    minval = min(minval, _min_union_search(X, S, list_taken + [x]))

  return minval

def gen_subadd_set_cover(m: int, tol: float = 1e-6):
  k = log2(float(m) + 1)
  assert abs(k - int(k)) < tol, "m must be of the form 2^k-1"
  assert k < 12, "it might bug"

  bin_repr = []
  for nb in range(1, m+1):
    bin_repr.append([int(x) for x in format(nb, "#016b")[2:]])
  
  S = []
  for bin_i in bin_repr:
    Si = set()
    for j, bin_j in enumerate(bin_repr):
      if _dot(bin_i, bin_j) % 2 == 1:
        Si.add(j)
    S.append(Si)
  
  v = []
  for bundle in possible_bundles(m):
    items = set()
    for item in bundle:
      items.add(item)
    v.append(_min_union_search(items, S, []))
  
  return v
