'''Launches ISAW with system call.

Uses Operators.F_LoadARCS in ARCS.jar 
'''
__author__='mmckerns'
__version__='1.0'

import os
import sys

# change 'WINHOME' if you run Windows / change 'LINHOME' if you run Linux
WINHOME='C:/"Documents and Settings"/mmckerns/"My Documents"/ISAW'
LINHOME='/home/mmckerns/prog/ISAW-1-4-1'

# HOME=        ISAW home directory
# JNEXUS_LIB=  jnexus home directory for ISAW
# JARS=        included ISAW jar files
if sys.platform[:3] == 'win':   # if Windows os...
	HOME=WINHOME
	JNEXUS_LIB=HOME+'/lib/jnexus.dll'
	JARS=HOME+'/ARCS.jar;'+HOME+'/IPNS.jar;'+HOME+'/sgt_v2.jar;'+HOME+'/jnexus.jar;'+HOME+'/jhall.jar;'+HOME+'/Isaw.jar;'+HOME+'/sdds.jar'
else:                           # if non-Windows os...
	HOME=LINHOME
	JNEXUS_LIB=HOME+'/lib/libjnexus.so'
	JARS=HOME+'/ARCS.jar:'+HOME+'/IPNS.jar:'+HOME+'/sgt_v2.jar:'+HOME+'/jnexus.jar:'+HOME+'/jhall.jar:'+HOME+'/Isaw.jar:'+HOME+'/sdds.jar'

# Isaw java module name to execute
operator='Operators.F_LoadARCS'

# java commandline args entered as python commandline args
ARGS=""
for arg in sys.argv[1:]: ARGS=ARGS+arg+" "

# commandline Isaw w/ java
os.system('java -cp '+JARS+' -Dneutron.nexus.JNEXUSLIB='+JNEXUS_LIB+' '+operator+' '+ARGS)
