import os
import webbrowser
import psutil
import subprocess

def open_chrome():
    """Opens Google Chrome."""
    webbrowser.open("https://www.google.com")

def open_calculator():
    try:
        os.system("calc")  # Windows
    except Exception:
        os.system("gnome-calculator")  # Linux

def open_notepad():
    try:
        os.system("notepad")  
    except Exception:
        os.system("gedit")  

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent

def run_shell_command(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout if result.stdout else result.stderr

def open_file_explorer():
    try:
        os.system("explorer")  # Windows
    except Exception:
        os.system("nautilus")  # Linux

def list_directory(path: str = "."):
    return os.listdir(path)
