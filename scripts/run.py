import shutil
import subprocess
import os
import json
import sys
import argparse
from dotenv import load_dotenv
import stat

"""
Must have passwordless ssh setup with orange pi before attempting to run script.
Must supply orange pi address by cmd line arg or .env file in src directory
Script uses cmake to build project and can deploy built arm64 linux binary to device via scp.
"""

# For force remove locked files in build dir
def force_remove_readonly(func, path, exc_info):
    # Make file writeable and try again
    os.chmod(path, stat.S_IWRITE)
    func(path)

def configure(build_dir, src_dir, presets_file, preset=None):
    print(f"\033[35m-- Running cmake configure with source dir: \"{src_dir}\" and build dir: \"{build_dir}\"\033[0m")
    with open(presets_file, 'r') as f:
        presets = [x["name"] for x in json.load(f)["configurePresets"]]

    if preset:
        presets = [preset]
    print(f"\033[35m-- Using preset(s): {presets}\033[0m")
    # Try out all the presets
    for preset_name in presets:
        print(f"\033[35m-- Attempting cmake configuration with preset: \"{preset_name}\"...\033[0m")
        # Remove old build folder and contents if exists
        if os.path.exists(build_dir):
            print("\033[35m-- Removing existing build prior to building...\033[0m")
            shutil.rmtree(build_dir, onerror=force_remove_readonly)

        # Try configuration and show output
        config_res = subprocess.run(['cmake', '--preset', preset_name],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(config_res.stdout.decode())

        # If cmake config succeeds try cmake build
        if config_res.returncode == 0:
            print(f"\033[92m-- Succeeded in cmake configure with preset {preset_name}\n\033[0m")
            return
        else:
            print(f"\033[33m-- Preset {preset_name} failed\n\033[0m")
            print(config_res.stderr.decode())

    sys.exit(1)

def build_binary(build_dir):

    print(f"\033[35m-- Running cmake build with build dir: \"{build_dir}\"\033[0m")

    build_res = subprocess.run(['cmake', '--build', build_dir],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(build_res.stdout)

    # If build failed exit script
    if build_res.returncode == 0:
        print(f"\033[92m-- Build succeeded\033[0m")
    else:
        print(f"\033[33m-- Build failed\033[0m")
        print(build_res.stderr)
        sys.exit(1)

def deploy_binary(local_bin, local_tests, remote_bin, remote_tests):
    print(f"\033[35m-- Deploying binary to remote device: {remote_bin}\033[0m")
    # Command to transfer binaries to device through scp
    deploy_bin_cmd = ["scp", local_bin, remote_bin]
    deploy_tests_cmd = ["scp", local_tests, remote_tests]

    if sys.platform == "win32":
        print(f"\033[35m-- Running command: {deploy_bin_cmd}\033[0m")
        print(f"\033[35m-- Running command: {deploy_tests_cmd}\033[0m")
    elif sys.platform == "linux":
        print("\033[35mDo linux...\033[0m")
    elif sys.platform == "apple":
        print("\033[35mDo apple\033[0m")

    # Copy binary to remote
    bin_res = subprocess.run(deploy_bin_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(bin_res.stdout)
    if bin_res.returncode != 0:
        print(f"\033[31m-- Error occurred deploying to device: {bin_res.stderr}\n\033[0m")
        sys.exit(1)
    # Copy tests binary to remote
    tests_res = subprocess.run(deploy_tests_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(tests_res.stdout)
    if tests_res.returncode != 0:
        print(f"\033[31m-- Error occurred deploying to device: {tests_res.stderr}\n\033[0m")
        sys.exit(1)

    print("\033[92m-- Successfully executed binaries deployment\n\033[0m")

def perform_tests(device, tests, results):
    print(f"\033[35m-- Running unit tests on remote device: {device}\033[0m")
    # Run tests command and don't close ssh connection on test fail
    test_cmd = ["ssh", "-t", device, f"chmod +x {tests} && {tests} --gtest_output=xml:{results} || true"]
    print(f"Running: {test_cmd}")
    # Run build command on remote device
    res = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(f"\033[31m-- Error occurred running unit tests on device: {res.stderr}\n\033[0m")
        sys.exit(1)
    print(f"\033[92m-- Success running tests on remote device\n\033[0m")

def get_tests_report(remote_file, local_file):
    print(f"\033[35m-- Retrieving remote tests logs at: {remote_file}\033[0m")
    get_res_cmd = ["scp", remote_file, local_file]
    res = subprocess.run(get_res_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(f"\033[31m-- Error occurred retrieving tests results: {res.stderr}\033[0m")
        sys.exit(1)
    print(f"\033[92m-- Test report written to {local_file}\033[0m")


if __name__ == "__main__":

    # Define cmd line args #######################

    # Flags
    parser = argparse.ArgumentParser(description="Build and/or deploy binary executable from dev environment to device")
    parser.add_argument('-c', '--configure', help= 'Do cmake configuration', action='store_true')
    parser.add_argument('-b', '--build', help= 'Build binary flag', action='store_true')
    parser.add_argument('-d', '--deploy', help='Deploy binary to device flag', action='store_true')
    parser.add_argument('-t', '--test', help='Run tests remotely on device and get results', action='store_true')
    #Optionals
    parser.add_argument('-p', '--preset', metavar='', help='If known, a cmake generator preset for your system')
    parser.add_argument('-a', '--device_addr', metavar='', help='If not supplied by .env file, the device\'s ip address', default=None)

    # Parse cmd line args
    args = parser.parse_args()
    doConfig = args.configure
    doBuild = args.build
    doDeploy = args.deploy
    doTest = args.test
    chosen_preset = args.preset
    device_addr = args.device_addr

    if not any([doConfig, doBuild, doDeploy, doTest]):
        print(f"\033[31m-- Must select and action or combination of actions to do: [-b --build, -d --deploy]\033[0m")
        sys.exit(1)

    # Get necessary directory paths
    src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build_path = os.path.join(src_path, "build")
    presets_filepath = os.path.join(src_path, "CMakePresets.json")
    bin_dir = os.path.join(build_path, "bin")
    tests_dir = os.path.join(build_path, "test")
    bin_file = os.path.join(bin_dir, "SecurityCamera")
    tests_file = os.path.join(bin_dir, "unit_tests")


    # If device address is not given as a command line argument, get device address from .env file in src directory
    # TODO: Address must come from one of these two sources
    if device_addr is None:
        load_dotenv()
        device_addr = os.getenv('PI_HOST')

    # Paths and consts
    REMOTE_USER = "root"
    REMOTE_ADDR = f"{REMOTE_USER}@{device_addr}"
    REMOTE_DIR = "/var"
    REMOTE_BIN = f"/var/SecurityCamera"
    REMOTE_TESTS = f"/var/unit_tests"
    RESULTS_FILE = "test_results.xml"


    # Perform selected actions
    if doConfig:
        configure(build_path, src_path, presets_filepath, chosen_preset)
    if doBuild:
        build_binary(build_path)
    if doDeploy:
        deploy_binary(bin_file, tests_file, f"{REMOTE_ADDR}:{REMOTE_BIN}", f"{REMOTE_ADDR}:{REMOTE_TESTS}")
    if doTest:
        perform_tests(REMOTE_ADDR, REMOTE_TESTS, RESULTS_FILE)
        get_tests_report(f"{REMOTE_ADDR}:{REMOTE_DIR}/{RESULTS_FILE}", f"{tests_dir}/{RESULTS_FILE}")

