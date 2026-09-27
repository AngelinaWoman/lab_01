from toolkit.errors import ConverterError

LENGTH_TO_BASE = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

MASS_TO_BASE = {
    "g": 1.0,
    "kg": 1000.0,
}

TEMPERATURE_UNITS = {"c", "f", "k"}

ALL_UNITS = set(LENGTH_TO_BASE) | set(MASS_TO_BASE) | TEMPERATURE_UNITS

def temperature_to_base(value: float, unit: str) -> float:
    if unit == "c":
        return value
    elif unit == "f":
        return (value - 32) / 1.8
    elif unit == "k":
        return value - 273.15

def temperature_to_final(value: float, unit: str) -> float:
    if unit == "c":
        return value
    elif unit == "f":
        return value * 1.8 + 32
    elif unit == "k":
        return value + 273.15

def convert(value: float, from_unit: str, to_unit: str) -> float:
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ConverterError("Неверное числовое значение")

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit not in ALL_UNITS or to_unit not in ALL_UNITS:
       raise ConverterError("Неизвестная единица")

    if from_unit in LENGTH_TO_BASE and to_unit in LENGTH_TO_BASE:
        value_in_base = value * LENGTH_TO_BASE[from_unit]
        final_value = value_in_base / LENGTH_TO_BASE[to_unit]
        return final_value

    elif from_unit in MASS_TO_BASE and to_unit in MASS_TO_BASE:
        value_in_base = value * MASS_TO_BASE[from_unit]
        final_value = value_in_base / MASS_TO_BASE[to_unit]
        return final_value

    elif from_unit in TEMPERATURE_UNITS and to_unit in TEMPERATURE_UNITS:
        value_in_base = temperature_to_base(value, from_unit)

        if value_in_base < -273.15:
            raise ConverterError("Температура ниже абсолютного нуля")

        return temperature_to_final(value_in_base, to_unit)

    raise ConverterError("Несовместимые единицы")