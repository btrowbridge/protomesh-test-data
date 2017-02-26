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
filename=/home/pi/PiShare/$host/txpower_test-$title.txt

echo $filename

#increment/decriment
pow_increment=1
pow_decriment=-1


#iterator
timer=0

#different method?

echo "[[[[BEGIN TX POWER TEST]]]]"
echo "Climbing Up ...."


while [ $timer -lt $duration ]; do

	pow_current=$(sudo batctl it)
	#SAMPLE
	sample_iterator=0
	while [ $sample_iterator -lt $spacing ] && [ $timer -lt $duration ]; do

		./batman_monitor.sh >> $filename
		((sample_iterator += $sample))
		sleep $sample
	done

	#Increment
	((timer += $sample_iterator))
	((pow_current += $pow_increment))
	sudo iwconfig wlan0 txpower $pow_current
	./batman_monitor.sh
done

./reset_defaults.sh
let "timer = 0"

echo "[[[[RESET!]]]]"
echo "Climbing Down...."

while [ $timer -lt $duration ] && [ $pow_current -gt 0 ]; do

	pow_current=$(sudo batctl it)
        #SAMPLE
        sample_iterator=0
        while [ $sample_iterator -lt $spacing ] && [ $timer -lt $duration ]; do

                ./batman_monitor.sh >> $filename
                ((sample_iterator += $sample))
        	sleep $sample
	done

        #Increment
	((timer += $sample_iterator))
        ((pow_current += $pow_decriment))
        sudo iwconfig wlan0 $pow_current
	./batman_monitor.sh
done


