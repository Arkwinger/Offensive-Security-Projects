#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./clean_wordlist.sh <wordlist>"
    exit 1
fi

sort "$1" | uniq > cleaned.txt

echo "[+] Cleaned wordlist saved as cleaned.txt"
echo "[+] Original entries: $(wc -l < "$1")"
echo "[+] Unique entries: $(wc -l < cleaned.txt)"
