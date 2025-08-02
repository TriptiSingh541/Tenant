import requests
from functools import wraps
from django.core.cache import cache
import time
import logging
logger=logging.getLogger("django")

MONITORED_DOMAINS = ['auth-service.com', 'billing-api.com']
ERROR_THRESHOLD = 3
COOLDOWN_TIME = 120  # seconds
WINDOW = 60  # seconds

def circuit_breaker(domain):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cache.get(f'cb_open:{domain}', False):
                logger.warning(f"[CIRCUIT BLOCKED] Request to {domain} blocked")
                raise Exception(f"Circuit open for {domain}")
            
            try:
                response = func(*args, **kwargs)
                if response.status_code >= 500:
                    _record_failure(domain)
                return response
            except requests.exceptions.RequestException:
                _record_failure(domain)
                raise
        return wrapper
    return decorator

def _record_failure(domain):
    key = f'cb_failures:{domain}'
    now = time.time()
    failures = cache.get(key, [])
    failures = [f for f in failures if now - f < WINDOW]
    failures.append(now)
    cache.set(key, failures, timeout=WINDOW)

    if len(failures) >= ERROR_THRESHOLD:
        cache.set(f'cb_open:{domain}', True, timeout=COOLDOWN_TIME)
        logger.warning(f"[CIRCUIT OPENED] Circuit opened for {domain}")