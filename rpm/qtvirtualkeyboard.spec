%global qt_version 5.15.8

%{?opt_qt5_default_filter}

Summary: Qt5 - VirtualKeyboard component
Name: opt-qt5-qtvirtualkeyboard
Version: 5.15.8
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://qt.io
Source0: %{name}-%{version}.tar.bz2

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel >= %{qt_version}
BuildRequires: opt-qt5-qtsvg-devel >= %{qt_version}

Requires: opt-qt5-qtbase-gui >= %{qt_version}
Requires: opt-qt5-qtdeclarative >= %{qt_version}
Requires: opt-qt5-qtsvg >= %{qt_version}

# version unknown
Provides: bundled(libpinyin)

%description
The Qt Virtual Keyboard project provides an input framework and reference keyboard frontend
for Qt 5.  Key features include:
* Customizable keyboard layouts and styles with dynamic switching.
* Predictive text input with word selection.
* Character preview and alternative character view.
* Automatic capitalization and space insertion.
* Scalability to different resolutions.
* Support for different character sets (Latin, Simplified/Traditional Chinese, Hindi, Japanese, Arabic, Korean, and others).
* Support for most common input languages, with possibility to easily extend the language support.
* Left-to-right and right-to-left input.
* Hardware key support for 2-way and 5-way navigation.
* Handwriting support, with gestures for fullscreen input.
* Audio feedback.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5} \
  CONFIG+=lang-all

# have to restart build several times due to bug in sb2
%make_build || chmod -R ugo+r . || true
%make_build || chmod -R ugo+r . || true
%make_build || chmod -R ugo+r . || true
%make_build



%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.*
%{_opt_qt5_libdir}/libQt5VirtualKeyboard.so.5*
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QVirtualKeyboardPlugin.cmake
%{_opt_qt5_plugindir}/platforminputcontexts/libqtvirtualkeyboardplugin.so
%{_opt_qt5_plugindir}/virtualkeyboard/
%{_opt_qt5_qmldir}/QtQuick/VirtualKeyboard/

%files devel
%{_opt_qt5_headerdir}/QtVirtualKeyboard/
%{_opt_qt5_libdir}/libQt5VirtualKeyboard.prl
%{_opt_qt5_libdir}/libQt5VirtualKeyboard.so
%{_opt_qt5_libdir}/cmake/Qt5VirtualKeyboard/
%{_opt_qt5_libdir}/pkgconfig/Qt5VirtualKeyboard.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_virtualkeyboard*.pri

