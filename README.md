domaininformation
========

Python package used to gather offline (no OSINT!, because there is about 50+ websites for that) information for a domain.

For use in passive dns databases to enrich/enhance queries/filtering, whitelisting/removing domains that are more than likely legitimate if you use or publish a domain blacklist or "threat intel", etc...
The data includes Alexa top million, OpenDNS top million, whether the domain is valid, splitting the domain by level (ie: www, google, com) and more.

The Alexa top million and OpenDNS top million are also very useful in DNS databases for very quick white listing (ie: alexa_rank == None AND open_dns_rank == None).
Provides ability to load Alexa DB and or OpenDNS DB into memory. Defaults to NOT load into memory. Loading into memory is useful if you have one script that is continuously gathering information for many domains.

Splitting each level of a domain is useful when using in a passive dns database for you to say "second level domain != google" which would be "level_domain.2": "google".
The level domain information is useful in databases where you do not want to do a full table scan or regex query..Also, if you were doing a query such as domain != ".*\.google\.com" and you even forget the "$" after ".com" then you would be excluding a domain such as "google.com.baddomain.com".. So this will help with some of that as well as being able to do something like trying to exclude a 3rd level without using a ".\*" before and after the query.
The same querying examples apply to excluding/whitelisting in a script.

Features
========
* Alexa top one million rank
* OpenDNS top one million query
* Each level of the domain
* Total length of domain
* Length of each level of the domain

Please Note
===========
* Downloads databases to the users home folder + "/domaininformation"
* If calling the script individually many times then do not specify the load in memory option (see below).
* If using Alexa rank then the script requires internet access for: downloading the database at https://s3.amazonaws.com/alexa-static/top-1m.csv.zip
* If using OpenDNS rank then the script requires internet access for: downloading the database at https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip

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
    
Detailed Usage Examples
=======================
Whitelisting "legitimate" domains using top one million Alexa & OpenDNS. Will exclude anything <= top 1,000 for Alexa and top 2,000 for OpenDNS. Can Change AND/OR or the number <=
---------
    from domaininformation import DomainInformation
    
    # Lets load the databases into memory for faster results
    DomainInformation.AlexaDatabase(load_in_memory=True)
    DomainInformation.OpenDNSDatabase(load_in_memory=True)
    
    # Give a list of domains to get results from
    domains = [ 'www.google.com', 'bigbassbillyfishing.ru', 'yahoo.com', 'accounts.google.com',
               'a.a.a.a.a.a.a.a.a.a.a.a.a.big-bad-scary-apt.dyndns.org', 'www.yahoo.com', 'www.www.www.msn.com', 'malwaresite.com',
               'adwaresite.com', 'google-login.badstuff.com', 'google-drive.loginsitebad.com', 'google-drive.loginsitebad.org',
               'find-myiphone.badloginfakephishwebsite.org', 'This-Is-Not-A-Domain-And-Should-Not-Be-In-The-List-Because-RFC-States-CantHave-hyphen-next-to-period-and-yes-rfc-is-suggestion-so-you-try-to-register-one-.com'  ]
    
    
    
    # Exclude/Whitelist domains <= to a rank of 1,000 using the Alexa list
    WhitelistAlexaDomainRankOf = 1000
    # Exclude/Whitelist domains <= to a rank of 2,000 using the OpenDNS list
    WhitelistOpenDNSDomainRankOf = 2000
    
    # List of domains that is filtered of high confidence legitimate domains
    FilteredDomainList = list()
    
    # Run on each domain
    for domain in domains:
        domaininfo = DomainInformation(domain)
    
        # Only perform rank query if it is a valid domain
        if domaininfo.is_domain():
            alexa_rank = domaininfo.get_alexa_rank().get('alexa_rank')
            opendns_rank = domaininfo.get_opendns_rank().get('opendns_rank')
    
            if alexa_rank and alexa_rank <= WhitelistAlexaDomainRankOf and opendns_rank <= WhitelistOpenDNSDomainRankOf:
                print 'Exclude me:', domain
    
            else:
                FilteredDomainList.append(domain)
    
    print "List of removed high confidence domains:\n",FilteredDomainList