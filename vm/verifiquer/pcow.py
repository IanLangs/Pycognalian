import re

from syntax.classtypes import String
from utils.decorators import allways
pcow = (r"def",
        r"print",
        r"input",
        r"lambda",
        r"import",
        r";",
        r"float",
        r" int")

def analize(code:str|String, prohibited:list[str]|tuple[str]=()):
    for p in prohibited:
        if p in code:
            raise SyntaxError(f"prohibited {"char" if len(p) == 1 else "word"} {p} in code")
    return code

