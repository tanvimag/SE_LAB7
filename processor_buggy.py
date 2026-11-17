"""processor.py (BUGGY version) - Lab 7: Fuzzing for Input Validation Bugs"""


def parse_int_list(s):
    """Parse a comma-separated string such as '1,2,3' into [1, 2, 3]."""
    return [int(x) for x in s.split(',')]


def sanitize_string(s):
    """Strip leading/trailing punctuation and lower-case the string."""
    return s.strip("!?.,;: ").lower()


def is_palindrome(s):
    """Return True if s reads the same forwards and backwards."""
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    print("parse_int_list('1,2,3')   ->", parse_int_list("1,2,3"))
    print("sanitize_string('!Hello!')->", sanitize_string("!Hello!"))
    print("is_palindrome('Race car') ->", is_palindrome("Race car"))
    print("parse_int_list('1,,3')    ->", end=" ")
    try:
        print(parse_int_list("1,,3"))
    except Exception as e:
        print(f"CRASH: {type(e).__name__}: {e}")
    print("sanitize_string(None)     ->", end=" ")
    try:
        print(sanitize_string(None))
    except Exception as e:
        print(f"CRASH: {type(e).__name__}: {e}")
    print("is_palindrome(None)       ->", end=" ")
    try:
        print(is_palindrome(None))
    except Exception as e:
        print(f"CRASH: {type(e).__name__}: {e}")
