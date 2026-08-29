#!/bin/bash

# read v and initial medoids
V=$(head -n 1 initialization.txt)
tail -n +2 initialization.txt > medoids.txt

i=1
# setup loop i <= V
while [ $i -le $V ]
do
    echo "Iteration $i:"

    # clear previous output
    hadoop fs -rm -r -f /Output/task2

    # run mapreduce job
    hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=3 \
    -files medoids.txt,mapper.py,reducer.py \
    -mapper ./mapper.py \
    -reducer ./reducer.py \
    -input /Input/Trips.txt \
    -output /Output/task2

    # pull full 4-column results (medoid_x, medoid_y, #points, avg_dissimilarity)
    hadoop fs -getmerge /Output/task2/part-* full_output.txt

    # print required iteration info directly to terminal
    cat full_output.txt

    # extract just x,y columns to become next iteration's medoids
    cut -f1,2 full_output.txt > task2.txt

    echo "Old medoids:"
    cat medoids.txt
    echo "New medoids:"
    cat task2.txt

    # convergence check
    if diff -q medoids.txt task2.txt > /dev/null
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
        break
    # save new medoids and loop again if convergence != true
    else
        mv task2.txt medoids.txt
    fi
    i=$((i+1))

done