#!/bin/bash
# SERIAL chain (one heavy process at a time, 45 s cooldown between jobs); every job via lowprio.py
cd "$(dirname "$0")"
PY=C:/Users/serge/miniconda3/envs/ape311/python3.exe
LP="../../scripts/lowprio.py"
$PY $LP pyr2.py 2 6 > results/pyr2_p2_lab6.txt 2>&1
sleep 45
$PY $LP pyr2.py 3 6 > results/pyr2_p3_lab6.txt 2>&1
echo done > results/serial_pyr.done
