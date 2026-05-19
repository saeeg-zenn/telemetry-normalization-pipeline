import subprocess
import sys
import json
from datetime import datetime, timezone

def canonical_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

STEPS = [
    ("Canonical Serializer",        "validation/canonical_serializer.py"),
    ("Deterministic Hash Proof",    "validation/deterministic_hash_proof.py"),
    ("Append-Only Store",           "persistence/append_only_store.py"),
    ("Frozen Snapshot Store",       "persistence/frozen_snapshot_store.py"),
    ("Lineage Hash Lock", "persistence/lineage_hash_lock.py"),
    ("Hostile Replay Test",         "replay/hostile_replay_test.py"),
    ("Interruption Recovery Test",  "tests/interruption_recovery_test.py"),
    ("Continuity Verifier", "validation/continuity_verifier.py"),
    ("Cross-Module Replay Validator","federation/cross_module_replay_validator.py"),
]

def print_header():
    print("=" * 60)
    print("   CANONICAL REPLAY INFRA — FULL PIPELINE EXECUTION")
    print("=" * 60)
    print(f"   Started At : {canonical_timestamp()}")
    print("=" * 60)

def print_footer(results: list, start_time: str, end_time: str):
    print("\n" + "=" * 60)
    print("   PIPELINE EXECUTION SUMMARY")
    print("=" * 60)
    all_passed = True
    for name, status, reason in results:
        tag = "PASSED" if status else "FAILED"
        print(f"   {name:<35} : {tag}")
        if not status:
            print(f"     Reason : {reason}")
            all_passed = False

    print()
    print(f"   Started At   : {start_time}")
    print(f"   Completed At : {end_time}")
    print()

    if all_passed:
        print("   OVERALL RESULT : PIPELINE COMPLETED SUCCESSFULLY")
    else:
        print("   OVERALL RESULT : PIPELINE FAILED — SEE ABOVE")

    print("=" * 60)
    return all_passed

def run_step(name: str, path: str) -> tuple:
    print(f"\n>>> [{name}]")
    print(f"    Running : {path}")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, path],
        capture_output=False
    )

    if result.returncode == 0:
        print(f"-" * 60)
        print(f"    STATUS : PASSED")
        return (name, True, None)
    else:
        print(f"-" * 60)
        print(f"    STATUS : FAILED — exit code {result.returncode}")
        return (name, False, f"Exit code {result.returncode}")

def generate_execution_proof(results: list, all_passed: bool):
    proof = {
        "execution_proof": {
            "generated_at": canonical_timestamp(),
            "repository": "canonical_replay_infra",
            "total_steps": len(results),
            "passed": sum(1 for _, s, _ in results if s),
            "failed": sum(1 for _, s, _ in results if not s),
            "steps": [
                {
                    "name": name,
                    "status": "PASSED" if status else "FAILED",
                    "reason": reason
                }
                for name, status, reason in results
            ],
            "overall_status": "PIPELINE COMPLETED SUCCESSFULLY" if all_passed
                              else "PIPELINE FAILED"
        }
    }

    with open("outputs/execution_proof.json", "w") as f:
        json.dump(proof, f, indent=2)

    print(f"\n   Execution proof written → outputs/execution_proof.json")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    start_time = canonical_timestamp()
    print_header()

    results = []
    failed_early = False

    for name, path in STEPS:
        name, status, reason = run_step(name, path)
        results.append((name, status, reason))

        if not status:
            print(f"\n   PIPELINE HALTED at step : {name}")
            print(f"   Reason                  : {reason}")
            print(f"   Fix the above step and re-run pipeline.\n")
            failed_early = True
            break

    end_time = canonical_timestamp()
    all_passed = print_footer(results, start_time, end_time)
    generate_execution_proof(results, all_passed)

    if not all_passed:
        sys.exit(1)