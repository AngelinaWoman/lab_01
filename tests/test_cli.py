import subprocess
import sys


def run_toolkit(*arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "toolkit", *arguments], capture_output=True, text=True, timeout=10, check=False)


class TestCli:
    def test_calc(self):
        result = run_toolkit("calc", "2 + 3 * 4")
        assert result.returncode == 0
        assert result.stdout.strip() == "14.0"
        assert result.stderr == ""

    def test_help(self):
        result = run_toolkit("--help")
        assert result.returncode == 0
        assert "calc" in result.stdout
        assert "convert" in result.stdout

    def test_convert(self):
        result = run_toolkit("convert", "100", "--from", "c", "--to", "f")
        assert result.returncode == 0
        assert result.stdout.strip() == "212.0"

    def test_convert_with_error(self):
        result = run_toolkit("convert", "1", "--from", "m", "--to", "kg")
        assert result.returncode == 2
        assert "Несовместимые единицы" in result.stderr