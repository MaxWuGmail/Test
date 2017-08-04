#!/usr/bin/python
# -*- coding: UTF-8 -*-
programname = 'TwseIsinIndex - version 2013-04-15'

####################################################################
# Public Libary
####################################################################
import sys, getopt, os.path, glob, HTMLParser, re, urllib
import shutil, csv
from datetime import datetime

try:    import psyco ; psyco.jit()
except: pass

####################################################################
# Private Libary
####################################################################
import html2csv

####################################################################
# TWSE ISIN and Quote index convert class
# From HTML file to CSV file
####################################################################
class TwseIsinSrc2Csv(html2csv.html2csv):

    #
    # Class initial function
    #
    def __init__(self):

        html2csv.html2csv.__init__(self)
        self.QuoteClass = 'QuoteClass'

    #
    # Process HTML <TR> tag
    #
    def start_tr(self):

        self.TmpRow = ''
        if self.inTR: self.end_tr()  # <TR> implies </TR>
        self.inTR = 1


    #
    # Process HTML </TR> tag
    #
    def end_tr(self):

        if self.inTD: self.end_td()  # </TR> implies </TD>
        self.inTR = 0
        if len(self.CSVrow) > 0:
            if len(self.CSVrow.split(',')) > 2:
                self.CSV += self.CSVrow[:-1]
                self.CSV += ',' + self.QuoteClass
                self.CSV += '\n'
            elif len(self.CSVrow.split(',')) == 2:
                self.QuoteClass = self.CSVrow.split(',')[0]
        self.CSVrow = ''
        self.rowCount += 1

    #
    # Process HTML <TD> tag
    #
    def start_td(self):

        if not self.inTR: self.start_tr() # <TD> implies <TR>
        self.CSVrow += ''
        self.inTD = 1

    #
    # Process HTML </TD> tag
    #
    def end_td(self):

        if self.inTD:
            self.CSVrow += ','  
            self.inTD = 0

    #
    # Process Index data in TD
    #
    def handle_data(self, data):

        if self.inTD:
            TmpRow =                                            \
              self.re_multiplespaces.sub(' ',
                                         data.replace('\t',' ').
                                         replace('\n','').
                                         replace('\r','').
                                         replace(' ','').
                                         replace('\xa1\x40',',')
                                        )
            # 有價證券代號及名稱
            if '\xa6\xb3\xbb\xf9\xc3\xd2\xa8\xe9\xa5\x4e\xb8\xb9\xa4\xce\xa6\x57\xba\xd9' in TmpRow:
                TmpRow = 'QuoteCode,QuoteName'
            # 國際證券辨識號碼(ISINCode)
            if '\xb0\xea\xbb\xda\xc3\xd2\xa8\xe9\xbf\xeb\xc3\xd1\xb8\xb9\xbdX' in TmpRow:
                TmpRow = 'QuoteIsin'
            # 上市日
            if '\xa4W\xa5\xab\xa4\xe9' in TmpRow:
                TmpRow = 'ListDate'
            # 市場別
            if '\xa5\xab\xb3\xf5\xa7O' in TmpRow:
                TmpRow = 'MarketC'
            # 產業別
            if '\xb2\xa3\xb7~\xa7O' in TmpRow:
                TmpRow = 'IndustC'
            # 備註
            if '\xb3\xc6\xb5\xf9' in TmpRow:
                TmpRow = 'QuoteNote'
            self.CSVrow += TmpRow

    #
    # CSV data output
    #
    def getCSV(self,purge=False):

        if purge and self.inTR: self.end_tr()
        dataout = self.CSV[:]
        self.CSV = ''
        return dataout

####################################################################
# TWSE ISIN and Quote index download class
####################################################################
class TwseIsinIndex:

    #
    # Class initial function
    #
    def __init__(self):

        self.UrlLocat   = '' # Array
        self.MetaHtml   = 'IsinMeta.html'
        self.MetaCsv    = 'IsinMeta.csv'
        self.IsinBackup = 'IsinBackup.csv'
        self.IsinFile   = '' # ['IsinMain.csv', 'IsinRemove.csv']
        self.CfgPath    = './'
        self.TmpPath    = './'
        self.DataPath   = './'

    #
    # Set Configuration Path
    #
    def CfgEnvSet(self, DataPath, CfgPath, TmpPath):

        self.CfgPath    = CfgPath
        self.TmpPath    = TmpPath
        self.DataPath   = DataPath

        self.MetaHtml   =  self.TmpPath + os.path.basename (self.MetaHtml)
        self.MetaCsv    =  self.TmpPath + os.path.basename (self.MetaCsv)
        self.IsinBackup =  self.DataPath + os.path.basename (self.IsinBackup)
        self.IsinFile   = [self.DataPath + os.path.basename (lFile) for lFile in self.IsinFile]

    #
    # Set URL name for getting ISIN data
    #
    def UrlLocatSet (self, UrlLocat):

        self.UrlLocat = UrlLocat

    #
    # Set ISIN index file for saving
    #
    def IsinFileSet (self, IsinFile):

        self.IsinFile = [self.DataPath + '/' + lFile for lFile in IsinFile]

    #
    # Convert ISIN html file to CSV meta file
    #
    def Html2MetaCsv (self):

        lParser = TwseIsinSrc2Csv()
        try:
            lHtmlFile = open(self.MetaHtml, 'rb')
            lCsvFile  = open(self.MetaCsv,  'wb')

            lData = lHtmlFile.read(8192)
            while lData:
                lParser.feed( lData )
                lCsvFile.write( lParser.getCSV() )
                lData = lHtmlFile.read(8192)

            lCsvFile.close()
            lHtmlFile.close()
        except:
            try:
                print 'Error converting %s        ' % self.MetaHtml
                lHtmlFile.close()
            except: pass
            try:
                print 'Error converting %s        ' % self.MetaCsv
                lCsvFile.close()
            except: pass

    #
    # Migrate meta CSV file into Isin index csv file
    #
    def CsvMigrate (self):

        try:
            lMetaFile = open(self.MetaCsv,     'rb')
            lIsinFile = open(self.IsinFile[0], 'ab')

            lMetaRows = csv.reader (lMetaFile, delimiter=',')
            lIsinW    = csv.writer (lIsinFile)

            for lRow in lMetaRows:
                lIsinW.writerow (lRow)


            lMetaFile.close ()
            lIsinFile.close ()
        except:
            print 'CsvMigrate Error'
            try:
                lMetaFile.close ()
            except: pass
            try:
                lIsinFile.close ()
            except: pass


    #
    # Save HTML data from TWSE into html meta file
    #
    def IsinUpdate (self):

        # Phase 1: Migrate Html file into CSV file
        try:
            shutil.move (self.IsinFile[0], self.IsinBackup)
        except: pass

        for lUrlLocat in self.UrlLocat:
            f_save = open (self.MetaHtml, 'wb')
            f_url  = urllib.urlopen(lUrlLocat)

            data = f_url.read(8192)
            while data:
                f_save.write(data)
                data = f_url.read(8192)

            f_url.close  ()
            f_save.close ()
            self.Html2MetaCsv ()
            self.CsvMigrate   ()

        try:
            os.remove (self.MetaCsv)
            os.remove (self.MetaHtml)
        except:
            print 'remove meta file fail'
            pass

        # Phase 2: remove redundant row
        shutil.move (self.IsinFile[0], self.MetaCsv)
        lIsinFile = open (self.IsinFile[0], 'wb')
        lMetaFile = open (self.MetaCsv, 'rb')

        lIsinRows = csv.writer (lIsinFile)
        lMetaRows = csv.reader (lMetaFile)
        lMetaHead = lMetaRows.next()
        lIsinRows.writerow (lMetaHead)

        for Row in lMetaRows:
            if Row[0] not in lMetaHead[0]:
                lIsinRows.writerow (Row)

        lMetaFile.close()
        lIsinFile.close()
        os.remove (self.MetaCsv)

        # Phase 3: select removed quotes
        try:
            lDQuoteFile = open(self.IsinFile[1], 'ab') # Removed file
            lMQuoteFile = open(self.IsinFile[0], 'rb') # Main file
            lBQuoteFile = open(self.IsinBackup,  'rb') # Backup File


            lDQuoteCsv  = csv.writer (lDQuoteFile)

            lMQuoteCsv  = csv.reader (lMQuoteFile)
            lMQuoteHead = lMQuoteCsv.next ()
            lMQuoteIdx  = [Row[2] for Row in lMQuoteCsv]

            lBQuoteCsv  = csv.reader (lBQuoteFile)
            lBQuoteCsv.next()
            for Row in lBQuoteCsv:
                if Row[2] not in lMQuoteIdx:
                    lDQuoteCsv.writerow(Row)

            lDQuoteFile.close ()
            lMQuoteFile.close ()
            lBQuoteFile.close ()

        except:
            print 'Select Removed quotes fail'
            pass
        
        try:
            os.remove (self.IsinBackup)
        except:
            print 'remove backup file fail'
            pass

    #
    # Open Isin File for qury Quote information
    # For performance issue, Quotes information is saved in system RAM
    #
    def IsinQueryOpen (self):

        self.IsinQueryFile = open (self.IsinFile[0], 'rb')
        self.IsinQueryCsv  = csv.reader (self.IsinQueryFile)
        self.IsinQueryHead = self.IsinQueryCsv.next ()
        self.IsinQueryDict = [lRow for lRow in
                                      csv.DictReader (self.IsinQueryFile,
                                                      self.IsinQueryHead)]

    #
    # Close Isin qury function
    #
    def IsinQueryClose (self):

        self.IsinQueryFile.close ()

    #
    # Query quote
    # Parameter:
    #   QuoteCode:  query quote by quote code
    #   QuoteCodeF: query quote by quote code in fuzzy
    #   QuoteName:  By quote name
    #   QuoteIsin:  By ISNI code
    #   ListDateEq: query quote by date (==)
    #   ListDateGt: query quote by date (>)
    #   ListDateGe: query quote by date (>=)
    #   ListDateLt: query quote by date (<)
    #   ListDateLe: query quote by date (<=)
    #   marketC:    query quote by Market class
    #   IndustC:    query quote by Industry class
    #   CFICode:    query quote by CFI code
    #   QuoteNote:  query note if args['QuoteNote'] is subset of Quote's note
    #
    # return:
    #   return in dictionary form
    #
    def IsinQueryQuote (self, **args):

        lRows = [Row for Row in self.IsinQueryDict]

        if args.has_key ('QuoteCodeF'):
            lRows = [Row for Row in lRows
                        if 0 == Row['QuoteCode'].find(args['QuoteCodeF'])]

        elif args.has_key ('QuoteCode'):
            lRows = [Row for Row in lRows
                        if Row['QuoteCode'] == args['QuoteCode']]

        if args.has_key ('QuoteName'):
            lRows = [Row for Row in lRows
                        if Row['QuoteName'] == args['QuoteName']]

        if args.has_key ('QuoteIsin'):
            lRows = [Row for Row in lRows
                        if Row['QuoteIsin'] == args['QuoteIsin']]

        if args.has_key ('ListDateEq'):
            lRows = [Row for Row in lRows
                        if Row['ListDate'] == args['ListDateEq']]

        elif args.has_key ('ListDateGt'):
            ArgD = datetime.strptime(args['ListDateGt'], '%Y/%m/%d')
            tRow = []
            for Row in lRows:
                CmpD = datetime.strptime(Row['ListDate'], '%Y/%m/%d')
                if CmpD > ArgD:
                    tRow.append (Row)
            lRows = tRow

        elif args.has_key ('ListDateGe'):
            ArgD = datetime.strptime(args['ListDateGt'], '%Y/%m/%d')
            tRow = []
            for Row in lRows:
                CmpD = datetime.strptime(Row['ListDate'], '%Y/%m/%d')
                if CmpD >= ArgD:
                    tRow.append (Row)
            lRows = tRow

        elif args.has_key ('ListDateLt'):
            ArgD = datetime.strptime(args['ListDateGt'], '%Y/%m/%d')
            tRow = []
            for Row in lRows:
                CmpD = datetime.strptime(Row['ListDate'], '%Y/%m/%d')
                if CmpD < ArgD:
                    tRow.append (Row)
            lRows = tRow

        elif args.has_key ('ListDateLe'):
            ArgD = datetime.strptime(args['ListDateGt'], '%Y/%m/%d')
            tRow = []
            for Row in lRows:
                CmpD = datetime.strptime(Row['ListDate'], '%Y/%m/%d')
                if CmpD <= ArgD:
                    tRow.append (Row)
            lRows = tRow

        if args.has_key ('MarketC'):
            lRows = [Row for Row in lRows
                        if Row['MarketC'] == args['MarketC']]

        if args.has_key ('IndustC'):
            lRows = [Row for Row in lRows
                        if Row['IndustC'] == args['IndustC']]

        if args.has_key ('CFICode'):
            lRows = [Row for Row in lRows
                        if Row['CFICode'] == args['CFICode']]

        if args.has_key ('QuoteNote'):
            lRows = [Row for Row in lRows
                        if args['QuoteNote'] in Row['QuoteNote']]

        if args.has_key ('QuoteClass'):
            lRows = [Row for Row in lRows
                        if args['QuoteClass'] in Row['QuoteClass']]

        return lRows

####################################################################
# TEST MAIN FUNCTION
####################################################################
if __name__ == "__main__":

    #
    # From Internet
    #
    #HtmlUrls  = ['http://brk.twse.com.tw:8000/isin/C_public.jsp?strMode=2',
    #             'http://brk.twse.com.tw:8000/isin/C_public.jsp?strMode=4']

    #
    # From Remove
    #
    #HtmlUrls  = ['file:///cygdrive/d/Code/a/sample/ch2.html',
    #             'file:///cygdrive/d/Code/a/sample/ch4.html']

    #
    # From Local
    #
    HtmlUrls  = ['file:///cygdrive/d/code/finance/sample/ch2.html',
                 'file:///cygdrive/d/code/finance/sample/ch4.html']

    IsinFile   = ['IsinMain.csv', 'IsinRemove.csv']

    IsinClass = TwseIsinIndex()

    IsinClass.IsinFileSet (IsinFile)
    IsinClass.UrlLocatSet (HtmlUrls)
    IsinClass.CfgEnvSet('./', './', './')

    #print 'Cfg Path:', IsinClass.CfgPath
    #print 'Tmp Path:', IsinClass.TmpPath
    #print 'Data Path:', IsinClass.DataPath

    #print IsinClass.MetaHtml
    #print IsinClass.MetaCsv

    #print IsinClass.IsinBackup
    #print IsinClass.IsinFile

    IsinClass.IsinUpdate  ()

    IsinClass.IsinQueryOpen ()

    print IsinClass.IsinQueryHead
    
    print 'A===================================================='
    ret = IsinClass.IsinQueryQuote(ListDateEq='2013/04/16', QuoteCodeF='0381')
    for Row in ret:
        print Row

    print 'B===================================================='
    ret = IsinClass.IsinQueryQuote(QuoteClass='ETF')
    for Row in ret:
        print Row

    IsinClass.IsinQueryClose()
