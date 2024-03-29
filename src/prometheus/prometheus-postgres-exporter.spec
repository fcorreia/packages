##
## Spec file for managing prometheus postgresql exporter
##

%define debug_package   %{nil}
%define __jar_repack    %{nil}

%define distnum %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}
%define disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}

##
##
##
%define name        prometheus-postgres-exporter
%define version     0.10.1
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
Summary:            A PostgresSQL metric exporter for Prometheus

Group:              System Environment/Base
License:            APLv2.0
URL:                https://github.com/wrouesnel/postgres_exporter
Source0:            https://github.com/prometheus-community/postgres_exporter/releases/download/v%{version}/postgres_exporter-%{version}.linux-amd64.tar.gz
Source1:            %{name}.service
Source2:            %{name}.defaults

BuildRequires:      systemd tar gzip

Requires(pre):      shadow-utils

%description
Prometheus exporter for PostgreSQL server metrics. Supported Postgres
versions: 9.1 and up.

%prep
%setup -q -c %{SOURCE0}

%install


install -D  postgres_exporter-%{version}.linux-amd64/postgres_exporter    \
            %{buildroot}%{home_dir}/bin/postgres_exporter


install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/default/%{name}



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
%{home_dir}/bin/postgres_exporter

%attr(644, root, root)  %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{_group})  %{_sysconfdir}/default/%{name}


%changelog
* Wed Oct 14 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 0.8.0
- https://github.com/wrouesnel/postgres_exporter/releases/tag/v0.8.0

* Tue Jul 02 2019 Francisco Correia <fcorreia@users.noreply.github.com> - 0.4.7
 - Initial package
