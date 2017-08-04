cache = {}

def func_c (n, r):
  if r == 1:
    return n
  if n == r:
    return 1
  try:
    return cache[(n, r)]
  except:
    return func_c (n - 1, r) + func_c (n - 1, r - 1)

#
# Building cache first
#
for r_ in list(xrange(1,33)):
  for n_ in list(xrange(r_,990)):

    try:
      a = cache[(n_, r_)]
    except:
      cache[(n_, r_)] = func_c (n_, r_)

print func_c (990, 33)
