#!/usr/bin/python
# -*- coding: UTF-8 -*-

##########################################################################
# Public Library
##########################################################################
import ConfigParser
import sys, os
from datetime import date

##########################################################################
# Public Global variable
##########################################################################
#
# Global variable for marking the directory and files
#
gTwseWorkDirRoot        = '../..'
gTwseWorkDirDwonload    = gTwseWorkDirRoot + '/opt/download/twse'
gTwseWorkDirInform      = gTwseWorkDirRoot + '/opt/tswe'
gTwseWorkDirInformIndex = gTwseWorkDirInform + '/00_INDEX.csv'

gTwseWorkDirTemp        = gTwseWorkDirRoot + '/tmp'

gTwseCfgDirectory       = gTwseWorkDirRoot + '/etc'
gTwseCfgFile            = gTwseCfgDirectory + '/TwseConfig.ini'

#
# Configuration file settings
#
gTwseCfgDateSection     = 'DATE SECTION'
gTwseCfgDateDownload    = 'DownloadDate'

gTwseCfgFileSection     = 'FILE SECTION'
gTwseCfgFileRoot        = 'FileRoot'
gTwseCfgFileDwonload    = 'DownloadFile'

gTwseConfig = ConfigParser.RawConfigParser()

#
# Global variable for marking the last download date, items
#
gTwseDwonloadDate = date(2000, 1, 4)
gTwseDownloadItem = 0

#
# Each phase of each download form site
#
# Phase 0: 民國89年1月4號
# Phase 1: 民國93年2月11號
TWSE_PHASE = [  [date(2000, 1,  4), date(2004, 2, 10)],     # 舊格式的TWSE資料,只有HTML格式
                [date(2004, 2, 11), date.today()]]          # 新格式的TWSE資料,有包含CSV格式

#
# 上市資訊下載網站 Pahse 1
#
TWSE_STOCK_URLP1 = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX2_print.php?genpage=genpage'

#
# 上市股票分類 Pahse 1
#
TWSE_STOCK_IDENP1 = [['MS',          'Market Summary',                   '大盤統計資訊'],
                   ['ALLBUT0999_1','All (no Warrant)',                 '全部(不含權證)'],
                   ['0049',        'Beneficiary Certificates',         '封閉式基金'],
                   ['0099P',       'ETF',                              'ETF'],
                   ['019919T',     'REITs',                            '受益證券'],
                   ['0999',        'Warrant (call)',                   '認購權證'],
                   ['0999P',       'Warrant (Put)',                    '認售權證'],
                   ['0999GA',      'Preferred Stock With Warrants',    '附認股權特別股'],
                   ['0999GD',      'Bond With Warrants',               '附認股權公司債'],
                   ['0999G9',      'Company Warrants',                 '認股權憑證'],
                   ['01',          'Cement',                           '水泥工業'],
                   ['02',          'Food',                             '食品工業'],
                   ['03',          'Plastic',                          '塑膠工業'],
                   ['04',          'Textile',                          '紡織纖維'],
                   ['05',          'Electric,Machinery',               '電機機械'],
                   ['06',          'Electrical and Cable',             '電器電纜'],
                   ['07',          'Chemical, Biotechnology, and Medical Care Industry',   '化學生技醫療'],
                   ['21',          'Chemical Industry',                '化學工業'],
                   ['22',          'Biotechnology and Medical Care Industry',      '生技醫療業'],
                   ['08',          'Glass and Ceramic',                '玻璃陶瓷'],
                   ['09',          'Paper and Pulp',                   '造紙工業'],
                   ['10',          'Iron and Steel',                   '鋼鐵工業'],
                   ['11',          'Rubber',                           '橡膠工業'],
                   ['12',          'Automobile',                       '汽車工業'],
                   ['13',          'Electronic',                       '電子工業'],
                   ['24',          'Semiconductor Industry',           '半導體業'],
                   ['25',          'Computer and Peripheral Equipment Industry',   '電腦及週邊設備業'],
                   ['26',          'Optoelectronic Industry',          '光電業'],
                   ['27',          'Communications and Internet Industry',         '通信網路業'],
                   ['28',          'Electronic Parts/Components Industry',         '電子零組件業'],
                   ['29',          'Electronic Products Distribution Industry',    '電子通路業'],
                   ['30',          'Information Service Industry',     '資訊服務業'],
                   ['31',          'Other Electronic Industry',        '其他電子業'],
                   ['14',          'Building Material and Construction',           '建材營造'],
                   ['15',          'Shipping and Transportation',      '航運業'],
                   ['16',          'Tourism',                          '觀光事業'],
                   ['17',          'Financial and Insurance',          '金融保險'],
                   ['18',          'Trading and Consumers\' Goods Industry',       '貿易百貨'],
                   ['9299',        'TDR',                              '存託憑證'],
                   ['23',          'Oil, Gas and Electricity Industry','油電燃氣業'],
                   ['19',          'General',                          '綜合'],
                   ['20',          'Other Industry',                   '其他'],
                   ['CB',          'Convertible Bond',                 '可轉換公司債'],
                   ['ALL',         'ALL',                              '全部'], ]
# TWSE_STOCK_IDENP1

#
# Function for create directory
#
def TwseDirectoryCreate():

    #
    # create necessiry directory
    #
    #try:
    if os.path.isdir(gTwseCfgDirectory):
        print >> sys.stderr, '  Directory', gTwseCfgDirectory, 'exist'
    else:
        os.makedirs(gTwseCfgDirectory)

    if os.path.isdir(gTwseWorkDirInform):
        print >> sys.stderr, '  Directory', gTwseWorkDirInform, 'exist'
    else:
        os.makedirs(gTwseWorkDirInform)

    if os.path.exists(gTwseWorkDirInformIndex):
        print >> sys.stderr, '  File', gTwseWorkDirInformIndex, 'exist'
    else:
        open(gTwseWorkDirInformIndex, 'a').close()

    if os.path.isdir(gTwseWorkDirDwonload):
        print >> sys.stderr, '  Directory', gTwseWorkDirDwonload, 'exist'
    else:
        os.makedirs(gTwseWorkDirDwonload)

    if os.path.isdir(gTwseWorkDirDwonload):
        print >> sys.stderr, '  Directory', gTwseWorkDirTemp, 'exist'
    else:
        os.makedirs(gTwseWorkDirTemp)

# TwseDirectoryCreate

