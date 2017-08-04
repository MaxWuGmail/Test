#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import date

TWSE_URL = 'http://www.twse.com.tw/'
TWSE_OLD = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX_oldtsec.php?input_date=100/09/07&status=1'

ArrayTest = [1, 2, 3, 4, 5]

#
# Unit test main
#
if __name__ == "__main__":
    print TWSE_URL

    print ArrayTest
    print ArrayTest[0]
    Array2 = ArrayTest
    Array2.append(100)
    print 19 in Array2
    print date.today()