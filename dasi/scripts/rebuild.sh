#!/bin/bash
sudo sh -c "truncate -s 0 /var/lib/docker/containers/*/*-json.log"
sudo sh -c "truncate -s 0 /mnt/data/docker/containers/*/*-json.log"

git pull origin
docker-compose -f ~/Gamja-Backend/dasi/docker-compose.yml stop

#IS_BLUE_RUNNING=$(docker ps | grep api_blue)
#NGINX_CONFIG_FILE="./nginx/nginx.conf"

##### BLUE RUNNING...
#if [ -n "$IS_BLUE_RUNNING"  ];then
#  CONTAINER_A="api_green" # to deploy
#  CONTAINER_B="api_blue"  # to stop
#else
#  CONTAINER_A="api_blue"
#  CONTAINER_B="api_green"
#fi

# Start container A
echo "Deploy $CONTAINER_A..."
docker-compose -f ~/Gamja-Backend/dasi/docker-compose.yml build
docker-compose -f ~/Gamja-Backend/dasi/docker-compose.yml up -d

# toggle nginx config file
#sed -i "s/$CONTAINER_B/$CONTAINER_A/g" $NGINX_CONFIG_FILE

# preserver logs
#log_path="./log/$(TZ="Asia/Seoul" date '+%Y-%m-%d-%H-%M')-$CONTAINER_B.out"
#docker logs $CONTAINER_B > $log_path

# stop container B

# clear unusing docker
docker image prune -af
docker system prune -af
docker volume prune -af
