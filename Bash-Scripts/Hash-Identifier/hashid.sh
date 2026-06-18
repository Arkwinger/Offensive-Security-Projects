#!/bin/bash

hash=$1

if [ -z "$hash" ]; then
    echo "Usage: ./hashid.sh <hash>"
    exit 1
fi

length=${#hash}

echo "Hash Length: $length"

case $length in
    32)
        echo "Possible: MD5"
        ;;
    40)
        echo "Possible: SHA1"
        ;;
    56)
        echo "Possible: SHA224"
        ;;
    64)
        echo "Possible: SHA256"
        ;;
    96)
        echo "Possible: SHA384"
        ;;
    128)
        echo "Possible: SHA512"
        ;;
    *)
        echo "Unknown hash type"
        ;;
esac
