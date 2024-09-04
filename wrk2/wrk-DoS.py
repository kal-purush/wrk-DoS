import argparse
from datetime import datetime
import os
import subprocess
import sys
import time
from urllib.parse import urlencode, urlparse
import pandas as pd
import validators
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shlex import split

class CommandLineTool:
    def uri_validator(self, x):
        return validators.url(x)
    
    def format_headers(self):
        formatted_headers = ""
        for key, value in self.headers.items():
            # print(value)
            # value = urlencode(value)
            formatted_headers += f'-H \"{key}: {value}\"'
        return formatted_headers.strip()

    def print_usage(self):
        print("Usage:")
        max_length = max(len(action.option_strings) for action in self.parser._actions if isinstance(action, argparse._StoreAction))
        for action in self.parser._actions:
            if isinstance(action, argparse._StoreAction):
                flags = ", ".join(action.option_strings)
                flags_padded = flags.ljust(max_length)
                default = f"[default: {action.default}]" if action.default is not None else ""
                help_text = action.help
                print(f"{flags_padded.ljust(35)}{help_text.ljust(70)}{default}")

    def parse_input(self, path):
        time_stamps =[]
        values =[]
        mp={}
        with open(path) as in_file:
            for line in in_file:
                if "0 0 0" not in line:
                    parts = line.split(' ')  # Split each line by whitespace
                    # timestamp = datetime.fromtimestamp(int(parts[-1].strip())/1000000).strftime('%H:%M:%S')
                    timestamp = int(parts[-2].strip())  # Extract timestamp
                    value = int(parts[0])  # Extract value
                    time_stamps.append(timestamp)
                    values.append(value)
                    mp.setdefault(timestamp, []).append(value/1000)
        
        # data = pd.DataFrame({'time':time_stamps, 'value':values})
        # return data
        return mp

    def save_figure(self, data, ext):
        values = []
        time_stamps = []
        if ext == 'benign':
            thoughput_file_path = f"{self.path}/req_per_sec_benign.txt"
        else:
            thoughput_file_path = f"{self.path}/req_per_sec_malicious.txt"
        with open(thoughput_file_path) as in_file:
            for line in in_file:
                if len(line.strip())>0 and "-1" not in line:
                    parts = line.split(' ')  # Split each line by whitespace
                    timestamp = int(parts[1].strip()) 
                    value = int(parts[0])  # Extract value
                    time_stamps.append(timestamp)
                    values.append(value)

        df = data
        sns.set_palette("Set2")
        fig, axes = plt.subplots(2, 1, figsize=(14, 8))
        # time_counts = df['time'].value_counts().sort_index()
        # # time_counts.plot(marker='o', ax=axes[0])
        # reqs = []
        # for time_value in time_counts.keys():
        #     count_value = time_counts[time_value]
        #     reqs.append(count_value)
        a=np.arange(len(values))
        # print(a)
        experiment_duration = self.attack_duration
        sns.lineplot(x=a,y=values, lw=5, label="Actual Throught", marker=".", markersize=12, ax=axes[0])
        if ext == 'benign':
            axes[0].axhline(y=self.work_rate, lw=3, label="Expected Throught", color='orange')
            axes[0].axvline(x=self.attack_start_time, ls='--', lw=2, color='red')
            axes[0].axvline(x=self.attack_start_time+self.attack_duration, ls='--', lw=2, color='red')
            axes[0].legend()
            experiment_duration = self.duration
        # axes[0].set_ylim([0, self.work_rate+5])
        axes[0].set_title('Throughput')
        axes[0].set_xlabel('Time')
        axes[0].set_ylabel('Throughput')
        axes[0].grid(True)
        
        time_series_lst=[[] for i in range(experiment_duration+5)]
        for key in data:
            time_series_lst[key]+=data[key]
        # sns.boxplot(x='time', y='value', data=data, ax=axes[1])
        axes[1].boxplot(time_series_lst, patch_artist=True, notch=True)
        axes[1].set_title('Latency')
        axes[1].set_xlabel('Time')
        axes[1].set_ylabel('Latency')
        # axes[1].grid(True)
        axes[1].set_xticks(a)
        axes[1].set_xticklabels(a)
        
        xticks = axes[1].get_xticks()  # Get current xticks
        if ext == 'benign':
            axes[1].set_xticks(xticks[::10])
        else:
            axes[1].set_xticks(xticks[::2])
        # axes[1].set_yscale('log')
        plt.tight_layout()
        plt.savefig(f"{self.path}/{ext}.pdf")  # Save the figure


    def run(self):
        headers = self.format_headers()
        # print(headers)
        # benign_process = subprocess.Popen(["./wrk", f"-t{self.number_of_benign_user}", f"-c{self.numer_of_connection}", f"-d{self.duration}s", f"-R{self.work_rate}", 
        #                     f"{self.benign_url}", headers, "-m", "0",  "-p", self.path], stdout=subprocess.PIPE, text=True)

        benign_process = subprocess.Popen(split(f"./wrk -t{self.number_of_benign_user} -c{self.numer_of_connection} -d{self.duration}s -R{self.work_rate} {self.benign_url} -m 0 -p{self.path}"), stdout=subprocess.PIPE, text=True)

        time.sleep(self.attack_start_time)
        print("Attack Started................................")

        # malicious_process = subprocess.Popen(["./wrk", f"-t{self.number_of_malicious_user}", f"-c{self.numer_of_connection}", f"-d{self.attack_duration}s", f"-R{self.work_rate}", 
        #                     f'{self.malicious_url}', headers, "-m", "1", "-p", self.path], stdout=subprocess.PIPE, text=True)

        malicious_process = subprocess.Popen(split(f"./wrk -t{self.number_of_malicious_user} -c{self.numer_of_connection} -d{self.attack_duration}s -R{self.attack_rate} {self.malicious_url} {headers} -m 1 -p{self.path}"), stdout=subprocess.PIPE, text=True)

        malicious_process.wait()
        print("Attack Finished................................")
        print(malicious_process.stdout.read())
        print(benign_process.stdout.read())
        benign_process.wait()

        print("Preparing Statistics................................")

        benign_data = self.parse_input(f"{self.path}/latency_per_req_benign.txt")
        malicious_data = self.parse_input(f"{self.path}/latency_per_req_malicious.txt")
        
        print("Ploting Figures................................")

        self.save_figure(benign_data, 'benign')
        self.save_figure(malicious_data, 'malicious')

        print("Done ................................")

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A simple command line tool")
        self.parser.add_argument("-c", "--connections", help="Connections to keep open, default 100")
        self.parser.add_argument("-b", "--benign-user", help="Number of benign users, default 1")
        self.parser.add_argument("-m", "--attacker", help="Number of attacker, default 1")
        self.parser.add_argument("-d", "--duration", help="Duration of test in seconds, default 60s")
        self.parser.add_argument("-t", "--attack-start-time", help="Starting time of the attack, default 15th second")
        self.parser.add_argument("-T", "--attack-duration", help="Duration of the attack in seconds, default 10s")
        # self.parser.add_argument("-H", "--header", help="Add header to request")
        self.parser.add_argument("--payload", help="Payload to include in the request")
        self.parser.add_argument("--attack-rate", help="--attack-rate Attack rate (throughput) in requests/sec (total) [Required Parameter]")
        self.parser.add_argument("-R", "--rate", help="-R Work rate (throughput) in requests/sec (total) [Required Parameter]")
        self.parser.add_argument("-u", "--benign-api", help="--benign-api Benign API endpoint [Required Parameter]")
        self.parser.add_argument("-a", "--malicious-api", help="--malicious-api Malicious API endpoint [Required Parameter]")
        self.parser.add_argument("-p", "--path", help="-p --path The directory paths where the result should be saved [Required Parameter]")
        self.parser.add_argument("-H", "--header", action="append", help="Add header to request (e.g., 'key:value')")

        # self.parser.add_argument("-o", "--output", help="Output file")
        # self.parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
        # self.parser.add_argument("-h", action="help", help="Show this help message and exit")

        # ./wrk -t1 -c50 -d60s -R$r "$url" $con 50 $framework_name $t 0 $i $r $file_path &
    def parse_argument(self):
        args = self.parse_arguments()
        self.set_payload(args.payload)
        self.set_headers(args.header)
        self.set_attack_rate(args.attack_rate)
        self.set_work_rate(args.rate)
        self.set_benign_api(args.benign_api)
        self.set_malicious_api(args.malicious_api)
        self.set_number_of_connections(args.connections)
        self.set_number_of_benign_users(args.benign_user)
        self.set_number_of_malicious_users(args.attacker)
        self.set_duration(args.duration)
        self.set_attack_start_time(args.attack_start_time)
        self.set_attack_duration(args.attack_duration)
        self.set_file_path(args.path)
        self.validate_configuration()
    
    def set_payload(self, payload):
        if payload is not None:
            self.payload = payload
        else:
            self.payload = ""

    
    def set_headers(self, headers):
        self.headers = {}
        if headers:
            for header in headers:
                try:
                    key, value = header.split(':', 1)
                    if key == 'payload':
                        self.payload = value
                    self.headers[key.strip()] = value.strip()
                except ValueError:
                    print("Invalid header format:", header)
                    sys.exit(1)

    def parse_arguments(self):
        try:
            return self.parser.parse_args()
        except argparse.ArgumentError:
            self.parser.print_help()
            sys.exit(1)

    def set_work_rate(self, rate):
        if rate is None:
            print("Work rate (throughput) in requests/sec is required.")
            sys.exit(1)
        else:
            self.work_rate = int(rate)
    
    def set_attack_rate(self, rate):
        if rate is None:
            print("Attack rate (throughput) in requests/sec is required.")
            sys.exit(1)
        else:
            self.attack_rate = int(rate)

    def create_folder(self, folder_path):
        try:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            result_folder_path = f"{folder_path}/{current_time}_{self.library}_{len(self.payload)}"
            os.makedirs(result_folder_path)
            self.path = result_folder_path
            # print(f"Folder '{folder_path}' created successfully.")
        except OSError as e:
            # print(f"Error: {e.strerror}")
            if not "File exists" in str(e.strerror):
                sys.exit(1)
    
    def set_file_path(self, path):
        if path is None:
            print("File path is required.")
            sys.exit(1)
        else:
            self.create_folder(path)
            

    def set_benign_api(self, benign_api):
        if benign_api is None:
            print("Benign API endpoint is required.")
            sys.exit(1)
        else:
            # if not self.uri_validator(benign_api):
            #     print("Benign API endpoint is not valid.")
            #     sys.exit(1)
            self.benign_url = benign_api
    
    def extract_library_name(self, url):
        # Split the URL by '/' and get the last non-empty part
        parts = url.rstrip('/').split('/')
        return parts[-1]

    def set_malicious_api(self, malicious_api):
        if malicious_api is None:
            print("Malicious API endpoint is required.")
            sys.exit(1)
        else:
            # if not self.uri_validator(malicious_api):
            #     print("Malicious API endpoint is not valid.")
            #     sys.exit(1)
            libray = self.extract_library_name(malicious_api)
            self.library = libray
            self.malicious_url = malicious_api

    def set_number_of_connections(self, connections):
        if connections:
            self.numer_of_connection = int(connections)
        else:
            self.numer_of_connection = 50

    def set_number_of_benign_users(self, benign_user):
        if benign_user:
            self.number_of_benign_user = int(benign_user)
        else:
            self.number_of_benign_user = 1

    def set_number_of_malicious_users(self, attacker):
        if attacker:
            self.number_of_malicious_user = int(attacker)
        else:
            self.number_of_malicious_user = 1

    def set_duration(self, duration):
        if duration:
            self.duration = int(duration)
        else:
            self.duration = 60

    def set_attack_start_time(self, attack_start_time):
        if attack_start_time:
            self.attack_start_time = int(attack_start_time)
        else:
            self.attack_start_time = 15

    def set_attack_duration(self, attack_duration):
        if attack_duration:
            self.attack_duration = int(attack_duration)
        else:
            self.attack_duration = 10

    def validate_configuration(self):
        if self.number_of_malicious_user > self.number_of_benign_user:
            print("Number of benign users should be greater than or equal to the number of attackers.")
            sys.exit(1)

    

if __name__ == "__main__":
    cli = CommandLineTool()
    # cli.print_usage()
    cli.parse_argument()
    cli.run()
    # print(cli.headers)
