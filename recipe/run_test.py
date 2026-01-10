from subprocess import call
import sys
import os

WIN = os.name == "nt"

NOGIL = "free-threading" in sys.version

COV_FAIL_UNDER = 93

K_SKIPS = [
    "client_connect_canceled_during_handshake",
    "close_idempotency_race_condition",
    "writing_in_recv_events_fails",
]

if NOGIL:
    # added in https://github.com/conda-forge/websockets-feedstock/pull/54
    COV_FAIL_UNDER = 73
    K_SKIPS += [
        "legacy",
        "test_keepalive_terminates_when_sending_ping_fails",
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
    print({"NOGIL": f"{NOGIL} {sys.version}", "WIN": f"{WIN} {os.name}"})
    print(">>>", "\n\t".join(args), flush=True)
    return call(args, cwd="src")


if __name__ == "__main__":
    sys.exit(do(PYTEST) or do(REPORT))
