"""
-Bryan Palomo

Python script that deploys compiled binary for arm64-linux from
build env to the device. Must have ssh key generated without
passphrase and on the device for scp to work.
"""

import subprocess
import sys
import argparse
import os
from dotenv import load_dotenv

# Load and pass args
parser = argparse.ArgumentParser(description="Deploy binary executable from dev environment to embedded device")
parser.add_argument('file_path', metavar='<file>', type=str, help='Enter the bin file\'s path')
args = parser.parse_args()
# load from .env file
load_dotenv()

# arguments

BINARY_FILE = args.file_path
PI_HOST = os.getenv('PI_HOST')


#Command to transfer binary to device through scp
deploy_bin_cmd = f"scp {BINARY_FILE} root@{PI_HOST}:/var/SecurityCamera"

if sys.platform == "win32":
    print(f"Running: {deploy_bin_cmd}")
elif sys.platform == "linux":
    print("Do linux...")
elif sys.platform == "apple":
    print("Do apple")

# Run command
res = subprocess.run(deploy_bin_cmd, capture_output=True, text=True)
print(res.stdout)

if res.returncode != 0:
    print(f"Error occurred deploying to device: {res.stderr}")
else:
    print("Successfully executed deployment")
