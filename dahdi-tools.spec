#
# TODO:
# warning: Installed (but unpackaged) file(s) found:
#    /etc/hotplug/usb/xpp_fxloader
#    /etc/hotplug/usb/xpp_fxloader.usermap
#
# Conditional build:
%bcond_with	oslec		# with Open Source Line Echo Canceller
%bcond_with	bristuff	# with bristuff support
%bcond_without	xpp		# without Astribank
%bcond_with	verbose

%include	/usr/lib/rpm/macros.perl

%ifarch sparc
%undefine	with_smp
%endif
%ifarch alpha
%undefine	with_xpp
%endif

%define		rel	2
Summary:	DAHDI telephony device support
Summary(pl.UTF-8):	Obsługa urządzeń telefonicznych DAHDI
Name:		dahdi-tools
Version:	2.4.1
Release:	%{rel}%{?with_bristuff:.bristuff}
License:	GPL
Group:		Base/Kernel
Source0:	http://downloads.digium.com/pub/telephony/dahdi-tools/%{name}-%{version}.tar.gz
# Source0-md5:	a06cf7c68b0b9fbb61f5804abd1a05e9
Source1:	dahdi.init
Source2:	dahdi.sysconfig
Patch0:		%{name}-as-needed.patch
Patch1:		%{name}-perl-path.patch
URL:		http://www.asterisk.org/
BuildRequires:	dahdi-linux-devel >= 2.3.0
BuildRequires:	newt-devel
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_bristuff:Provides:	dahdi(bristuff)}
Obsoletes:	zaptel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Rules:
# - modules_X: single modules, just name module with no suffix
# - modules_X: subdir modules are just directory name with slash like dirname/
# - keep X and X_in in sync
# - X is used for actual building (entries separated with space), X_in for pld macros (entries separated with comma)

%description
DAHDI telephony device driver.

%description -l pl.UTF-8
Sterownik do urządzeń telefonicznych DAHDI.

%package devel
Summary:	DAHDI development headers
Summary(pl.UTF-8):	Pliki nagłówkowe DAHDI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{rel}
%{?with_bristuff:Provides:	dahdi-devel(bristuff)}
Obsoletes:	zaptel-devel

%description devel
DAHDI development headers.

%description devel -l pl.UTF-8
Pliki nagłówkowe DAHDI.

%package static
Summary:	DAHDI static library
Summary(pl.UTF-8):	Biblioteka statyczna DAHDI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{rel}
%{?with_bristuff:Provides:	dahdi-static(bristuff)}

%description static
DAHDI static library.

%description static -l pl.UTF-8
Biblioteka statyczna DAHDI.

%package utils
Summary:	DAHDI utility programs
Summary(pl.UTF-8):	Programy narzędziowe DAHDI
Group:		Applications/Communications
Obsoletes:	zaptel-utils

%description utils
DAHDI card utility programs, mainly for diagnostics.

%description utils -l pl.UTF-8
Programy narzędziowe do kart DAHDI, służące głównie do diagnostyki.

%package init
Summary:	DAHDI init scripts
Summary(pl.UTF-8):	Skrypty inicjalizujące DAHDI
Group:		Applications/Communications
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-utils = %{version}-%{rel}
Requires:	rc-scripts
Obsoletes:	zaptel-init

%description init
DAHDI boot-time initialization.

%description init -l pl.UTF-8
Inicjalizacja DAHDI w czasie startu systemu.

%package -n perl-Dahdi
Summary:	Perl interface to DAHDI
Summary(pl.UTF-8):	Perlowy interfejs do DAHDIa
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{rel}

%description -n perl-Dahdi
Perl inferface to DAHDI.

%description -n perl-Dahdi -l pl.UTF-8
Perlowy interfejs do DAHDIa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%if %{with kernel}
mkdir firmware
for a in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
	ln -s $a firmware
	tar -C firmware -xzf $a
done

cat > download-logger <<'EOF'
#!/bin/sh
# keep log of files make wanted to download in firmware/ dir
echo "$@" >> download.log
EOF
chmod a+rx download-logger
%endif

%build
%configure
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcppflags} %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dahdi
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/dahdi
touch $RPM_BUILD_ROOT%{_sysconfdir}/dahdi.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add dahdi
%service dahdi restart

%preun init
if [ "$1" = "0" ]; then
	%service dahdi stop
	/sbin/chkconfig --del dahdi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dahdi.conf
%dir %{_sysconfdir}/dahdi
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dahdi/system.conf
#/etc/hotplug/usb/xpp_fxloader
#/etc/hotplug/usb/xpp_fxloader.usermap
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*.so.*
%if %{with xpp}
%{_datadir}/dahdi
%{_mandir}/man8/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dahdi

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/dahdi

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*

%files -n perl-Dahdi
%defattr(644,root,root,755)
%{perl_vendorlib}/Dahdi
%{perl_vendorlib}/Dahdi.pm
%endif
