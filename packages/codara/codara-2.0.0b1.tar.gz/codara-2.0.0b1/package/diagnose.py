import subprocess
import threading
import requests
import datetime
import os
from package.token_utils import get_codararc_value
from package.utils import spinning_loader
from package.config import config


def format_command(command: str) -> str:
    return command.replace(' ', '-').replace('/', '-')


def diagnose_file_path(command: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    diagnosis_dir = 'diagnostics'
    if not os.path.exists(diagnosis_dir):
        os.makedirs(diagnosis_dir)

    file_name = f"{format_command(command)}_{timestamp}.txt"
    return os.path.join(diagnosis_dir, file_name)


def get_diagnostic_output(command: str) -> str or None:
    """Run a command and return the output or error as a string."""
    print('Running command...')
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check if there is an error
    if result.returncode != 0:
        # If there's an error, return the stderr as a string
        error_message = f"Error running command '{command}': {result.stderr}"
        return error_message

    # If no error, return the stdout
    return result.stdout.strip()


def diagnose_code(code: str) -> str or bool:
    print("Diagnosing...", end="", flush=True)
    task_done = threading.Event()
    loader_thread = threading.Thread(target=spinning_loader, args=(task_done,))
    headers = {
        'Authorization': f'Bearer {get_codararc_value("access_token")}'
    }

    try:
        loader_thread.start()
        url = f"{config.get('api_domain')}/api/gpt/generate-diagnosis"
        response = requests.post(url, json={"prompt": code}, headers=headers)
        if response.status_code == 201:
            response_data = response.json()
            review_content = response_data.get("diagnosis")
            if review_content is not None:
                print("\nDiagnosis received.")
                return review_content
            else:
                print('\n')
                print("Error: Code content not found in response")
                return False
        elif response.status_code == 400:
            print('\n')
            print(
                f"{response.status_code} ERROR: There was an issue diagnosis your code. The issue is most likely because the code error's output is too large and exceed our models maximum token limit. Please try again with a smaller error or upgrade your plan to allow for more tokens.")
            return False
        else:
            print('\n')
            print(f"{response.status_code} Error in diagnose_code: {response.json().get('error')}")
            return False
    finally:
        task_done.set()
        loader_thread.join()
