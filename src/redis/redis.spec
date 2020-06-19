
%define debug_package   %{nil}
%define __jar_repack    %{nil}

%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}

##
##
##
%define name        redis
%define version     6.0.5
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    %{_sharedstatedir}/%{name}
%define work_dir    %{_sharedstatedir}/%{name}
%define conf_dir    %{_sysconfdir}/redis
##
%define _user       redis
%define _group      redis

%global tls_support 0

##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            In-Memory persistent key-value database

Group:              Application/Databases
License:            BSD
URL:                https://redis.io/
Source0:            http://download.redis.io/releases/redis-%{version}.tar.gz
Source1:            redis.service
Source2:            redis.sysconfig
Source3:            redis.SHA256SUM

Patch0:             redis.conf.patch
BuildRequires:      systemd tar gzip

%if 0%{?tls_support}
BuildRequires:      openssl-devel   tcltls
%endif

## Running Tests
BuildRequires:      tcl >= 8.5
## Required support for C11
#BuildRequires:      gcc >= 4.9

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Redis is an open source (BSD licensed), in-memory data structure store, used as a database,
cache and message broker. It supports data structures such as strings, hashes, lists, sets,
sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries
and streams. Redis has built-in replication, Lua scripting, LRU eviction, transactions and
different levels of on-disk persistence, and provides high availability via Redis Sentinel
and automatic partitioning with Redis Cluster.


%prep
pushd %{_sourcedir}
grep $(basename %{SOURCE0})  %{SOURCE3} | sha256sum -c
popd

%setup -q
%patch0 -p0

%build
# cd ${name}-%{version}
%if 0%{?tls_support}
make %{?_smp_mflags} BUILD_TLS=yes all
./utils/gen-test-certs.sh
./runtest --tls
%else
make %{?_smp_mflags} all
make %{?_smp_mflags} test
%endif

%install
make install PREFIX=%{buildroot}%{_prefix}

# Install Systemd and configs
install -p -D -m 755 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -p -D -m 750 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 750 redis.conf %{buildroot}%{_sysconfdir}/%{name}/redis.conf
install -p -D -m 750 sentinel.conf %{buildroot}%{_sysconfdir}/%{name}/sentinel.conf

## Logging
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}

## Working directory
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}

## Pid Location
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

%pre
getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd --system --no-create-home  --gid  %{_group} --home-dir %{work_dir} \
    --shell /sbin/nologin  --comment "%{name} user" %{_user}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
## getent passwd %{_user} >/dev/null && userdel %{_user}
## getent group %{_group} >/dev/null && groupdel %{_group}
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,%{_user},%{_group},-)
%dir %attr(0755, %{_user}, %{_group}) %{_sysconfdir}/%{name}
%config(noreplace) %attr(644, %{_user},%{_group}) %{_sysconfdir}/%{name}/redis.conf
%config(noreplace) %attr(644, %{_user},%{_group}) %{_sysconfdir}/%{name}/sentinel.conf
%config(noreplace) %attr(644, %{_user},%{_group}) %{_sysconfdir}/sysconfig/%{name}

%dir %attr(0755, %{_user}, %{_group}) %{_localstatedir}/lib/%{name}
%dir %attr(0755, %{_user}, %{_group}) %{_localstatedir}/log/%{name}
%dir %attr(0755, %{_user}, %{_group}) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*

%attr(644, root, root)  %{_unitdir}/%{name}.service


%changelog
* Fri Jun 19 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 6.0.5-1
- Initial package
