from typing import Final


WHITESPACE: Final[str] = "\t\n\r\v\f "
ASCII_LOWERCASE: Final[str] = "abcdefghijklmnopqrstuvwxyz"
ASCII_UPPERCASE: Final[str] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ASCII_DIGITS: Final[str] = "0123456789"
ASCII_PUNCTUATION: Final[str] = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
ASCII_LETTERS: Final[str] = ASCII_LOWERCASE + ASCII_UPPERCASE
ASCII_PRINTABLE: Final[str] = "".join(chr(i) for i in range(32, 127))
ASCII_CONTROL: Final[str] = "".join([chr(i) for i in range(32)]) + chr(127)
ASCII_ALL: Final[str] = "".join([chr(i) for i in range(128)])

ANSI_ALL: Final[str] = "".join(
    [
        chr(i)
        for i in range(256)
        if i not in (129, 141, 143, 144, 157)  # why the fuck are some not used???
    ]
)

OCTAL_DIGITS: Final[str] = "01234567"
HEX_DIGITS_LOWER: Final[str] = ASCII_DIGITS + "abcdef"
HEX_DIGITS_UPPER: Final[str] = ASCII_DIGITS + "ABCDEF"
HEX_DIGITS: Final[str] = HEX_DIGITS_UPPER
BASE64_DIGITS: Final[str] = ASCII_UPPERCASE + ASCII_LOWERCASE + ASCII_DIGITS + "+/"
BASE64_DIGITS_WITH_EQUALS: Final[str] = BASE64_DIGITS + "="
