import logging

class TraceIDLogFilter(logging.Filter):
    def filter(self, record):
        try:
            from threading import local
            from django.utils.deprecation import MiddlewareMixin
            thread_local = MiddlewareMixin.thread_local
            record.trace_id = getattr(thread_local, 'trace_id', 'N/A')
        except Exception:
            record.trace_id = 'N/A'
        return True
