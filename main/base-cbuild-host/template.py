pkgname = "base-cbuild-host"
pkgver = "0.1"
pkgrel = 0
build_style = "meta"
depends = [
    "apk-tools", "openssl", "git", "bubblewrap", "chimerautils", "fakeroot"
]
pkgdesc = "Everything one needs to use cbuild and cports"
maintainer = "q66 <q66@chimera-linux.org>"
license = "custom:meta"
url = "https://chimera-linux.org"
