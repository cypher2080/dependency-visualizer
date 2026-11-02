import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from src.main import FAILURE_CODE, main


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class MainTest(unittest.TestCase):
    def test_params(self):
        code, out, _ = run("configs/simple.yaml", "params")
        self.assertEqual(code, 0)
        self.assertIn("package = A", out)

    def test_deps(self):
        _, out, _ = run("configs/simple.yaml", "deps")
        self.assertIn("  B", out)

    def test_order(self):
        _, out, _ = run("configs/cycle.yaml", "order")
        self.assertIn("Не загружены из-за цикла: A B C", out)

    def test_unknown_mode(self):
        code, _, err = run("configs/simple.yaml", "draw")
        self.assertEqual(code, FAILURE_CODE)
        self.assertIn("неизвестный режим", err)

    def test_config_error(self):
        code, _, _ = run("configs/errors/zero_depth.yaml")
        self.assertEqual(code, FAILURE_CODE)


if __name__ == "__main__":
    unittest.main()
