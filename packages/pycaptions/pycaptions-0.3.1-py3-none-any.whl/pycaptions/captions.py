import io
from .captionsFormat import CaptionsFormat


class Captions(CaptionsFormat):
    """
    Captions

    A generic class to read different types of caption formats.

    Example:

    with Captions("path/to/file.srt") as captions:
        captions.saveSRT("file")
    """
    def __init__(self, filename: str = None, default_language: str = "und", **options):
        super().__init__(filename, default_language, **options)

    from .lrc import detectLRC, saveLRC, readLRC
    from .sami import detectSAMI, saveSAMI, readSAMI
    from .srt import detectSRT, saveSRT, readSRT
    from .sub import detectSUB, saveSUB, readSUB
    from .ttml import detectTTML, saveTTML, readTTML
    from .usf import detectUSF, saveUSF, readUSF
    from .vtt import detectVTT, saveVTT, readVTT

    readers = {
        "lrc": readLRC,
        "sami": readSAMI,
        "srt": readSRT,
        "sub": readSUB,
        "ttml": readTTML,
        "usf": readUSF,
        "vtt": readVTT
    }

    savers = {
        "lrc": saveLRC,
        "sami": saveSAMI,
        "srt": saveSRT,
        "sub": saveSUB,
        "ttml": saveTTML,
        "usf": saveUSF,
        "vtt": saveVTT
    }

    def get_format(self, file: str | io.IOBase) -> str | None:
        if self.detectSRT(file):
            self.fileFormat = "srt"
        elif self.detectVTT(file):
            self.fileFormat = "vtt"
        elif self.detectTTML(file):
            self.fileFormat = "ttml"
        elif self.detectSUB(file):
            self.fileFormat = "sub"
        elif self.detectSAMI(file):
            self.fileFormat = "sami"
        elif self.detectUSF(file):
            self.fileFormat = "usf"
        elif self.detectLRC(file):
            self.fileFormat = "lrc"
        
        return self.fileFormat

    def detect(self, content: str | io.IOBase) -> bool:
        if not self.get_format(content):
            return False
        return True

    def read(self, content: str | io.IOBase, languages: list[str] = None, **kwargs):
        format = self.get_format(content)
        if not format:
            return
        self.readers[format](self, content, languages, **kwargs)

    def save(self, filename: str, languages: list[str] = None, output_format: str = None, **kwargs):
        output_format = output_format.lstrip(".") or self.fileFormat
        if output_format not in self.savers:
            raise ValueError("Incorect output format")
        self.savers[output_format](self, filename=filename, languages=languages, **kwargs)
