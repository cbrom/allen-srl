#!/usr/bin/env bash
sudo docker build --file Dockerfile . -t singularitynet:srl_allen
sudo docker run -d -v /home/zelalem/nlp-services-misc/allen-srl/etcd:/allen_srl/etcd -v /etc/letsencrypt:/etc/letsencrypt -it -p 8018:8018 -p 8008:8008 --name allen_srl singularitynet:allen_srl
