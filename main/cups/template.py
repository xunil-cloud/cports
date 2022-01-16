pkgname = "cups"
pkgver = "2.4.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--enable-relro", "--enable-acl", "--enable-dbus",
    "--enable-libpaper", "--enable-pam",
    "--enable-raw-printing",

    "--disable-gssapi", "--without-rcdir", "--without-systemd",

    "--with-tls=gnutls",
    "--with-dnssd=avahi",
    "--with-rundir=/run/cups",
    "--with-logdir=/var/log/cups",
    "--with-docdir=/usr/share/cups/doc",
    "--with-menudir=/usr/share/applications",
    "--with-xinetd=/etc/xinetd.d",
    "--with-cups-user=_cups",
    "--with-cups-group=lp",
    "--with-system-groups=_lpadmin sys root",
]
# build system is bad
make_dir = "."
make_check_args = ["-j1"]
hostmakedepends = [
    "pkgconf", "avahi-devel", "gnutls-devel", "poppler", "xdg-utils",
]
makedepends = [
    "acl-devel", "gnutls-devel", "libpaper-devel", "libpng-devel",
    "libtiff-devel", "libpoppler-devel", "libusb-devel", "linux-pam-devel",
    "avahi-devel", "linux-headers",
]
depends = ["xdg-utils"]
pkgdesc = "Common Unix Printing System"
maintainer = "q66 <q66@chimera-linux.org>"
license = "Apache-2.0"
url = "https://github.com/OpenPrinting/cups"
source = f"{url}/releases/download/v{pkgver}/{pkgname}-{pkgver}-source.tar.gz"
sha256 = "9abecec128ca6847c5bb2d3e3d30c87b782c0697b9acf284d16fa38f80a3a6de"
# build system is bad
tool_flags = {
    "CFLAGS": ["-Wno-unused-command-line-argument"],
    "CXXFLAGS": ["-Wno-unused-command-line-argument"],
}
file_modes = {
    "var/cache/cups/rss": ("_cups:0", "lp:10", 0o750),
    "var/spool/cups": ("_cups:0", "lp:10", 0o755),
    "etc/cups/ssl": ("_cups:0", "lp:10", 0o700),
    "etc/cups/classes.conf": ("root:0", "lp:10", 0o644),
    "etc/cups/printers.conf": ("root:0", "lp:10", 0o644),
    "etc/cups/subscriptions.conf": ("root:0", "lp:10", 0o644),
    "etc/cups/cups-files.conf": ("root:0", "lp:10", 0o640),
    "etc/cups/cups-files.conf.default": ("root:0", "lp:10", 0o640),
    "etc/cups/cupsd.conf": ("root:0", "lp:10", 0o640),
    "etc/cups/cupsd.conf.default": ("root:0", "lp:10", 0o640),
    "etc/cups/snmp.conf": ("root:0", "lp:10", 0o640),
    "etc/cups/snmp.conf.default": ("root:0", "lp:10", 0o640),
}
# undefined references everywhere
options = ["!lto"]

system_users = [
    {
        "name": "_cups",
        "id": None,
        "pgroup": "lp",
        "home": "/var/spool/cups",
    }
]
system_groups = ["_lpadmin"]

def init_configure(self):
    # build system is bad
    self.configure_args += [
        "--with-optim=" + self.get_cflags(shell = True) + \
        " " + self.get_ldflags(shell = True)
    ]

def post_install(self):
    self.install_file(self.files_path / "cups.pam", "etc/pam.d", name = "cups")
    self.install_file(self.files_path / "client.conf", "etc/cups")

    self.install_service(self.files_path / "cupsd")

    # install some more configuration files that will get filled by cupsd
    for f in ["printers", "classes", "subscriptions"]:
        (self.destdir / f"etc/cups/{f}.conf").touch(mode = 0o644)

    self.install_dir("usr/lib/cups/driver", empty = True)
    self.install_dir("var/log/cups", mode = 0o750, empty = True)
    self.install_dir("var/cache/cups/rss", mode = 0o750, empty = True)
    self.install_dir("var/spool/cups", empty = True)
    self.install_dir("etc/cups/ssl", mode = 0o700, empty = True)

@subpackage("cups-libs")
def _libs(self):
    self.file_modes = {"etc/cups/client.conf": ("root:0", "lp:10", 0o644)}

    return self.default_libs(extra = [
        "etc/cups/client.conf",
        "usr/share/man/man5/client.conf.5",
    ])

@subpackage("cups-devel")
def _devel(self):
    self.depends += ["zlib-devel"]

    return self.default_devel()
