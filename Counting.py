import os
from operator import itemgetter

urls = [
  "http://www.google.com/a.txt",
  "http://www.google.com.tw/a.txt",
  "http://www.google.com/download/c.jpg",
  "http://www.google.co.jp/a.txt",
  "http://www.google.com/b.txt",
  "https://facebook.com/move/b.txt",
  "http://yahoo.com/123/000/c.jpg",
  "http://gliacloud.com/haha.jpg"
]

couting = {}

for url in urls:
  fname  = os.path.basename(url)
  try:
    couting[fname] += 1
  except:
    couting[fname] = 1

sortedF = sorted(couting.items(), key=itemgetter(1))
for fname in sortedF[:-4:-1]:
  print fname[0], fname[1]