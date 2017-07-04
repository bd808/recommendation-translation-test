#!/bin/bash

function run_command {
  echo "$1"
  psql test -c "$1"
}

columns=$(head -n1 $1 | cut -d',' -f2-)

# Run indexing operations in parallel
N=8
for c in $(echo $columns | sed 's/,/ /g')
do
  ((i=i%N)); ((i++==0)) && wait && echo $c
  run_command "create index on predictions ($c);" &
done

