FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask requests

EXPOSE 5001 5002 5003 5004 5005

CMD ["python", "-m", "services.governance_service.app"]