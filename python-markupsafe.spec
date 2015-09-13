#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	markupsafe
Summary:	MarkupSafe - a XML/HTML/XHTML Markup safe string for Python 2
Summary(pl.UTF-8):	MarkupSafe - łańcuch dla Pythona 2 bezpieczny pod kątem znaczników XML/HTML/XHTML
Name:		python-%{module}
Version:	0.23
Release:	4
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/pypi/MarkupSafe
Source0:	https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
# Source0-md5:	f5ab3deee4c37cd6a922fb81e730da6e
URL:		http://www.pocoo.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
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
%setup -qc
mv MarkupSafe-%{version} py2
# for %doc
cp -p py2/{AUTHORS,LICENSE,README.rst} .

%if %{with python3}
cp -a py2 py3
2to3 --write --nobackups py3
%endif

%build
%if %{with python2}
cd py3
# CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build
%{?with_tests:%{__python} setup.py test}
cd ..
%endif

%if %{with python3}
cd py3
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build
%{?with_tests:%{__python3} setup.py test}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
cd py2
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# C code errantly gets installed
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/markupsafe/_speedups.c
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
cd ..
%endif

%if %{with python3}
cd py3
%{__python3} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT


# C code errantly gets installed
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/markupsafe/_speedups.c
cd ..
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%dir %{py_sitedir}/markupsafe
%{py_sitedir}/markupsafe/*.py[co]
%attr(755,root,root) %{py_sitedir}/markupsafe/_speedups.so
%{py_sitedir}/MarkupSafe-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-markupsafe
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%dir %{py3_sitedir}/markupsafe
%{py3_sitedir}/markupsafe/*.py
%{py3_sitedir}/markupsafe/__pycache__
%attr(755,root,root) %{py3_sitedir}/markupsafe/_speedups.cpython-*.so
%{py3_sitedir}/MarkupSafe-%{version}-py*.egg-info
%endif
