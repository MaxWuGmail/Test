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
# Phase 0: ����89�~1��4��
# Phase 1: ����93�~2��11��
TWSE_PHASE = [  [date(2000, 1,  4), date(2004, 2, 10)],     # �®榡��TWSE���,�u��HTML�榡
                [date(2004, 2, 11), date.today()]]          # �s�榡��TWSE���,���]�tCSV�榡

#
# �W����T�U������ Pahse 1
#
TWSE_STOCK_URLP1 = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX2_print.php?genpage=genpage'

#
# �W���Ѳ����� Pahse 1
#
TWSE_STOCK_IDENP1 = [['MS',          'Market Summary',                   '�j�L�έp��T'],
                   ['ALLBUT0999_1','All (no Warrant)',                 '����(���t�v��)'],
                   ['0049',        'Beneficiary Certificates',         '�ʳ������'],
                   ['0099P',       'ETF',                              'ETF'],
                   ['019919T',     'REITs',                            '���q�Ҩ�'],
                   ['0999',        'Warrant (call)',                   '�{���v��'],
                   ['0999P',       'Warrant (Put)',                    '�{���v��'],
                   ['0999GA',      'Preferred Stock With Warrants',    '���{���v�S�O��'],
                   ['0999GD',      'Bond With Warrants',               '���{���v���q��'],
                   ['0999G9',      'Company Warrants',                 '�{���v����'],
                   ['01',          'Cement',                           '���d�u�~'],
                   ['02',          'Food',                             '���~�u�~'],
                   ['03',          'Plastic',                          '�콦�u�~'],
                   ['04',          'Textile',                          '��´�ֺ�'],
                   ['05',          'Electric,Machinery',               '�q������'],
                   ['06',          'Electrical and Cable',             '�q���q�l'],
                   ['07',          'Chemical, Biotechnology, and Medical Care Industry',   '�ƾǥͧ�����'],
                   ['21',          'Chemical Industry',                '�ƾǤu�~'],
                   ['22',          'Biotechnology and Medical Care Industry',      '�ͧ������~'],
                   ['08',          'Glass and Ceramic',                '��������'],
                   ['09',          'Paper and Pulp',                   '�y�Ȥu�~'],
                   ['10',          'Iron and Steel',                   '���K�u�~'],
                   ['11',          'Rubber',                           '�󽦤u�~'],
                   ['12',          'Automobile',                       '�T���u�~'],
                   ['13',          'Electronic',                       '�q�l�u�~'],
                   ['24',          'Semiconductor Industry',           '�b����~'],
                   ['25',          'Computer and Peripheral Equipment Industry',   '�q���ζg��]�Ʒ~'],
                   ['26',          'Optoelectronic Industry',          '���q�~'],
                   ['27',          'Communications and Internet Industry',         '�q�H�����~'],
                   ['28',          'Electronic Parts/Components Industry',         '�q�l�s�ե�~'],
                   ['29',          'Electronic Products Distribution Industry',    '�q�l�q���~'],
                   ['30',          'Information Service Industry',     '��T�A�ȷ~'],
                   ['31',          'Other Electronic Industry',        '��L�q�l�~'],
                   ['14',          'Building Material and Construction',           '�ا���y'],
                   ['15',          'Shipping and Transportation',      '��B�~'],
                   ['16',          'Tourism',                          '�[���Ʒ~'],
                   ['17',          'Financial and Insurance',          '���īO�I'],
                   ['18',          'Trading and Consumers\' Goods Industry',       '�T���ʳf'],
                   ['9299',        'TDR',                              '�s�U����'],
                   ['23',          'Oil, Gas and Electricity Industry','�o�q�U��~'],
                   ['19',          'General',                          '��X'],
                   ['20',          'Other Industry',                   '��L'],
                   ['CB',          'Convertible Bond',                 '�i�ഫ���q��'],
                   ['ALL',         'ALL',                              '����'], ]
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

