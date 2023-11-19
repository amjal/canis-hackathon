#!/bin/bash

for ((i=74;i<=100;i++)); do
    python3 twitter/twitter-tweets-crawler.py $i
    if [ $((i % 10)) -eq 0 ]; then
        echo "Sleeping for 5 minutes..."
        sleep 600  # 600 seconds = 10 minutes
    fi
done
