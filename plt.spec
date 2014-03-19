%define major	%{version}
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1
%define epoch 1

Name:		plt
Version:	4.2.4
Release:	3
Summary:	PLT Scheme
License:	LGPLv2+
Group:		Development/Other
Url:		http://www.plt-scheme.org
Source0:	http://download.plt-scheme.org/bundles/%{version}/plt/%{name}-%{version}-src-unix.tgz
Source1:        drscheme.png
Source2:        %{name}.rpmlintrc
Patch0:		plt-4.2.4-strfmt.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	xaw-devel
BuildRequires:	spec-helper >= 0.12
BuildRequires:	imagemagick
Epoch:		%{epoch}

%description
PLT Scheme is an umbrella name for a family of implementations of the
Scheme programming language.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{epoch}:%{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Other
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%{mklibname %{name} -d 370}

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package	mzscheme
Summary:	PLT Scheme implementation
Group:		Development/Other
Requires:	%{libname} = %{epoch}:%{version}

%description mzscheme
MzScheme is the PLT Scheme implementation. It implements
the language as described in the Revised^5 Report on the
Algorithmic Language Scheme and adds numerous extensions.

%package	mred
Summary:	PLT graphical Scheme implementation
Group:		Development/Other
Requires:	%{name}-mzscheme = %{epoch}:%{version}

%description	mred
MrEd is the PLT's graphical Scheme implementation. It embeds and
extends MzScheme with a graphical user interface (GUI) toolbox.

%package	drscheme
Summary:	PLT graphical development environment
Group:		Development/Other
Requires:	%{name}-mred = %{epoch}:%{version}

%description	drscheme
DrScheme is the graphical development environment for creating 
MzScheme and MrEd applications.

%prep
%setup -q
%patch0 -p1 -b .strfmt

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

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-drscheme.desktop << EOF
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
%exclude %{_datadir}/%{name}/doc/drscheme

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libmzscheme3m-%{version}.so
%{_libdir}/libmred3m-%{version}.so

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libmzscheme3m.so
%{_libdir}/libmred3m.so
%{_includedir}/*

%files mred
%defattr(-,root,root)
%{_libdir}/%{name}/collects/mred
%{_bindir}/mred
%{_mandir}/man1/mred.1*

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


%changelog
* Fri Jan 29 2010 Frederik Himpe <fhimpe@mandriva.org> 1:4.2.4-1mdv2010.1
+ Revision: 498295
- Update to new version 4.2.4
- Rediff strfmt patch

* Tue Jan 19 2010 Frederik Himpe <fhimpe@mandriva.org> 1:4.2.3-1mdv2010.1
+ Revision: 493840
- update to new version 4.2.3

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 1:4.2.2-1mdv2010.1
+ Revision: 462293
- update to new version 4.2.2

* Thu Jul 30 2009 Frederik Himpe <fhimpe@mandriva.org> 1:4.2.1-1mdv2010.0
+ Revision: 404824
- Update to new version 4.2.1

* Wed Mar 11 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:4.1.4-2mdv2009.1
+ Revision: 353966
- rebuild for missing binaries

* Thu Mar 05 2009 Frederik Himpe <fhimpe@mandriva.org> 1:4.1.4-1mdv2009.1
+ Revision: 349474
- Update to o new version 4.1.4
- Add patch to build with -Werror=format-security

* Fri Nov 21 2008 Frederik Himpe <fhimpe@mandriva.org> 1:4.1.3-1mdv2009.1
+ Revision: 305536
- update to new version 4.1.3

* Thu Nov 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1:4.1.2-3mdv2009.1
+ Revision: 302731
- rebuilt against new libxcb

* Wed Nov 12 2008 Funda Wang <fwang@mandriva.org> 1:4.1.2-2mdv2009.1
+ Revision: 302413
- rebuild for new xcb

* Tue Oct 28 2008 Frederik Himpe <fhimpe@mandriva.org> 1:4.1.2-1mdv2009.1
+ Revision: 298065
- update to new version 4.1.2

* Sat Oct 11 2008 Frederik Himpe <fhimpe@mandriva.org> 1:4.1.1-1mdv2009.1
+ Revision: 292135
- Update to new version 4.1.1

* Thu Sep 11 2008 Frederik Himpe <fhimpe@mandriva.org> 1:4.1-1mdv2009.0
+ Revision: 283926
- Needs epoch because of upstream change in version numbering...
- Update to new version 4.1
- Define _disable_ld_as_needed and define _disable_ld_no_undefined to
  make it link correctly with things lib libm and libdl

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Feb 06 2008 Frederik Himpe <fhimpe@mandriva.org> 372-1mdv2008.1
+ Revision: 163313
- New upstream version

* Sat Dec 22 2007 Guillaume Rousse <guillomovitch@mandriva.org> 371-1mdv2008.1
+ Revision: 136848
- reduce icons set to what is really needed
- new devel policy
- new version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 370-4mdv2008.0
+ Revision: 89555
- install binaries in standard place (fix #33658)

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Sun Aug 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 370-3mdv2008.0
+ Revision: 67139
- rebuild

* Mon Jun 25 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 370-2mdv2008.0
+ Revision: 43947
- oops, forgot adding source for icon
- compulsive pedantic neatpicking by me ;p
- from Frederik Himpe <fhimpe@telenet.be> :
  	o drop -DDONT_INLINE_NZERO_TEST CFLAG as it's no longer needed
  	o fd.o menu item & icons
  	o replace wrapper script with working symlinks

* Tue Jun 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 370-1mdv2008.0
+ Revision: 41563
- fix libtool configuration call
- use system libtool instead of bundled one
- new version
- import plt


* Wed Jun 21 2006 Guillaume Rousse <guillomovitch@mandriva.org> 350-2mdv2007.0
- fix multiarch issue
- drop old obsoletes
- less strict interdependencies
- nuke rpath

* Wed Jun 21 2006 Guillaume Rousse <guillomovitch@mandriva.org> 350-1mdv2007.0
- new version
- destdir patch

* Tue Jun 20 2006 Guillaume Rousse <guillomovitch@mandriva.org> 301-2mdv2007.0
- new version

* Fri May 19 2006 Guillaume Rousse <guillomovitch@mandriva.org> 301-1mdk
- new version
- %%mkrel
- fix multiarch includes

* Sun Jan 16 2005 Guillaume Rousse <guillomovitch@mandrake.org> 209-1mdk
- New release 209

* Thu Aug  5 2004 Guillaume Rousse <guillomovitch@mandrakesoft.com> 208-1mdk
- New release 208

* Wed Jul 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 207-3mdk 
- rebuild

* Fri Jun 04 2004 Guillaume Rousse <guillomovitch@mandrake.org> 207-2mdk 
- binaries in %%{_libdir}/%%{name}/bin, wrappers in %%{_bindir}

* Tue Jun 01 2004 Guillaume Rousse <guillomovitch@mandrake.org> 207-1mdk
- new version
- libification
- fixed scripts (Bruno T Santos <bluey@netcabo.pt>)
- rpmbuildupdate aware

* Mon Jan 12 2004 Guillaume Rousse <guillomovitch@mandrake.org> 205-2mdk
- buildrequires (slbd)

* Tue Dec 30 2003 Guillaume Rousse <guillomovitch@mandrake.org> 205-1mdk
- new version

* Fri Apr 25 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 202-6mdk
- fixed buildrequires (Stefan van der Eijk <stefan@eijk.nu>)
- quiet setup

* Sat Jan 04 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 202-5mdk
- rebuild
- fixed compiled code directory perms

* Tue Oct 08 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 202-4mdk
- fixed missing syntax collect

* Mon Oct 07 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 202-3mdk
- fixed missing bin symlink
- fixed doc

* Mon Oct 07 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 202-2mdk
- changed name to %%{name}
- set PLT_HOME to %%{_libdir}/%%{name}
- package split
- corrected license and url tags
- reworked descriptions

* Sat Oct 05 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 202-1mdk
- first mdk release
