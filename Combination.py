def func_c (n, r):
  if r == 1:
    return n
  if n == r:
    return 1
  return func_c (n - 1, r) + func_c (n - 1, r - 1)

print func_c (990, 33)