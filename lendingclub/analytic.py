#!/usr/bin/env python

from collections import OrderedDict


class Filter:

    @classmethod
    def lt(cls, ele, val):
        return ele < val

    @classmethod
    def gt(cls, ele, val):
        return ele > val

    @classmethod
    def lte(cls, ele, val):
        return ele <= val

    @classmethod
    def gte(cls, ele, val):
        return ele >= val

    @classmethod
    def eq(cls, ele, val):
        return ele == val

    @classmethod
    def contain(cls, ele, vals):
        return ele in vals

FILTER_MAPPING = {'<': Filter.lt,
                  '>': Filter.gt,
                  '>=': Filter.gte,
                  '<=': Filter.lte,
                  '==': Filter.eq,
                  }


class BaseAnalytic:

    def __init__(self):
        pass

    # def filter(self, seq, rule):
    #     """ common filter function
    #             rule = ('attr', '>', 30)
    #             attr, filter, value
    #     """
    #     a, f, v = seq
    #     fn = FILTER_MAPPING[f]
    #     return filter(lambda x: fn(x.__getattr__(a))


class NotesAnalytic(BaseAnalytic):

    def __init__(self, detailednotes):
        self.notes = detailednotes

    def estimate_daily_payments(self):
        """ return dict of dates, and expect payment
        """
        result = {}
        for note in self.notes:
            if note.loanStatus in ("Issued", "Current"):
                nxt_pmt_date = note.nextPaymentDate
                nxt_pmt_amt = note.estimate_next_payment_amount()
                result[nxt_pmt_date] = result.get(
                    nxt_pmt_date, 0) + nxt_pmt_amt
        ordered = OrderedDict(sorted(result.items(), key=lambda t: t[0]))
        return ordered


class LoansAnalytic(BaseAnalytic):

    def __init__(self, loans):
        pass
