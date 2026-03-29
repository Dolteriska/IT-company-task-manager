from django.utils import timezone
from tasks.models import Worker


class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            (Worker.objects.filter(id=request.user.id)
             .update(last_seen=timezone.now()))
        return self.get_response(request)
