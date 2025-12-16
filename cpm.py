import sys, subprocess, re
def main():
    command = ["python3.14", "-m","pip"] + sys.argv[1:]
    pipr = subprocess.run(command, text=True, capture_output=True)
    code =  re.sub(r"pip(\d*)", lambda m:f"cpm{m.group(1)}", str(pipr.stdout) +"\n"+ str(pipr.stderr))
    print(f"\n{code}\n")

if __name__ == "__main__":
    main()