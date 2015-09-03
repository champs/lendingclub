#!/usr/bin/env python

import requests
import json
from objects import Note, DetailedNote, Loan, FolioLoan
requests.packages.urllib3.disable_warnings()


class RequstError(Exception):
    pass


class API:
    """ Lending Club API """
    def __init__(self, investor_id, token, version='v1'):
        self.api = 'https://api.lendingclub.com/api'
        self.investor_id = investor_id
        self.token = token
        self.version = version
        # summary cache
        self._summary = None
        # loans/notes cache for analytics
        self._notes = None
        self._loans = None
        self._detailednotes = None

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
        if not self._summary:
            self._summary = self.get('summary')
        return self._summary

    def availablecash(self):
        return self.get('availablecash')

    def notes(self):
        if not self._notes:
            self._notes = self.get('notes')['myNotes']
        return self._notes

    def detailednotes(self):
        if not self._detailednotes:
            self._detailednotes = self.get('detailednotes')['myNotes']
        return self._detailednotes

    def portfolios(self):
        return self.get('portfolios')

    def loanlisting(self, show_all=False):
        if show_all:
            params = {'showAll': True}
        else:
            params = {}
        loans = self.get(
            'loans/listing',
            params=params,
            base=self._construct_loan_url(),
        )
        self._loans = loans['loans']
        return loans

    def get_notes(self):
        """ Return Note Objects
        """
        if not self._notes:
            self.notes()
        return [Note(n) for n in self._notes]

    def get_detailednotes(self):
        """ Return List of DetailedNote Objects
        """
        if not self._detailednotes:
            self.detailednotes()
        return [DetailedNote(n) for n in self._detailednotes]

    def get_loans(self):
        """ Return List of Loan Objects
        """
        if not self._loans:
            self.loanlisting()
        return [Loan(l) for l in self._loans]


class FolioFn:
    """ FolioFnAPI 
        http://www.foliofnapi.com/api.html
        The FOLIOfn API project is a Moran Nachum project.

    """
    def __init__(self, user=None, password=None):
        self.api = 'http://www.foliofnapi.com/get.php'
        self._loans = None
        self.user = user
        self.password = password

    def _getbody(self, content):
        begin = '<body>'
        end = '</body>'
        idx1 = content.find(begin)
        idx2 = content.find(end)
        content = content[idx1+len(begin):idx2].strip()
        content = content.replace('": <br/>}', '": null}')
        content = content.replace('<br/>', '')
        content = content.replace("}, ]", "}]")
        return content

    def get(self, params={}):
        url = self.api
        params.update({'format': 'JSON'})
        headers = {'content-type': 'application/json'}
        response = requests.get(url,
                                headers=headers,
                                params=params)
        if response.status_code != 200:
            msg = '{}: {}'.format(response.status_code,
                                  response.content)
            raise RequstError(msg)
        content = self._getbody(response.content)
        if content == 'No rows returned.':
            return {'notes': []}
        return json.loads(content)

    def filter(self, params):
        if not self._loans:
            self._loans = self.get(params)['notes']
        return [FolioLoan(l) for l in self._loans]

    def sorted(self, loanlist):
        return sorted(loanlist, key=lambda k: k['loanClass'], reverse=True)