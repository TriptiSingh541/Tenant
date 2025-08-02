import logging
import os
import uuid
from threading import local

_thread_locals = local()

def set_trace_id(trace_id=None):
    """Set a trace ID in thread-local storage."""
    _thread_locals.trace_id = trace_id or str(uuid.uuid4())

def get_trace_id():
    """Retrieve the current trace ID from thread-local storage."""
    return getattr(_thread_locals, 'trace_id', 'no-trace')

class TraceLogFilter(logging.Filter):
    """Inject trace_id and service name into log records."""
    def filter(self, record):
        record.trace_id = get_trace_id()
        record.service = os.getenv("SERVICE_NAME", "unknown")
        return True
