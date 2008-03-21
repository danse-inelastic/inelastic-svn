#!/usr/bin/env sh
#. dottools && _repo_/cgi/main.py $@
. dottools && cgi/main.py $@ > test.html
firefox test.html
