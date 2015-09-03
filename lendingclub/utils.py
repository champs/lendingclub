from dateutil.parser import parse
import datetime
from pytz import timezone, UTC
import urllib
import urllib2
import cookielib

PROXY_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


def get_time_now():
    """
    This will return the current UTC time, which will include UTC info
    """
    return datetime.datetime.utcnow().replace(tzinfo=UTC)


def parse_time(date_str):
    if not date_str:
        return None
    return parse(date_str)


def auth(login_url, username, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    params = {'login_url': '',
              'login_email': username,
              'login_password': password,
              'login_remember_me': 'on',
              'offeredNotListedPromotionFlag': ''}

    login_data = urllib.urlencode(params)
    resp = opener.open(login_url, login_data)
    print resp.read()
    return opener