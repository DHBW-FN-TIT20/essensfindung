"""Contains all own created Exceptions"""


class NoResultsException(Exception):
    """Exception if the Search got no results"""


class GoogleApiException(NoResultsException):
    """Exception if some Error from the Google API request are made"""


class DatabaseException(Exception):
    """Exception for all Database Query"""


class UserNotFound(DatabaseException):
    """Exception of a DB Query if the User does not exist"""

    def __init__(self, error_msg: str, user: str) -> None:
        super().__init__(error_msg)
        self.user = user


class RestaurantNotFound(DatabaseException):
    """Exception of a DB Query if the User does not exist"""

    def __init__(self, error_msg: str, place_id: str) -> None:
        super().__init__(error_msg)
        self.place_id = place_id


class DuplicateEntry(DatabaseException):
    """Exception if you add a duplicate entry"""
