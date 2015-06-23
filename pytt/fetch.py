""" Module to fetch data from SSU
"""

import requests
import ConfigParser
import logging

from requests import ConnectionError


class SSUFetcher(object):
    """ Class to download data from SSU. Constist of
        fetch_genreal() - download data about departments
        fetch_department(tag) - get specific information
    """
    _logger = logging.getLogger()

    def __init__(self, url=None, propfile=None):
        """ Constructor of the downloader class
        Parameters:
            url (str): string to download from, optional, used for testing
            propfile (str): property file with credentials to access SSU and
        URL to use, optional.
        Can either use url or propfile. url is primary if both passed
        """
        if not url:
            config = ConfigParser.ConfigParser()
            config.read(propfile)
            try:
                self.gen_address = 'http://%s:%s@%s' % \
                (config.get('SSU', 'ssu_user'),
                 config.get('SSU', 'ssu_password'),
                 config.get('SSU', 'ssu_url'))
            except KeyError as error:
                raise IOError('Proprety file is corrupted: %s' % error)
        else:
            if not url.startswith('http'):
                self.gen_address = 'http://%s' % url
            else:
                self.gen_address = url

    def fetch_general(self):
        """ Get data about departments, their timetable types,
        information, etc.
        Returns:
            (dictionary) 'status': raw.status_code and 'data': raw.text
        """
        try:
            raw = requests.get(self.gen_address)
            success = True
            if raw.status_code != 200:
                raise ConnectionError()
        except ConnectionError as error:
            self._logger.critical('Downloading data of departments has'
                                  'failed %s (%s)', error, self.gen_address)
            success = False
        return dict(zip(['text', 'success'], [raw.text, success]))

    def fetch_department(self, tag):
        """ Get data about specific department, its groups and each group
        schedule
        Parameters:
            tag (str): tag of the department
        Returns:
            (dictionary) 'status': raw.status_code and 'data: raw.text
        """
        address = '%s?dep=%s' % (self.gen_address, tag)
        success = True
        try:
            raw = requests.get(address)
            if raw.status_code != 200:
                raise ConnectionError()
        except ConnectionError as error:
            self._logger.critical('Downloading data of groups has'
                                  'failed %s (%s)', error, address)
            success = False
        return dict(zip(['text', 'success'], [raw.text, success]))
