IMAGE=nicr9/groupie:latest

test:
	python3 groupie.py

push:
	docker build -f Dockerfile -t ${IMAGE} .
	docker push ${IMAGE}

deploy:
	kubectl apply -f manifest.yml

helm-deploy:
	helm install groupie --set apiKey=${TICKETMASTER_API_KEY}
