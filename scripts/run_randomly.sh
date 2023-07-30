#!/bin/bash

# Get a random number between 0 and 99
RAND_NUM=$(($RANDOM % 100))
ECHO $RAND_NUM

# Set a threshold, for example, to run the script 4 out of 24 times in a day on average
# 4/24 = 1/6, so the threshold is roughly 16.66 or 17 out of 100
THRESHOLD=17

if [ $RAND_NUM -lt $THRESHOLD ]; then
    /usr/local/bin/python3 /Users/chris/code/coinex/hodl_pre.py
fi
