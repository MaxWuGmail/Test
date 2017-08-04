#!/usr/bin/python
# -*- coding: UTF-8 -*-

##########################################################################
# Public Library
##########################################################################
#
# System related library
#
import sys, os, signal, atexit

#
# High level file operation
#
import shutil

#
# Date/Time related library
#
from datetime import timedelta
import calendar

##########################################################################
# Private Library
##########################################################################
from TwseOldLib import *
from TwseConfig import *

##########################################################################
# Private Function
##########################################################################
#
# Function for Download begine
# Reading configuration files
#
def TwseDownloadBegin(StartDate):

    global gTwseDwonloadDate

    TwseDirectoryCreate()

    print >> sys.stderr, '  Before Doenload, get configuration from', gTwseCfgFile

    #
    # Read configuration
    #
    gTwseConfig.read(gTwseCfgFile)

    #
    # Checking if DATE SECTION exist
    #
    if gTwseConfig.has_section(gTwseCfgDateSection) == False:

        gTwseConfig.add_section(gTwseCfgDateSection)

    #
    # Get last download date of last time
    #
    if gTwseConfig.has_option(gTwseCfgDateSection, gTwseCfgDateDownload) == True:

        StartDate = date.fromordinal(gTwseConfig.getint(gTwseCfgDateSection, gTwseCfgDateDownload))

    else:

        gTwseConfig.set(gTwseCfgDateSection, gTwseCfgDateDownload, str(StartDate.toordinal()))

    print >> sys.stderr, '  Start download date is', StartDate

    gTwseDwonloadDate = StartDate
    
# TwseDownloadBegin

#
# Function for download end
#
def TwaseDownloadExit(EndDate, EndCount):

    global gTwseConfig

    print >> sys.stderr, 'Download exit...'
    print >> sys.stderr, '  Last download date is:', EndDate
    print >> sys.stderr, '  Last download item is:', EndCount

    gTwseConfig.set(gTwseCfgDateSection, gTwseCfgDateDownload, str(EndDate.toordinal()))

    with open(gTwseCfgFile, 'wb') as configfile:

        gTwseConfig.write(configfile)
        configfile.close()

# TwaseDownloadExit

#
# Function for signal CTRL+C control
#
def TwaseExit(SigNum, frame):

    print >> sys.stderr, '\nCaugh By Kill sginal....'

    TwaseDownloadExit(gTwseDwonloadDate, gTwseDownloadItem)

    sys.exit(0)

# TwaseExit

#
# Library for download TWSE data
#
# Procedure...
# 1. Download data from URL
# 2. save date to template file
# 3. Verify download data
# 4. Saving data if not empty
#
def TwseDataDownData(dest_url, dest_file):

    a = 0

    print >> sys.stderr, dest_url
    print >> sys.stderr, dest_file

# TwseDataDownload

##########################################################################
# program Entry
##########################################################################
if __name__ == "__main__":

    print >> sys.stderr, 'TWSE data download.....'

    TwseDownloadBegin(gTwseDwonloadDate)

    #
    # Caught exit signal
    #
    signal.signal(signal.SIGINT,  TwaseExit)
    signal.signal(signal.SIGTERM, TwaseExit)

    print >> sys.stderr, '  Output dir:', gTwseWorkDirDwonload
    print >> sys.stderr, '  Progress checking'

    #
    # Phase 0 download (All are html files)
    #
    date_id = gTwseDwonloadDate
    date_to = TWSE_PHASE[0][1]

    if True:
        while (date_id <= date_to):
        
            fname = 'TwsePhaseA%(p0)02d%(p1)02d%(p2)02d.csv' % \
                {"p0":date_id.year, "p1":date_id.month, "p2":date_id.day}
            print >> sys.stderr, 'P0 <', fname, '>'
            gTwseDwonloadDate = date_id
            date_s = '%(p0)02d/%(p1)02d/%(p2)02d' % \
                {"p0":date_id.year - 1911, "p1":date_id.month, "p2":date_id.day}
        
            if TwseOldDownloadTry(gTwseWorkDirTemp + '/tmp.csv', date_s) == True:
                print >> sys.stderr, date_s, 'True'
                shutil.move (gTwseWorkDirTemp + '/tmp.csv', gTwseWorkDirDwonload + '/' + fname)
            else:
                print >> sys.stderr, date_s, 'False'
        
            date_id = date_id + timedelta(days = 1)

    #
    # Phase 1 download (All are csv files)
    #
    date_id = gTwseDwonloadDate

    #if gTwseDwonloadDate == TWSE_PHASE[0][1]:

    date_id = TWSE_PHASE[1][0]
        
    date_to = TWSE_PHASE[1][1]

    while (date_id <= date_to):

        fname = 'TwsePhaseB%(p0)02d%(p1)02d%(p2)02d.csv' % \
            {"p0":date_id.year, "p1":date_id.month, "p2":date_id.day}
        print >> sys.stderr, 'P1 <', fname, '>'

        gTwseDownloadItem = 0

        for iden in TWSE_STOCK_IDENP1:

            d_url = TWSE_STOCK_URLP1 + '/Report' + date_id.strftime("%Y%m") + (
                    '/A112' + date_id.strftime("%Y%m%d") + iden[0] + '.php&type=csv')

            d_file = 'A112' + date_id.strftime("%Y%m%d") + iden[0] + '.csv'

            TwseDataDownData(d_url, d_file)

            gTwseDwonloadDate = date_id
            gTwseDownloadItem = gTwseDownloadItem + 1

        date_id = date_id + timedelta(days = 1)

    #
    # Log last download flags
    #
    TwaseDownloadExit(gTwseDwonloadDate, gTwseDownloadItem)

# __main__

