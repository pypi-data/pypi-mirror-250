"""request counter middleware"""
import redis
from django.conf import settings


class APICounterMiddleware:
    """api counter to store in redis"""

    RC_API_START_PATH = getattr(settings, "RC_RC_API_START_PATH", "/api/")
    RC_ENVIRONMENT_PREFIX = getattr(settings, "RC_ENVIRONMENT", "")

    def __init__(self, get_response):
        self.get_response = get_response
        url = getattr(settings, "REDIS_URL", "redis://localhost:6379/7")
        # Adjust connection settings
        self.redis_client = redis.from_url(url)

    def __call__(self, request):
        # Modify this path to match your API endpoints
        if request.path.startswith(self.RC_API_START_PATH):
            path = request.path
            if self.RC_ENVIRONMENT_PREFIX:
                path = f"{self.RC_ENVIRONMENT_PREFIX} {path}"
            self.increment_request_count(path)
        response = self.get_response(request)
        return response

    def increment_request_count(self, path):
        """Increment request count in Redis"""
        path_key = f"api_request_count:{path}"
        current_count = self.redis_client.get(path_key)
        if current_count is None:
            current_count = 0
        else:
            current_count = int(current_count)
        self.redis_client.set(path_key, current_count + 1)
