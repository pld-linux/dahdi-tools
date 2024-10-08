# TODO: package /etc/dracut.conf.d/50-dahdi.conf
#
# Conditional build
%bcond_without	ppp		# pppd plugin
#
Summary:	DAHDI telephony device support
Summary(pl.UTF-8):	Obsługa urządzeń telefonicznych DAHDI
Name:		dahdi-tools
Version:	3.4.0
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.asterisk.org/pub/telephony/dahdi-tools/%{name}-%{version}.tar.gz
# Source0-md5:	c2ca147fcf8b6160105fdfa8771e26ff
Source1:	dahdi.init
Source2:	dahdi.sysconfig
Patch0:		%{name}-includes.patch
Patch1:		%{name}-pppd.patch
URL:		https://www.asterisk.org/
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	dahdi-linux-devel >= 3.4.0
BuildRequires:	libpcap-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel >= 1.0.9
BuildRequires:	newt-devel
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%{?with_ppp:BuildRequires:	ppp-plugin-devel >= 3:2.5.0}
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
Requires:	libusb >= 1.0.9
Obsoletes:	dahdi-tools-utils < 2.6.1
Obsoletes:	zaptel < 2
Obsoletes:	zaptel-utils < 2
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
Obsoletes:	zaptel-devel < 2

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

%package perl
Summary:	DAHDI utility programs written in Perl
Summary(pl.UTF-8):	Programy narzędziowe DAHDI napisane w Perlu
Group:		Applications/Communications
Requires:	perl-Dahdi = %{version}-%{release}

%description perl
DAHDI utility programs written in Perl.

%description perl -l pl.UTF-8
Programy narzędziowe DAHDI napisane w Perlu.

%package init
Summary:	DAHDI init scripts
Summary(pl.UTF-8):	Skrypty inicjalizujące DAHDI
Group:		Applications/Communications
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	zaptel-init < 2

%description init
DAHDI boot-time initialization.

%description init -l pl.UTF-8
Inicjalizacja DAHDI w czasie startu systemu.

%package -n dracut-dahdi-tools
Summary:	dracut rules for DAHDI kernel modules
Summary(pl.UTF-8):	Reguły dracut dla modułów jądra Linuksa dla DAHDI
Group:		Applications/System
Requires:	%{name} >= 2.2.0
Requires:	dracut

%description -n dracut-dahdi-tools
dracut rules for DAHDI kernel modules.

%description -n dracut-dahdi-tools -l pl.UTF-8
Reguły dracut dla modułów jądra Linuksa dla DAHDI.

%package -n udev-dahdi-tools
Summary:	udev rules for DAHDI kernel modules
Summary(pl.UTF-8):	Reguły udev dla modułów jądra Linuksa dla DAHDI
Group:		Applications/System
Obsoletes:	dahdi-linux-udev < 2.9.0
Obsoletes:	dahdi-tools-udev < 3.1.0
Requires:	%{name} >= 2.2.0
Requires:	udev-core

%description -n udev-dahdi-tools
udev rules for DAHDI kernel modules.

%description -n udev-dahdi-tools -l pl.UTF-8
Reguły udev dla modułów jądra Linuksa dla DAHDI.

%package -n bash-completion-dahdi
Summary:	Bash completion for DAHDI commands
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla poleceń DAHDI
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-dahdi
Bash completion for DAHDI commands.

%description -n bash-completion-dahdi -l pl.UTF-8
Bashowe dopełnianie składni dla poleceń DAHDI.

%package -n perl-Dahdi
Summary:	Perl interface to DAHDI
Summary(pl.UTF-8):	Perlowy interfejs do DAHDI
Group:		Development/Languages/Perl
# needs dahdi_scan
Requires:	%{name} = %{version}-%{release}

%description -n perl-Dahdi
Perl inferface to DAHDI.

%description -n perl-Dahdi -l pl.UTF-8
Perlowy interfejs do DAHDI.

%package -n ppp-plugin-dahdi
Summary:	DAHDI plugin for PPP daemon
Summary(pl.UTF-8):	Wtyczka DAHDI dla demona PPP
Group:		Libraries
Requires:	ppp >= 3:2.5.0

%description -n ppp-plugin-dahdi
DAHDI plugin for PPP daemon.

%description -n ppp-plugin-dahdi -l pl.UTF-8
Wtyczka DAHDI dla demona PPP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

cat > download-logger <<'EOF'
#!/bin/sh
# keep log of files make wanted to download in firmware/ dir
echo "$@" >> download.log
EOF
chmod a+rx download-logger

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-perllib=%{perl_vendorlib} \
	%{!?with_ppp:--without-ppp}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} -j1 install install-config \
	DESTDIR=$RPM_BUILD_ROOT \
	PPPD_VERSION=plugins \
	dracutconfdir=/etc/dracut.conf.d

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtonezone.la
%if %{with ppp}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pppd/plugins/dahdi.{la,a}
%endif

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dahdi
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/dahdi
touch $RPM_BUILD_ROOT%{_sysconfdir}/dahdi.conf

# sample configuration files - nothing enabled by default, so safe to install
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/dahdi/assigned-spans.conf{.sample,}
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/dahdi/span-types.conf{.sample,}
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/dahdi/system.conf{.sample,}

# used by upstream (but not PLD) init script
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/dahdi/{init.conf,modules.sample}

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
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dahdi/assigned-spans.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dahdi/span-types.conf
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/dahdi-blacklist.conf
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/dahdi.conf
%attr(755,root,root) %{_sbindir}/astribank_*
%attr(755,root,root) %{_sbindir}/dahdi_cfg
%attr(755,root,root) %{_sbindir}/dahdi_maint
%attr(755,root,root) %{_sbindir}/dahdi_monitor
%attr(755,root,root) %{_sbindir}/dahdi_scan
%attr(755,root,root) %{_sbindir}/dahdi_speed
%attr(755,root,root) %{_sbindir}/dahdi_test
%attr(755,root,root) %{_sbindir}/dahdi_tool
%attr(755,root,root) %{_sbindir}/dahdi_span_assignments
%attr(755,root,root) %{_sbindir}/dahdi_span_types
%attr(755,root,root) %{_sbindir}/dahdi_waitfor_span_assignments
%attr(755,root,root) %{_sbindir}/fxotune
%attr(755,root,root) %{_sbindir}/sethdlc
%attr(755,root,root) %{_libdir}/libtonezone.so.2.*
%attr(755,root,root) %ghost %{_libdir}/libtonezone.so.2
%{_datadir}/dahdi
%{_mandir}/man8/astribank_*.8*
%{_mandir}/man8/dahdi_cfg.8*
%{_mandir}/man8/dahdi_maint.8*
%{_mandir}/man8/dahdi_monitor.8*
%{_mandir}/man8/dahdi_scan.8*
%{_mandir}/man8/dahdi_span_assignments.8*
%{_mandir}/man8/dahdi_span_types.8*
%{_mandir}/man8/dahdi_test.8*
%{_mandir}/man8/dahdi_tool.8*
%{_mandir}/man8/dahdi_waitfor_span_assignments.8*
%{_mandir}/man8/fxotune.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtonezone.so
%{_includedir}/dahdi/tonezone.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtonezone.a

%files perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dahdi_genconf
%attr(755,root,root) %{_sbindir}/dahdi_hardware
%attr(755,root,root) %{_sbindir}/dahdi_registration
%attr(755,root,root) %{_sbindir}/lsdahdi
%attr(755,root,root) %{_sbindir}/twinstar
%attr(755,root,root) %{_sbindir}/xpp_blink
%attr(755,root,root) %{_sbindir}/xpp_sync
# for dahdi_genconf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dahdi/genconf_parameters
%{_mandir}/man8/dahdi_genconf.8*
%{_mandir}/man8/dahdi_hardware.8*
%{_mandir}/man8/dahdi_registration.8*
%{_mandir}/man8/lsdahdi.8*
%{_mandir}/man8/twinstar.8*
%{_mandir}/man8/xpp_blink.8*
%{_mandir}/man8/xpp_sync.8*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/dahdi
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dahdi

%files -n udev-dahdi-tools
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/dahdi.rules
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/xpp.rules

%files -n dracut-dahdi-tools
%defattr(644,root,root,755)
/etc/dracut.conf.d/50-dahdi.conf

%files -n bash-completion-dahdi
%defattr(644,root,root,755)
/etc/bash_completion.d/dahdi

%files -n perl-Dahdi
%defattr(644,root,root,755)
%{perl_vendorlib}/Dahdi
%{perl_vendorlib}/Dahdi.pm

%if %{with ppp}
%files -n ppp-plugin-dahdi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pppd/plugins/dahdi.so
%endif
