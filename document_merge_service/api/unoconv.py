import re
import subprocess
from collections import namedtuple
from mimetypes import guess_type

UnoconvResult = namedtuple(
    "UnoconvResult", ["stdout", "stderr", "returncode", "content_type"]
)


def run_subprocess(cmd):
    return subprocess.run(
        [str(arg) for arg in cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE
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
        p = run_subprocess(self.cmd + ["--show"])
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
        p = run_subprocess(self.cmd + ["--format", convert, "--stdout", filename])
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
