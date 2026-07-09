from distributed_tests.test_service_failure import run as service_failure
from distributed_tests.test_replay_divergence import run as replay_divergence
from distributed_tests.test_delayed_ack import run as delayed_ack
from distributed_tests.test_node_desync import run as node_desync
from distributed_tests.test_conflicting_telemetry import run as telemetry
from distributed_tests.test_observability_failure import run as observability

print("=" * 60)
print("SANSKAR DISTRIBUTED FAILURE MATRIX")
print("=" * 60)

service_failure()
replay_divergence()
delayed_ack()
node_desync()
telemetry()
observability()

print()
print("=" * 60)
print("ALL DISTRIBUTED TESTS PASSED")
print("PROOF FILES GENERATED")
print("=" * 60)