!/bin/bash

for ((i=0;i<=199;i++)); do
    python3 twitter/twitter-following-extractor.py $i
done