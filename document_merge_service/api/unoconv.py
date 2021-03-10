import os
import re
import signal
from collections import namedtuple
from datetime import timedelta
from mimetypes import guess_type
from subprocess import PIPE, CalledProcessError, CompletedProcess, Popen, TimeoutExpired

UnoconvResult = namedtuple(
    "UnoconvResult", ["stdout", "stderr", "returncode", "content_type"]
)


def getpgid(proc):
    try:
        return (proc, os.getpgid(proc.pid))
    except ProcessLookupError:
        return (proc, None)


def kill(proc, sig):
    process, group = proc
    try:
        if group is None:
            if process.returncode is None:
                os.kill(process.pid, sig)
        else:
            os.killpg(group, sig)
    except ProcessLookupError:
        pass


def terminate_then_kill(proc):
    process, _ = proc
    kill(proc, signal.SIGTERM)
    try:
        process.wait(timeout=timedelta(seconds=1))
    except TimeoutExpired:
        pass
    finally:
        kill(proc, signal.SIGKILL)


def run_fork_safe(
    *popenargs,
    input=None,
    capture_output=False,
    timeout=None,
    check=False,
    **kwargs,
):
    """Run command with arguments and return a CompletedProcess instance.

    Works like `subprocess.run`, but puts the subprocess and its children in a new
    process group, so orphan forks can be terminated, too.
    """
    if input is not None:
        if kwargs.get("stdin") is not None:
            raise ValueError("stdin and input arguments may not both be used.")
        kwargs["stdin"] = PIPE

    if capture_output:
        if kwargs.get("stdout") is not None or kwargs.get("stderr") is not None:
            raise ValueError(
                "stdout and stderr arguments may not be used " "with capture_output."
            )
        kwargs["stdout"] = PIPE
        kwargs["stderr"] = PIPE

    with Popen(*popenargs, start_new_session=True, **kwargs) as process:
        proc = getpgid(process)
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        finally:
            terminate_then_kill(proc)
        retcode = process.poll()
        if check and retcode:
            raise CalledProcessError(
                retcode, process.args, output=stdout, stderr=stderr
            )
    return CompletedProcess(process.args, retcode, stdout, stderr)


def run(cmd):
    return run_fork_safe([str(arg) for arg in cmd], stdout=PIPE, stderr=PIPE)


class Unoconv:
    def __init__(self, pythonpath, unoconvpath):
        """
        Convert documents with unoconv command-line utility.

        :param pythonpath: str() - path to the python interpreter
        :param unoconvpath: str() - path to the unoconv binary
        """
        self.cmd = [pythonpath, unoconvpath]

    def get_formats(self):
        p = run(self.cmd + ["--show"])
        if not p.returncode == 0:  # pragma: no cover
            raise Exception("Failed to fetch the formats from unoconv!")

        formats = []
        for line in p.stderr.decode("utf-8").split("\n"):
            if line.startswith("  "):
                match = re.match(r"^\s\s(?P<format>[a-z]*)\s", line)
                if match:
                    formats.append(match.group("format"))

        return set(formats)

    def process(self, filename, convert):
        """
        Convert a file.

        :param filename: str()
        :param convert: str() - target format. e.g. "pdf"
        :return: UnoconvResult()
        """
        # unoconv MUST be running with the same python version as libreoffice
        p = run(self.cmd + ["--format", convert, "--stdout", filename])
        stdout = p.stdout
        if not p.returncode == 0:  # pragma: no cover
            stdout = f"unoconv returncode: {p.returncode}"

        content_type, _ = guess_type(f"something.{convert}")

        result = UnoconvResult(
            stdout=stdout,
            stderr=p.stderr,
            returncode=p.returncode,
            content_type=content_type,
        )

        return result
