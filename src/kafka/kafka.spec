# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


%define debug_package   %{nil}
%define __jar_repack    %{nil}


##
##
##
%define name            kafka
%define version         2.5.1
%define scala_version   2.12
%define release         %{rpm_release}.%{disttype}%{distnum}
%define conf_dir        /etc/%{name}
%define home_dir        /opt/%{name}
%define log_dir         /var/log/%{name}
%define work_dir        %{_sharedstatedir}/%{name}
##
%define _user           %{name}
%define _group          %{name}



##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Apache Kafka® is a distributed streaming platform

Group:              System Environment/Base
License:            APLv2.0
URL:                https://kafka.apache.org/
Source0:            https://archive.apache.org/dist/kafka/%{version}/kafka_%{scala_version}-%{version}.tgz
Source1:            kafka.512sum
Source2:            kafka.service
Source3:            kafka.sysconfig
Source4:            kafka-zookeeper.service
Source5:            kafka-zookeeper.sysconfig
Source6:            kafka-zookeeper.properties


BuildRequires:      systemd tar gzip

Requires(pre):      shadow-utils
Requires:           jre >= 1.8

%description
Apache Kafka is a community distributed event streaming platform capable of handling trillions of events a day.
Initially conceived as a messaging queue, Kafka is based on an abstraction of a distributed commit log. Since being
created and open sourced by LinkedIn in 2011, Kafka has quickly evolved from messaging queue to a full-fledged
event streaming platform.

%prep

%setup -q -c

%build
echo "Validating Package"
pushd %{_sourcedir}
grep $(basename %{SOURCE0})  %{SOURCE1} | sha512sum -c
popd

%install
mkdir -vp       %{buildroot}%{conf_dir}
mkdir -vp       %{buildroot}%{work_dir}
mkdir -vp       %{buildroot}/opt
mkdir -vp       %{buildroot}/var/log/%{name}

cp -rp          kafka_%{scala_version}-%{version}  %{buildroot}/opt/kafka

sed             's/log.dirs=.*/log.dirs=\/var\/log\/kafka/g'  \
                %{buildroot}%{home_dir}/config/server.properties \
                > %{buildroot}%{conf_dir}/server.properties


install -D  %{SOURCE2}     %{buildroot}/%{_unitdir}/%{name}.service
install -D  %{SOURCE3}     %{buildroot}/%{_sysconfdir}/sysconfig/%{name}


## Zookeeper
mkdir -vp       %{buildroot}/var/lib/%{name}-zookeeper
cp              %{SOURCE6} %{buildroot}%{conf_dir}/zookeeper.properties

install -D  %{SOURCE4}     %{buildroot}/%{_unitdir}/%{name}-zookeeper.service
install -D  %{SOURCE5}     %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-zookeeper


%pre
getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd -r -g %{_group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name} user" %{_user}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
getent passwd %{_user} >/dev/null && userdel %{_user}
## getent group %{_group} >/dev/null && groupdel %{_group}
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,%{_user},%{_group},-)
%{home_dir}
%dir %{work_dir}
%dir /var/log/%{name}

%attr(644, root, root)  %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{_group}) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %attr(640, root, %{_group}) %{conf_dir}/server.properties

## Zookeeper
%dir /var/lib/%{name}-zookeeper
%attr(644, root, root)  %{_unitdir}/%{name}-zookeeper.service
%config(noreplace) %attr(640, root, %{_group}) %{_sysconfdir}/sysconfig/%{name}-zookeeper
%config(noreplace) %attr(640, root, %{_group}) %{conf_dir}/zookeeper.properties

%changelog
* Wed Nov 22 2017 Francisco Correia <fcorreia@users.noreply.github.com> - 2.5.1
- Initial package
