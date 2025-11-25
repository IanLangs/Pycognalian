import re
def use(code):
    code = re.sub(r"from: (.*) use: (.*)", lambda m: f"from {m.group(1)} import {m.group(2)})", code)
    code = re.sub(r"use: (.*)", lambda m: f"import {m.group(1)}", code)
    return code
def fn(code):
    return re.sub(r"fn", lambda m: f"def", code)
def loop(code):
    return re.sub(r"loop:", "while True:", code)
def cientific(code):
    return re.sub(r"([-\+]?\d+(?:_\d+)*(?:\.\d+)?)e([-\+]?\d+(?:_\d+)*(?:\.\d+)?)", lambda m: f"scientific({m.group(1)}, {m.group(2)})", code)
def anonimus(code):
    def repl_lam(m):
        params = m.group(1)
        code = m.group(2)
        return f"Lambda({code}, {params})"
    return re.sub(r"<(\{[^<>]*\}) *-> *([^<>]*)", repl_lam, code)
def all(code):
    code = use(code)
    code = fn(code)
    code = loop(code)
    code = cientific(code)
    code = anonimus(code)
    return code