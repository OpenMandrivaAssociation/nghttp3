# nghttp3 can be used by curl, curl is used by libsystemd,
# libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 9
%define libname %mklibname nghttp3
%define develname %mklibname -d nghttp3
%define lib32name libnghttp3
%define devel32name libnghttp3-devel

Summary:	Experimental HTTP/3 client, server and proxy
Name:		nghttp3
Version:	1.8.0
Release:	1
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ngtcp2/nghttp3
Source0:	https://github.com/ngtcp2/nghttp3/releases/download/v%{version}/nghttp3-%{version}.tar.xz
BuildRequires:	cmake ninja
%if %{with compat32}
BuildRequires:	libc6
%endif

%description
This package contains the HTTP/3 client, server and proxy programs.

%package -n %{libname}
Summary: A library implementing the HTTP/3 protocol
Group: System/Libraries

%description -n %{libname}
libnghttp3 is a library implementing the Hypertext Transfer Protocol
version 3 (HTTP/3) protocol in C.

%package -n %{develname}
Summary: Files needed for building applications with libnghttp2
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} >= %{version}-%{release}

%description -n %{develname}
The libnghttp3-devel package includes libraries and header files needed
for building applications with libnghttp2.

%package -n %{lib32name}
Summary: A library implementing the HTTP/3 protocol (32-bit)
Group: System/Libraries

%description -n %{lib32name}
libnghttp3 is a library implementing the Hypertext Transfer Protocol
version 3 (HTTP/3) protocol in C.

%package -n %{devel32name}
Summary: Files needed for building applications with libnghttp2 (32-bit)
Group: Development/C
Requires: %{lib32name} = %{EVRD}
Requires: %{develname} = %{EVRD}

%description -n %{devel32name}
The libnghttp3-devel package includes libraries and header files needed
for building applications with libnghttp2.

%prep
%autosetup -p1 -n %{name}-%{version}



%if %{with compat32}
#define build_ldflags -O2 -fno-lto
%cmake32 -G Ninja -DENABLE_STATIC_LIB=OFF
cd ..
%endif
%cmake -G Ninja -DENABLE_STATIC_LIB=OFF

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build

%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}"
%ninja -C build check || :

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build

%files

%files -n %{libname}
%{_libdir}/libnghttp3.so.%{major}*

%files -n %{develname}
%{_includedir}/nghttp3
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_prefix}/lib/cmake/nghttp3
%doc %{_docdir}/nghttp3

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libnghttp3.so.%{major}*

%files -n %{devel32name}
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/*.so
%endif
