import sys, subprocess, re
def main():
    command = ["python", "-m", "pip"] + sys.argv
    pipr = subprocess.run(command, capture_output=True, text=True, stdout=subprocess.DEVNULL, check=True)
    code = re.sub(r"pip(\d*)", lambda m:f"cpm{m.group(1)}", pipr.stdout +"\n"+ pipr.stderr)
    print(f"\n{code}\n")
