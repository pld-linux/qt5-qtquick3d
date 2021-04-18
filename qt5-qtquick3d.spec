#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtquick3d
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Quick3D libraries
Summary(pl.UTF-8):	Biblioteki Qt5 Quick3D
Name:		qt5-%{orgname}
Version:	5.15.2
Release:	1
License:	GPL v3+ or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	d4379fd99acb1d4cc960c52ca646013a
Patch0:		%{name}-system-assimp.patch
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	assimp-devel >= 5.0.0
BuildRequires:	pkgconfig
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
BuildRequires:	qt5-doc-common >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Quick3D libraries.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera biblioteki Qt5 Quick3D.

%package -n Qt5Quick3D
Summary:	The Qt5 Quick3D library
Summary(pl.UTF-8):	Biblioteka Qt5 Quick3D
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}
Requires:	assimp >= 5.0.0

%description -n Qt5Quick3D
Qt5 Quick3D libraries.

%description -n Qt5Quick3D -l pl.UTF-8
Biblioteki Qt5 Quick3D.

%package -n Qt5Quick3D-devel
Summary:	Qt5 Quick3D - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Quick3D - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}

%description -n Qt5Quick3D-devel
Qt5 Quick3D - development files.

%description -n Qt5Quick3D-devel -l pl.UTF-8
Biblioteka Qt5 Quick3D - pliki programistyczne.

%package doc
Summary:	Qt5 Quick3D documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick3D w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Quick3D documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick3D w formacie HTML.

%package doc-qch
Summary:	Qt5 Quick3D documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick3D w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Quick3D documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick3D w formacie QCH.

%package examples
Summary:	Qt5 Quick3D examples
Summary(pl.UTF-8):	Przykłady do bibliotek Qt5 Quick3D
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Quick3D examples.

%description examples -l pl.UTF-8
Przykłady do bibliotek Qt5 Quick3D.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}
%patch0 -p1

%build
qmake-qt5 -- \
	-system-quick3d-assimp

%{__make}

%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# remove compiled examples (package only sources)
for d in $RPM_BUILD_ROOT%{_examplesdir}/qt5/quick3d/* ; do
	[ -d "$d" ] && %{__rm} "$d/$(basename $d)"
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Quick3D -p /sbin/ldconfig
%postun	-n Qt5Quick3D -p /sbin/ldconfig

%files -n Qt5Quick3D
%defattr(644,root,root,755)
%doc README.md dist/changes-*
# R: Qt5Core Qt5Gui Qt5Qml Qt5QmlModels Qt5Quick Qt5Quick3DRender Qt5Quick3DRuntimeRender Qt5Quick3DUtils
%attr(755,root,root) %{_libdir}/libQt5Quick3D.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Quick3D.so.5
# R: Qt5Core Qt5Gui Qt5Quick3DUtils
%attr(755,root,root) %{_libdir}/libQt5Quick3DAssetImport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Quick3DAssetImport.so.5
# R: Qt5Core Qt5Gui Qt5Quick3DUtils
%attr(755,root,root) %{_libdir}/libQt5Quick3DRender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Quick3DRender.so.5
# R: Qt5Core Qt5Gui Qt5Quick3DUtils Qt5Quick3DRender Qt5Quick3DAssetImport
%attr(755,root,root) %{_libdir}/libQt5Quick3DRuntimeRender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Quick3DRuntimeRender.so.5
# R: Qt5Core Qt5Gui
%attr(755,root,root) %{_libdir}/libQt5Quick3DUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Quick3DUtils.so.5
# R: Qt5Core Qt5Quick3DAssetImport
%attr(755,root,root) %{qt5dir}/bin/balsam
# R: Qt5Core Qt5Gui Qt5Quick3DAssetImport
%attr(755,root,root) %{qt5dir}/bin/meshdebug
%dir %{qt5dir}/plugins/assetimporters
# Qt5Core Qt5Gui Qt5Quick3DAssetImport assimp
%attr(755,root,root) %{qt5dir}/plugins/assetimporters/libassimp.so
# Qt5Core Qt5Gui Qt5Quick3DAssetImport
%attr(755,root,root) %{qt5dir}/plugins/assetimporters/libuip.so
%dir %{qt5dir}/qml/QtQuick3D
# R: Qt5Core Qt5Qml Qt5Quick Qt5Quick3D
%attr(755,root,root) %{qt5dir}/qml/QtQuick3D/libqquick3dplugin.so
%{qt5dir}/qml/QtQuick3D/plugins.qmltypes
%{qt5dir}/qml/QtQuick3D/qmldir
%{qt5dir}/qml/QtQuick3D/designer
%dir %{qt5dir}/qml/QtQuick3D/Effects
# R: Qt5Core Qt5Qml Qt5Quick3D
%attr(755,root,root) %{qt5dir}/qml/QtQuick3D/Effects/libqtquick3deffectplugin.so
%{qt5dir}/qml/QtQuick3D/Effects/plugins.qmltypes
%{qt5dir}/qml/QtQuick3D/Effects/qmldir
%{qt5dir}/qml/QtQuick3D/Effects/*.qml
%{qt5dir}/qml/QtQuick3D/Effects/designer
%{qt5dir}/qml/QtQuick3D/Effects/maps
%dir %{qt5dir}/qml/QtQuick3D/Helpers
# R: Qt5Core Qt5Gui Qt5Qml Qt5Quick3D
%attr(755,root,root) %{qt5dir}/qml/QtQuick3D/Helpers/libqtquick3dhelpersplugin.so
%{qt5dir}/qml/QtQuick3D/Helpers/plugins.qmltypes
%{qt5dir}/qml/QtQuick3D/Helpers/qmldir
%{qt5dir}/qml/QtQuick3D/Helpers/*.qml
%{qt5dir}/qml/QtQuick3D/Helpers/meshes
%dir %{qt5dir}/qml/QtQuick3D/Materials
# R: Qt5Core Qt5Qml Qt5Quick3D
%attr(755,root,root) %{qt5dir}/qml/QtQuick3D/Materials/libqtquick3dmaterialplugin.so
%{qt5dir}/qml/QtQuick3D/Materials/plugins.qmltypes
%{qt5dir}/qml/QtQuick3D/Materials/qmldir
%{qt5dir}/qml/QtQuick3D/Materials/*.qml
%{qt5dir}/qml/QtQuick3D/Materials/designer
%{qt5dir}/qml/QtQuick3D/Materials/maps

%files -n Qt5Quick3D-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Quick3D.so
%attr(755,root,root) %{_libdir}/libQt5Quick3DAssetImport.so
%attr(755,root,root) %{_libdir}/libQt5Quick3DRender.so
%attr(755,root,root) %{_libdir}/libQt5Quick3DRuntimeRender.so
%attr(755,root,root) %{_libdir}/libQt5Quick3DUtils.so
%{_libdir}/libQt5Quick3D.prl
%{_libdir}/libQt5Quick3DAssetImport.prl
%{_libdir}/libQt5Quick3DRender.prl
%{_libdir}/libQt5Quick3DRuntimeRender.prl
%{_libdir}/libQt5Quick3DUtils.prl
%{_includedir}/qt5/QtQuick3D
%{_includedir}/qt5/QtQuick3DAssetImport
%{_includedir}/qt5/QtQuick3DRender
%{_includedir}/qt5/QtQuick3DRuntimeRender
%{_includedir}/qt5/QtQuick3DUtils
%{_pkgconfigdir}/Qt5Quick3D.pc
%{_pkgconfigdir}/Qt5Quick3DAssetImport.pc
%{_pkgconfigdir}/Qt5Quick3DRender.pc
%{_pkgconfigdir}/Qt5Quick3DRuntimeRender.pc
%{_pkgconfigdir}/Qt5Quick3DUtils.pc
%{_libdir}/cmake/Qt5Quick3D
%{_libdir}/cmake/Qt5Quick3DAssetImport
%{_libdir}/cmake/Qt5Quick3DRender
%{_libdir}/cmake/Qt5Quick3DRuntimeRender
%{_libdir}/cmake/Qt5Quick3DUtils
%{qt5dir}/mkspecs/modules/qt_lib_quick3d.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3d_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3dassetimport.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3dassetimport_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3drender.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3drender_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3druntimerender.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3druntimerender_private.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3dutils.pri
%{qt5dir}/mkspecs/modules/qt_lib_quick3dutils_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtquick3d

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtquick3d.qch
%endif

%files examples
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
%{_examplesdir}/qt5/quick3d
