#!/bin/bash
echo "This script is about to start model training for " $1 "minutes"
sh ./create-spot-instance.sh MUDR24-302-base MUDR24-302-Model-4 $1
echo "This script has just finished model training"
