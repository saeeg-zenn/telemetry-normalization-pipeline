#!/bin/sh

echo "Checking Governance Service..."
curl http://localhost:5001/health

echo "Checking Truth Service..."
curl http://localhost:5002/health

echo "Checking Observability..."
curl http://localhost:5003/health

echo "Checking Testing..."
curl http://localhost:5004/health

echo "Checking Gateway..."
curl http://localhost:5005/health