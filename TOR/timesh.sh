#!/bin/bash

for i in {1..20}
do
	(time (python3 ./telescoping_circuit.py --mode random --url http://example.com > logs/"log_$i.log" 2>&1)) 2> logs/"time_$i.txt"
	echo "log_$i.log Done"
done
