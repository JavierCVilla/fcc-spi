---
layout: site
---

FCC Software Infrastructure
===========================

Table of Content:

- Main components
- Workflow
- Releases
- Nightlies
- Using the FCC Software


## Main components

The FCC build infrastructure combines the following tools:

- [Github repositories](#github-repositories): Host the code to run the internal tasks
- [Jenkins](#jenkins): Server to automate tasks
- [CVMFS](#cvmfs): Network file system to deploy the experiment software
- [CDash](#cdash): Dashboard to visualize the result of the different builds
- [FCC Jira Issues](#jira): Track issues and tasks


### Github repositories

Most of the FCC Software code is hosted on the official Github project: [HEP-FCC](https://github.com/HEP-FCC/).
Repositories on this project can be classified on three main categories:

- [FCCSW](https://github.com/HEP-FCC/FCCSW): Common software package for all FCC experiments.
- FCC Externals: Specific software packages for the FCC experiment
    + [Heppy](https://github.com/HEP-FCC/heppy): Python framework for HEP Data Analysis
    + [FCC Analyses](https://github.com/HEP-FCC/FCCAnalyses): FCC Specific Analyses
    + [dag](https://github.com/HEP-FCC/dag): Library and examples for DirectedAcyclicGraphs
- Build system tools: Scripts for software deployment and continuous integration.
    + [fcc-spi](https://github.com/HEP-FCC/fcc-spi): Integration tools
    + [fcc-spack](https://github.com/HEP-FCC/fcc-spack): Spack recipes to build and install FCC packages

### Jenkins

FCC makes use of the Jenkins server hosted and mantained by the EP-SFT team: [https://epsft-jenkins.cern.ch](https://epsft-jenkins.cern.ch).
Inside this server, there is a dedicated view for the [FCC Projects](https://epsft-jenkins.cern.ch/view/FCC/).

Current operations run through Jenkins are:

**Continuous integration builds**

Some of the previous software packages listed [above](#github-repositories)
are configured to automatically run builds for every new Pull Request. These builds take the code with the changes
proposed in the Pull Request and build the package. If the build phase is successful, then all tests are run.
Once the compilation and tests have been passed without errors, the Pull Request in Github is marked as good to
be merged after the corresponding code reviews.

For each package configured with this continuous integration process we have three different jenkins job:

    + `<package_name>-pullrequest-trigger`: It is the connection between Github and Jenkins, it gets triggered every time there is a new Pull Request or an existing Pull Request is updated.
    + `<package_name>-pullrequest-handler`: Receives the configuration set of options to spawn one build per combination of platform and compiler, i.e.: `centos7/gcc8` and `slc6/gcc8`.
    + `<package_name>-pullrequest-build`: Runs the build for a given combination. Each package has a different [build script](https://github.com/HEP-FCC/fcc-spi/tree/master/builds) to get built and run the corresponding tests.

In the case of FCCSW the result of the last job (`<package_name>-pullrequest-build`) the result of the CMake build and tests is reported
to the CDash dashboard and grouped into a [slot dedicated to Pull Requests](https://cdash.cern.ch/index.php?project=FCC#PullRequests).

**Nightlies**

These are jobs that run every night or on a daily basis, each with a different purpose:

- [FCCSW](https://epsft-jenkins.cern.ch/view/FCC/job/FCCSW/): Build the latest version of [FCCSW](https://github.com/HEP-FCC/FCCSW) and run the tests (master branch on Github). Uses the latest stable release of the externals specified in the [init.sh](https://github.com/HEP-FCC/FCCSW/blob/master/init.sh) script inside the repo.
- [FCCSW-exp](https://epsft-jenkins.cern.ch/view/FCC/job/FCCSW-exp): Same as *FCCSW*, but using the latest version of the nightlies for the external dependencies (the result of *FCC-nightlies*)
- [FCC-nightlies](https://epsft-jenkins.cern.ch/view/FCC/job/FCC-nightlies/): Build the FCC External packages (develop versions) against the latest [LCG Release](http://lcginfo.cern.ch/#releases) version picked up by the project.
- [FCC-nightlies-exp](https://epsft-jenkins.cern.ch/view/FCC/job/FCC-nightlies): Same as *FCC-nightlies* but using the [latest version of the LCG nightlies (dev4)](http://lcginfo.cern.ch/release/dev4/).
- [FCC-cvmfs-install-nightlies](https://epsft-jenkins.cern.ch/view/FCC/job/FCC-cvmfs-install-nightlies/): Deploy the result of *FCC-nightlies* to CVMFS.


**Releases**
- [FCC-release-spack](https://epsft-jenkins.cern.ch/view/FCC/job/FCC-release-spack/): Build a release of the the FCC Externals (a set of specific stable versions, i.e: `94.2.0`, `96.0.0`) against the latest [LCG Release](http://lcginfo.cern.ch/#releases) version picked up by the project.
- [FCC-cvmfs-install](https://epsft-jenkins.cern.ch/view/FCC/job/FCC-cvmfs-install/): Deploy the result of *FCC-release-spack* to CVMFS.


### CVMFS



 in a fast, scalable, and reliable way

### CDash



### FCC Jira Issues


