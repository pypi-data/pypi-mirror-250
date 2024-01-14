from typing import List


class ValidationError(Exception):
    """
    A class to represent a validation error.

    ...

    Attributes
    ----------
    path : str
            the schema path of the input respnsable for the error
            or the schema name itself
    inner : Optional[List[ValidationError]]
            a list of inner error in case the exception is beeing raise for
            the schema and not a single input
    """

    def __init__(
        self,
        path: str,
        message: str,
        inner: List["ValidationError"] = [],
    ):
        """
        Constructs all the necessary attributes for the validation
        error object.

        Parameters
        ----------
                path (str): the schema path of the input that
                failed or the schema itself
                message (str): The error message
                inner (list): takes a list of the internal error in the schema
        """

        super(ValidationError, self).__init__(message)
        self._path = path
        self.inner = inner

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = path.replace("._PyYepBlank", "")
