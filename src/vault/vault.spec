##
##
##
%define debug_package   %{nil}
%define __jar_repack    %{nil}


##
##
##
%define name        vault
%define version     1.6.2
%define release     %{rpm_release}.%{disttype}%{distnum}
%define conf_dir    %{_sysconfdir}/%{name}
%define work_dir    %{_sharedstatedir}/%{name}
%define log_dir     /var/log/%{name}

##
%define _user       vault
%define _group      vault



##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            A tool for secrets management, encryption as a service, and privileged access management.

Group:              Service/Security
License:            MPLv2.0
Vendor:             HashiCorp
URL:                https://www.vaultproject.io/
Packager:           Skywalker
Source0:            https://releases.hashicorp.com/vault/%{version}/vault_%{version}_linux_amd64.zip
Source1:            https://releases.hashicorp.com/vault/%{version}/vault_%{version}_SHA256SUMS
Source2:            vault.service
Source3:            vault.sysconfig
Source4:            server.hcl

BuildRequires:      systemd tar gzip
Requires(pre):      shadow-utils

%description
A tool for secrets management, encryption as a service, and privileged access management.
Please submit issues to https://github.com/hashicorp/vault/issues




%prep

%setup -q -c

%build
echo "Using pre-compiled Binaries"
pushd %{_sourcedir}
grep $(basename %{SOURCE0})  %{SOURCE1} | sha256sum -c
popd

%install

## Binary
mkdir -p %{buildroot}%{_bindir}/
cp -p %{name} %{buildroot}%{_bindir}/

## Working directory
mkdir -p %{buildroot}%{work_dir}

## SystemD Unit File
mkdir -p %{buildroot}%{_unitdir}
cp -p %{SOURCE2} %{buildroot}%{_unitdir}

## Sysconfig
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp -p %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

## Configuration
mkdir -p %{buildroot}%{conf_dir}
cp -p %{SOURCE4} %{buildroot}%{conf_dir}/server.hcl

## Logging Directory
mkdir -p %{buildroot}%{log_dir}


%clean
rm -rf %{buildroot}

%pre
getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd -r -g %{_group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    --system -c "%{name} user" %{_user}
exit 0


%post

## Set IPC_LOCK capabilities on vault
setcap cap_ipc_lock=+ep /usr/bin/vault

##
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service

%postun
if [ "$1" = "purge" ]; then
  getent passwd %{_user} >/dev/null && userdel %{_user}
  getent group %{_group} >/dev/null && groupdel %{_group}
fi


%systemd_postun_with_restart %{name}.service


%files
%defattr(-,%{_user},%{_group},-)
%caps(cap_ipc_lock=+ep) %attr(755, root, root) %{_bindir}/%{name}

## Configuration Directory
%dir %attr(-, %{name}, %{name}) %{conf_dir}
%config(noreplace) %attr(750, %{name}, %{name}) %{conf_dir}/server.hcl

## Work Directory
%dir %attr(750,%{name},%{name}) %{work_dir}

## Logging Directory
%dir %attr(750,%{name},%{name}) %{log_dir}

## SystemD
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(644, root, root)  %{_unitdir}/%{name}.service



%changelog
* Tue Jan 04 2021 Francisco Correia <fcorreia@users.noreply.github.com> - 1.6.2
- Initial package

