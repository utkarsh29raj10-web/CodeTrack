import os
import platform
import urllib.request
import zipfile
import stat
import logging
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
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

        logging.info(f"Downloading")

        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(url, context=context) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                extracted_name = zip_ref.namelist()[0]
                zip_ref.extractall(self.wakatime_dir)

            os.remove(zip_path)

            extracted_path = os.path.join(self.wakatime_dir, extracted_name)
            binary_name = "wakatime-cli.exe" if platform.system().lower() == "windows" else "wakatime-cli"
            binary_path = os.path.join(self.wakatime_dir, binary_name)

            if os.path.exists(binary_path):
                os.remove(binary_path)

            os.rename(extracted_path, binary_path)

            if platform.system().lower() != "windows":
                st = os.stat(binary_path)
                os.chmod(binary_path, st.st_mode | stat.S_IEXEC)

            logging.info(f"CLI successfully installed at {binary_path}")
            return binary_path

        except Exception as e:
            logging.error(f"Download failed: {e}")
            raise

    def get_vscode_extension_dir(self) -> str:
        return os.path.join(self.home_dir, ".vscode", "extensions")

    def inject_vscode_plugin(self) -> bool:
        import gzip

        ext_dir = self.get_vscode_extension_dir()
        if not os.path.exists(ext_dir):
            os.makedirs(ext_dir)

        url = "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/WakaTime/vsextensions/vscode-wakatime/latest/vspackage"
        vsix_path = os.path.join(self.wakatime_dir, "vscode-wakatime.vsix")

        logging.info("Downloading")

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open (vsix_path, 'wb') as out_file:
                out_file.write(response.read())

            try:
                with gzip.open(vsix_path, 'rb') as f_in:
                    uncompressed_data = f_in.read()
                with open(vsix_path, 'wb') as f_out:
                    f_out.write(uncompressed_data)

            except gzip.BadGzipFile:
                pass

            target_folder = os.path.join(ext_dir, "wakatime.vscode-wakatime-master")
            with zipfile.ZipFile(vsix_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)

            os.remove(vsix_path)
            logging.info("VS Code plugin injected successfully")

            return True

        except Exception as e:
            logging.error(f"Failed to inject VS Code plugin: {e}")
            return False

# Testing manually
if __name__ == "__main__":
    print("Testing Downloader & Installer")

    try:
        installer = Installer()
        binary_path = installer.download_cli()
        print(f"Successfully installed the core engine")
    except Exception as e:
        print(f"Something went wrong: {e}")

    print("Testing VS Code Plugin Installation")

    try:
        installer.inject_vscode_plugin()
    except Exception as e:
        print(f"injection failed")