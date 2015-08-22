#!/usr/bin/env python

from collections import OrderedDict


class BaseAnalytic:

    def __init__(self):
        pass

    def filter(self, filter_dict):
        pass


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
            	result[nxt_pmt_date] = result.get(nxt_pmt_date, 0) + nxt_pmt_amt
        ordered = OrderedDict(sorted(result.items(), key=lambda t: t[0]))
        return ordered


class LoansAnalytic(BaseAnalytic):

    def __init__(self, loans):
        pass
