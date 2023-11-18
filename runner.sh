#!/bin/bash

for ((i=198;i<=200;i++)); do
    python3 twitter/twitter-tweets-crawler.py $i
    if [ $((i % 10)) -eq 0 ]; then
        echo "Sleeping for 5 minutes..."
        sleep 300  # 600 seconds = 10 minutes
    fi
done
