#!/usr/bin/env python2.7
from datetime import datetime
import os, sys
import csv
from StringIO import StringIO
from zipfile import ZipFile
import urllib2
from dateutil import parser

######################################## # Edit If Need Be
base_directory = os.path.expanduser("~") #Directory where 'alexa' folder will be created (currently home directory)
hours_to_pull_new_geoip_db = 120 #Use this variable in hours to determine how often to download and update the local databases
########################################

alexa_directory = os.path.join( base_directory, 'alexa' )

if not os.path.exists(alexa_directory):
    print '%s does not exist. Creating it now.'%alexa_directory

    try:
        os.mkdir(alexa_directory)

    except OSError as error:
        print 'Failed to create %s'%alexa_directory
        print '%s'%error
        print 'Exiting Script'
        sys.exit(1)


def AlexaDB( filename='top-1m.csv', download_url='https://s3.amazonaws.com/alexa-static/top-1m.csv.zip' ):
    """download_and_update_alexa(  ) = Update Or Download information from Alexa Rank and return it for use"""

    current_time = datetime.utcnow()
    need_to_download = False
    file_last_downloaded = os.path.join( alexa_directory, 'last_downloaded_%s.txt' )%filename # File that will be used to determine the last time the DBs were downloaded

    if os.path.exists( os.path.join( alexa_directory, filename ) ):

        try:

            # Check to see if download timestamp exists and if it does see time diff since download
            if os.path.exists(file_last_downloaded):

                with open(file_last_downloaded, 'r+') as lastdlf:
                    last_downloaded = lastdlf.read().strip()

                    # File is blank
                    if not last_downloaded:
                        lastdlf.write(str(current_time))

                    else:
                        time_diff = (current_time - parser.parse(last_downloaded)).total_seconds()

                        if time_diff > hours_to_pull_new_geoip_db*3600:
                            need_to_download = True

            else:
                # Set download timestamp if it was not downloaded using this script and this is the first time the script is ran
                with open(file_last_downloaded, 'w+') as lastdlf:
                    lastdlf.write(str(current_time))

        except IOError as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            sys.exit(1)

    else:
        need_to_download = True

    if need_to_download:
        print 'Alexa file needs to be updated or does not exist!\nTrying to download it to %s/%s\n'%( alexa_directory, filename )

        try:
            url = urllib2.urlopen(download_url)

            with open( os.path.join( alexa_directory, filename ), 'wb' ) as downloaded_file, open(file_last_downloaded, 'w') as lastdownloadf, ZipFile(StringIO(url.read()), 'r') as zipfile:
                downloaded_file.write(zipfile.open(filename).read())
                lastdownloadf.write(str(current_time))
                zipfile.close()

        except IOError as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            sys.exit(1)

        except urllib2.HTTPError as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            sys.exit(1)

        except urllib2.URLError as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            sys.exit(1)

    #Set Alexa database
    alexa_db = dict()

    with open(os.path.join( alexa_directory, filename ), 'rb') as alexacsvfile:
        alexa_file = csv.reader( alexacsvfile, delimiter=',' )

        for row in alexa_file:
            alexa_db.setdefault( row[1], int(row[0]) )

    return alexa_db

