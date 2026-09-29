import pytest

from toolkit.calculator import calculate
from toolkit.errors import CalculatorError


class TestCalculator:
    def test_simple_addition(self):
        assert calculate("2 + 2") == 4.0

    def test_simple_subtraction(self):
        assert calculate("6 - 4") == 2.0

    def test_division(self):
        assert calculate("10 / 2") == 5.0

    def test_unary_minus(self):
        assert calculate("-5 * 3") == -15.0

    def test_float_numbers(self):
        assert calculate("1.5 + 2.5") == 4.0

    def test_multiple_dots_error(self):
        with pytest.raises(CalculatorError):
            calculate("1..2")

    def test_three_dots_error(self):
        with pytest.raises(CalculatorError):
            calculate("5...3")

    def test_invalid_format_error(self):
        with pytest.raises(CalculatorError):
            calculate("1.2.3")

    def test_single_dot_error(self):
        with pytest.raises(CalculatorError):
            calculate(".")

    def test_division_by_zero(self):
        with pytest.raises(CalculatorError):
            calculate("10 / 0")

    def test_empty_expression(self):
        with pytest.raises(CalculatorError):
            calculate("")
