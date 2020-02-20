# This display all active Internet connections to the server
# only established connections are included.

def name():
    return "netstat-lookup"

def help():
    return "Displays all active connectios to the server"

def args():
    return ""

def run(args):
    from subprocess import run, DEVNULL, PIPE
    proc = run(["netstat", args.path, "-na"], stdout=PIPE, stderr=DEVNULL)
    print(proc.stdout.decode("utf-8"))
