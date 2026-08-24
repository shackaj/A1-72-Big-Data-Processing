#!/usr/bin/env python3
import sys

# taxi_id for count, sum_distance, sum_sqr_distance
stats = {}

# read lines from trips.txt
for line in sys.stdin:
    line = line.strip() # strip white space & \n
    if not line:
        continue
    
    fields = line.split(",")
    taxi_id = fields[1]
    distance = float(fields[3])

    # group by taxi
    key = taxi_id

    # for first time taxi is seen
    if key not in stats:
        stats[key] = [0, 0.0, 0.0]
    
    # accumlate for each taxi
    stats[key][0] += 1 # running total num trips by the taxi
    stats[key][1] += distance # running total distance by the taxi
    stats[key][2] += distance ** 2 # running total distance of taxi (squared) for standard deviation formula
    
# output for reducer
for key, (count, total_distance, total_distance_sqrd) in stats.items():
    print(f"{key}\t{count},{total_distance},{total_distance_sqrd}")

# Format: taxi_id   count,total_distance,total_distance_sqrd