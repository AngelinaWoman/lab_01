import pytest
from toolkit.converter import convert
from toolkit.errors import ConverterError

class TestConverter:
    def test_from_m_to_km(self):
        assert convert(100, 'm', 'km') == 0.1

    def test_from_cm_to_m(self):
        assert convert(100, 'cm', 'm') == 1.0

    def test_from_kg_to_g(self):
        assert convert(1.5, 'kg', 'g') == 1500.0

    def test_same_units(self):
        assert convert(5, 'm', 'm') == 5.0

    def test_celsius_to_fahrenheit(self):
        assert convert(0, 'c', 'f') == 32.0

    def test_fahrenheit_to_celsius(self):
        assert convert(212, 'f', 'c') == 100.0

    def test_incompatible_units(self):
        with pytest.raises(ConverterError):
            convert(100, 'm', 'kg')

    def test_unknown_unit(self):
        with pytest.raises(ConverterError):
            convert(100, 'm', 'zdraste_priehali')

    def test_below_absolute_zero(self):
        with pytest.raises(ConverterError):
            convert(-300, 'c', 'k')

    def test_invalid_value_type(self):
        with pytest.raises(ConverterError):
            convert("сто", 'm', 'km')