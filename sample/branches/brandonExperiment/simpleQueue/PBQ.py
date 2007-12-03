#!/usr/bin/env python
################################################################################
#
#       File:   PBQ.py
#
#       This is part of PBQ - The Python Batch Queue. 
#
#       Copyright (C) 2007, Brandon Keith
#       Copyright (C) 1998-1999, Alexander Schliep
#       For Information see http://www.zpr.uni-koeln.de/~schliep/PBQ
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
# 
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
# 
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
################################################################################
#
# Synopsis:
#
# PBQ.py hostfile joblist
#
#
################################################################################
import sys
import string
import posix
import os

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print " "
        print " Synopsis: PBQ.py hostfile jobfile command [host1 ...]"
        print " "
        print "     stop  stop all PBQ-Managers and all jobs"
        print "     cont  continue all PBQ-Managers and all jobs"
        print "     quit  let running jobs finish and then quit  PBQ-Managers"
        print "     term  terminate all PBQ-Managers and all jobs"
        print " "
        print "     kill  kill all PBQ-Managers. Does *not* kill jobs"
        print " "
        print "     load  display load of all machines in hostfile"
        print " "
        sys.exit(1)
    jobfile  = sys.argv[2]
    command  = sys.argv[3]

    onlyhosts = []
    for i in xrange(4,len(sys.argv)):
        onlyhosts.append(sys.argv[i])

    # Read in hostfile 
    hosts       = []
    hostname    = {}
    arch        = {}
    max         = {}
    wday        = {}
    interactive = {}
    pid         = {}

    hostfile = open(sys.argv[1],'r')
    lines = hostfile.readlines()
    for line in lines:
        l = string.split(line)
        if len(l) > 0:
            # Take only name up to first .
            hostnick = string.split(l[0],'.')[0]
            if hostnick[0] != '#':
                hosts.append(hostnick)
                hostname[hostnick] = l[0]
                arch[hostnick] = l[1]
                max[hostnick] = l[2]
                wday[hostnick] = l[3]
                interactive[hostnick] = l[4]
                # Try to get corresponding pid
                try:
                    pidFile = open(jobfile + '.' + hostnick + '.pid','r')
                    line = pidFile.readline()
                    pid[hostnick] = eval(line)
                    pidFile.close()
                except:
                    pid[hostnick] = None

    hostfile.close()

    if len(sys.argv) > 4:
	for host in onlyhosts:
	    if not host in hosts:
		print "Error: illegal host",host
		onlyhosts.remove(host)
	hosts=onlyhosts

	
    if command in ['stop','cont','quit','term','kill']:

	signal = {'stop': 'USR1',
		  'cont': 'CONT',
		  'quit': 'USR2',
		  'term': 'TERM', 
		  'kill': 'KILL' }

	for hostnick in hosts:
	    if pid[hostnick] != None:
		commandLine = "rsh %s kill -%s %d" % (hostnick,signal[command],pid[hostnick])
		print commandLine
		result = os.popen(commandLine,'r').readlines()
		for line in result:
			print line

    elif command == 'check':

	for hostnick in hosts:
	    if pid[hostnick] != None:
		commandLine = "rsh %s ps -p %d -o pid,time,s,fname" % (hostnick,pid[hostnick])
		print commandLine
		result = os.popen(commandLine,'r').readlines()
		for line in result:
			sys.stdout.write(line)

    elif command == 'load':
	commandLine = "rup"
	for host in hosts:
	    commandLine = commandLine + ' ' + host 
	result = os.popen(commandLine,'r').readlines()
	for line in result:
	    print line[:-1]
    else:
	print "Illegal command",command
    
