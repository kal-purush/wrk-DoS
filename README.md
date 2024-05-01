# wrk-DoS: CPU-Based Denial of Service (DoS) Attack Simulator

wrk-DoS is an easy-to-use tool designed for developers and researchers to simulate various CPU-based Denial of Service (DoS) attacks against their systems and evaluate their impact. This tool allows users to measure the severity of known CPU exhaustion vulnerabilities or the effectiveness of existing defenses through a series of experiments.

## Features

- Simulate different CPU-based DoS attacks
- Measure the impact of attacks on target systems
- Assess the severity of known CPU exhaustion vulnerabilities
- Evaluate the effectiveness of existing defenses

## Installation

1. Clone the wrk-DoS repository:
```
git clone https://github.com/your_username/wrk-DoS.git
```
2. Navigate to the wrk-DoS directory:
```
cd wrk-DoS
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

## USAGE AND OPTIONS
```
python wrk-DoS.py [options]
```
A simple command line tool for conducting load tests.

## Options:
```
  -c, --connections                         Connections to keep open, default 100
  -b, --benign-user                         Number of benign users, default 1
  -m, --attacker                            Number of attackers, default 1
  -d, --duration                            Duration of test in seconds, default 60s
  -t, --attack-start-time                   Starting time of the attack, default 15th second
  -T, --attack-duration                     Duration of the attack in seconds, default 10s
  -H, --header                              Add header to request
  --payload                                 Add payload to request
  -R, --rate                                Work rate (throughput) in requests/sec (total) [Required Parameter]
  -u, --benign-api                          Benign API endpoint [Required Parameter]
  -a, --malicious-api                       Malicious API endpoint [Required Parameter]
  -p, --path                                The directory path where the result should be saved [Required Parameter]
```
## Required Parameters:
```
  -R, --rate                                The work rate (throughput) in requests per second (total).
  -u, --benign-api                          The endpoint for the benign API.
  -a, --malicious-api                       The endpoint for the malicious API.
  -p, --path                                The directory path where the result should be saved.
```

## Example:
```
python wrk-DoS.py -c 200 -b 5 -m 2 -d 120 -t 5 -T 60 -H "Authorization: Token my_token" --payload "data=example" -R 100 -u http://example.com/api/benign -a http://example.com/api/malicious -p /path/to/save/results
```
