import re
import subprocess
from collections import namedtuple
from mimetypes import guess_type

UnoconvResult = namedtuple(
    "UnoconvResult", ["stdout", "stderr", "returncode", "content_type"]
)


class Unoconv:
    def __init__(self, pythonpath, unoconvpath, server=None, port=2002):
        """
        Convert documents with unoconv command-line utility.

        :param filename: str() - path to the python interpreter
        :param convert: str() - path to the unoconv binary
        :param connection: str() - connection string to an unoconv listener
        """
        self.pythonpath = pythonpath
        self.unoconvpath = unoconvpath
        self.server = server
        self.port = port

    @property
    def cmd(self):
        cmd = [self.pythonpath, self.unoconvpath]

        if self.server:
            cmd.extend(
                [
                    "--server",
                    self.server,
                    "--port",
                    self.port,
                    "--no-launch",  # Crash if no listener is found.
                ]
            )

        return cmd

    def get_formats(self):
        p = subprocess.run(
            self.cmd + ["--show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
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
        p = subprocess.run(
            self.cmd + ["--format", convert, "--stdout", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
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
