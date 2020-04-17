
%define version     1.6.0

#global _beta 3
Summary: An implementation of Primary Rate ISDN
Name:    libpri
Version: %{version}
Release: %{rpm_release}.%{disttype}%{distnum}
License: GPLv2+
URL: http://www.asterisk.org/
Source0: http://downloads.asterisk.org/pub/telephony/libpri/releases/libpri-%{version}%{?_beta:-beta%{_beta}}.tar.gz
Source1: http://downloads.asterisk.org/pub/telephony/libpri/releases/libpri-%{version}%{?_beta:-beta%{_beta}}.tar.gz.asc


BuildRequires: dahdi-tools-devel%{?isa}
BuildRequires: gcc

Requires: glibc

%description
libpri is a C implementation of the Primary Rate ISDN specification.
It was based on the Bellcore specification SR-NWT-002343 for National
ISDN.  As of May 12, 2001, it has been tested work with NI-2, Nortel
DMS-100, and Lucent 5E Custom protocols on switches from Nortel and
Lucent.

%package devel
Summary: Development files for libpri
Requires: libpri = %{version}-%{release}

%description devel
Development files for libpri.

%prep
%setup0 -q -n %{name}-%{version}%{?_beta:-beta%{_beta}}
%{__sed} -ri -e 's@\$\(INSTALL_BASE\)\/lib@%{_libdir}@g' Makefile
%{__sed} -ri -e '\@/sbin\/restorecon@d' Makefile

%build
make %{?_smp_mflags}

%install
make INSTALL_PREFIX=%{buildroot} install
rm %{buildroot}%{_libdir}/libpri.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE README
%{_libdir}/libpri.so.*

%files devel
%{_includedir}/libpri.h
%{_libdir}/libpri.so

%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.6.0
- Initial Spec file from Fedora project: https://src.fedoraproject.org/rpms/libpri.git