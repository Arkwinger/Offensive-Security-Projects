# Log Parser

A simple Bash script that extracts failed login attempts and summarizes IP address activity from log files.

## Features

* Detects failed login events
* Extracts IP addresses from logs
* Displays the most frequently observed IP addresses
* Useful for basic log review and incident analysis

## Usage

Make the script executable:

```bash
chmod +x log_parser.sh
```

Run the script:

```bash
./log_parser.sh <logfile>
```

Example:

```bash
./log_parser.sh auth.log
```

## Disclaimer

This script is intended for educational purposes, lab environments, and authorized security assessments only.
