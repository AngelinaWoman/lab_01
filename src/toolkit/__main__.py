import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m toolkit",
        description="CLI набор утилит: калькулятор и конвертер",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser(
        "calc", help="Вычислить математическое выражение"
    )
    calc_parser.add_argument(
        "expression", help="Выражение в кавычках, например '2 + 2'"
    )

    convert_parser = subparsers.add_parser(
        "convert", help="Конвертировать единицы измерения"
    )
    convert_parser.add_argument("value", type=float, help="Числовое значение")
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, help="Исходная единица"
    )
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, help="Конечная единица"
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        if args.command == "calc":
            result = calculate(args.expression)
        elif args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
    except ToolkitError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(2)

    print(result)


if __name__ == "__main__":
    main()
