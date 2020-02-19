# Attempts to ping sweep the specified CIDR addres space
def name():
    return "ping-sweep"

def help():
    return "Look for hosts on the network"

def args():
    return ["address"]

def run(args):
    from subprocess import run, DEVNULL, PIPE
    proc = run(["nmap", "-PS", "-n", args.address], stdout=PIPE, stderr=PIPE)
    print(proc.stdout.decode("utf-8"))
