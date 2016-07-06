#!/usr/bin/env python2.7
from . import AlexaDBConnection
import re
from AlexaDBConnection import logging_file

# Regex to verify a valid domain. Uses most of the RFC, although still allows things not necessarily in the the RFC like two or more -- ie: google--analytics.com (which is malicious) and allows for IDN domain names.
domain_regex = r'(([\da-zA-Z])([\w-]{,62})\.){,127}(([\da-zA-Z])[\w-]{,61})?([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z]{2,})))'
domain_regex = '{0}$'.format(domain_regex)
valid_domain_name_regex = re.compile(domain_regex, re.IGNORECASE)

# Download and call Alexa DB
AlexaDBConnection.DownloadAlexaDB()
alexa_db = AlexaDBConnection.GetAlexaDB()

class DomainInformation:
    def __init__(self, domain_name):
        """
        :param domain_name: The Domain name to gather information for
        :return:
        """
        self.domain_name = domain_name
        try:
            self.domain_name = self.domain_name.lower().strip().encode('ascii')
            self.valid_encoding = True

        except ( UnicodeEncodeError, ValueError, AttributeError) as error:
            self.valid_encoding = False
            print u'{0} is not valid. It should be input as an ascii string.'.format( unicode(self.domain_name) )
            logging_file.error( u'{0} is not valid. It should be input as an ascii string.'.format( unicode(self.domain_name) ) )

    def level_domain_info(self):
        """
        Get the length and level of each domain/http host split by level(ie:'.').
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
                ld_information['level_domain'].update( { 'length_%s'%ld_number: ld_length } )
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
        """
        Get the alexa rank of the first and second level domain (ie: google.com).
        Rank will be based on the max of the sixth level domain and will iterate all the way down to the first and second level.
        ie: www.google.com would match google.com in the database.

        Returns:
            Dictionary: {'alexa_rank': Int(AlexaRank)}

        >>> from domaininformation import DomainInformation
        >>> print DomainInformation(domain_name='www.google.com').get_alexa_rank()
            {'alexa_rank': 1}
        >>> print DomainInformation(domain_name='NotADomain').get_alexa_rank()
            "notadomain" Is not a domain
            {'alexa_rank': None}
        """
        alexa_rank = {'alexa_rank': None }

        if self.is_domain():
            level_domain = self.domain_name.split('.')[-6:]
            level_domain_length = len(level_domain)

            if level_domain_length >= 2:

                # for n in range(level_domain_length-1):#TODO:Reenable or Delete
                #     domain = '%s.%s' %('.'.join(level_domain[:-1][n:]), level_domain[-1] )
                #     alexa_rank = alexa_db.get(domain)
                #
                #     if alexa_rank:
                #         ret['alexa_rank'] = alexa_rank
                #         break

                domains = [ '%s.%s' %('.'.join(level_domain[:-1][n:]), level_domain[-1] ) for n in range(level_domain_length-1) ]

                for ranking in alexa_db:
                    for domain in domains:
                        if domain == ranking[1]:
                            alexa_rank['alexa_rank'] = ranking[0]
            else:
                print 'Domain does not have a first and second level, and therefore can not get the alexa rank.\n'

        return alexa_rank

    def is_domain(self):
        """
        Return true if valid domain return false if invalid domain.
        >>> from domaininformation import DomainInformation
        >>> print DomainInformation(domain_name='google.com').is_domain()
            True
        >>> print DomainInformation(domain_name='NotADomain').is_domain()
            False
        """
        if self.valid_encoding:

            if re.match(valid_domain_name_regex, self.domain_name ):
                return True

        # print u'{0} is not a domain.'.format( unicode(self.domain_name) )
        logging_file.warn( u'"{0}" is not a domain.'.format( unicode(self.domain_name) ) )
        return False

    def all(self):
        """
        Put everything together.
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
