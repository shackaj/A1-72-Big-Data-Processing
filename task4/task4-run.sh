#!/bin/bash

chmod +x mapper.py reducer.py
chmod +x task4-run.sh
hadoop fs -rm -r -f /Output/task4

hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=3 \
    -files mapper.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input /Input/Trips.txt \
    -output /Output/task4
