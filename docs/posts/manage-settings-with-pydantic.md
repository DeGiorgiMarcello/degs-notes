---
draft: true 
date: 2024-10-18 
comments: true
authors:
  - MarcelloDeg
categories:
  - validation

tags:
  - pydantic
  - validation
  - env 

---

# Manage settings with Pydantic
[Pydantic](https://docs.pydantic.dev/latest/) is a wonderful library that allows to easily validate your data, simply defining a schema. It is highly customizable and can be used, for instance, to validate data coming from a POST request. 

In this tutorial we will use it to create a `Settings` class whose fields can be changed in different ways, triggering any time the validation. 

<!-- more -->

## Installation

From **v2**, pydantic has been split in `pydantic`, `pydantic-core` and `pydnatic-settings`. Let's install the latter one simply with:

`pip install pydantic-settings`.

## Class definition and usage
Let's start defining our class. It must extend the pydantic `BaseSettings` class. No `__init__` is here needed.

```py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    foo: int = 1
    bar: str = "eeee"
```

Extending the class and defining some fields with *type hinting* is sufficient to let pydantic trigger the validation anytime this values are changed.

We can change the values simply defining a new `Settings` object and passing some values for the fields. This is not so useful for our purpose but can help us to understand how the validation works.

```
Settings(foo=5)
> Settings(foo=5, bar='eeee')
```

but 

```py
Settings(foo="five")
```
raise the following exception:

> ValidationError: 1 validation error for Settings
foo
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='five', input_type=str]

### Environment variables
For sure it is more useful to set the settings values directly changing the *environment variables*. This can be done using the `export` command on Linux or the `set` one on Windows. Let's try what happens changing the value of the *bar* field and to instance a `Setting` object without any input argument.

```sh
export bar="I'm an env variable!"
```
```
Settings()
> Settings(foo=1, bar="I'm an env variable!")
```

If we then pass an input argument it will have the precedence!
```
Settings(bar="?")
> Settings(foo=1, bar='?')
```

### Using a .env file
Sometimes could be useful to collect more environment variables in a `.env` file. There is no need to load this file at the beginning of the module, pydantic will do this for us. To do so, the path to the file must be specified. For this and other configuration, our `Settings` class must be a little bit changed, including the `SettingsConfigDict`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import expanduser

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=expanduser("~/.env"), 
        env_file_encoding="utf-8",
        env_prefix="example_"
      )

    foo: int = 1
    bar: str = "eeee"
```

Let's take a look at the new addings:

- `env_file`: the path to the `.env` file
- `env_file_econding`: for specifying an encoding different from the one used by your OS
- `env_prefix`: to specify a prefix that **ALL** the variables must have to be considered field of the `Settings` class.

Let's fill our file with the variables:

```env title=".env"
example_foo=42
bar="Will I be ignored?"
```

Let's now create another Settings object:

```
Settings()
> Settings(foo=42 bar='eeee')
```
As you can see, the `bar` variable has not been taken, since no `env_prefix` has been used. Furthermore, the previous values set using the `export bar=...` command is not showing up, because of the prefix! Let's now fix it to simply understand the **priority**.

Let's rerun the export command and update the env file, adding this time the prefix **example_**":

```sh
export example_bar="I'm an env variable!"
```

```env title=".env"
example_foo=42
example_bar="Will I be ignored?"
```

The output is `Settings(foo=42 bar="I'm an env variable!")`!!

The *bar* variable from the .env file has been totally overridden!

#### Evaluation order
To sum up, the priority order for which value will be taken is:

1. Values passed as input arguments
1. Values loaded from the environment variables
1. Values loaded from the `.env` file
1. Field default values

### More validations
As we have seen, the type hinting lets Pydantic to validate the values based on the provided type. Pydantic has great variety of [built in types](https://docs.pydantic.dev/latest/api/types/#pydantic.types), like `PositiveInt`, `PositiveFloat`, `FilePath` and also types to define sensitive data that should be kept secret (just classess that override the `__repr__` and `__str__` methods), like the `SecretStr` or the `PaymentCardNumber`.

Let's doing an example using some of them and a custom type:

```python
from pydantic.types import SecretStr, PositiveInt
from enum import StrEnum

class Role(StrEnum):
    READER = "reader"
    MODERATOR = "moderator"
    ADMIN = "admin"

class Settings(BaseSettings):
    username: str
    password: SecretStr
    age: PositiveInt
    role: Role = Role.READER
```

Let's create a new Setting object:

!!! warning 
  
    Never hardcode your passwords!

```python
Settings(
    username="Deg", 
    password="not_supposed_to_be_hardcoded_here", 
    age=29, 
    role="moderator"
  )
``` 
results in
```
Settings(username='Deg' password=SecretStr('**********') age=29 role=<Role.MODERATOR: 'moderator'>)
```

Changing the role to `"story-teller"` results in a `ValidationError`:


> 1 validation error for Settings
role
  Input should be 'reader', 'moderator' or 'admin' [type=enum, input_value='story_teller', input_type=str]

### Custom validation
It is also possible to define custom validators to be performed before or after the Field validations seen before.

#### Field validators

The `field_validator` decorator allows to add another validator to a field. It is used to decorate only `classmethods` and accepts as input the field name and another optional argument.

For example, we want to validate the `password` field used before in order to accept only passwords that are at least 8 characters long. We would write something like:

```python
from pydantic import field_validator

class Settings(BaseSettings):
    ...

  @field_validator("password")
  @classmethod
  def validate_field_length(cls, v: str):
      if len(v) < 8:
          raise ValueError("The field 'password' must be at least of 8 characters long")
      return v
```

It is also possible to use the same validator for more than one field, listing all the fields. In this case, the message shown in the exception raised wouldn't be correct! Fortunately, a third argument gives us a hand:

```python
@field_validator("password","username")
@classmethod
def validate_field_length(cls, v: str, info: ValidationInfo):
    if len(v) < 8:
        raise ValueError(f"The field {info.field_name} must have a length at least of 8 characters")
    return v
```


## Sources
- <https://docs.pydantic.dev/latest/>
- <https://docs.pydantic.dev/latest/concepts/pydantic_settings/#settings-management>
- <https://docs.pydantic.dev/latest/concepts/validators/>