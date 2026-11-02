import unittest

from src.config import build_config, parse_yaml, load_config
from src.errors import ConfigError

VALID = """
# comment
package: requests
repository: "https://pypi.org/pypi"
test_mode: false
max_depth: 2
exclude: test
"""


def config_from(text):
    return build_config(parse_yaml(text))


class ConfigTest(unittest.TestCase):
    def test_valid(self):
        config = config_from(VALID)
        self.assertEqual(config.package, "requests")
        self.assertEqual(config.repository, "https://pypi.org/pypi")
        self.assertFalse(config.test_mode)
        self.assertEqual(config.max_depth, 2)
        self.assertEqual(config.exclude, "test")

    def test_missing_file(self):
        with self.assertRaises(ConfigError):
            load_config("no_such_file.yaml")

    def test_bad_line(self):
        with self.assertRaises(ConfigError):
            parse_yaml("package requests")

    def test_duplicate_key(self):
        with self.assertRaises(ConfigError):
            parse_yaml("package: a\npackage: b")

    def test_unknown_key(self):
        with self.assertRaises(ConfigError):
            config_from(VALID + "color: red\n")

    def test_missing_package(self):
        with self.assertRaises(ConfigError):
            config_from("repository: x\nmax_depth: 1")

    def test_package_with_space(self):
        with self.assertRaises(ConfigError):
            config_from("package: a b\nrepository: x\nmax_depth: 1")

    def test_missing_repository(self):
        with self.assertRaises(ConfigError):
            config_from("package: a\nmax_depth: 1")

    def test_bad_mode(self):
        with self.assertRaises(ConfigError):
            config_from(VALID.replace("false", "maybe"))

    def test_bad_depth(self):
        with self.assertRaises(ConfigError):
            config_from(VALID.replace("2", "two"))

    def test_zero_depth(self):
        with self.assertRaises(ConfigError):
            config_from(VALID.replace("2", "0"))

    def test_default_exclude(self):
        config = config_from("package: a\nrepository: x\nmax_depth: 1")
        self.assertEqual(config.exclude, "")


if __name__ == "__main__":
    unittest.main()
