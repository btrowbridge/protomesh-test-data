#!/bin/bash


#ARGS:
#       $1=output file name
#       $2=duration for each test (minutes)
#       $3=spacing between increments (minutes
#       $4=spacing between samp (seconds)


echo "[[[BEGINNING ALL TESTS on $(date)]]]"


fileTag=${1:-$(date)}
duration=${2:-30}
increment_rate=${3:-5}
sample_rate=${4:-1}

((duration *= 60))
((increment_rate *= 60))

./bat_it_test.sh $fileTag $seconds $increment_rate $sample_rate
./txpower_test.sh $fileTag $seconds $increment_rate $sample_rate

echo "[[[TEST COMPLETE ON $(date)]]]"

