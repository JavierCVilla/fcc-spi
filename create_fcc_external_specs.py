#!/usr/bin/env python

# Parse an installation of the FCC Externals in CVMFS and generate
# a configuration file to be added to the packages.yaml in the 
# Spack configuration.


import argparse
import yaml
import sys
import glob 
import os

compiler_labels={
    "gcc62":"gcc-6.2.0",
    "gcc8":"gcc-8.2.0"   
}

class Package(object):
    def __init__(self, spec, prefix_path):
	self.name, self.version, self.hash = spec.rsplit("-",2)
        self.prefix_path = prefix_path

def get_compiler_spec(platform):
    """
    Extract compiler from the target platform and return the equivalent name for Spack
    """

    arch, distribution, compiler, buildmode = platform.split("-")
    if compiler in compiler_labels.keys():
        return compiler_labels[compiler]
    raise Exception("Invalid compiler")

def get_spack_platform(platform):
    """
    Return the equivalent platform in Spack
    """

    if "centos7" in platform:
        return "linux-centos7-x86_64"
    elif "slc6" in platform:
        return "linux-scientificlinux6-x86_64"
    raise Exception("Not supported platform")

def get_externals_version(prefix):
    # Remove trailing slash if any
    if prefix[-1] == "/":
	prefix = prefix[:-1]
    version = prefix.split("/")[-1]
    if version:
        return version
    raise Exception("Version not detected in prefix: %s" % prefix)

def generate_config_file(platform, prefix):
    """
    Write a configuration file with the metadata of the packages installed in a given path.
    Assumes the following hierarchy of directories:

    <prefix>/<platform/><spack_platform>/<spack_compiler>/packages

    For example:
     
        |------------- prefix ------------------------||--------platform--------||--spack platoform--||compiler|
        /cvmfs/fcc.cern.ch/sw/releases/externals/94.3.0/x86_64-centos7-gcc62-opt/linux-centos7-x86_64/gcc-6.2.0/packages
    """

    packages_dict = {"packages" : {}}

    spack_compiler = get_compiler_spec(platform)
    spack_platform = get_spack_platform(platform)
    externals_version = get_externals_version(prefix)    

    package_paths = glob.glob(os.path.join(prefix, platform, spack_platform, spack_compiler, "*"))
    packages = [ Package(path.split("/")[-1], path) for path in package_paths ]

    spec_template = "{name}@{version}%{compiler} arch={platform}"
    
    for pkg in packages:
        spec_string = spec_template.format(name=pkg.name,
                                           version=pkg.version,
                                           compiler=spack_compiler.replace('-','@'),
                                           platform=spack_platform)
    
        packages_dict['packages'][pkg.name] = {
            "buildable": False,
       	    "version": [pkg.version],
            "paths": {
                spec_string : pkg.prefix_path
            }
        }

    try:
        # Example: 94.3.0-fcc_externals.yaml
        filename = externals_version + "-fcc_externals.yaml"
        with open(filename, 'w') as f:
           f.write(yaml.dump(packages_dict))
           print("{} successfully written".format(filename))
    except IOError as e:
	print("Configuration file could not be written: (%s)." % e) 

if __name__ == '__main__':
    desc = 'Parse and generate configuration file for FCC Externals installed in CVMFS'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--platform', action="store", dest="platform")
    parser.add_argument('--prefix', action="store", dest="prefix")

    args = parser.parse_args()
    generate_config_file(args.platform, args.prefix)
