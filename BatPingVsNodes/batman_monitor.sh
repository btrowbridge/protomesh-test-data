#!/bin/bash


echo "{\"datapoint\" : { "
echo "\"timestamp\": \"" $(date +%x_%r) "\" ,"
echo "'nodes': {"
sudo batctl o -t 10 -H | awk '{printf "{\"node\": { \"mac\": %s,  \"latency\":  %s, \"signal\": %s,  \"neighbor\": %s }},\n", $1, $2, $3, $4  }'
echo " },"
sudo batctl o -t 10 -H | wc -l | awk '{printf "\"total\": %s", $1 + 1 }'
echo " },"


