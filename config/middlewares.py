import re
import socket
from typing import List, Pattern

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden


class GlobalHostRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_limit = getattr(settings, "RATELIMIT_REQUESTS", 1000)
        self.timeframe = getattr(settings, "RATELIMIT_TIMEFRAME", 3600)
        # Load blacklist patterns from settings
        self.blacklist_patterns: List[Pattern] = []
        blacklist = getattr(settings, "HOSTNAME_BLACKLIST", [])
        for pattern in blacklist:
            try:
                self.blacklist_patterns.append(re.compile(pattern, re.IGNORECASE))
            except re.error:
                continue

    def is_blacklisted(self, hostname: str) -> bool:
        return any(pattern.search(hostname) for pattern in self.blacklist_patterns)

    def __call__(self, request):
        try:
            ip = request.META.get("REMOTE_ADDR")
            hostname = socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror):
            hostname = ip

        if self.is_blacklisted(hostname):
            return HttpResponseForbidden(
                "Access denied due to hostname restrictions", content_type="text/plain"
            )

        cache_key = f"rl:global:{hostname}"
        request_count = cache.get(cache_key, 0)

        if request_count >= self.requests_limit:
            return HttpResponse(
                "Global rate limit exceeded", content_type="text/plain", status=429
            )

        # Use atomic increment
        if not cache.add(cache_key, 1, timeout=self.timeframe):
            cache.incr(cache_key)

        return self.get_response(request)
