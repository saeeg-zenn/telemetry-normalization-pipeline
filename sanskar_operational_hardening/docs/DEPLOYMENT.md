# DEPLOYMENT GUIDE

## Requirements

- Python 3.11+
- Flask
- Requests
- Docker Desktop (optional)

---

## Install

pip install flask requests

---

## Run Services

python -m services.governance_service.app

python -m services.truth_service.app

python -m services.observability_service.app

python -m services.testing_service.app

python -m services.bhiv_gateway.app

---

## Execute Tests

python -m distributed_tests.run_all_tests

---

## Generate Proofs

python -m proofs.generate_proofs

---

## Docker

docker build -f docker/Dockerfile -t sanskar .

docker compose -f docker/docker-compose.yml up