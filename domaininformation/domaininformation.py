#!/usr/bin/env python2.7
import re
try:
    from . import DBConnections
    from DBConnections import logging_file
except ImportError as error:
    print 'Could not import function.'
    print error

# Regex to verify a valid domain. Uses most of the RFC, although still allows things not necessarily in the the RFC like two or more -- ie: google--analytics.com (which is malicious) and allows for IDN domain names.
domain_regex = r'(([\da-zA-Z])([_\w-]{,62})\.){,127}(([\da-zA-Z])[_\w-]{,61})?([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z]{2,})))'
domain_regex = '{0}$'.format(domain_regex)
valid_domain_name_regex = re.compile(domain_regex, re.IGNORECASE)

class DomainInvalidLevels():
    pass

class DomainInformation(object):
    def __init__(self, domain_name):
        """
        :param domain_name: The Domain name to gather information for
        :return:
        """
        self.domain_name = domain_name
        try:
            self.domain_name = self.domain_name.lower().strip().encode('ascii')
            self.valid_encoding = True

            if re.match(valid_domain_name_regex, self.domain_name):
                self.IsDomain = True
            else:
                raise DomainInvalidLevels

        except (UnicodeEncodeError, ValueError, AttributeError) as error:
            self.valid_encoding = False
            self.IsDomain = False
            print r'{0} is not valid. It should be input as an ascii string.'.format(self.domain_name)
            logging_file.error( r'{0} is not valid. It should be input as an ascii string.'.format(self.domain_name))

        except DomainInvalidLevels:
            self.IsDomain = False
            print r'{0} is not valid. It does not have enough levels.'.format(self.domain_name)
            logging_file.error( r'{0} is not valid. It does not have enough levels.'.format(self.domain_name))

    @classmethod
    def AlexaDatabase(self, load_in_memory=False, number_to_load_in_memory=1000000):
        """
        :param load_in_memory: Bool. load the database into memory, only recommend if one script is calling this..
    Not if
        script will be run over and over
        :param number_to_load_in_memory: Int. if loading into memory how many of the database to load
        """
        self.LoadAlexaDBInMemory = load_in_memory
        self.AlexaDBNumberToLoadInMemory = number_to_load_in_memory
        # Download Alexa DB
        DBConnections.DownloadAlexaDB()
        self.AlexaDB = DBConnections.GetAlexaDB(self.LoadAlexaDBInMemory, self.AlexaDBNumberToLoadInMemory)

    @classmethod
    def OpenDNSDatabase(self, load_in_memory=False, number_to_load_in_memory=1000000):
        """
        :param load_in_memory: Bool. load the database into memory, only recommend if one script is calling this..
    Not if
        script will be run over and over
        :param number_to_load_in_memory: Int. if loading into memory how many of the database to load
        """
        self.LoadOpenDNSDBInMemory = load_in_memory
        self.OpenDNSDBNumberToLoadInMemory = number_to_load_in_memory
        # Download penDNS DB
        DBConnections.DownloadOpenDNSDB()
        self.OpenDNSDB = DBConnections.GetOpenDNSDB(self.LoadOpenDNSDBInMemory, self.OpenDNSDBNumberToLoadInMemory)


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
        ld_information = {'level_domain': None}

        if self.IsDomain:
            domain_split = self.domain_name.split('.')
            total = len(domain_split)
            total_length = len(self.domain_name.replace('.', ''))
            ld_information = {'level_domain': {}}

            any_ld = list()
            any_ld_length = list()

            for ld_number, ld_value in enumerate(reversed(domain_split)):
                ld_number += 1
                ld_length = len(ld_value)
                ld_information['level_domain'].update({'%s' % ld_number: ld_value})
                ld_information['level_domain'].update({'length_%s' % ld_number: ld_length})
                any_ld.append(ld_value)
                any_ld_length.append(ld_length)

            ld_information['level_domain'].update({'any': list(set(any_ld))})
            ld_information['level_domain'].update({'any_length': list(set(any_ld_length))})
            ld_information['level_domain'].update({'total_length': total_length})
            ld_information['level_domain'].update({'total': total})
            return ld_information

        return ld_information

    def get_alexa_rank(self):
        """
        Get the alexa rank of the first and second level domain (ie: google.com).
        Rank will be based on the max of the sixth level domain and will iterate all the way down to the
        first and second level.
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
        alexa_rank = {'alexa_rank': None}

        if self.IsDomain:
            level_domain = self.domain_name.split('.')[-6:]
            level_domain_length = len(level_domain)

            try:
                if self.AlexaDB:
                    for n in range(level_domain_length - 1):
                        domain = '%s.%s' % ('.'.join(level_domain[:-1][n:]), level_domain[-1])
                        rank = self.AlexaDB.get(domain)
                        if rank:
                            alexa_rank['alexa_rank'] = rank
                            break
                else:
                    raise AttributeError

            except AttributeError:
                domains = ['%s.%s' % ('.'.join(level_domain[:-1][n:]), level_domain[-1]) for n in
                           range(level_domain_length - 1)]

                # Sometimes trouble reading file / index out of range
                try:
                    self.AlexaDatabase()
                    for ranking in self.AlexaDB:
                        for domain in domains:
                            if domain == ranking[1]:
                                alexa_rank['alexa_rank'] = int(ranking[0])
                                break

                except IndexError:
                    pass

        return alexa_rank

    def get_opendns_rank(self):
        """
        Get the opendns rank of the first and second level domain (ie: google.com).
        Rank will be based on the max of the sixth level domain and will iterate all the way down to the
        first and second level.
        ie: www.google.com would match google.com in the database.

        Returns:
            Dictionary: {'opendns_rank': Int(OpenDNSRank)}

        >>> from domaininformation import DomainInformation
        >>> print DomainInformation(domain_name='www.google.com').get_opendns_rank()
            {'opendns_rank': 1}
        >>> print DomainInformation(domain_name='NotADomain').get_opendns_rank()
            "notadomain" Is not a domain
            {'opendns_rank': None}
        """
        opendns_rank = {'opendns_rank': None}

        if self.IsDomain:
            level_domain = self.domain_name.split('.')[-6:]
            level_domain_length = len(level_domain)

            try:
                if self.OpenDNSDB:
                    for n in range(level_domain_length - 1):
                        domain = '%s.%s' % ('.'.join(level_domain[:-1][n:]), level_domain[-1])
                        rank = self.OpenDNSDB.get(domain)
                        if rank:
                            opendns_rank['opendns_rank'] = rank
                            break
                else:
                    raise AttributeError

            except AttributeError:
                domains = ['%s.%s' % ('.'.join(level_domain[:-1][n:]), level_domain[-1]) for n in
                           range(level_domain_length - 1)]

                # Sometimes trouble reading file / index out of range
                try:
                    self.OpenDNSDatabase()
                    for ranking in self.OpenDNSDB:
                        for domain in domains:
                            if domain == ranking[1]:
                                opendns_rank['opendns_rank'] = int(ranking[0])
                                break

                except IndexError:
                    pass

        return opendns_rank

    def is_domain(self):
        return self.IsDomain