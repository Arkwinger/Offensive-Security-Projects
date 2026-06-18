# IOC Extractor

A simple Python utility that extracts common Indicators of Compromise (IOCs) from text files.

## Features

* Extracts IPv4 addresses
* Extracts domain names
* Extracts URLs
* Extracts MD5 hashes
* Uses regular expressions for pattern matching
* Lightweight and easy to use

## Usage

Run the script:

```bash
python ioc_extractor.py
```

Provide a file when prompted:

```text
sample.txt
```

The script will scan the file and display any identified indicators.

## Example Output

```text
IP Addresses:
8.8.8.8

Domains:
example.com

URLs:
https://example.com/login

MD5 Hashes:
5f4dcc3b5aa765d61d8327deb882cf99
```

## Disclaimer

This utility is intended for educational purposes, lab environments, and authorized security assessments only.
