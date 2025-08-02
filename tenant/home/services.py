from tenant.utils.circuit_breaker import circuit_breaker
import requests
@circuit_breaker('auth-service.com')
def call_auth_service():
    return requests.get("http://auth-service.com/api/check/")