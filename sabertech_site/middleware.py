from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseNotFound


class SecurityThrottleMiddleware:
    """Per-instance throttle for obvious bot floods before requests hit views."""

    EXEMPT_PREFIXES = ('/static/', '/media/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_blocked_probe(request):
            return HttpResponseNotFound('Not found.')
        if self._should_throttle(request):
            response = HttpResponse('Too many requests. Please try again later.', status=429)
            response['Retry-After'] = '60'
            return response
        return self.get_response(request)

    def _is_blocked_probe(self, request):
        path = request.path.lower()
        return any(
            path.startswith(prefix.lower())
            for prefix in getattr(settings, 'SECURITY_BLOCKED_PATH_PREFIXES', ())
        )

    def _should_throttle(self, request):
        if not getattr(settings, 'SECURITY_THROTTLE_ENABLED', True):
            return False
        if request.path.startswith(self.EXEMPT_PREFIXES):
            return False

        ip_address = self._client_ip(request)
        checks = [
            ('all', settings.SECURITY_THROTTLE_GENERAL_LIMIT, settings.SECURITY_THROTTLE_GENERAL_WINDOW),
        ]

        if request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
            checks.append(('write', settings.SECURITY_THROTTLE_POST_LIMIT, settings.SECURITY_THROTTLE_POST_WINDOW))

        if request.path.startswith('/admin/'):
            checks.append(('admin', settings.SECURITY_THROTTLE_ADMIN_LIMIT, settings.SECURITY_THROTTLE_ADMIN_WINDOW))

        return any(
            self._is_limited(f'{scope}:{ip_address}', limit, window)
            for scope, limit, window in checks
        )

    def _is_limited(self, key, limit, window):
        cache_key = f'security-throttle:{key}'
        if cache.add(cache_key, 1, window):
            return False
        try:
            count = cache.incr(cache_key)
        except ValueError:
            cache.set(cache_key, 1, window)
            return False
        return count > limit

    def _client_ip(self, request):
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
