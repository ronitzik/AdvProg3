class ItemNotExistError(Exception):
    pass


class ItemAlreadyExistsError(Exception):
    pass


class TooManyMatchesError(Exception):
    pass

class ItemCanNotHaveNegativePrice(Exception):
    pass
