from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import requests

# Role-permission mapping
role_permissions = {
    'admin': {
        'abc': {
            'dashboard': ['read', 'write'],
            'reports': ['read'],
        }
    },
    'viewer': {
        'abc': {
            'dashboard': ['read'],
        }
    }
}
AUTH_SERVICE_URL = "http://localhost/auth/check_permission/"

def has_permission(user_id, tenant, role, product_id, feature, permission):
    payload = {
        "user_id": user_id,
        "tenant": tenant,
        "role": role,
        "product_id": product_id,
        "feature": feature,
        "permission": permission
    }
    try:
        response = requests.post(AUTH_SERVICE_URL, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get("allowed", False)
        return False
    except requests.RequestException:
        return False


def check_permission(product_id, feature, permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user

            tenant = request.headers.get('Tenant', 'skewb') 
            role = request.headers.get('Role', 'admin')      
            payload = {
                "user_id": user.id,
                "tenant": tenant,
                "role": role,
                "product_id": product_id,
                "feature": feature,
                "permission": permission
            }

            try:
                response = requests.post(AUTH_SERVICE_URL, json=payload, timeout=5)
                if response.status_code == 200 and response.json().get("allowed", False):
                    return view_func(self, request, *args, **kwargs)
                else:
                    return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            except requests.RequestException:
                return Response({"detail": "Auth service unreachable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return _wrapped_view
    return decorator