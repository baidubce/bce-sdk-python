# -*- coding: UTF-8 -*-
import hashlib
import hmac
import string
import datetime


AUTHORIZATION = "authorization"
BCE_PREFIX = "x-bce-"
DEFAULT_ENCODING = 'UTF-8'


# AK/SK Storage Class
class BceCredentials(object):
    def __init__(self, access_key_id, secret_access_key):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key


# Encode every character according to RFC 3986, except：
#   1.Alphabet in upper or lower case
#   2.Numbers
#   3.Dot '.', wave '~', minus '-' and underline '_'
RESERVED_CHAR_SET = set(string.ascii_letters + string.digits + '.~-_')
def get_normalized_char(i):
    char = chr(i)
    if char in RESERVED_CHAR_SET:
        return char
    else:
        return '%%%02X' % i
NORMALIZED_CHAR_LIST = [get_normalized_char(i) for i in range(256)]


def normalize_string(in_str, encoding_slash=True):
    if in_str is None:
        return ''

    # Encode unicode with UTF-8 before normalizing
    in_str = in_str.encode(DEFAULT_ENCODING) if isinstance(in_str, unicode) else str(in_str)

    if encoding_slash:
        encode_f = lambda c: NORMALIZED_CHAR_LIST[ord(c)]
    else:
        encode_f = lambda c: NORMALIZED_CHAR_LIST[ord(c)] if c != '/' else c

    return ''.join([encode_f(ch) for ch in in_str])


def get_canonical_time(timestamp=0):
    # return current timestamp by default
    if timestamp == 0:
        utctime = datetime.datetime.utcnow()
    else:
        utctime = datetime.datetime.utcfromtimestamp(timestamp)

    # Format of timestamp: [year]-[month]-[day]T[hour]:[minute]:[second]Z
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (
        utctime.year, utctime.month, utctime.day,
        utctime.hour, utctime.minute, utctime.second)


def get_canonical_uri(path):
    # Format of canonical URI: /{object}, will encode every character except slash '/'
    return normalize_string(path, False)


def get_canonical_querystring(params):
    if params is None:
        return ''

    # Processing every query string except authorization
    result = ['%s=%s' % (k, normalize_string(v)) for k, v in params.items() if k.lower != AUTHORIZATION]

    # Sort in alphabet order
    result.sort()

    # Catenate all strings with &
    return '&'.join(result)


def get_canonical_headers(headers, headers_to_sign=None):
    headers = headers or {}

    # If you don't specify header_to_sign, will use:
    #   1.host
    #   2.content-md5
    #   3.content-length
    #   4.content-type
    #   5.all the headers begin with x-bce-
    if headers_to_sign is None or len(headers_to_sign) == 0:
        headers_to_sign = {"host", "content-md5", "content-length", "content-type"}

    # Strip key in headers and change them to lower case
    # Convert value in headers to string and strip them
    f = lambda (key, value): (key.strip().lower(), str(value).strip())

    result = []
    for k, v in map(f, headers.iteritems()):
        # Headers begin with x-bce- should be in canonical headers in any case
        if k.startswith(BCE_PREFIX) or k in headers_to_sign:
            result.append("%s:%s" % (normalize_string(k), normalize_string(v)))

    # Sort in alphabet order
    result.sort()

    # Catenate all strings with \n
    return '\n'.join(result)


def sign(credentials, http_method, path, headers, params,
         timestamp=0, expiration_in_seconds=1800, headers_to_sign=None):
    headers = headers or {}
    params = params or {}

    # 1.Generate sign key
    # 1.1.Build auth-string，format：bce-auth-v1/{accessKeyId}/{timestamp}/{expirationPeriodInSeconds}
    sign_key_info = 'bce-auth-v1/%s/%s/%d' % (
        credentials.access_key_id,
        get_canonical_time(timestamp),
        expiration_in_seconds)
    # 1.2.Generate sign key with auth-string and SK using SHA-256
    sign_key = hmac.new(
        credentials.secret_access_key,
        sign_key_info,
        hashlib.sha256).hexdigest()

    # 2.Generate canonical uri
    canonical_uri = get_canonical_uri(path)

    # 3.Generate canonical query string
    canonical_querystring = get_canonical_querystring(params)

    # 4.Generate canonical headers
    canonical_headers = get_canonical_headers(headers, headers_to_sign)

    # 5.Generate string to sign with results from step 2,3 and 4
    string_to_sign = '\n'.join(
        [http_method, canonical_uri, canonical_querystring, canonical_headers])

    # 6.Generate signature with string to sign and sign key using SHA-256
    sign_result = hmac.new(sign_key, string_to_sign, hashlib.sha256).hexdigest()

    # 7.Catenate result string
    if headers_to_sign:
        # header to sign specified by caller
        result = '%s/%s/%s' % (sign_key_info, ';'.join(headers_to_sign), sign_result)
    else:
        # header to sign not specified by caller
        result = '%s//%s' % (sign_key_info, sign_result)

    return result

if __name__ == "__main__":
    credentials = BceCredentials("0b0f67dfb88244b289b72b142befad0c","bad522c2126a4618a8125f4b6cf6356f")
    http_method = "PUT"
    path = "/v1/test/myfolder/readme.txt"
    headers = {"host": "bj.bcebos.com",
               "content-length": 8,
               "content-md5": "0a52730597fb4ffa01fc117d9e71e3a9",
               "content-type":"text/plain",
               "x-bce-date": "2015-04-27T08:23:49Z"}
    params = {"partNumber": 9,
              "uploadId": "VXBsb2FkIElpZS5tMnRzIHVwbG9hZA"}
    timestamp = 1430123029
    result = sign(credentials, http_method, path, headers, params, timestamp)
    print result