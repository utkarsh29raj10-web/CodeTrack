import os
import json
import logging
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidKey
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SecurityManager:
    def __init__(self):
        raw_key = os.getenv("MASTER_KEY")

        if not raw_key:
            logging.error("key env var is missing. Fix it")
            raise ValueError("Missing key")

        try:
            self.cipher_suite = Fernet(raw_key.encode('utf-8'))
        except (ValueError, InvalidKey) as e:
            logging.error(f"Failed to initialize Security Manger: Invalid key. {e}")
            raise

    def encrypt_payload(self, raw_api_key: str, dashboard_url: str) -> str:
        if not raw_api_key or not dashboard_url:
            raise ValueError("API key or Dashboard URL must have a value")

        payload_dict = {
            "key": raw_api_key.strip(),
            "url": dashboard_url.strip()
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

if __name__ == "__main__":
    print("Testing SecurityManager encryption with .env key")

    try:
        manager = SecurityManager()
        secure_code = manager.encrypt_payload("abc-123-blah-blah", "https://dashboard.blah.com")
        print (f"Successfully generated configuration code:\t{secure_code}")

    except Exception as e:
        print(f"Something went wrong: {e}")
