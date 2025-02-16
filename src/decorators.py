from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[[Any, Any], Any]], Callable[[Any, Any], Any]]:
    """Декоратор логирует начало и конец выполнения функции, а также ее результаты или возникшие ошибки"""
    def decorator(func: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                print(f"Starting function: {func.__name__}")
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok: {result}"
                print(log_message)

                if filename:
                    with open(filename, "a") as file:
                        file.write(log_message + "\n")
                return result

            except Exception as error:
                error_message = f"{func.__name__} error: {type(error).__name__}. Inputs: {args}, {kwargs}"
                print(error_message)

                if filename:
                    with open(filename, "a") as file:
                        file.write(error_message + "\n")
                raise error

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    """Складывает два числа"""
    return x + y


@log(filename="mylog.txt")
def func_with_error(x: Any, y: Any) -> None:
    """Вызывает исключение"""
    raise TypeError("Something went wrong!")


if __name__ == "__main__":
    print(my_function)
    print(func_with_error)
