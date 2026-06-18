# CIDR Expander

A simple Python utility that expands a CIDR range and displays all available host addresses.

## Features

* Expands IPv4 CIDR ranges
* Displays valid host addresses
* Lightweight and easy to use
* Uses Python's built-in `ipaddress` module

## Usage

Run the script:

```bash id="a4l6wq"
python cidr_expander.py
```

Enter a CIDR range when prompted:

```text id="m9d3rk"
10.10.10.0/24
```

The script will display all valid host addresses within the specified range.

## Example Output

```text id="7z1vbp"
10.10.10.1
10.10.10.2
10.10.10.3
...
```

## Disclaimer

This utility is intended for educational purposes, lab environments, and authorized security assessments only.
