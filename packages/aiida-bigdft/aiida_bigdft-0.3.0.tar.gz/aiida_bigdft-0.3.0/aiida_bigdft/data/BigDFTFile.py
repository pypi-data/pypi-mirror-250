"""
Module for adding extra BigDFT functionality to AiiDA's base SinglefileData
"""

import os
from typing import Union

from BigDFT.Logfiles import Logfile
import yaml

from aiida.orm import SinglefileData


class BigDFTFile(SinglefileData):
    """
    Wrapper class for a BigDFT yaml format file as SinglefileData
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._content = self._open()

    def _open(self):
        """
        Attempts to open the stored file, returning an empty dict on failure
        """
        try:
            with self.open() as o:  # pylint: disable=not-context-manager
                content = yaml.safe_load(o)
                if content is None:
                    return {}
                return content
        except FileNotFoundError:
            self.logger.warning(f"file {self.filename} could not be opened!")
            return {}

    @property
    def content(self):
        """
        Attempts to return file content from cache, loading otherwise
        """
        try:
            return self._content
        except AttributeError:
            self._content = self._open()
            return self._content

    def dump_file(self, path=None):
        """
        Dump the stored file to `path`
        defaults to cwd + filename if not provided
        """
        path = path or os.path.join(os.getcwd(), self.filename)

        with self.open() as inp:  # pylint: disable=not-context-manager
            with open(path, "w+", encoding="utf8") as out:
                out.write(inp.read())


class BigDFTLogfile(BigDFTFile):
    """
    Specialised class for wrapping a BigDFT Logfile class as SinglefileData
    """

    @property
    def logfile(self) -> Union[Logfile, None]:
        """
        Create and return the BigDFT Logfile object
        """
        if not hasattr(self, "_logfile"):
            try:
                self._logfile = Logfile(dictionary=self.content)
            except Exception as e:
                self._logfile_generate_error = e
                self._logfile = None

        return self._logfile
