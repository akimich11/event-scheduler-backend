class ObjectNotFoundError(Exception):
    pass


class CategoryNotFoundError(ObjectNotFoundError):
    pass


class IntervalNotFoundError(ObjectNotFoundError):
    pass


class StatusNotFoundError(ObjectNotFoundError):
    pass
