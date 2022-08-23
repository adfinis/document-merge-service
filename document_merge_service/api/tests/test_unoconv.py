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

from .. import unoconv
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
    conv = Unoconv("/usr/bin/python3", shutil.which("unoconv"))
    return conv.process(test_file, "pdf")


def test_unoconv_unshare_error(loadtest_data, caplog):
    test_file = Path(loadtest_data, "1.docx")
    conv = Unoconv("/usr/bin/python3", shutil.which("unoconv"))
    try:
        save = unoconv._unshare
        unoconv._unshare = "false"
        conv.process(test_file, "pdf")
        assert "CAP_SYS_ADMIN" in caplog.text
    finally:
        unoconv._unshare = save


def test_unoconv_error(caplog):
    test_file = "/asdfasdfa"
    conv = Unoconv("/usr/bin/python3", shutil.which("unoconv"))
    conv.process(test_file, "pdf")
    assert "unoconv failed with returncode" in caplog.text


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


def test_fork_load(capsys, loadtest_data):
    count = 8
    test_files = []
    test_files += [Path(loadtest_data.parent, "docx-mailmerge.docx")] * count
    test_files += [Path(loadtest_data, "1.doc")] * count
    test_files += [Path(loadtest_data, "2.docx")] * count
    test_files += [Path(loadtest_data, "3.docx")] * count
    test_files += [Path(loadtest_data, "4.docx")] * count
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
