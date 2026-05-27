#!/bin/bash

hosts=(
  "appserver1.osay21.me"
  "appserver2.osay21.me"
  "database.osay21.me"
  "loadbalancer.osay21.me"
)

for host in "${hosts[@]}"; do
  echo "Removing $host from known_hosts..."
  ssh-keygen -R "$host"
done

echo "Done."
