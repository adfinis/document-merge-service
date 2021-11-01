import os
from subprocess import TimeoutExpired, run
from time import sleep

import pytest
from psutil import process_iter

from ..unoconv import run_fork_safe


def test_timeout():
    with pytest.raises(TimeoutExpired):
        run_fork_safe(["sleep", "infinity"], timeout=0.5)


def kill_zombies():  # pragma: no cover
    # Depending on if we are pid 1, we want to cleanup zombie processes
    # As our pid depends on how the tests are run, we add "no cover" to this function
    if os.getpid() != 1:
        return
    for x in process_iter(["name"]):
        if x.status() == "zombie":
            x.wait()


def kill_dms_sleep(bin):
    found = False
    kill_zombies()
    for x in process_iter(["name"]):
        if bin == x.name():
            found = True
            x.kill()
            x.wait()
    return found


def test_fork():
    bin = "dms_test_sleep"
    kill_dms_sleep(bin)
    shell_cmd = f"{bin} infinity & disown"
    run(["/bin/bash", "-c", shell_cmd])
    sleep(0.2)
    assert kill_dms_sleep(bin)
    run_fork_safe(["/bin/bash", "-c", shell_cmd])
    assert not kill_dms_sleep(bin)
