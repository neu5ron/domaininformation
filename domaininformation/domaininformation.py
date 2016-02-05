#!/usr/bin/env python2.7
from . import AlexaDBConnection
import re

######## Regular Expressions
# Regex to verify a valid domain. Uses most of the RFC, although still allows things not necessarily in the the RFC like two or more -- ie: google--analytics.com (which is malicious) and allows for IDN domain names.
valid_domain_name_regex = re.compile('^(([\da-zA-Z])([\w-]{,62})\.){,127}([\da-zA-Z])[\w-]{,61}([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z]{2,})))$', re.IGNORECASE)

######## Call and Use Databases
alexa_db = AlexaDBConnection.AlexaDB()

class DomainInformation:
    def __init__(self, domain_name):
        self.domain_name = domain_name

        try:
            self.domain_name = self.domain_name.lower().strip().encode('ascii')
            valid_encoding = True

        except ( UnicodeEncodeError, ValueError) as error:
            valid_encoding = False
            print error
            print '%s is not valid. It should be input as an ascii string.\n'%self.domain_name.encode('utf8','replace')

        finally:
            self.valid_encoding = valid_encoding

    def level_domain_info(self):
        """level_domain_info( ) = Get the length and level of each domain/http host split by level(ie:'.').
        >>> from domaininformation import DomainInformation
        >>> from pprint import pprint
        >>> pprint( DomainInformation(domain_name='www.google.com').level_domain_info() )
        {'level_domain': {'1': 'com',
                          '1_length': 3,
                          '2': 'google',
                          '2_length': 6,
                          '3': 'www',
                          '3_length': 3,
                          'any': ['com', 'google', 'www'],
                          'any_length': [3, 6, 3],
                          'total': 2,
                          'total_length': 12}}
        >>> pprint( DomainInformation(domain_name='NotADomain').level_domain_info() )
        "notadomain" Is not a domain
        {'level_domain': None}
        """
        if self.is_domain():
            domain_split = self.domain_name.split('.')
            total = len(domain_split)
            total_length = len(self.domain_name.replace('.',''))
            ld_information = { 'level_domain': { } }

            any_ld = list()
            any_ld_length = list()

            for ld_number, ld_value in enumerate(reversed(domain_split)):
                ld_number+=1
                ld_length = len(ld_value)
                ld_information['level_domain'].update( { '%s'%ld_number: ld_value } )
                ld_information['level_domain'].update( { '%s_length'%ld_number: ld_length } )
                any_ld.append(ld_value)
                any_ld_length.append(ld_length)

            ld_information['level_domain'].update( { 'any': list(set(any_ld)) } )
            ld_information['level_domain'].update( { 'any_length': list(set(any_ld_length)) } )
            ld_information['level_domain'].update( { 'total_length': total_length } )
            ld_information['level_domain'].update( { 'total': total } )
            return ld_information

        else:
            return { 'level_domain': None }

    def get_alexa_rank(self):
        """get_alexa_rank( ) = Get the alexa rank of the first and second level domain (ie: google.com)
        Rank will be based on the max of the sixth level domain.
        >>> from domaininformation import DomainInformation
        >>> print DomainInformation(domain_name='www.google.com').get_alexa_rank()
            {'alexa_rank': 1}
        >>> print DomainInformation(domain_name='NotADomain').get_alexa_rank()
            "notadomain" Is not a domain
            {'alexa_rank': None}
        """
        if self.is_domain():
            level_domain = self.domain_name.split('.')[-6:]
            level_domain_length = len(level_domain)

            if level_domain_length >= 2:

                for n in range(level_domain_length-1):
                    domain = '%s.%s' %('.'.join(level_domain[:-1][n:]), level_domain[-1] )
                    alexa_rank = alexa_db.get(domain)

                    if alexa_rank:
                        return {'alexa_rank': alexa_rank }
                return {'alexa_rank': alexa_rank }

            else:
                print 'Domain does not have a first and second level, and therefore can not get the alexa rank.\n'
                return {'alexa_rank': None }

        else:
            return { 'alexa_rank': None }

    def is_domain(self):
        """is_domain( ) = Return true if valid domain return false if invalid domain.
        >>> from domaininformation import DomainInformation
        >>> print DomainInformation(domain_name='google.com').is_ip()
            True
        >>> print DomainInformation(domain_name='NotADomain').is_ip()
            False
        """
        if self.valid_encoding:

            if re.match(valid_domain_name_regex, self.domain_name ):
                return True

        print '"%s" Is not a domain'%self.domain_name
        return False

    def all(self):
        """all( ) = put everything together.
        >>> from domaininformation import DomainInformation
        >>> from pprint import pprint
        >>> pprint( DomainInformation(domain_name='www.google.com').all() )
        {'alexa_rank': 1,
         'level_domain': {'1': 'com',
                          '1_length': 3,
                          '2': 'google',
                          '2_length': 6,
                          '3': 'www',
                          '3_length': 3,
                          'any': ['com', 'google', 'www'],
                          'any_length': [3, 6, 3],
                          'total': 2,
                          'total_length': 12}}
        >>> pprint( DomainInformation(domain_name='NotADomain').all() )
        "notadomain" Is not a domain
        {'alexa_rank': None, 'level_domain': None}
        """
        data = dict()

        if self.is_domain():
            data.update(self.level_domain_info())
            data.update(self.get_alexa_rank())
            return data

        else:
            data.update({ 'level_domain': None })
            data.update({ 'alexa_rank': None })
            return data
