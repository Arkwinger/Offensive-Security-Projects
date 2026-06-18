# Nmap Parser

A simple Python utility that parses Nmap output files and extracts open ports and associated services.

## Features

* Parses standard Nmap output
* Identifies open TCP ports
* Extracts service information
* Displays a summary of discovered services

## Usage

Run the script:

```bash
python nmap_parser.py
```

Provide the path to an Nmap output file when prompted.

Example:

```text
scan.txt
```

## Example Output

```text
22/tcp - ssh
80/tcp - http
445/tcp - microsoft-ds

Total Open Ports: 3
```

## Disclaimer

This utility is intended for educational purposes, lab environments, and authorized security assessments only.
