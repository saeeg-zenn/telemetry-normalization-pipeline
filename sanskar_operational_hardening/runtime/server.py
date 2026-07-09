"""
Runtime demo.
"""

from runtime.config import SYSTEM_NAME
from runtime.trace_manager import TraceManager
from runtime.replay_engine import ReplayEngine
from runtime.dependency_manager import status

print("=" * 50)

print(SYSTEM_NAME)

print("=" * 50)

trace = TraceManager()

tid = trace.new_trace()

print("Trace ID:", tid)

engine = ReplayEngine()

print(engine.compare("HELLO", "HELLO"))

print()

print(status())