pkgname = "iso-codes"
pkgver = "4.15.0"
pkgrel = 1
build_style = "gnu_configure"
configure_gen = []
make_cmd = "gmake"
hostmakedepends = ["gettext", "python", "pkgconf", "gmake"]
pkgdesc = "List of country, language and currency names"
maintainer = "q66 <q66@chimera-linux.org>"
license = "LGPL-2.1-or-later"
url = "https://salsa.debian.org/iso-codes-team/iso-codes"
source = f"$(DEBIAN_SITE)/main/i/{pkgname}/{pkgname}_{pkgver}.orig.tar.xz"
sha256 = "3d50750bf1d62d83b6085f5815ceb8392df34266a15f16bcf8d4cf7eb15d245c"
