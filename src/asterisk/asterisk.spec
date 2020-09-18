
##
%define _user       asterisk
%define _group      asterisk


%global           pjsip_version   2.9
%global           jansson_version 2.12

%global           optflags        %{optflags} -Werror-implicit-function-declaration -DLUA_COMPAT_MODULE -fPIC
%ifarch s390 %{arm} aarch64 %{mips}
%global           ldflags         -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags}
%else
%global           ldflags         -m%{__isa_bits} -Wl,--as-needed,--library-path=%{_libdir} %{__global_ldflags}
%endif

%global           astvarrundir     /run/asterisk
%if 0%{?fedora}
%global           astdatadir      %{_datadir}
%global           astvarlibdir    %{_datadir}
%else
%global           astdatadir      %{_sharedstatedir}
%global           astvarlibdir    %{_sharedstatedir}
%endif

%global           makeargs        DEBUG= OPTIMIZE= DESTDIR=%{buildroot} ASTVARRUNDIR=%{astvarrundir} ASTDATADIR=%{astdatadir}/asterisk ASTVARLIBDIR=%{astvarlibdir}/asterisk ASTDBDIR=%{_localstatedir}/spool/asterisk NOISY_BUILD=1

%global           tmpfilesd        1

## Build individual packages for the following group
%global           apidoc     0
%global           mysql      1
%global           odbc       1
%global           postgresql 1
%global           radius     1
%global           snmp       1
%global           misdn      0
%global           ldap       1
%global           gmime      1
%global           corosync   1
%if 0%{?fedora} >= 21 || 0%{?rhel} >=7
%global           jack       0
%else
%global           jack       1
%endif
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 7
%global           phone      0
%global           xmpp       0
%else
%global           phone      1
%global           xmpp       1
%endif
%global           meetme     0
%global           ooh323     0


## Building options, things to include in the package
%global           ext_mp3    1
%global           lib_nbs    1


Summary:	Asterisk, The Open Source PBX
Name:		asterisk
Version:    16.13.0
Release:    %{rpm_release}.%{disttype}%{distnum}
License:	GPL v2
Group:		Applications/System
URL:		http://www.asterisk.org/


Source0:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}.tar.gz
Source1:          http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}.tar.gz.asc
Source2:          asterisk-logrotate
Source3:          menuselect.makedeps
Source4:          menuselect.makeopts
Source5:          asterisk.service
Source6:          asterisk-tmpfiles
# GPG keyring with Asterisk developer signatures
# Created by running:
#gpg2 --no-default-keyring --keyring ./asterisk-gpgkeys.gpg \
#--keyserver=hkp://pool.sks-keyservers.net --recv-keys \
#0x21A91EB1F012252993E9BF4A368AB332B59975F3 \
#0x80CEBC345EC9FF529B4B7B808438CBA18D0CAA72 \
#0xCDBEE4CC699E200EB4D46BB79E76E3A42341CE04 \
#0x639D932D5170532F8C200CCD9C59F000777DCC45 \
#0x551F29104B2106080C6C2851073B0C1FC9B2E352 \
#0x57E769BC37906C091E7F641F6CB44E557BD982D8 \
#0x0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD \
#0xF2FC93DB7587BD1FB49E045A5D984BE337191CE7
Source7:          asterisk-gpgkeys.gpg

# Now building Asterisk with bundled pjproject, because they apply custom patches to it
Source8:          https://raw.githubusercontent.com/asterisk/third-party/master/pjproject/%{pjsip_version}/pjproject-%{pjsip_version}.tar.bz2

# Bundling jansson on EL7 and EL8, because the version in CentOS is too old
Source9:          http://www.digip.org/jansson/releases/jansson-%{jansson_version}.tar.bz2

%if 0%{?fedora} || 0%{?rhel} >= 8
Patch0:           asterisk-mariadb.patch
%endif

%if 0%{?fedora} || 0%{?rhel} >=7
Patch1:           asterisk-16.1.0-explicit-python3.patch
%endif

# Asterisk now builds against a bundled copy of pjproject, as they apply some patches
# directly to pjproject before the build against it
Provides:         bundled(pjproject) = %{pjsip_version}

# Does not build on s390x: https://bugzilla.redhat.com/show_bug.cgi?id=1465162
ExcludeArch:      s390x


# Required Tools
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    perl

# Essential Libraries
BuildRequires:  jansson-devel
BuildRequires:  sqlite-devel >= 3
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  uuid-devel

# core build requirements
BuildRequires:    openssl-devel
BuildRequires:    newt-devel
BuildRequires:    ncurses-devel
BuildRequires:    libcap-devel
%if 0%{?gmime}
BuildRequires:    gtk2-devel
%endif
BuildRequires:    libsrtp-devel >= 1.5.4
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
BuildRequires:    popt-devel
%{?systemd_requires}
BuildRequires:    systemd
BuildRequires:    kernel-headers

# for res_http_post
%if 0%{?gmime}
BuildRequires:    gmime-devel
%endif

# for building docs
BuildRequires:    doxygen
BuildRequires:    graphviz
BuildRequires:    libxml2-devel
BuildRequires:    latex2html

# for building res_calendar_caldav
BuildRequires:    neon-devel
BuildRequires:    libical-devel
BuildRequires:    libxml2-devel

# for codec_speex
BuildRequires:    speex-devel >= 1.2
%if (0%{?fedora} > 21 || 0%{?rhel} > 7)
BuildRequires:    speexdsp-devel >= 1.2
%endif


# for format_ogg_vorbis
BuildRequires:    libogg-devel
BuildRequires:    libvorbis-devel

# codec_gsm
BuildRequires:    gsm-devel

# additional dependencies
BuildRequires:    SDL-devel
BuildRequires:    SDL_image-devel

# cli
BuildRequires:    libedit-devel

# codec_ilbc
BuildRequires:    ilbc-devel

# res_rtp_asterisk
BuildRequires:    libuuid-devel

%if 0%{?corosync}
BuildRequires:    corosynclib-devel
%endif

BuildRequires:    alsa-lib-devel
BuildRequires:    libcurl-devel
BuildRequires:    dahdi-tools-devel >= 2.0.0
BuildRequires:    dahdi-tools-libs >= 2.0.0
BuildRequires:    libpri-devel >= 1.6.0
BuildRequires:    libss7-devel >= 2.0.0
BuildRequires:    spandsp-devel >= 0.0.5-0.1.pre4
BuildRequires:    libtiff-devel
BuildRequires:    libjpeg-turbo-devel
BuildRequires:    lua-devel
%if 0%{?jack}
BuildRequires:    jack-audio-connection-kit-devel
%endif
BuildRequires:    libresample-devel => 0.1.3
BuildRequires:    bluez-libs-devel
BuildRequires:    libtool-ltdl-devel
BuildRequires:    portaudio-devel >= 19
BuildRequires:    sqlite-devel
BuildRequires:    freetds-devel

%if 0%{?misdn}
BuildRequires:    mISDN-devel
%endif

%if 0%{?ldap}
BuildRequires:    openldap-devel
%endif

%if 0%{?mysql}
%if 0%{?rhel} >= 7
BuildRequires:    mariadb-devel
%else
BuildRequires:    mariadb-connector-c-devel
%endif
%endif

%if 0%{?odbc}
BuildRequires:    libtool-ltdl-devel
BuildRequires:    unixODBC-devel
%endif

%if 0%{?postgresql}
%if 0%{?rhel}
BuildRequires:    postgresql-devel
%else
BuildRequires:    libpq-devel
%endif
%endif

%if 0%{?radius}
%if 0%{?fedora} || 0%{?rhel} < 7
BuildRequires:    freeradius-client-devel
%else
BuildRequires:    radcli-compat-devel
%endif
%endif

%if 0%{?snmp}
BuildRequires:    net-snmp-devel
BuildRequires:    lm_sensors-devel
%endif

BuildRequires:    uw-imap-devel

%if 0%{?fedora}
BuildRequires:    jansson-devel
%else
Provides:         bundled(jansson) = 2.11
%endif


# Essential Libraries
Requires: libxml2
Requires: libxslt
Requires: ncurses
Requires: openssl
Requires: uuid

# Core Libraries
## libsrtp >= 1.5.4
Requires: libsrtp >= 1.5.4
Requires: sqlite >= 3


Requires(pre):    shadow-utils
Requires(post):   systemd-units
Requires(post):   systemd-sysv
Requires(preun):  systemd-units
Requires(postun): systemd-units


Provides:	group(asterisk)
Provides:	user(asterisk)


Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
Asterisk is an open source framework for building communications applications.
Asterisk turns an ordinary computer into a communications server. Asterisk
powers IP PBX systems, VoIP gateways, conference servers and other custom
solutions. It is used by small businesses, large businesses, call centers,
carriers and government agencies, worldwide. Asterisk is free and open source.
Asterisk is sponsored by Digium.

Today, there are more than one million Asterisk-based communications systems
in use, in more than 170 countries. Asterisk is used by almost the entire
Fortune 1000 list of customers. Most often deployed by system integrators
and developers, Asterisk can become the basis for a complete business phone
system, or used to enhance or extend an existing system, or to bridge a
gap between systems.


%package ael
Summary: AEL (Asterisk Extension Logic) modules for Asterisk
Requires: asterisk = %{version}-%{release}

%description ael
AEL (Asterisk Extension Logic) mdoules for Asterisk

%package alsa
Summary: Modules for Asterisk that use Alsa sound drivers
Requires: asterisk = %{version}-%{release}

%package alembic
Summary: Alembic scripts for the Asterisk DB (realtime)
Requires: asterisk = %{version}-%{release}

%description alembic
Alembic scripts for the Asterisk DB


%description alsa
Modules for Asterisk that use Alsa sound drivers.

%if 0%{?apidoc}
%package apidoc
Summary: API documentation for Asterisk
Requires: asterisk = %{version}-%{release}

%description apidoc
API documentation for Asterisk.
%endif

%package calendar
Summary: Calendar applications for Asterisk
Requires: asterisk = %{version}-%{release}

%description calendar
Calendar applications for Asterisk.

%if 0%{?corosync}
%package corosync
Summary: Modules for Asterisk that use Corosync
Requires: asterisk = %{version}-%{release}

%description corosync
Modules for Asterisk that use Corosync.
%endif

%package curl
Summary: Modules for Asterisk that use cURL
Requires: asterisk = %{version}-%{release}

%description curl
Modules for Asterisk that use cURL.

%package dahdi
Summary: Modules for Asterisk that use DAHDI
Requires: asterisk = %{version}-%{release}
Requires: dahdi-tools >= 2.0.0
Requires(pre): %{_sbindir}/usermod
Provides: asterisk-zaptel = %{version}-%{release}

%description dahdi
Modules for Asterisk that use DAHDI.

%package devel
Summary: Development files for Asterisk
Requires: asterisk = %{version}-%{release}

%description devel
Development files for Asterisk.

%package fax
Summary: FAX applications for Asterisk
Requires: asterisk = %{version}-%{release}

%description fax
FAX applications for Asterisk

%package festival
Summary: Festival application for Asterisk
Requires: asterisk = %{version}-%{release}
Requires: festival

%description festival
Application for the Asterisk PBX that uses Festival to convert text to speech.

%package iax2
Summary: IAX2 channel driver for Asterisk
Requires: asterisk = %{version}-%{release}

%description iax2
IAX2 channel driver for Asterisk

%package hep
Summary: Modules for capturing SIP traffic using Homer (HEPv3)
Requires: asterisk = %{version}-%{release}

%description hep
Modules for capturing SIP traffic using Homer (HEPv3)

%package ices
Summary: Stream audio from Asterisk to an IceCast server
Requires: asterisk = %{version}-%{release}
Requires: ices

%description ices
Stream audio from Asterisk to an IceCast server.

%if 0%{?jack}
%package jack
Summary: JACK resources for Asterisk
Requires: asterisk = %{version}-%{release}

%description jack
JACK resources for Asterisk.
%endif

%package lua
Summary: Lua resources for Asterisk
Requires: asterisk = %{version}-%{release}

%description lua
Lua resources for Asterisk.

%if 0%{?ldap}
%package ldap
Summary: LDAP resources for Asterisk
Requires: asterisk = %{version}-%{release}

%description ldap
LDAP resources for Asterisk.
%endif

%if 0%{?misdn}
%package misdn
Summary: mISDN channel for Asterisk
Requires: asterisk = %{version}-%{release}
Requires(pre): %{_sbindir}/usermod

%description misdn
mISDN channel for Asterisk.
%endif

%package mgcp
Summary: MGCP channel driver for Asterisk
Requires: asterisk = %{version}-%{release}

%description mgcp
MGCP channel driver for Asterisk

%package mobile
Summary: Mobile (BlueTooth) channel for Asterisk
Requires: asterisk = %{version}-%{release}
Requires(pre): %{_sbindir}/usermod

%description mobile
Mobile (BlueTooth) channel for Asterisk.

%package minivm
Summary: MiniVM applicaton for Asterisk
Requires: asterisk = %{version}-%{release}

%description minivm
MiniVM application for Asterisk.

%package mwi-external
Summary: Support for developing external voicemail applications
Requires: asterisk = %{version}-%{release}
Conflicts: asterisk-voicemail = %{version}-%{release}
Conflicts: asterisk-voicemail-implementation = %{version}-%{release}

%description mwi-external
Support for developing external voicemail applications

%if 0%{?mysql}
%package mysql
Summary: Applications for Asterisk that use MySQL
Requires: asterisk = %{version}-%{release}

%description mysql
Applications for Asterisk that use MySQL.
%endif

%if 0%{?odbc}
%package odbc
Summary: Applications for Asterisk that use ODBC (except voicemail)
Requires: asterisk = %{version}-%{release}

%description odbc
Applications for Asterisk that use ODBC (except voicemail)
%endif

%if 0%{?ooh323}
%package ooh323
Summary: H.323 channel for Asterisk using the Objective Systems Open H.323 for C library
Requires: asterisk = %{version}-%{release}

%description ooh323
H.323 channel for Asterisk using the Objective Systems Open H.323 for C library.
%endif

%package oss
Summary: Modules for Asterisk that use OSS sound drivers
Requires: asterisk = %{version}-%{release}

%description oss
Modules for Asterisk that use OSS sound drivers.

%package phone
Summary: Channel driver for Quicknet Technologies, Inc.'s Telephony cards
Requires: asterisk = %{version}-%{release}

%description phone
Quicknet Technologies, Inc.'s Telephony cards including the Internet
PhoneJACK, Internet PhoneJACK Lite, Internet PhoneJACK PCI, Internet
LineJACK, Internet PhoneCARD and SmartCABLE.

%package pjsip
Summary: SIP channel based upon the PJSIP library
Requires: asterisk = %{version}-%{release}

%description pjsip
SIP channel based upon the PJSIP library

%package portaudio
Summary: Modules for Asterisk that use the portaudio library
Requires: asterisk = %{version}-%{release}

%description portaudio
Modules for Asterisk that use the portaudio library.

%if 0%{?postgresql}
%package postgresql
Summary: Applications for Asterisk that use PostgreSQL
Requires: asterisk = %{version}-%{release}

%description postgresql
Applications for Asterisk that use PostgreSQL.
%endif

%if 0%{?radius}
%package radius
Summary: Applications for Asterisk that use RADIUS
Requires: asterisk = %{version}-%{release}

%description radius
Applications for Asterisk that use RADIUS.
%endif

%package skinny
Summary: Modules for Asterisk that support the SCCP/Skinny protocol
Requires: asterisk = %{version}-%{release}

%description skinny
Modules for Asterisk that support the SCCP/Skinny protocol.

%package sip
Summary: Legacy SIP channel driver for Asterisk
Requires: asterisk = %{version}-%{release}

%description sip
Legacy SIP channel driver for Asterisk

%if 0%{?snmp}
%package snmp
Summary: Module that enables SNMP monitoring of Asterisk
Requires: asterisk = %{version}-%{release}
# This subpackage depends on perl-libs, this Requires tracks versioning.
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description snmp
Module that enables SNMP monitoring of Asterisk.
%endif

%package sqlite
Summary: Sqlite modules for Asterisk
Requires: asterisk = %{version}-%{release}
#? Require: sqlite

%description sqlite
Sqlite modules for Asterisk.

%package tds
Summary: Modules for Asterisk that use FreeTDS
Requires: asterisk = %{version}-%{release}

%description tds
Modules for Asterisk that use FreeTDS.

%package unistim
Summary: Unistim channel for Asterisk
Requires: asterisk = %{version}-%{release}

%description unistim
Unistim channel for Asterisk

%package voicemail
Summary: Common Voicemail Modules for Asterisk
Requires: asterisk = %{version}-%{release}
Requires: asterisk-voicemail-implementation = %{version}-%{release}
Requires: /usr/bin/sox
Requires: /usr/sbin/sendmail
Conflicts: asterisk-mwi-external <= %{version}-%{release}

%description voicemail
Common Voicemail Modules for Asterisk.

%package voicemail-imap
Summary: Store voicemail on an IMAP server
Requires: asterisk = %{version}-%{release}
Requires: asterisk-voicemail = %{version}-%{release}
Provides: asterisk-voicemail-implementation = %{version}-%{release}
Conflicts: asterisk-voicemail-odbc <= %{version}-%{release}
Conflicts: asterisk-voicemail-plain <= %{version}-%{release}

%description voicemail-imap
Voicemail implementation for Asterisk that stores voicemail on an IMAP
server.

%package voicemail-odbc
Summary: Store voicemail in a database using ODBC
Requires: asterisk = %{version}-%{release}
Requires: asterisk-voicemail = %{version}-%{release}
Provides: asterisk-voicemail-implementation = %{version}-%{release}
Conflicts: asterisk-voicemail-imap <= %{version}-%{release}
Conflicts: asterisk-voicemail-plain <= %{version}-%{release}

%description voicemail-odbc
Voicemail implementation for Asterisk that uses ODBC to store
voicemail in a database.

%package voicemail-plain
Summary: Store voicemail on the local filesystem
Requires: asterisk = %{version}-%{release}
Requires: asterisk-voicemail = %{version}-%{release}
Provides: asterisk-voicemail-implementation = %{version}-%{release}
Conflicts: asterisk-voicemail-imap <= %{version}-%{release}
Conflicts: asterisk-voicemail-odbc <= %{version}-%{release}

%description voicemail-plain
Voicemail implementation for Asterisk that stores voicemail on the
local filesystem.

%if 0%{?xmpp}
%package xmpp
Summary: Jabber/XMPP resources for Asterisk
Requires: asterisk = %{version}-%{release}

%description xmpp
Jabber/XMPP resources for Asterisk.
%endif

%prep
%if 0%{?fedora} || 0%{?rhel} >=8
# only verifying on Fedora and RHEL >=8 due to version of gpg
gpgv2 --keyring %{SOURCE7} %{SOURCE1} %{SOURCE0}
%endif
%setup -q -n asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}


# copy the pjproject tarball to the cache/ directory
mkdir cache
cp %{SOURCE8} cache/

%if 0%{?rhel} >= 7
cp %{SOURCE9} cache/
%endif

echo '*************************************************************************'
ls -altr cache/
pwd
echo '*************************************************************************'

%if 0%{?fedora} || 0%{?rhel} >=8
%patch0 -p1
%endif

%if 0%{?fedora} || 0%{?rhel} >=7
%patch1 -p1
%endif

cp %{S:3} menuselect.makedeps
cp %{S:4} menuselect.makeopts



# Fixup makefile so sound archives aren't downloaded/installed
%{__perl} -pi -e 's/^all:.*$/all:/' sounds/Makefile
%{__perl} -pi -e 's/^install:.*$/install:/' sounds/Makefile

# convert comments in one file to UTF-8
mv main/fskmodem.c main/fskmodem.c.old
iconv -f iso-8859-1 -t utf-8 -o main/fskmodem.c main/fskmodem.c.old
touch -r main/fskmodem.c.old main/fskmodem.c
rm main/fskmodem.c.old

chmod -x contrib/scripts/dbsep.cgi

%if ! 0%{?corosync}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_corosync/g' menuselect.makeopts
%endif

%if ! 0%{?mysql}
%{__perl} -pi -e 's/^MENUSELECT_ADDONS=(.*)$/MENUSELECT_ADDONS=\1 res_config_mysql app_mysql cdr_mysql/g' menuselect.makeopts
%endif

%if ! 0%{?postgresql}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_config_pgsql/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CDR=(.*)$/MENUSELECT_CDR=\1 cdr_pgsql/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CEL=(.*)$/MENUSELECT_CEL=\1 cel_pgsql/g' menuselect.makeopts
%endif

%if ! 0%{?radius}
%{__perl} -pi -e 's/^MENUSELECT_CDR=(.*)$/MENUSELECT_CDR=\1 cdr_radius/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CEL=(.*)$/MENUSELECT_CEL=\1 cel_radius/g' menuselect.makeopts
%endif

%if ! 0%{?snmp}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_snmp/g' menuselect.makeopts
%endif

%if ! 0%{?misdn}
%{__perl} -pi -e 's/^MENUSELECT_CHANNELS=(.*)$/MENUSELECT_CHANNELS=\1 chan_misdn/g' menuselect.makeopts
%endif

%if ! 0%{?jack}
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_jack/g' menuselect.makeopts
%endif

%if ! 0%{?ldap}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_config_ldap/g' menuselect.makeopts
%endif

%if ! 0%{?gmime}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_http_post/g' menuselect.makeopts
%endif

%if ! 0%{xmpp}
%{__perl} -pi -e 's/^MENUSELECT_RES=(.*)$/MENUSELECT_RES=\1 res_xmpp/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_CHANNELS=(.*)$/MENUSELECT_CHANNELS=\1 chan_motif/g' menuselect.makeopts
%endif

%if ! 0%{meetme}
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_meetme/g' menuselect.makeopts
%{__perl} -pi -e 's/^MENUSELECT_APPS=(.*)$/MENUSELECT_APPS=\1 app_page/g' menuselect.makeopts
%endif

%if ! 0%{ooh323}
%{__perl} -pi -e 's/^MENUSELECT_ADDONS=(.*)$/MENUSELECT_ADDONS=\1 chan_ooh323/g' menuselect.makeopts
%endif

## Options to include in the build
%if 0%{ext_mp3}
cat menuselect.makeopts
contrib/scripts/get_mp3_source.sh
%endif

%if 0%{lib_nbs}
svn export http://svn.digium.com/svn/nbs/trunk nbs-trunk
%endif


%build

%if 0%{lib_nbs}
pushd nbs-trunk
make all install
popd
%endif

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS=" "

%if 0%{?fedora}
sed -i '1s/env python/python3/' contrib/scripts/refcounter.py
%endif

#aclocal -I autoconf --force
#autoconf --force
#autoheader --force
./bootstrap.sh

pushd menuselect
%configure
popd


echo "*******************************************************************************"
cat menuselect.makeopts
echo "*******************************************************************************"

## Generic configuration, assuming always above or equal centOS 7
%configure --with-imap=system --with-gsm=/usr --with-ilbc=/usr --with-libedit=yes --with-srtp --with-jansson-bundled --with-pjproject-bundled --with-externals-cache=%{_builddir}/asterisk-%{version}%{?_rc:-rc%{_rc}}%{?_beta:-beta%{_beta}}/cache LDFLAGS="%{ldflags}" NOISY_BUILD=1 CPPFLAGS="-fPIC"

%make_build menuselect-tree NOISY_BUILD=1
%{__perl} -n -i -e 'print unless /openr2/i' menuselect-tree


# Build with plain voicemail and directory
echo "### Building with plain voicemail and directory"
%make_build %{makeargs}

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_plain.so
mv apps/app_directory.so apps/app_directory_plain.so

# Now build with IMAP storage for voicemail and directory
sed -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=IMAP_STORAGE/' menuselect.makeopts

echo "### Building with IMAP voicemail and directory"
%make_build %{makeargs}

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_imap.so
mv apps/app_directory.so apps/app_directory_imap.so

# Now build with ODBC storage for voicemail and directory

sed -i -e 's/^MENUSELECT_OPTS_app_voicemail=.*$/MENUSELECT_OPTS_app_voicemail=ODBC_STORAGE/' menuselect.makeopts
echo "### Building with ODBC voicemail and directory"
%make_build %{makeargs}

rm apps/app_voicemail.o apps/app_directory.o
mv apps/app_voicemail.so apps/app_voicemail_odbc.so
mv apps/app_directory.so apps/app_directory_odbc.so

# so that these modules don't get built again
touch apps/app_voicemail.o apps/app_directory.o
touch apps/app_voicemail.so apps/app_directory.so

sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_mwi_external\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_mwi_external_ami\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_stasis_mailbox\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_RES=\(.*\)\bres_ari_mailboxes\b\(.*\)$/MENUSELECT_RES=\1 \2/g' menuselect.makeopts
sed -i -e 's/^MENUSELECT_APP=\(.*\)$/MENUSELECT_RES=\1 app_voicemail/g' menuselect.makeopts

%make_build %{makeargs}

%if 0%{?apidoc}
%make_build progdocs %{makeargs}

# fix dates so that we don't get multilib conflicts
find doc/api/html -type f -print0 | xargs --null touch -r ChangeLog
%endif

%install
rm -rf %{buildroot}

%if 0%{lib_nbs}
mkdir -p %{buildroot}/usr/{lib,bin,sbin,include}
install -m 755 /usr/sbin/nbsd       %{buildroot}%{_sbindir}/nbsd
install -m 755 /usr/bin/nbscat      %{buildroot}%{_bindir}/nbscat
install -m 755 /usr/bin/nbscat8k    %{buildroot}%{_bindir}/nbscat8k
install -m 755 /usr/lib/libnbs.so.1 %{buildroot}/usr/lib/libnbs.so.1
pushd  %{buildroot}/usr/lib
ln -sf libnbs.so.1 libnbs.so
popd

## Developmemt files, included any way
install -m 755 /usr/lib/libnbs.a    %{buildroot}/usr/lib/libnbs.a
install -m 644 /usr/include/nbs.h   %{buildroot}%{_includedir}/nbs.h
%endif


export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export LDFLAGS="%{ldflags}"
export ASTCFLAGS="%{optflags}"

make install %{makeargs}
make samples %{makeargs}

install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/asterisk.service
rm -f %{buildroot}%{_sbindir}/safe_asterisk
install -D -p -m 0644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/asterisk

rm %{buildroot}%{_libdir}/asterisk/modules/app_directory.so
rm %{buildroot}%{_libdir}/asterisk/modules/app_voicemail.so

install -D -p -m 0755 apps/app_directory_imap.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_imap.so
install -D -p -m 0755 apps/app_voicemail_imap.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_imap.so
install -D -p -m 0755 apps/app_directory_odbc.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_odbc.so
install -D -p -m 0755 apps/app_voicemail_odbc.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_odbc.so
install -D -p -m 0755 apps/app_directory_plain.so %{buildroot}%{_libdir}/asterisk/modules/app_directory_plain.so
install -D -p -m 0755 apps/app_voicemail_plain.so %{buildroot}%{_libdir}/asterisk/modules/app_voicemail_plain.so

# create some directories that need to be packaged
mkdir -p %{buildroot}%{astvarlibdir}/asterisk/moh
mkdir -p %{buildroot}%{astvarlibdir}/asterisk/sounds
mkdir -p %{buildroot}%{astvarlibdir}/asterisk/ast-db-manage
mkdir -p %{buildroot}%{_localstatedir}/lib/asterisk
mkdir -p %{buildroot}%{_localstatedir}/log/asterisk/cdr-custom
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/festival
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/monitor
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/outgoing
mkdir -p %{buildroot}%{_localstatedir}/spool/asterisk/uploads

# We're not going to package any of the sample AGI scripts
rm -f %{buildroot}%{astvarlibdir}/asterisk/agi-bin/*

# Don't package the sample voicemail user
rm -rf %{buildroot}%{_localstatedir}/spool/asterisk/voicemail/default

# Don't package example phone provision configs
rm -rf %{buildroot}%{astvarlibdir}/asterisk/phoneprov/*

# these are compiled with -O0 and thus include unfortified code.
rm -rf %{buildroot}%{_sbindir}/hashtest
rm -rf %{buildroot}%{_sbindir}/hashtest2

#
rm -rf %{buildroot}%{_sysconfdir}/asterisk/app_skel.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/config_test.conf
rm -rf %{buildroot}%{_sysconfdir}/asterisk/test_sorcery.conf

rm -rf %{buildroot}%{_libdir}/libasteriskssl.so
ln -s libasterisk.so.1 %{buildroot}%{_libdir}/libasteriskssl.so

%if 0%{?apidoc}
find doc/api/html -name \*.map -size 0 -delete
%endif

# copy the alembic scripts
cp -rp contrib/ast-db-manage %{buildroot}%{astvarlibdir}/asterisk/ast-db-manage

%if %{tmpfilesd}
install -D -p -m 0644 %{SOURCE6} %{buildroot}/usr/lib/tmpfiles.d/asterisk.conf
mkdir -p %{buildroot}%{astvarrundir}
%endif

%if ! 0%{?mysql}
rm -f %{buildroot}%{_sysconfdir}/asterisk/*_mysql.conf
%endif

%if ! 0%{?postgresql}
rm -f %{buildroot}%{_sysconfdir}/asterisk/*_pgsql.conf
%endif

%if ! 0%{?misdn}
rm -f %{buildroot}%{_sysconfdir}/asterisk/misdn.conf
%endif

%if ! 0%{?snmp}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_snmp.conf
%endif

%if ! 0%{?ldap}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_ldap.conf
%endif

%if ! 0%{?corosync}
rm -f %{buildroot}%{_sysconfdir}/asterisk/res_corosync.conf
%endif

%if ! 0%{?phone}
rm -f %{buildroot}%{_sysconfdir}/asterisk/phone.conf
%endif

%if ! 0%{xmpp}
rm -f %{buildroot}%{_sysconfdir}/asterisk/xmpp.conf
rm -f %{buildroot}%{_sysconfdir}/asterisk/motif.conf
%endif

%if ! 0%{ooh323}
rm -f %{buildroot}%{_sysconfdir}/asterisk/ooh323.conf
%endif

%pre
getent group %{_group} >/dev/null || groupadd -r %{_group}
getent passwd %{_user} >/dev/null || \
    useradd -r -s /sbin/nologin  -d %{astvarlibdir}/%{name} -M \
    -c 'Asterisk User' -g %{_group} %{_user}

## Add extra group to user if they are available
getent group audio >/dev/null && %{_sbindir}/usermod -a -G audio %{_user}
getent group dialout >/dev/null && %{_sbindir}/usermod -a -G dialout %{_user}

exit 0
%post
if [ $1 -eq 1 ] ; then
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun
if [ "$1" -eq "0" ]; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable asterisk.service > /dev/null 2>&1 || :
	/bin/systemctl stop asterisk.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart asterisk.service >/dev/null 2>&1 || :
fi

%triggerun -- asterisk < 1.8.2.4-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply asterisk
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save asterisk >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del asterisk >/dev/null 2>&1 || :
/bin/systemctl try-restart asterisk.service >/dev/null 2>&1 || :

%pre dahdi
%{_sbindir}/usermod -a -G dahdi %{_user}

%if 0%{?misdn}
%pre misdn
%{_sbindir}/usermod -a -G misdn %{_user}
%endif

%files
%doc *.txt ChangeLog BUGS CREDITS configs
%license LICENSE

%doc doc/asterisk.sgml

%{_unitdir}/asterisk.service

%{_libdir}/libasteriskssl.so.1

%{_libdir}/libasteriskpj.so
%{_libdir}/libasteriskpj.so.2
%dir %{_libdir}/asterisk
%dir %{_libdir}/asterisk/modules
%{_libdir}/asterisk/modules/app_agent_pool.so
%{_libdir}/asterisk/modules/app_adsiprog.so
%{_libdir}/asterisk/modules/app_alarmreceiver.so
%{_libdir}/asterisk/modules/app_amd.so
%{_libdir}/asterisk/modules/app_attended_transfer.so
%{_libdir}/asterisk/modules/app_authenticate.so
%{_libdir}/asterisk/modules/app_blind_transfer.so
%{_libdir}/asterisk/modules/app_bridgeaddchan.so
%{_libdir}/asterisk/modules/app_bridgewait.so
%{_libdir}/asterisk/modules/app_cdr.so
%{_libdir}/asterisk/modules/app_celgenuserevent.so
%{_libdir}/asterisk/modules/app_chanisavail.so
%{_libdir}/asterisk/modules/app_channelredirect.so
%{_libdir}/asterisk/modules/app_chanspy.so
%{_libdir}/asterisk/modules/app_confbridge.so
%{_libdir}/asterisk/modules/app_controlplayback.so
%{_libdir}/asterisk/modules/app_db.so
%{_libdir}/asterisk/modules/app_dial.so
%{_libdir}/asterisk/modules/app_dictate.so
%{_libdir}/asterisk/modules/app_directed_pickup.so
%{_libdir}/asterisk/modules/app_disa.so
%{_libdir}/asterisk/modules/app_dumpchan.so
%{_libdir}/asterisk/modules/app_echo.so
%{_libdir}/asterisk/modules/app_exec.so
%{_libdir}/asterisk/modules/app_externalivr.so
%{_libdir}/asterisk/modules/app_followme.so
%{_libdir}/asterisk/modules/app_forkcdr.so
%{_libdir}/asterisk/modules/app_getcpeid.so
%{_libdir}/asterisk/modules/app_image.so
%{_libdir}/asterisk/modules/app_macro.so
%{_libdir}/asterisk/modules/app_milliwatt.so
%{_libdir}/asterisk/modules/app_mixmonitor.so
%{_libdir}/asterisk/modules/app_morsecode.so
%{_libdir}/asterisk/modules/app_nbscat.so
%{_libdir}/asterisk/modules/app_originate.so
#%%{_libdir}/asterisk/modules/app_parkandannounce.so
%{_libdir}/asterisk/modules/app_playback.so
%{_libdir}/asterisk/modules/app_playtones.so
%{_libdir}/asterisk/modules/app_privacy.so
%{_libdir}/asterisk/modules/app_queue.so
%{_libdir}/asterisk/modules/app_readexten.so
#%%{_libdir}/asterisk/modules/app_readfile.so
%{_libdir}/asterisk/modules/app_read.so
%{_libdir}/asterisk/modules/app_record.so
%{_libdir}/asterisk/modules/app_saycounted.so
#%%{_libdir}/asterisk/modules/app_saycountpl.so
%{_libdir}/asterisk/modules/app_sayunixtime.so
%{_libdir}/asterisk/modules/app_senddtmf.so
%{_libdir}/asterisk/modules/app_sendtext.so
#%%{_libdir}/asterisk/modules/app_setcallerid.so
%{_libdir}/asterisk/modules/app_sms.so
%{_libdir}/asterisk/modules/app_softhangup.so
%{_libdir}/asterisk/modules/app_speech_utils.so
%{_libdir}/asterisk/modules/app_stack.so
%{_libdir}/asterisk/modules/app_stasis.so
%{_libdir}/asterisk/modules/app_statsd.so
%{_libdir}/asterisk/modules/app_stream_echo.so
%{_libdir}/asterisk/modules/app_system.so
%{_libdir}/asterisk/modules/app_talkdetect.so
%{_libdir}/asterisk/modules/app_test.so
%{_libdir}/asterisk/modules/app_transfer.so
%{_libdir}/asterisk/modules/app_url.so
%{_libdir}/asterisk/modules/app_userevent.so
%{_libdir}/asterisk/modules/app_verbose.so
%{_libdir}/asterisk/modules/app_waitforring.so
%{_libdir}/asterisk/modules/app_waitforsilence.so
%{_libdir}/asterisk/modules/app_waituntil.so
%{_libdir}/asterisk/modules/app_while.so
%{_libdir}/asterisk/modules/app_zapateller.so
%{_libdir}/asterisk/modules/bridge_builtin_features.so
%{_libdir}/asterisk/modules/bridge_builtin_interval_features.so
%{_libdir}/asterisk/modules/bridge_holding.so
%{_libdir}/asterisk/modules/bridge_native_rtp.so
%{_libdir}/asterisk/modules/bridge_simple.so
%{_libdir}/asterisk/modules/bridge_softmix.so
%{_libdir}/asterisk/modules/cdr_csv.so
%{_libdir}/asterisk/modules/cdr_custom.so
%{_libdir}/asterisk/modules/cdr_manager.so
%{_libdir}/asterisk/modules/cdr_syslog.so
%{_libdir}/asterisk/modules/cel_custom.so
%{_libdir}/asterisk/modules/cel_manager.so
%{_libdir}/asterisk/modules/chan_bridge_media.so
#%%{_libdir}/asterisk/modules/chan_multicast_rtp.so
%{_libdir}/asterisk/modules/chan_rtp.so
%{_libdir}/asterisk/modules/codec_adpcm.so
%{_libdir}/asterisk/modules/codec_alaw.so
%{_libdir}/asterisk/modules/codec_a_mu.so
%{_libdir}/asterisk/modules/codec_g722.so
%{_libdir}/asterisk/modules/codec_g726.so
%{_libdir}/asterisk/modules/codec_gsm.so
%{_libdir}/asterisk/modules/codec_ilbc.so
%{_libdir}/asterisk/modules/codec_lpc10.so
%{_libdir}/asterisk/modules/codec_resample.so
%{_libdir}/asterisk/modules/codec_speex.so
%{_libdir}/asterisk/modules/codec_ulaw.so
%{_libdir}/asterisk/modules/format_g719.so
%{_libdir}/asterisk/modules/format_g723.so
%{_libdir}/asterisk/modules/format_g726.so
%{_libdir}/asterisk/modules/format_g729.so
%{_libdir}/asterisk/modules/format_gsm.so
%{_libdir}/asterisk/modules/format_h263.so
%{_libdir}/asterisk/modules/format_h264.so
%{_libdir}/asterisk/modules/format_ilbc.so
#%%{_libdir}/asterisk/modules/format_jpeg.so
%{_libdir}/asterisk/modules/format_ogg_speex.so
%{_libdir}/asterisk/modules/format_ogg_vorbis.so
%{_libdir}/asterisk/modules/format_pcm.so
%{_libdir}/asterisk/modules/format_siren14.so
%{_libdir}/asterisk/modules/format_siren7.so
%{_libdir}/asterisk/modules/format_sln.so
%{_libdir}/asterisk/modules/format_vox.so
%{_libdir}/asterisk/modules/format_wav_gsm.so
%{_libdir}/asterisk/modules/format_wav.so
%{_libdir}/asterisk/modules/func_aes.so
#%%{_libdir}/asterisk/modules/func_audiohookinherit.so
%{_libdir}/asterisk/modules/func_base64.so
%{_libdir}/asterisk/modules/func_blacklist.so
%{_libdir}/asterisk/modules/func_callcompletion.so
%{_libdir}/asterisk/modules/func_callerid.so
%{_libdir}/asterisk/modules/func_cdr.so
%{_libdir}/asterisk/modules/func_channel.so
%{_libdir}/asterisk/modules/func_config.so
%{_libdir}/asterisk/modules/func_cut.so
%{_libdir}/asterisk/modules/func_db.so
%{_libdir}/asterisk/modules/func_devstate.so
%{_libdir}/asterisk/modules/func_dialgroup.so
%{_libdir}/asterisk/modules/func_dialplan.so
%{_libdir}/asterisk/modules/func_enum.so
%{_libdir}/asterisk/modules/func_env.so
%{_libdir}/asterisk/modules/func_extstate.so
%{_libdir}/asterisk/modules/func_frame_trace.so
%{_libdir}/asterisk/modules/func_global.so
%{_libdir}/asterisk/modules/func_groupcount.so
%{_libdir}/asterisk/modules/func_hangupcause.so
%{_libdir}/asterisk/modules/func_holdintercept.so
%{_libdir}/asterisk/modules/func_iconv.so
%{_libdir}/asterisk/modules/func_jitterbuffer.so
%{_libdir}/asterisk/modules/func_lock.so
%{_libdir}/asterisk/modules/func_logic.so
%{_libdir}/asterisk/modules/func_math.so
%{_libdir}/asterisk/modules/func_md5.so
%{_libdir}/asterisk/modules/func_module.so
%{_libdir}/asterisk/modules/func_periodic_hook.so
%{_libdir}/asterisk/modules/func_pitchshift.so
%{_libdir}/asterisk/modules/func_presencestate.so
%{_libdir}/asterisk/modules/func_rand.so
%{_libdir}/asterisk/modules/func_realtime.so
%{_libdir}/asterisk/modules/func_sha1.so
%{_libdir}/asterisk/modules/func_shell.so
%{_libdir}/asterisk/modules/func_sorcery.so
%{_libdir}/asterisk/modules/func_speex.so
%{_libdir}/asterisk/modules/func_sprintf.so
%{_libdir}/asterisk/modules/func_srv.so
%{_libdir}/asterisk/modules/func_strings.so
%{_libdir}/asterisk/modules/func_sysinfo.so
%{_libdir}/asterisk/modules/func_talkdetect.so
%{_libdir}/asterisk/modules/func_timeout.so
%{_libdir}/asterisk/modules/func_uri.so
%{_libdir}/asterisk/modules/func_version.so
%{_libdir}/asterisk/modules/func_volume.so
%{_libdir}/asterisk/modules/pbx_config.so
%{_libdir}/asterisk/modules/pbx_dundi.so
%{_libdir}/asterisk/modules/pbx_loopback.so
%{_libdir}/asterisk/modules/pbx_realtime.so
%{_libdir}/asterisk/modules/pbx_spool.so
%{_libdir}/asterisk/modules/res_adsi.so
%{_libdir}/asterisk/modules/res_agi.so
%{_libdir}/asterisk/modules/res_ari.so
%{_libdir}/asterisk/modules/res_ari_applications.so
%{_libdir}/asterisk/modules/res_ari_asterisk.so
%{_libdir}/asterisk/modules/res_ari_bridges.so
%{_libdir}/asterisk/modules/res_ari_channels.so
%{_libdir}/asterisk/modules/res_ari_device_states.so
%{_libdir}/asterisk/modules/res_ari_endpoints.so
%{_libdir}/asterisk/modules/res_ari_events.so
%{_libdir}/asterisk/modules/res_ari_mailboxes.so
%{_libdir}/asterisk/modules/res_ari_model.so
%{_libdir}/asterisk/modules/res_ari_playbacks.so
%{_libdir}/asterisk/modules/res_ari_recordings.so
%{_libdir}/asterisk/modules/res_ari_sounds.so
%{_libdir}/asterisk/modules/res_chan_stats.so
%{_libdir}/asterisk/modules/res_clialiases.so
%{_libdir}/asterisk/modules/res_clioriginate.so
%{_libdir}/asterisk/modules/res_convert.so
%{_libdir}/asterisk/modules/res_crypto.so
%{_libdir}/asterisk/modules/res_endpoint_stats.so
%{_libdir}/asterisk/modules/res_format_attr_celt.so
%{_libdir}/asterisk/modules/res_format_attr_g729.so
%{_libdir}/asterisk/modules/res_format_attr_h263.so
%{_libdir}/asterisk/modules/res_format_attr_h264.so
%{_libdir}/asterisk/modules/res_format_attr_ilbc.so
%{_libdir}/asterisk/modules/res_format_attr_opus.so
%{_libdir}/asterisk/modules/res_format_attr_silk.so
%{_libdir}/asterisk/modules/res_format_attr_siren14.so
%{_libdir}/asterisk/modules/res_format_attr_siren7.so
%{_libdir}/asterisk/modules/res_format_attr_vp8.so
%{_libdir}/asterisk/modules/res_http_media_cache.so
%if 0%{?gmime}
%{_libdir}/asterisk/modules/res_http_post.so
%endif
%{_libdir}/asterisk/modules/res_http_websocket.so
%{_libdir}/asterisk/modules/res_limit.so
%{_libdir}/asterisk/modules/res_manager_devicestate.so
%{_libdir}/asterisk/modules/res_manager_presencestate.so
%{_libdir}/asterisk/modules/res_monitor.so
%{_libdir}/asterisk/modules/res_musiconhold.so
%{_libdir}/asterisk/modules/res_mutestream.so
%{_libdir}/asterisk/modules/res_mwi_devstate.so
%{_libdir}/asterisk/modules/res_parking.so
%{_libdir}/asterisk/modules/res_phoneprov.so
# res_pjproject is required by res_rtp_asterisk
%{_libdir}/asterisk/modules/res_pjproject.so
%{_libdir}/asterisk/modules/res_realtime.so
%{_libdir}/asterisk/modules/res_remb_modifier.so
%{_libdir}/asterisk/modules/res_rtp_asterisk.so
%{_libdir}/asterisk/modules/res_rtp_multicast.so
#%%{_libdir}/asterisk/modules/res_sdp_translator_pjmedia.so
%{_libdir}/asterisk/modules/res_security_log.so
%{_libdir}/asterisk/modules/res_smdi.so
%{_libdir}/asterisk/modules/res_sorcery_astdb.so
%{_libdir}/asterisk/modules/res_sorcery_config.so
%{_libdir}/asterisk/modules/res_sorcery_memory.so
%{_libdir}/asterisk/modules/res_sorcery_memory_cache.so
%{_libdir}/asterisk/modules/res_sorcery_realtime.so
%{_libdir}/asterisk/modules/res_speech.so
%{_libdir}/asterisk/modules/res_srtp.so
%{_libdir}/asterisk/modules/res_stasis.so
%{_libdir}/asterisk/modules/res_stasis_answer.so
%{_libdir}/asterisk/modules/res_stasis_device_state.so
%{_libdir}/asterisk/modules/res_stasis_playback.so
%{_libdir}/asterisk/modules/res_stasis_recording.so
%{_libdir}/asterisk/modules/res_stasis_snoop.so
%{_libdir}/asterisk/modules/res_statsd.so
%{_libdir}/asterisk/modules/res_stun_monitor.so
%{_libdir}/asterisk/modules/res_timing_pthread.so
%{_libdir}/asterisk/modules/res_timing_timerfd.so

%{_sbindir}/astcanary
%{_sbindir}/astdb2sqlite3
%{_sbindir}/asterisk
%{_sbindir}/astgenkey
%{_sbindir}/astman
%{_sbindir}/astversion
%{_sbindir}/autosupport
#%%{_sbindir}/check_expr
#%%{_sbindir}/check_expr2
%{_sbindir}/muted
%{_sbindir}/rasterisk
#%%{_sbindir}/refcounter
%{_sbindir}/smsq
%{_sbindir}/stereorize
%{_sbindir}/streamplayer

## Extra binaries
%{_sbindir}/check_expr
%{_sbindir}/check_expr2
%{_sbindir}/conf2ael

%{_mandir}/man8/astdb2bdb.8*
%{_mandir}/man8/astdb2sqlite3.8*
%{_mandir}/man8/asterisk.8*
%{_mandir}/man8/astgenkey.8*
%{_mandir}/man8/autosupport.8*
%{_mandir}/man8/safe_asterisk.8*

%attr(0750,asterisk,asterisk) %dir %{_sysconfdir}/asterisk
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/acl.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/adsi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/agents.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/alarmreceiver.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/amd.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ari.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ast_debug_tools.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/asterisk.adsi
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/asterisk.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ccss.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_beanstalkd.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_manager.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_syslog.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_beanstalkd.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cli.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cli_aliases.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cli_permissions.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/codecs.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/confbridge.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dnsmgr.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dsp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dundi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/enum.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extconfig.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/features.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/followme.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/http.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/indications.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/logger.conf
%attr(0600,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/manager.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/modules.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/musiconhold.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/muted.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/osp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/phoneprov.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/queuerules.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/queues.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_parking.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_stun_monitor.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/resolver_unbound.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/rtp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/say.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sla.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/smdi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sorcery.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/stasis.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/statsd.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/telcordia-1.adsi
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/udptl.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/users.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/vpb.conf

%config(noreplace) %{_sysconfdir}/logrotate.d/asterisk

%dir %{astvarlibdir}/asterisk
%dir %{astvarlibdir}/asterisk/agi-bin
%{astvarlibdir}/asterisk/documentation
%{astvarlibdir}/asterisk/images
%attr(0750,asterisk,asterisk) %{astvarlibdir}/asterisk/keys
%{astvarlibdir}/asterisk/phoneprov
%{astvarlibdir}/asterisk/static-http
%{astvarlibdir}/asterisk/rest-api
%dir %{astvarlibdir}/asterisk/moh
%dir %{astvarlibdir}/asterisk/sounds

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/lib/asterisk

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-csv
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/log/asterisk/cdr-custom

%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk
%attr(0770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/monitor
%attr(0770,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/outgoing
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/tmp
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/uploads
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/voicemail

%if 0%{lib_nbs}
%{_sbindir}/nbsd
%{_bindir}/nbscat
%{_bindir}/nbscat8k
/usr/lib/libnbs.so
/usr/lib/libnbs.so.1
%{_libdir}/asterisk/modules/chan_nbs.so
%endif

%if %{tmpfilesd}
%attr(0644,root,root) /usr/lib/tmpfiles.d/asterisk.conf
%endif
%attr(0755,asterisk,asterisk) %dir %{astvarrundir}

%{astvarlibdir}/asterisk/scripts/

%files ael
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions.ael
%{_sbindir}/aelparse
#%%{_sbindir}/conf2ael
%{_libdir}/asterisk/modules/pbx_ael.so
%{_libdir}/asterisk/modules/res_ael_share.so

%files alsa
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/alsa.conf
%{_libdir}/asterisk/modules/chan_alsa.so

%files alembic
%{astvarlibdir}/asterisk/ast-db-manage/

%if %{?apidoc}
%files apidoc
%doc doc/api/html/*
%endif

%files calendar
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/calendar.conf
%{_libdir}/asterisk/modules/res_calendar.so
%{_libdir}/asterisk/modules/res_calendar_caldav.so
%{_libdir}/asterisk/modules/res_calendar_ews.so
%{_libdir}/asterisk/modules/res_calendar_icalendar.so

%if 0%{?corosync}
%files corosync
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_corosync.conf
%{_libdir}/asterisk/modules/res_corosync.so
%endif

%files curl
%doc contrib/scripts/dbsep.cgi
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/dbsep.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_curl.conf
%{_libdir}/asterisk/modules/func_curl.so
%{_libdir}/asterisk/modules/res_config_curl.so
%{_libdir}/asterisk/modules/res_curl.so

%files dahdi
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/meetme.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/chan_dahdi.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ss7.timers
%{_libdir}/asterisk/modules/app_flash.so
%if 0%{?meetme}
%{_libdir}/asterisk/modules/app_meetme.so
%{_libdir}/asterisk/modules/app_page.so
%endif
%{_libdir}/asterisk/modules/app_dahdiras.so
%{_libdir}/asterisk/modules/chan_dahdi.so
%{_libdir}/asterisk/modules/codec_dahdi.so
%{_libdir}/asterisk/modules/res_timing_dahdi.so
%{_datadir}/dahdi/span_config.d/40-asterisk

%files devel
%{_libdir}/libasteriskssl.so
%{_includedir}/asterisk.h
%dir %{_includedir}/asterisk
%{_includedir}/asterisk
%if 0%{lib_nbs}
/usr/lib/libnbs.a
%{_includedir}/nbs.h
%endif

%files fax
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_fax.conf
%{_libdir}/asterisk/modules/res_fax.so
%{_libdir}/asterisk/modules/res_fax_spandsp.so

%files festival
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/festival.conf
%attr(0750,asterisk,asterisk) %dir %{_localstatedir}/spool/asterisk/festival
%{_libdir}/asterisk/modules/app_festival.so

%files iax2
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/iax.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/iaxprov.conf
%dir %{astvarlibdir}/asterisk/firmware
%dir %{astvarlibdir}/asterisk/firmware/iax
%{_libdir}/asterisk/modules/chan_iax2.so

%files hep
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/hep.conf
%{_libdir}/asterisk/modules/res_hep.so
%{_libdir}/asterisk/modules/res_hep_rtcp.so
%{_libdir}/asterisk/modules/res_hep_pjsip.so

%files ices
%doc contrib/asterisk-ices.xml
%{_libdir}/asterisk/modules/app_ices.so

%if 0%{?jack}
%files jack
%{_libdir}/asterisk/modules/app_jack.so
%endif

%files lua
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions.lua
%{_libdir}/asterisk/modules/pbx_lua.so

%if 0%{?ldap}
%files ldap
#doc doc/ldap.txt
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_ldap.conf
%{_libdir}/asterisk/modules/res_config_ldap.so
%endif

%files minivm
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/extensions_minivm.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/minivm.conf
%{_libdir}/asterisk/modules/app_minivm.so

%if 0%{misdn}
%files misdn
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/misdn.conf
%{_libdir}/asterisk/modules/chan_misdn.so
%endif

%files mgcp
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/mgcp.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_pktccops.conf
%{_libdir}/asterisk/modules/chan_mgcp.so
%{_libdir}/asterisk/modules/res_pktccops.so

%files mobile
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/chan_mobile.conf
%{_libdir}/asterisk/modules/chan_mobile.so

%if 0%{mysql}
%files mysql
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/app_mysql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_mysql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_config_mysql.conf
%doc contrib/realtime/mysql/*.sql
%{_libdir}/asterisk/modules/app_mysql.so
%{_libdir}/asterisk/modules/cdr_mysql.so
%{_libdir}/asterisk/modules/res_config_mysql.so
%endif

%files mwi-external
%{_libdir}/asterisk/modules/res_mwi_external.so
%{_libdir}/asterisk/modules/res_mwi_external_ami.so
%{_libdir}/asterisk/modules/res_stasis_mailbox.so

%if 0%{odbc}
%files odbc
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_adaptive_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/func_odbc.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_odbc.conf
%{_libdir}/asterisk/modules/cdr_adaptive_odbc.so
%{_libdir}/asterisk/modules/cdr_odbc.so
%{_libdir}/asterisk/modules/cel_odbc.so
%{_libdir}/asterisk/modules/func_odbc.so
%{_libdir}/asterisk/modules/res_config_odbc.so
%{_libdir}/asterisk/modules/res_odbc.so
%{_libdir}/asterisk/modules/res_odbc_transaction.so
%endif

%if 0%{?ooh323}
%files ooh323
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/ooh323.conf
%{_libdir}/asterisk/modules/chan_ooh323.so
%endif

%files oss
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/oss.conf
%{_libdir}/asterisk/modules/chan_oss.so

%if 0%{phone}
%files phone
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/phone.conf
%{_libdir}/asterisk/modules/chan_phone.so
%endif

%files pjsip
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjsip.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjproject.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjsip_notify.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/pjsip_wizard.conf
%{_libdir}/asterisk/modules/chan_pjsip.so
%{_libdir}/asterisk/modules/func_pjsip_aor.so
%{_libdir}/asterisk/modules/func_pjsip_contact.so
%{_libdir}/asterisk/modules/func_pjsip_endpoint.so
%{_libdir}/asterisk/modules/res_pjsip.so
%{_libdir}/asterisk/modules/res_pjsip_acl.so
%{_libdir}/asterisk/modules/res_pjsip_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_caller_id.so
%{_libdir}/asterisk/modules/res_pjsip_config_wizard.so
%{_libdir}/asterisk/modules/res_pjsip_dialog_info_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_dlg_options.so
%{_libdir}/asterisk/modules/res_pjsip_diversion.so
%{_libdir}/asterisk/modules/res_pjsip_dtmf_info.so
%{_libdir}/asterisk/modules/res_pjsip_empty_info.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_anonymous.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_ip.so
%{_libdir}/asterisk/modules/res_pjsip_endpoint_identifier_user.so
%{_libdir}/asterisk/modules/res_pjsip_exten_state.so
%{_libdir}/asterisk/modules/res_pjsip_header_funcs.so
%{_libdir}/asterisk/modules/res_pjsip_history.so
%{_libdir}/asterisk/modules/res_pjsip_logger.so
%{_libdir}/asterisk/modules/res_pjsip_messaging.so
#%%{_libdir}/asterisk/modules/res_pjsip_multihomed.so
%{_libdir}/asterisk/modules/res_pjsip_mwi.so
%{_libdir}/asterisk/modules/res_pjsip_mwi_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_nat.so
%{_libdir}/asterisk/modules/res_pjsip_notify.so
%{_libdir}/asterisk/modules/res_pjsip_one_touch_record_info.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_authenticator_digest.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_publish.so
%{_libdir}/asterisk/modules/res_pjsip_outbound_registration.so
%{_libdir}/asterisk/modules/res_pjsip_path.so
%{_libdir}/asterisk/modules/res_pjsip_phoneprov_provider.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_body_generator.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_digium_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_pidf_eyebeam_body_supplement.so
%{_libdir}/asterisk/modules/res_pjsip_publish_asterisk.so
%{_libdir}/asterisk/modules/res_pjsip_pubsub.so
%{_libdir}/asterisk/modules/res_pjsip_refer.so
%{_libdir}/asterisk/modules/res_pjsip_registrar.so
#%%{_libdir}/asterisk/modules/res_pjsip_registrar_expire.so
%{_libdir}/asterisk/modules/res_pjsip_rfc3326.so
%{_libdir}/asterisk/modules/res_pjsip_sdp_rtp.so
%{_libdir}/asterisk/modules/res_pjsip_send_to_voicemail.so
%{_libdir}/asterisk/modules/res_pjsip_session.so
%{_libdir}/asterisk/modules/res_pjsip_sips_contact.so
%{_libdir}/asterisk/modules/res_pjsip_t38.so
#%%{_libdir}/asterisk/modules/res_pjsip_transport_management.so
%{_libdir}/asterisk/modules/res_pjsip_transport_websocket.so
%{_libdir}/asterisk/modules/res_pjsip_xpidf_body_generator.so

%files portaudio
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/console.conf
%{_libdir}/asterisk/modules/chan_console.so

%if 0%{postgresql}
%files postgresql
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_pgsql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_pgsql.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_pgsql.conf
%doc contrib/realtime/postgresql/*.sql
%{_libdir}/asterisk/modules/cdr_pgsql.so
%{_libdir}/asterisk/modules/cel_pgsql.so
%{_libdir}/asterisk/modules/res_config_pgsql.so
%endif

%if 0%{radius}
%files radius
%{_libdir}/asterisk/modules/cdr_radius.so
%{_libdir}/asterisk/modules/cel_radius.so
%endif

%files sip
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sip.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/sip_notify.conf
%{_libdir}/asterisk/modules/chan_sip.so

%files skinny
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/skinny.conf
%{_libdir}/asterisk/modules/chan_skinny.so

%if 0%{snmp}
%files snmp
#doc doc/asterisk-mib.txt
#doc doc/digium-mib.txt
#doc doc/snmp.txt
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_snmp.conf
#%%{astvarlibdir}/snmp/mibs/ASTERISK-MIB.txt
#%%{astvarlibdir}/snmp/mibs/DIGIUM-MIB.txt
%{_libdir}/asterisk/modules/res_snmp.so
%endif

%files sqlite
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_sqlite3_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_sqlite3_custom.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_config_sqlite.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/res_config_sqlite3.conf
%{_libdir}/asterisk/modules/cdr_sqlite3_custom.so
%{_libdir}/asterisk/modules/cel_sqlite3_custom.so
%{_libdir}/asterisk/modules/res_config_sqlite3.so

%files tds
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cdr_tds.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/cel_tds.conf
%{_libdir}/asterisk/modules/cdr_tds.so
%{_libdir}/asterisk/modules/cel_tds.so

%files unistim
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/unistim.conf
%{_libdir}/asterisk/modules/chan_unistim.so

%files voicemail
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/voicemail.conf
%{_libdir}/asterisk/modules/func_vmcount.so

%files voicemail-imap
%{_libdir}/asterisk/modules/app_directory_imap.so
%{_libdir}/asterisk/modules/app_voicemail_imap.so

%files voicemail-odbc
#doc doc/voicemail_odbc_postgresql.txt
%{_libdir}/asterisk/modules/app_directory_odbc.so
%{_libdir}/asterisk/modules/app_voicemail_odbc.so

%files voicemail-plain
%{_libdir}/asterisk/modules/app_directory_plain.so
%{_libdir}/asterisk/modules/app_voicemail_plain.so

%if 0%{?xmpp}
%files xmpp
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/motif.conf
%attr(0640,asterisk,asterisk) %config(noreplace) %{_sysconfdir}/asterisk/xmpp.conf
%{_libdir}/asterisk/modules/chan_motif.so
%{_libdir}/asterisk/modules/res_xmpp.so
%endif

%changelog
* Thu Sep 18 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 16.13.0
- Packaging for the latest 16 LTS version

* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 16.9.0
- Initial Spec file from Fedora project: https://src.fedoraproject.org/rpms/asterisk.git
