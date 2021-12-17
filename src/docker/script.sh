#!/usr/bin/bash

var=`date +%F`
sudo docker exec master pg_dumpall -U postgres > /home/danylo/projects/course_work_db/src/backup/$var.sql

