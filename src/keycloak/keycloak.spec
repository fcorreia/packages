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
%define name        keycloak
%define version     %{rpm_version}
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    /opt/%{name}
%define work_dir    %{_sharedstatedir}/keycloak
##
%define _user       keycloak
%define _group      keycloak



##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Keycloak is an open source identity and access management solution.

Group:              System Environment/Base
License:            APLv2.0
URL:                http://www.keycloak.org/
Source0:            %{name}-%{version}.tar.gz
Source1:            https://downloads.jboss.org/%{name}/%{version}.Final/%{name}-%{version}.Final.tar.gz

BuildRequires:      systemd tar gzip

Requires(pre):      shadow-utils
Requires:           jre

%description
Keycloak is an open source Identity and Access Management solution aimed at
modern applications and services. It makes it easy to secure applications and
services with little to no code.

%prep
# curl -OL %{SOURCE0}
%setup -q

%build

pushd %{_builddir}/%{name}-%{version}
    tar -xzf %{_sourcedir}/%{name}-%{version}.Final.tar.gz
    mv %{name}-%{version}.Final   %{name}
popd

%install
mkdir -vp       %{buildroot}%{work_dir}/data
mkdir -vp       %{buildroot}/opt

mv    keycloak  %{buildroot}/opt

install -D  %{name}.service     %{buildroot}/%{_unitdir}/%{name}.service
install -D  %{name}.sysconfig   %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

mkdir -vp %{buildroot}/var/log/%{name}

pushd %{buildroot}%{home_dir}/standalone
  ln -s /var/log/%{name}  log
  ln -s %{work_dir}/data  data
popd


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
%{work_dir}
%dir /var/log/%{name}

%attr(644, root, root)  %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{_group}) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Wed Nov 22 2017 Francisco Correia <hello@brainvoid.pt>
- Initial package
