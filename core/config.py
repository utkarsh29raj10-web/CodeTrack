import os
import configparser
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ConfigManager:
    DEFAULT_API_URL=""

    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        self.config_path = os.path.join(self.home_dir, ".wakatime.cfg")

    def write_config(self, api_key: str, api_url: str = "", employee_name: str = "") -> bool:
        import random
        import string

        if not api_key:
            logging.error("Failed to write config: Please enter API key")
            raise ValueError("API key cannot be empty")

        final_url = api_url.strip() if api_url else self.DEFAULT_API_URL

        final_hostname = employee_name.strip()
        if not final_hostname:
            random_suffix=''.join(random.choices(string.ascii_letters, k=6))
            final_hostname = random_suffix

        config = configparser.ConfigParser()

        if os.path.exists(self.config_path):
            config.read(self.config_path)

        if not config.has_section('settings'):
            config.add_section('settings')

        config.set('settings', 'api_key', api_key)
        config.set('settings', 'api_url', final_url)
        config.set('settings', 'heartbeat_rate_limit_seconds', '30')
        config.set('settings', 'exclude_unknown_project', 'true')
        config.set('settings', 'hide_branch_names', 'true')
        config.set('settings', 'hostname', final_hostname)

        try:
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)
            logging.info(f"Successfully wrote WakaTime configuration to {self.config_path}")
            return True

        except IOError as e:
            logging.error(f"Failed to write to {self.config_path}: {e}")
            raise

# Manual Testing
if __name__ == "__main__":
    print("Testing ConfigManager")
    try:
        manager = ConfigManager()
        manager.write_config(api_key="test-api-blah-blah", api_url="")
        print ("Successfully checked your home directory for ~/.wakatime.cfg")
    except Exception as error:
        print(f"Testing failed: {error}")