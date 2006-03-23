Summary:	Daemon that watches lm_sensors and beeps on alarms
Summary(pl):	Demon kontroluj±cy stan lm_sensors i piszcz±cy podczas alarmów
Name:		alarmwatch
Version:	1.0
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://www.azstarnet.com/~donut/programs/alarmwatch/%{name}-%{version}.tar.gz
# Source0-md5:	8a905a4746fdb028257af842afe748db
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.azstarnet.com/~donut/programs/alarmwatch.html
BuildRequires:	autoconf
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	lm_sensors
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
alarmwatch watches the lm_sensors /proc filesystem for the chips you
specify, and alerts you by beeping and syslog messages when an alarm
that is not ignored is active.

%description -l pl
alarmwatch kontroluje stan wybranych uk³adów poprzez lm_sensors w
systemie plików /proc i ostrzega piskami oraz komunikatami w logach,
kiedy nie ignorowany alarm jest aktywny.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

install alarmwatch $RPM_BUILD_ROOT%{_sbindir}
sed -e 's@alarmwatch 1@alarmwatch 8@' alarmwatch.1 \
	> $RPM_BUILD_ROOT%{_mandir}/man8/alarmwatch.8

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alarmwatch
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/alarmwatch

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add alarmwatch
%service alarmwatch restart "alarmwatch daemon"
if [ "$1" = 1 ]; then
	echo "Remember to configure it first!"
fi

%preun
if [ "$1" = "0" ]; then
	%service alarmwatch stop
	/sbin/chkconfig --del alarmwatch
fi

%files
%defattr(644,root,root,755)
%doc README Changelog
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/alarmwatch
%attr(754,root,root) /etc/rc.d/init.d/alarmwatch
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
