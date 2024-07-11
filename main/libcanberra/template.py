pkgname = "libcanberra"
pkgver = "0.30"
pkgrel = 2
build_style = "gnu_configure"
configure_args = [
    "--enable-null",
    "--enable-pulse",
    "--enable-gstreamer",
    "--enable-gtk3",
    "--disable-gtk",
    "--disable-alsa",
    "--disable-oss",
    "--disable-lynx",
    "--with-builtin=dso",
]
make_cmd = "gmake"
make_install_args = ["-j1"]  # racey install
hostmakedepends = [
    "automake",
    "gmake",
    "gtk-doc-tools",
    "libtool",
    "pkgconf",
]
makedepends = [
    "gtk+3-devel",
    "gstreamer-devel",
    "libvorbis-devel",
    "libpulse-devel",
    "udev-devel",
    "libltdl-devel",
    "tdb-devel",
]
pkgdesc = "Portable sound event API"
maintainer = "q66 <q66@chimera-linux.org>"
license = "LGPL-2.1-or-later"
url = "https://0pointer.de/lennart/projects/libcanberra"
source = f"{url}/{pkgname}-{pkgver}.tar.xz"
sha256 = "c2b671e67e0c288a69fc33dc1b6f1b534d07882c2aceed37004bf48c601afa72"


@subpackage("libcanberra-devel")
def _devel(self):
    return self.default_devel()


@subpackage("libcanberra-gtk3")
def _gtk3(self):
    self.subdesc = "Gtk+3 support"
    self.install_if = [f"{pkgname}={pkgver}-r{pkgrel}", "gtk+3"]
    # compat
    self.provides = [f"libcanberra-progs={pkgver}-r{pkgrel}"]

    return [
        "usr/bin/canberra-gtk-play",
        "usr/lib/libcanberra-gtk3.so.*",
        "usr/lib/gtk-3.0",
    ]


@subpackage("libcanberra-pulse")
def _pulse(self):
    self.subdesc = "PulseAudio support"
    self.install_if = [f"{pkgname}={pkgver}-r{pkgrel}", "libpulse"]

    return ["usr/lib/libcanberra-*/libcanberra-pulse.so"]


@subpackage("libcanberra-gstreamer")
def _gst(self):
    self.subdesc = "GStreamer support"
    self.install_if = [f"{pkgname}={pkgver}-r{pkgrel}", "gstreamer"]

    return ["usr/lib/libcanberra-*/libcanberra-gstreamer.so"]


@subpackage("libcanberra-gnome")
def _gnome(self):
    self.subdesc = "GNOME support"
    self.depends += [f"libcanberra-gtk3={pkgver}-r{pkgrel}"]
    self.install_if = [f"{pkgname}={pkgver}-r{pkgrel}", "gnome"]

    return [
        "usr/lib/gnome*",
        "usr/share/gdm",
        "usr/share/gnome",
    ]
