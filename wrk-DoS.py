import argparse
import os
import subprocess
import sys
import time
from urllib.parse import urlparse
import pandas as pd
import validators
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

class CommandLineTool:
    def uri_validator(self, x):
        return validators.url(x)
    
    # def show_usages(self):
    #      print("Usage: wrk <options> <url>                        \n"
    #        "  Options:                                            \n"
    #        "    -c, --connections <N>  Connections to keep open   \n"
    #        "    -d, --duration    <T>  Duration of test           \n"
    #        "    -t, --threads     <N>  Number of threads to use   \n"
    #        "                                                      \n"
    #        "    -s, --script      <S>  Load Lua script file       \n"
    #        "    -H, --header      <H>  Add header to request      \n"
    #        "    -L  --latency          Print latency statistics   \n"
    #        "    -U  --u_latency        Print uncorrected latency statistics\n"
    #        "        --timeout     <T>  Socket/request timeout     \n"
    #        "    -B, --batch_latency    Measure latency of whole   \n"
    #        "                           batches of pipelined ops   \n"
    #        "                           (as opposed to each op)    \n"
    #        "    -v, --version          Print version details      \n"
    #        "    -R, --rate        <T>  work rate (throughput)     \n"
    #        "                           in requests/sec (total)    \n"
    #        "                           [Required Parameter]       \n"
    #        "                                                      \n"
    #        "                                                      \n"
    #        "  Numeric arguments may include a SI unit (1k, 1M, 1G)\n"
    #        "  Time arguments may include a time unit (2s, 2m, 2h)\n")
    def format_headers(self):
        formatted_headers = ""
        for key, value in self.headers.items():
            formatted_headers += f'-H "{key}: {value}" '
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
        with open(path) as in_file:
            for line in in_file:
                if "1970" not in line:
                    parts = line.split(' ')  # Split each line by whitespace
                    # print(parts)
                    timestamp = parts[6]  # Extract timestamp
                    value = int(parts[0])  # Extract value
                    time_stamps.append(timestamp)
                    values.append(value)
        
        data = pd.DataFrame({'time':time_stamps, 'value':values})
        return data

    def save_figure(self, data, ext):
        df = data
        sns.set_palette("Set2")
        fig, axes = plt.subplots(2, 1, figsize=(14, 8))
        time_counts = df['time'].value_counts().sort_index()
        time_counts.plot(marker='o', ax=axes[0])
        axes[0].set_title('Count of Time Points')
        axes[0].set_xlabel('Time')
        axes[0].set_ylabel('Count')
        axes[0].grid(True)

        sns.histplot(df['value'], bins=30, kde=True, color='skyblue', ax=axes[1])
        axes[1].set_title('Histogram of Latency Values')
        axes[1].set_xlabel('Latency')
        axes[1].set_ylabel('Frequency')
        axes[1].grid(True)
        plt.tight_layout()

        # sns.set(style='white')
        # plt.figure(figsize=(14, 6))
        # time_counts = df['time'].value_counts().sort_index()
        # time_counts.plot(marker='o')
        # plt.title('Count of Time Points')
        # plt.xlabel('Time')
        # plt.ylabel('Count')
        # plt.grid(True)
        # plt.savefig(f"result/{ext}_throughput.pdf")  # Save the figure

        # # Plotting distribution of values
        # plt.figure(figsize=(14, 6))
        # # sns.kdeplot(df['value'], fill=True, color='skyblue')
        # sns.histplot(df['value'], bins=30, kde=True, color='skyblue')
        # plt.title('Distribution of Values')
        # plt.xlabel('Value')
        # plt.ylabel('Density')
        # plt.grid(True)
        plt.savefig(f"result/{ext}.pdf")  # Save the figure




    def run(self):
        headers = self.format_headers()
        benign_process = subprocess.Popen(["./wrk", f"-t{self.number_of_benign_user}", f"-c{self.numer_of_connection}", f"-d{self.duration}s", f"-R{self.work_rate}", 
                            f"{self.benign_url}", headers, "-m", "0",  "-p", self.path], stdout=subprocess.PIPE, text=True)
        time.sleep(self.attack_start_time)
        print("Attack Started................................")

        malicious_process = subprocess.Popen(["./wrk", f"-t{self.number_of_malicious_user}", f"-c{self.numer_of_connection}", f"-d{self.attack_duration}s", f"-R{self.work_rate}", 
                            f'{self.malicious_url}', headers, "-m", "1", "-p", self.path], stdout=subprocess.PIPE, text=True)

        malicious_process.wait()
        print("Attack Finished................................")
        # print(malicious_process.stdout.read())
        benign_process.wait()

        print("Preparing Statistics................................")

        benign_data = self.parse_input("result/latency_per_req_benign.txt")
        malicious_data = self.parse_input("result/latency_per_req_malicious.txt")
        
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
        self.parser.add_argument("-R", "--rate", help="Work rate (throughput) in requests/sec (total) [Required Parameter]")
        self.parser.add_argument("-u", "--benign-api", help="Benign API endpoint [Required Parameter]")
        self.parser.add_argument("-a", "--malicious-api", help="Malicious API endpoint [Required Parameter]")
        self.parser.add_argument("-p", "--path", help="The directory paths where the result should be saved [Required Parameter]")
        self.parser.add_argument("-H", "--header", action="append", help="Add header to request (e.g., 'key:value')")

        # self.parser.add_argument("-o", "--output", help="Output file")
        # self.parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
        # self.parser.add_argument("-h", action="help", help="Show this help message and exit")

        # ./wrk -t1 -c50 -d60s -R$r "$url" $con 50 $framework_name $t 0 $i $r $file_path &
    def parse_argument(self):
        args = self.parse_arguments()

        self.set_work_rate(args.rate)
        self.set_file_path(args.path)
        self.set_benign_api(args.benign_api)
        self.set_malicious_api(args.malicious_api)
        self.set_number_of_connections(args.connections)
        self.set_number_of_benign_users(args.benign_user)
        self.set_number_of_malicious_users(args.attacker)
        self.set_duration(args.duration)
        self.set_attack_start_time(args.attack_start_time)
        self.set_attack_duration(args.attack_duration)
        self.set_headers(args.header)
        self.set_payload(args.payload)
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

    def create_folder(self, folder_path):
        try:
            os.makedirs(folder_path)
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
            self.path = path

    def set_benign_api(self, benign_api):
        if benign_api is None:
            print("Benign API endpoint is required.")
            sys.exit(1)
        else:
            # if not self.uri_validator(benign_api):
            #     print("Benign API endpoint is not valid.")
            #     sys.exit(1)
            self.benign_url = benign_api

    def set_malicious_api(self, malicious_api):
        if malicious_api is None:
            print("Malicious API endpoint is required.")
            sys.exit(1)
        else:
            # if not self.uri_validator(malicious_api):
            #     print("Malicious API endpoint is not valid.")
            #     sys.exit(1)
            self.malicious_url = malicious_api

    def set_number_of_connections(self, connections):
        if connections:
            self.numer_of_connection = int(connections)
        else:
            self.numer_of_connection = 10

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

    # def run(self):
    #     try:
    #         args = self.parser.parse_args()
    #         print(args)
    #         if args.rate is None:
    #             print("Work rate (throughput) in requests/sec is required.")
    #             sys.exit(1)
    #         else:
    #             self.work_rate = int(args.rate)
            
    #         if args.path is None:
    #             print("File path is required.")
    #             sys.exit(1)
    #         else:
    #             self.path = args.path
            
    #         if args.benign_api is None:
    #             print("Benign API endpoint is required.")
    #             sys.exit(1)
    #         else:
    #             if not self.uri_validator(args.benign_api):
    #                 print("Benign API endpoint is not valid.")
    #                 sys.exit(1)
    #             self.benign_url = args.benign_api
            
    #         if args.malicious_api is None:
    #             print("Malicious API endpoint is required.")
    #             sys.exit(1)
    #         else:
    #             if not self.uri_validator(args.malicious_api):
    #                 print("Malicious API endpoint is not valid.")
    #                 sys.exit(1)
    #             self.malicious_url = args.malicious_api

    #         if args.connections:
    #             self.numer_of_connection = int(args.connections)
    #             # print(self.numer_of_connection)
    #         else:
    #             self.numer_of_connection = 50
            
    #         if args.benign_user:
    #             self.number_of_benign_user = int(args.benign_user)
    #             # print(self.number_of_benign_user)
    #         else:
    #             self.number_of_benign_user = 1

    #         if args.attacker:
    #             self.number_of_malicious_user = int(args.attacker)
    #             # print(self.number_of_malicious_user)
    #         else:
    #             self.number_of_malicious_user = 1
            
    #         if self.number_of_malicious_user>self.number_of_benign_user:
    #             print("Number of benign users should be greater than or equal to the number of attackers.")
    #             os._exit(1)
            
    #         if args.duration:
    #             self.duration = int(args.duration)
    #             # print(self.number_of_malicious_user)
    #         else:
    #             self.duration = 60
            
    #         if args.attack_start_time:
    #             self.attack_start_time=int(args.attack_start_time)
    #         else:
    #             self.attack_start_tim = 15
            
    #         if args.attack_duration:
    #             self.attack_duration = int(args.attack_duration)
    #         else:
    #             self.attack_duration = 10
            

    #         # if ar

    #         # if args.verbose:
    #         #     print("Input file:", args.input)
    #         #     if args.output:
    #         #         print("Output file:", args.output)
    #         #     print("Verbose mode activated")
    #         # else:
    #         #     self.show_usages()
    #         #     print("Input file:", args.input)
    #         #     if args.output:
    #         #         print("Output file:", args.output)
    #     except:
    #         print("here")
    #         # self.parser.print_help()
    #         self.show_usages()

if __name__ == "__main__":
    cli = CommandLineTool()
    # cli.print_usage()
    cli.parse_argument()
    cli.run()
    # print(cli.headers)
