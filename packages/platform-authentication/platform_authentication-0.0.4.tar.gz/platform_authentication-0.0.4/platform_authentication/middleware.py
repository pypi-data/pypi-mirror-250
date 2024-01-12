#Python Imports
from abc import ABC, abstractmethod

#Django Imports
from django.http import JsonResponse
from django.urls import resolve

#Third-Party Imports
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

#Project-Specific Imports


#Relative Import
from .errors import AuthenticationErrorMessages



class JWTMiddleware(ABC):
    """
    Middleware for handling JSON Web Token (JWT) authentication.

    This middleware checks if the requested endpoint is excluded from JWT authentication
    based on the defined EXCLUDED_ENDPOINTS. If excluded, the request proceeds as usual.
    If not excluded, it attempts JWT authentication, and if successful, sets the user
    and token in the request. If authentication fails, it returns a 403 Forbidden response
    with error details.

    Attributes:
        get_response (callable): The next middleware or view in the request-response chain.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        endpoint = self._get_endpoint_name(request=request)
        if self._is_excluded_endpoint(endpoint=endpoint):
            response = self.get_response(request)
        else:
            try:
                auth = JWTAuthentication()
                auth_result = auth.authenticate(request)
                if auth_result is not None:
                    user, token = auth_result
                    request.user = user
                # else:
                #     response = self._build_no_token_response()
                #     return response
            except AuthenticationFailed as error:
                response = self._build_error_response(error)
                return response
            response = self.get_response(request)
        return response


    def _build_no_token_response(self):
        errors = AuthenticationErrorMessages().get_no_token_message()
        response_data = {"status": 403, "errors": errors}
        return JsonResponse(response_data, status=403)


    def _build_error_response(self, error):
        code = error.detail.get('code', [])
        errors = error.detail.get('detail', [])
        if code == "user_not_found":
            errors = AuthenticationErrorMessages().get_user_not_registred_message()
        response_data = {"status": 403, "errors": errors}
        return JsonResponse(response_data, status=403)

    def _get_endpoint_name(self, request):
        """Helper method to get the endpoint name from the request."""
        resolver_match = resolve(request.path_info)
        return resolver_match.route if resolver_match.route is not None else None

    @abstractmethod
    def _is_excluded_endpoint(self, endpoint):
        """Helper method to check if an endpoint is excluded from subscription checks."""
        pass
