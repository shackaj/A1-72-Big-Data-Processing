import sys
import math

#loaded medoids from intialisation txt, ensuring to skip iteration limit as v
with open("initialization.txt") as f:
    mds = [tuple(map(float, line.split())) for line in f.read().splitlines()[1:] if line.strip()]

#processing trip.txt 
for l in sys.stdin:
    field = l.strip().split(",") #skipping header just incase it is present.
    if len(field) >= 8 and not field[0].startswith("Trip ID"):
        x,y = float(field[6]), float(field[7])

#calcluating eucledian distance 
        idx_c = min(range(len(mds)), key=lambda z: math.sqrt((x-mds[z][0])**2 + (y-mds[z][1])**2))
        #print key value
        print(f"{idx_c}\t{x},{y}")
