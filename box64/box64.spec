%global date 20240314
%global commit cd8bda7a29a2ef15d939890cacab02efb84e0158
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# Tests are disabled as they require x86_64 libraries to run
%bcond_with tests

# Disable -Werror=implicit-function-declaration as it breaks the build
%global build_type_safety_c 0

%global forgeurl https://github.com/ptitSeb/box64

%global common_description %{expand:
Box64 lets you run x86_64 Linux programs (such as games) on non-x86_64 Linux
systems, like ARM (host system needs to be 64-bit little-endian).}

Name:           box64
Version:        0.2.6^%{date}git%{shortcommit}
Release:        %autorelease
Summary:        Linux userspace x86_64 emulator with a twist, targeted at ARM64

License:        MIT
URL:            https://box86.org
Source:         %{forgeurl}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-podlators
BuildRequires:  systemd-rpm-macros

# box64 only supports these architectures
ExclusiveArch:  aarch64 riscv64 ppc64le x86_64

Requires:       %{name}-data = %{version}-%{release}
%ifarch aarch64
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%endif

%description    %{common_description}

%package        data
Summary:        Common files for %{name}
BuildArch:      noarch

%description    data %{common_description}

%ifarch aarch64
%package        adlink
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    adlink %{common_description}

This package contains a version of box64 targeting ADLink AmpereAltra systems.

%package        asahi
Summary:        Apple Silicon version of box64

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    asahi %{common_description}

This package contains a version of box64 targeting Apple Silicon systems using
a 16k page size.

%package        lx2160a
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    lx2160a %{common_description}

This package contains a version of box64 targeting NXP LX2160A systems.

%package        odroidn2
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    odroidn2 %{common_description}

This package contains a version of box64 targeting ODROID-N2/N2+ systems.

%package        rk3326
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    rk3326 %{common_description}

This package contains a version of box64 targeting Rockchip RK3326 systems.

%package        rk3399
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    rk3399 %{common_description}

This package contains a version of box64 targeting Rockchip RK3399 systems.

%package        rk3588
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    rk3588 %{common_description}

This package contains a version of box64 targeting Rockchip RK3588 / RK3588S
systems.

%package        rpi3
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    rpi3 %{common_description}

This package contains a version of box64 targeting Raspberry Pi 3 systems.

%package        rpi4
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    rpi4 %{common_description}

This package contains a version of box64 targeting Raspberry Pi 4 systems.

%package        rpi5
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    rpi5 %{common_description}

This package contains a version of box64 targeting Raspberry Pi 5 systems.

%package        sd845
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    sd845 %{common_description}

This package contains a version of box64 targeting Qualcomm Snapdragon 845
systems.

%package        sd888
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    sd888 %{common_description}

This package contains a version of box64 targeting Qualcomm Snapdragon 888
systems.

%package        sd8g2
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    sd8g2 %{common_description}

This package contains a version of box64 targeting Qualcomm Snapdragon 8 Gen 2
systems.

%package        tegrax1
Summary:        %{summary}

Requires:       %{name}-data = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description    tegrax1 %{common_description}

This package contains a version of box64 targeting Nvidia Tegra X1 systems.
%endif

%prep
%autosetup -p1 -n %{name}-%{commit}

# Remove prebuilt libraries
rm -r x64lib

# Fix encoding
sed -i 's/\r$//' docs/*.md

# Fix install paths
sed -i 's:/etc/binfmt.d:%{_binfmtdir}:g' CMakeLists.txt

%build
%global common_flags -DNOGIT=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo
%ifarch aarch64
# ADLink AmpereAltra
%cmake %{common_flags} -DADLINK=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.adlink
rm -r %{__cmake_builddir}

# Apple Silicon
%cmake %{common_flags} -DM1=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.asahi
rm -r %{__cmake_builddir}

# NXP LX2160A
%cmake %{common_flags} -DLX2160A=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.lx2160a
rm -r %{__cmake_builddir}

# ODROID-N2/N2+
%cmake %{common_flags} -DODROIDN2=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.odroidn2
rm -r %{__cmake_builddir}

# Rockchip RK3326
%cmake %{common_flags} -DRK3326=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.rk3326
rm -r %{__cmake_builddir}

# Rockchip RK3399
%cmake %{common_flags} -DRK3399=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.rk3399
rm -r %{__cmake_builddir}

# Rockchip RK3588/RK3588S
%cmake %{common_flags} -DRK3588=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.rk3588
rm -r %{__cmake_builddir}

# Raspberry PI 3
%cmake %{common_flags} -DRPI3ARM64=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.rpi3
rm -r %{__cmake_builddir}

# Raspberry PI 4
%cmake %{common_flags} -DRPI4ARM64=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.rpi4
rm -r %{__cmake_builddir}

# Raspberry PI 5
%cmake %{common_flags} -DRPI5ARM64=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.rpi5
rm -r %{__cmake_builddir}

# Qualcomm Snapdragon 845
%cmake %{common_flags} -DSD845=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.sd845
rm -r %{__cmake_builddir}

# Qualcomm Snapdragon 888
%cmake %{common_flags} -DSD888=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.sd888
rm -r %{__cmake_builddir}

# Qualcomm Snapdragon 8 Gen 2
%cmake %{common_flags} -DSD8G2=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.sd8g2
rm -r %{__cmake_builddir}

# Nvidia Tegra X1
%cmake %{common_flags} -DTEGRAX1=ON
%cmake_build
cp -p %{__cmake_builddir}/%{name} %{name}.tegrax1
rm -r %{__cmake_builddir}
%endif

%cmake %{common_flags} -DNO_LIB_INSTALL=ON \
%ifarch aarch64
  -DARM_DYNAREC=ON
%endif
%ifarch riscv64
  -DRV64=ON
%endif
%ifarch ppc64le
  -DPPC64LE=ON
%endif
%ifarch x86_64
  -DLD80BITS=ON \
  -DNOALIGN=ON
%endif
%cmake_build

# Build manpage
pod2man --stderr docs/%{name}.pod > docs/%{name}.1

%install
%ifarch x86_64
# Install manually as cmake_install doesn't seem to work on x86_64
install -Dpm0755 -t %{buildroot}%{_bindir} %{__cmake_builddir}/%{name}
install -Ddpm0755 %{buildroot}%{_binfmtdir}
sed 's:${CMAKE_INSTALL_PREFIX}/bin/${BOX64}:%{_bindir}/%{name}:' \
  < system/box64.conf.cmake > system/box64.conf
install -Dpm0644 -t %{buildroot}%{_binfmtdir} system/box64.conf
install -Dpm0644 -t %{buildroot}%{_sysconfdir} system/box64.box64rc
%else
%cmake_install
%endif

# Install manpage
install -Dpm0644 -t %{buildroot}%{_mandir}/man1 docs/%{name}.1

%ifarch aarch64
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.aarch64
touch %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}
install -Dpm0755 -t %{buildroot}%{_bindir} \
  %{name}.adlink \
  %{name}.asahi \
  %{name}.lx2160a \
  %{name}.odroidn2 \
  %{name}.rk3326 \
  %{name}.rk3399 \
  %{name}.rk3588 \
  %{name}.rpi3 \
  %{name}.rpi4 \
  %{name}.rpi5 \
  %{name}.sd845 \
  %{name}.sd888 \
  %{name}.sd8g2 \
  %{name}.tegrax1

%post
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.aarch64 20

%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.aarch64
fi

%post adlink
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.adlink 10

%postun adlink
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.adlink
fi

%post asahi
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.asahi 10

%postun asahi
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.asahi
fi

%post lx2160a
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.lx2160a 10

%postun lx2160a
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.lx2160a
fi

%post odroidn2
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.odroidn2 10

%postun odroidn2
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.odroidn2
fi

%post rk3326
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.rk3326 10

%postun rk3326
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.rk3326
fi

%post rk3399
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.rk3399 10

%postun rk3399
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.rk3399
fi

%post rk3588
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.rk3588 10

%postun rk3588
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.rk3588
fi

%post rpi3
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.rpi3 10

%postun rpi3
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.rpi3
fi

%post rpi4
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.rpi4 10

%postun rpi4
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.rpi4
fi

%post rpi5
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.rpi5 10

%postun rpi5
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.rpi5
fi

%post sd845
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.sd845 10

%postun sd845
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.sd845
fi

%post sd888
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.sd888 10

%postun sd888
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.sd888
fi

%post sd8g2
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.sd8g2 10

%postun sd8g2
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.sd8g2
fi

%post tegrax1
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} \
  %{name} %{_bindir}/%{name}.tegrax1 10

%postun tegrax1
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove %{name} %{_bindir}/%{name}.tegrax1
fi
%endif

%if %{with tests}
%check
%ctest
%endif

%files
%ifarch aarch64
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.aarch64
%else
%{_bindir}/%{name}
%endif

%ifarch aarch64
%files adlink
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.adlink

%files asahi
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.asahi

%files lx2160a
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.lx2160a

%files odroidn2
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.odroidn2

%files rk3326
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.rk3326

%files rk3399
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.rk3399

%files rk3588
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.rk3588

%files rpi3
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.rpi3

%files rpi4
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.rpi4

%files rpi5
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.rpi5

%files sd845
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.sd845

%files sd888
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.sd888

%files sd8g2
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.sd8g2

%files tegrax1
%ghost %{_bindir}/%{name}
%{_bindir}/%{name}.tegrax1
%endif

%files data
%license LICENSE
%doc README.md
%doc %lang(cn) README_CN.md
%doc %lang(uk) README_UK.md
%doc docs/*.md docs/img
%{_binfmtdir}/box64.conf
%{_mandir}/man1/box64.1*
%config(noreplace) %{_sysconfdir}/box64.box64rc

%changelog
%autochangelog
