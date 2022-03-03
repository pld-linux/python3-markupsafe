#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	markupsafe
Summary:	Implements a XML/HTML/XHTML Markup safe string for Python 3
Summary(pl.UTF-8):	MarkupSafe - łańcuch dla Pythona 3 bezpieczny pod kątem znaczników XML/HTML/XHTML
Name:		python3-%{module}
Version:	2.0.1
Release:	2
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/markupsafe/
Source0:	https://files.pythonhosted.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
# Source0-md5:	892e0fefa3c488387e5cc0cad2daa523
URL:		https://markupsafe.palletsprojects.com/
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%if %{with doc}
BuildRequires:	python3-pallets-sphinx-themes >= 1.1.0
BuildRequires:	python3-sphinx_issues >= 1.2.0
BuildRequires:	python3-sphinxcontrib-log-cabinet >= 1.0.1
BuildRequires:	sphinx-pdg-3 >= 1.8.0
%endif
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%description -l pl.UTF-8
MarkupSafe to implementacja łańcucha znaków dla Pythona bezpiecznego
pod kątem znaczników XML/HTML/XHTML.

%package apidocs
Summary:	API documentation for Python MarkupSafe module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona MarkupSafe
Group:		Documentation

%description apidocs
API documentation for Python MarkupSafe module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona MarkupSafe.

%prep
%setup -q -n MarkupSafe-%{version}

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/$(echo build-3/lib.*) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/markupsafe/_speedups.c

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%dir %{py3_sitedir}/markupsafe
%{py3_sitedir}/markupsafe/*.py
%{py3_sitedir}/markupsafe/__pycache__
%{py3_sitedir}/markupsafe/_speedups.pyi
%{py3_sitedir}/markupsafe/py.typed
%attr(755,root,root) %{py3_sitedir}/markupsafe/_speedups.cpython-*.so
%{py3_sitedir}/MarkupSafe-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
