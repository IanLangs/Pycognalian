import cmath
import re
import warnings
from collections import deque
from typing import Any
import subprocess as sub
from functools import partial 
from abc import ABC
import math
# ==========================================================
# Registro central de tipos Cognalian
# ==========================================================

_COG_TYPES = []

def register_type(cls):
    _COG_TYPES.append(cls)
    return cls


def wrap_value(res):
    """Envuelve resultados Python en tipos Cognalian"""
    for t in _COG_TYPES:
        if isinstance(res, t):
            return res
        try:
            if t.__mro__[1] is not object and isinstance(res, t.__mro__[1]):
                return t(res)
        except Exception:
            pass
    return res


# ==========================================================
# Dunder factory (corregido)
# ==========================================================

def _make_dunder(name, cls):
    base = cls.__mro__[1]
    fn = getattr(base, name, None)
    if fn is None:
        return None

    def method(self, *args, **kwargs):
        res = fn(self, *args, **kwargs)
        if res is NotImplemented:
            return NotImplemented
        return wrap_value(res)

    method.__name__ = name
    return method


# ==========================================================
# Enum
# ==========================================================

class Enum:
    def __init__(self, **kwargs):
        object.__setattr__(self, "_data", kwargs)

    def __getitem__(self, name):
        return self._data[name]

    def __getattr__(self, name):
        raise AttributeError("Enum has no attributes")

    def __setattr__(self, *_):
        raise AttributeError("Enum is immutable")

    def __repr__(self):
        return f"<Enum {self._data}>"


# ==========================================================
# List
# ==========================================================

@register_type
class List(deque):
    def slice(self, p1=None, p2=None, p3=None):
        return List(list(self)[slice(p1, p2, p3)])

    def __repr__(self):
        return repr(list(self))


for name in dir(deque):
    if name.startswith("__") and name.endswith("__") and not hasattr(List, name):
        fn = _make_dunder(name, List)
        if fn:
            setattr(List, name, fn)


# ==========================================================
# Bool
# ==========================================================

@register_type
class Bool(int):
    def __bool__(self):
        if int(self) == 0:
            return False
        return True

    def __str__(self):
        return "true" if self else "false"

    __repr__ = __str__


for name in dir(bool):
    if name.startswith("__") and name.endswith("__") and not hasattr(Bool, name):
        fn = _make_dunder(name, Bool)
        if fn:
            setattr(Bool, name, fn)


# ==========================================================
# String
# ==========================================================

@register_type
class String(str):
    def split(self, sep=None, maxsplit=0, flags=0):
        if sep is None:
            return List(map(String, re.split(r"\s+", self, maxsplit)))
        return List(map(String, re.split(sep, self, maxsplit, flags)))


for name in dir(str):
    if name.startswith("__") and name.endswith("__") and not hasattr(String, name):
        fn = _make_dunder(name, String)
        if fn:
            setattr(String, name, fn)


# ==========================================================
# Number
# ==========================================================

@register_type
class Number(float):
    def __truediv__(self, other):
        try:
            return wrap_value(float.__truediv__(self, other))
        except ZeroDivisionError:
            if self == 0:
                return Number.nan()
            return Number.inf(1 if self > 0 else -1)

    def __rtruediv__(self, other):
        try:
            return wrap_value(float.__truediv__(other, self))
        except ZeroDivisionError:
            return Number.nan()

    def is_nan(self):
        return math.isnan(self)

    def is_inf(self):
        return math.isinf(self)

    @classmethod
    def nan(cls):
        return cls(float('nan'))

    @classmethod
    def inf(cls, sign=1):
        return cls(float('inf') if sign >= 0 else float('-inf'))

for name in dir(float):
    if name.startswith("__") and name.endswith("__") and not hasattr(Number, name):
        fn = _make_dunder(name, Number)
        if fn:
            setattr(Number, name, fn)


# ==========================================================
# Complex Number (CNum)
# ==========================================================

@register_type
class CNum:
    def __init__(self, real=0, imag=0):
        if Number.is_nan(Number(real)) or Number.is_nan(Number(imag)):
            real = float("nan")
            imag = float("nan")
        self.real = Number(real)
        self.imag = Number(imag)

        if self.real.is_nan() or self.imag.is_nan():
            self._p = complex(float("nan"), float("nan"))
        else:
            self._p = complex(self.real, self.imag)

    @classmethod
    def convert(cls, x):
        if isinstance(x, CNum):
            return x
        if isinstance(x, Number):
            return cls(x, 0)
        raise TypeError("cannot convert to CNum")

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"

    def __add__(self, other):
        o = CNum.convert(other)
        return CNum(self.real + o.real, self.imag + o.imag)

    def __sub__(self, other):
        o = CNum.convert(other)
        return CNum(self.real - o.real, self.imag - o.imag)

    def __mul__(self, other):
        o = CNum.convert(other)
        r = self.real * o.real - self.imag * o.imag
        i = self.real * o.imag + self.imag * o.real
        return CNum(r, i)

    def __truediv__(self, other):
        o = CNum.convert(other)
        try:
            res = self._p / o._p
        except ZeroDivisionError:
            return CNum(float("nan"), float("nan"))
        return CNum(res.real, res.imag)


# ==========================================================
# Tuple / Dict
# ==========================================================

@register_type
class Tuple(tuple):
    pass

@register_type
class Dict(dict):
    def getEnum(self):
        return Enum(**self)


for name in dir(tuple):
    if name.startswith("__") and name.endswith("__") and not hasattr(Tuple, name):
        fn = _make_dunder(name, Tuple)
        if fn:
            setattr(Tuple, name, fn)

for name in dir(dict):
    if name.startswith("__") and name.endswith("__") and not hasattr(Dict, name):
        fn = _make_dunder(name, Dict)
        if fn:
            setattr(Dict, name, fn)


# ==========================================================
# Regex facade
# ==========================================================

import microlangs.regex as _regex

class regex(_regex.regex):
    class regexCompile(_regex.regex.regexCompile): ...
    class regexCompileTo(_regex.regex.regexCompileTo): ...


# ==========================================================
# Lambda
# ==========================================================

class Lambda:
    def __init__(self, code: String, params):
        self.__code__ = code
        if isinstance(params, dict):
            self.params = params
        else:
            self.params = {p: None for p in params}

    def __getattribute__(self, name):
        return f"{name} = {self.params[name]}"

    def __repr__(self):
        return f"<{self.params} -> {self.__code__}>"

    def __call__(self, **kwargs):
        if not set(kwargs) <= set(self.params):
            warnings.warn("invalid arguments", UserWarning)
            return None
        try:
            res = eval(self.__code__, globals(), self.params | kwargs)
            return wrap_value(res)
        except Exception as e:
            warnings.warn(str(e), UserWarning)
            return None


# ==========================================================
# Struct
# ==========================================================

class Struct(Enum):
    def __repr__(self):
        return f"<struct -> {self._data}>"

# ==========================================================
# Time units
# ==========================================================

class Time:
    __slots__ = ("timevalue",)

    _factor = 1.0  # Factor base en segundos
    
    def __init__(self, timevalue: float):
        self.timevalue = timevalue

    def to_seconds(self) -> float:
        """Convierte el valor de tiempo a segundos."""
        return self.timevalue * self._factor

    @classmethod
    def from_seconds(cls, seconds: float):
        """Crea una nueva instancia a partir de un valor en segundos."""
        return cls(seconds / cls._factor)

    def convert(self, target_cls):
        """Convierte esta instancia a la clase target_cls (una subclase de Time)."""
        if not issubclass(target_cls, Time):
            raise TypeError("Target must be a Time type")
        return target_cls.from_seconds(self.to_seconds())

    def __add__(self, other):
        """Suma dos instancias de la misma clase."""
        if type(self) is not type(other):
            raise TypeError(f"Cannot add {type(self).__name__} with {type(other).__name__}")
        return type(self)(self.timevalue + other.timevalue)

    def __repr__(self):
        return f"{type(self).__name__}({self.timevalue})"

class Seconds(Time):
    _factor = 1.0 

class Milliseconds(Time):
    _factor = 0.001 

class Minutes(Time):
    _factor = 60.0  

class Hours(Time):
    _factor = 3600.0 

# ==========================================================
# Comands
# ==========================================================

class Command:
    def __init__(
            self,
            command_list
        ):
        self.c = command_list
        self.run = partial(sub.run, self.c)
    
    def __class_getitem__(cls, items):
        cls(list(items))