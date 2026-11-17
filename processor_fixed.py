"""processor.py (FIXED version) - Lab 7: Fuzzing for Input Validation Bugs

Every function is hardened so that it never raises on unexpected input:
  * non-string input (None, ints, lists, bytes...) is handled explicitly
  * malformed elements are skipped instead of crashing
  * Unicode edge cases (e.g. non-ASCII digits, huge numbers) are handled
"""
import string

# Largest integer we accept (guards against DoS via giant numbers; Python 3.11+
# also limits int<->str conversion to 4300 digits and raises ValueError).
MAX_DIGITS = 18


def parse_int_list(s):
    """Parse a comma-separated string such as '1,2,3' into [1, 2, 3].

    Returns [] for None / non-string / empty input. Invalid or empty
    elements (e.g. '1,,3', 'one,two') are skipped.
    """
    if not isinstance(s, str) or not s.strip():
        return []
    result = []
    for part in s.split(','):
        part = part.strip()
        # ASCII-only: int() also accepts things like Arabic-Indic digits
        # and underscores ('1_0'), which we treat as invalid.
        body = part[1:] if part[:1] in "+-" else part
        if not body or not (body.isascii() and body.isdigit()):
            continue
        if len(body) > MAX_DIGITS:
            continue
        result.append(int(part))
    return result


def sanitize_string(s):
    """Strip leading/trailing punctuation/whitespace and lower-case the string.

    Returns '' for None / non-string input.
    """
    if not isinstance(s, str):
        return ""
    return s.strip(string.punctuation + string.whitespace).lower()


def is_palindrome(s):
    """Return True if s reads the same forwards and backwards.

    Case and whitespace are ignored. None / non-string input returns False.
    The empty string is treated as a palindrome.
    """
    if not isinstance(s, str):
        return False
    chars = [c for c in s if not c.isspace()]
    # Compare char-by-char: casefold()/lower() on the whole string can expand
    # one character into several (e.g. 'ᾀ'), which breaks string reversal.
    return all(a.casefold() == b.casefold()
               for a, b in zip(chars, reversed(chars)))


if __name__ == "__main__":
    print("parse_int_list('1,2,3')   ->", parse_int_list("1,2,3"))
    print("sanitize_string('!Hello!')->", sanitize_string("!Hello!"))
    print("is_palindrome('Race car') ->", is_palindrome("Race car"))
    print("parse_int_list('1,,3')    ->", parse_int_list("1,,3"))
    print("sanitize_string(None)     ->", repr(sanitize_string(None)))
    print("is_palindrome(None)       ->", is_palindrome(None))
