import os
import sys
import platform
import subprocess

def remove_quotes(s):
    return s.replace("\"", "").replace("\'", "").replace("\`", "")

def detect_os():
    current_os = platform.system()
    if current_os == "Linux":
        return "linux"
    elif current_os == "Darwin":
        return "mac"
    else:
        raise RuntimeError(f"This script is not supported on {current_os}. Please run it on Linux, or macOS.")

def get_url(os):
    url = f"https://s3.ap-south-1.amazonaws.com/releases.knowl.io/api-docs/apidocs_{os}"
    binary_name = f"apidocs_{os}"
    return url, binary_name

def run_subprocess(command, name="Operation"):
    try:
        binary_process = subprocess.Popen(command, universal_newlines=True,)
        binary_process.wait()
        if binary_process.returncode == 0:
            print(f"{name} completed successfully.")
        else:
            print(
                f"{name} failed with return code {binary_process.returncode}."
            )
            return 1
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error while running the script: {e}")
        return 1

MANDATORY_ENV_VARIABLE = ["OPENAI_API_KEY"]

def main():
    repo = sys.argv[1]
    if len(sys.argv) < 2:
        raise RuntimeError("Path to Repo not provided")
    repo_env_path = os.path.join(repo, ".knowlenv")
    if os.path.exists(repo_env_path):
        print("Loading variables from .knowlenv file.")
        with open(repo_env_path, "r") as file:
            lines = file.readlines()
        for line in lines:
            line_split = line.split("=")
            env_key = line_split[0]
            env_value = remove_quotes(line_split[1])
            os.environ[env_key] = env_value        
    else:
        print(".env file not found.")

    for v in MANDATORY_ENV_VARIABLE:
        if v not in os.environ.keys():
            raise RuntimeError(f"{v} not found in ENVIRONMENT VARIABLES. Either add it to .knowlenv files or it add permanently as Environment variable")

    current_os = detect_os()
    url, binary_name = get_url(current_os)
    path = os.path.join(os.getcwd(), binary_name)
    if os.path.exists(path):
        print("Binary file already exist. Deleting the old file.")
        os.remove(path)
    command = ["wget", url]
    run_subprocess(command, "Downloading binary")
    command = ["chmod", "+x", path]
    run_subprocess(command, "Granting Executable Permission")
    command = [path, repo]
    run_subprocess(command, "Document Generation")
