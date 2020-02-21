# Looks for common c code with vulns.
import os

def name():
    return "find-common-vul"

def help():
    return "Find files with common vulnerability code words"

def args():
    return ["path"]

def run(args):
	rootdir=(args.path)
	common_vulnerabilities = "gets scanf strcat strcpy strcmp printf access chown chgrp chmod mktemp tmpfile exec popen system GET POST shell_exec exec".split()
	print(common_vulnerabilities)
	try:
		for folder, dirs, files in os.walk(rootdir):
			for file in files:
				if file.endswith('.c'):
					fullpath = os.path.join(folder, file)
					with open(fullpath, 'r') as f:
						for line in f:
							for v in common_vulnerabilities:
								if v in line:
									print(fullpath)
									break
	except:
		print("Error Searching Path!")