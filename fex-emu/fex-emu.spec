%global date 20240508
%global commit 2cae2f246247020e3ea3f3081e8f34ce25d925b5
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global toolchain clang

# Not practical to run tests for aarch64 builds as a RootFS is required
%bcond check %[ "x86_64" == "%{_target_cpu}" ]

# TODO: building thunks is still broken
%bcond thunks 0

%global forgeurl https://github.com/FEX-Emu/FEX

Name:       fex-emu
Version:    2405^%{date}git%{shortcommit}
Release:    1%{?dist}
Summary:    Fast x86 emulation frontend

License:    MIT
URL:        https://fex-emu.com/
Source0:    %{forgeurl}/archive/%{commit}/FEX-%{commit}.tar.gz

# External dependencies
# These are git submodules in upstream repo
%{lua:
local externals = {
  { name="Catch2", ref="v3.5.3-g8ac8190", owner="catchorg" },
  { name="cpp-optparse", ref="eab4212", owner="Sonicadvance1", path="../Source/Common/cpp-optparse" },
  { name="drm-headers", ref="34a2039", owner="FEX-Emu" },
  { name="fex-gcc-target-tests-bins", ref="442678a", owner="FEX-Emu" },
  { name="fex-gvisor-tests-bins", ref="71349ae", owner="FEX-Emu" },
  { name="fex-posixtest-bins", ref="9ae2963", owner="FEX-Emu" },
  { name="fmt", ref="10.1.1-gf5e5435", owner="fmtlib" },
  { name="imgui", ref="4c986ec", owner="Sonicadvance1" },
  { name="jemalloc", ref="16f8061", owner="FEX-Emu" },
  { name="jemalloc", ref="888181c", owner="FEX-Emu", path="jemalloc_glibc" },
  { name="json-maker", ref="8ecb8ec", owner="Sonicadvance1" },
  { name="robin-map", ref="f1ab690", owner="FEX-Emu" },
  { name="tiny-json", ref="9d09127", owner="Sonicadvance1" },
  { name="vixl", ref="7725aec", owner="FEX-Emu" },
  { name="Vulkan-Headers", ref="v1.3.278-g31aa7f6", owner="KhronosGroup" },
  { name="xbyak", ref="v7.02-gf17cb9d", owner="herumi" },
  { name="xxhash", ref="v0.8.2-gbbb27a5", owner="Cyan4973" },
}

for i, s in ipairs(externals) do
  print(string.format("Source%d: https://github.com/%s/%s/archive/%s/%s-%s.tar.gz", i, s.owner, s.name, s.ref, s.name, s.ref).."\n")
end

function print_setup_externals()
  local target_cpu = rpm.expand("%{_target_cpu}")
  for i, s in ipairs(externals) do
    local matches_arch = (s.arch == nil)
    if not matches_arch then
      for _, t in ipairs(s.arch) do
        if t == target_cpu then matches_arch = true end
      end
    end
    if matches_arch then
      print(string.format("mkdir -p External/%s", (s.path or s.name)).."\n")
      print(string.format("tar -xzf %s --strip-components=1 -C External/%s", rpm.expand("%{SOURCE"..i.."}"), (s.path or s.name)).."\n")
    end
  end
end
}

# FEX only supports aarch64 and x86_64
ExclusiveArch:  aarch64 x86_64

BuildRequires:  ccache
BuildRequires:  clang
BuildRequires:  cmake
#BuildRequires:  cmake(epoxy)
BuildRequires:  cmake(SDL2)
BuildRequires:  git
BuildRequires:  libepoxy-devel
BuildRequires:  lld
BuildRequires:  llvm
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  systemd-rpm-macros

%if %{with thunks}
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake(Clang)
BuildRequires:  libdrm-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libX11-devel
BuildRequires:  llvm-devel
BuildRequires:  pkgconfig(openssl)
BuildRequires:  wayland-devel
%endif

%if %{with check}
BuildRequires:  nasm
BuildRequires:  python3-clang
%endif

Recommends:     squashfs-tools
Recommends:     squashfuse

Suggests:       erofs-fuse
Suggests:       erofs-utils

%description
FEX allows you to run x86 and x86-64 binaries on an AArch64 host, similar to
qemu-user and box86. It has native support for a rootfs overlay, so you don't
need to chroot, as well as some thunklibs so it can forward things like GL to
the host. FEX presents a Linux 5.0 interface to the guest, and supports both
AArch64 and x86-64 as hosts. FEX is very much work in progress, so expect things
to change.

%package devel
Summary:    Development header files for fex-emu

%description devel
Development header files for fex-emu.

%prep
%setup -q -n FEX-%{commit}

%{lua: print_setup_externals()}

%autopatch -p1

# Fix binfmt install
sed -i \
    's#'\'':\([^:]\+\):\([^'\'']\+\)'\'' > /proc/sys/fs/binfmt_misc/register#'\'':\1:\2'\'' > %{buildroot}%{_binfmtdir}/\1.conf#g' \
    Source/Tools/FEXLoader/CMakeLists.txt

%build
%cmake -G Ninja \
    %{?with_thunks:-DBUILD_THUNKS=True} \
    %{?with_thunks:-DENABLE_CLANG_THUNKS=True} \
    %dnl %{?with_check:-DENABLE_CLANG_THUNKS=True} \
    %{!?with_check:-DBUILD_TESTS=False} \
    %dnl %{?with_check:-DBUILD_FEX_LINUX_TESTS=True}

%cmake_build

%install
%cmake_install

install -Ddpm0755 %{buildroot}%{_libdir}
mv %{buildroot}%{_exec_prefix}/lib/libFEXCore.so %{buildroot}%{_libdir}/libFEXCore.so
mv %{buildroot}%{_exec_prefix}/lib/libFEXCore.a %{buildroot}%{_libdir}/libFEXCore.a

install -Ddpm0755 %{buildroot}%{_binfmtdir}
%cmake_build -t binfmt_misc
rm %{buildroot}%{_datadir}/binfmts/FEX-x86
rm %{buildroot}%{_datadir}/binfmts/FEX-x86_64

%post
%binfmt_apply FEX-x86.conf
%binfmt_apply FEX-x86_64.conf

%postun
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi

%check
%if %{with check}
%ctest
%endif

%files
%license LICENSE
%{_bindir}/FEXBash
%{_bindir}/FEXConfig
%{_bindir}/FEXGetConfig
%{_bindir}/FEXInterpreter
%{_bindir}/FEXLoader
%{_bindir}/FEXpidof
%{_bindir}/FEXRootFSFetcher
%{_bindir}/FEXServer
%{_bindir}/FEXUpdateAOTIRCache
%{_libdir}/libFEXCore.so
%exclude %{_libdir}/libFEXCore.a
%{_binfmtdir}/FEX-x86.conf
%{_binfmtdir}/FEX-x86_64.conf
%dir %{_datadir}/fex-emu/
%dir %{_datadir}/fex-emu/AppConfig/
%{_datadir}/fex-emu/AppConfig/*.json
%{_datadir}/fex-emu/ThunksDB.json
%{_mandir}/man1/FEX.1*

%files devel
%{_includedir}/FEXCore/

%changelog
%autochangelog
