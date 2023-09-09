import subprocess
import sys
import os
import ctypes
import time





def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    if is_admin():
        stop_windows_update_service()
    else:
        # Re-launch the script as administrator
        script_path = os.path.abspath(sys.argv[0])
        params = ' '.join([script_path] + sys.argv[1:])
        shell_cmd = f'powershell -Command "Start-Process \'{sys.executable}\' -ArgumentList \'{params}\' -Verb RunAs"'
        subprocess.run(shell_cmd, shell=True)

def stop_windows_update_service():

    try:
        subprocess.run(['net', 'stop', 'wuauserv'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Windows Update service: {e}")
    except FileNotFoundError:
        print("Error: 'net' command not found. This script is meant to run on Windows.")


if __name__ == "__main__":
    while True:

        run_as_admin()
        # Wait for 20 minutes before the next execution
        time.sleep(5 * 60)
