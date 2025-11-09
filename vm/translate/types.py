import re

def primitive(code):
    # Strings entre comillas dobles (no greedy, captura vacíos)
    code = re.sub(r'norm"([^"]*)"', lambda m: f"'{m.group(1)}'", code)
    code = re.sub(r'r"([^"]*)"', lambda m: f"r'{m.group(1)}'", code)
    code = re.sub(r'"([^"]*)"', lambda m: f'String("{m.group(1)}")', code)
    # Booleanos: true/false
    code = re.sub(r"\b(true|false)\b", lambda m: f"Bool({1 if m.group(1) == 'true' else 0})", code)
    # Números (enteros o flotantes, opcional underscore)
    code = re.sub(r"\b\d+(?:_\d+)*(?:\.\d+)?\b", lambda m: f"Number({m.group(0)})", code)
    # Complex
    code = re.sub(r"complex\((.*?)\)", lambda m: f"CNum({m.group(1)})", code)
    return code


# Función recursiva para procesar colecciones anidadas
def parse_collections(code):

    # Diccionarios: {key: value, ...}
    def replace_dict(m):
        inner = m.group(1)
        inner = parse_collections(inner)  # Recursivo para valores internos
        return f"Dict({{{inner}}})"

    # Sets: {item, ...} que no tenga ":" dentro
    def replace_set(m):
        inner = m.group(1)
        inner = parse_collections(inner)
        return f"Set({{{inner}}})"

    # Listas: [item, ...]
    def replace_list(m):
        inner = m.group(1)
        inner = parse_collections(inner)
        return f"List([{inner}])"

    # Tuplas: (item, ...)
    def replace_tuple(m):
        inner = m.group(1)
        inner = parse_collections(inner)
        return f"Tuple({inner})"

    # Diccionarios primero (con ":"), sets después (sin ":")
    code = re.sub(r"\{([^{}]*:[^{}]*)\}", replace_dict, code)
    code = re.sub(r"\{([^{}:]*)\}", replace_set, code)

    # Listas y tuplas (non-greedy)
    code = re.sub(r"\[([^\[\]]*?)\]", replace_list, code)
    code = re.sub(r"([^\s])<(.*)>", lambda m: f"{m.group(1)}[{m.group(2)}]", code)
    code = re.sub(r"\s\(([^\(\)]*?)\)", replace_tuple, code)
    code = re.sub(r"expr\((.*)\)", lambda m: f"({m.group(1)})", code)
    return code


def all(code):
    code = primitive(code)
    code = parse_collections(code)
    return code
