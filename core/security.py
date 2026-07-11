import os
import json
import logging
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidKey
from core import secrets
from cryptography.fernet import InvalidToken
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SecurityManager:
    def __init__(self):
        raw_key = getattr(secrets, "MASTER_KEY", None)

        if not raw_key:
            logging.error("key env var is missing. Fix it")
            raise ValueError("Missing key")

        try:
            self.cipher_suite = Fernet(raw_key.encode('utf-8'))
        except (ValueError, InvalidKey) as e:
            logging.error(f"Failed to initialize Security Manger: Invalid key. {e}")
            raise

    def encrypt_payload(self, raw_api_key: str, dashboard_url: str = "", employee_name: str = "") -> str:
        if not raw_api_key:
            raise ValueError("API key must have a value")

        payload_dict = {
            "key": raw_api_key.strip(),
            "url": dashboard_url.strip() if dashboard_url else "",
            "name": employee_name.strip() if employee_name else "",
        }

        try:
            payload_json = json.dumps(payload_dict)
            encrypted_bytes = self.cipher_suite.encrypt(payload_json.encode('utf-8'))
            return encrypted_bytes.decode('utf-8')

        except TypeError as e:
            logging.error(f"Failed to serialize payload to JSON: {e}")
            raise

        except Exception as e:
            logging.error(f"Something went wrong during encryption: {e}")
            raise

    def decrypt_payload(self, encrypted_string: str) -> dict:
        if not encrypted_string:
            raise ValueError("Encrypted string must have a value")

        try:
            decrypted_bytes = self.cipher_suite.decrypt(encrypted_string.encode('utf-8'))
            payload_json = decrypted_bytes.decode('utf-8')
            return json.loads(payload_json)

        except InvalidToken:
            logging.error("Failed to decrypt: Invalid or corrupted key")
            raise ValueError("Invalid token. Please recehck the code or contact employer ")

        except Exception as e:
            logging.error(f"Something went wrong: {e}")
            raise

# Testing (Manual)
if __name__ == "__main__":
    print("Testing SecurityManager encryption with .env key")

    try:
        manager = SecurityManager()
        secure_code = manager.encrypt_payload("abc-123-blah-blah")
        print (f"Successfully generated configuration code:\t{secure_code}")

    except Exception as e:
        print(f"Something went wrong: {e}")
