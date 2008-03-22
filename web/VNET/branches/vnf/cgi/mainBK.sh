#!/usr/bin/env sh
#. dottools && _repo_/cgi/main.py $@
cd vnf; mm; cd -
. cgi/dottools && cgi/main.py $@ > test.html
firefox test.html
