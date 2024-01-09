import platform
import subprocess
import sys


def get_system_info():
    system_info = {
        'OS': platform.system(),
        'OS Release': platform.release(),
        'Architecture': platform.architecture(),
        'Python Version': platform.python_version(),
    }
    return system_info


def check_python_installation():
    try:
        subprocess.run([sys.executable, '--version'], check=True)
        print("Python is already installed.")
    except FileNotFoundError:
        print("Python not found. Installing Python...")
        install_python()

def install_python():
    if platform.system() == "Linux":
        subprocess.run(['sudo', 'apt-get', 'install', 'python3'])
    elif platform.system() == "Windows":
        subprocess.run(
            ['powershell', 'Start-Process', 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe'])
    elif platform.system() == "Darwin":
        subprocess.run(['brew', 'install', 'python@3.10'])
    else:
        print("Unsupported OS. Manual installation of Python is required.")


check_python_installation()
