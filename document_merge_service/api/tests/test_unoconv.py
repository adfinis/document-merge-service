import os
import random
import shutil
import sys
from multiprocessing.pool import ThreadPool
from pathlib import Path
from subprocess import TimeoutExpired, run
from time import sleep

import pytest
from psutil import process_iter

from ..unoconv import Unoconv, run_fork_safe


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


def kill_dms_sleep(dms_test_bin):  # pragma: no cover
    found = False
    kill_zombies()
    for x in process_iter(["name"]):
        if dms_test_bin.name == x.name():
            found = True
            x.kill()
            x.wait()
    return found


def test_fork(dms_test_bin):  # pragma: no cover
    kill_dms_sleep(dms_test_bin)
    shell_cmd = f"{dms_test_bin} infinity & disown"
    run(["/bin/bash", "-c", shell_cmd])
    sleep(0.5)
    assert kill_dms_sleep(dms_test_bin)
    run_fork_safe(["/bin/bash", "-c", shell_cmd])
    sleep(0.5)
    assert not kill_dms_sleep(dms_test_bin)


def run_fork_load(test_file):
    unoconv = Unoconv("/usr/bin/python3", shutil.which("unoconv"))
    return unoconv.process(test_file, "pdf")


def try_fork_load(arg):
    n, test_file = arg
    if n < 10:
        # slowly start load test
        sleep(0.05 * (10 - n))
    try:
        result = run_fork_load(test_file)
        return result
    except Exception as e:  # pragma: no cover
        return e


def test_fork_load(capsys):
    count = 8
    base = Path(__file__).parent.parent.absolute()
    data = Path(base, "data")
    load = Path(data, "loadtest")
    test_files = []
    test_files += [Path(data, "docx-mailmerge.docx")] * count
    test_files += [Path(load, "1.doc")] * count
    test_files += [Path(load, "2.docx")] * count
    test_files += [Path(load, "3.docx")] * count
    test_files += [Path(load, "4.docx")] * count
    random.shuffle(test_files)
    try:
        pool = ThreadPool(8)
        with capsys.disabled():
            sys.stdout.write(" Loadtest: ")
            sys.stdout.flush()
        for result in pool.imap(try_fork_load, enumerate(test_files)):
            with capsys.disabled():
                sys.stdout.write(".")
                sys.stdout.flush()
            if isinstance(result, Exception):  # pragma: no cover
                raise result
            elif not result.stdout.startswith(b"%PDF"):  # pragma: no cover
                raise ValueError(result)
        with capsys.disabled():
            sys.stdout.write("done")
    finally:
        pool.close()
        pool.join()
