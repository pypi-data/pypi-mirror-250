class ProfileLimitReached(Exception):
    pass


class TooManyRequests(Exception):
    pass


class UnableToStartBrowser(Exception):
    pass


class UnableToStopBrowser(Exception):
    pass


class BadProxy(Exception):
    pass


class UnexpectedError(Exception):
    def __init__(self, json):
        self.json = json

    def __repr__(self):
        return self.json
