from json import dumps
from urllib.request import urlopen
from urllib.parse import urlencode, quote
from urllib.error import URLError, HTTPError


def myURLopen(url, data=None, ret=False, quote_data=None):
    if data is not None:
        data = urlencode({"code": data}).encode()
    elif quote_data is not None:
        url += quote(dumps(quote_data))
    try:
        with urlopen(url=url, data=data) as f:
            if ret:
                return f.read()
    except HTTPError as e:
        return e
    except URLError as e:
        return e.reason
