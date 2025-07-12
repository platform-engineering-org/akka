.PHONY: build up down clean

build:
	docker build -t ghcr.io/platform-engineering-org/akka-manager:latest -f manager/Dockerfile .

up: build
	kind create cluster
	kind load docker-image ghcr.io/platform-engineering-org/akka-manager:latest
	kubectl apply -f manager/deploy/manager.yaml
	sleep 20
	kubectl port-forward service/manager 5000:5000 &

down:
	kind delete cluster

clean:
	docker system prune --all --force
