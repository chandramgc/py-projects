import unittest
from src.utils.config_reader import ConfigReader


class TestConfigReader(unittest.TestCase):
    def setUp(self):
        # Assumes that src/config/application-dev.yml exists and has known values.
        self.config_reader = ConfigReader(env="dev")

    def test_get_existing_key(self):
        # Assuming application-dev.yml defines server.port as 5000
        port = self.config_reader.get("server.port")
        self.assertEqual(port, 5000)

    def test_get_nonexistent_key(self):
        # Expecting that a nonexistent key returns an empty dict
        value = self.config_reader.get("server.nonexistent")
        self.assertEqual(value, {})


if __name__ == "__main__":
    unittest.main()
