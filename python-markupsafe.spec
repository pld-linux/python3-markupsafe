#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	markupsafe
Summary:	MarkupSafe - a XML/HTML/XHTML Markup safe string for Python 2
Summary(pl.UTF-8):	MarkupSafe - łańcuch dla Pythona 2 bezpieczny pod kątem znaczników XML/HTML/XHTML
Name:		python-%{module}
Version:	1.1.0
Release:	2
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/pypi/MarkupSafe/
Source0:	https://files.pythonhosted.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
# Source0-md5:	49e3f3230cedb7ae34faf06913db83fc
URL:		http://www.pocoo.org/projects/markupsafe/#markupsafe
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python-2to3
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
Provides:	python-MarkupSafe = %{version}-%{release}
Obsoletes:	python-MarkupSafe < 0.15-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%description -l pl.UTF-8
MarkupSafe to implementacja łańcucha znaków dla Pythona bezpiecznego
pod kątem znaczników XML/HTML/XHTML.

%package -n python3-markupsafe
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python 3
Summary(pl.UTF-8):	MarkupSafe - łańcuch dla Pythona 3 bezpieczny pod kątem znaczników XML/HTML/XHTML
Group:		Development/Languages
Requires:	python3-modules

%description -n python3-markupsafe
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%description -n python3-markupsafe -l pl.UTF-8
MarkupSafe to implementacja łańcucha znaków dla Pythona bezpiecznego
pod kątem znaczników XML/HTML/XHTML.

%prep
%setup -q -n MarkupSafe-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install

%py_postclean
# C code errantly gets installed
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/markupsafe/_speedups.c
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/markupsafe/_speedups.c
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.rst README.rst
%dir %{py_sitedir}/markupsafe
%{py_sitedir}/markupsafe/*.py[co]
%attr(755,root,root) %{py_sitedir}/markupsafe/_speedups.so
%{py_sitedir}/MarkupSafe-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-markupsafe
%defattr(644,root,root,755)
%doc LICENSE.rst README.rst
%dir %{py3_sitedir}/markupsafe
%{py3_sitedir}/markupsafe/*.py
%{py3_sitedir}/markupsafe/__pycache__
%attr(755,root,root) %{py3_sitedir}/markupsafe/_speedups.cpython-*.so
%{py3_sitedir}/MarkupSafe-%{version}-py*.egg-info
%endif
