domaininformation
========

domaininformation is a python package focused on combining information about a domain in JSON format.

Features
========
* Alexa top one million rank
* Each level of the domain
* Total length of domain
* Length of each level of the domain

Please Note
===========
* Converts all timestamps to UTC.
* Currently only supports IPv4.
* Requires internet access for: downloading alexa databases

Requirements
============
* Python 2.7
* pip install -U requests[security] #Install requests security
* pip install -U dateutils; #Time/Date Utility

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
-------------
	get_alexa_rank( ) = Get the alexa rank of the first and second level domain (ie: google.com).
    Rank will be based on the max of the sixth level domain and will iterate all the way down to the first and second level.
    ie: www.google.com would match google.com in the database.
    >>> from domaininformation import DomainInformation
    >>> print DomainInformation(domain_name='www.google.com').get_alexa_rank()
        {'alexa_rank': 1}
    >>> print DomainInformation(domain_name='NotADomain').get_alexa_rank()
        "notadomain" Is not a domain
        {'alexa_rank': None}

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

All Information / Put everything together
---------------
	all( ) = put everything together.
    >>> from domaininformation import DomainInformation
    >>> from pprint import pprint
    >>> pprint( DomainInformation(domain_name='www.google.com').all() )
    {'alexa_rank': 1,
     'level_domain': {'1': 'com',
                      'length_1': 3,
                      '2': 'google',
                      'length_2': 6,
                      '3': 'www',
                      'length_3': 3,
                      'any': ['com', 'google', 'www'],
                      'any_length': [3, 6, 3],
                      'total': 2,
                      'total_length': 12}}
    >>> pprint( DomainInformation(domain_name='NotADomain').all() )
    "notadomain" Is not a domain
    {'alexa_rank': None, 'level_domain': None}