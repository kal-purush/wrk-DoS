import argparse
import os
import sys
from urllib.parse import urlparse
import validators

class CommandLineTool:
    def uri_validator(self, x):
        return validators.url(x)
    
    def show_usages(self):
         print("Usage: wrk <options> <url>                        \n"
           "  Options:                                            \n"
           "    -c, --connections <N>  Connections to keep open   \n"
           "    -d, --duration    <T>  Duration of test           \n"
           "    -t, --threads     <N>  Number of threads to use   \n"
           "                                                      \n"
           "    -s, --script      <S>  Load Lua script file       \n"
           "    -H, --header      <H>  Add header to request      \n"
           "    -L  --latency          Print latency statistics   \n"
           "    -U  --u_latency        Print uncorrected latency statistics\n"
           "        --timeout     <T>  Socket/request timeout     \n"
           "    -B, --batch_latency    Measure latency of whole   \n"
           "                           batches of pipelined ops   \n"
           "                           (as opposed to each op)    \n"
           "    -v, --version          Print version details      \n"
           "    -R, --rate        <T>  work rate (throughput)     \n"
           "                           in requests/sec (total)    \n"
           "                           [Required Parameter]       \n"
           "                                                      \n"
           "                                                      \n"
           "  Numeric arguments may include a SI unit (1k, 1M, 1G)\n"
           "  Time arguments may include a time unit (2s, 2m, 2h)\n")
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A simple command line tool")
        self.parser.add_argument("-c", "--connections", help="Connections to keep open, default 100")
        self.parser.add_argument("-b", "--benign-user", help="Number of benign users, default 1")
        self.parser.add_argument("-m", "--attacker", help="Number of attacker, default 1")
        self.parser.add_argument("-d", "--duration", help="Duration of test in seconds, default 60s")
        self.parser.add_argument("-t", "--attack-start-time", help=" Starting time of the attack, default 15th second")
        self.parser.add_argument("-T", "--attack-duration", help="Duration of the attack in seconds, default 10s")
        self.parser.add_argument("-H", "--header", help="Add header to request")
        self.parser.add_argument("--payload", help="Add header to request")
        self.parser.add_argument("-R", "--rate", help="Work rate (throughput) in requests/sec (total) [Required Parameter]")
        self.parser.add_argument("-u", "--benign-api", help="Benign API endpoint [Required Parameter]")
        self.parser.add_argument("-a", "--malicious-api", help="Malicious API endpoint [Required Parameter]")
        self.parser.add_argument("-p", "--path", help=" The directory paths where the result should be saved [Required Parameter]")

        # self.parser.add_argument("-o", "--output", help="Output file")
        # self.parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
        # self.parser.add_argument("-h", action="help", help="Show this help message and exit")

        # ./wrk -t1 -c50 -d60s -R$r "$url" $con 50 $framework_name $t 0 $i $r $file_path &
    def run(self):
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

        self.validate_configuration()

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

    def set_file_path(self, path):
        if path is None:
            print("File path is required.")
            sys.exit(1)
        else:
            self.path = path

    def set_benign_api(self, benign_api):
        if benign_api is None:
            print("Benign API endpoint is required.")
            sys.exit(1)
        else:
            if not self.uri_validator(benign_api):
                print("Benign API endpoint is not valid.")
                sys.exit(1)
            self.benign_url = benign_api

    def set_malicious_api(self, malicious_api):
        if malicious_api is None:
            print("Malicious API endpoint is required.")
            sys.exit(1)
        else:
            if not self.uri_validator(malicious_api):
                print("Malicious API endpoint is not valid.")
                sys.exit(1)
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
    cli.run()
