Name:           eucaconsole-selinux
Version:        0.1.3
Release:        1%{?dist}
Summary:        SELinux policy for eucaconsole

License:        ISC
URL:            https://github.com/eucalyptus/eucaconsole-selinux
Source0:        %{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  selinux-policy-devel

Requires:       libselinux-utils
Requires:       policycoreutils
Requires(post): policycoreutils
Requires(post): selinux-policy-base >= %{_selinux_policy_version}
Requires(postun): policycoreutils

%description
This package installs and sets up the SELinux policy security module
for eucaconsole.


%prep
%autosetup


%build
make


%install
install -Dp -m 0644 eucaconsole.if $RPM_BUILD_ROOT%{_datadir}/selinux/devel/include/contrib/eucaconsole.if
install -Dp -m 0644 eucaconsole.pp $RPM_BUILD_ROOT%{_datadir}/selinux/packages/eucaconsole.pp


%files
%license COPYING
%{_datadir}/selinux/devel/include/contrib/eucaconsole.if
%{_datadir}/selinux/packages/eucaconsole.pp


%post
if /usr/sbin/selinuxenabled; then
    /usr/sbin/semodule -i %{_datadir}/selinux/packages/eucaconsole.pp >/dev/null || :
fi


%postun
if [ $1 -eq 0 ] && /usr/sbin/selinuxenabled; then
    /usr/sbin/semodule -r eucaconsole >/dev/null || :
fi


%changelog
* Tue Jun 13 2017 Garrett Holmstrom <gholms@dxc.com> - 0.1.3-1
- Version bump (0.1.3)

* Tue Feb 14 2017 Garrett Holmstrom <gholms@hpe.com> - 0.1.2-1
- Version bump (0.1.2)

* Wed Oct 26 2016 Garrett Holmstrom <gholms@hpe.com> - 0.1.1-1
- Moved policy to /usr/share/selinux/packages

* Tue Jul 12 2016 Garrett Holmstrom <gholms@hpe.com> - 0.1.0-1
- Created
