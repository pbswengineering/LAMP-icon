.PHONY: all clean install uninstall

all:
	@echo "It's all there, just an ls away!"

clean:
	rm -f *~

install:
	mkdir -p $(DESTDIR)/usr/share/lamp-icon/
	cp lamp-icon.py running.png stopped.png lamp-icon.svg $(DESTDIR)/usr/share/lamp-icon/
	mkdir -p $(DESTDIR)/usr/share/doc/lamp-icon/
	cp AUTHORS COPYING README $(DESTDIR)/usr/share/doc/lamp-icon/
	test -d $(DESTDIR)/usr/bin/ || mkdir -p $(DESTDIR)/usr/bin/
	ln -s $(DESTDIR)/usr/share/lamp-icon/lamp-icon.py $(DESTDIR)/usr/bin/lamp-icon
	test -d $(DESTDIR)/usr/share/applications/ || mkdir -p $(DESTDIR)/usr/share/applications/
	cp lamp-icon.desktop $(DESTDIR)/usr/share/applications/
	update-desktop-database || true

uninstall:
	rm -f $(DESTDIR)/usr/bin/lamp-icon
	rm -fr $(DESTDIR)/usr/share/lamp-icon/
	rm -fr $(DESTDIR)/usr/share/doc/lamp-icon/
	rm -f $(DESTDIR)/usr/share/applications/lamp-icon.desktop
	update-desktop-database || true
