# Attempts to create shellcode with given format.
from pwn import *
import os

def name():
    return "gen-shellcode"

def help():
    return "Generates and returns shellcode."

def args():
    return ['command', 'nops']

def run(args):
	context(arch='i386', os='linux')
	sc = shellcraft.i386
	command = args.command
	nop_size = args.nops
	try:
		print('Shellcode for: ' + command)
		shellcode = sc.linux.execve(args.command)
		shellcode = asm(shellcode)
		nop_asm = sc.nop() * int(nop_size)
		nop_asm = asm(nop_asm)
		shellcode = nop_asm + shellcode
		print (shellcode)
	except:
		print("Error Generating Shellcode!")
