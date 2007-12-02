%define		_rel 3
%define		_java_source	1.2
%define		_java_target	1.2
%include	/usr/lib/rpm/macros.java
Summary:	HTML syntax checker and pretty printer
Summary(pl.UTF-8):	Narzędzie do sprawdzania składni HTML i ładnego drukowania
Name:		jtidy
Version:	1.0
Release:	0.20000804r7dev.%{_rel}
License:	BSD-style
Group:		Applications/Text
Source0:	http://dl.sourceforge.net/jtidy/%{name}-04aug2000r7-dev.zip
# Source0-md5:	8fa91a760f7eea722e57f8b8da4a7d5f
Source1:	%{name}.jtidy.script
Patch0:		%{name}.noapis.patch
Patch1:		%{name}-version.patch
URL:		http://jtidy.sourceforge.net/
BuildRequires:	ant >= 1.6
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jaxp_parser_impl
Requires:	xml-commons
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JTidy is a Java port of HTML Tidy, a HTML syntax checker and pretty
printer. Like its non-Java cousin, JTidy can be used as a tool for
cleaning up malformed and faulty HTML. In addition, JTidy provides a
DOM parser for real-world HTML.

%description -l pl.UTF-8
JTidy to javowy port narzędzia HTML Tidy służącego do sprawdzania
składni HTML i ładnego drukowania. Podobnie do niejavowego kuzyna
JTidy może służyć za narzędzie do czyszczenia źle sformułowanego i
błędnego HTML-a. Ponadto JTidy udostępnia analizator DOM dla HTML-a
spotykanego w rzeczywistości.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package scripts
Summary:	Utility scripts for %{name}
Summary(pl.UTF-8):	Skrypty narzędziowe dla pakietu %{name}
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils >= 0:1.5

%description scripts
Utility scripts for %{name}.

%description scripts -l pl.UTF-8
Skrypty narzędziowe dla pakietu %{name}.

%prep
%setup -q -n %{name}-04aug2000r7-dev
%patch0 -p0
%patch1 -p1

# remove all binary libs, javadocs, and included JAXP API sources
find -name '*.jar' | xargs rm -v

%build
export CLASSPATH=$(build-classpath xml-commons-apis)
%ant jar javadoc \
	-Dcompile.target=%{_java_target} \
	-Dcompile.source=%{_java_source}

%install
rm -rf $RPM_BUILD_ROOT
# jar
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a build/Tidy.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -sf %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# shell script
install -d $RPM_BUILD_ROOT%{_bindir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}

# ant.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name} << 'EOF'
jtidy xml-commons-apis
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -sf %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE NOTES doc/devel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ant.d/%{name}
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files scripts
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
