import sys
import vm.vm as vm
from syntax.classtypes import *
from syntax.buildins import *
from utils import filesmanipule
yaml = filesmanipule.yaml()
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
            with open("cognalian.yml", "r") as f:
                print(f.read())
        elif sys.argv[1] == "--version":
            with open("cognalian.yml", "r") as f:
                print(f"cognalian version {(yaml.load(f))["language"]["version"]}")
        else:
            vm.execute(sys.argv[1])
    else:
        raise Exception("Usage: cog file or cog -info or cog file -r")

if __name__ == "__main__":
    main()