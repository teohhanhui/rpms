# yuzu

## Download sources

    spectool -g yuzu.spec

## Build RPM

    fedpkg --release f39 mockbuild --root fedora+rpmfusion_free-39-aarch64

## Update compatibility list

    curl -sSLo compatibility_list.json https://api.yuzu-emu.org/gamedb/
