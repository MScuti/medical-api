class AuthCodeError(Exception):
    """ Raise if auth code is error"""


class UserAuthError(Exception):
    """ Raise if auth error by code """


class UserNotAuthError(Exception):
    """ Raise if user is not auth """


class UserNotAllowError(Exception):
    """ Raise if user is not auth """


class UserTokenInvalid(Exception):
    """ Raise if user token is invalid """


class PodTerminalPermDeny(Exception):
    """ Raise if Pod terminal permission deny """


class ServiceNotFound(Exception):
    """ Raise if Pod terminal permission deny """