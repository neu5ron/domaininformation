#!/usr/bin/env python2.7
from datetime import datetime
import os, sys
import csv
from StringIO import StringIO
from zipfile import ZipFile
import requests
from dateutil import parser
import logging
from logging import handlers

######################################## # Edit If Need Be
base_directory = os.path.expanduser("~") # Directory where 'alexa' folder will be created (currently home directory)
hours_to_pull_new_geoip_db = 120 # Use this variable in hours to determine how often to download and update the local databases
########################################

# Set logging
log_file = os.path.join ( os.path.realpath( os.path.join( __file__, '..' ) ), 'domaininformation.log' )
logging_file = logging.getLogger(__name__)
logging_file.setLevel(logging.DEBUG)
logging_file_handler = handlers.RotatingFileHandler( log_file, maxBytes=5, backupCount=0  )
info_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - Function: %(funcName)s - LineNumber: %(lineno)s - %(message)s')
logging_file_handler.setFormatter(info_format)
logging_file.addHandler(logging_file_handler)

# Create Alexa Directory
alexa_directory = os.path.join( base_directory, 'alexa' )

if not os.path.exists(alexa_directory):
    # print '%s does not exist. Creating it now.'%alexa_directory
    logging_file.info( '{0} does not exist. Creating it now.'.format(alexa_directory) )

    try:
        os.mkdir(alexa_directory)

    except OSError as error:
        # print 'Failed to create %s'%alexa_directory
        # print '%s'%error
        logging_file.error( 'Failed to create {0}. Due to:\n{1}'.format( alexa_directory, error ) )
        sys.exit(1)


def AlexaDB( filename='top-1m.csv', download_url='https://s3.amazonaws.com/alexa-static/top-1m.csv.zip' ):
    """
    Update Or Download information from Alexa Rank and return it for use
    :param filename:
    :param download_url:
    :return:
    """

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
            # print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

    else:
        need_to_download = True

    if need_to_download:
        # print 'Alexa file needs to be updated or does not exist!\nTrying to download it to %s/%s\n'%( alexa_directory, filename )
        logging_file.info( 'Alexa file needs to be updated or does not exist! Trying to download it to "{0}/{1}"'.format( alexa_directory, filename ) )

        try:
            response = requests.get( download_url, timeout=(10,2) )

            with open( os.path.join( alexa_directory, filename ), 'wb' ) as downloaded_file, open(file_last_downloaded, 'w') as lastdownloadf, ZipFile(StringIO(response.content), 'r') as zipfile:
                downloaded_file.write(zipfile.open(filename).read())
                lastdownloadf.write(str(current_time))
                zipfile.close()

            downloaded_file.close()
            lastdownloadf.close()


        except IOError as error:
            # print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.HTTPError as error:
            # print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.Timeout as error:
            # print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.ConnectionError as error:
            # print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.TooManyRedirects as error:
            # print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.URLRequired as error:
            # print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            return False

    # Set Alexa database
    alexa_db = dict()

    with open(os.path.join( alexa_directory, filename ), 'rb') as alexacsvfile:
        alexa_file = csv.reader( alexacsvfile, delimiter=',' )

        for row in alexa_file:
            alexa_db.setdefault( row[1], int(row[0]) )
            # if a == 100001:#TODO:Eventually allow choice of how many of the alexa top million to grab
            #     break
            # else:
                # alexa_db.setdefault( row[1], int(row[0]) )

    alexacsvfile.close()

    return alexa_db

