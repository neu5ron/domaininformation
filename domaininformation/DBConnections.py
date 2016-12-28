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
base_directory = os.path.join( os.path.expanduser("~"), "domaininformation" )  # Directory where the databases will be stored (currently home directory)
hours_to_pull_new_geoip_db = 120#TOOD:Change back # Use this variable in hours to determine how often to download and update the local databases
########################################

# Set logging
log_file = os.path.join ( '/tmp', 'domaininformation.log' )
logging_file = logging.getLogger(__name__)
logging_file.setLevel(logging.DEBUG)
logging_file_handler = handlers.RotatingFileHandler( log_file, maxBytes=5, backupCount=0  )
info_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - Function: %(funcName)s - LineNumber: %(lineno)s - %(message)s')
logging_file_handler.setFormatter(info_format)
logging_file.addHandler(logging_file_handler)

def CreateDBDirectory(Directory):
    if not os.path.exists(Directory):
        logging_file.info('{0} does not exist. Creating it now.'.format(Directory))

        try:
            os.mkdir(Directory)

        except OSError as error:
            print 'Failed to create {0}. Due to:\n{1}'.format(Directory, error)
            logging_file.error('Failed to create {0}. Due to:\n{1}'.format(Directory, error))
            sys.exit(1)

# Create Base Directory
CreateDBDirectory(base_directory)

# Create Alexa Directory
Alexa_directory = os.path.join(base_directory, 'alexa')
Alexa_filename = 'top-1m.csv'# Default alexa filename
CreateDBDirectory(Alexa_directory)

# Create OpenDNS Directory
OpenDNS_directory = os.path.join( base_directory, 'opendns' )
OpenDNS_filename = 'top-1m.csv'# Default alexa filename
CreateDBDirectory(OpenDNS_directory)

def DownloadAlexaDB(filename=Alexa_filename, download_url='https://s3.amazonaws.com/alexa-static/top-1m.csv.zip'):
    """
    Update Or Download information from Alexa
    :param filename:
    :param download_url:
    :return:
    """
    current_time = datetime.utcnow()
    need_to_download = False
    file_last_downloaded = os.path.join(Alexa_directory, 'last_downloaded_%s.txt') % filename # File that will be used to determine the last time the DBs were downloaded

    if os.path.exists(os.path.join(Alexa_directory, filename)):

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
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

    else:
        need_to_download = True

    if need_to_download:
        print 'Alexa file needs to be updated or does not exist!\nTrying to download it to %s/%s\n'%(Alexa_directory, filename)
        logging_file.info( 'Alexa file needs to be updated or does not exist! Trying to download it to "{0}/{1}"'.format(Alexa_directory, filename))

        try:
            response = requests.get( download_url, timeout=(10,5) )

            with open(os.path.join(Alexa_directory, filename), 'wb') as downloaded_file, open(file_last_downloaded, 'w') as lastdownloadf, ZipFile(StringIO(response.content), 'r') as zipfile:
                downloaded_file.write(zipfile.open(filename).read())
                lastdownloadf.write(str(current_time))
                zipfile.close()

            downloaded_file.close()
            lastdownloadf.close()

        except IOError as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.HTTPError as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.Timeout as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.ConnectionError as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.TooManyRedirects as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.URLRequired as error:
            print 'Could not download and write Alexa database due to %s.\n'%error
            logging_file.error( 'Could not download and write Alexa database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

def DownloadOpenDNSDB(filename=OpenDNS_filename, download_url='https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip'):
    """
    Update Or Download information from OpenDNS
    :param filename:
    :param download_url:
    :return:
    """
    current_time = datetime.utcnow()
    need_to_download = False
    file_last_downloaded = os.path.join(OpenDNS_directory, 'last_downloaded_%s.txt') % filename # File that will be used to determine the last time the DBs were downloaded

    if os.path.exists(os.path.join(OpenDNS_directory, filename)):

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
            print 'Could not download and write OpenDNS database due to %s.\n'%error
            logging_file.error( 'Could not download and write OpenDNS database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

    else:
        need_to_download = True

    if need_to_download:
        print 'OpenDNS file needs to be updated or does not exist!\nTrying to download it to %s/%s\n'%(OpenDNS_directory, filename)
        logging_file.info( 'OpenDNS file needs to be updated or does not exist! Trying to download it to "{0}/{1}"'.format(OpenDNS_directory, filename))

        try:
            response = requests.get( download_url, timeout=(10,5) )

            with open(os.path.join(OpenDNS_directory, filename), 'wb') as downloaded_file, open(file_last_downloaded, 'w') as lastdownloadf, ZipFile(StringIO(response.content), 'r') as zipfile:
                downloaded_file.write(zipfile.open(filename).read())
                lastdownloadf.write(str(current_time))
                zipfile.close()

            downloaded_file.close()
            lastdownloadf.close()

        except IOError as error:
            print 'Could not download and write OpenDNS database due to %s.\n'%error
            logging_file.error( 'Could not download and write OpenDNS database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.HTTPError as error:
            print 'Could not download and write OpenDNS database due to %s.\n'%error
            logging_file.error( 'Could not download and write OpenDNS database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.Timeout as error:
            print 'Could not download and write OpenDNS database due to %s.\n'%error
            logging_file.error( 'Could not download and write OpenDNS database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.ConnectionError as error:
            print 'Could not download and write OpenDNS database due to %s.\n'%error
            logging_file.error( 'Could not download and write OpenDNS database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.TooManyRedirects as error:
            print 'Could not download and write OpenDNS database due to %s.\n'%error
            logging_file.error( 'Could not download and write OpenDNS database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

        except requests.URLRequired as error:
            print 'Could not download and write OpenDNS database due to %s.\n'%error
            logging_file.error( 'Could not download and write OpenDNS database. Due to:\n{0}'.format( error ) )
            sys.exit(1)

def GetAlexaDB( load_in_memory=False, number_to_load_in_memory=1000000 ):
    """
    :param load_in_memory: whether to load the alexa DB into memory as a dictionary for fast lookups. Default=False
    :param number_to_load_in_memory: if load_in_memory=True than decide how much of the alexa DB to load. Default=1,000,000
    :return: alexa_db
    """
    if not load_in_memory:
        alexacsvfile = open(os.path.join(Alexa_directory, Alexa_filename), 'rb')
        alexa_db = csv.reader(alexacsvfile, delimiter=',')
    else:
        alexa_db = dict()
        with open(os.path.join(Alexa_directory, Alexa_filename), 'rb') as alexacsvfile:
            alexa_file = csv.reader( alexacsvfile, delimiter=',' )
            for num, row in enumerate(alexa_file):
                if num != number_to_load_in_memory and num != 1000001:
                    alexa_db.setdefault( row[1], int(row[0]) )
                else:
                    break
        alexacsvfile.close()

    return alexa_db

def GetOpenDNSDB( load_in_memory=False, number_to_load_in_memory=1000000 ):
    """
    :param load_in_memory: whether to load the alexa DB into memory as a dictionary for fast lookups. Default=False
    :param number_to_load_in_memory: if load_in_memory=True than decide how much of the alexa DB to load. Default=1,000,000
    :return: opendns_db
    """
    if not load_in_memory:
        opendnscsvfile = open(os.path.join(OpenDNS_directory, Alexa_filename), 'rb')
        opendns_db = csv.reader(opendnscsvfile, delimiter=',')
    else:
        opendns_db = dict()
        with open(os.path.join(OpenDNS_directory, OpenDNS_filename), 'rb') as opendnscsvfile:
            opendns_file = csv.reader( opendnscsvfile, delimiter=',' )
            for num, row in enumerate(opendns_file):
                if num != number_to_load_in_memory and num != 1000001:
                    opendns_db.setdefault( row[1], int(row[0]) )
                else:
                    break
        opendnscsvfile.close()

    return opendns_db

