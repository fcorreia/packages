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
%define name        prometheus-mysqld-exporter
%define version     0.14.0
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    /opt/prometheus

##
%define _user       prometheus-exporter
%define _group      prometheus



##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Prometheus MySQL Server Exporter

Group:              System Environment/Base
License:            APLv2.0
URL:                https://github.com/prometheus/mysqld_exporter
Source0:            https://github.com/prometheus/mysqld_exporter/releases/download/v%{version}/mysqld_exporter-%{version}.linux-amd64.tar.gz
Source1:            %{name}.service
Source2:            %{name}.defaults

BuildRequires:      systemd tar gzip

Requires(pre):      shadow-utils

%description
Prometheus exporter for MySQL server metrics.
Supported versions:
    MySQL >= 5.6.
    MariaDB >= 10.1
NOTE: Not all collection methods are supported on MySQL/MariaDB < 5.6

%prep
%setup -q -c %{SOURCE0}

%install



install -D  mysqld_exporter-%{version}.linux-amd64/mysqld_exporter    \
            %{buildroot}%{home_dir}/bin/mysqld_exporter


install -D -p -m 0644 %{SOURCE1}    %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2}    %{buildroot}/%{_sysconfdir}/default/%{name}



%pre
getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd -r -g %{_group} -d %{home_dir} -s /sbin/nologin \
    -c "%{name} user" %{_user}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
## Disable service if uninstall
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,%{_user},%{_group},-)
%{home_dir}/bin/mysqld_exporter

%attr(644, root, root)  %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{_group})      %{_sysconfdir}/default/%{name}


%changelog
* Wed Oct 14 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 0.12.1
- https://github.com/prometheus/mysqld_exporter/releases/tag/v0.12.1
