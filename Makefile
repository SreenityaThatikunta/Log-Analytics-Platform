build-images:
	./scripts/build.sh

compose-up:
	docker compose -f infrastructure/docker-compose.yml up --build

compose-down:
	docker compose -f infrastructure/docker-compose.yml down

k8s-deploy:
	./scripts/deploy.sh

k8s-dry-run:
	kubectl apply --dry-run=client -k infrastructure/kubernetes

test-log:
	LOG_COLLECTOR_ADDRESS=$${LOG_COLLECTOR_ADDRESS:-localhost:50051} python3 sdk/python-client/example.py

test-log-batch:
	LOG_COLLECTOR_ADDRESS=$${LOG_COLLECTOR_ADDRESS:-localhost:50051} LOG_TEST_SCENARIO=batch python3 sdk/python-client/example.py

test-log-list:
	LOG_TEST_SCENARIO=list python3 sdk/python-client/example.py
