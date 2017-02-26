#!/bin/bash


# Default values
DEFAULT_BAT_IT=1000
DEFAULT_POWER=25

sudo batctl it $DEFAULT_BAT_IT
sudo iwconfig wlan0 txpower $DEFAULT_POWER

