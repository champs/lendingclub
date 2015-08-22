#!/usr/bin/env python

import requests
import json
requests.packages.urllib3.disable_warnings()

__doc__ = """   Created-by: Peerakit Champ Somsuk
                
          """


class RequstError(Exception):
    pass


class LendingClub:

    """ from lendingclub import LendingClub
        lc = LendingClub(investor_id=999999999,
                         token="oBe+FFFF/FFFFFFFFfffFFFFFFFFF=")
    """

    def __init__(self, investor_id, token, version='v1'):
        self.api = 'https://api.lendingclub.com/api'
        self.investor_id = investor_id
        self.token = token
        self.version = version

    def _construct_base_url(self):
        return '{api}/investor/{version}/accounts/{investor_id}'.format(
            api=self.api,
            version=self.version,
            investor_id=self.investor_id)

    def _construct_loan_url(self):
        return '{api}/investor/{version}'.format(
            api=self.api,
            version=self.version)

    def get(self, endpoint, params={}, base=None):
        if not base:
            base = self._construct_base_url()
        url = '{base}/{endpoint}'.format(
            base=base,
            endpoint=endpoint)
        headers = {'Authorization': self.token,
                   'content-type': 'application/json'}
        response = requests.get(url,
                                headers=headers,
                                params=params)
        if response.status_code != 200:
            msg = '{}: {}'.format(response.status_code,
                                  response.content)
            raise RequstError(msg)
        return response.json()

    def summary(self):
        return self.get('summary')

    def availablecash(self):
        return self.get('availablecash')

    def notes(self):
        return self.get('notes')

    def detailednotes(self):
        return self.get('detailednotes')

    def portfolios(self):
        return self.get('portfolios')

    def loanlisting(self, show_all=False):
        if show_all:
            params = {'showAll': True}
        else:
            params = {}
        return self.get(
            'loans/listing',
            params=params,
            base=self._construct_loan_url(),
        )
