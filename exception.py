class CommonException(Exception):

    def __init__(self, message='Internal Server Error', status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

class ImageTooSmall(CommonException):
    status_code = 400
    message = "Image too small for specified cols!"
