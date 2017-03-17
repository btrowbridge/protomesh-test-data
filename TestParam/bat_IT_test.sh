#!/bin/bash

#ARGS: 
#	$1=output file name
#	$2=duration for each test 
#	$3=spacing between increments
#	$4=spacing between samp

#Initialize
./reset_defaults.sh

#Test Params
title=${1:- $(date +"%F_%H-%M-%S")}
duration=${2:-60}
spacing=${3:-$((60 * 5))}
sample=${4:-1}

echo "[[[TEST PARAMS]]]"
echo "Tag: $title"
echo "Durration: $duration"
echo "Samples Per Change: $spacing"
echo "Sample Rate: $sample"

host=$(hostname)
filename="/home/pi/PiShare/$host/bat_it_test_${title}.txt"

echo $filename

#increment/decriment
it_increment=100
it_decriment=-100


#iterator
timer=0

#different method?

echo "[[[[BEGIN BATMAN IT TEST]]]]"
echo "Climbing UP...."
echo

while [ $timer -lt $duration ]; do

	it_current=$(sudo batctl it)
	#SAMPLE
	sample_iterator=0
	while [ $sample_iterator -lt $spacing ] && [ $timer -lt $duration ]; do

		./batman_monitor.sh >> "$filename"
		((sample_iterator += $sample))
		echo -n "."
		sleep $sample
	done

	#Increment
	((timer += $sample_iterator))
	((it_current += $it_increment))
	sudo batctl it $it_current
#	./batman_monitor.sh
	echo "*"
done

./reset_defaults

echo "[[[[RESET!]]]]"
echo "Climbing DOWN...."

let "timer = 0"


while [ $timer -lt $duration ] && [ $it_current -gt 0 ]; do

	it_current=$(sudo batctl it)
        #SAMPLE
        sample_iterator=0
        while [ $sample_iterator -lt $spacing ] && [ $timer -lt $duration ]; do

                ./batman_monitor.sh >> "$filename"
                ((sample_iterator += $sample))
        	sleep $sample
		echo -n "."
	done

        #Increment
	((timer += $sample_iterator))
        ((it_current += $it_decriment))
        sudo batctl it $it_current
#	./batman_monitor.sh
	echo "*"
done


