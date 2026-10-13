#!/bin/bash
# Serial queue: ONE heavy job at a time, 45 s cool-down between jobs, each job wall-bounded (<=~9 min).
cd "E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/experiments/20261003-lum-chua-continuation"
PY="C:/Users/serge/miniconda3/envs/ape311/python3.exe"
LP="E:/Проверка Гипотез/работаю над проверкой гипотез/Y-17 100 gipotez/scripts/lowprio.py"
run() { echo "=== $(date +%H:%M:%S) $*" >> queue.log; "$PY" "$LP" search3.py "$@" >> queue.log 2>&1; sleep 45; }
run phase1 0.03 400 2 300
run phase1 0.3 400 3 300
run rand 1500 4 400
run es 0.05 100 11 540
run es 0.02 100 12 540
run es 0.2 100 13 540
echo "=== QUEUE DONE $(date +%H:%M:%S)" >> queue.log
