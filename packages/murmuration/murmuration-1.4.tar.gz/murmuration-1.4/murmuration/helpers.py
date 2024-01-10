from base64 import b64encode
from base64 import b64decode
from typing import Union
import re


__all__ = [
    'as_bytes',
    'b64_str',
    'from_b64_str',
    'prefix_alias',
]

uuid_regex = re.compile(
    '[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
    '-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}')


def as_bytes(value):
    if isinstance(value, str):
        value = value.encode('utf-8')
    return value


def b64_str(value: Union[str, bytes]) -> str:
    value = as_bytes(value)
    return b64encode(value).decode('utf-8')


def from_b64_str(value: str):
    value = value.encode('utf-8')
    return b64decode(value)


def prefix_alias(alias: str):
    if alias.startswith('arn:'):
        return alias
    if uuid_regex.match(alias):
        return alias
    if not alias.startswith('alias/'):
        alias = f'alias/{alias}'
    return alias
