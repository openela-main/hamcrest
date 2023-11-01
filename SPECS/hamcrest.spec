%bcond_with bootstrap

%global upstream_version %(echo %{version} | tr '~' '-')

Name:           hamcrest
Version:        2.2
Release:        7%{?dist}
Summary:        Library of matchers for building test expressions
License:        BSD
URL:            https://github.com/hamcrest/JavaHamcrest
BuildArch:      noarch

Source0:        https://github.com/hamcrest/JavaHamcrest/archive/v%{upstream_version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://repo1.maven.org/maven2/org/hamcrest/hamcrest/%{upstream_version}/hamcrest-%{upstream_version}.pom

Patch0:         0001-Fix-build-with-OpenJDK-11.patch

BuildRequires:  maven-local
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  mvn(junit:junit)
%endif

Provides:       hamcrest-core = %{version}-%{release}
Obsoletes:      hamcrest-core < 1.3-32
Obsoletes:      hamcrest-demo < 1.3-32

%description
Provides a library of matcher objects (also known as constraints or predicates)
allowing 'match' rules to be defined declaratively, to be used in other
frameworks. Typical scenarios include testing frameworks, mocking libraries and
UI validation rules.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n JavaHamcrest-%{upstream_version}
%patch0 -p1

rm -rf docs
rm -rf *gradle*
rm -rf */*.gradle

mv hamcrest/src .
rm -rf hamcrest
rm -rf hamcrest-core
rm -rf hamcrest-integration
rm -rf hamcrest-library

cp -p %{SOURCE1} pom.xml
%pom_add_dep junit:junit::test
%pom_xpath_inject pom:project '
<build>
	<plugins>
		<plugin>
		<groupId>org.apache.maven.plugins</groupId>
		<artifactId>maven-compiler-plugin</artifactId>
		<version>3.8.1</version>
		<configuration>
			<source>1.8</source>
			<target>1.8</target>
		</configuration>
		</plugin>
	</plugins>
</build>'

%mvn_alias org.hamcrest:hamcrest org.hamcrest:hamcrest-all
%mvn_alias org.hamcrest:hamcrest org.hamcrest:hamcrest-core
%mvn_alias org.hamcrest:hamcrest org.hamcrest:hamcrest-library

sed -i 's/\r//' LICENSE.txt

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2.2-7
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 09 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-6
- Rebuild to workaround DistroBaker issue

* Tue Jun 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-5
- Bootstrap Maven for CentOS Stream 9

* Tue Jun 01 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-4
- Obsolete hamcrest-core and -demo
- Resolves: rhbz#1966269

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-3
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:1.3-29
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jun 24 2020 Roland Grunberg <rgrunber@redhat.com> - 0:1.3-28
- Use source/target 1.6 to build against Java 11.
- Disable checking of remote javadoc links.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-2
- Mass rebuild for javapackages-tools 201902

* Thu Oct 17 2019 Marian Koncek <mkoncek@redhat.com> - 2.2-1
- Update to upstream version 2.2

* Wed Sep 18 2019 Marian Koncek <mkoncek@redhat.com> - 2.2~rc1-1
- Update to upstream version 2.2~rc1

* Mon Aug 19 2019 Marian Koncek <mkoncek@redhat.com> - 2.1-1
- Update to upstream version 2.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-24
- Mass rebuild for javapackages-tools 201901

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-22
- Elimitate race condition when injecting JAR manifest
- Resolves: rhbz#1495234
- Remove bogus hamcrest-text JAR

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Michael Simacek <msimacek@redhat.com> - 0:1.3-20
- Fix mistake in mvn_artifact invocation

* Tue Mar 21 2017 Michael Simacek <msimacek@redhat.com> - 0:1.3-19
- Install with XMvn
- Update upstream URL
- Build from github source
- Specfile cleanup

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Michael Simacek <msimacek@redhat.com> - 0:1.3-17
- Port to current QDox

* Mon Jan 02 2017 Michael Simacek <msimacek@redhat.com> - 0:1.3-16
- Try to fix nondeterministic failures by forking javac

* Mon Oct  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-15
- Remove build-requires on perl

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-12
- Disable javadoc doclint

* Tue Feb 24 2015 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-11
- Add obsoletes in core to the main package to ease updates.

* Mon Feb 23 2015 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-10
- Split hamcrest-core subpackage to allow other frameworks to reduce deps.

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-9
- Port to QDox 2.0
- Resolves: rhbz#1166700

* Wed Jul 30 2014 Mat Booth <mat.booth@redhat.com> - 0:1.3-8
- Fix FTBFS
- Always build integration jar (removes some complexity from the spec)
- Drop unused patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.3-6
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-5
- Update osgi manifests.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Alexander Kurtakov <akurtako@redhat.com> 0:1.3-3
- Build against easymock3.

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 0:1.3-2
- Add easymock2 to classpath (Resolves: #979501)

* Thu Mar 21 2013 Tomas Radej <tradej@redhat.com> - 0:1.3-1
- Updated to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1-21
- Fix core manifest typo ";" -> ","

* Tue Aug 14 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:1.1-20
- Remove attributes in Export-Package header of hamcrest-core
  manifest.

* Wed Aug 1 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-19
- Add OSGi metadata to hamcrest-generator.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-18
- Actually build integration.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-17
- Add OSGi metadata to hamcrest-integration.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-16
- Remove checksums from manifest.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-15
- Add OSGi metadata to hamcrest-text.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-14
- Add OSGi metadata for hamcrest-library.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-11
- Do not BR/R openjdk6 but java >= 1:1.6.0
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Mat Booth <fedora@matbooth.co.uk> 0:1.1-9.4
- Fix FTBFS due to zip BR - RHBZ #661011.

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-9.3
- Drop gcj support.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-9.2
- Add OSGi manifest for hamcrest-core.
- Make javadoc package noarch.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-7.1
- Fedora-specific: enable GCJ support
- Fedora-specific: build with java 1.6.0
- Fedora-specific: disable integration and tests

* Mon Nov 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-7
- update summary and description

* Tue Oct 28 2008 David Walluck <dwalluck@redhat.com> 0:1.1-6
- make demo dependency on testng conditional

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-5
- fix GCJ file list
- simplify build by always setting OPT_JAR_LIST

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-4
- add epoch to demo Requires

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-3
- set -Dant.build.javac.source=1.5

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-2
- add options to build without integration, jarjar, and tests
- allow build with java-devel >= 1.5.0
- remove javadoc scriptlets
- use more strict file list
- fix maven directory ownership
- add non-versioned symlink for demo
- fix GCJ requires
- fix eol in LICENSE.txt
- remove Vendor and Distribution

* Tue Feb 19 2008 Ralph Apel <r.apel@r-apel.de> - 0:1.1-1jpp
- 1.1

* Mon Feb 11 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-4jpp
- Fix versioned jar name, was junit-4.3.1
- Restore Epoch

* Fri Jan 25 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-3jpp
- build and upload noarch packages
- Add pom and depmap frag
- BR java-devel = 1.5.0
- Restore Vendor, Distribution from macros

* Tue Aug 07 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-2jpp
- Set gcj_support to 0 to work around problems with GCJ.
- Fix buglet with the gcj post/postun if statement.
- Fix tab / space problems.
- Fix buildroot.
- Update Summary.
- Convert html files to Unix file endings.
- Disable aot-compile-rpm because it's not working ATM.

* Mon Jul 09 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-1jpp
- 4.3.1.

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1.fc7
- Add dist tag

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1
- Committed on behalf of Tania Bento <tbento@redhat.com>
- Update per Fedora review process
- Resolves rhbz#225954

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-3jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 0:3.8.2-2jpp_3fc
- Require(post/postun): coreutils

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_2fc
- Rebuilt.

* Thu Jun 22 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_1fc
- Upgrade to 3.8.2
- Added conditional native compilation.
- Fix path where demo is located.

* Fri Mar 03 2006 Ralph Apel <r.apel at r-apel.de> - 0:3.8.2-1jpp
- First JPP-1.7 release

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %%{_datadir}/%%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
