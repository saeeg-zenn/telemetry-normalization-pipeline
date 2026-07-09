# API REFERENCE

## Governance Service

GET /

Returns service status.

GET /health

Returns health information.

GET /validate/<trace_id>

Validates a trace.

---

## Truth Service

GET /

Service status.

GET /health

Health endpoint.

GET /replay

Replay status.

---

## Observability Service

GET /

Service status.

GET /health

Health endpoint.

GET /trace

Trace inspection.

---

## Testing Service

GET /

Service status.

GET /health

Health endpoint.

GET /run

Execute distributed tests.

---

## BHIV Gateway

GET /

Gateway status.

GET /health

Gateway health.

GET /dependencies

Dependency status.