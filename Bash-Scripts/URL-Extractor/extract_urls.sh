#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./extract_urls.sh <file>"
    exit 1
fi

grep -oE 'https?://[^ ]+' "$1" | sort -u
