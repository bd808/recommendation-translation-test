#!/bin/bash

function run_command {
  echo "$1"
  psql test -c "$1"
}

run_command "drop table if exists predictions;"

columns=$(head -n1 $1 | cut -d',' -f2-)
column_names=$(echo $columns | sed 's/,/ decimal, /g')

run_command "create table predictions (id varchar, $column_names decimal);"

bunzip2 -k -c $(realpath $1) | psql test -c "\copy predictions from STDIN header delimiter ',' csv;"

