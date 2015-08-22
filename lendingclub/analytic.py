#!/usr/bin/env python


class BaseAnalytic:

    def __init__(self):
        pass

    def filter(self, filter_dict):
        pass


class NotesAnalytic(BaseAnalytic):

    def __init__(self, detailednotes):
        self.notes = detailednotes
    	

class LoansAnalytic(BaseAnalytic):

    def __init__(self, loans):
        pass
