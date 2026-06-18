#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./log_parser.sh <logfile>"
    exit 1
fi

echo "[+] Failed Login Attempts"
grep -i "failed" "$1"

echo ""
echo "[+] Top IP Addresses"

grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' "$1" |
sort |
uniq -c |
sort -nr |
head
