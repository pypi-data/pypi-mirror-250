import io

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT


EXTENSIONS = [".usf"]


@staticmethod
def detectUSF(content: str | io.IOBase) -> bool:
    """
    Used to detect Universal Subtitle Format caption format.

    It returns True if:
     - the first line starts with <USFSubtitles
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if content.readline().lstrip().startswith("<USFSubtitles"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readUSF(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or 0
    raise ValueError("Not Implemented")


def saveUSF(self, filename: str, languages: list[str] = None, **kwargs):
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


class USF(CaptionsFormat):
    """
    Universal Subtitle Format

    Read more about it https://en.wikipedia.org/wiki/Universal_Subtitle_Format

    Example:

    with USF("path/to/file.usf") as usf:
        usf.saveSRT("file")
    """
    detect = staticmethod(detectUSF)
    read = readUSF
    save = saveUSF

    from .lrc import saveLRC
    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT   
