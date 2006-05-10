%define		_rel 1.1
Summary:	HTML syntax checker and pretty printer
Name:		jtidy
Version:	1.0
Release:	0.20000804r7dev.%{_rel}
License:	BSD-style
URL:		http://jtidy.sourceforge.net/
Source0:	http://dl.sourceforge.net/jtidy/%{name}-04aug2000r7-dev.zip
# Source0-md5:	8fa91a760f7eea722e57f8b8da4a7d5f
Source1:	%{name}.jtidy.script
Patch0:		%{name}.noapis.patch
Group:		Applications/Text
BuildRequires:	jakarta-ant >= 1.6
Requires:	jaxp_parser_impl
Requires:	xml-commons
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%package scripts
Summary:	Utility scripts for %{name}
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils >= 0:1.5

%description scripts
Utility scripts for %{name}.

%prep
%setup -q -n %{name}-04aug2000r7-dev
%patch0 -p0
# remove all binary libs, javadocs, and included JAXP API sources
find . -name "*.jar" -exec rm -f {} \;
rm -rf doc/api src/org/xml src/org/w3c/dom
# correct silly permissions
chmod -R go=u-w *

%build
export CLASSPATH=$(build-classpath xml-commons-apis)
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a build/Tidy.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
# jar versioning
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do \
ln -s ${jar} `echo $jar| %{__sed} "s|-%{version}||g"`; done)

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -s %{name}-%{version} %{name})

# shell script
install -d $RPM_BUILD_ROOT%{_bindir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}

# ant.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name} << EOF
jtidy xml-commons-apis
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE NOTES doc/devel
%{_javadir}/*
%config(noreplace) %{_sysconfdir}/ant.d/%{name}

%files javadoc
%defattr(644,root,root,755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}

%files scripts
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
