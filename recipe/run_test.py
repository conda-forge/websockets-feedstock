from subprocess import call
import sys

WIN = sys.platform == "nt"

COV_FAIL_UNDER = 93

K_SKIPS = [
    "test_client_connect_canceled_during_handshake",
    "test_close_idempotency_race_condition",
    "test_writing_in_recv_events_fails"
]

PYTEST = [
    "coverage",
    "run",
    "--source=websockets",
    "--branch",
    "-m",
    "pytest",
    "-vv",
    "--tb=long",
    "--color=yes",
    "-k",
    f"""not ({" or ".join(K_SKIPS)})""",
]

REPORT = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COV_FAIL_UNDER}",
]


def do(args: list[str]) -> int:
    if WIN:
        print("Skipping tests on windows due to hangs")
        return 0
    print(">>>", "\t".join(args), flush=True)
    return call(args, cwd="src")


if __name__ == "__main__":
    sys.exit(do(PYTEST) or do(REPORT))
