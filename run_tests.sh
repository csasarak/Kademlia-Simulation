#!/bin/sh

if [ $# -lt 2 ]; then
    echo "Usage: ./run_tests.sh <node disable upper bound> <node disable increment>"
    exit
fi

node_increase_n=0
while [ $node_increase_n -lt $1 ]
do
        echo "./RunSimulation.py 42 10000 100 $node_increase_n ${node_increase_n}.dat"
	./RunSimulation.py 42 10000 100 $node_increase_n ${node_increase_n}_increase.dat
        node_increase_n=`expr $node_increase_n + $2`
done
