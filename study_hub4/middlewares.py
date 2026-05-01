import time

from tasks.models import RequestLog


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time() - start_time
        print(f"METHOD: {request.method} PATH: {request.path} TOOK: ", end_time)

        response_type = "ok"
        if "/api/" in request.path.lower():
            if end_time >= 0.5:
                response_type = "slow"
            RequestLog(user_id=request.user.id, method=request.method, path=request.path, execution_time=end_time,
                       timestamp=time.time(), response_type=response_type
                       ).save()

        return response
