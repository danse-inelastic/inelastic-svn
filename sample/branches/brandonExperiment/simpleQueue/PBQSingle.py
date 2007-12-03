#!/usr/bin/env python
################################################################################
#
#       File:   PBQSingle.py
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
# Single machine version
#
# To do:
#
# - change log etc. filename to include pid for detecting multiple
#   scheduler, lock access ?
# ? record completed jobs (seperatly ?) as jobfile.host.completed
# - record running time of completed jobs (Maybe)
# - increase sleep time only if we have no stopped jobs!
#

from time import time,localtime,strftime,sleep
import regex
import regsub
import os
import sys
import signal
import posix
import errno
import fcntl
import string



# Utility functions etc.
gInfinity = 444

def hibyte(b):
    return b >> 8

def lobyte(b):
    return b - ((b >> 8) << 8)


gLogFile = sys.stdout
gLogFileName = None

def log(line):
    """ All output goes through log to allow easy redirection etc. 
        if global var gLogFileName is set"""
    try:
	if gLogFileName == None:
	    logFile = sys.stdout
	else:
	    logFile = open(gLogFileName, 'a')    

	logFile.write(strftime('%H:%M:%S',localtime(time())) + ' ' + line + '\n')
	logFile.flush()

	if gLogFileName != None:
	    logFile.close()
    except:
	# Caught a stupid IOError here
	i = 2

################################################################################
#
# Abstract machine class
#
################################################################################
class Machine:
    """ Abstract base class for machines. Only relies on posix functionality.
Only instantiate sub-classes

- nick         short name for host
- name         complete name 
- arch         the architecture
- maxLoad      maximum load = number of CPUs
- maxLoadDay   maximum load during the day (M-F, 8am - 8pm)
- interactive  how many CPUs to surrender to interactive users

""" 
    def __init__(self,nick,name,arch,maxLoad,maxLoadDay,interactive):
        self.nick        = nick 
        self.name        = name
        self.arch        = arch
        self.maxLoad     = maxLoad
        self.maxLoadDay  = maxLoadDay
        self.interactive = interactive
        self.load        = 0

    def MaxLoad(self):
        """ Calculate the maximal load allowable on host at this time. """
#        t = localtime(time())
#        dayOfTheWeek = t[6]
#        hour = t[3]
#        if dayOfTheWeek == 5 or dayOfTheWeek == 6: # its weekend
#            return self.maxLoad
#        if 8 < hour and hour < 20: # Only respect active users during the day
#            active = self.ActiveUsers()
#    	    if active > 4: # Cheating ?
#                return max(0,self.maxLoadDay - 1)
#    	    elif active > 11:
#                return max(0,self.maxLoadDay - 2)
#    	    else:
#                return self.maxLoadDay
#    	else:
#    	    return self.maxLoad		
        return self.maxLoad

    def Load(self):
    	""" Abstract method """
    	return self.load

    def ResidualLoad(self):
    	""" How much additional load could be put on the machine """
        max=self.MaxLoad()
        load=self.Load()
    	return self.MaxLoad() - self.Load()

    def StartJob(self,command,args):
    	""" Fork a child, make it process group leader, nice 19, make it
    	    ignore SIGHUP """
    	pid = os.fork()
    	
    	if pid == 0: # Child
    	    os.setsid() # Make child process group leader
    	    # so we can stop child and all its children
    	    os.nice(19)
    	    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    	    os.execv(command, args)
    	else: # Parent
    	    return pid

    def SignalPID(self,pid,sig):
    	""" Send one of the signals QUIT KILL STOP CONT to specified
    	    PID """
    	signals = {'QUIT': 3, 'KILL': 9, 'STOP': 23, 'CONT': 25}
    	try:
    	    os.kill(-pid,signals[sig]) # -pid since we did set pgid to pid
    	    # and we are trying to kill all children too
    	except os.error:
    	    log("%12s kill - %s %d failed" % (self.nick,sig,pid))

    def ReturnValue(self,pid):
        """ Try to obtain return value for child pid 
- (None,None) if the process pid is still running
- (-1, errMsg) if we cant find pid or an error occured
- (1, 'Completed') else """
        try:
    	    #(p,status) = os.waitpid(pid,posix.WNOHANG)
    	    (p,status) = os.waitpid(pid,posix.WNOHANG)
            if p == 0: # Process is not yet done 
                return (None,None) 
    		
    	    signal = lobyte(status)
    
    	    if signal == 0: # child wasnt killed by signal
                exitCode = hibyte(status)
    		if exitCode == 0:
    		    return (1, 'Completed')
    		else:
    		    return (-1, 'Error: exited with %d' % exitCode)
    	    else:
                return (-1, 'Error: child was signaled %d' % signal)
    		
    	except:
    	    log("Machine.ReturnValue: Error in waitpid %d" % pid)
    	    return (-1,'Process vanished')

class Linux(Machine):
    """ Implement Linux-specific behaviour """
    def __init__(self,nick,name,maxLoad,maxLoadDay,interactive):
        Machine.__init__(self,nick,name,"linux",maxLoad,maxLoadDay,interactive)

    def ActiveUsers(self):
        """ Determine number of active users on host:
            An active user is someone who has not been idle for more
            than a minute """
        active = 0
        try:
            users = os.popen("who -u",'r').readlines()
            for u in users:
                time = string.split(u)[5] # idle
            if time == '.':
                active = active + 1
            elif regex.match('[0-9]+:[0-9]',time) > -1:
                minutes = string.split(time,':')[0]
                if eval(minutes) < 1:
                    active = active + 1
            return active
        
        except:
            log("%12s could not nr of active users" % self.nick)
            return active
    
    def Load(self):
        """ Determine load for the machine """
        try:
            pat = "load average: \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\)"
            x = regex.compile(pat)
            uptime = os.popen("uptime",'r').readline()
            if x.search(uptime) > 0:
                load = eval(x.group(1))
                return load
            else:
                return gInfinity # XXX Hack
        except:
            log("%12s could not determine load" % self.nick)
            return gInfinity # Will always be larger than MaxLoad !!
    
    def StatusPID(self,pid):
        """ Obtain the status of the process pid. Return values are
            'Running','Sleeping','Runable','Zombie','Stopped','Error' """    
        output = os.popen("ps -p %d -o s" % pid,'r').readlines()
        # Produces eg.
        # S
        # O
        map = {'O': 'Running',
               'S': 'Sleeping',
               'R': 'Runable',
               'Z': 'Zombie',
               'T': 'Stopped'}
        if len(output) < 2:
            return 'Error'
        return map[output[1][0]]

class Upgrayedd(Machine): #NOT FINISHED
    """ Implement Upgrayedd-specific behaviour """
    def __init__(self,nick,name,maxLoad,maxLoadDay,interactive):
        Machine.__init__(self,nick,name,"linux",maxLoad,maxLoadDay,interactive)

    def ActiveUsers(self):
        """ Determine number of active users on host:
            An active user is someone who has not been idle for more
            than a minute """
        active = 0
        try:
            users = os.popen("who -u",'r').readlines()
            for u in users:
                time = string.split(u)[5] # idle
            if time == '.':
                active = active + 1
            elif regex.match('[0-9]+:[0-9]',time) > -1:
                minutes = string.split(time,':')[0]
                if eval(minutes) < 1:
                    active = active + 1
            return active
        
        except:
            log("%12s could not nr of active users" % self.nick)
            return active
    
    def Load(self):
        """ Determine load for the machine """
        try:
            pat = "load average: \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\)"
            x = regex.compile(pat)
            uptime = os.popen("uptime",'r').readline()
            if x.search(uptime) > 0:
                load = eval(x.group(1))
                return load
            else:
                return gInfinity # XXX Hack
        except:
            log("%12s could not determine load" % self.nick)
            return gInfinity # Will always be larger than MaxLoad !!
    
    def StatusPID(self,pid):
        """ Obtain the status of the process pid. Return values are
            'Running','Sleeping','Runable','Zombie','Stopped','Error' """    
        output = os.popen("ps -p %d -o s" % pid,'r').readlines()
        # Produces eg.
        # S
        # O
        map = {'O': 'Running',
               'S': 'Sleeping',
               'R': 'Runable',
               'Z': 'Zombie',
               'T': 'Stopped'}
        if len(output) < 2:
            return 'Error'
        return map[output[1][0]]


class Solaris(Machine):
    """ Implement Solaris-specific behaviour """
    def __init__(self,nick,name,maxLoad,maxLoadDay,interactive):
    	Machine.__init__(self,nick,name,"sol2",maxLoad,maxLoadDay,interactive)

    def ActiveUsers(self):
    	""" Determine number of active users on host:
    	    An active user is someone who has not been idle for more
    	    than a minute """
    	active = 0
    	try:
    	    users = os.popen("who -u",'r').readlines()
    	    for u in users:
    		time = string.split(u)[5] # idle
    		if time == '.':
    		    active = active + 1
    		elif regex.match('[0-9]+:[0-9]',time) > -1:
    		    minutes = string.split(time,':')[0]
    		    if eval(minutes) < 1:
    			active = active + 1
    	    return active
    	
    	except:
    	    log("%12s could not nr of active users" % self.nick)
    	    return active
    
    def Load(self):
        """ Determine load for the machine """
        try:
            pat = "load average: \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\)"
    	    x = regex.compile(pat)
    	    uptime = os.popen("uptime",'r').readline()
    	    if x.search(uptime) > 0:
                load = eval(x.group(1))
                return load
    	    else:
                return gInfinity # XXX Hack
    	except:
    	    log("%12s could not determine load" % self.nick)
    	    return gInfinity # Will always be larger than MaxLoad !!
	
    def StatusPID(self,pid):
    	""" Obtain the status of the process pid. Return values are
    	    'Running','Sleeping','Runable','Zombie','Stopped','Error' """    
    	output = os.popen("ps -p %d -o s" % pid,'r').readlines()
    	# Produces eg.
    	# S
    	# O
    	map = {'O': 'Running',
    	       'S': 'Sleeping',
    	       'R': 'Runable',
    	       'Z': 'Zombie',
    	       'T': 'Stopped'}
    	if len(output) < 2:
    	    return 'Error'
    	return map[output[1][0]]

class SGI(Machine):
    """ Implement SGI-specific behaviour """
    def __init__(self,nick,name,maxLoad,maxLoadDay,interactive):
    	Machine.__init__(self,nick,name,"sgi",maxLoad,maxLoadDay,interactive)

    def ActiveUsers(self):
        """ Determine number of active users on host:
            An active user is someone who has not been idle for more
            than a minute """
        active = 0
        # Looks just like on Solaris
        # BCchallenge01:/users/xprakt% who -u
        # pkr        ttyq0        Jul  7 07:59  0:51   2213
        # ole        ttyq1        Jul  9 07:01  5:04   8161
        # xprakt     ttyq2        Jul  9 12:07   .     9533
        # ole        ttyq3        Jul  8 07:34  old    4076
        try:
            users = os.popen("who -u",'r').readlines()
            for u in users:
        	time = string.split(u)[5] # idle
        	if time == '.':
        	    active = active + 1
        	elif regex.match('[0-9]+:[0-9]',time) > -1:
        	    minutes = string.split(time,':')[0]
        	    if eval(minutes) < 1:
        		active = active + 1
            return active
        
        except:
            log("%12s could not nr of active users" % self.nick)
            return active
    
    def Load(self):
    	""" Determine load for the machine """
    	# BCchallenge01:/users/xprakt% uptime
    	#  12:08pm  up 3 days,  4:26,  6 users,  load average: 0.07, 0.04, 0.00
    	try:
    	    pat = "load average: \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\)"
    	    x = regex.compile(pat)
    	    uptime = os.popen("uptime",'r').readline()
    	    if x.search(uptime) > 0:
    		load = eval(x.group(1))
    		return load
    	    else:
    		return gInfinity # XXX Hack
    	except:
    	    log("%12s could not determine load" % self.nick)
    	    return gInfinity # Will always be larger than MaxLoad !!
	
    def StatusPID(self,pid):
    	""" Obtain the status of the process pid. Return values are
    	    'Running','Sleeping','Runable','Zombie','Stopped','Error' """    
    	output = os.popen("ps -p %d -o state" % pid,'r').readlines()
    	# Produces eg.
    	# S
    	# O
    	map = {'O': 'Running',
    	       'S': 'Sleeping',
    	       'R': 'Runable',
    	       'Z': 'Zombie',
    	       'T': 'Stopped'}
    	if len(output) < 2:
    	    return 'Error'
    	return map[output[1][0]]

class AIX(Machine):
    """ Implement AIX-specific behaviour """
    def __init__(self,nick,name,maxLoad,interactive):
    	Machine.__init__(self,nick,name,"aix",maxLoad,interactive)
    
    def Load(self):
    	""" Determine load for the machine """
    	try:
    	    pat = "load average: \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\), \([0-9]+\.[0-9]+\)"
    	    x = regex.compile(pat)
    	    uptime = os.popen("uptime",'r').readline()
    	    if x.search(uptime) > 0:
    		load = eval(x.group(1))
    		# log("%s has load %2.2f" % (self.nick,load))
    		return load
    	    else:
    		return gInfinity # XXX Hack
    	except:
    	    log("%12s could not determine load" % self.nick)
    	    return gInfinity # Will always be larger than MaxLoad !!
	
    def StatusPID(self,pid):
    	""" Obtain the status of the process pid. Return values are
    	    'Running','Sleeping','Runable','Zombie','Stopped','Error' """    
    	output = os.popen("ps s %d" % pid,'r').readlines()
    	# Produces eg.
    	#  SSIZ     PID    TTY STAT  TIME COMMAND
            #     0   75922 pts/85 A     0:01 -tcsh 
    	pat = "\([O|A|W|I|Z|T]\)"
    	x = regex.compile(pat) 
    
    	map = {'A': 'Running',
    	       'W': 'Sleeping',
    	       'I': 'Runable',
    	       'O': 'Zombie',
    	       'T': 'Stopped'}
    	if len(output) < 2:
    	    return 'Error'
    	return map[output[1][0]]

################################################################################
#
# A Job
#
################################################################################
class Job:
    """ Wrapper for one Job """

    def __init__(self,command,args):
    	self.status  = 'Pending'
    	self.command = command
    	self.args    = args
    	self.machine = None
    	self.pid     = None
    	self.killed  = 0
    	self.final   = "" # the final status
    	self.info    = self.command
    	for a in args[1:]:
    	    self.info = self.info + ' ' + a 

    def StartOn(self,machine):
    	self.machine = machine
    	self.pid = self.machine.StartJob(self.command,self.args)
    	log("%12s started job pid=%d" % (self.machine.nick,self.pid))
    	self.status = 'Running'

    def Stop(self):
    	self.machine.SignalPID(self.pid,'STOP')
    	log("%12s stopped job pid=%d" % (self.machine.nick,self.pid))
    	self.status = 'Stopped'
	    	
    def Cont(self):
    	self.machine.SignalPID(self.pid,'CONT')
    	log("%12s continued job pid=%d" % (self.machine.nick,self.pid))
    	self.status = 'Running'

    def Kill(self):
    	self.machine.SignalPID(self.pid,'KILL')
    	log("%12s killed job pid=%d" % (self.machine.nick,self.pid))
    	self.status = 'Killed'
    	self.killed = 1

    def Terminated(self):
    	""" Determine if Job terminated. Return values are
    	    - 1 if terminated
    	    - 0 if running
    	    - -1 if dead """
    	(code,msg) = self.machine.ReturnValue(self.pid)
    	if code == None:
    	    return 0
    	else:
    	    if code == -1: # Kill father (and other children) 
                self.Kill() # of manually killed child
                self.status = 'Error'
    	    else:
                self.status = 'Completed'	
    	    # NOTE: This might raise an error when there was exactly one process
    	    self.final = msg
    	    return code
	    
    def Status(self):
    	""" possible return values 
    	    - 'Running':   the jobs is still on the machine and appears to be in
    	                   good health
    	    - 'Stopped':   the jobs has been stopped (if we did it, scheduler knows
    	                   about it
    	    - 'Error':     an error occurred while running the job (self.final holds
    	                   more info then)
                - 'Completed': the jobs was completed """
    	if self.pid == None:
    	    return self.status
    	status = self.machine.StatusPID(self.pid)
    	if status in ['Running','Sleeping','Runable','Zombie']:
    	    return 'Running'
    	else:
    	    return status
	    

################################################################################
#
# lockfile controlled access to Jobfile. Is also a Job-factory
#
################################################################################
class JobFile:
    """ Provide lockfile controlled access to Jobfile. It is a
        Job-factory """
    
    def __init__(self, fileName):
    	self.fileName = fileName
		
    def GetNextJob(self):
    	""" returns 
    	    - the next job to run, or 
    	    - None, if there are no more jobs """
    	jobFile = open(self.fileName,'r+')
    	fcntl.flock(jobFile.fileno(),fcntl.LOCK_EX)
    	first = jobFile.readline()
    	lines = jobFile.readlines() # Need buffer here
    	jobFile.seek(0)
    	if len(lines) > 0:
    	    for line in lines:
    		jobFile.write(line)	
    	jobFile.truncate()
    	jobFile.close()
    	if first == "":
    	    return None
    	else:
    	    # cmdName arg1 arg2 arg3 ... 
    	    args = regsub.split(first[:-1],' ')
    	    job = Job(args[0],args)
    	    return job



################################################################################
#
# The Scheduler
#
################################################################################
class Scheduler:

    def __init__(self,host,jobFile):
    	self.host             = host
    	self.running          = []
     	self.stopped          = []
    	self.completed        = [] 
    	self.error            = []
    	self.jobsPending      = 1
    	self.jobFileName      = jobFile
    	self.jobFile          = JobFile(jobFile)
    	self.sleepTime        = 15 # seconds
    	self.action           = None # Can be 'GoToSleep' or 'Terminate'
    	self.runForever       = 1
    	self.startNewJobs     = 1

    def Run(self):
    	log("%12s scheduler started pid=%d" % (self.host.nick,posix.getpid()))
    
    	signal.signal(signal.SIGUSR2, self.handleUSR2)
    	signal.signal(signal.SIGUSR1, self.handleUSR1)
    	signal.signal(signal.SIGCONT, self.handleCONT)
    	signal.signal(signal.SIGTERM, self.handleTERM)
    
    	while self.Done() == 0:
    
    	    # React to signal received 
    	    if self.action == 'GoToSleep':
                self.Stop()
                self.action = None
                os.kill(posix.getpid(),23)
    	    elif self.action == 'Terminate':
                self.Kill()
                self.jobsPending = 0
                self.action = None
    
    	    self.ScheduleJobs()
    	    self.WriteRunningJobs()
    	    self.WriteStoppedJobs()
    
    	    if self.action == None:
    		if self.jobsPending == 0 and len(self.running) == 0 and len(self.stopped) == 0 and self.runForever == 1:
    		    self.sleepTime = 300
    		else:
    		    self.sleepTime = 15		
    		os.system("sleep %d" % self.sleepTime)
    	log("%12s scheduler done" % self.host.nick)
    	posix.remove(self.jobFileName + '.' + self.host.nick + '.pid')

    def WriteErrorJob(self,job):
    	""" Write job to error log file """
    	fileName = self.jobFileName + '.' + self.host.nick + '.errors'
    	try:
    	    file = open(fileName,'a+')
    	    file.write(job.info + '\n')
    	    file.close()
    	except:
    	    i = 1
	
    def WriteRunningJobs(self):
    	""" Write out all running jobs """
    	try:
    	    fileName = self.jobFileName + '.' + self.host.nick + '.running'
    	    if len(self.running) > 0:
    		file = open(fileName,'w')
    		for job in self.running:
    		    file.write(job.info + '\n')
    		file.close()
    	    else:
    		if os.path.isfile(fileName):
    		    posix.remove(fileName)
    	except:
    	    log("%12s WriteRunningJobs failed" % self.host.nick)
		
    def WriteStoppedJobs(self):
    	""" Write out all stopped jobs """
    	try:
    	    fileName = self.jobFileName + '.' + self.host.nick + '.stopped'
    	    if len(self.stopped) > 0:
    		file = open(fileName,'w')
    		for job in self.stopped:
    		    file.write(job.info + '\n')
    		file.close()
    	    else:
    		if os.path.isfile(fileName):
    		    posix.remove(fileName) 
    	except:
    	    log("%12s WriteStoppedJobs failed" % self.host.nick)

    def Kill(self):
    	""" Kill all runnning jobs (this is bound to term signal) """
    	for job in self.running:
    	    job.Kill()	
    	for job in self.stopped:
    	    job.Kill()	
    	posix.remove(self.jobFileName + '.' + self.host.nick + '.pid')
    	log("%12s scheduler done" % self.host.nick)
    	sys.exit(1)

    def Stop(self):
    	""" Stop all running jobs """
    	for job in self.running:
    	    job.Stop()	
    	    self.stopped.append(job)		
    	self.running = []

    # Signal handlers
    def handleUSR2(self,*args):
    	""" Exit properly by letting all jobs currently running finish,
    	    but dont start new ones """
    	log("%12s scheduler: sig USR2: wont start more jobs" % self.host.nick)
    	self.startNewJobs = 0
    	self.runForever = 0 

    def handleUSR1(self,*args):
    	""" use instead of kill -STOP to stop all jobs and scheduler. """
    	log("%12s scheduler: sig USR1: going to sleep" % self.host.nick)
    	self.action = 'GoToSleep'

    def handleCONT(self,*args):
    	""" we only install handler for kill -CONT so that we can log """
    	log("%12s scheduler: sig CONT: waking up" % self.host.nick)

    def handleTERM(self,*args):
    	""" Kill all jobs """
    	log("%12s scheduler: sig TERM: killing all jobs" % self.host.nick)
    	self.action = 'Terminate'
	
    def Done(self):
    	""" We are Done scheduling if we have no pending and no
    	    stoppped and no running jobs"""	
    	if self.runForever == 1:
    	    return 0 # We are never done
    		
    	if self.jobsPending == 1 or len(self.stopped) > 0 or len(self.running) > 0:
    	    return 0
    	else:
    	    return 1

    def ScheduleJobs(self):
    	# Print out job counts 
    	resLoad = self.host.ResidualLoad()
    	log("%12s res. load %2.2f\trunning=%d stopped=%d" % (
    	    self.host.nick,
    	    resLoad,
    	    len(self.running),
    	    len(self.stopped)))
    
    	# Check running jobs for return values
    	for job in self.running:
    
    	    t = job.Terminated()
    	    if t == 1:
    		log("%12s pid=%d %s '%s'" % (self.host.nick,job.pid,job.final,job.info))
    		self.running.remove(job)
    		self.completed.append(job)
    	    elif t == -1:
    		log("%12s pid=%d %s '%s'" % (self.host.nick,job.pid,job.final,job.info))
    		self.running.remove(job)
    		self.error.append(job)
    		self.WriteErrorJob(job)
    		
    	    status = job.Status()
    	    
    	    if status == 'Stopped':
    		log("%12s pid=%d was stopped by somebody. Continuing" % (self.host.nick,
    									  job.pid))
    		job.Cont()
    		    
    		
    	# Determine the number of jobs we can start
    	if resLoad > 0: # We can put additional load on the machine
    	    maxJobsOnHost = min( max(self.host.MaxLoad() - len(self.running),0),
    				 int(resLoad + .5))				 
    	    nrOfJobs = min(len(self.stopped),maxJobsOnHost)
    	    for i in xrange(nrOfJobs):
    		job = self.stopped[0]
    		self.stopped.remove(job)
    		job.Cont()
    		self.running.append(job)
    		
    	    # Start new jobs 
    	    # Cant start more than we have left and as most as many
    	    # as left form restarting stopped jobs ...
    	    
    	    if self.startNewJobs == 1:
    		nrOfJobs = max(maxJobsOnHost - nrOfJobs,0)
    		for i in xrange(nrOfJobs):
    		    job = self.jobFile.GetNextJob()
    		    if job == None:
    			self.jobsPending = 0
    			break
    		    else:
    			job.StartOn(self.host)
    			self.running.append(job)
    
    	else:
    	    # Stop running jobs 
    	    nrOfJobs = min(len(self.running),int(-resLoad + .5))
    	    #log("%12s nrOfJobs to stop=%d" % (self.host.nick,nrOfJobs))
    	    for i in xrange(nrOfJobs):
    		job = self.running[0]
    		self.running.remove(job)
    		job.Stop()	
    		self.stopped.append(job)


if __name__ == '__main__':
    try:
        hostnick = posix.environ['HOSTNAME']
    except:
        hostnick = os.popen("/bin/hostname",'r').readline()[:-1]

    # Take only name up to first .
    hostnick = string.lower(string.split(hostnick,'.')[0])
	
    if len(sys.argv) < 3:
        print "Synopsis: PBQSingle.py hostfile jobfile"
        sys.exit(1)

    jobfile  = sys.argv[2]

    hostfile = open(sys.argv[1],'r')
    lines = hostfile.readlines()
    hostname = None
    for line in lines:
        l = string.split(line)
        if len(l) > 0:
            # Take only name up to first .
            h = string.lower(string.split(l[0],'.')[0])
            if h == hostnick:
        	hostname = l[0]
        	arch = l[1]
        	mload = eval(l[2])
        	wday = eval(l[3])
        	interactive = l[4]
        	break
    hostfile.close()

    if hostname == None:
        print "PBQSingle Error: host %s not in hostfile %s" % (hostnick,sys.argv[1])
        sys.exit(1)

    if string.lower(arch) == 'linux':
        host = Linux(hostnick,hostname,mload,wday,interactive)
    elif string.lower(arch) == 'sol2':
        host = Solaris(hostnick,hostname,mload,wday,interactive)
    elif string.lower(arch) == 'aix4':
        host = AIX(hostnick,hostname,mload,wday,interactive)
    elif string.lower(arch) == 'sgi':
        host = SGI(hostnick,hostname,mload,wday,interactive)
    else:
        print "PBQSingle Error: arch %s is unknown" % arch 
        sys.exit(1)

    # Looks good if we got so far -- return our pid by writing it to a pid file
    pidfile = open(jobfile + '.' + hostnick + '.pid','w')
    pidfile.write("%d\n" %posix.getpid())
    pidfile.close()

    gLogFileName = jobfile + '.' + hostnick + '.log'
    S = Scheduler(host, jobfile)
    S.Run()



