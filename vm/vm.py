from vm.translate import comments, sentences, types
from vm.verifiquer import pcow
from utils import filesmanipule
from syntax.buildins import *
from syntax.classtypes import *
import utils
import ast, pickle
from builtins import exec as xc
def eb(file):
    with open(file, "rb") as f:
        tree = pickle.load(f)
    code = compile(tree, file, mode="exec")
    xc(code)

def cb(file):
    code=filesmanipule.rfile(file)
    code = translate(code)
    tree = ast.parse(code)
    with open(file.replace(".cni", ".cnb"), "wb") as f:
        pickle.dump(tree, f)
def translate(code):
    code = pcow.analize(code, pcow.pcow)
    code = comments.all(code)
    code = sentences.all(code)
    code = types.all(code)

    code = f"import sys, os\nsys.path.append(os.path.dirname(__file__))\n{code}"
    return code

def execute(file):
    code=filesmanipule.rfile(file)
    executeStr(code, file)

def executeStr(code:str, path:str|None=None):
    code = translate(code)
    code = compile(code, path or "code.cni", "exec")
    if path is None:
        xc(code, globals=globals(), locals=locals())
    else:
        xc(code, globals=globals()|{"__file__":path}, locals=locals())

def returned(file):
    code=filesmanipule.rfile(file)
    return returnedStr(code)

def returnedStr(code:str):
    code = translate(code)
    return code


