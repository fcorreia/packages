##
##
%define debug_package   %{nil}
%define __jar_repack    %{nil}

##
##
##
%define name        activemq-artemis
%define version     2.17.0
%define release     %{rpm_release}.%{disttype}%{distnum}
%define home_dir    /opt/%{name}
%define work_dir    %{_sharedstatedir}/%{name}
%define conf_dir    %{_sysconfdir}/%{name}

##
%define _user       artemis
%define _group      artemis


##
## Package Metadata
##
Name:               %{name}
Version:            %{version}
Release:            %{release}
Summary:            Apache ActiveMQ Artemis messaging service

Group:              System Environment/Base
License:            APLv2.0
URL:                http://activemq.apache.org/artemis/
Source0:            https://www.apache.org/dyn/closer.cgi?action=download&filename=activemq/activemq-artemis/%{version}/apache-artemis-%{version}-bin.tar.gz
Source1:            https://www.apache.org/dist/activemq/activemq-artemis/%{version}/apache-artemis-%{version}-bin.tar.gz.sha512
Source2:            activemq-artemis.service


BuildRequires:      systemd tar gzip coreutils

Requires(pre):      shadow-utils
Requires:           jre >= 1.7
Requires:           libaio

Provides:           activemq-artemis-server
Provides:           artemis-server
Provides:           activemq-server
Provides:           activemq



%description
Apache ActiveMQ Artemis has a proven non blocking architecture. It delivers outstanding performance.

%prep
%setup -q -c


%build
echo "Using pre-compiled Binaries"
pushd %{_sourcedir}
grep $(basename %{SOURCE0})  %{SOURCE1} | sha512sum -c
popd


%install
mkdir -vp   %{buildroot}/opt
mv          apache-artemis-%{version}   %{buildroot}/%{home_dir}

mkdir -vp   %{buildroot}%{work_dir}
mkdir -vp   %{buildroot}%{conf_dir}

## Remove examples and README
rm -rf  %{buildroot}%{home_dir}/examples
rm -rf  %{buildroot}%{home_dir}/README.html

## Symbolic links
pushd %{buildroot}%{work_dir}
    ## remove folders before linking
    if [ -e log ]; then rm -rf log; fi
    if [ -e tmp ]; then rm -rf tmp; fi

    mkdir -vp %{buildroot}/var/log/%{name}
    ln -s /var/log/%{name}    log

    mkdir -vp %{buildroot}/var/tmp/%{name}
    ln -s /var/tmp/%{name}    tmp
popd

install -D  %{SOURCE2}  %{buildroot}/%{_unitdir}/%{name}.service



%pre
getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd --system --no-create-home -g %{_group} -d %{home_dir} -s /sbin/nologin \
    -c "%{name} user" %{_user}
exit 0

%post
%systemd_post %{name}.service

## Sample Initial Configuration
if [ ! -e "%{work_dir}/bin/artemis" ]; then
    echo "Configuration not found, Initialize"
    %{home_dir}/bin/artemis create --allow-anonymous  --autocreate  \
    --home %{home_dir} --data %{work_dir}/data  --etc %{conf_dir} \
    --user admin --password admin %{work_dir}
fi

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
%dir %{home_dir}
%dir /var/log/%{name}
%dir %{work_dir}
%{work_dir}/log
%{work_dir}/tmp
%dir /var/tmp/%{name}
%dir %{conf_dir}
%attr(644, root, root)  %{_unitdir}/%{name}.service

%changelog
* Wed Feb 17 2021 Francisco Correia <fcorreia@users.noreply.github.com> - 2.17.0
- Initial package
