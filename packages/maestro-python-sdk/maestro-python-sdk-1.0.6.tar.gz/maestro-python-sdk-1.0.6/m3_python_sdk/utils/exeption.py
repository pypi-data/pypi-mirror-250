class ApplicationException(Exception):

    def __init__(self, code=None, content=None):
        self.code = code
        self.content = content

    def __str__(self):
        return f'{self.code}:{self.content}'


def raise_application_exception(code=None, content=None):
    raise ApplicationException(code=code, content=content)
