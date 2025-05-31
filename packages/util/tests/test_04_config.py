import unittest
import os
from unittest.mock import patch
from packages.util.utils.config import get_env_variable

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.original_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_env)

    @patch.dict(os.environ, {"API_CYPHEROCK": "https://test.cypherock.com"})
    def test_config_with_custom_env(self):
        from packages.util.utils.config import Config
        config = Config()
        self.assertIsNotNone(config)
        self.assertEqual(config.API_CYPHEROCK, "https://test.cypherock.com")

    def test_config_with_default_values(self):
        if "API_CYPHEROCK" in os.environ:
            del os.environ["API_CYPHEROCK"]

        from packages.util.utils.config import config

        self.assertIsNotNone(config)
        self.assertEqual(config.API_CYPHEROCK, "https://api.cypherock.com")

    def test_get_env_variable_error(self):
        with self.assertRaises(ValueError):
            get_env_variable("TEST")


if __name__ == "__main__":
    unittest.main()
