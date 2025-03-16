#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.3.3
%define		qtver		5.15.2
%define		kpname		milou
Summary:	A dedicated search application built on top of Baloo
Name:		kp6-%{kpname}
Version:	6.3.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	81b76ff6d8789c55c3af797650ecce8c
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-kdeclarative-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-krunner-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kp6-libplasma-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A dedicated search application built on top of Baloo.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_libdir}/qt6/qml/org/kde/milou
%{_datadir}/plasma/plasmoids/org.kde.milou
%{_datadir}/metainfo/org.kde.milou.appdata.xml
