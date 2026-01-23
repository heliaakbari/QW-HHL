#!/bin/bash

for m in 2 4
do
    for p in {1..6}
    do
        for q in {2..3}
        do
            python3 Updated/MainSimDebugBench.py ${m} ${p} ${q}
        done
    done
done

