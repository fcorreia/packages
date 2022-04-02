

## Quick Solution for the dependencies




```shell script
# Install devtoolset-9
# On CentOS, install package centos-release-scl available in CentOS repository:
yum install -y centos-release-scl 

# On RHEL, enable RHSCL repository for you system:
yum-config-manager --enable rhel-server-rhscl-9-rpms

# 2. Install the collection:
yum install -y devtoolset-9

# 3. Start using software collections:
scl enable devtoolset-9 bash

## Error: No Package found for mariadb-connector-c-devel
## Error: No Package found for signalwire-client-c
yum install -y \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/broadvoice-0.1.0-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/broadvoice-devel-0.1.0-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/flite-2.0.0-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/flite-devel-2.0.0-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/g722_1-0.2.0-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/g722_1-devel-0.2.0-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/ilbc2-0.0.1-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/ilbc2-devel-0.0.1-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/libks-1.6.0-1.el7.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/libsilk-1.0.9-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/libsilk-devel-1.0.9-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/opus-1.1-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/opus-devel-1.1-1.el7.x86_64.rpm \
/workspace/repository/el7/freeswitch/sofia-sip-1.13.7-1.skywalker.el7.x86_64.rpm \
/workspace/repository/el7/freeswitch/sofia-sip-devel-1.13.7-1.skywalker.el7.x86_64.rpm \
/workspace/repository/el7/freeswitch/sofia-sip-glib-1.13.7-1.skywalker.el7.x86_64.rpm \
/workspace/repository/el7/freeswitch/sofia-sip-glib-devel-1.13.7-1.skywalker.el7.x86_64.rpm \
/workspace/repository/el7/freeswitch/sofia-sip-utils-1.13.7-1.skywalker.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/soundtouch-1.7.1-1.el7.x86_64.rpm \
https://packages.2600hz.com/centos/7/stable/freeswitch-deps/2021.02.15/soundtouch-devel-1.7.1-1.el7.x86_64.rpm \
/workspace/repository/el7/freeswitch/spandsp3-3.0.0-1.skywalker.el7.x86_64.rpm \
/workspace/repository/el7/freeswitch/spandsp3-devel-3.0.0-1.skywalker.el7.x86_64.rpm 

```

```shell script

yum install -y \
http://repo.okay.com.mx/centos/7/x86_64/release/signalwire-client-c-1.2.0-1.el7.x86_64.rpm \
http://repo.okay.com.mx/centos/7/x86_64/release/signalwire-client-c-devel-1.2.0-1.el7.x86_64.rpm \
http://repo.okay.com.mx/centos/7/x86_64/release/mariadb-connector-c-3.0.10-1.el7.x86_64.rpm \
http://repo.okay.com.mx/centos/7/x86_64/release/mariadb-connector-c-devel-3.0.10-1.el7.x86_64.rpm
```