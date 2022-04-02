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
%define name        prometheus-alertmanager
%define version     0.24.0
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    /opt/prometheus
%define work_dir    %{_sharedstatedir}/prometheus/alertmanager

##
%define _user       alertmanager
%define _group      prometheus



##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Prometheus Alertmanager

Group:              System Environment/Base
License:            APLv2.0
URL:                https://github.com/prometheus/alertmanager
Source0:            https://github.com/prometheus/alertmanager/releases/download/v%{version}/alertmanager-%{version}.linux-amd64.tar.gz
Source1:            %{name}.service
Source2:            %{name}.defaults

BuildRequires:      systemd tar gzip

Requires(pre):      shadow-utils

%description
The Alertmanager handles alerts sent by client applications such as the Prometheus
server. It takes care of deduplicating, grouping, and routing them to the correct
receiver integrations such as email, PagerDuty, or OpsGenie. It also takes care of
silencing and inhibition of alerts.

%prep
%setup -q -c %{SOURCE0}

%install

mkdir -vp       %{buildroot}%{home_dir}/bin
mkdir -vp       %{buildroot}%{work_dir}
mkdir -vp       %{buildroot}%{_sysconfdir}/prometheus

install -D  alertmanager-%{version}.linux-amd64/alertmanager      \
            %{buildroot}%{home_dir}/bin/alertmanager
install -D  alertmanager-%{version}.linux-amd64/amtool            \
            %{buildroot}%{home_dir}/bin/amtool
install -D  alertmanager-%{version}.linux-amd64/alertmanager.yml  \
            %{buildroot}%{_sysconfdir}/prometheus/alertmanager.yml

install -D -p -m 0644 %{SOURCE1}    %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2}    %{buildroot}/%{_sysconfdir}/default/%{name}



%pre
getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd -r -g %{_group} -d %{work_dir} -s /sbin/nologin \
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
%{home_dir}/bin/alertmanager
%{home_dir}/bin/amtool

%defattr(-,%{_user},%{_group},750)
%dir %{work_dir}

%attr(644, root, root)  %{_unitdir}/%{name}.service

%config(noreplace) %attr(640, root, %{_group})      %{_sysconfdir}/default/%{name}
%config(noreplace) %attr(640, %{_user}, %{_group})  %{_sysconfdir}/prometheus/alertmanager.yml


%changelog
* Wed Oct 14 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 0.21.0
- https://github.com/prometheus/alertmanager/releases/tag/v0.21.0
