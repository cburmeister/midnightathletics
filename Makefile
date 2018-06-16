.PHONY: deploy
deploy:
	rsync -a . root@midnightathletics.com:/root/midnightathletics --delete
	ssh root@midnightathletics.com "pushd midnightathletics; . bin/deploy.sh $(container)"
