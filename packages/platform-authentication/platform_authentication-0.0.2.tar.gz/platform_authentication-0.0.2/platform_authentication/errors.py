#Python Imports
from dataclasses import dataclass, field

#Django Imports

#Third-Party Imports

#Project-Specific Imports
from common_utils.errors import V2stechErrorMessageHandler,get_error_message

#Relative Import

class AuthenticationErrorMessageCodes:
    """
    Class that defines error codes related to OTP (One-Time Password) verification.
    This class manages error codes used in the OTP verification process.
    """
    INVALID_CREDENTIALS= "E0500"
    USER_NOT_REGISTED= "E0501"
    OTP_VERIFICATION_FAILED = "E0502"
    MOBILE_NUMBER_VALIDATION = "E0503"

    TOKEN_NOT_PROVIDED = "E0505"
    TOKEN_IS_INVALID = "E0506"


class AuthenticationErrorMessages(V2stechErrorMessageHandler):
    """
    Class that provides methods for generating OTP (One-Time Password) verification error messages.
    This class is responsible for handling and generating error messages related to OTP verification.
    """

    def get_otp_verification_failed_message(self):
        """
        Generate an error message for OTP verification failure.
        This method generates an error message specific to OTP verification failures.
        """
        self.add_message(AuthenticationErrorMessageCodes.OTP_VERIFICATION_FAILED, get_error_message(AuthenticationErrorMessageCodes.OTP_VERIFICATION_FAILED))
        return self.get_messages()


    def get_user_not_registred_message(self):
        """
        Generate an error message for OTP verification failure.
        This method generates an error message specific to OTP verification failures.
        """
        self.add_message(AuthenticationErrorMessageCodes.USER_NOT_REGISTED, get_error_message(AuthenticationErrorMessageCodes.USER_NOT_REGISTED))
        return self.get_messages()


    def get_invalid_credentials_message(self):
        """
        Generate an error message for OTP verification failure.
        This method generates an error message specific to OTP verification failures.
        """
        self.add_message(AuthenticationErrorMessageCodes.INVALID_CREDENTIALS, get_error_message(AuthenticationErrorMessageCodes.INVALID_CREDENTIALS))
        return self.get_messages()


    def get_mobile_number_validation_message(self):
        """
        Generate an error message for mobile number validation failure.
        This method generates an error message specific to mobile number validation failures.
        """
        self.add_message(AuthenticationErrorMessageCodes.MOBILE_NUMBER_VALIDATION, get_error_message(AuthenticationErrorMessageCodes.MOBILE_NUMBER_VALIDATION))
        return self.get_messages()
    
    def get_token_is_invalid_message(self):
        """
        Generate an error message if token is invalid.
        This method generates an error message specific to jwt token is invalid.
        """
        self.add_message(AuthenticationErrorMessageCodes.TOKEN_IS_INVALID, get_error_message(AuthenticationErrorMessageCodes.TOKEN_IS_INVALID))
        return self.get_messages()
    
    
    def get_no_token_message(self):
        """
        Generate an error message if no token is provided.
        This method generates an error message specific to jwt token not provided.
        """
        self.add_message(AuthenticationErrorMessageCodes.TOKEN_NOT_PROVIDED, get_error_message(AuthenticationErrorMessageCodes.TOKEN_NOT_PROVIDED))
        return self.get_messages()
    
    
class HandlerErrorMessageCodes:
    """Defines error codes for the error message handler."""
    HANDLER_404 = "E0000"

class HandlerErrorMessages(V2stechErrorMessageHandler):
    """Handles error messages and codes."""

    def get_handler_404_message(self):
        """Retrieves and adds a custom error message for the 404 error code."""
        self.add_message(HandlerErrorMessageCodes.HANDLER_404, get_error_message(HandlerErrorMessageCodes.HANDLER_404))
        return self.get_messages()
