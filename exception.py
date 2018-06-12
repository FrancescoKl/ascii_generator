class CommonException(Exception):

    def __init__(self, message='Internal Server Error', status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or 500
        self.payload = payload

class BadRequest(CommonException):
    status_code = 400

class ImageTooSmall(BadRequest):
    message = "Image too small for specified cols!"

class FormValidationFailed(BadRequest):
    message = "Unrecognized error in form validation"