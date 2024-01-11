import io

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT


EXTENSIONS = [".srt"]


@staticmethod
def detectSRT(content: str | io.IOBase) -> bool:
    """
    Used to detect SubRip caption format.

    It returns True if:
     - the first line is a number 1
     - the second line contains a `-->`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if content.readline().rstrip() == "1" and '-->' in content.readline():
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def convertFromSRTLayout(self, id, layout, width, height):
    layout = layout.split(" ")
    if len(layout) != 4:
        print(f"Error converting layout: Excpected 4 arguments got {len(layout)}")
        return
    for i, v in enumerate(["X1","X2","Y1","Y2"]):
        if layout[i][2:] != v:
            print(f"Error converting layout: Invalid field at position {i} expected {v} got {layout[0][2:]}")
            return
    try:
        x1 = int(layout[0][3:])
        x2 = int(layout[1][3:])
        y1 = int(layout[2][3:])
        y2 = int(layout[3][3:])
        self.addLayout(id,
            Block(BlockType.LAYOUT, id=id, layout={
            "width": (x2-x1) / width,
            "height": (y2-y1) / height,
            "viewportanchor": [x1 / width, y1 / height],
            "regionanchor": [0, 0],
        }))
    except Exception as e:
        print(f"Error converting layout: {e}")
        return
    
def getSRTLayout(self, id, width, height):
    layout = self.getLayout(id)
    if not layout:
        return ""
    x1 = layout.options["layout"]["viewportanchor"][0] * width
    x2 = layout.options["layout"]["width"] * width + x1
    y1 = layout.options["layout"]["viewportanchor"][1] * height
    y2 = layout.options["layout"]["height"] * height + y1
    return f" X1:{x1} X2:{x2} Y1:{y1} Y2:{y2}"

def readSRT(self, content: str | io.IOBase, languages: list[str], **kwargs):
    """
    kwargs: 
     - time_offset (MicroTime, optional): Used for shifting time on read (default is 0)
     - media_width (int, optional): Used for extended SRT coordinates conversion
     - media_height (int, optional): Used for extended SRT coordinates conversion
    """
    content = self.checkContent(content=content, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or MT()
    width = kwargs.get("media_width") or self.media_width
    height = kwargs.get("media_height") or self.media_height

    counter = 1
    id = content.readline()
    while id:
        start, end = content.readline().split(" --> ")
        end = end.strip().split(" ", 1)
        
        caption = Block(BlockType.CAPTION, languages[0], MT.fromSRTTime(start),
                        MT.fromSRTTime(end[0]), content.readline().strip())
        if len(end) == 2:
            convertFromSRTLayout(self, id.strip(), end[1], width, height)
        line = content.readline().strip()
        while line:
            if len(languages) > 1:
                caption.append(line, languages[counter])
                counter += 1
            else:
                caption.append(line, languages[0])
            line = content.readline().strip()
        caption.shift_time(time_offset)
        self.append(caption)
        id = content.readline()


def saveSRT(self, filename: str, languages: list[str] = None, **kwargs):
    """
    kwargs: 
     - file_encoding (str, optional): Used for opening files (default is UTF-8)
     - srt_extended (bool, optional): Used to make extended version of SRT (default is False)
     - media_width (int, optional): Used for extended SRT coordinates conversion
     - media_height (int, optional): Used for extended SRT coordinates conversion
    """
    filename = self.makeFilename(filename=filename, extension=self.extensions.SRT,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    width = kwargs.get("media_width") or self.media_width
    height = kwargs.get("media_height") or self.media_height
    isExtended = kwargs.get("srt_extended") or False
    extended = ""
    languages = languages or [self.default_language]
    try:
        with open(filename, "w", encoding=encoding) as file:
            index = 1
            for data in self:
                if data.block_type != BlockType.CAPTION:
                    continue
                elif index != 1:
                    file.write("\n\n")
                if isExtended:
                    extended = getSRTLayout(self, index, width, height)
                file.write(f"{index}\n")
                file.write(f"{data.start_time.toSRTTime()} --> {data.end_time.toSRTTime()}{extended}\n")
                file.write("\n".join(data.get(i) for i in languages))
                index += 1
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")


class SubRip(CaptionsFormat):
    """
    SubRip

    Read more about it https://en.wikipedia.org/wiki/SubRip

    Example:

    with SubRip("path/to/file.srt") as srt:
        srt.saveVTT("file")
    """
    detect = staticmethod(detectSRT)
    read = readSRT
    save = saveSRT

    from .sami import saveSAMI
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT
