##
## Spec file for managing Keucloak version and installation
## This file is based on project https://github.com/abn/keycloak-rpm
## Credits to Arun Babu Neelicattu <arun.neelicattu@gmail.com>
##
%define debug_package   %{nil}
%define __jar_repack    %{nil}

%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}

##
##
##
%define name        prometheus
%define version     2.21.0
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    /opt/%{name}
%define work_dir    %{_sharedstatedir}/%{name}
##
%define _user       prometheus
%define _group      prometheus



##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Event monitoring system with a time series database

Group:              System Environment/Base
License:            APLv2.0
URL:                https://prometheus.io
Source0:            https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1:            %{name}.service
Source2:            %{name}.defaults

BuildRequires:      systemd tar gzip

Requires(pre):      shadow-utils

%description
Prometheus, a Cloud Native Computing Foundation project, is a systems and service
monitoring system. It collects metrics from configured targets at given intervals,
evaluates rule expressions, displays the results, and can trigger alerts if some
condition is observed to be true.

%prep
%setup -q -c %{SOURCE0}

%build



%install

mkdir -vp       %{buildroot}/opt
mkdir -vp       %{buildroot}%{work_dir}/data
mkdir -vp       %{buildroot}%{_sysconfdir}/prometheus
mkdir -vp       prometheus-%{version}.linux-amd64/bin

mv          prometheus-%{version}.linux-amd64       %{buildroot}/%{home_dir}
mv          %{buildroot}/%{home_dir}/prometheus     %{buildroot}/opt/%{name}/bin
mv          %{buildroot}/%{home_dir}/promtool       %{buildroot}/opt/%{name}/bin


mv      %{buildroot}/%{home_dir}/prometheus.yml \
        %{buildroot}%{_sysconfdir}/prometheus/prometheus.yml

install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/default/%{name}




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
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,%{_user},%{_group},-)
%{home_dir}
%{home_dir}/bin/prometheus
%{home_dir}/bin/promtool
%{home_dir}/consoles
%{home_dir}/console_libraries

%defattr(-,%{_user},%{_group},750)
%dir %{work_dir}/data

%attr(644, root, root)  %{_unitdir}/%{name}.service

%config(noreplace) %attr(640, root, %{_group})      %{_sysconfdir}/default/%{name}
%config(noreplace) %attr(640, %{_user}, %{_group})  %{_sysconfdir}/prometheus/prometheus.yml


%changelog
* Wed Oct 14 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 2.21.0
- https://github.com/prometheus/prometheus/releases/tag/v2.21.0
