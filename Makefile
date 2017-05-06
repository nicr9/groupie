IMAGE=nicr9/groupie:latest

test:
	python3 groupie.py

push:
	docker build -f Dockerfile -t ${IMAGE} .
	docker push ${IMAGE}

deploy:
	@helm install --set apiKey=${TICKETMASTER_API_KEY} --name groupie ./groupie

status:
	helm status groupie

upgrade:
	@helm upgrade --set apiKey=${TICKETMASTER_API_KEY} groupie ./groupie

teardown:
	helm delete groupie
