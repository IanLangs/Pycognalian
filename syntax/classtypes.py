import cmath
import re
import warnings
from typing import Any


class Enum:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__.get(name)
        raise KeyError("can't get item if item not exist")
    def __getattr__(self, name):
        raise AttributeError("can't get attributes")
    def __setattr__(self, name, value):
        raise AttributeError("can't set attributes")
    def __delattr__(self, name):
        raise AttributeError("can't delete attributes")
    def __setitem__(self, key, value):
        raise AttributeError("can't set items")
    def __iter__(self):
        return iter(self.__dict__.items())
    def __str__(self):
        return f"<Enum {self.__class__.__name__ } -> {self.__dict__}>"
    def __repr__(self):
        return f"<Enum {self.__class__.__name__ } -> {object.__str__(self)}>"
from collections import deque
class List(deque):
    def slice(self, p1=None, p2=None, p3=None):
        return List(list(self)[slice(p1,p2,p3)])
    def __str__(self):
        return str(list(self))
    def __repr__(self):
        return repr(list(self))
class Bool(int):
    def __bool__(self):
        if int(self) == 0:
            import random
            if ru:=random.uniform(0.0,1.0) < 0.5:
                return False
            elif ru > 0.5:
                return True
            else:
                return None
        return int(self) > 0
    def __str__(self):
        return str(bool(self)).lowercase() if bool(self) != None else "null"
    __repr__ = __str__
class String(str):
    def split(self, sep=None, maxsplit=0, flags=0):
        if sep is None:
            return re.split(r"\s+", str(self), maxsplit, flags)
        return re.split(sep, str(self), maxsplit, flags)

class Number(float):
    # ======== utilidades internas ========
    _to_float = staticmethod(lambda number: float(number))
    @staticmethod
    def _wrap(value):
        if isinstance(value, Number):
            return value
        return Number(value)
    
    def int(self):
        return Number(int(float(self)))

    def dec(self):
        return Number(self - int(self))

    # ======== operaciones aritméticas ========
    def __add__(self, other):
        return Number(float(self) + float(other))

    def __radd__(self, other):
        return Number(float(other) + float(self))

    def __sub__(self, other):
        return Number(float(self) - float(other))

    def __rsub__(self, other):
        return Number(float(other) - float(self))

    def __mul__(self, other):
        return Number(float(self) * float(other))

    def __rmul__(self, other):
        return Number(float(other) * float(self))

    def __truediv__(self, other):
        return Number(float(self) / float(other))

    def __rtruediv__(self, other):
        return Number(float(other) / float(self))

    def __floordiv__(self, other):
        return Number(float(self) // float(other))

    def __rfloordiv__(self, other):
        return Number(float(other) // float(self))

    def __mod__(self, other):
        return Number(float(self) % float(other))

    def __rmod__(self, other):
        return Number(float(other) % float(self))

    def __pow__(self, other):
        return Number(float(self) ** float(other))

    def __rpow__(self, other):
        return Number(float(other) ** float(self))
    # ======== unarios ========
    def __neg__(self):
        return Number(-float(self))

    def __pos__(self):
        return Number(+float(self))

    def __abs__(self):
        return Number(abs(float(self)))

    # ======== redondeos ========
    def __round__(self, ndigits=None):
        if ndigits is None:
            return Number(round(float(self)))
        return Number(round(float(self), ndigits))

    def __floor__(self):
        import math
        return Number(math.floor(float(self)))

    def __ceil__(self):
        import math
        return Number(math.ceil(float(self)))

    def __trunc__(self):
        import math
        return Number(math.trunc(float(self)))

    # ======== comparaciones (devuelven bool, deben quedar así) ========
    def __lt__(self, other):
        return float(self) < float(other)

    def __le__(self, other):
        return float(self) <= float(other)

    def __gt__(self, other):
        return float(self) > float(other)

    def __ge__(self, other):
        return float(self) >= float(other)

    def __eq__(self, other):
        return float(self) == float(other)

    def __ne__(self, other):
        return float(self) != float(other)

    # ======== shifts numéricos personalizados ========
    def __rshift__(self, other):
        return Number(float(self) // (2 ** float(other)))

    def __lshift__(self, other):
        return Number(float(other) * (2 ** float(self)))

    def __rrshift__(self, other):
        return Number(float(other) // (2 ** float(self)))

    def __rlshift__(self, other):
        return Number(float(other) * (2 ** float(self)))
    #asigancion
    def __iadd__(self, other):
        return Number(float(self) + float(other))

    def __isub__(self, other):
        return Number(float(self) - float(other))

    def __imul__(self, other):
        return Number(float(self) * float(other))

    def __itruediv__(self, other):
        return Number(float(self) / float(other))

    def __ifloordiv__(self, other):
        return Number(float(self) // float(other))

    def __imod__(self, other):
        return Number(float(self) % float(other))

    def __ipow__(self, other):
        return Number(float(self) ** float(other))

    # shifts personalizados
    def __ilshift__(self, other):
        return Number(float(self) * (2 ** float(other)))

    def __irshift__(self, other):
        return Number(float(self) // (2 ** float(other)))

class CNum:
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag
        self.pvalue = real + imag * 1j
    @classmethod
    def convert(cls, *args):
        if len(args) == 1:
            if isinstance(args[0], Number):
                return cls(args[0], 0)
            elif isinstance(args[0], CNum):
                return cls(args[0].real, args[0].imag)
        elif len(args) == 2:
            if not (isinstance(args[0], Number) and isinstance(args[1], Number)):
                raise TypeError("can't create a cnumber of it real or imag part is a complex or imaginary")
            return cls(args[0], args[1])

    def __str__(self):
        return f"{self.real} {"+" if self.imag >= 0 else "-"} {abs(self.imag)}i"
    def __add__(self, other):
        other = self.convert(other)
        return CNum(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        other = self.convert(other)
        return CNum(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        other = self.convert(other)
        r = self.real * other.real - self.imag * other.imag
        i = self.real * other.imag + self.imag * other.real
        return CNum(r, i)

    def __truediv__(self, other):
        other = self.convert(other)
        denom = other.real ** 2 + other.imag ** 2
        if denom == 0:
            raise ZeroDivisionError("can't divide by zero")
        r = (self.real * other.real + self.imag * other.imag) / denom
        i = (self.imag * other.real - self.real * other.imag) / denom
        return CNum(r, i)

    def __floordiv__(self, other):
        q = self / other
        return CNum(int(q.real), int(q.imag))

    def __pow__(self, other):
        other = self.convert(other)
        res = cmath.pow(self.pvalue, other.pvalue)
        return CNum(res.real, res.imag)

    # ---------------------- Operadores unarios ----------------------

    def __neg__(self):
        return CNum(-self.real, -self.imag)

    def __pos__(self):
        return self

    def __abs__(self):
        return (self.real ** 2 + self.imag ** 2) ** 0.5

    def __round__(self, ndigits=None):
        return CNum(round(self.real, ndigits), round(self.imag, ndigits))

    # ---------------------- Operaciones reversas ----------------------

    def __radd__(self, other):
        return self.convert(other) + self

    def __rsub__(self, other):
        return self.convert(other) - self

    def __rmul__(self, other):
        return self.convert(other) * self

    def __rtruediv__(self, other):
        return self.convert(other) / self

    def __rfloordiv__(self, other):
        return self.convert(other) // self

    def __rpow__(self, other):
        other = self.convert(other)
        res = cmath.pow(other.pvalue, self.pvalue)
        return CNum(res.real, res.imag)
    # ---------------------- Comparadores ----------------------

    def __eq__(self, other):
        try:
            other = self.convert(other)
            return self.real == other.real and self.imag == other.imag
        except TypeError:
            return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        other = self.convert(other)
        return abs(self) < abs(other)

    def __le__(self, other):
        other = self.convert(other)
        return abs(self) <= abs(other)

    def __gt__(self, other):
        other = self.convert(other)
        return abs(self) > abs(other)

    def __ge__(self, other):
        other = self.convert(other)
        return abs(self) >= abs(other)

    def __class_getitem__(cls, item:tuple[CNum, str]):
        geter = getattr(item[0], item[1], None)
        if geter is None:
            warnings.warn("can't get cnum item", UserWarning)
        return geter


class Tuple(tuple):pass
class Dict(dict):
    def getEnum(self) -> Enum:
        return Enum(**dict(self))
class Set(set):pass

import microlangs.regex as _regex
class regex(_regex.regex):
    class regexCompile(_regex.regex.regexCompile):pass
    class regexCompileTo(_regex.regex.regexCompileTo):pass

class Lambda:
    def __init__(self, code:String, params:Dict[str, Any]):
        self.__code__ = code
        self.params = params
        self.__dict__.update(self.params)
    def __str__(self):
        return f"{self.__code__}, {self.params}"
    def __call__(self, **kwargs):
        if set(kwargs.keys()) <= set(self.params.keys()):
            try:
                return eval(self.__code__, globals(), self.params | kwargs)
            except Exception as e:
                warnings.warn(f"Error executing Lambda: {e}", UserWarning)
                return None
        else:
            warnings.warn("The function did not execute because the arguments did not match", UserWarning)

class Struct(Enum):
    def __str__(self):
        sstr = Enum.__str__(self)
        rstr = sstr.replace(f"Enum {self.__class__.__name__ }", f"struct{(" " + self.__class__.__name__)  if self.__class__.__name__ != "Struct" else ""}")
        return rstr
