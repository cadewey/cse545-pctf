# List and block threatning IPs.

def name():
    return "block-ip"

def help():
    return "List and block IPs on the iptable. use -l 'IP' to see the blocked ip address and '-d IP'  to block"

def args():
    return ""


def main(args):
	import getopt

	import subprocess
	import sys
	
	try:
		opt, arg = getopt.getopt(args, "ha:d:l", ["help", "add=", "delete=", "list"])
			
		if len(opt) == 0:
				# Adding without -a or --add: iptables 1.2.3.6
			if len(arg) > 0:
				opt = []
				for i in arg:
					opt.append(("-a", arg))
				
			else:
				opts = [("-h","")]
			
		for a, b in opt:
				
			if a in ("-a", "--add"):
				subprocess.call(["iptables", "-A", "INPUT", "-s", b, "-j", "DROP"])
			elif a in ("-d", "--delete"):
				subprocess.call(["iptables", "-D", "INPUT", "-s", b, "-j", "DROP"])
			elif a in ("-l", "--list"):
				subprocess.call(["iptables", "-L", "-n"])
	except getopt.GetoptError as err:
		print ("blockip error:" + str(err))
		sys.exit(2)


	




