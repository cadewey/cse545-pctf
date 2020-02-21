# Team 9 PCTF tool

This is a multi-purpose python tool written in python 3 to help Team 9 with the PCTF project assignment.

## Running the tool

There's no specific installation at this time; the tool assumes any dependencies are already in place, meaning that any modules that rely on external binaries will not run correctly if the binaries cannot be found. Simply clone the repo and you'll be ready to run.

**Possible improvement idea:** Give this tool the ability to install dependencies for a module via [exodus](https://github.com/intoli/exodus).

To see a list of commands, run `./pctf.py -h`.

## Adding modules

Using the existing modules as a template is a good way to get your own module off the ground, but briefly:

1. Create a new .py file in the `modules/` directory that will contain your functionality.
2. Implement the following methods with the following return types in your file:
   - `name()` (`str`) - The name of your module as it would be typed on the command line when running it.
   - `help()` (`str`) - A brief description of what your module does. This is displayed for your command in the main help page.
   - `args()` (`list` of `str`) - Additional positional arguments that your module requires.
   - `run()` (no return value) - The method that will be invoked when your tool is executed.
3. That's it! The main loop will import anything in the `modules/` directory that meets this format.

**Possible improvement idea:** Make arguments more flexible, so that you can specify optional args and things of that nature.

**References:** 

 - https://linuxaria.com/howto/how-to-verify-ddos-attack-with-netstat-command-on-linux-terminal
 - Flags in `gcc-harden` taken from https://wiki.debian.org/Hardening

**Requirements for Specific Modules:**

	1. swpag-client (Class Requirement): pip3 install swpag-client for:
		- submit-flag
		- get-vm	
	2. pwn-tools:
		- gen-shellcode
