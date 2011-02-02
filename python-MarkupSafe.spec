%define 	module	MarkupSafe
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python
Summary(pl.UTF-8):	-
Name:		python-%{module}
Version:	0.11
Release:	0.2
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/M/MarkupSafe/%{module}-%{version}.tar.gz
# Source0-md5:	48d445941c16d6aa55caf8e148fc0911
URL:		http://www.pocoo.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
#Requires:		python-libs
Requires:		python-modules
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implements a XML/HTML/XHTML Markup safe string for Python.

%description -l pl.UTF-8

%prep
%setup -q -n %{module}-%{version}

%build
# CFLAGS is only for arch packages - remove on noarch packages
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitedir}/markupsafe/*.py[co]
%dir %attr(755,root,root) %{py_sitedir}/markupsafe
%attr(755,root,root) %{py_sitedir}/markupsafe/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-*.egg-info
%endif
