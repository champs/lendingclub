#!/usr/bin/env python

import json
import datetime


class AttrError(Exception):
    pass


class BaseObject(object):

    def __init__(self, dict_obj):
        self.__dict__ = dict_obj

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except:
            raise AttrError('{} does not exists')

    def dumps(self):
    	print json.dumps(self.__dict__, indent=3)

class Note(BaseObject):

    """
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

    """
    {
            "loanId":11111,
            "noteId":22222,
            "orderId":33333,
            "purpose":"Debt consolidation",
            "interestRate":13.57,
            "loanLength":36,
            "loanStatus":"Late (31-120 days)",
            "grade":"C3",
            "currentPaymentStatus":"Not Received",
            "canBeTraded":true,
            "creditTrend":"DOWN",
            "loanAmount":10800,
            "noteAmount":25,
            "paymentsReceived":5.88,
            "accruedInterest":12.1,
            "principalPending":20.94,
            "interestPending":0,
            "principalReceived":4.06,
            "interestReceived":1.82,
            "nextPaymentDate":"2014-05-15T00:00:00.000-07:00",
            "issueDate":"2009-11-12T00:00:00.000-08:00",
            "orderDate":"2009-11-05T00:00:00.000-08:00",
            "loanStatusDate":"2013-05-20T00:00:00.000-07:00"
    }
    """
    def __str__(self):
    	return '<DetailedNote: {}>'.format(self.noteId)


class Loan(BaseObject):

    """
    {
            "id":111111,
            "memberId":222222,
            "loanAmount":1750.0,
            "fundedAmount":25.0,
            "term":36,
            "intRate":10.99,
            "expDefaultRate":3.5,
            "serviceFeeRate":0.85,
            "installment":57.29,
            "grade":"B",
            "subGrade":"B3",
            "empLength":0,
            "homeOwnership":"OWN",
            "annualInc":123432.0,
            "isIncV":"Requested",
            "acceptD":"2014-08-25T10:56:29.000-07:00",
            "expD":"2014-09-08T10:57:13.000-07:00",
            "listD":"2014-08-25T10:50:20.000-07:00",
            "creditPullD":"2014-08-25T10:56:18.000-07:00",
            "reviewStatusD":"2014-09-03T14:41:53.957-07:00",
            "reviewStatus":"NOT_APPROVED",
            "desc":"Loan description",
            "purpose":"debt_consolidation",
            "addrZip":"904xx",
            "addrState":"CA",
            "investorCount":"",
            "ilsExpD":"2014-08-25T11:00:00.000-07:00",
            "initialListStatus":"F",
            "empTitle":"",
            "accNowDelinq":"",
            "accOpenPast24Mths":23,
            "bcOpenToBuy":30000,
            "percentBcGt75":23.0,
            "bcUtil":23.0,
            "dti":0.0,
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
