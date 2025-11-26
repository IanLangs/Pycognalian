import re, sys

class regex:
    sub = staticmethod(re.sub)
    match = staticmethod(re.match)
    split = staticmethod(re.split)
    flags = {"D": re.DOTALL, "M": re.MULTILINE, "V": re.VERBOSE, "I": re.IGNORECASE, "U": re.UNICODE}
    def __init__(self, *a, **kw):
        raise SyntaxError("regex mlang is not callable")
    @classmethod
    def get_flags(cls, chars: str):
        total = 0
        for ch in chars:
            total |= cls.flags.get(ch.upper(), 0)
        return total
    class regexCompile:
        def __init__(self, pattern, flags=0):
            self.__compilepat = re.compile(pattern, flags=flags)
        def __getattr__(self, item):
            return getattr(self.__compilepat, item)
    class regexCompileTo:
        def __init__(self, p, t):
            self.pattern = p
            self.to = t
            self.frozen = True
        def __setattr__(self,key,value):
            if not getattr(self, "frozen", False):
                return object.__setattr__(self,key,value)
            raise RuntimeError("attrs are inmutable")
        def sub(self, text, count=0, flags=0):
            return regex.sub(self.pattern, self.to, text, count=count, flags=flags)
        def match(self, text, flags=0):
            return regex.match(self.pattern, text, flags=flags)

        def split(self, text, maxsplit=0, flags=0):
            return regex.split(self.pattern, text, maxsplit, flags=flags)

    def __class_getitem__(cls, item: tuple | str):
        if isinstance(item, str):
            return cls.regexCompile(item)
        if len(item) == 2:
            return cls.regexCompileTo(item[0], item[1])
        elif len(item) == 1:
            return cls.regexCompile(item[0])
        else:
            raise RuntimeError("invalid length for items")

