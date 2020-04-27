# packages
Custom Software Packaging



## Tools for Packaging

```shell script
## Minimal tools to install
yum install -y gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools
```


RPM Dev Tools

|Command            | Description                                               |
|:------------------|:----------------------------------------------------------|
|rpmdev-setuptree   |Create RPM build tree within user's home directory         |
|rpmdev-diff 	    |Diff contents of two archives                              |
|rpmdev-newspec 	|Creates new .spec from template                            |
|rpmdev-rmdevelrpms |Find (and optionally remove) "development" RPMs            |
|rpmdev-checksig 	|Check package signatures using alternate RPM keyring       |
|rpminfo 	        |Print information about executables and libraries          |
|rpmdev-md5 	    |Display the md5sum of all files in an RPM                  |
|rpmdev-vercmp 	    |RPM version comparison checker                             |
|spectool 	        |Expand and download sources and patches in specfiles       |
|rpmdev-wipetree 	|Erase all files within dirs created by rpmdev-setuptree    |
|rpmdev-extract 	|Extract various archives, "tar xvf" style                  |


## Useful Commands
```shell script
# List System macros
rpm --showrc

# Evaluate a macro
$ rpm --eval %{_sharedstatedir}
```


## References
 - [RPM Packaging Guide](https://rpm-packaging-guide.github.io/)
 - [SystemD :: Execution environment configuration](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)
