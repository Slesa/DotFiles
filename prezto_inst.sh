#/bin/bash
setopt EXTENDED_GLOB
for rcfile in ~/.zprezto/runcoms/^README.md(.N); do
	ln -s $rcfile ~/.${rcfile:t}
done
