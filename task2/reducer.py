import sys
import math

current_key = None
points = []  # all (x, y) drop-off points assigned to this medoid this round

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def process_cluster(medoid_id, pts):
    n = len(pts)
    if n == 0:
        return

    # PAM Step 3 (Update): try every assigned point as a candidate medoid,
    # compute its average dissimilarity to all other points in the cluster,
    # keep whichever candidate minimises this average
    best_candidate = None
    best_avg_cost = float('inf')
    for candidate in pts:
        total_dist = sum(euclidean(candidate, other) for other in pts)
        avg_cost = total_dist / n
        if avg_cost < best_avg_cost:
            best_avg_cost = avg_cost
            best_candidate = candidate

    print(f"{best_candidate[0]}\t{best_candidate[1]}\t{n}\t{best_avg_cost:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    key, value = line.split('\t')
    x_str, y_str = value.split(',')
    x, y = float(x_str), float(y_str)

    if key == current_key:
        points.append((x, y))
    else:
        if current_key is not None:
            process_cluster(current_key, points)
        current_key = key
        points = [(x, y)]

if current_key is not None:
    process_cluster(current_key, points)