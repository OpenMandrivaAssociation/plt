%define	name 	plt
%define version 371
%define release %mkrel 1
%define major	%{version}
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	PLT Scheme
License:	LGPL
Group:		Development/Other
Url:		http://www.plt-scheme.org
Source0:	http://download.plt-scheme.org/bundles/%{version}/plt/%{name}-%{version}-src-unix.tgz
Source1:        drscheme.png
BuildRequires:	X11-devel
BuildRequires:	spec-helper >= 0.12
BuildRequires:	imagemagick
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
PLT Scheme is an umbrella name for a family of implementations of the
Scheme programming language.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} -d 370}

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package	mzscheme
Summary:	PLT Scheme implementation
Group:		Development/Other
Requires:	%{libname} = %{version}

%description mzscheme
MzScheme is the PLT Scheme implementation. It implements
the language as described in the Revised^5 Report on the
Algorithmic Language Scheme and adds numerous extensions.

%package	mred
Summary:	PLT graphical Scheme implementation
Group:		Development/Other
Requires:	%{name}-mzscheme = %{version}

%description	mred
MrEd is the PLT's graphical Scheme implementation. It embeds and
extends MzScheme with a graphical user interface (GUI) toolbox.

%package	drscheme
Summary:	PLT graphical development environment
Group:		Development/Other
Requires:	%{name}-mred = %{version}

%description	drscheme
DrScheme is the graphical development environment for creating 
MzScheme and MrEd applications.

%prep
%setup -q

%build
cd src
%configure2_5x \
    --enable-shared
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

# correct perms
find %{buildroot}%{_libdir}/%{name}/collects -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/%{name}/doc -type d -exec chmod 755 {} \;

%multiarch_includes %{buildroot}%{_includedir}/plt/mzconfig.h

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-drscheme.desktop << EOF
[Desktop Entry]
Name=DrScheme
Comment=Scheme IDE
Exec=drscheme
Icon=drscheme
Terminal=false
Type=Application
StartupNotify=true
Categories=Development;IDE;
EOF

mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale "48X48" %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/drscheme.png
convert -scale "16x16" %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/drscheme.png
convert -scale "32x32" %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/drscheme.png
convert -scale "48x48" %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/drscheme.png

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
%exclude %{_datadir}/%{name}/doc/mred
%exclude %{_datadir}/%{name}/doc/drscheme

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libmzscheme3m-%{version}.so
%{_libdir}/libmred3m-%{version}.so

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libmzscheme3m.so
%{_libdir}/libmred3m.so
%{_libdir}/*.la
%{_includedir}/*

%files mred
%defattr(-,root,root)
%{_libdir}/%{name}/collects/mred
%{_bindir}/mred
%{_mandir}/man1/mred.1*
%{_datadir}/%{name}/doc/mred

%files drscheme
%defattr(-,root,root)
%{_libdir}/%{name}/collects/drscheme
%{_bindir}/drscheme
%{_mandir}/man1/drscheme.1*
%{_datadir}/%{name}/doc/drscheme
%{_datadir}/pixmaps/drscheme.png
%{_iconsdir}/hicolor/16x16/apps/drscheme.png
%{_iconsdir}/hicolor/32x32/apps/drscheme.png
%{_iconsdir}/hicolor/48x48/apps/drscheme.png
%{_datadir}/applications/mandriva-drscheme.desktop
