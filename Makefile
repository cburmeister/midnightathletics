SSH?=ssh root@midnightathletics.com

.PHONY: deploy
deploy:
	rsync -a . root@midnightathletics.com:/root/midnightathletics --delete
	$(SSH) "pushd midnightathletics; . bin/deploy.sh"

.PHONY: data
data:
	$(SSH) "aws s3 sync s3://mixes-b2d2c7df84340c274011ecdffcca275d /mnt/volume-sfo2-01/mixes"
