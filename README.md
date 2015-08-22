# lendingclub
API for lendingclub

## required:
pip install requests

## Install:
python setup.py install

## Usage:
```
from lendingclub import LendingClub
lc = LendingClub(investor_id=999999999, token='<auth_token>')
print lc.summary()
{u'accountTotal': 5107.35, u'receivedLateFees': 0, u'receivedInterest': 111.74, u'infundingBalance': 225,
u'outstandingPrincipal': 4831.93, u'investorId': 999999, u'receivedPrincipal': 518.07, u'accruedInterest': 24.79,
u'availableCash': 50.42, u'totalPortfolios': 3, u'totalNotes': 170}

```
> auth_token is an authentication token generated via the Lending Club web application.

## Available Commands
```
from lendingclub import api
* api.summary()
* api.availablecash()
* api.notes()
* api.detailednotes()
* api.portfolios()
* api.loanlisting()
## Notes, Loans objects
* api.get_loans() 				# return list of loans
* api.get_notes()				# return list of notes
* api.get_detailednotes()		# return list of detailednotes
```

## Reference:
https://www.lendingclub.com/developers/lc-api.action
https://www.lendingclub.com/info/download-data.action

## Analysis
### estimate_daily_payment 
```
notes = lc.get_detailednotes()
payments = lendingclub.NotesAnalytic(notes).get_daily_payments()
print json.dumps(payments, indent=3)
{
   "2015-08-25T00:00:00.000-07:00": 4.65, 
   "2015-08-26T00:00:00.000-07:00": 5.57, 
   "2015-08-27T00:00:00.000-07:00": 15.866805555555555, 
   "2015-08-28T00:00:00.000-07:00": 9.082569444444445, 
   "2015-08-31T00:00:00.000-07:00": 5.9, 
   "2015-09-01T00:00:00.000-07:00": 8.17, 
   "2015-09-02T00:00:00.000-07:00": 1.56, 
   "2015-09-03T00:00:00.000-07:00": 3.95, 
   "2015-09-08T00:00:00.000-07:00": 15.23, 
   "2015-09-09T00:00:00.000-07:00": 0.84, 
   "2015-09-10T00:00:00.000-07:00": 1.53, 
   "2015-09-11T00:00:00.000-07:00": 8.58, 
   "2015-09-14T00:00:00.000-07:00": 1.68, 
   "2015-09-15T00:00:00.000-07:00": 9.400000000000002, 
   "2015-09-16T00:00:00.000-07:00": 0, 
   "2015-09-17T00:00:00.000-07:00": 9.430000000000001, 
   "2015-09-18T00:00:00.000-07:00": 1.66, 
   "2015-09-21T00:00:00.000-07:00": 41.449999999999996, 
   "2015-09-22T00:00:00.000-07:00": 6.31, 
   "2015-09-23T00:00:00.000-07:00": 0, 
   "2015-09-24T00:00:00.000-07:00": 5.6000000000000005
}
```

## Todo
- Data Analysis on old loans, find the pattern of defaults.
- generate static file to store summary, and render graph based on summary history
- filtered loan listing, with filter terms.
- Buy Notes (using loan ids)
