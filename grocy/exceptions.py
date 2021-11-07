class GrocyException(Exception):
    pass


class MissingConversionException(GrocyException):
    pass


class InvalidUnitException(GrocyException):
    pass
