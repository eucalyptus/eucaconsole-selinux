# Copyright (c) 2016 Hewlett Packard Enterprise Development LP
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

distdir = eucaconsole-selinux-$(shell sed -n '/^policy_module/s/.*, \([0-9.]*\).*/\1/p' eucaconsole.te)

include /usr/share/selinux/devel/Makefile

.PHONY: all clean dist distdir relabel

all: eucaconsole.pp

relabel:
	restorecon -Riv /etc/eucaconsole /etc/rc.d/init.d/eucaconsole /etc/sysconfig/eucaconsole /usr/bin/eucaconsole /var/log/eucaconsole* /var/run/eucaconsole

distdir: Makefile COPYING eucaconsole.te eucaconsole.fc eucaconsole.if eucaconsole-selinux.spec
	rm -rf $(distdir)
	mkdir -p $(distdir)
	cp -pR $^ $(distdir)

dist: distdir
	mkdir -p dist
	tar -cJ -f dist/$(distdir).tar.xz $(distdir)
	rm -rf $(distdir)

clean:
	rm -rf dist
	rm -rf tmp
	rm -rf $(distdir)
	rm -f  eucaconsole.pp
