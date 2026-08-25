#!/usr/bin/env python3
import sys
import math

#intiate variables
current_t= None
count= 0
sum_v= 0.0
sum_sqrt= 0.0

for l in sys.stdin:
    line = l.strip()
    if not line:
        continue

    key, values = line.split('\t') #split input from mapper formart: {v}\t{x},{y},{z}.

    count_str, distance_str, distance_sqrt_str = values.split(',') #split values variables, then change value types.
    c = int(count_str)
    x_values = float(distance_str)
    x_sqrt = float(distance_sqrt_str)

    if current_t == key:
        count+= c
        sum_v+= x_values
        sum_sqrt+= x_sqrt
    else:
        if current_t is not None: #compute standard deviation 3 part expanded formula.
            mean = sum_v/count #1st calculate mean to then calculate variance.
            variance = max(0.0,(sum_sqrt/count)-(mean**2)) #2nd calculate variance to then calculate mean.
            stndrd_dev = math.sqrt(variance) #compute standard deviation from variance. 
            print(f"{current_t}\t{mean:.2f}\t{stndrd_dev:.2f}") #format output.

        #reset.
        current_t = key
        count = c
        sum_v = x_values
        sum_sqrt = x_sqrt
#loop over last value
if current_t is not None:
    mean= sum_v /count
    variance= max(0.0,(sum_sqrt/count)-(mean**2))
    stndrd_dev= math.sqrt(variance)
    print(f"{current_t}\t{mean:.2f}\t{stndrd_dev:.2f}")
