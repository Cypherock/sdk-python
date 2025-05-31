import unittest
from unittest import TestCase
from packages.util.utils.assert_utils import assert_condition

class TestAssert(TestCase):
    def test_assert_fails(self):
        test_cases = [
            {
                "name": "undefined",
                "condition": None,
                "error": "Invalid argument",
                "error_message": "AssertionError: Invalid argument"
            },
            {
                "name": "null",
                "condition": None,
                "error": "Invalid argument",
                "error_message": "AssertionError: Invalid argument"
            },
            {
                "name": "false",
                "condition": False,
                "error": "Invalid argument",
                "error_message": "AssertionError: Invalid argument"
            },
            {
                "name": "false with custom error",
                "condition": False,
                "error": Exception("Custom error"),
                "error_message": "Custom error"
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case["name"]):
                with self.assertRaises(Exception) as context:
                    assert_condition(test_case["condition"], test_case["error"])

                self.assertEqual(str(context.exception), test_case["error_message"])

    def test_assert_passes(self):
        test_cases = [
            {
                "name": "string",
                "condition": "aksjdh"
            },
            {
                "name": "empty string",
                "condition": ""
            },
            {
                "name": "object",
                "condition": {}
            },
            {
                "name": "array",
                "condition": []
            },
            {
                "name": "number",
                "condition": 1
            },
            {
                "name": "number zero",
                "condition": 0
            },
            {
                "name": "negative number",
                "condition": -12
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case["name"]):
                try:
                    assert_condition(test_case["condition"], "Should not have failed")
                except Exception:
                    self.fail(f"assert_condition raised an exception unexpectedly for {test_case['name']}")


if __name__ == "__main__":
    unittest.main()
