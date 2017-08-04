#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import csv

print "Argument number:", len(sys.argv)
print "Convert file:", sys.argv[1]

#spamReader = csv.reader(open('MI_INDEX_oldtsec.19900104.utf8.csv', 'rb'), delimiter=',', quotechar='\"')
spamReader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',', quotechar='\"')

def str2num(s):
    s = s.replace(',', '')
    #return (s.isa1num() and str(s) or "." in s and [float(s)] or [int(s)] )[0]
    try:
        return ("." in s and [float(s)] or [int(s)] )[0]
    except:
        return s

def removeCommon(s):
    return s.replace(',', '')

seed = 1

for row in spamReader:
    print 'ROW:', seed, row
    seed += 1

    row = map(str.lstrip, row)
    row = map(removeCommon, row)
    print '|'.join(row)

    # row = map(str2num, row)
    # print row

num = ['1','2','3','4','123.4', 'a', '12,345', '單位', '', '+']

ff = map(str2num, num)
print ff

aa = ' 123'
print aa.isdigit()
