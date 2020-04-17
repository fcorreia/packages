%global shortname srtp

Name:		libsrtp
Version:	1.5.4
Release:    %{rpm_release}.%{disttype}%{distnum}
Summary:	An implementation of the Secure Real-time Transport Protocol (SRTP)
License:	BSD
URL:		https://github.com/cisco/libsrtp
Source0:	https://github.com/cisco/libsrtp/archive/v%{version}.tar.gz
# Universal config.h
Source2:	config.h
BuildRequires:	gcc
BuildRequires:  libusb-devel
BuildRequires:  newt-devel
BuildRequires:  perl-generators
BuildRequires:  chrpath

# Fix shared lib so ldconfig doesn't complain
Patch0:		libsrtp-1.5.4-shared-fix.patch
Patch1:		libsrtp-srtp_aes_encrypt.patch
Patch2:		libsrtp-sha1-name-fix.patch
Patch3:		libsrtp-fix-name-collision-on-MIPS.patch

%description
This package provides an implementation of the Secure Real-time
Transport Protocol (SRTP), the Universal Security Transform (UST), and
a supporting cryptographic kernel.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .sharedfix
%patch1 -p1 -b .srtp_aes_encrypt
%patch2 -p1 -b .sha1-name-fix
%patch3 -p1 -b .mips-name-fix

%if 0%{?rhel} > 0
%ifarch ppc64
sed -i 's/-z noexecstack//' Makefile.in
%endif
%endif

%build
export CFLAGS="%{optflags} -fPIC"
%configure
make %{?_smp_mflags} shared_library

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Handle multilib issues with config.h
mv %{buildroot}%{_includedir}/%{shortname}/config.h %{buildroot}%{_includedir}/%{shortname}/config-%{__isa_bits}.h
cp -a %{SOURCE2} %{buildroot}%{_includedir}/%{shortname}/config.h

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc CHANGES README TODO VERSION doc/*.txt doc/*.pdf
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{shortname}/
%{_libdir}/pkgconfig/libsrtp.pc
%{_libdir}/*.so

%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 1.5.4
- Initial Spec file from Fedora project: https://src.fedoraproject.org/rpms/libsrtp.git


