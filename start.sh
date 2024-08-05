#!/bin/bash
echo "This script is about to start MUDR24-302-Model-" $1 " training for " $2 "minutes"
sh ./create-spot-instance.sh MUDR24-302-base "MUDR24-302-Model-{$1}" $2
echo "This script has just finished model training"
