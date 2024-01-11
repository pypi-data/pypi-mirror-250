"""
Minimised logger class to handle debugging once the daemon takes control

"""
import os.path
from datetime import datetime


class MiniLogger:
    """
    Miniature logger class

    :param path: path to intended file
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, path: str):

        dpath = os.path.split(path)[0]
        if not os.path.isdir(dpath):
            os.makedirs(dpath)

        self._path = path

        self.debug("minilogger class init", wipe=True)

    def debug(self, msg: str, wipe: bool = False):
        """
        Append debug string `msg` to file (unless wipe=True, then create a fresh file)

        :param msg: string to write
        :param wipe: clears the file before writing if True
        """
        mode = "w+" if wipe else "a"
        timestr = datetime.now().strftime("%H:%M:%S")
        with open(self._path, mode, encoding="utf8") as o:
            o.write(f"[{timestr}] {msg}\n")
