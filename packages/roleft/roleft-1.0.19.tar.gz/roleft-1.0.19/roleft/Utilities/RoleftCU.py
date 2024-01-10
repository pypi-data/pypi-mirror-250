import math
import pathlib
import random
import time

from roleft.Entities.RoleftDateTime import xDateTime

_strSrc = "2345678abcdefghjkmnprstuvwxyzABCDEFGHJKMNPRSTUVWXYZ"
_step = 1024
_kvps = {
    "B": math.pow(_step, 1),
    "KB": math.pow(_step, 2),
    "MB": math.pow(_step, 3),
    "GB": math.pow(_step, 4),
    "TB": math.pow(_step, 5),
}

class CU:
    @classmethod
    def GenRandom(cls, min=0,  max=10) -> int:
        return random.randrange(min, max)

    @classmethod
    def GetRandomStr(cls, length=16) -> str:
        return ''.join(random.sample(_strSrc, length))

    @classmethod
    def HasValue(cls, items: list) -> bool:
        return len(items) > 0

    @classmethod
    def CheckIfBetween(cls, src: int, min: int, max: int) -> bool:
        return src > min and src < max

    @classmethod
    def ReadAllText(cls, path: str) -> str:
        fo = open(path, "r")
        content = fo.read()
        fo.close()
        return content

    @classmethod
    def Save2File(cls, content: str, path: str) -> None:
        file = open(path, 'w')
        file.write(content)
        file.close()
        
    @classmethod
    def SureDir(cls, dirPath: str) -> None:
        path = pathlib.Path(dirPath)
        if not path.exists():
            path.mkdir(511, True)
    
    @classmethod
    def RandomBool(cls) -> bool:
        return bool(CU.GenRandom(0, 2))

    @classmethod
    def RandomDateTime(cls) -> xDateTime:
        ticks = CU.GenRandom(0, 17280000000)
        tm = time.localtime(ticks)
        return xDateTime(tm)

    @classmethod
    def GenSizeDesc(cls, length: int) -> str:
        showNum = float(length)

        currKey = ''
        for key, value in _kvps.items():
            currKey = key
            if showNum < _step:
                break

            showNum = length / value

        return f"{round(showNum, 2)}{currKey}"

