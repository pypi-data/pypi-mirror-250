# Makefile for fead
# Copyright (C) 2022  Nguyễn Gia Phong
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

SHELL = /bin/sh
PREFIX ?= /usr/local

.PHONY: man all clean install uninstall

man: src/fead.py doc/fead.h2m
	help2man --name='advert generator from web feeds'\
		--include=doc/fead.h2m --output=doc/fead.1\
		--no-info src/fead.py

all: man

clean:
	rm doc/fead.1

install: all
	install -Dm 755 src/fead.py ${DESTDIR}${PREFIX}/bin/fead
	install -Dm 644 doc/fead.1 ${DESTDIR}${PREFIX}/share/man/man1/fead.1

uninstall:
	rm ${DESTDIR}${PREFIX}/bin/fead
	rm ${DESTDIR}${PREFIX}/share/man/fead.1
