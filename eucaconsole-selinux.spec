%global selinux_variants mls targeted

Name:           eucaconsole-selinux
Version:        0.1.0
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
for variant in %{selinux_variants}; do
    make NAME=${variant}
    mv eucaconsole.pp eucaconsole.pp.${variant}
    make NAME=${variant} clean
done


%install
for variant in %{selinux_variants}; do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/selinux/${variant}
    install -p -m 0644 eucaconsole.pp.${variant} $RPM_BUILD_ROOT%{_datadir}/selinux/${variant}/eucaconsole.pp
done
mkdir -p $RPM_BUILD_ROOT%{_datadir}/selinux/devel/include/contrib
install -p -m 0644 eucaconsole.if $RPM_BUILD_ROOT%{_datadir}/selinux/devel/include/contrib/eucaconsole.if


%files
%license COPYING
%{_datadir}/selinux/devel/include/contrib/eucaconsole.if
%{_datadir}/selinux/*/eucaconsole.pp


%post
if /usr/sbin/selinuxenabled; then
    for variant in %{selinux_variants}; do
        /usr/sbin/semodule -s ${variant} -i %{_datadir}/selinux/${variant}/eucaconsole.pp >/dev/null || :
    done
fi


%postun
if [ $1 -eq 0 ] && /usr/sbin/selinuxenabled; then
    for variant in %{selinux_variants}; do
        /usr/sbin/semodule -s ${variant} -r eucaconsole >/dev/null || :
    done
fi


%changelog
* Tue Jul 12 2016 Garrett Holmstrom <gholms@hpe.com> - 0.1.0-1
- Created
