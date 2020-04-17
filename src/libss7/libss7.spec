
Name:           libss7
Version:        2.0.0
Release:        %{rpm_release}.%{disttype}%{distnum}
Summary:        SS7 protocol services to applications


License:        GPLv2

URL:            http://www.asterisk.org/

## Also avilable at: https://github.com/asterisk/libss7/releases
Source0:        http://downloads.digium.com/pub/telephony/libss7/releases/libss7-%{version}.tar.gz


BuildRequires:  gcc
%description
libss7 is a userspace library that is used for providing SS7 protocol
services to applications.  It has a working MTP2, MTP3, and ISUP for
ITU and ANSI style SS7, however it was written in a manner that will
easily allow support for other various national specific variants in
the future.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup0 -q

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_PREFIX=$RPM_BUILD_ROOT libdir=%{_libdir}
#ln -s libss7.so.1.0 $RPM_BUILD_ROOT%{_libdir}/libss7.so.1
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc ChangeLog NEWS* README LICENSE
%{_libdir}/*.so.*

%files devel
%doc README LICENSE
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 2.0.0-1
- Initial Spec file from Fedora project: https://src.fedoraproject.org/rpms/libss7.git

