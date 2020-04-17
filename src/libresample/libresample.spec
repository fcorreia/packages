Name: libresample
Version: 0.1.3
Summary: A real-time library for audio sampling rate conversion
Release: %{rpm_release}.%{disttype}%{distnum}
License: LGPLv2+
URL: https://ccrma.stanford.edu/~jos/resample/Free_Resampling_Software.html
Source0: http://ccrma.stanford.edu/~jos/gz/libresample-%{version}.tgz
Source1: libresample.pc
Patch1: libresample_shared-libs.patch
BuildRequires: cmake >= 2.4
BuildRequires: doxygen
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libsndfile-devel
BuildRequires: libsamplerate-devel

%description
A real-time library for audio sampling rate conversion providing
several useful features relative to resample-1.7 on which it is based:

    * It should build "out of the box" on more platforms, including
      Linux, Solaris, and Mac OS X (using the included configure
      script). There is also a Visual C++ project file for building
      under Windows.

    * Input and output signals are in memory (as opposed to sound
      files).

    * Computations are in floating-point (instead of fixed-point).

    * Filter table increased by a factor of 32, yielding more accurate
      results, even without linear interpolation (which also makes it
      faster).

    * Data can be processed in small chunks, enabling time-varying
      resampling ratios (ideal for time-warping applications and
      supporting an ``external clock input'' in software).

    * Easily applied to any number of simultaneous data channels 

%package devel
Summary: Development files for libresample
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libresample.

%prep
%autosetup
mkdir pkgconfig
cp %{SOURCE1} pkgconfig/

%configure

%build
%make_build VERBOSE=1

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mkdir -p %{buildroot}%{_includedir}
cp tests/resample-sndfile %{buildroot}%{_bindir}/
cp libresample.so.0 %{buildroot}%{_libdir}/
cp include/libresample.h %{buildroot}%{_includedir}/
cp libresample.so %{buildroot}%{_libdir}/
cp pkgconfig/libresample.pc %{buildroot}%{_libdir}/pkgconfig/

%check
export LD_LIBRARY_PATH=.
make tests

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE.txt README.txt
%{_bindir}/resample-sndfile
%{_libdir}/libresample.so.0

%files devel
%doc README.txt
%license LICENSE.txt
%{_includedir}/libresample.h
%{_libdir}/libresample.so
%{_libdir}/pkgconfig/libresample.pc

%changelog
* Thu Apr 16 2020 Francisco Correia <fcorreia@users.noreply.github.com> - 0.1.3
- Initial Spec file from Fedora project: https://src.fedoraproject.org/rpms/libresample.git


