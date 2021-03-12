from subprocess import TimeoutExpired, run
from time import sleep

import pytest
from psutil import process_iter

from .unoconv import run_fork_safe


def test_timeout():
    with pytest.raises(TimeoutExpired):
        run_fork_safe(["sleep", "infinity"], timeout=0.5)


def kill_dms_sleep(bin):
    found = False
    for x in process_iter(["name"]):
        if bin == x.name():
            found = True
            x.kill()
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
