import json
import sys
import vm.vm as vm
from syntax.classtypes import *
from syntax.buildins import *
from utils import filesmanipule
def main():
    if len(sys.argv) == 3:
        if sys.argv[1].startswith("-"):
            if sys.argv[1] == "-r":
                print(vm.returned(sys.argv[2]))
            else:
                raise Exception("mode are invalid")
        elif sys.argv[2].startswith("-"):
            if sys.argv[2] == "-r":
                print(vm.returned(sys.argv[1]))
            else:
                raise Exception("mode are invalid")
        else:
            raise Exception("Usage: cog file or cog -info or cog file -r")
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-info":
            print(json.dumps(filesmanipule.rfile("./cognalian.json"), indent=4).replace(r"\n", """
""").replace(r'"{', "{").replace(r'}"', "}").replace(r'\"', '"'))
        else:
            vm.execute(sys.argv[1])

if __name__ == "__main__":
    main()