#!/usr/bin/env python

# This script takes an existing Spack buildcache and reindex the index.html
# file with all the packages existing in the current directory.
#
# Spack's buildcache feature uses an index.html file as a database to keep
# track all the available binaries. New binaries added to the directory
# without updating the index.html file will not be considered by Spack.
#
# Usage
# 1. Move to the directory where index.html exists
# 2. Copy the new binaries into this directory
# 3. Run the script:
#
#     python reindex-buildcache.py
#
# Note: This script will remove the existing index.html and replace it with a
# new one.

import glob

opening_html="""
<html>

<head>
</head>

<list>
"""

closing_html="""
</list>
</html>
"""

def write_index(binary_specs):
    filename="index.html"

    with open(filename, 'w') as f:
        template_line = '<li><a href="{0}"</a> {0}</a>\n'
        # Write HTML headers
        f.write(opening_html)
        for spec in binary_specs:
            f.write(template_line.format(spec))
        # Write HTML Closing headers
        f.write(closing_html)

def reindex():
    all_specs = glob.glob("*.yaml")
    print("Adding %d files" % len(all_specs))
    write_index(all_specs)

if __name__ == "__main__":
    reindex()

