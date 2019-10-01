import hmac
from hashlib import sha1
from ipaddress import ip_address, ip_network

import requests
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.encoding import force_bytes


def validate_request(view_method):
    def decorator(request):
        if not is_valid(request):
            return HttpResponseForbidden('Permission denied.')
        return view_method(request)
    return decorator


def is_valid(request):
    return all((validate_ip(request), validate_signature(request)))


def validate_ip(request):
    client_ip_address = ip_address(request.META['HTTP_X_FORWARDED_FOR'])
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            return True


def validate_signature(request):
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return False

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return False

    mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return False

    return True

