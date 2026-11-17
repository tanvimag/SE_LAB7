"""test_processor.py - Hypothesis fuzz tests for processor.py (Lab 7)"""
from hypothesis import given, settings, strategies as st
from processor import parse_int_list, sanitize_string, is_palindrome

# Anything a fuzzer might throw at a "string" function
anything = st.one_of(
    st.none(), st.text(), st.integers(), st.floats(allow_nan=True),
    st.binary(), st.booleans(), st.lists(st.integers()),
)


# ---------- parse_int_list ----------
@settings(max_examples=300)
@given(anything)
def test_parse_int_list_no_crash(s):
    try:
        parse_int_list(s)
    except Exception as e:
        assert False, f"parse_int_list crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_int_list_returns_list_of_ints(s):
    result = parse_int_list(s)
    assert isinstance(result, list)
    assert all(isinstance(x, int) for x in result)


@given(st.lists(st.integers(min_value=-10**9, max_value=10**9), min_size=1))
def test_parse_int_list_roundtrip(nums):
    assert parse_int_list(",".join(map(str, nums))) == nums


# ---------- sanitize_string ----------
@settings(max_examples=300)
@given(anything)
def test_sanitize_string_no_crash(s):
    try:
        sanitize_string(s)
    except Exception as e:
        assert False, f"sanitize_string crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_sanitize_string_returns_str(s):
    assert isinstance(sanitize_string(s), str)


@given(st.text())
def test_sanitize_string_idempotent(s):
    once = sanitize_string(s)
    assert sanitize_string(once) == once


# ---------- is_palindrome ----------
@settings(max_examples=300)
@given(anything)
def test_is_palindrome_no_crash(s):
    try:
        is_palindrome(s)
    except Exception as e:
        assert False, f"is_palindrome crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_is_palindrome_returns_bool(s):
    assert isinstance(is_palindrome(s), bool)


@given(st.text())
def test_is_palindrome_of_text_plus_reverse(s):
    # Any string followed by its reverse is a palindrome
    assert is_palindrome(s + s[::-1])
