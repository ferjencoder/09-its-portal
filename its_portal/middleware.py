# its_portal/middleware.py

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


# Por haber creado un grupo/role admin, este middleware intenta arreglar el inicio del admin como user y el admin como http://127.0.0.1:8000/admin
class AdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, "session"):
            if request.path.startswith("/admin"):
                request.session_cookie_name = settings.ADMIN_SESSION_COOKIE_NAME
            else:
                request.session_cookie_name = settings.SESSION_COOKIE_NAME

    def process_response(self, request, response):
        if hasattr(request, "session_cookie_name"):
            response.set_cookie(
                request.session_cookie_name, request.session.session_key
            )
        return response
