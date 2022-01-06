
%define debug_package   %{nil}
%define __jar_repack    %{nil}

%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}

##
##
##
%define name        consul
%define version     1.9.13
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    /opt/%{name}
%define work_dir    %{_sharedstatedir}/%{name}
%define conf_dir    %{_sysconfdir}/consul.d
##
%define _user       consul
%define _group      consul


%ifarch x86_64 amd64
%define consul_arch  amd64
%endif

##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Service discovery and configuration made easy.

Group:              System Environment/Daemons
License:            Mozilla Public License, version 2.0
URL:                https://www.consul.io/
Source0:            https://releases.hashicorp.com/consul/%{version}/consul_%{version}_%{_os}_%{consul_arch}.zip
Source1:            https://releases.hashicorp.com/consul/%{version}/consul_%{version}_SHA256SUMS
Source2:            consul.service
Source3:            consul.sysconfig

BuildRequires:      systemd tar gzip

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a
   DNS or HTTP interface. External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster.
   The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level
   circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination,
   leader election and more. The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.


%prep
# curl -OL %{SOURCE0}
%setup -q -c

%build
echo "Using pre-compiled Binaries"
pushd %{_sourcedir}
grep $(basename %{SOURCE0})  %{SOURCE1} | sha256sum -c
popd

%install

## directories
mkdir -vp %{buildroot}%{work_dir}
mkdir -vp %{buildroot}%{conf_dir}

## consul binary
%{__install} -p -D -m 0755 consul %{buildroot}%{_sbindir}/consul

install -D  %{SOURCE2}     %{buildroot}/%{_unitdir}/%{name}.service
install -D  %{SOURCE3}     %{buildroot}/%{_sysconfdir}/sysconfig/%{name}


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
%{_sbindir}/consul

%defattr(-,%{_user},%{_group},750)
%dir %{work_dir}
%dir %{conf_dir}

%attr(644, root, root)  %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{_group})      %{_sysconfdir}/sysconfig/%{name}


%changelog
* Thu Jan 06 2022 Francisco Correia <fcorreia@users.noreply.github.com> - 1.9.13-1
- Upgrade Version

* Wed Feb 17 2021 Francisco Correia <fcorreia@users.noreply.github.com> - 1.9.3-1
- Upgrade Version

* Wed Nov 18 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.8.5-1
- Upgrade Version

* Mon Apr 27 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.7.2-1
- Initial package
