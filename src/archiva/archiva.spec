##
## Simple package to keep a local version of the software
##
%define debug_package   %{nil}
%define __jar_repack    %{nil}


##
##
##
%define name        archiva
%define version     2.2.5
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    /opt/%{name}
%define work_dir    %{_sharedstatedir}/archiva
##
%define _user       archiva
%define _group      archiva



##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Build Artifact Repository Manager
Group:              System Environment/Base
License:            APLv2.0
URL:                https://archiva.apache.org
Source0:            http://mirrors.up.pt/pub/apache/archiva/%{version}/binaries/apache-archiva-%{version}-bin.tar.gz
Source1:            https://www.apache.org/dist/archiva/%{version}/binaries/apache-archiva-%{version}-bin.tar.gz.sha512
Source2:            archiva.service
Source3:            archiva.sysconfig

BuildRequires:      systemd tar gzip
Requires(pre):      shadow-utils
AutoReqProv:        no

%description
Apache Archiva™ is an extensible repository management software that helps taking care of your own personal or
enterprise-wide build artifact repository. It is the perfect companion for build tools such as Maven, Continuum,
and ANT.

%prep
%setup -q -c

%build
echo "Using pre-compiled Binaries"
pushd %{_sourcedir}
grep $(basename %{SOURCE0})  %{SOURCE1} | sha512sum -c
popd


%install
mkdir -vp       %{buildroot}%{work_dir}/repositories
mkdir -vp       %{buildroot}%{_tmppath}/%{name}
mkdir -vp       %{buildroot}/opt

mv              apache-archiva-%{version} \
                %{buildroot}/opt/%{name}

install -D  %{SOURCE2}    %{buildroot}/%{_unitdir}/%{name}.service
install -D  %{SOURCE3}    %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

mkdir -vp %{buildroot}/var/log/%{name}

pushd %{buildroot}%{home_dir}
  ## Logs
  if [ -e logs ]; then rm -rf logs; fi
  ln -s /var/log/%{name}    logs

  ## Working directory
  ln -s %{work_dir}/repositories  repositories

  ## Temporary Folder
  if [ -e temp ]; then rm -rf temp; fi
  ln -s %{_tmppath}/%{name}  temp
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
## Disable service if uninstall
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,%{_user},%{_group},-)
%{home_dir}
%{work_dir}
%dir /var/log/%{name}
%dir %{_tmppath}/%{name}

## Configuration files
%config(noreplace) %{home_dir}/conf
%config(noreplace) %{home_dir}/contexts/archiva.xml

%attr(644, root, root)  %{_unitdir}/%{name}.service
%config(noreplace) %attr(640, root, %{_group}) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Wed Feb 17 2021 Francisco Correia <fcorreia@users.noreply.github.com> - 2.2.5-1
- Initial package
