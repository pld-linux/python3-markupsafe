%define 	module	MarkupSafe
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python
Name:		python-%{module}
Version:	0.15
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/M/MarkupSafe/%{module}-%{version}.tar.gz
# Source0-md5:	4e7c4d965fe5e033fa2d7bb7746bb186
URL:		http://www.pocoo.org/
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implements a XML/HTML/XHTML Markup safe string for Python.

%prep
%setup -q -n %{module}-%{version}

%build
# CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/markupsafe/_speedups.c

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitedir}/markupsafe/*.py[co]
%dir %{py_sitedir}/markupsafe
%attr(755,root,root) %{py_sitedir}/markupsafe/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-*.egg-info
%endif
