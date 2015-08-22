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
{u'accountTotal': 5107.35, u'receivedLateFees': 0, u'receivedInterest': 111.74, u'infundingBalance': 225, u'outstandingPrincipal': 4831.93, u'investorId': 999999, u'receivedPrincipal': 518.07, u'accruedInterest': 24.79, u'availableCash': 50.42, u'totalPortfolios': 3, u'totalNotes': 170}

```
> auth_token is an authentication token generated via the Lending Club web application.

```
## Available Commands
from lendingclub import api
1. summary()
2. availablecash()
3. notes()
4. detailednotes()
5. portfolios()
6. loanlisting()
## Notes, Loans objects
7. get_loans()
8. get_notes()
9. get_detailednotes()
```

## Reference:
https://www.lendingclub.com/developers/lc-api.action
