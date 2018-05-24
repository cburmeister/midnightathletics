#!/bin/bash

bucket=s3://mixes-b2d2c7df84340c274011ecdffcca275d
mixes_path=/mnt/volume-sfo2-01/mixes

aws s3 sync $bucket $mixes_path
aws s3 sync $mixes_path $bucket
