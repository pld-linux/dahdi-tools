# TODO:
# warning: Installed (but unpackaged) file(s) found:
#    /etc/hotplug/usb/xpp_fxloader
#    /etc/hotplug/usb/xpp_fxloader.usermap
#
%include	/usr/lib/rpm/macros.perl
Summary:	DAHDI telephony device support
Summary(pl.UTF-8):	Obsługa urządzeń telefonicznych DAHDI
Name:		dahdi-tools
Version:	2.6.1
Release:	1
License:	GPL v2
Group:		Base/Kernel
Source0:	http://downloads.digium.com/pub/telephony/dahdi-tools/%{name}-%{version}.tar.gz
# Source0-md5:	c2e4f476a8e7f96a5cad46dd9b648446
Source1:	dahdi.init
Source2:	dahdi.sysconfig
Patch0:		%{name}-as-needed.patch
Patch1:		%{name}-perl-path.patch
Patch2:		%{name}-includes.patch
URL:		http://www.asterisk.org/
BuildRequires:	dahdi-linux-devel >= 2.3.0
BuildRequires:	newt-devel
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.379
Obsoletes:	dahdi-tools-utils
Obsoletes:	zaptel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DAHDI telephony device driver.

%description -l pl.UTF-8
Sterownik do urządzeń telefonicznych DAHDI.

%package devel
Summary:	DAHDI development headers
Summary(pl.UTF-8):	Pliki nagłówkowe DAHDI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dahdi-linux-devel
Obsoletes:	zaptel-devel

%description devel
DAHDI development headers.

%description devel -l pl.UTF-8
Pliki nagłówkowe DAHDI.

%package static
Summary:	DAHDI static library
Summary(pl.UTF-8):	Biblioteka statyczna DAHDI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
DAHDI static library.

%description static -l pl.UTF-8
Biblioteka statyczna DAHDI.

%package init
Summary:	DAHDI init scripts
Summary(pl.UTF-8):	Skrypty inicjalizujące DAHDI
Group:		Applications/Communications
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	zaptel-init

%description init
DAHDI boot-time initialization.

%description init -l pl.UTF-8
Inicjalizacja DAHDI w czasie startu systemu.

%package -n perl-Dahdi
Summary:	Perl interface to DAHDI
Summary(pl.UTF-8):	Perlowy interfejs do DAHDI
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-Dahdi
Perl inferface to DAHDI.

%description -n perl-Dahdi -l pl.UTF-8
Perlowy interfejs do DAHDI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

cat > download-logger <<'EOF'
#!/bin/sh
# keep log of files make wanted to download in firmware/ dir
echo "$@" >> download.log
EOF
chmod a+rx download-logger

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
%attr(755,root,root) %{_sbindir}/astribank_*
%attr(755,root,root) %{_sbindir}/dahdi_*
%attr(755,root,root) %{_sbindir}/fpga_load
%attr(755,root,root) %{_sbindir}/fxotune
%attr(755,root,root) %{_sbindir}/lsdahdi
%attr(755,root,root) %{_sbindir}/sethdlc
%attr(755,root,root) %{_sbindir}/twinstar
%attr(755,root,root) %{_sbindir}/xpp_blink
%attr(755,root,root) %{_sbindir}/xpp_sync
%attr(755,root,root) %{_libdir}/libtonezone.so.1.*
%attr(755,root,root) %ghost %{_libdir}/libtonezone.so.1
%attr(755,root,root) %{_libdir}/libtonezone.so.2.*
%attr(755,root,root) %ghost %{_libdir}/libtonezone.so.2
%{_datadir}/dahdi
%{_mandir}/man8/astribank_*.8*
%{_mandir}/man8/dahdi_*.8*
%{_mandir}/man8/fpga_load.8*
%{_mandir}/man8/fxotune.8*
%{_mandir}/man8/lsdahdi.8*
%{_mandir}/man8/twinstar.8*
%{_mandir}/man8/xpp_blink.8*
%{_mandir}/man8/xpp_sync.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtonezone.so
%{_includedir}/dahdi/tonezone.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtonezone.a

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/dahdi
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dahdi

%files -n perl-Dahdi
%defattr(644,root,root,755)
%{perl_vendorlib}/Dahdi
%{perl_vendorlib}/Dahdi.pm
