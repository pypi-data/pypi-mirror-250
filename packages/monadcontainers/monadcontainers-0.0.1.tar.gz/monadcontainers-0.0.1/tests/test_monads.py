import pytest

from monadcontainers import monads


def test_monad_class_function_chaining_produces_expected():
    actual = monads.Monad(2).bind(lambda x: x + 1).bind(lambda x: x * 2)
    assert actual.value == 6


def test_monad_class_provides_unwrap_option_to_access_value():
    actual = monads.Monad(2).unwrap()
    assert actual == 2


def test_monad_class_overrides_rshift():
    actual = monads.Monad("hello") >> (lambda x: x + " world!")
    assert actual.value == "hello world!"


def test_monad_class_provides_string_method_displaying_value():
    actual = str(monads.Monad(2))
    assert actual == "Monad(2)"


def test_monad_string_method_is_inhereted_correctly():
    class TestMonad(monads.Monad):
        def nothing(self):
            pass

    actual = str(TestMonad("seven"))
    assert actual == "TestMonad(seven)"


def test_maybe_monad_doesnt_run_functions_when_none():
    actual = monads.Maybe(None).bind(lambda x: x**2)
    assert actual.value is None


def test_maybe_monad_otherwise_runs_as_normal():
    actual = monads.Maybe(2).bind(lambda x: x + 1)
    assert actual.unwrap() == 3


def test_list_monad_applies_single_function_over_list():
    actual = monads.List([1, 2]).bind(lambda x: x + 1)
    assert set(actual.unwrap()) == {2, 3}


def test_result_monad_captures_error_without_raising():
    actual = monads.Result(1).bind(lambda x: x / 0)
    assert actual.value == None
    assert isinstance(actual.exception, ZeroDivisionError)


def test_result_monad_raises_error_on_unwraps():
    actual = monads.Result(1).bind(lambda x: x / 0)
    with pytest.raises(ZeroDivisionError):
        _ = actual.unwrap()


def test_result_monad_replaces_error_with_unwrap_or():
    actual = monads.Result(1).bind(lambda x: x / 0).unwrap_or(2)
    assert actual == 2


def test_result_monad_otherwise_works_as_normal():
    actual = monads.Result(2).bind(lambda x: x + 1).bind(lambda x: x * 2).unwrap()
    assert actual == 6
