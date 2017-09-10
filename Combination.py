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
for r_ in list(xrange(1,50)):
  for n_ in list(xrange(r_,1000)):

    try:
      a = cache[(n_, r_)]
    except:
      cache[(n_, r_)] = func_c (n_, r_)

def Combination (n, r):

  a = 1
  b = 1
  c = 1
  for idx in xrange(1, n + 1):
    c = c * idx
    if idx == r:
      a = c
    if idx == n - r:
      b = c
  return c / (a * b)

print func_c (1000, 50)
print Combination (1000, 50)
