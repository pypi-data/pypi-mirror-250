import pytest
import functools
import logging
import allure
import threading
from typing import Any, Callable, Tuple, Optional


def run_with_timeout(func: Callable, args: Tuple[Any, ...], kwargs: dict, timeout: int) -> Any:
    result: Optional[Any] = None
    exception: Optional[Exception] = None

    def wrapper():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return "timeout"
    if exception is not None:
        raise exception
    return result


def Mark(mark_name):
    def decorator(func):
        if not hasattr(func, "pytestmark"):
            func.pytestmark = []
        func.pytestmark.append(pytest.mark.custom(mark_name))
        return func

    return decorator


@pytest.fixture(scope="function")
def repeat_fixture(request):
    yield


def Test(run_test=True, repetitions=1, group_name="default", log=False, description=None):
    def decorator(func):
        if not run_test:
            func = pytest.mark.skip(reason="Тест пропущен на основе параметра run_test")(func)

        func = pytest.mark.repeat(repetitions)(func)
        func = pytest.mark.group(group_name)(func)

        if description:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                allure.dynamic.description(description)
                return func(*args, **kwargs)
            func = wrapper

        if log:
            func = Log(func)

        return func
    return decorator


def Log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.INFO)

        # Логгер для вывода в консоль
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        with allure.step(f"Начало теста {func.__name__}"):
            logger.info(f"Начало теста {func.__name__}")
            try:
                result = func(*args, **kwargs)
                with allure.step(f"Успешное завершение теста {func.__name__}"):
                    logger.info(f"Успешное завершение теста {func.__name__}")
                return result
            except Exception as e:
                error_message = f"Ошибка в тесте {func.__name__}: {e}"
                with allure.step(error_message):
                    logger.error(error_message)
                    allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
                raise
            finally:
                logger.removeHandler(console_handler)

    return wrapper
