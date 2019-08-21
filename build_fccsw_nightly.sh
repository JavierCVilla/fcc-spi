#!/bin/sh 

# Exit the script if any statement returns a non-true return value
set -e

env | sort

# Prepare environment
echo "export COMPILER=$COMPILER" >> $WORKSPACE/setup.sh
echo "export BUILDTYPE=$BUILDTYPE" >> $WORKSPACE/setup.sh
echo "export WORKSPACE=$PWD" >> $WORKSPACE/setup.sh
echo "export weekday=$weekday" >> $WORKSPACE/setup.sh
echo "source fcc-spi/jk-setup-spack.sh ${LCG_VERSION} ${FCC_VERSION}" >> $WORKSPACE/setup.sh

source fcc-spi/jk-setup-spack.sh ${lcg_version} ${fcc_version}

# Configure upstream installation in cvmfs
cp fcc-spi/config/upstreams.tpl $WORKSPACE/.spack/upstreams.yaml

# Replace externals path
externals=/cvmfs/fcc.cern.ch/sw/nightlies/externals/$FCC_VERSION/$PLATFORM
prefix=/cvmfs/fcc.cern.ch/sw/releases/externals/$FCC_VERSION
sed -i "s@{{EXTERNALS_PATH}}@`echo $externals`@" $WORKSPACE/.spack/upstreams.yaml

# Install the FCCSW
pkgname="fccsw"
pkgversion=$PACKAGE_VERSION

# Get number of cpu in the machine
# and use half of them for the build
ncpu=`cat /proc/cpuinfo | grep processor | wc -l`
halfcpu=$((ncpu / 2))

# Generate configuration file for fcc externals
python fcc-spi/create_fcc_external_specs.py --prefix $prefix --platform $PLATFORM

# Merge this configuration file with the existing packages.yaml
python fcc-spi/merge-packages-yaml.py --source ${FCC_VERSION}-fcc_externals.yaml --target $WORKSPACE/.spack/linux/packages.yaml

# Running
echo "spack install -j $halfcpu $pkgname %gcc@${!COMPILERversion}"
spack install -j $halfcpu $pkgname@$pkgversion %gcc@${!COMPILERversion}

# Get hash of installed package
pkghash=`spack find -L ${pkgname}@${pkgversion}%gcc@${!COMPILERversion} | grep $pkgname | cut -d" " -f 1`

# Ensure patchelf is installed and get hash
spack install patchelf %gcc@${!COMPILERversion}
patchelfHash=`spack find -L ${pkgname}@${pkgversion}%gcc@${!COMPILERversion} | grep $pkgname | cut -d" " -f 1`

# Create buildcache
# -f option: overwrite existing binaries if any
spack buildcache create -f -d $WORKSPACE/tarballs -u -a $pkgname
spack buildcache create -f -d $WORKSPACE/tarballs -u /$patchelfHash

# Define path to get the buildcache
export BUILDCACHE_PATH=$WORKSPACE/tarballs

# Define build as a release
export BUILDMODE='release'

# Define path to send the buildcache in the cvmfs node
export BUILDCACHETARGET=/var/spool/cvmfs/fcc.cern.ch/sftnight/build_cache

kinit sftnight@CERN.CH -5 -V -k -t /ec/conf/sftnight.keytab
scp -r $BUILDCACHE_PATH sftnight@cvmfs-fcc:$BUILDCACHETARGET
export BUILDCACHETARGET=$BUILDCACHETARGET/tarballs
export PKGHASH=${pkghash}
export LCG_VERSION=${lcg_version}

#--Create property file to transfer variables
cat > $WORKSPACE/properties.txt << EOF
PLATFORM=${PLATFORM}
COMPILER=${COMPILER}
weekday=${weekday}
BUILDCACHE=${BUILDCACHETARGET}
PKGHASH=${pkghash}
PKGNAME=${pkgname}
LCG_VERSION=${lcg_version}
FCC_VERSION=${fcc_version}
BUILDTYPE=${BUILDTYPE}
BUILDMODE=${BUILDMODE}
EOF
