# Generic command

def name():
    return "Generic command"

def help():
    return "Execute commands with two arguments"

def args(*args):
    arg0  = "Command"
    arg1  = "arg1"
    arg3  = "arg2"
    return args 


def run(args):
    from subprocess import run, DEVNULL, PIPE
    proc = run([ args.Command, args.arg1, args.arg2 ], stdout=PIPE, stderr=DEVNULL)
    print(proc.stdout.decode("utf-8"))
