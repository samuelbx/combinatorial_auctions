from .utils import possible_bundles

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
