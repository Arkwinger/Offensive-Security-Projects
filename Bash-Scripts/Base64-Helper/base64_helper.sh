#!/bin/bash

if [ "$1" == "encode" ]; then

    echo "$2" | base64

elif [ "$1" == "decode" ]; then

    echo "$2" | base64 -d

else

    echo "Usage:"
    echo "./base64_helper.sh encode <text>"
    echo "./base64_helper.sh decode <base64>"
fi
