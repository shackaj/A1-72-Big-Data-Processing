#!/bin/bash

chmod +x mapper.py reducer.py

# read v and initial medoids
V=$(head -n 1 initialization.txt)
tail -n +2 initialization.txt > medoids.txt

i=1
# setup loop i <= V
while [ $i -le $V ]
do
    OUTDIR="/Output/task2_iter_$i"   # unique per-iteration temp dir per requirements
    hadoop fs -rm -r -f "$OUTDIR"

    # run mapreduce job
    hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=3 \
    -files medoids.txt,mapper.py,reducer.py \
    -mapper "/usr/bin/python3 mapper.py" \
    -reducer "/usr/bin/python3 reducer.py" \
    -input /Input/Trips.txt \
    -output "$OUTDIR"

    # pull full 4-column results (medoid_x, medoid_y, #points, avg_dissimilarity)
    hadoop fs -getmerge "$OUTDIR"/part-* full_output.txt
    echo "Iteration $i:"

    # print required iteration info directly to terminal
    cat full_output.txt

    # extract just x,y columns to become next iteration's medoids
    cut -f1,2 full_output.txt > task2.txt

    # convergence check
     sort medoids.txt > /tmp/m_sorted.txt
     sort task2.txt > /tmp/t_sorted.txt
     if diff -q /tmp/m_sorted.txt /tmp/t_sorted.txt > /dev/null
     then
        seeiftrue=1
    else
        seeiftrue=0
    fi

    # stop early if convergence == true
    if [ $seeiftrue = 1 ]
    then
        mv task2.txt medoids.txt
        echo "Converged after $i iterations."
        # promote this iteration's output as the final graded result
        hadoop fs -rm -r -f /Output/task2
        hadoop fs -mkdir -p /Output/task2
        hadoop fs -cp "$OUTDIR"/part-* /Output/task2/
        break
    # save new medoids and loop again if convergence != true
    else
        mv task2.txt medoids.txt
    fi
    i=$((i+1))

done

# if loop ended by hitting v without converging, then last OUTDIR is the final result
if [ $seeiftrue != 1 ]; then
    hadoop fs -rm -r -f /Output/task2
    hadoop fs -mkdir -p /Output/task2
    hadoop fs -cp "/Output/task2_iter_$V"/part-* /Output/task2/
fi

# clean up all intermediate iteration directories
hadoop fs -rm -r -f /Output/task2_iter_*