#!/bin/bash
# SERIAL chain, one heavy process at a time, 45 s cooldown, all through lowprio.py
cd "$(dirname "$0")"
PY=C:/Users/serge/miniconda3/envs/ape311/python3.exe
LP="../../scripts/lowprio.py"
$PY $LP pyr2.py 2 6 > results/pyr2_p2_lab6.txt 2>&1
sleep 45
$PY $LP pyr2.py 3 12 > results/pyr2_p3_lab12.txt 2>&1
sleep 45
$PY $LP controls1.py > results/controls1_rerun.txt 2>&1
sleep 45
$PY $LP controls2.py > results/controls2_out.txt 2>&1
sleep 45
$PY $LP pyr2.py 2 12 > results/pyr2_p2_lab12.txt 2>&1
echo done > results/serial2.done
