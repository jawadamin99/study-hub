import time

from tasks.models import RequestLog


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        execution_time = time.time() - start_time

        if request.path.startswith("/admin/"):
            return response

        response_type = "slow" if execution_time > 0.5 else "ok"
        user = request.user if request.user.is_authenticated else None

        RequestLog.objects.create(
            user=user,
            method=request.method,
            path=request.path,
            execution_time=execution_time,
            status_code=response.status_code,
            response_type=response_type,
        )

        return response
