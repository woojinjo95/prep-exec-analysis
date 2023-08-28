import ipaddress
import re
import socket
from urllib.parse import urlparse

# info와의 차이
# util.network는 동작 os, 위치, 상황에 관계 없이 일반적으로 다른 시스템에서 가공 없이 사용가능한 형태

# https://stackoverflow.com/a/55827638
url_domain_format = re.compile(
    r'(?:^(\w{1,255}):(.{1,255})@|^)'  # http basic authentication [optional]
    # check full domain length to be less than or equal to 253 (starting after http basic auth, stopping before port)
    r'(?:(?:(?=\S{0,253}(?:$|:))'
    # check for at least one subdomain (maximum length per subdomain: 63 characters), dashes in between allowed
    r'((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+'
    r'(?:[a-z0-9]{1,63})))'  # check for top level domain, no dashes allowed
    r'|localhost)'   # accept also 'localhost' only
    r'(:\d{1,5})?',  # port [optional]
    re.IGNORECASE
)
url_scheme_format = re.compile(
    r'^(http|hxxp|ftp|fxp)s?$',  # scheme: http(s) or ftp(s)
    re.IGNORECASE
)


def is_valid_ip_address(ip_str: any) -> bool:
    try:
        ipaddress.ip_address(str(ip_str))
        return True
    except ValueError:
        return False
    except:
        # not string or something
        return False


def check_ipv4(ip_str: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET, ip_str)
        return True
    except socket.error:
        return False


def check_ipv6(ip_str: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET6, ip_str)
        return True
    except socket.error:
        return False


def validate_url(url: str) -> tuple:
    url = url.strip()

    if not url:
        is_valid, message = False, 'No URL specified'
    elif len(url) > 2048:
        is_valid, message = False, f'URL exceeds its maximum length of 2048 characters (given length={len(url)})'
    else:
        result = urlparse(url)
        scheme = result.scheme
        domain = result.netloc

        if not scheme:
            is_valid, message = False, 'No URL scheme specified'
        elif not re.fullmatch(url_scheme_format, scheme):
            is_valid, message = False, f'URL scheme must either be http(s) or ftp(s) (given scheme={scheme})'
        elif not domain:
            is_valid, message = False, 'No URL domain specified'
        elif not re.fullmatch(url_domain_format, domain):
            is_valid, message = False, f'URL domain malformed (domain={domain})'
        else:
            is_valid, message = True, 'URL is valid'

    return is_valid, message
