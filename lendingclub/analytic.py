#!/usr/bin/env python

from collections import OrderedDict
from utils import get_time_now, parse_time, auth


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
                if nxt_pmt_date:
                    result[nxt_pmt_date] = result.get(
                        nxt_pmt_date, 0) + nxt_pmt_amt
        ordered = OrderedDict(sorted(result.items(), key=lambda t: t[0]))
        return ordered

    def report_note_maturity(self):
        """ return
            {get_current_payment_number(): count}
        """
        result = {}
        for note in self.notes:
            cur_months = note.get_current_payment_number()
            cur_term = '{0:02d}/{1:02d}'.format(cur_months, note.loanLength)
            result[cur_term] = result.get(cur_term, 0) + 1

        ordered = OrderedDict(sorted(
            result.items(),
            key=lambda t: ''.join(t[0].split('/')[::-1])))

        return ordered

    def report_note_stats(self):
        """ return
            - loanstatus: count by loanstatus
            - paymentstatus: count by payment status
            - lastpayment date: date since last payment
                - 33 = 30 days + 3 processing date

        """
        loanstatus = {}
        paymentstatus = {}
        lastpaymentdate = {}
        for note in self.notes:
            loanstatus[note.loanStatus] = loanstatus.get(
                note.loanStatus, 0) + 1
            paymentstatus[note.currentPaymentStatus] = paymentstatus.get(
                note.currentPaymentStatus, 0) + 1
            if note.lastPaymentDate and note.loanStatus in ['Issued', 'Current']:
                day_since_last_pmt = note.days_since_last_pmt()
                if day_since_last_pmt >= 33: #
                    print note.__dict__
                    if day_since_last_pmt in lastpaymentdate:
                        lastpaymentdate[day_since_last_pmt].append(
                            note.url_params())
                    else:
                        lastpaymentdate[day_since_last_pmt] = [
                            note.url_params()]
        return {'loanstatus': loanstatus,
                'paymentstatus': paymentstatus,
                'lastpaymentdate': lastpaymentdate}

    def sell_list(self, x=10):
        """ Sell note if it reach (X) %
        """
        row_table = "{:<55} |" + "{:<10}" * 6
        for note in self.notes:
            if note.profitgain_sell():
                print row_table.format(note.url_params(),
                                       'profit',
                                       note.principalReceived,
                                       note.noteAmount,
                                       note.calculate_note_profit(),
                                       note.loanStatus,
                                       ''
                                       )
            if note.cutloss_sell():
                print row_table.format(note.url_params(),
                                       'cutloss',
                                       note.principalReceived,
                                       note.noteAmount,
                                       note.calculate_note_profit(),
                                       note.loanStatus,
                                       ' ({} days)'.format(
                    note.days_since_last_pmt())
                )


class LoansAnalytic(BaseAnalytic):

    def __init__(self, loans):
        self.loans = loans
