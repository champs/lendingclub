from dateutil.parser import parse
import datetime
from pytz import timezone, UTC
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
