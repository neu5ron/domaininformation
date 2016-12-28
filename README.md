domaininformation
========

Python package used to gather offline information for a domain. For use in passive dns databases, whitelisting, etc... The data includes Alexa top million, OpenDNS top million, whether the domain is valid, splitting the domain by level (ie: www, google, com) and more. Provides ability to load Alexa DB and or OpenDNS DB into memory. Defaults to NOT load into memory. Loading into memory is useful if you have one script that is continuously gathering information for many domains.  If calling the script individually many times then do not specify the load in memory option (see below). Splitting a domain by levels is helpful when using in a passive dns database for you to say "second level domain != google" which would be "level_domain.2": "google". The level domain information is useful in databases where you do not want to do a full table scan or regex query..Also, if you were doing a query such as domain != ".*\.google\.com" and you even forget the "$" after ".com" then you would be excluding a domain such as "google.com.baddomain.com".. So this will help with some of that as well as being able to do something like trying to exclude a 3rd level without using a ".\*" before and after the query. The Alexa top million and OpenDNS top million are also very useful in DNS databases for very quick white listing (ie: alexa_rank == None AND open_dns_rank == None).

Features
========
* Alexa top one million rank
* OpenDNS top one million query
* Each level of the domain
* Total length of domain
* Length of each level of the domain

Please Note
===========
* Downloads databases to the users home folder + "domaininformation"
* Requires internet access for: downloading alexa database at https://s3.amazonaws.com/alexa-static/top-1m.csv.zip
* Requires internet access for: downloading opendns database at https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip

Requirements
============
sudo apt-get install build-essential libssl-dev libffi-dev python-dev; # For python requests security
* Python 2.7
* pip install -U requests; # Install requests
* pip install -U requests[security]; # Install requests security
* pip install -U dateutils; # Time/Date Utility

Install
=======
pip install -e git+https://github.com/neu5ron/domaininformation@master#egg=domaininformation

Usage Examples
==============
Valid Domain
---------
    is_domain( ) = Return true if valid domain return false if invalid domain.
    >>> from domaininformation import DomainInformation
    >>> print DomainInformation(domain_name='google.com').is_domain()
        True
    >>> print DomainInformation(domain_name='NotADomain').is_domain()
        False

Alexa Rank
----------
    get_alexa_rank( ) = Get the alexa rank of the first and second level domain (ie: google.com).
    Rank will be based on the max of the sixth level domain and will iterate all the way down to the first and second level.
    ie: www.google.com would match google.com in the database.
    >>> from domaininformation import DomainInformation
    # To load the DB into memory for faster querying (turned off by default) perform below. By default all one million are loaded. Also you only need to perform this once for the entire script.
    DomainInformation.AlexaDatabase(load_in_memory=True)
    # To specify how many of the one million are loaded perform:
    DomainInformation.AlexaDatabase(load_in_memory=True, number_to_load_in_memory=1000)    
    >>> print DomainInformation(domain_name='www.google.com').get_alexa_rank()
        {'alexa_rank': 1}
    >>> print DomainInformation(domain_name='NotADomain').get_alexa_rank()
        "notadomain" Is not a domain
        {'alexa_rank': None}

OpenDNS Rank
------------
    get_opendns_rank( ) = Get the opendns rank of the first and second level domain (ie: google.com).
    Rank will be based on the max of the sixth level domain and will iterate all the way down to the first and second level.
    ie: www.google.com would match google.com in the database.
    >>> from domaininformation import DomainInformation
    # To load the DB into memory for faster querying (turned off by default) perform below. By default all one million are loaded. Also you only need to perform this once for the entire script.
    DomainInformation.OpenDNSDatabase(load_in_memory=True)
    # To specify how many of the one million are loaded perform:
    DomainInformation.OpenDNSDatabase(load_in_memory=True, number_to_load_in_memory=1000)    
    >>> print DomainInformation(domain_name='www.google.com').get_opendns_rank()
        {'opendns_rank': 8}
    >>> print DomainInformation(domain_name='NotADomain').get_opendns_rank()
        "notadomain" Is not a domain
        {'opendns_rank': None}

Level Domain Information
-------------------
    level_domain_info( ) = Get the length and level of each domain/http host split by level(ie:'.').
    >>> from domaininformation import DomainInformation
    >>> from pprint import pprint
    >>> pprint( DomainInformation(domain_name='www.google.com').level_domain_info() )
    {'level_domain': {'1': 'com',
                      'length_1': 3,
                      '2': 'google',
                      'length_2': 6,
                      '3': 'www',
                      'length_3': 3,
                      'any': ['com', 'google', 'www'],
                      'any_length': [3, 6, 3],
                      'total': 2,
                      'total_length': 12}}
    >>> pprint( DomainInformation(domain_name='NotADomain').level_domain_info() )
    "notadomain" Is not a domain
    {'level_domain': None}