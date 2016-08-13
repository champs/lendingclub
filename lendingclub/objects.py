#!/usr/bin/env python

import json
import datetime
from utils import get_time_now, parse_time, auth
import requests


class AttrError(Exception):
    pass


class BaseObject(object):
    """ Object Base Class
    """

    def __init__(self, dict_obj):
        self.__dict__ = dict_obj

    def __getattr__(self, name):
        try:
            val = self.__dict__[name]
            if type(val) == float:
                return round(val, 2)
            else:
                return val
        except KeyError:
            raise AttrError('{} does not exists [{}]'.format(
                name,
                self.__dict__.keys()))

    def __getitem__(self, name):
        return self.__dict__.get(name, None)

    def dumps(self):
        print json.dumps(self.__dict__, indent=3)

    def is_pass_filter(self, crit={}):
        """ crit = [ {'grade__gt': 'D',
                      ''}
                    ]
        """


class Summary(BaseObject):
    pass


class Note(BaseObject):
    """ 
    Note Object (meta data of each note)
    {
            "loanId":11111,
            "noteId":22222,
            "orderId":33333,
            "interestRate":13.57,
            "loanLength":36,
            "loanStatus":"Late (31-120 days)",
            "grade":"C",
            "loanAmount":10800,
            "noteAmount":25,
            "paymentsReceived":5.88,
            "issueDate":"2009-11-12T06:34:02.000-08:00",
            "orderDate":"2009-11-05T09:33:50.000-08:00",
            "loanStatusDate":"2013-05-20T13:13:53.000-07:00"
    }
    """

    def __str__(self):
        return '<Note: {}>'.format(self.noteId)


class DetailedNote(BaseObject):

    """ Detail Note Object provide all note attributes
    {
       "grade": "C1", 
       "loanId": 55555555, 
       "interestRate": 12.29, 
       "accruedInterest": 0.21, 
       "creditTrend": "UP", 
       "portfolioName": "xxxxxxxx", 
       "loanStatus": "Current", 
       "loanAmount": 10000, 
       "canBeTraded": true, 
       "loanStatusDate": "2015-04-24T00:00:00.000-07:00", 
       "interestPending": 0, 
       "lastPaymentDate": "2015-07-30T11:53:21.000-07:00", 
       "principalReceived": 2.49, 
       "nextPaymentDate": "2015-09-01T00:00:00.000-07:00", 
       "orderId": 11111111111, 
       "portfolioId": 11111111111, 
       "currentPaymentStatus": "Completed", 
       "purpose": "Debt consolidation", 
       "paymentsReceived": 3.44, 
       "noteAmount": 25, 
       "noteId": 11111111111, 
       "principalPending": 22.51, 
       "issueDate": "2015-03-26T00:00:00.000-07:00", 
       "interestReceived": 0.95, 
       "loanLength": 36, 
       "orderDate": "2015-03-20T00:00:00.000-07:00"
    }
    """

    def __str__(self):
        return '<DetailedNote: {}>'.format(self.noteId)

    def get_current_payment_number(self):
        """ return number of current payment
            calculate by:
            = number of month of (now() - orderdate) / 30
        """
        issueDate = parse_time(self.issueDate)
        lastPaymentDate = parse_time(self.lastPaymentDate)
        if not lastPaymentDate:
            return 0
        payment_no = (lastPaymentDate - issueDate).days / 30
        if lastPaymentDate and not payment_no:
            return 1
        else:
            return payment_no

    def estimate_next_payment_amount(self):
        """ return estimate payment for this note
            calculate by:
            = paymentReceived / payment_no
        """
        payment_no = self.get_current_payment_number()

        if self.loanStatus == "Fully Paid":
            return 0
        elif self.loanStatus not in ("Issue", "Current"):
            return 0
        elif not self.lastPaymentDate:
            return self.noteAmount * (100 + self.interestRate) / 100 / self.loanLength
        return round(self.paymentsReceived / payment_no, 2)

    def calculate_note_profit(self):
        """ calculate note's profit in percent %
        """
        return round(float(self.paymentsReceived - self.principalReceived) / self.noteAmount * 100.0, 2)

    def profitgain_sell(self, x=10):
        """ We should sell note when borrower paid half of the principal
            or profit reach x=10 percent
        """
        return (
            self.loanStatus == 'Current' and
            self.principalReceived > self.noteAmount / 2 or
            self.calculate_note_profit() > x)

    def cutloss_sell(self):
        return (
            self.loanStatus not in ['Issued', 'Current', 'Fully Paid'])

    def days_since_last_pmt(self):
        if not self.lastPaymentDate:
            return None
        return (get_time_now() - parse_time(self.lastPaymentDate)).days

    def url_params(self):
        return 'loan_id={}&order_id={}&note_id={}'.format(self.loanId, self.orderId, self.noteId)


class Loan(BaseObject):

    """
    https://www.lendingclub.com/developers/listed-loans.action
    {
            "id":111111,
            "memberId":222222,
            "loanAmount":1750.0,
            "fundedAmount":25.0,
            "term":36,                      **
            "intRate":10.99,                **
            "expDefaultRate":3.5,           **
            "serviceFeeRate":0.85,          **
            "installment":57.29,
            "grade":"B",                    **
            "subGrade":"B3",                **
            "empLength":0,                  **
            "homeOwnership":"OWN",          **
            "annualInc":123432.0,           **
            "isIncV":"Requested",
            "acceptD":"2014-08-25T10:56:29.000-07:00",
            "expD":"2014-09-08T10:57:13.000-07:00",
            "listD":"2014-08-25T10:50:20.000-07:00",
            "creditPullD":"2014-08-25T10:56:18.000-07:00",
            "reviewStatusD":"2014-09-03T14:41:53.957-07:00",
            "reviewStatus":"NOT_APPROVED",  
            "desc":"Loan description",      **
            "purpose":"debt_consolidation",
            "addrZip":"904xx",              **
            "addrState":"CA",               **
            "investorCount":"",             **
            "ilsExpD":"2014-08-25T11:00:00.000-07:00",
            "initialListStatus":"F",
            "empTitle":"",
            "accNowDelinq":"",              **
            "accOpenPast24Mths":23,
            "bcOpenToBuy":30000,
            "percentBcGt75":23.0,           **
            "bcUtil":23.0,                  **
            "dti":0.0,                      **
            "delinq2Yrs":1,
            "delinqAmnt":0.0,
            "earliestCrLine":"1984-09-15T00:00:00.000-07:00",
            "ficoRangeLow":750,
            "ficoRangeHigh":754,
            "inqLast6Mths":0,
            "mthsSinceLastDelinq":90,
            "mthsSinceLastRecord":0,
            "mthsSinceRecentInq":14,
            "mthsSinceRecentRevolDelinq":23,
            "mthsSinceRecentBc":23,
            "mortAcc":23,
            "openAcc":3,
            "pubRec":0,
            "totalBalExMort":13944,
            "revolBal":1.0,
            "revolUtil":0.0,
            "totalBcLimit":23,
            "totalAcc":4,
            "totalIlHighCreditLimit":12,
            "numRevAccts":28,
            "mthsSinceRecentBcDlq":52,
            "pubRecBankruptcies":0,
            "numAcctsEver120Ppd":12,
            "chargeoffWithin12Mths":0,
            "collections12MthsExMed":0,
            "taxLiens":0,
            "mthsSinceLastMajorDerog":12,
            "numSats":8,
            "numTlOpPast12m":0,
            "moSinRcntTl":12,
            "totHiCredLim":12,
            "totCurBal":12,
            "avgCurBal":12,
            "numBcTl":12,
            "numActvBcTl":12,
            "numBcSats":7,
            "pctTlNvrDlq":12,
            "numTl90gDpd24m":12,
            "numTl30dpd":12,
            "numTl120dpd2m":12,
            "numIlTl":12,
            "moSinOldIlAcct":12,
            "numActvRevTl":12,
            "moSinOldRevTlOp":12,
            "moSinRcntRevTlOp":11,
            "totalRevHiLim":12,
            "numRevTlBalGt0":12,
            "numOpRevTl":12,
            "totCollAmt":12
    }
    """

    def __str__(self):
        return '<Loan: {}>'.format(self.id)


class FolioLoan(BaseObject):

    """
    {
        "loanId": "28102419",
        "noteId": "58215920",
        "orderId": "50738493",
        "accruedInterest": 31.24,
        "status": "Current",
        "askPrice": 1989.93,
        "markupDiscount": 7.70,
        "ytm": 20.73,
        "daysSinceLastPayment": 20,
        "creditScoreTrend": "UP",
        "ficoRange": "735-739",
        "dateTimeListed": "2015-08-21",
        "neverLate": "true",
        "loanClass": "G1",
        "loanMaturity": 60,
        "originalNoteAmount": 2000.00,
        "interestRate": 2.00,
        "principalInterest": 
    },
    """

    def __str__(self):
        return '<FolioFn: {}/{}/{}>'.format(self.loanId,
                                            self.orderId,
                                            self.noteId)

    @property
    def daysSinceLastPayment(self):
        return self.__dict__.get('daysSinceLastPayment', 0)

    def construct_url(self):
        """
        https://www.lendingclub.com/foliofn/browseNotesLoanPerf.action?showfoliofn=true&loan_id=1593342&order_id=3469444&note_id=14470297
        """
        base = "https://www.lendingclub.com/foliofn/browseNotesLoanPerf.action?showfoliofn=true&"
        return "{}loan_id={}&order_id={}&note_id={}".format(base,
                                                            self.loanId,
                                                            self.orderId,
                                                            self.noteId)

    def get_loanlisting(self, email, password):
        login_url = 'https://www.lendingclub.com/account/login.action'
        opener = auth(login_url, email, password)
        print opener.get(self.consolidation())
