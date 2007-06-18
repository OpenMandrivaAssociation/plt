%define	name 	plt
%define version 370
%define release %mkrel 1
%define major	%{version}
%define libname %mklibname %{name} %{major}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	PLT Scheme
License:	LGPL
Group:		Development/Other
Source:		http://download.plt-scheme.org/bundles/%{version}/plt/%{name}-%{version}-src-unix.tgz
Patch0:		%{name}-370-destdir.patch
Patch1:		%{name}-370-fix-libtool-use.patch
Url:		http://www.plt-scheme.org
BuildRequires:	X11-devel
BuildRequires:	chrpath
BuildRequires:	spec-helper >= 0.12
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
PLT Scheme is an umbrella name for a family of implementations of the
Scheme programming language.

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package mzscheme
Summary:        PLT Scheme implementation
Group:          Development/Other
Requires:	%{libname} = %{version}

%description mzscheme
MzScheme is the PLT Scheme implementation. It implements
the language as described in the Revised^5 Report on the
Algorithmic Language Scheme and adds numerous extensions.

%package mred
Summary:        PLT graphical Scheme implementation
Group:          Development/Other
Requires:       %{name}-mzscheme = %{version}

%description mred
MrEd is the PLT's graphical Scheme implementation. It embeds and
extends MzScheme with a graphical user interface (GUI) toolbox.

%package drscheme
Summary:	PLT graphical development environment
Group:          Development/Other
Requires:	%{name}-mred = %{version}

%description drscheme
DrScheme is the graphical development environment for creating 
MzScheme and MrEd applications.

%prep
%setup -q
%patch0 -p 1
%patch1 -p 1

%build
cd src
%configure2_5x \
    --enable-shared \
    CFLAGS="$CFLAGS -DDONT_INLINE_NZERO_TEST"
# parallel build doesn't work
make

%install
rm -rf %{buildroot}
mkdir %{buildroot}
cd src
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%makeinstall_std

# correct installation
install -d -m 755 %{buildroot}%{_datadir}
install -d -m 755 %{buildroot}%{_libdir}/%{name}
install -d -m 755 %{buildroot}%{_libdir}/%{name}/bin
mv %{buildroot}%{_bindir}/mred %{buildroot}%{_libdir}/%{name}/bin 
mv %{buildroot}%{_bindir}/mzscheme %{buildroot}%{_libdir}/%{name}/bin 

# install wrappers
cat > %{buildroot}%{_bindir}/mzscheme <<EOF
#!/bin/sh
# mzscheme wrapper

if [ "$PLTHOME" = '' ] ; then
  PLTHOME="/usr/lib/plt"
  export PLTHOME
fi

exec \${PLTHOME}/bin/mzscheme
EOF
chmod 755 %{buildroot}%{_bindir}/mzscheme

cat > %{buildroot}%{_bindir}/mred <<EOF
#!/bin/sh
# mred wrapper

if [ "$PLTHOME" = '' ] ; then
  PLTHOME="/usr/lib/plt"
  export PLTHOME
fi

exec \${PLTHOME}/bin/mred
EOF
chmod 755 %{buildroot}%{_bindir}/mred

# correct path in scripts
perl -pi -e 's|PLTHOME=".*"|PLTHOME="%{_libdir}/%{name}"|' %{buildroot}%{_bindir}/*
#perl -pi -e 's|\${PLTHOME}/bin|%{_bindir}|' %{buildroot}%{_bindir}/*

# correct perms
find %{buildroot}%{_libdir}/%{name}/collects -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/%{name}/doc -type d -exec chmod 755 {} \;

# nuke rpath
chrpath -d  %{buildroot}%{_libdir}/plt/bin/*

%multiarch_includes %{buildroot}%{_includedir}/plt/mzconfig.h

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files mzscheme
%defattr(-,root,root)
%doc readme.txt
%{_libdir}/%{name}
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}
%exclude %{_bindir}/mred
%exclude %{_bindir}/drscheme
%exclude %{_mandir}/man1/mred.1*
%exclude %{_mandir}/man1/drscheme.1*
%exclude %{_libdir}/%{name}/collects/mred
%exclude %{_libdir}/%{name}/collects/drscheme
%exclude %{_libdir}/%{name}/bin/mred
%exclude %{_datadir}/%{name}/doc/mred
%exclude %{_datadir}/%{name}/doc/drscheme

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libmzscheme3m-%{version}.so
%{_libdir}/libmred3m-%{version}.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libmzscheme3m.so
%{_libdir}/libmred3m.so
%{_libdir}/*.la
%{_includedir}/*

%files mred
%defattr(-,root,root)
%{_libdir}/%{name}/collects/mred
%{_libdir}/%{name}/bin/mred
%{_bindir}/mred
%{_mandir}/man1/mred.1*
%{_datadir}/%{name}/doc/mred

%files drscheme
%defattr(-,root,root)
%{_libdir}/%{name}/collects/drscheme
%{_bindir}/drscheme
%{_mandir}/man1/drscheme.1*
%{_datadir}/%{name}/doc/drscheme
