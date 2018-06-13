"""
Exception class
"""

class CommonException(Exception):
    """
    Base Class Exception
    """
    def __init__(self, message='Internal Server Error', status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or 500
        self.payload = payload


class BadRequest(CommonException):
    """
    Base Bad Request Exception
    """
    status_code = 400


class ImageTooSmall(BadRequest):
    """
    Bad Request Exception
    """
    message = "Image too small for specified cols!"


class FormValidationFailed(BadRequest):
    """
    Bad Request Exception
    """
    message = "Unrecognized error in form validation"
