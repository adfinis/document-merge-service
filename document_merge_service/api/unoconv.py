import os
import re
import signal
from collections import namedtuple
from mimetypes import guess_type
from subprocess import PIPE, CalledProcessError, CompletedProcess, Popen, TimeoutExpired

UnoconvResult = namedtuple(
    "UnoconvResult", ["stdout", "stderr", "returncode", "content_type"]
)

# in testing 2 seconds is enough
_min_timeout = 2

# terminate_then_kill() takes 1 second in the worst case, so we have to use two seconds,
# or the timeout won't be triggered before harakiri.
_ahead_of_harakiri = 2


def get_default_timeout():
    timeout = 55
    try:  # pragma: no cover
        import uwsgi

        harakiri = uwsgi.opt.get("harakiri")
        if harakiri:
            try:
                timeout = max(int(harakiri) - _ahead_of_harakiri, _min_timeout)
            except ValueError:
                pass
    except ModuleNotFoundError:
        pass
    return timeout


_default_timeout = get_default_timeout()


def getpgid(proc):
    try:
        return (proc, os.getpgid(proc.pid))
    except ProcessLookupError:  # pragma: no cover
        return (proc, None)


def kill(proc, sig):
    process, group = proc
    try:
        if group is None:
            if process.returncode is None:  # pragma: no cover
                os.kill(process.pid, sig)
        else:
            os.killpg(group, sig)
    except ProcessLookupError:
        pass


def terminate_then_kill(proc):
    process, _ = proc
    kill(proc, signal.SIGTERM)
    try:
        process.wait(timeout=1)
    except TimeoutExpired:  # pragma: no cover
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
    if input is not None:  # pragma: no cover
        if kwargs.get("stdin") is not None:
            raise ValueError("stdin and input arguments may not both be used.")
        kwargs["stdin"] = PIPE

    if capture_output:  # pragma: no cover
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
        if check and retcode:  # pragma: no cover
            raise CalledProcessError(
                retcode, process.args, output=stdout, stderr=stderr
            )
    return CompletedProcess(process.args, retcode, stdout, stderr)


def run(cmd):
    return run_fork_safe(
        [str(arg) for arg in cmd],
        stdout=PIPE,
        stderr=PIPE,
        timeout=_default_timeout,
    )


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
