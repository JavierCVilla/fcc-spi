#!/usr/bin/env python

import sys

def get_compiler(filename):
    with open(filename) as fname:
        compiler_line = fname.readlines()[2]
        compiler = compiler_line.split()[-1]
        name, version = compiler.split(';')
	print("Compiler: %s@%s" % (name, version))
        
    with open('lcg_compiler.txt', 'w') as f:
        f.write(version)
        print("Compiler version saved in: lcg_compiler.txt")

if __name__ == "__main__":
    for arg in sys.argv:
	if 'LCG_externals' in arg:
            lcg_spec_file = arg
            get_compiler(lcg_spec_file)
