#!/usr/bin/env python

# Given two packages.yaml files merge the content of the 'source' into the 'target'.
# Only those packages present in both files (source and target) are modified in the
# target file.
#
# This allows to override an existing configuration with a set of packages already
# installed in the system or in CVMFS
#
# Those packages present in the target file but not in the source are not affected.
# This script overwrites the target file with the merged content.

import argparse
import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two packages.yaml files")

    parser.add_argument("-s", "--source", action="store", dest="source")
    parser.add_argument("-t", "--target", action="store", dest="target")

    args = parser.parse_args()
    
    with open(args.source, 'r') as f:
        source_dict = yaml.load(f.read())

    with open(args.target, 'r') as f:
        target_dict = yaml.load(f.read())

    for pkg in source_dict['packages'].keys():
        if pkg in target_dict['packages']:
             target_dict['packages'][pkg] = source_dict['packages'][pkg]

    try:
        with open(args.target, 'w') as f:
            f.write(yaml.dump(target_dict))
            print("Content of %s successfully updated" % args.target)
	    print("The following packages were updated:")
            for pkg in sorted(source_dict['packages'].keys()):
                print("- %s" % pkg)
    except IOError as e:
        print("Could not update the target file (%s)." % e)
