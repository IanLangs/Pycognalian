from syntax.classtypes import Number
import time as t
from vm import vm
from copy import copy
readInput = input
write = print
def scientific(n:Number, te:Number):
    return Number(float(n) * (2 ** float(te)))
def exec(code, filename=None):
    vm.executeStr(code, filename)
file = copy(open)

time = t
time.now = t.time
del time.time

NAN = Number(float("nan"))