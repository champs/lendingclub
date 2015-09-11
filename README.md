# lendingclub
API for lendingclub

## required:
pip install -r requirement.pip

## Install:
python setup.py install

## Usage 
- view Summary: 
```
from lendingclub import LendingClub
lc = LendingClub(investor_id=999999999, token='<auth_token>')
print lc.summary()
{u'accountTotal': 5107.35, u'receivedLateFees': 0, u'receivedInterest': 111.74, u'infundingBalance': 225,
u'outstandingPrincipal': 4831.93, u'investorId': 999999, u'receivedPrincipal': 518.07, u'accruedInterest': 24.79,
u'availableCash': 50.42, u'totalPortfolios': 3, u'totalNotes': 170}

```
- view current Note status:
```
notes = lc.get_detailednotes()
payments = lendingclub.NotesAnalytic(notes).estimate_daily_payments()
print '- income', '-' * 40
print json.dumps(payments, indent=3)
print '- stats', '-' * 40
result = lendingclub.NotesAnalytic(notes).report_note_stats()
print json.dumps(result, indent=3)
print '- sell list', '-' * 40
lendingclub.NotesAnalytic(notes).sell_list(x=10)

- income ----------------------------------------
{
   "2015-09-11T00:00:00.000-07:00": 7.056805555555554, 
   "2015-09-14T00:00:00.000-07:00": 0.85, 
   "2015-09-15T00:00:00.000-07:00": 9.400000000000002, 
   "2015-09-16T00:00:00.000-07:00": 5.262708333333334, 
   "2015-09-17T00:00:00.000-07:00": 10.260000000000002, 
   "2015-09-18T00:00:00.000-07:00": 1.66, 
   "2015-09-21T00:00:00.000-07:00": 19.51, 
   "2015-09-22T00:00:00.000-07:00": 6.31, 
   "2015-09-23T00:00:00.000-07:00": 4.9, 
   "2015-09-24T00:00:00.000-07:00": 15.669999999999998, 
   "2015-09-28T00:00:00.000-07:00": 3.21, 
   "2015-09-29T00:00:00.000-07:00": 12.780000000000001, 
   "2015-09-30T00:00:00.000-07:00": 22.819999999999997, 
   "2015-10-01T00:00:00.000-07:00": 17.21701388888889, 
   "2015-10-02T00:00:00.000-07:00": 2.17, 
   "2015-10-05T00:00:00.000-07:00": 1.56, 
   "2015-10-06T00:00:00.000-07:00": 3.1900000000000004, 
   "2015-10-07T00:00:00.000-07:00": 15.64, 
   "2015-10-08T00:00:00.000-07:00": 7.49, 
   "2015-10-21T00:00:00.000-07:00": 0
}
- stats ----------------------------------------
{
   "lastpaymentdate": {
      "34": [
         "loan_id=51947491&order_id=70156699&note_id=84487450"
      ], 
      "35": [
         "loan_id=44239461&order_id=61385146&note_id=76307547"
      ]
   }, 
   "paymentstatus": {
      "Scheduled": 10, 
      "Paid Off": 5, 
      "Completed": 156, 
      "Processing...": 3, 
      "null": 1, 
      "Overdue": 1
   }, 
   "loanstatus": {
      "Current": 159, 
      "Issued": 10, 
      "In Review": 1, 
      "Fully Paid": 5, 
      "In Grace Period": 1
   }
}
- maturity ----------------------------------------
{
   "00/36": 8, 
   "01/36": 24, 
   "02/36": 38, 
   "03/36": 3, 
   "04/36": 22, 
   "05/36": 65, 
   "09/36": 1, 
   "10/36": 1, 
   "16/36": 1, 
   "18/36": 1, 
   "00/60": 7, 
   "01/60": 2, 
   "03/60": 1, 
   "04/60": 1, 
   "17/60": 1
}

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
