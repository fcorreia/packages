%global majorver 1
%global minorver 0
%global tinyver  0

Name:			signalwire-client-c
Summary:		SignalWire C Client and Library Headers
Version:		1.3.0
Release:		%{rpm_release}.%{disttype}%{distnum}
License:		MIT
Group:			Development/Libraries/C and C++
Source0:		%{name}-%{version}.tar.gz
#Patch0:			signalwire-client-c-1.2.0-pkgconfig.patch
#Patch1:			signalwire-client-c-1.2.0-lib.patch
URL:			http://freeswitch.org/

BuildRequires:		libuuid-devel
BuildRequires:		libatomic
BuildRequires:		libks-devel
BuildRequires:		openssl-devel
BuildRequires:		git

%if 0%{?rhel} < 8
BuildRequires:		cmake3
%else
BuildRequires:		cmake
%endif

%description
signalwire-client-c

%package devel
Summary:		Development files for libks
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against
signalwire-client-c.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
#autoreconf -i

%build
#configure
%if 0%{?rhel} < 8
cmake3 . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} -DCMAKE_INSTALL_PREFIX:PATH=/usr
%else
cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} -DCMAKE_INSTALL_PREFIX:PATH=/usr
%endif

%{__make}

%install
DESTDIR=%{buildroot} %{__make} install


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README copyright
%{_libdir}/libsignalwire_client.so.*
%if 0%{?rhel} < 8
%exclude /usr/share/doc/signalwire-client-c/copyright
%endif

%files devel
# These are SDK docs, not really useful to an end-user.
%{_libdir}/pkgconfig/signalwire_client.pc
%{_includedir}/signalwire-client-c/*


%changelog
* Thu Mar 31 2022 Tux Skywaler <tux.skywalker@users.noreply.github.com> - 1.2.0
- update spec file to lates GitHub version