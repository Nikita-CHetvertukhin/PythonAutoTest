import pytest
from utils.exception_handler.decorator_error_handler import exception_handler

@exception_handler
def test_test1(error_handler, logger, admin_driver):
    assert True