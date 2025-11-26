from syntax.classtypes import Number

from vm import vm
readInput = input
write = print
def scientific(n:Number, te:Number):
    return Number(float(n) * (10 ** float(te)))
def exec(code, filename=None):
    vm.executeStr(code, filename)
file = open