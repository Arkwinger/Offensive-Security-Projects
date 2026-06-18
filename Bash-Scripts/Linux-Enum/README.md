# Linux Enumeration

A simple Bash script that gathers basic system information commonly reviewed during Linux host enumeration.

## Features

* Current user information
* Hostname and operating system details
* Kernel information
* Network interfaces and IP addresses
* Active network connections
* Logged-in users
* Sudo permissions
* Home directory enumeration
* World-writable file discovery

## Usage

Make the script executable:

```bash
chmod +x enum.sh
```

Run the script:

```bash
./enum.sh
```

## Example Output

```text
[+] Current User
root

[+] Hostname
target-host

[+] Kernel Information
Linux target-host 5.15.0

[+] IP Addresses
192.168.1.100
```

## Disclaimer

This script is intended for educational purposes, lab environments, and authorized security assessments only.
