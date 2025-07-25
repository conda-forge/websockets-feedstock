from subprocess import call
import sys
import platform

WIN = platform.system() == "Windows"
OSX = platform.system() == "Darwin"

COV_FAIL_UNDER = 93

K_SKIPS = [
    "test_client_connect_canceled_during_handshake",
    "test_close_idempotency_race_condition",
    # https://github.com/conda-forge/websockets-feedstock/pull/52
    "test_close_timeout_waiting_for_recv",
    "test_close_waits_for_close_frame",
    "test_close_waits_for_recv",
    "test_explicit_host_port",
    "test_server_shuts_down_and_waits_until_handlers_terminate",
    "test_writing_in_recv_events_fails",
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
    if WIN or OSX:
        print("Skipping tests on windows/osx due to hangs")
        return 0
    print(">>>", "\t".join(args), flush=True)
    return call(args, cwd="src")


if __name__ == "__main__":
    sys.exit(do(PYTEST) or do(REPORT))
