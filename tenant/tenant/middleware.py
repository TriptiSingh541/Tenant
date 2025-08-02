import uuid
from django.utils.deprecation import MiddlewareMixin

class TraceIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        request.trace_id = trace_id

        request.tenant_id = request.headers.get("X-Tenant-ID", "unknown")
        request.user_id = request.headers.get("X-User-ID", "anonymous")

    def process_response(self, request, response):
        if hasattr(request, "trace_id"):
            response["X-Trace-ID"] = request.trace_id
        return response
