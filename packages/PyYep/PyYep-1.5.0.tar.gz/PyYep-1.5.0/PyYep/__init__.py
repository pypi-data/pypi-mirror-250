"""
Allows simple schema parsing and validation for inputs.

Classes:
    Schema
    InputItem
    StringValidator
    NumericValidator
    BooleanValidator
    ArrayValidator
    DictValidator
    ValidationError
"""

from __future__ import annotations
from typing import (
    Any,
    List,
    Callable,
    Self,
    TypeVar,
    TypedDict,
    Generic,
    TYPE_CHECKING,
    cast,
)
from PyYep.validators.string import StringValidator
from PyYep.validators.numeric import NumericValidator
from PyYep.validators.bool import BooleanValidator
from PyYep.validators.array import ArrayValidator
from PyYep.validators.dict import DictValidator
from PyYep.exceptions import ValidationError

if TYPE_CHECKING:
    from PyYep.validators.validator import Validator


DataContainerT = TypeVar("DataContainerT")
T = TypeVar("T", bound=Any)
R = TypeVar("R", bound=TypedDict)


class Schema(Generic[R]):
    """
    A class to represent a schema.

    ...

    Attributes
    ----------
    _inputs: Union[List[InputItem], List[Validator]]
            the schema inputs
    on_fail: Callable[[], None]
            a callable to be used as a error hook
    abort_early: bool
            sets if the schema will raise a exception soon after
            a validation error happens

    Methods
    -------
    validate():
            Execute the inputs validators and return a dict containing all the
            inputs' values
    """

    def __init__(
        self,
        inputs: List[Validator | InputItem],
        on_fail: Callable[[], None] | None = None,
        abort_early: bool | None = True,
    ) -> None:
        """
        Constructs all the necessary attributes for the schema object.

        Parameters
        ----------
                inputs (Union[List[InputItem], List[Validator]]):
                    the schema inputs
                on_fail (Callable[[], None]):
                    a callable to be used as a error hook
                abort_early (bool):
                    sets if the schema will raise a exception soon after
                    an error happens
        """

        for item in inputs:
            item.set_schema(self)

        self._inputs = inputs
        self.on_fail = on_fail
        self.abort_early = abort_early

    def validate(self) -> R:
        """
        Execute the inputs validators and return a dict containing
        all the inputs' values

        Raises
        -------
        ValidationError: if any validation error happens in the
        inputs validation methods

        Returns
        -------
        result (R): a dict containing all the validated values
        """

        result = {}
        errors = []

        for item in self._inputs:
            try:
                result[item.name] = item.verify()
            except ValidationError as error:
                if self.abort_early:
                    raise error

                if error.inner:
                    errors.extend(error.inner)
                    continue

                errors.append(error)

        if not self.abort_early and errors:
            raise ValidationError(
                "", "One or more inputs failed during validation", inner=errors
            )

        return cast(R, result)


class InputItem(Generic[T]):
    """
    A class to represent a input item.

    ...

    Attributes
    ----------
    name: str
            the name of the input item
    _schema: Schema
            the parent schema
    data_container: DataContainerT
            the object containing the data to be validated
    _path: str
            the property or method name that store the value within
            the data_container
    _validators: List[Callable[[T], None]]
            a list of validators
    on_success: Callable[[], None]
            a callable used as a local success hook
    on_fail: Callable[[], None]
            a callable used as a local error hook

    Methods
    -------
    set_schema(form):
            Set the parent schema of the input item

    verify(result):
            Execute the inputs validators and return the result

    validate(validator):
            receives a validator and appends it on the validators list

    condition(condition):
            Set a condition for the execution of the previous validator

    modifier(modifier):
            Set a modifier to allow changes in the value after validation

    string():
            create a StringValidator using the input item as base

    number():
            create a NumericValidator using the input item as base
    """

    def __init__(
        self,
        name: str,
        data_container: DataContainerT,
        path: str,
        on_success: Callable[[], None] | None = None,
        on_fail: Callable[[], None] | None = None,
    ) -> None:
        """
        Constructs all the necessary attributes for the input item object.

        Parameters
        ----------
                name (str):
                    the name of the input item
                data_container (DataContainerT):
                    the input itself
                path (str):
                    the input's property or method name that store the value
                on_success (Callable[[], None]):
                    a callable to be used as a local success hook
                on_fail (Callable[[], None]):
                    a callable to be used as a local error hook
        """

        self.name = name
        self._schema = None
        self.data_container = data_container
        self._path = path

        self._validators = []
        self._conditions = {}
        self._modifier = None
        self.on_fail = on_fail
        self.on_success = on_success

    def set_data_container(
        self, name: str, data_container: DataContainerT, path: str
    ) -> None:
        """
        Sets the item

        Parameters
        ----------
                name (str):
                    the name of the input item
                data_container (DataContainerT):
                    the object containing the data to be validated
                path (str):
                    the input's property or method name that store the value
        """

        self.name = name
        self.data_container = data_container
        self._path = path

    def set_schema(self, form: Schema) -> None:
        """
        Set the parent schema of the input item

        Parameters
        ----------
        form : Schema
                the input item parent schema

        Returns
        -------
        None
        """

        self._schema = form

    def verify(self, result: T | None = None) -> T | None:
        """
        Get the input value and execute all the validators

        Parameters
        ----------
        result : Optional[T]
                the value stored on the input, if not passed it will use
                the value returned by the method or attribute with the name
                stored on the input item _path attribute

        Raises:
        _______
        ValidationError:
                if any error happens during the validation process

        Returns
        -------
        result (T): The value received after all the validation
        """

        if result is None:
            result = self.get_container_value()

        for validator in self._validators:
            if validator in self._conditions and not self._conditions[
                validator
            ](result):
                continue

            try:
                validator(result)
            except ValidationError as error:
                if self.on_fail is not None:
                    self.on_fail()
                elif (
                    self._schema is not None
                    and self._schema.on_fail is not None
                ):
                    self._schema.on_fail()

                raise error

        if self.on_success is not None:
            self.on_success()

        if self._modifier is not None:
            return self._modifier(result)

        return result

    def get_container_value(self) -> T:
        value = getattr(self.data_container, self._path)

        if callable(value):
            return value()

        return value

    def validate(self, validator: Callable[[T], None]) -> Self:
        """
        Append a validator in the input item validators list

        Returns
        -------
        self (InputItem): The input item itself
        """

        self._validators.append(validator)
        return self

    def condition(self, condition: Callable[[T], bool]) -> Self:
        """
        Set a condition for the execution of the previous validator

        Parameters
        ----------
        condition : Callable
                a callable that return a boolean that defines if the condition
                was satisfied

        Returns
        -------
        InputItem
        """

        self._conditions[self._validators[-1]] = condition
        return self

    def modifier(self, modifier: Callable[[T | None], T | None]) -> Self:
        """
        Set a modifier to allow changes in the value after validation

        Parameters
        ----------
        modifier : Callable
                a callable that executes changes in the value after validation

        Returns
        -------
        InputItem
        """

        self._modifier = modifier
        return self

    def string(self) -> StringValidator[T]:
        """
        create a StringValidator using the input item as base

        Returns
        -------
        result (StringValidator): A string validator object
        """
        return StringValidator[T](self)

    def number(self) -> NumericValidator[T]:
        """
        create a NumericValidator using the input item as base

        Returns
        -------
        result (NumericValidator): A numeric validator object
        """
        return NumericValidator[T](self)

    def bool(self, strict: bool = False) -> BooleanValidator[T]:
        """
        create a BooleanValidator using the input item as base

        Returns
        -------
        result (BooleanValidator): A boolean validator object
        """
        return BooleanValidator[T](strict, self)

    def array(self) -> ArrayValidator[T]:
        """
        create a ArrayValidator using the input item as base

        Returns
        -------
        result (ArrayValidator): An array validator object
        """
        return ArrayValidator[T](self)

    def dict(self) -> DictValidator[T]:
        """
        create a DictValidator using the input item as base

        Returns
        -------
        result (DictValidator): A dict validator object
        """
        return DictValidator[T](self)
