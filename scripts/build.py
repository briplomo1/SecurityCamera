import shutil
import subprocess
import os
import json
import sys

# Get parent folder path which should be the main project directory
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

build_dir = os.path.join(src_dir, "build")
presets_file = os.path.join(src_dir, "CMakePresets.json")

print(f"\033[35m -- Running cmake build with source dir: \"{src_dir}\" and build dir: \"{build_dir}\"\033[0m")

# Get presets name from CMakePresets.json file
with open(presets_file, 'r') as f:
    presets = json.load(f)["configurePresets"]



# Try out all the presets
for preset in presets:
    preset_name = preset["name"]
    print(f"\033[35m -- Attempting cmake configuration with configuration preset: \"{preset_name}\"...\033[0m")
    # Remove old build folder and contents if exists
    if os.path.exists(build_dir):
        print("\033[35m -- Removing existing build prior to building...\033[0m")
        shutil.rmtree(build_dir)

    # Try configuration and show output
    config_res = subprocess.run(['cmake', '--preset', preset_name],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(config_res.stdout.decode())

    # If cmake config succeeds try cmake build
    if config_res.returncode == 0:
        print(f"\033[92m -- Succeeded in cmake configure with preset {preset_name}. "
              f"Attempting build...\n\033[0m")
        build_res = subprocess.run(['cmake', '--build', build_dir],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(build_res.stdout.decode())

        # Build succeeded. Exit script
        if build_res.returncode == 0:
            print(f"\033[92m -- Build succeeded for configuration preset {preset_name}\n\033[0m")
            sys.exit(0)
        else:
            print(f"\033[33m -- Build failed for configuration preset {preset_name}\n\033[0m")
            print(build_res.stderr.decode())
    else:
        print(f"\033[33m -- Preset {preset_name} failed\n\033[0m")
        print(config_res.stderr.decode())

print("\033[31m -- Unable to successfully configure and build with available configuration presets. "
      "Try installing one of the build generators if none are present and setting your path to include it.\033[0m")
