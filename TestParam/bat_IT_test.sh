#!/bin/bash

#ARGS: 
#	$1=output file name
#	$2=duration for each test 
#	$3=spacing between increments
#	$4=spacing between samp

#Initialize
./reset_defaults.sh

#Test Params
title=${1:- $(date)}
duration=${2:-60}
spacing=${3:-$((60 * 5))}
sample=${4:-1}

host=$(hostname)
filename=/home/pi/PiShare/$host/bat_it_test-$title.txt

echo $filename

#increment/decriment
it_increment=10
it_decriment=-10


#iterator
timer=0

#different method?

echo "[[[[BEGIN BATMAN IT TEST]]]]"
echo "Climbing UP...."

while [ $timer -lt $duration ]; do

	it_current=$(sudo batctl it)
	#SAMPLE
	sample_iterator=0
	while [ $sample_iterator -lt $spacing ] && [ $timer -lt $duration ]; do

		./batman_monitor.sh >> $filename
		((sample_iterator += $sample))
		sleep $sample
	done

	#Increment
	((timer += $sample_iterator))
	((it_current += $it_increment))
	sudo batctl it $it_current
	./batman_monitor.sh
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

                ./batman_monitor.sh >> $filename
                ((sample_iterator += $sample))
        	sleep $sample
	done

        #Increment
	((timer += $sample_iterator))
        ((it_current += $it_decriment))
        sudo batctl it $it_current
	./batman_monitor.sh
done


