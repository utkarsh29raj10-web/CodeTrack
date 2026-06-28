import unittest
from core.security import SecurityManager

class TestSecurityManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = SecurityManager()

    def test_encryption_decryption_cycle(self):
        raw_key = "blah-1-2-api-meow"
        dashboard_url = "x.meow.com"
        employee_name = ""

        encrypted_str = self.manager.encrypt_payload(raw_key, dashboard_url, employee_name)
        self.assertTrue(isinstance(encrypted_str, str))
        self.assertNotEqual(encrypted_str, "")

        decrypted_dict = self.manager.decrypt_payload(encrypted_str)

        self.assertEqual(decrypted_dict.get("key"), raw_key)
        self.assertEqual(decrypted_dict.get("url"), dashboard_url)
        self.assertEqual(decrypted_dict.get("name"), employee_name)

    def test_invalid_decryption(self):
        with self.assertRaises(ValueError):
            self.manager.decrypt_payload("not encrypted bro")

if __name__ == '__main__':
    unittest.main()