#!/usr/local/bin/bash
# make -C /usr/ports/devel/qt5 run-depends-list | sed -e 's/\/usr\/ports\//g/' > /root/depends_list && portmaster `cat /root/depends_list`

function build() {
	cd $1
	echo ### Building $1 ###
	sudo make reinstall clean
	cd ..
}

cd /usr/ports/devel
build qt5-buildtools
build qt5-core
build qt5-qmake
build qt5-concurrent
build qt5-uitools
build qt5-qdbus
build qt5-dbus
build qt5-script
build qt5-scripttools
build qt5-help
#build qt5-location
build qt5-testlib
build qt5-scxml

build qt5-assistant
build qt5-linguisttools
build qt5-qdoc
#build qt5-remoteobjects
#build qt5-designer
#build qt5-linguist
#build qtcreator
