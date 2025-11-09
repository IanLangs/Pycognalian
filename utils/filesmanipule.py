import ruamel.yaml as _yaml
import json as _json
def rfile(filepath):
    with open(filepath) as f:
        text = f.read()
    return text
def wfile(filepath,newtext):
    with open(filepath, "w") as f:
        f.write(newtext)
def afile(filepath,newtext):
    with open(filepath, "a") as f:
        f.write(newtext)
class yaml:
    def __init__(self, typ='rt', pure=False, output=None, plugins=None):
        super().__setattr__("yaml", _yaml.YAML(typ=typ, pure=pure, output=output, plug_ins=plugins))
    def __getattr__(self, name):
        return getattr(self.yaml, name)
    def __setattr__(self, name, value):
        raise AttributeError("Can't set attributes")
    def __delattr__(self, name):
        raise AttributeError("Can't delete attributes")

class json:
    def __getattr__(self, name):
        return getattr(_json, name)
    def __setattr__(self, name, value):
        raise AttributeError("Can't set attributes")
    def __delattr__(self, name):
        raise AttributeError("Can't delete attributes")
