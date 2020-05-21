# Giving Prolexa a Language model frontend

We assume you're using Linux.

### FIX

SWI-Prolog 8 doesn't work with pyswip unless you symlink it to the new name:

`sudo ln -s /usr/lib/swi-prolog/lib/x86_64-linux/libswipl.so /usr/lib/libpl.so`

It also only works in Python 2.7

`conda create -n prolexa python=2.7 ipykernel`
`python2 -m ipykernel install --user --name=prolexa`
`conda install -c auto pyswip`

Pyswip seems to be unstable; segfault as soon as you run any query
