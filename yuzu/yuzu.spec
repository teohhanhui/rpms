%global date 20231216
%global commit defda5dae4c504ffefda673903b8048543456fe1
%global shortcommit %(c=%{commit}; echo ${c:0:9})

Name:           yuzu
Version:        1653
Release:        %autorelease
Summary:        Nintendo Switch emulator

License:        GPL-3.0-or-later
URL:            https://github.com/yuzu-emu/yuzu
Source0:        https://github.com/yuzu-emu/yuzu-mainline/releases/download/mainline-0-%{version}/%{name}-linux-%{date}-%{shortcommit}-source.tar.xz

# External dependencies
# These are git submodules in upstream repo
%{lua:
local externals = {
  { name="cpp-jwt", ref="v1.4-18-g10ef573", owner="arun11299" },
  { name="discord-rpc", ref="20cc99aeffa08a4834f156b6ab49ed68618cf94a", owner="yuzu-emu" },
  { name="dynarmic", ref="r4-936-g0df09e2f", owner="merryhime", arch={ "x86_64", "aarch64" } },
  { name="mbedtls", ref="v2.16.9-115-g8c88150ca", owner="yuzu-emu" },
  { name="oaknut", ref="1.2.1-18-g918bd94", owner="merryhime", arch={ "aarch64" } },
  { name="simpleini", ref="4.19-15-g382ddbb", owner="brofield" },
  { name="sirit", ref="ab75463999f4f3291976b079d42d52ee91eebf3f", owner="yuzu-emu" },
  { name="SPIRV-Headers", ref="1.5.4.raytracing.fixed-201-gc214f6f", owner="KhronosGroup", path="sirit/externals/SPIRV-Headers" },
  { name="tz", ref="2022g-11-g16ce126a", owner="eggert", path="nx_tzdb/tzdb_to_nx/externals/tz/tz" },
  { name="tzdb_to_nx", ref="221202-4-gf668009", owner="lat9nq", path="nx_tzdb/tzdb_to_nx" },
  { name="VulkanMemoryAllocator", ref="v2.1.0-819-g2f382df", owner="GPUOpen-LibrariesAndSDKs" },
  { name="xbyak", ref="v3.71-1034-ga1ac375", owner="herumi" },
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
      print(string.format("mkdir -p externals/%s", (s.path or s.name)).."\n")
      print(string.format("tar -xzf %s --strip-components=1 -C externals/%s", rpm.expand("%{SOURCE"..i.."}"), (s.path or s.name)).."\n")
    end
  end
end
}

Source99:       compatibility_list.json

Patch0:         cmake-httplib-0.13.patch
Patch1:         tzdb_to_nx-hardcode-tz-commit-time.patch

BuildRequires:  boost-devel
BuildRequires:  ccache
BuildRequires:  cmake
#BuildRequires:  cmake(cpp-jwt)
BuildRequires:  cmake(cubeb)
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(httplib)
BuildRequires:  cmake(nlohmann_json)
BuildRequires:  cmake(rapidjson)
BuildRequires:  cmake(SDL2)
BuildRequires:  cmake(VulkanHeaders)
#BuildRequires:  cmake(VulkanMemoryAllocator)
#BuildRequires:  cmake(xbyak)
BuildRequires:  ffmpeg-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  glslang
BuildRequires:  hidapi-devel
BuildRequires:  ninja-build
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(opus)
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtwebengine-devel
BuildRequires:  wayland-devel
BuildRequires:  zlib-devel

%description
yuzu is the world's most popular, open-source, Nintendo Switch emulator —
started by the creators of Citra. It is written in C++ with portability in mind,
and we actively maintain builds for Windows, Linux and Android.

%prep
%autosetup -N -n %{name}-linux-%{date}-%{shortcommit}-source

%{lua: print_setup_externals()}

%autopatch -p1

cp %{SOURCE99} dist/compatibility_list/compatibility_list.json

%build
%cmake -G Ninja \
    -DENABLE_COMPATIBILITY_LIST_DOWNLOAD=OFF \
    -DENABLE_QT_TRANSLATION=ON \
    -DUSE_DISCORD_PRESENCE=ON \
    -DDISPLAY_VERSION="%{version}" \
    -DYUZU_USE_BUNDLED_SDL2=OFF \
    -DYUZU_USE_EXTERNAL_SDL2=OFF \
    -DYUZU_USE_EXTERNAL_FFMPEG=OFF \
    -DYUZU_USE_EXTERNAL_VULKAN_HEADERS=OFF \
    -DYUZU_USE_BUNDLED_VCPKG=OFF \
    -DYUZU_CHECK_SUBMODULES=OFF \
    -DYUZU_TESTS=OFF

%cmake_build

%install
%cmake_install

rm -rf \
    %{buildroot}%{_includedir}/tsl \
    %{buildroot}%{_datadir}/cmake/tsl-robin-map \
    %{buildroot}%{_includedir}/xbyak \
    %{buildroot}%{_libdir}/cmake/xbyak

%files
%license LICENSE.txt LICENSES/*
%{_bindir}/yuzu
%{_bindir}/yuzu-cmd
%{_bindir}/yuzu-room
%{_datadir}/applications/org.yuzu_emu.yuzu.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.yuzu_emu.yuzu.svg
%{_datadir}/metainfo/org.yuzu_emu.yuzu.metainfo.xml
%{_datadir}/mime/packages/org.yuzu_emu.yuzu.xml

%changelog
%autochangelog
