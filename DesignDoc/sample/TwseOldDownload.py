#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

params = urllib.urlencode({'input_date': '89/01/08', 'select2': 'MS'} )

f = urllib.urlopen("http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX_oldtsec.php", params)
print f.read()

# end
