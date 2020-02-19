# Looks for files in the specified path that have either the SUID
# or SGID bit set. Potentially useful for identifying files that
# could be attack vectors.

def name():
    return "find-sid"

def help():
    return "Find files with the SUID/SGID bit set"

def args():
    return ["path"]

def run(args):
    from subprocess import run, DEVNULL, PIPE
    proc = run(["find", args.path, "-perm", "/u=s,g=s"], stdout=PIPE, stderr=DEVNULL)
    print(proc.stdout.decode("utf-8"))