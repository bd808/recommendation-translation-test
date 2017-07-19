#!/bin/bash

function run_command {
  echo "$1"
  mysql --defaults-file=./replica.my.cnf -h tools.labsdb s53132__trex_p -e "$1"
  #psql test -c "$1"
}


columns=$(head -n1 $1 | cut -d',' -f2-)

N=8
for c in $(echo $columns | sed 's/,/ /g')
do
  ((i=i%N)); ((i++==0)) && wait && echo $c
  # mysql
  run_command "create index idx_$c on predictions ($c);" &
  # postgres
  # run_command "create index on predictions ($c);" &
done
