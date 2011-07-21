%define tarname automake-1.4-p6

Summary:    A GNU tool for automatically creating Makefiles
Name:       automake14
Version:    1.4p6
Release:    19.2%{?dist}
License:    GPLv2+
Group:      Development/Tools
URL:        http://sources.redhat.com/automake
Source:     ftp://ftp.gnu.org/gnu/automake/%{tarname}.tar.gz
Patch1:     automake-1.4-libtoolize.patch
Patch2:     automake-1.4-subdir.patch
Patch3:     automake-1.4-backslash.patch
Patch6:     automake-1.4-tags.patch
Patch7:     automake-1.4-subdirs-89656.patch
Patch8:     automake14-info.patch
Patch9:     automake-1.4-p6-CVE-2009-4029.patch
Conflicts:  automake < 1.5
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info
Buildrequires:  texinfo
BuildArch:  noarch
Buildroot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Automake is a tool for automatically generating
`Makefile.in' files compliant with the GNU Coding Standards.

This package contains Automake 1.4, an older version of Automake.
You should install it if you need to run automake in a project that
has not yet been updated to work with newer versions of Automake.

%prep
%setup -q -n %{tarname}
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
mv automake.texi automake14.texi
rm automake.info

%build
%configure
make %{?_smp_mflags}

## 5 of 194 tests fail
## (cygwin32.test error.test pluseq2.test pluseq3.test xsource.test)
#make check 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## create this dir empty so we can own it
mkdir -p $RPM_BUILD_ROOT%{_datadir}/aclocal

rm $RPM_BUILD_ROOT%{_bindir}/automake $RPM_BUILD_ROOT%{_bindir}/aclocal
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/*-1.4
%{_datadir}/aclocal*/
%{_datadir}/automake-1.4/
%{_infodir}/*

%changelog
* Tue Feb 16 2010 Karsten Hopp <karsten@redhat.com> 1.4p6-19.2
- fix CVE-2009-4029

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.4p6-19.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4p6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4p6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4p6-17
- fix license tag

* Fri Jun 13 2008 Karsten Hopp <karsten@redhat.com> 1.4p6-16
- rebuild to fix vendor tag (#451242)

* Mon Feb 19 2007 Karsten Hopp <karsten@redhat.com> 1.4p6-15
- drop autoconf BR
- drop perl requirement

* Thu Feb 15 2007 Karsten Hopp <karsten@redhat.com> 1.4p6-14
- misc. fixes for review

* Mon Jun 12 2006 Karsten Hopp <karsten@redhat.de> 1.4p6-13
- don't run autoreconf during build (#194735)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Sep 28 2004 Warren Togami <wtogami@redhat.com> - 1.4p6-12
- trim docs

* Thu Sep 23 2004 Daniel Reed <djr@redhat.com> - 1.4p6-10
- rebuilt for dist-fc3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec  9 2003 Jens Petersen <petersen@redhat.com> - 1.4p6-8
- buildrequire texinfo (#111170) [mvd@mylinux.com.ua]

* Sat Apr 26 2003 Jens Petersen <petersen@redhat.com> - 1.4p6-7
- add automake-1.4-subdirs-89656.patch (#89656) [thanks to hjl@gnu.org]
- License not Copyright
- update source url
- don't prerequire install-info
- remove unwanted files rather than excluding them

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Nov 23 2002 Jens Petersen <petersen@redhat.com> 1.4p6-4.1
- exclude unwanted files rather than removing them

* Sat Nov 23 2002 Jens Petersen <petersen@redhat.com> 1.4p6-4
- remove bin and info files not for manifest
- update url (#77325)

* Fri Sep  5 2002 Jens Petersen <petersen@redhat.com> 1.4p6-3
- bring back COPYING and INSTALL in datadir

* Fri Aug 16 2002 Jens Petersen <petersen@redhat.com> 1.4p6-2
- conflict with automake < 1.5, to prevent both automake-1.4 and automake14
  from being installed at the same time (#71626)

* Mon Jul 29 2002 Jens Petersen <petersen@redhat.com> - 1.4p6-1
- 1.4-p6 with versioning from upstream
- versioning and lisp patches no longer required
- include the info files in the docs dir
- remove doc files from the automake-1.4 datadir.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan 18 2002 Jens Petersen <petersen@redhat.com> - 1.4p5-1
- new package based on automake-1.4p5-3
- add version suffix to prgram names and data directories
- no info files, since only 1.5 info files will be installed

* Wed Nov 14 2001 Jakub Jelinek <jakub@redhat.com> - 1.4p5-3
- fix lisp.am bug

* Fri Aug 24 2001 Jens Petersen <petersen@redhat.com> - 1.4p5-2
- dont raise error when there is source in a subdirectory (bug #35156).
  This was preventing automake from working in binutuls/gas 
  [patch from HJ Lu <hjl@gnu.org>]
- format long lines of output properly with backslash + newlines as in 1.4
  (bug #35259) [patch from HJ Lu <hjl@gnu.org>]

* Sat Jul 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.4-p5, fixes #48788

* Tue Jun 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add the patch from #20559
- really update to 1.4-p4

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.4-p4

* Sat May 12 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.4-p1 to work with libtool-1.4

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bug #8870

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- revert to pristine automake-1.4.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- arm netwinder patch

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- add patches from CVS for 6.0beta1

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.4.

* Mon Nov 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.3b.
- add URL.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to 1.3

* Tue Oct 28 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot; added aclocal files

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- made it a noarch package

* Thu Oct 16 1997 Michael Fulbright <msf@redhat.com>
- Fixed some tag lines to conform to 5.0 guidelines.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- updated to 1.2

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- first version (1.0)
