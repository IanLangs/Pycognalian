import sys
from vm.verifiquer.pcow import *
import vm.vm as vm
from syntax.classtypes import *
from syntax.buildins import *
from utils import filesmanipule
from utils import *

yaml = filesmanipule.yaml()

def main():
    if len(sys.argv) == 4:
        if sys.argv[2] == "-p":
            code = filesmanipule.rfile(sys.argv[1])
            code = vm.translate(code)
            filesmanipule.wfile(sys.argv[3], code)
    elif len(sys.argv) == 3:
        if sys.argv[2].startswith("-"):
            if sys.argv[2] == "-r":
                print(vm.returned(sys.argv[1]))
            elif sys.argv[2] == "-cb":
                vm.cb(sys.argv[1])
            elif sys.argv[2] == "-eb":
                vm.eb(sys.argv[1])
            else:
                raise Exception("mode are invalid")
        else:
            raise Exception("Usage: py cog2 file | py cog2 -info | py cog2 file -r | py cog2 file -p file2")
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-info":
            with open("cognalian.yml", "r") as f:
                print(f.read().replace(r"\n", "\n").replace(r"\t", "\t"))
        elif sys.argv[1] == "--version":
            with open("cognalian.yml", "r") as f:
                print(f"cognalian version {(yaml.load(f))["language"]["version"]}")
        else:
            vm.execute(sys.argv[1])
    else:
        raise Exception("Usage: py cog2 file | py cog2 -info | py cog2 file -r | py cog2 file -p file2")
if __name__ == "__main__":
    main()


