import pytest

from StenLib.StenDecorators import ErrorHandler


class CustomException(Exception):
    """A custom exception."""


def test_error_handler():
    """Test the ErrorHandler decorator."""

    @ErrorHandler(CustomException)
    def raise_exception():
        """Raise a custom exception."""
        raise CustomException('This is a custom exception')

    with pytest.raises(CustomException):
        raise_exception()

    @ErrorHandler(CustomException)
    def no_exception():
        """Return a string."""
        return 'No exception raised'

    assert no_exception() == 'No exception raised'
