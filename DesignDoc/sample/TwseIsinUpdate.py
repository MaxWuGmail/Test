#!/usr/bin/python
# -*- coding: UTF-8 -*-
programname = 'TwseIsinDownload - version 2013-04-15'

####################################################################
# Public Libary
####################################################################
import sys, getopt, os.path, glob, HTMLParser, re, html2csv, urllib

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
                self.CSV += '\n'
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
            if '\xa6\xb3\xbb\xf9\xc3\xd2\xa8\xe9\xa5\x4e\xb8\xb9\xa4\xce\xa6\x57\xba\xd9' in TmpRow:
                TmpRow = TmpRow.replace('\xa4\xce', ',')
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
class TwseIsinSrcDownload:

    #
    # Class initial function
    #
    def __init__(self):

        self.UrlLocat   = '' # Array
        self.MetaHtml   = 'IsinMeta.html'
        self.MetaCsv    = 'IsinMeta.csv'
        self.IsinFile   = '' # ['IsinMain.csv', 'IsinRemove.csv']

    #
    # Set URL name for getting ISIN data
    #
    def UrlLocatSet (self, UrlLocat):

        self.UrlLocat = UrlLocat

    #
    # Set ISIN index file for saving
    #
    def IsinFileSet (self, IsinFile):

        self.IsinFile = IsinFile

    def Html2MetaCsv (self):

        print '===>', self.MetaCsv
        print '===>', self.MetaHtml

        lParser = TwseIsinSrc2Csv()
        try:
            lHtmlFile = open(self.MetaHtml, 'rb')
            lCsvFile  = open(self.MetaCsv,  'w+b')
            lData = lHtmlFile.read(8192)
            while lData:
                lParser.feed( lData )
                lCsvFile.write( lParser.getCSV() )
                lData = lHtmlFile.read(8192)
            lCsvFile.write( parser.getCSV(True) )
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
    # Save HTML data from TWSE into html meta file
    #
    def IsinUpdate (self):

        for lUrlLocat in self.UrlLocat:
            #print 'Pull', lUrlLocat
            #f_save = open (self.MetaHtml, 'w+b')
            #f_url  = urllib.urlopen(lUrlLocat)

            #data = f_url.read(8192)
            #while data:
            #    f_save.write(data)
            #    data = f_url.read(8192)

            #f_url.close  ()
            #f_save.close ()
            self.Html2MetaCsv ()

    #
    # Migrate downloaded CSV file into ISIN index file
    #
    def Csv2IsinIndex (self, dst):

        print 'Migrate'


if __name__ == "__main__":
    #try: # Put getopt in place for future usage.
    #    opts, args = getopt.getopt(sys.argv[1:],None)
    #except getopt.GetoptError:
    #    print usage(sys.argv[0])  # print help information and exit:
    #    sys.exit(2)
    #if len(args) == 0:
    #    print usage(sys.argv[0])  # print help information and exit:
    #    sys.exit(2)       
    #print programname
    #html_files = glob.glob(args[0])

    html_files = ['IsinTmp.html']
    HtmlUrls  = ['http://brk.twse.com.tw:8000/isin/C_public.jsp?strMode=4']
    IsinFile   = ['IsinMain.txt', 'IsinRemove.txt']

    IsinClass = TwseIsinSrcDownload()
    IsinClass.IsinFileSet (IsinFile)
    IsinClass.UrlLocatSet (HtmlUrls)
    IsinClass.IsinUpdate  ()
    #IsniFile.UrlSave(html_files)

    #for htmlfilename in html_files:
    #    # print htmlfilename
    #    outputfilename = os.path.splitext(htmlfilename)[0]+'.csv'
    #    parser = TwseIsinSrc2Csv()
    #    print 'Reading %s, writing %s...' % (htmlfilename, outputfilename)
    #    try:
    #        htmlfile = open(htmlfilename, 'rb')
    #        csvfile = open( outputfilename, 'w+b')
    #        data = htmlfile.read(8192)
    #        while data:
    #            parser.feed( data )
    #            csvfile.write( parser.getCSV() )
    #            sys.stdout.write('%d CSV rows written.\r' % parser.rowCount)
    #            data = htmlfile.read(8192)
    #        csvfile.write( parser.getCSV(True) )
    #        csvfile.close()
    #        htmlfile.close()
    #    except:
    #        print 'Error converting %s        ' % htmlfilename
    #        try:    htmlfile.close()
    #        except: pass
    #        try:    csvfile.close()
    #        except: pass
    #print 'All done.                                      '

