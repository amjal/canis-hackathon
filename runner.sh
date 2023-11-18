!/bin/bash

for ((i=80;i<=86;i++)); do
    python3 twitter/twitter-following-extractor.py $i
done