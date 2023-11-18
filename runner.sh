!/bin/bash

for ((i=0;i<=10;i++)); do
    python3 twitter/twitter-tweets-crawler.py $i
    if [ $((i % 10)) -eq 0 ]; then
        echo "Sleeping for 10 minutes..."
        sleep 600  # 600 seconds = 10 minutes
    fi
done