Name:           dci-feeder
Version:        0.0.1
Release:        1.VERS%{?dist}
Summary:        DCI Feeder

License:        ASL 2.0
URL:            https://softwarefactory-project.io/r/dci-feeder
Source0:        dcifeeder-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-setuptools

Requires:       epel-release
Requires:       python-flask
Requires:       python-requests
Requires:       python2-celery
Requires:       python2-dciclient
Requires:       openssh-clients
Requires:       rabbitmq-server
Requires:       rsync

%description
Artefacts distribution infrastructure for Distributed CI.

%prep
%autosetup -n dcifeeder-%{version}

%build
%py2_build

%install
%py2_install
install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_rundir}/celery
install -d %{buildroot}/var/log/celery
install -d %{buildroot}/%{_sysconfdir}/conf.d
install -d %{buildroot}/%{_sysconfdir}/systemd/system
install -d %{buildroot}/%{_localstatedir}/log/celery

cp bin/run-feeder-api %{buildroot}/%{_bindir}/run-feeder-api
cp systemd/dci-worker.service %{buildroot}/%{_sysconfdir}/systemd/system/dci-worker.service
cp systemd/celery %{buildroot}/%{_sysconfdir}/conf.d/celery

%files
%doc README.md
%license LICENSE
%{python2_sitelib}/dcifeeder-*-py2.7.egg-info
%{python2_sitelib}/dcifeeder
%{_bindir}/run-feeder-api
%{_rundir}/celery
%{_sysconfdir}/conf.d/celery
%{_sysconfdir}/systemd/system/dci-worker.service

%changelog
