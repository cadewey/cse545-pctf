# Compiles a .c file with "hardened" options enabled to (hopefully) make it more
# difficult for an attacker to exploit the program

def name():
    return "gcc-harden"

def help():
    return "Compile a .c file with hardened security options"

def args():
    return ["arch", "path", "output"]

def run(args):
    from subprocess import run, DEVNULL, PIPE, STDOUT
    
    gcc_flags = [
        "-m{0}".format(args.arch),
        "-fPIE",
        "-fstack-protector-strong",
        "-D_FORTIFY_SOURCE=2",
        "-Wformat",
        "-Wformat-security",
        "-Wl,-z,relro",
        "-Wl,-z,now",
        "-o {0}".format(args.output),
        args.path
    ]
    
    proc = run(["/usr/bin/gcc"] + gcc_flags, stdout=PIPE, stderr=STDOUT)
    print(proc.stdout.decode("utf-8"))
