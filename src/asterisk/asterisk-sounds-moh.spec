%if 0%{?fedora}
%global sounds_dir %{_datadir}/asterisk/moh
%else
%global sounds_dir %{_sharedstatedir}/asterisk/moh
%endif



Name:           asterisk-sounds-moh
Version:        2.03
Release:        %{rpm_release}.%{disttype}%{distnum}
Summary:        Music on Hold sounds for Asterisk

License:        CC-BY-SA
URL:            http://www.asterisk.org/

Source0:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-alaw-%{version}.tar.gz
Source1:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-g722-%{version}.tar.gz
Source2:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-g729-%{version}.tar.gz
Source3:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-gsm-%{version}.tar.gz
Source4:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-siren7-%{version}.tar.gz
Source5:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-siren14-%{version}.tar.gz
Source6:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-sln16-%{version}.tar.gz
Source7:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-ulaw-%{version}.tar.gz
Source8:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-moh-opsound-wav-%{version}.tar.gz


BuildArch:      noarch

%description
Music on Hold sounds for Asterisk

%package alaw
Summary: Core English ALAW sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description alaw
Music on Hold ALAW sound files for Asterisk.

%package g722
Summary: Core English G.722 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description g722
Music on Hold G.722 sound files for Asterisk.

%package g729
Summary: Core English G.729 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description g729
Music on Hold G.729 sound files for Asterisk.

%package gsm
Summary: Core English GSM sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description gsm
Music on Hold GSM sound files for Asterisk.

%package siren7
Summary: Core English Siren7 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description siren7
Music on Hold Siren7 sound files for Asterisk.

%package siren14
Summary: Core English GSM sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description siren14
Music on Hold Siren14 sound files for Asterisk.

%package sln16
Summary: Core English SLN16 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description sln16
Music on Hold SLN16 sound files for Asterisk.

%package ulaw
Summary: Core English ULAW sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description ulaw
Music on Hold ULAW sound files for Asterisk.

%package wav
Summary: Core English WAV sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-moh = %{version}-%{release}

%description wav
Music on Hold WAV sound files for Asterisk.

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


%files alaw -f asterisk-moh-opsound-alaw-%{version}.list
%doc asterisk-moh-opsound-alaw-%{version}.list

%files g722 -f asterisk-moh-opsound-g722-%{version}.list
%doc asterisk-moh-opsound-g722-%{version}.list

%files g729 -f asterisk-moh-opsound-g729-%{version}.list
%doc asterisk-moh-opsound-g729-%{version}.list

%files gsm -f asterisk-moh-opsound-gsm-%{version}.list
%doc asterisk-moh-opsound-gsm-%{version}.list

%files siren7 -f asterisk-moh-opsound-siren7-%{version}.list
%doc asterisk-moh-opsound-siren7-%{version}.list

%files siren14 -f asterisk-moh-opsound-siren14-%{version}.list
%doc asterisk-moh-opsound-gsm-%{version}.list

%files sln16 -f asterisk-moh-opsound-sln16-%{version}.list
%doc asterisk-moh-opsound-sln16-%{version}.list

%files ulaw -f asterisk-moh-opsound-ulaw-%{version}.list
%doc asterisk-moh-opsound-ulaw-%{version}.list

%files wav -f asterisk-moh-opsound-wav-%{version}.list
%doc asterisk-moh-opsound-wav-%{version}.list


%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 2.03-1
- Initial Spec file

