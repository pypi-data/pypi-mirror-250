# PyYep [![CI](https://github.com/danielmbomfim/PyYep/actions/workflows/ci.yaml/badge.svg)](https://github.com/danielmbomfim/PyYep/actions/workflows/ci.yaml) ![PyPI - Version](https://img.shields.io/pypi/v/pyyep) [![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release) [![Coverage Status](https://coveralls.io/repos/github/danielmbomfim/PyYep/badge.svg?branch=master)](https://coveralls.io/github/danielmbomfim/PyYep?branch=master)

PyYep is a python schema builder for value parsing and validation. Define a schema, transform a value to match and validate the inputs with existing validator or custom functions.

PyYep is heavily inspired by [Yup](https://github.com/jquense/yup)

[Docs](https://danielmbomfim.github.io/PyYep/)

## Install

```sh
pip install PyYep
```

## Getting Started

### Basic usage

There are two ways of defining an schema, using the Schema and the InputItem objects or using an DictValidator to define the schema directly. On both methods you can chain multiple validation methods

#### Validation using the Schema and InputItem objects

You define and create schema objects with its inputs and validation methods. Then use the verify method to check the schema. A ValidationError will be raised if some input value does not match the validation.

```python
from PyYep import Schema, InputItem, ValidationError

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.string().email().required(),
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.number().min(10).max(100).required(),
], abort_early=False) 

# check validity

try:
	result = schema.validate()
	# handle result
except ValidationError:
	# handle fail
```

#### Validation using the DictValidator directly

You can also define the schema directly using the shape method of a DictValidator as shown bellow.

```python
from PyYep import DictValidator, StringValidator, NumericValidator, ArrayValidator, ValidationError

schema = DictValidator().shape({
	"string": StringValidator().email().required(),
	"number": NumericValidator().min(8).max(10).required(),
	"list": ArrayValidator().of(
		NumericValidator().max(3).required()
	).min(1).required(),
})

# check validity
data = { "string": "test", "number": 10, "list": [1, 2, 3] }

try:
	result = schema.verify(data)
	# handle result
except ValidationError:
	# handle fail
```

## Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [API](#api)
  - [String validation](#string-validation)
    - [email](#email)
    - [min](#min)
    - [max](#max)
  - [Number validation](#number-validation)
    - [min](#min-1)
    - [max](#max-1)
  - [Array validation](#array-validation)
    - [of](#of)
    - [includes](#includes)
    - [len](#len)
    - [min](#min-2)
    - [max](#max-2)
  - [Dict validation](#dict-validation)
    - [shape](#shape)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## API

### String validation

#### email

Validates the value as an email address.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.string().email()
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"string": StringValidator().email(),
})
```

#### min

Set a minimum length limit for the string value.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.string().min(8)
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"string": StringValidator().min(8),
})
```

#### max

Set a maximum length limit for the string value.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.string().max(10)
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"string": StringValidator().max(10),
})
```

### Number validation

#### min

Set the minimum value allowed.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.number().min(5)
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"number": NumericValidator().min(5),
})
```

#### max

Set the maximum value allowed.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.number().max(10)
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"number": NumericValidator().max(10),
})
```

### Array validation

#### of

Specify the schema of iterable elements.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.array().of(NumericValidator().required())
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"array": ArrayValidator().of(
		NumericValidator().required()
	),
})
```

#### includes

Requires the iterable to have a defined value as one of its values.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.array().includes("value")
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"array": ArrayValidator().includes("value"),
})
```

#### len

Set a specific length requirement for the iterable.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.array().len(3)
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"array": ArrayValidator().len(3),
})
```

#### min

Set a minimum length limit for the iterable.

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.array().min(5)
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"array": ArrayValidator().min(5),
})
```

#### max

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.array().max(5)
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"array": ArrayValidator().max(5),
})
```

Set a minimum length limit for the iterable.

### Dict validation

#### shape

Define the keys of the dict and the schemas for said keys

```python
# Example using the Schema and InputItem objects.

schema = Schema([
	InputItem("name", input_object, "path-to-input_object-value-property-or-method")
		.dict().shape({ "value": StringValidator().required() })
])
```

```python
# Example using the DictValidator.

schema = DictValidator().shape({
	"value": StringValidator().required()
})
```