import re

def primitive(code):
    # Strings entre comillas dobles (no greedy, captura vacíos)
    code = re.sub(r'r"([^"]*)"', lambda m: f"r'{m.group(1)}'", code)
    code = re.sub(r'"([^"]*)"', lambda m: f'String("{m.group(1)}")', code)
    #null
    code = re.sub(r"null", "None", code)
    # Booleanos: true/false/maybe
    code = re.sub(r"\b(true|false|maybe)\b", lambda m: f"Bool({1 if m.group(1) == 'true' else (0 if m.group(1) == "maybe" else -1)})", code)
    # Números (enteros o flotantes, opcional underscore)
    code = re.sub(r"\b[-\+]*?\d+(?:_\d+)*(?:\.\d+)?\b", lambda m: f"Number({m.group(0)})", code)
    # Complex
    code = re.sub(r"complex\((.*?)\)", lambda m: f"CNum({m.group(1)})", code)
    return code


# Función recursiva para procesar colecciones anidadas
def parse_collections(code):
    def repl_struct(m):
        name = m.group(1)
        fields = [f.strip() for f in m.group(2).split(",") if f.strip()]

        params = ", ".join(fields)
        assigns = ", ".join(f"{f}={f}" for f in fields)
        return f"def {name}({params}):return Struct({assigns})"
    # Diccionarios: {key: value, ...}
    def replace_dict(m):
        inner = m.group(1)
        inner = parse_collections(inner)  # Recursivo para valores internos
        inner = primitive(inner)
        return f"Dict({{{inner}}})"

    # Listas: [item, ...]
    def replace_list(m):
        inner = m.group(1)
        inner = parse_collections(inner)
        inner = primitive(inner)
        return f"List([{inner}])"

    # Tuplas: (item, ...)
    def replace_tuple(m):
        inner = m.group(1)
        inner = parse_collections(inner)
        inner = primitive(inner)
        return f"Tuple({inner})"

    def replace_index(m: re.Match):
        inner1:str = m.group(1)
        inner2:str = m.group(2)
        return f"{inner1}[{inner2}]"
    # Diccionarios primero (con ":")
    code = re.sub(r"\{(.*)\}", replace_dict, code)

    # Listas y tuplas (non-greedy)
    code = re.sub(r"struct\s+(\w+)\s*\(\s*([a-zA-Z0-9_,\s]+)\)", repl_struct, code)
    code = re.sub(r"\[([^\[\]]*?)\]", replace_list, code)
    code = re.sub(r"([^\s])<([^<>]*)>", replace_index, code)
    code = re.sub(r"(>|])<([^<>]*)>", replace_index, code)
    code = re.sub(r"\s\(([^\(\)]*?)\)", replace_tuple, code)
    code = re.sub(r"expr\((.*)\)", lambda m: f"({m.group(1)})", code)
    return code


def all(code):
    code = primitive(code)
    code = parse_collections(code)
    return code
