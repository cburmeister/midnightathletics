SSH?=ssh root@midnightathletics.com

.PHONY: deploy
deploy:
	rsync -a . root@midnightathletics.com:/root/midnightathletics --delete
	$(SSH) "pushd midnightathletics; . bin/deploy.sh"
