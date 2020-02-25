#!/usr/bin/env python3

import argparse
import importlib
from glob import glob
from pathlib import Path
import sys

# Set up the top-level argument parser which will host the sub-parsers
# of each of the modules.
parser = argparse.ArgumentParser(description="PCTF helper tool")
command_parser = parser.add_subparsers(dest="command", metavar="command")
command_parser.required = True

def load_modules():
    # Find all .py files in the ./modules subdirectory
    for module in glob("./modules/*.py"):
        try:
            # Try to import the module
            module_name = "modules.{0}".format(Path(module).stem)
            imported_module = importlib.import_module(module_name)

            # We imported it; now try to set up the command parsers
            cmd = command_parser.add_parser(imported_module.name(), help=imported_module.help())
            cmd.set_defaults(func=imported_module.run)
            for arg in imported_module.args():
                cmd.add_argument(arg)
        except:
            # The module wasn't valid for some reason. Print the
            # reason and move on to the next one.
            e = sys.exc_info()[0]
            print("Unable to import module {0}".format(module))
            print("Exception: {0}".format(e))

def main():
    load_modules()

    # Parse our command line args, which will set func() to the
    # proper module in the process. Then invoke that module.
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()