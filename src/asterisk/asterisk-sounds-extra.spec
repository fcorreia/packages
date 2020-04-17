%if 0%{?fedora}
%global sounds_dir %{_datadir}/asterisk/sounds
%else
%global sounds_dir %{_sharedstatedir}/asterisk/sounds
%endif


Name:           asterisk-sounds-extra
Version:        1.5.2
Release:        %{rpm_release}.%{disttype}%{distnum}
Summary:        Extra sounds for Asterisk


License:        CC-BY-SA
URL:            http://www.asterisk.org/

Source0:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-alaw-%{version}.tar.gz
Source1:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-g722-%{version}.tar.gz
Source2:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-g729-%{version}.tar.gz
Source3:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-gsm-%{version}.tar.gz
Source4:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-siren7-%{version}.tar.gz
Source5:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-siren14-%{version}.tar.gz
Source6:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-sln16-%{version}.tar.gz
Source7:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-ulaw-%{version}.tar.gz
Source8:        http://downloads.asterisk.org/pub/telephony/sounds/releases/asterisk-extra-sounds-en-wav-%{version}.tar.gz


BuildArch:      noarch

%description
Extra sound files for Asterisk.

%package en-alaw
Summary: Extra English ALAW sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-alaw
Extra English ALAW sound files for Asterisk.

%package en-g722
Summary: Extra English G.722 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-g722
Extra English G.722 sound files for Asterisk.

%package en-g729
Summary: Extra English G.729 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-g729
Extra English G.729 sound files for Asterisk.

%package en-gsm
Summary: Extra English GSM sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-gsm
Extra English GSM sound files for Asterisk.

%package en-siren7
Summary: Extra English Siren7 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-siren7
Extra English Siren7 sound files for Asterisk.

%package en-siren14
Summary: Extra English GSM sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-siren14
Extra English Siren14 sound files for Asterisk.

%package en-sln16
Summary: Extra English SLN16 sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-sln16
Extra English SLN16 sound files for Asterisk.

%package en-ulaw
Summary: Extra English ULAW sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-ulaw
Extra English ULAW sound files for Asterisk.

%package en-wav
Summary: Extra English WAV sound files for Asterisk
Requires: asterisk >= 1.4.0
Provides: asterisk-sounds-core = %{version}-%{release}
Provides: asterisk-sounds-core-en = %{version}-%{release}

%description en-wav
Extra English WAV sound files for Asterisk.

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


%files en-alaw -f asterisk-extra-sounds-en-alaw-%{version}.list
%doc asterisk-extra-sounds-en-alaw-%{version}.list

%files en-g722 -f asterisk-extra-sounds-en-g722-%{version}.list
%doc asterisk-extra-sounds-en-g722-%{version}.list

%files en-g729 -f asterisk-extra-sounds-en-g729-%{version}.list
%doc asterisk-extra-sounds-en-g729-%{version}.list

%files en-gsm -f asterisk-extra-sounds-en-gsm-%{version}.list
%doc asterisk-extra-sounds-en-gsm-%{version}.list

%files en-siren7 -f asterisk-extra-sounds-en-siren7-%{version}.list
%doc asterisk-extra-sounds-en-siren7-%{version}.list

%files en-siren14 -f asterisk-extra-sounds-en-siren14-%{version}.list
%doc asterisk-extra-sounds-en-gsm-%{version}.list

%files en-sln16 -f asterisk-extra-sounds-en-sln16-%{version}.list
%doc asterisk-extra-sounds-en-sln16-%{version}.list

%files en-ulaw -f asterisk-extra-sounds-en-ulaw-%{version}.list
%doc asterisk-extra-sounds-en-ulaw-%{version}.list

%files en-wav -f asterisk-extra-sounds-en-wav-%{version}.list
%doc asterisk-extra-sounds-en-wav-%{version}.list


%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.5.2-1
- Initial Spec file

