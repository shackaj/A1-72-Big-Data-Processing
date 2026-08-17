#!/usr/bin/env python3
import sys

current_key = None
current_value = None

# format function to help clean output
def format_output(key, count, max_fare, min_fare, total):
    taxi_id, trip_type = key.split('_', 1) # split key into necessary format
    # get avg fare and handle 0
    if count:
        avg_fare = total / count
    else:
        avg_fare = 0
        
    print(f"{taxi_id}\t{trip_type}\t{count}\t{max_fare:.2f}\t{min_fare:.2f}\t{avg_fare:.2f}")

for line in sys.stdin:
    
    line = line.strip()
    if not line:
        continue
    
    key, stats = line.split("\t")
    count, max_fare, min_fare, total = stats.split(',')
    
    count = int(count)
    max_fare = float(max_fare)
    min_fare = float(min_fare)
    total = float(total)
    
    # merge partial into running
    if key == current_key:
        current_count += count
        current_max = max(current_max, max_fare)
        current_min = min(current_min, min_fare)
        current_total += total
    
    else:
        # key change = output the final stats for key
        if current_key is not None:
            format_output(current_key, current_count, current_max, current_min, current_total)
        
        # start running again/or intially
        current_key = key
        current_count = count
        current_max = max_fare
        current_min = min_fare
        current_total = total

# output last key
if current_key is not None:
    format_output(current_key, current_count, current_max, current_min, current_total)
