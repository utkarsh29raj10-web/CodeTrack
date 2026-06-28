import os
import platform
import urllib.request
import zipfile
import stat
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class Installer:
    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        self.wakatime_dir = os.path.join(self.home_dir,".wakatime")

        if not os.path.exists(self.wakatime_dir):
            os.makedirs(self.wakatime_dir)

    def get_cli_download_url(self) -> str:
        system = platform.system().lower()
        machine = platform.machine().lower()

        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["arm64", "aarch64"]:
            arch = "arm64"
        else:
            arch = "386"

        filename = f"wakatime-cli-{system}-{arch}.zip"
        return f"https://github.com/wakatime/wakatime-cli/releases/latest/download/{filename}"

    def download_cli(self) -> str:
        url = self.get_cli_download_url()
        zip_path = os.path.join(self.wakatime_dir, "wakatime-cli.zip")

        logging.info(f"Downloading WakaTime CLI...")

        try:
            urllib.request.urlretrieve(url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.wakatime_dir)

            os.remove(zip_path)

            binary_name = "wakatime-cli.exe" if platform.system().lower() == "windows" else "wakatime-cli"
            binary_path = os.path.join(self.wakatime_dir, binary_name)

            if platform.system().lower() != "windows":
                st = os.stat(binary_path)
                os.chmod(binary_path, st.st_mode | stat.S_IEXEC)

            logging.info(f"Installation was successful.")
            return binary_path

        except Exception as e:
            logging.error(f"Download failed: {e}")
            raise

# Testing manually
if __name__ == "__main__":
    print("Testing Downloader & Installer")

    try:
        installer = Installer()
        binary_path = installer.download_cli()
        print(f"Successfully installed the core engine")
    except Exception as e:
        print(f"Something went wrong: {e}")