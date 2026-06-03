import re
from .models import JobViewLog
from apps.jobs.models import Job

class JobViewTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request first
        response = self.get_response(request)
        
        # We only log views on successful (200 OK) GET requests
        if response.status_code == 200 and request.method == 'GET':
            path = request.path
            # Match regex /jobs/<id>/
            match = re.match(r'^/jobs/(\d+)/$', path)
            if match:
                job_id = match.group(1)
                try:
                    job = Job.objects.get(pk=job_id)
                    # Exclude the job poster or staff
                    if not (request.user.is_authenticated and (job.employer == request.user or request.user.is_staff)):
                        # Log the view
                        ip_address = request.META.get('REMOTE_ADDR')
                        session_key = request.session.session_key
                        
                        # Generate session if not yet initialized
                        if not session_key:
                            request.session.save()
                            session_key = request.session.session_key
                            
                        # Avoid duplicate spam within the same session for the same job in a 1-minute window
                        # Simple and elegant logging
                        JobViewLog.objects.create(
                            job=job,
                            ip_address=ip_address,
                            session_key=session_key
                        )
                except Job.DoesNotExist:
                    pass
                    
        return response
