import unittest
import os
import configparser
from core.config import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.manager = ConfigManager()
        self.manager.config_path = os.path.join(self.manager.home_dir, ".wakatime_test.cfg")

    def tearDown(self):
        if os.path.exists(self.manager.config_path):
            os.remove(self.manager.config_path)

    def test_write_config_with_all_inputs(self):
        api_key = "test-blah-meow"
        api_url = "sample.com"
        emp_name = "mewo"

        result = self.manager.write_config(api_key, api_url, emp_name)
        self.assertTrue(result)

        config = configparser.ConfigParser()
        config.read(self.manager.config_path)

        self.assertEqual(config.get('settings', 'api_key'), api_key)
        self.assertEqual(config.get('settings', 'api_url'), api_url)
        self.assertEqual(config.get('settings', 'hostname'), emp_name)
        self.assertEqual(config.get('settings', 'heartbeat_rate_limit_seconds'), '30')

    def test_write_config_fallback_defaults(self):
        api_key = "test-blah-key"

        result = self.manager.write_config(api_key, "", "")
        self.assertTrue(result)

        config = configparser.ConfigParser()
        config.read(self.manager.config_path)
        self.assertEqual(config.get('settings', 'api_key'), api_key)
        self.assertEqual(config.get('settings', 'api_url'), self.manager.DEFAULT_API_URL)

        fallback_hostname = config.get('settings', 'hostname')
        self.assertEqual(len(fallback_hostname), 6)
        self.assertTrue(fallback_hostname.isalpha())

    def test_write_config_empty_key_fails(self):
        with self.assertRaises(ValueError):
            self.manager.write_config("","url", "name")

if __name__ == "__main__":
    unittest.main()
