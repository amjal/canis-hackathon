!/bin/bash

for ((i=0;i<=200;i++)); do
    python3 twitter/twitter-following-extractor.py $i
done
