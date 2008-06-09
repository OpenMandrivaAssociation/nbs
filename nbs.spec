%define	snap	20040615

%define	major 1
%define libname	%mklibname nbs %{major}

Summary:	Network Broadcast Sound Daemon
Name:		nbs
Version:	1.0
Release:	%mkrel 0.%{snap}.2
License:	GPL
Group:		System/Servers
URL:		http://www.asterisk.org/
Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source1:	nbsd.init
Patch0:		nbs-1.0-20040615-mdk.diff
Patch1:		nbs-1.0-20040615-socket_path.diff
BuildConflicts:	%{name}-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Network Broadcast Sound Daemon

%package -n	%{libname}
Summary:	Network Broadcast Sound Daemon Library
Group:          System/Libraries

%description -n	%{libname}
Network Broadcast Sound Daemon Library

%package -n	%{libname}-devel
Summary:	Development files for the Network Broadcast Sound Daemon Library
Group:		Development/C
Obsoletes:	%{name}-devel libnbs-devel
Provides:	%{name}-devel libnbs-devel
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
Development files for the Network Broadcast Sound Daemon Library

This package contains the static nbs library and its header
files.

%package	server
Summary:	Network Broadcast Sound Daemon
Group:          System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description	server
Network Broadcast Sound Daemon

%package	client
Summary:	Network Broadcast Sound Daemon (Client Listener)
Group:          System/Servers

%description	client
Network Broadcast Sound Daemon (Client Listener)

%prep

%setup -q -n %{name}-%{version}-%{snap}
%patch0 -p0 -b .mdk
%patch1 -p0 -b .socket

cp %{SOURCE1} nbsd.init

%build

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_localstatedir}/lib/nbsd
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}

install -m0755 libnbs.so.%{major}.0 %{buildroot}%{_libdir}/
ln -snf libnbs.so.%{major}.0 %{buildroot}%{_libdir}/libnbs.so.%{major}
ln -snf libnbs.so.%{major}.0 %{buildroot}%{_libdir}/libnbs.so
install -m0755 libnbs.a %{buildroot}/%{_libdir}/
install -m0644 nbs.h %{buildroot}%{_includedir}/
install -m0755 nbscat %{buildroot}%{_bindir}/
install -m0755 nbscat8k %{buildroot}%{_bindir}/
install -m0755 nbsd %{buildroot}%{_sbindir}/
install -m0755 nbsd.init %{buildroot}%{_initrddir}/nbsd

bzip2 *.patch

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post server
%_post_service nbsd

%preun server
%_preun_service nbsd

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc xmms-nbs-1.2.10.patch* xmms-nbs.patch*
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a

%files server
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/nbsd
%{_sbindir}/nbsd
%dir %{_localstatedir}/lib/nbsd

%files client
%defattr(-,root,root)
%{_bindir}/nbscat
%{_bindir}/nbscat8k
