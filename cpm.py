import sys, subprocess, re
file = "/".join(re.split(r"\\|/",__file__)[:-1])
System = sys.platform
def main():
    command = [file + "/Python314-" + System + "/python.exe", "-m", "pip"] + sys.argv
    pipr = subprocess.run(command, capture_output=True, text=True, stdout=subprocess.DEVNULL, check=True)
    code = re.sub(r"pip(\d*)", lambda m:f"cpm{m.group(1)}", pipr.stdout +"\n"+ pipr.stderr)
    print(f"\n{code}\n")
