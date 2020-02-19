#!/usr/bin/env python3

import argparse
import importlib
from glob import glob
from pathlib import Path

parser = argparse.ArgumentParser(description="PCTF helper tool")
command_parser = parser.add_subparsers(dest="command", metavar="command")
command_parser.required = True

def load_modules():
    for module in glob("./modules/*.py"):
        module_name = "modules.{0}".format(Path(module).stem)
        imported_module = importlib.import_module(module_name)

        cmd = command_parser.add_parser(imported_module.name(), help=imported_module.help())
        cmd.set_defaults(func=imported_module.run)
        for arg in imported_module.args():
            cmd.add_argument(arg)

def main():
    load_modules()

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()