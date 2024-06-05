import requests
import tempfile
import os
import json
import sys
import shutil


SOLC_BIN = "https://binaries.soliditylang.org"
PLATFORM = "linux-amd64"
LIST = f"{SOLC_BIN}/{PLATFORM}/list.json"

def get_releases():
    obj = json.loads(requests.get(LIST).text)
    return obj["builds"]

def download_version(dst_path: str, release):
    relative_path = release["path"]
    url = f"{SOLC_BIN}/{PLATFORM}/{relative_path}"
    print(f"downloading solc: {url}")
    binary = requests.get(url).content
    with open(dst_path, "wb") as f:
        f.write(binary)
    os.chmod(dst_path, 0o755)

def fetch_artifacts(dst):
    releases = get_releases()
    with tempfile.TemporaryDirectory() as tempdir:
        print(tempdir)
        artifacts_dir = f"{tempdir}/artifacts"
        for release in releases:
            version = release["version"]
            version_dir = f"{artifacts_dir}/solc-{version}"
            os.makedirs(version_dir)
            binary_path = f"{version_dir}/solc-{version}"
            download_version(binary_path, release)
        shutil.make_archive(dst, 'zip', root_dir=tempdir, base_dir="artifacts")
        

if __name__ == '__main__':
    dst = sys.argv[1]
    fetch_artifacts(dst)