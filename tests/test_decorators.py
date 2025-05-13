import pytest

from src.decorators import func_with_error, my_function


def test_my_function_result() -> None:
    assert my_function(1, 2) == 3


def test_starting_my_function(capsys: pytest.CaptureFixture) -> None:
    my_function(1, 2)
    captured = capsys.readouterr()
    assert "Starting function: my_function\n" in captured.out


def test_my_function_ok(capsys: pytest.CaptureFixture) -> None:
    my_function(1, 2)
    captured = capsys.readouterr()
    assert "my_function ok: 3\n" in captured.out


def test_exception() -> None:
    with pytest.raises(TypeError, match="Something went wrong!"):
        func_with_error(1, 2)
