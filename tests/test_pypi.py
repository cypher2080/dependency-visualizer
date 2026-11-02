import unittest

from src.pypi import normalize, parse_requirement, requirements_to_names


class RequirementTest(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("Typing_Extensions"), "typing-extensions")

    def test_plain(self):
        self.assertEqual(parse_requirement("idna<4,>=2.5"), "idna")

    def test_with_marker(self):
        text = 'colorama; platform_system == "Windows"'
        self.assertEqual(parse_requirement(text), "colorama")

    def test_extra_is_skipped(self):
        text = 'PySocks!=1.5.7,>=1.5.6; extra == "socks"'
        self.assertIsNone(parse_requirement(text))

    def test_with_brackets(self):
        self.assertEqual(parse_requirement("urllib3[socks]>=1"), "urllib3")

    def test_unique_names(self):
        names = requirements_to_names(["a>1", "a<3", "b"])
        self.assertEqual(names, ["a", "b"])

    def test_none(self):
        self.assertEqual(requirements_to_names(None), [])


if __name__ == "__main__":
    unittest.main()
