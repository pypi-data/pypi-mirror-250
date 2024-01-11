import io
import re

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT


EXTENSIONS = [".sub"]
PATTERN = r"\{.*?\}"


@staticmethod
def detectSUB(content: str | io.IOBase) -> bool:
    r"""
    Used to detect MicroDVD caption format.

    It returns True if:
     - the start of a first line in a file matches regex `^{\d+}{\d+}`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    line = content.readline()
    if re.match(r"^{\d+}{\d+}", line) or line.startswith(r"{DEFAULT}"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False

controlCodes = {
    "{y:i}": "<i>{}</i>",
    "{y:b}": "<b>{}</b>",
    "{y:u}": "<u>{}</u>",
    "{y:s}": "<s>{}</s>",
    
}

def formatLine(self, pattern):
    start = ""
    end = ""
    font_vars = []
    for control_code in pattern:
        control_code, value = control_code.strip("{} ").split(":",1)
        control_code = control_code.upper()
        if control_code == "Y":
            value = value.split(",")
            for i in value:
                if i == "i":
                    start += "<i>"
                    end += "</i>"
                elif i == "b":
                    start += "<i>"
                    end += "</i>"
                elif i == "u":
                    start += "<i>"
                    end += "</i>"
                elif i == "s":
                    start += "<i>"
                    end += "</i>"
        elif control_code == "F":
            font_vars.append("font-family:"+value)
        elif control_code == "S":
            font_vars.append("font-size:"+value)
        elif control_code == "C":
            font_vars.append("color:#"+value[-2:]+value[-4:-2]+value[-6:-4])
        elif control_code == "P":
            pass
        elif control_code == "H":
            pass
    if font_vars:
        start += "<p style='"+";".join(font_vars)+";'>" 
        end += "</p>" 
    return start, end
    

def readSUB(self, content: str | io.IOBase, languages: list[str] = [], **kwargs):
    content = self.checkContent(content=content, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or 0

    if not self.options.get("frame_rate"):
        self.options["frame_rate"] = kwargs.get("frame_rate") or 25
    frame_rate = kwargs.get("frame_rate") or self.options.get("frame_rate")

    if not self.options.get("blocks"):
        self.options["blocks"] = []
    
    line = content.readline().strip()
    while line:
        if line.startswith(r"{DEFAULT}"):
            self.options["blocks"].append(Block(BlockType.STYLE, style=line))
        else:
            lines = line.split("|")
            params = re.findall(PATTERN, lines[0])
            start = MT.fromSUBTime(params[0].strip("{} "), frame_rate)
            end = MT.fromSUBTime(params[1].strip("{} "), frame_rate)
            caption = Block(BlockType.CAPTION, start_time=start, end_time=end,
                            style=[p.strip("{}") for p in params[2:]])
            for counter, line in enumerate(lines):
                start, end = formatLine(self, re.findall(PATTERN, line))
                line = start+re.sub(PATTERN, "", line)+end
                if len(languages) > 1:
                    caption.append(line, languages[counter])
                else:
                    caption.append(line, languages[0])
            caption.shift_time(time_offset)
            self.append(caption)
        line = content.readline().strip()


def saveSUB(self, filename: str, languages: list[str] = None, **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SUB,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    languages = languages or [self.default_language]
    frame_rate = kwargs.get("frame_rate") or self.options.get("frame_rate") or 25
    
    with open(filename, "w", encoding=encoding) as file:
        index = 1
        for data in self:
            if data.block_type != BlockType.CAPTION:
                continue
            elif index != 1:
                file.write("\n")
            file.write("{"+data.start_time.toSUBTime(frame_rate)+"}{"+data.end_time.toSUBTime(frame_rate)+"}")
            file.write("|".join(data.get(i) for i in languages))
            index += 1
    


class MicroDVD(CaptionsFormat):
    """
    MicroDVD

    Read more about it https://en.wikipedia.org/wiki/MicroDVD

    Example:

    with MicroDVD("path/to/file.sub") as sub:
        sub.saveSRT("file")
    """
    detect = staticmethod(detectSUB)
    _read = readSUB
    _save = saveSUB

    from .sami import saveSAMI
    from .srt import saveSRT
    from .ttml import saveTTML
    from .vtt import saveVTT
