#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
# The original data is download from...
# http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX_oldtsec.php
#

##########################################################################
# Public Library
##########################################################################
import urllib
import sys

import csv
from datetime import date
from datetime import timedelta

##########################################################################
# Private Library
##########################################################################
import html2csv
from TwseConfig import *

##########################################################################
# Private Varaible
##########################################################################
parser = html2csv.html2csv()

##########################################################################
# Private Fuction
##########################################################################
#
# Try OldDownloadTry to check if varid data
#
def TwseOldDownloadTry(filename, date_s):

    try:
        # string: "琩礚戈" (BIG5)
        base_str = '\xac\x64\xb5\x4c\xb8\xea\xae\xc6'
        ret_value = True;

        # 1st stage
        # Download from TWSE and save to csv file

        # param = urllib.urlencode({'input_date': date_s, 'select2': 'MS'} )
        param = urllib.urlencode({'input_date': date_s, 'select2': ''} )
        f_url = urllib.urlopen("http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX_oldtsec.php", param)

        f_write = open(filename, 'w+b')

        data = f_url.read(8192)
        while data:
            parser.feed( data )
            f_write.write(parser.getCSV())
            data = f_url.read(8192)

        f_url.close()
        f_write.close()

        # 2nd stage
        # read csv file and read row 8 to check if varid data

        f_read = open(filename, 'rb')
        csvReader = csv.reader(f_read, delimiter=',', quotechar='\"')

        seed = 0
        for row in csvReader:
            seed += 1
            if seed == 8:
                ret_value = not (base_str in row[0])
                break;

        f_read.close

        return ret_value

    except:
      raise
      return False

#
# TwseOldDownload: to download all stock date
#
def TwseOldDownload(filename, date):

    date_s = '%(p0)02d/%(p1)02d/%(p2)02d' % \
        {"p0":date.year - 1911, "p1":date.month, "p2":date.day}
    return TwseOldDownloadTry(filename, date_s)

#
# TwseOldparsing: to parsing each company data
#
def TwseOldparsing(DstFolder, filename, date):

    print >> sys.stderr, "Process ", date, "data"

    idx = [[], [], []]

    #
    # Read database 00_INDEX.csv
    #
    f_idx = open(gTwseWorkDirInformIndex, 'rb')
    csvReader = csv.reader(f_idx, delimiter=',', quotechar='\"')
    try:
        idx[0] = csvReader.next()
        idx[1] = csvReader.next()
        idx[2] = csvReader.next()
    except:
        idx[0] = []
        idx[1] = []
        idx[2] = []
    f_idx.close()

    # string: "害禴才腹弧" (BIG5)
    base_str = '\xba\xa6\xb6\x5e\xb2\xc5\xb8\xb9\xbb\xa1\xa9\xfa'

    f_src = open(filename, 'rb')
    csvReader = csv.reader(f_src, delimiter=',', quotechar='\"')

    seed = 0
    for row in csvReader:

        seed += 1
        if seed <= 41:
            continue;

        if (base_str in row[0]):
            break;

        DstFName = DstFolder + '/' + row[0] + '-' + row[1]
        DstName = row[0] + '-' + row[1]
        if os.path.isdir(DstFName) == False:
            os.makedirs(DstFName)

            if row[0] in idx[0]:
                print >> sys.stderr, "WARNNING: ", row[0], "Exist(", row[1], ")"
            if row[1] in idx[1]:
                print >> sys.stderr, "WARNNING: ", row[1], "Exist(", row[0], ")"

            idx[0].append(row[0]);
            idx[1].append(row[1]);
            idx[2].append(DstName);

        SInfo = []
        SInfo.append(int(row[2].replace(',','')))   # Θユ眎计
        SInfo.append(int(row[3].replace(',','')))   # Θユ掸计
        SInfo.append(int(row[4].replace(',','')))   # Θユ肂
        SInfo.append(row[5])                        # 秨絃基
        SInfo.append(row[6])                        # 程蔼基
        SInfo.append(row[7])                        # 程基
        SInfo.append(row[8])                        # Μ絃基
        SInfo.append(row[9])                        # +/-
        SInfo.append(row[10])                       # 害禴基畉
        SInfo.append(row[11])                       # 程处ボ禦基
        SInfo.append(0)                             # 程处ボ禦秖
        SInfo.append(row[12])                       # 程处ボ芥基
        SInfo.append(0)                             # 程处ボ芥秖
        SInfo.append(row[13])                       # セ痲ゑ

        DstDateName = DstFName + "/" + str(date.toordinal()) + ".csv"
        with open(DstDateName, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(SInfo)

    f_src.close

    with open(gTwseWorkDirInformIndex, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(idx)

##########################################################################
# program Entry for test
##########################################################################
if __name__== "__main__":

    print >> sys.stderr, 'Main'

    #
    # This day is close
    #
    print >> sys.stderr, 'TwseOldDownload date:', date(2000, 1, 9)
    if TwseOldDownload(gTwseWorkDirTemp + '/tmpClose.csv', date(2000, 1, 9)) == True:
        print >> sys.stderr, True
    else:
        print >> sys.stderr, False

    #
    # This day is open
    #

    if os.path.exists(gTwseWorkDirInformIndex):
        print >> sys.stderr, '  File', gTwseWorkDirInformIndex, 'exist'
    else:
        open(gTwseWorkDirInformIndex, 'a').close()

    print >> sys.stderr, 'TwseOldDownload date:', date(2000, 1, 10)
    if TwseOldDownload(gTwseWorkDirTemp + '/tmpOpen.csv', date(2000, 1, 10)) == True:
        print >> sys.stderr, True
        TwseOldparsing(gTwseWorkDirInform, gTwseWorkDirTemp + '/tmpOpen.csv', date(2000, 1, 10))
    else:
        print >> sys.stderr, False

    if False:
      #
      # This day is open
      #
      print >> sys.stderr, 'TwseOldDownload date:', date(2000, 1, 11)
      if TwseOldDownload(gTwseWorkDirTemp + '/tmpOpen2.csv', date(2000, 1, 11)) == True:
          print >> sys.stderr, True
      else:
          print >> sys.stderr, False

