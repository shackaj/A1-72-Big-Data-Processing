#!/usr/bin/env python3
import sys

# initialize dict to hold stats per key
stats = {}

for line in sys.stdin:
    line = line.strip()  # handles \r\n from Trips.txt
    if not line:
        continue
    
    fields = line.split(",") # split line

    trip_id = fields[0]
    taxi_id = fields[1]
    fare = float(fields[2])
    distance = float(fields[3])
    
    # classify distance into short/medium/long
    if distance < 100:
        trip_type = 'short'
    elif distance < 200 and distance >= 100:
        trip_type = 'medium'
    elif distance >= 200:
        trip_type = 'long'
    
    # build composite key
    key = f"{taxi_id}_{trip_type}"
    
    # update stats[key] — if key not seen before, initialize (count=0, max=-inf, min=+inf, sum=0)
    # then: count += 1, max = max(...), min = min(...), sum += fare
    if key not in stats:
        stats[key] = [0, float('-inf'), float('inf'), 0]
        stats[key][0] += 1                                  # count
        stats[key][1] = max(stats[key][1], fare)             # max fare
        stats[key][2] = min(stats[key][2], fare)             # min fare
        stats[key][3] += fare                                # sum

# close: emit one line per key
for key, (count, max_fare, min_fare, total) in stats.items():
    print(f"{key}\t{count},{max_fare},{min_fare},{total}")

