%define	snap 20040615

%define	major 1
%define libname %mklibname nbs %{major}
%define develname %mklibname nbs -d

Summary:	Network Broadcast Sound Daemon
Name:		nbs
Version:	1.0
Release:	%mkrel 0.%{snap}.5
License:	GPL
Group:		System/Servers
URL:		http://www.asterisk.org/
Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source1:	nbsd.init
Patch0:		nbs-1.0-20040615-mdk.diff
Patch1:		nbs-1.0-20040615-socket_path.diff
BuildConflicts:	%{name}-devel

%description
Network Broadcast Sound Daemon

%package -n	%{libname}
Summary:	Network Broadcast Sound Daemon Library
Group:          System/Libraries

%description -n	%{libname}
Network Broadcast Sound Daemon Library

%package -n	%{develname}
Summary:	Development files for the Network Broadcast Sound Daemon Library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libnbs-devel = %{version}-%{release}
Obsoletes:	%{mklibname nbs -d 1}

%description -n	%{develname}
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

%post server
%_post_service nbsd

%preun server
%_preun_service nbsd

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%doc xmms-nbs-1.2.10.patch* xmms-nbs.patch*
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a

%files server
%attr(0755,root,root) %{_initrddir}/nbsd
%{_sbindir}/nbsd
%dir %{_localstatedir}/lib/nbsd

%files client
%{_bindir}/nbscat
%{_bindir}/nbscat8k


%changelog
* Sat Dec 11 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20040615.5mdv2011.0
+ Revision: 620478
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.0-0.20040615.4mdv2010.0
+ Revision: 430155
- rebuild

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20040615.3mdv2009.0
+ Revision: 233038
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Jul 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20040615.2mdv2008.0
+ Revision: 54939
- bunzip the init script
- misc spec file fixes
- don't start the server per default, this conforms to the 2008 specifications


* Fri Oct 20 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20040615.1mdv2007.0
+ Revision: 71220
- Import nbs

* Sun Dec 25 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20040616.1mdk
- rebuild

* Tue Nov 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0-0.20040615.1mdk
- initial mandrake package
- added P0 and P1

