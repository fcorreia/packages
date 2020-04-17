%if 0%{?fedora}
%global sounds_dir %{_datadir}/asterisk/sounds
%else
%global sounds_dir %{_sharedstatedir}/asterisk/sounds
%endif


Name:           asterisk-sounds-core
Version:        1.6.1
Release:        %{rpm_release}.%{disttype}%{distnum}
Summary:        Core sounds for Asterisk


License:        CC-BY-SA
URL:            http://www.asterisk.org/

Source0:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-alaw-%{version}.tar.gz
Source1:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-g722-%{version}.tar.gz
Source2:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-g729-%{version}.tar.gz
Source3:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-gsm-%{version}.tar.gz
Source4:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-siren7-%{version}.tar.gz
Source5:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-siren14-%{version}.tar.gz
Source6:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-sln16-%{version}.tar.gz
Source7:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-ulaw-%{version}.tar.gz
Source8:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-core-sounds-en-wav-%{version}.tar.gz


BuildArch:      noarch

%description
Core sound files for Asterisk.

%package en
Summary: Core English sound files for Asterisk
Requires: asterisk >= 1.4.0

%description en
Core English sound files for Asterisk.

%package en-alaw
Summary: Core English ALAW sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-alaw
Core English ALAW sound files for Asterisk.

%package en-g722
Summary: Core English G.722 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-g722
Core English G.722 sound files for Asterisk.

%package en-g729
Summary: Core English G.729 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-g729
Core English G.729 sound files for Asterisk.

%package en-gsm
Summary: Core English GSM sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-gsm
Core English GSM sound files for Asterisk.

%package en-siren7
Summary: Core English Siren7 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-siren7
Core English Siren7 sound files for Asterisk.

%package en-siren14
Summary: Core English GSM sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-siren14
Core English Siren14 sound files for Asterisk.

%package en-sln16
Summary: Core English SLN16 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-sln16
Core English SLN16 sound files for Asterisk.

%package en-ulaw
Summary: Core English ULAW sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-ulaw
Core English ULAW sound files for Asterisk.

%package en-wav
Summary: Core English WAV sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core-en = %{version}-%{release}
Provides: asterisk-sounds-core = %{version}-%{release}

%description en-wav
Core English WAV sound files for Asterisk.

%prep

%setup -c -T

%build

for file in %{S:0} %{S:1} %{S:2} %{S:3} %{S:4} %{S:5} %{S:6} %{S:7} %{S:8}
do
  tar --list --file $file | grep -E '.(alaw|g722|g729|gsm|siren7|siren14|sln16|ulaw|wav)$' | sed -e 's!^!%{sounds_dir}/!' > `basename $file .tar.gz`.list
  tar --extract --directory . --file $file
done

%install
rm -rf %{buildroot}

for file in `cat *.list | sed -e 's!^%{sounds_dir}/!!'`
do
  mkdir -p %{buildroot}%{sounds_dir}/`dirname $file`
  cp -p $file %{buildroot}%{sounds_dir}/$file
done


%files en-alaw -f asterisk-core-sounds-en-alaw-%{version}.list
%doc asterisk-core-sounds-en-alaw-%{version}.list

%files en-g722 -f asterisk-core-sounds-en-g722-%{version}.list
%doc asterisk-core-sounds-en-g722-%{version}.list

%files en-g729 -f asterisk-core-sounds-en-g729-%{version}.list
%doc asterisk-core-sounds-en-g729-%{version}.list

%files en-gsm -f asterisk-core-sounds-en-gsm-%{version}.list
%doc asterisk-core-sounds-en-gsm-%{version}.list

%files en-siren7 -f asterisk-core-sounds-en-siren7-%{version}.list
%doc asterisk-core-sounds-en-siren7-%{version}.list

%files en-siren14 -f asterisk-core-sounds-en-siren14-%{version}.list
%doc asterisk-core-sounds-en-gsm-%{version}.list

%files en-sln16 -f asterisk-core-sounds-en-sln16-%{version}.list
%doc asterisk-core-sounds-en-sln16-%{version}.list

%files en-ulaw -f asterisk-core-sounds-en-ulaw-%{version}.list
%doc asterisk-core-sounds-en-ulaw-%{version}.list

%files en-wav -f asterisk-core-sounds-en-wav-%{version}.list
%doc asterisk-core-sounds-en-wav-%{version}.list


%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.6.1-1
- Initial Spec file from Fedora project: https://src.fedoraproject.org/rpms/asterisk-sounds-core.git

