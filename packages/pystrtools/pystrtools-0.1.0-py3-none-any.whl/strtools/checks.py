from typing import Iterable
from . import consts


def contains_only(string: str, charset: Iterable[str]) -> bool:
    for char in string:
        if char not in charset:
            return False
    return True


def is_base64(string: str) -> bool:
    return contains_only(string, consts.BASE64_DIGITS_WITH_EQUALS)


def is_base64_no_equals(string: str) -> bool:
    return contains_only(string, consts.BASE64_DIGITS)


def is_octal(string: str) -> bool:
    return contains_only(string, consts.OCTAL_DIGITS)


def is_numerical(string: str) -> bool:
    return contains_only(string, consts.ASCII_DIGITS)


def is_hex(string: str) -> bool:
    return contains_only(string, consts.HEX_DIGITS)


def is_hex_upper(string: str) -> bool:
    return contains_only(string, consts.HEX_DIGITS_UPPER)


def is_hex_lower(string: str) -> bool:
    return contains_only(string, consts.HEX_DIGITS_LOWER)


def is_whitespace(string: str) -> bool:
    return contains_only(string, consts.WHITESPACE)


def is_lowercase(string: str) -> bool:
    return string == string.lower()


def is_uppercase(string: str) -> bool:
    return string == string.upper()


def is_fully_lowercase(string: str) -> bool:
    return contains_only(string, consts.ASCII_LOWERCASE)


def is_fully_uppercase(string: str) -> bool:
    return contains_only(string, consts.ASCII_UPPERCASE)


def is_ascii_letters(string: str) -> bool:
    return contains_only(string, consts.ASCII_LETTERS)


def is_ascii_punctuation(string: str) -> bool:
    return contains_only(string, consts.ASCII_PUNCTUATION)


def is_ascii_printable(string: str) -> bool:
    return contains_only(string, consts.ASCII_PRINTABLE)


def is_ascii_control(string: str) -> bool:
    return contains_only(string, consts.ASCII_CONTROL)


def is_ascii(string: str) -> bool:
    return contains_only(string, consts.ASCII_ALL)


def is_ansi(string: str) -> bool:
    return contains_only(string, consts.ANSI_ALL)
