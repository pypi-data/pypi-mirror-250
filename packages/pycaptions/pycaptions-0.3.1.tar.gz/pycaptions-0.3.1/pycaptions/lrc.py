import io
import re

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT


EXTENSIONS = [".lrc"]


@staticmethod
def detectLRC(content: str | io.IOBase) -> bool:
    r"""
    Used to detect Synchronized Accessible Media Interchange caption format.

    It returns True if:
     - the first line starts with `[` and ends with `]` OR
     - ^\[(\d{1,3}):(\d{1,2}(?:[:.]\d{1,3})?)\]
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    line = content.readline().strip()
    if line.startswith("[") and line.endswith("]") or re.match(r"^\[(\d{1,3}):(\d{1,2}(?:[:.]\d{1,3})?)\]", line):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readLRC(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or 0
    raise ValueError("Not Implemented")


def saveLRC(self, filename: str, languages: list[str] = None, **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SAMI,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    languages = languages or [self.default_language]
    try:
        with open(filename, "w", encoding=encoding) as file:
            pass
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")
    raise ValueError("Not Implemented")


class LyRiCs(CaptionsFormat):
    """
    Synchronized Accessible Media Interchange

    Read more about it https://learn.microsoft.com/en-us/previous-versions/windows/desktop/dnacc/understanding-sami-1.0

    Example:

    with SAMI("path/to/file.sami") as sami:
        sami.saveSRT("file")
    """
    detect = staticmethod(detectLRC)
    read = readLRC
    save = saveLRC

    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
    from .usf import saveUSF
    from .vtt import saveVTT
