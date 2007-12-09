# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
'''
runSim.py

setting up and running the simulator, for Simulate or Minimize
(i.e. the same code that would change if the simulator interface changed),
and the user-visible commands for those operations.

$Id: runSim.py,v 1.166 2007/06/04 20:36:39 polosims Exp $

History: Mark created a file of this name, but that was renamed to SimSetup.py
by bruce on 050325.

Bruce 050324 pulled in lots of existing code for running the simulator
(and some code for reading its results) into this file, since that fits
its name. That existing code was mostly by Mark and Huaicai, and was
partly cleaned up by Bruce, who also put some of it into subclasses
of the experimental CommandRun class.

Bruce 050331 is splitting writemovie into several methods in more than
one subclass (eventually) of a new SimRunner class.

bruce 050901 and 050913 used env.history in some places.

bruce 051115 some comments and code cleanup; add #SIMOPT wherever a simulator executable command-line flag is hardcoded.

bruce 051231 partly-done code for using pyrex interface to sim; see use_dylib
'''

from debug import print_compact_traceback, _sim_params_set, _sim_param_values
from qt4transition import qt4todo
import platform
from platform import fix_plurals
import os, sys, time
from math import sqrt
from SimSetup import SimSetup
from PyQt4.Qt import QApplication, QCursor, Qt, QStringList, QProcess, QObject, SIGNAL
from movie import Movie
from HistoryWidget import redmsg, greenmsg, orangemsg, quote_html, _graymsg
import env
from env import seen_before
from VQT import A, V
import re
from chem import AtomDict
from debug_prefs import debug_pref, Choice, Choice_boolean_True, Choice_boolean_False

from prefs_constants import electrostaticsForDnaDuringAdjust_prefs_key
from prefs_constants import electrostaticsForDnaDuringMinimize_prefs_key
from prefs_constants import electrostaticsForDnaDuringDynamics_prefs_key
# more imports lower down

debug_sim_exceptions = 0 # DO NOT COMMIT WITH 1 -- set this to reproduce a bug mostly fixed by Will today #bruce 060111

debug_all_frames = 0 # DO NOT COMMIT with 1
debug_all_frames_atom_index = 1 # index of atom to print in detail, when debug_all_frames

debug_sim = 0 # DO NOT COMMIT with 1
debug_pyrex_prints = 0 # prints to stdout the same info that gets shown transiently in statusbar
debug_timing_loop_on_sbar = 0

use_pyrex_sim = True 
    # Use pyrex sim by default.  Use debug menu to use the standalone sim. mark 060314.

if debug_sim_exceptions:
    debug_all_frames = 1

_FAILURE_ALREADY_DOCUMENTED = -10101

# ==

def timestep_flag_and_arg( mflag = False): #bruce 060503
    timestep_fs_str = debug_pref("dynamics timestep (fs)", Choice(["0.1", "0.2", "0.5", "1.0"]), non_debug = True)
    timestep_fs = float(timestep_fs_str)
        # kluge: we use a string in the menu, since float 0.1 shows up in menu text as 0.100000000000000001 or so
    timestep = timestep_fs * 1e-15
    use_timestep_arg = (timestep_fs != 0.1) and not mflag
        # only supply the arg if not minimizing, and if a non-default value is chosen
        # (in case the code to supply it has a bug, or supplies it to the sim in the wrong format)
    return use_timestep_arg, timestep

##timestep_flag_and_arg() # Exercise the debug_pref so it shows up in the debug menu before the first sim/min run...
##    # Oops, this doesn't work from here, since this module is not imported until it's needed! Never mind for now,
##    # since it won't be an issue later when timestep is again supported as a movie attribute.

# ==




class SimRunner:
    "class for running the simulator [subclasses can run it in special ways, maybe]"
    #bruce 050330 making this from writemovie and maybe some of Movie/SimSetup; experimental,
    # esp. since i don't yet know how much to factor the input-file writing, process spawning,
    # file-growth watching, file reading, file using. Surely in future we'll split out file using
    # into separate code, and maybe file-growth watching if we run procs remotely
    # (or we might instead be watching results come in over a tcp stream, frames mixed with trace records).
    # So for now, let's make the minimal class for running the sim, up to having finished files to look at
    # but not looking at them, then the old writemovie might call this class to do most of its work
    # but also call other classes to use the results.

    # wware 060406 bug 1263 - provide a mechanism to be notified when the program is exiting
    # This is set to True in ops_files.py. This is a class (not instance) variable which matters
    # because ops_files.py can set this without a reference to the currently active SimRunner instance.
    PREPARE_TO_CLOSE = False
    
    def __init__(self, part, mflag, simaspect = None, use_dylib_sim = use_pyrex_sim, cmdname = "Simulator", cmd_type = 'Minimize'):
            # [bruce 051230 added use_dylib_sim; revised 060102; 060106 added cmdname]
        "set up external relations from the part we'll operate on; take mflag since someday it'll specify the subclass to use"
        self.assy = assy = part.assy # needed?
        #self.tmpFilePath = assy.w.tmpFilePath
        self.win = assy.w  # might be used only for self.win.progressbar.launch
        self.part = part # needed?
        self.mflag = mflag # see docstring
        self.simaspect = simaspect # None for entire part, or an object describing what aspect of it to simulate [bruce 050404]
        self.errcode = 0 # public attr used after we're done; 0 or None = success (so far), >0 = error (msg emitted)
        self.said_we_are_done = False #bruce 050415
        self.pyrexSimInterrupted = False  #wware 060323, bug 1725, if interrupted we don't need so many warnings
        
        prefer_standalone_sim = debug_pref("force use of standalone sim", Choice_boolean_False,
                                      prefs_key = 'use-standalone-sim', non_debug = True)
        
        if prefer_standalone_sim:
            use_dylib_sim = False
        self.use_dylib_sim = use_dylib_sim #bruce 051230
            
        self.cmdname = cmdname
        self.cmd_type = cmd_type #060705
        if not use_dylib_sim:
            env.history.message(greenmsg("Using the standalone simulator (not the pyrex simulator)"))
        return
    
    def run_using_old_movie_obj_to_hold_sim_params(self, movie): #bruce 051115 removed unused 'options' arg
        self._movie = movie # general kluge for old-code compat (lots of our methods still use this and modify it)
        # note, this movie object (really should be a simsetup object?) does not yet know a proper alist (or any alist, I hope) [bruce 050404]
        self.errcode = self.set_options_errQ( ) # set movie alist, output filenames, sim executable pathname (verify it exists)
            #obs comment [about the options arg i removed?? or smth else?]
            # options include everything that affects the run except the set of atoms and the part
        if self.errcode: # used to be a local var 'r'
            # bruce 051115 comment: more than one reason this can happen, one is sim executable missing
            return
        self.sim_input_file = self.sim_input_filename() # might get name from options or make up a temporary filename
        self.set_waitcursor(True)
        
        # Disable some QActions (menu items/toolbar buttons) while the sim is running.
        self.win.disable_QActions_for_sim(True)
        
        try: #bruce 050325 added this try/except wrapper, to always restore cursor
            self.write_sim_input_file() # for Minimize, uses simaspect to write file; puts it into movie.alist too, via writemovie
            self.simProcess = None #bruce 051231
            self.spawn_process()
                # spawn_process is misnamed since it can go thru either interface (pyrex or exec OS process),
                # since it also monitors progress and waits until it's done,
                # and insert results back into part, either in real time or when done.
                # result error code (or abort button flag) stored in self.errcode
        except:
            print_compact_traceback("bug in simulator-calling code: ")
            self.errcode = -11111
        self.set_waitcursor(False)
        self.win.disable_QActions_for_sim(False)
        
        if not self.errcode:
            return # success
        if self.errcode == 1: # User pressed Abort button in progress dialog.
            msg = redmsg("Aborted.")
            env.history.message(self.cmdname + ": " + msg)

            if self.simProcess: #bruce 051231 added condition (since won't be there when use_dylib)
                ##Tries to terminate the process the nice way first, so the process
                ## can do whatever clean up it requires. If the process
                ## is still running after 2 seconds (a kludge). it terminates the 
                ## process the hard way.
                #self.simProcess.tryTerminate()
                #QTimer.singleShot( 2000, self.simProcess, SLOT('kill()') )
                
                # The above does not work, so we'll hammer the process with SIGKILL.
                # This works.  Mark 050210
                self.simProcess.kill()
            
        elif not self.pyrexSimInterrupted and self.errcode != _FAILURE_ALREADY_DOCUMENTED:   # wware 060323 bug 1725
            # Something failed...
            msg = redmsg("Simulation failed: exit code or internal error code %r " % self.errcode) #e identify error better!
            env.history.message(self.cmdname + ": " + msg)
                #fyi this was 'cmd' which was wrong, it says 'Simulator' even for Minimize [bruce 060106 comment, fixed it now]
        self.said_we_are_done = True # since saying we aborted or had an error is good enough... ###e revise if kill can take time.
        return # caller should look at self.errcode
        # semi-obs comment? [by bruce few days before 050404, partly expresses an intention]
        # results themselves are a separate object (or more than one?) stored in attrs... (I guess ###k)
        # ... at this point the caller probably extracts the results object and uses it separately
        # or might even construct it anew from the filename and params
        # depending on how useful the real obj was while we were monitoring the progress
        # (since if so we already have it... in future we'll even start playing movies as their data comes in...)
        # so not much to do here! let caller care about res, not us.
    
    def set_options_errQ(self): #e maybe split further into several setup methods? #bruce 051115 removed unused 'options' arg
        """Set movie alist (from simaspect or entire part); debug-msg if it was already set (and always ignore old value).
        Figure out and set filenames, including sim executable path.
        All inputs and outputs are self attrs or globals or other obj attrs... except, return error code if sim executable missing
        or on other errors detected by subrs.
        
        old docstring:
        Caller should specify the options for this simulator run
        (including the output file name);
        these might affect the input file we write for it
        and/or the arguments given to the simulator executable.
        Temporary old-code compatibility: use self._movie
        for simsetup params and other needed params, and store new ones into it.
        """
        part = self.part
        movie = self._movie

        # set up alist (list of atoms for sim input and output files, in order)
        if movie.alist is not None:
            # this movie object is being reused, which is a bug. complain... and try to work around.
            if platform.atom_debug: # since I expect this is possible for "save movie file" until fixed... [bruce 050404] (maybe not? it had assert 0)
                print "BUG (worked around??): movie object being reused unexpectedly"
            movie.alist = None
        movie.alist_fits_entire_part = False # might be changed below
        if not self.simaspect:
            # No prescribed subset of atoms to minimize. Use all atoms in the part.
            # Make sure some chunks are in the part.
            if not part.molecules: # Nothing in the part to minimize.
                msg = redmsg("Can't create movie.  No chunks in part.")
                    ####@@@@ is this redundant with callers? yes for simSetup,
                    # don't know about minimize, or the weird fileSave call in MWsem.
                env.history.message(msg)
                return -1
            movie.set_alist_from_entire_part(part) ###@@@ needs improvement, see comments in it
            for atm in movie.alist:
                assert atm.molecule.part == part ###@@@ remove when works
            movie.alist_fits_entire_part = True # permits optims... but note it won't be valid
                # anymore if the part changes! it's temporary... not sure it deserves to be an attr
                # rather than local var or retval.
        else:
            # the simaspect should know what to minimize...
            alist = self.simaspect.atomslist()
            movie.set_alist(alist)
            for atm in movie.alist: # redundant with set_alist so remove when works
                assert atm.molecule.part == part

        # Set up filenames.
        # We use the process id to create unique filenames for this instance of the program
        # so that if the user runs more than one program at the same time, they don't use
        # the same temporary file names.
        # We now include a part-specific suffix [mark 051030]]
        # [This will need revision when we can run more than one sim process
        #  at once, with all or all but one in the "background" [bruce 050401]]
        
        # simFilesPath = "~/materialBuilder/SimFiles". Mark 051028.
        from platform import find_or_make_materialBuilder_subdir
        simFilesPath = find_or_make_materialBuilder_subdir('SimFiles')
        
        # Create temporary part-specific filename.  Example: "partname-minimize-pid1000"
        # We'll be appending various extensions to tmp_file_prefix to make temp file names
        # for sim input and output files as needed (e.g. mmp, xyz, etc.)
        from movieMode import filesplit
        junk, basename, ext = filesplit(self.assy.filename)
        if not basename: # The user hasn't named the part yet.
            basename = "Untitled"
        self.tmp_file_prefix = os.path.join(simFilesPath, "%s-minimize-pid%d" % (basename, os.getpid()))
            
        r = self.old_set_sim_output_filenames_errQ( movie, self.mflag)
        if r: return r
        # don't call sim_input_filename here, that's done later for some reason

        # prepare to spawn the process later (and detect some errors now)
        bin_dir = self.sim_bin_dir_path()
        
        # Make sure the simulator exists (as dylib or as standalone program)
        if self.use_dylib_sim:
            #bruce 051230 experimental code
            self.dylib_path = bin_dir
                # this works for developers if they set up symlinks... might not be right...
            worked = self.import_dylib_sim(self.dylib_path)
            if not worked:
                # The dylib filename on Windows can be either sim.dll or sim.pyd -- should we mention them both?
                # If the imported name is not the usual one, or if two are present, should we print a warning?
                ##e Surely this message text (and the other behavior suggested above) should depend on the platform
                # and be encapsulated in some utility function for loading dynamic libraries. [bruce 060104]
                msg = redmsg("The simulator dynamic library [sim.so or sim.dll, in " + self.dylib_path +
                             "] is missing or could not be imported. Trying command-line simulator.")
                env.history.message(self.cmdname + ": " + msg)
                ## return -1
                self.use_dylib_sim = False
                ####@@@@ bug report: even after this, it will find tracefile from prior run (if one exists) and print its warnings.
                # probably we should remove that before this point?? [bruce 051230] [hmm, did my later removal of the old tracefile
                # fix this, or is it not removed until after this point?? bruce question 060102]

        if not self.use_dylib_sim:
            # "program" is the full path to the simulator executable. 
            if sys.platform == 'win32': 
                program = os.path.join(bin_dir, 'simulator.exe')
            else:
                program = os.path.join(bin_dir, 'simulator')
            if not os.path.exists(program):
                msg = redmsg("The simulator program [" + program + "] is missing.  Simulation aborted.")
                env.history.message(self.cmdname + ": " + msg)
                return -1
            self.program = program
        
        return None # no error
        
    def sim_bin_dir_path(self): #bruce 060102 split this out
        """Return pathname of bin directory that ought to contain simulator executable and/or dynamic library.
        (Doesn't check whether it exists.)
        """
        # filePath = the current directory NE-1 is running from.
        filePath = os.path.dirname(os.path.abspath(sys.argv[0]))
        return os.path.normpath(filePath + '/../bin')

    def import_dylib_sim(self, dylib_path): #bruce 051230 experimental code
        """Try to import the dynamic library version of the simulator, under the module name 'sim',
        located in dylib_path. Return a success flag.
        """
        import sys
        if not sys.modules.has_key('sim'):
            oldpath = sys.path
            sys.path = [dylib_path] + oldpath
                ##k Do we need to include oldpath here? if not, we get better error detection if we leave it out.
                # But we might need to (in principle), if this import has to do another one behind the scenes for some reason.
                ##e maybe for some errors we should remove this invalid module so we can try the import again later??
                # This might never work, since maybe Python removes it unless it got too far to try again;
                # if it does ever import it it won't do more (even with reload) until you rerun the app.
                # So it's probably not worth improving this error handling code.
            try:
                import sim
                assert sys.modules.has_key('sim')
                worked = True
            except:
                print_compact_traceback("error trying to import dylib sim: ")
                worked = False
                #e should we worry about whether sys.modules.has_key('sim') at this point? Might depend on how it failed.
            sys.path = oldpath
        else:
            worked = True # optimistic
        if worked:
            try:
                from sim import Minimize, Dynamics # the two constructors we might need to use
            except:
                worked = False
                print_compact_traceback("error trying to import Minimize and Dynamics from dylib sim: ")
        return worked
    
    def old_set_sim_output_filenames_errQ(self, movie, mflag):
        """Old code, not yet much cleaned up. Uses and/or sets movie.filename,
        with movie serving to hold desired sim parameters
        (more like a SimSetup object than a Movie object in purpose).
        Stores shell command option for using tracefile (see code, needs cleanup).
        Returns error code (nonzero means error return needed from entire SimRunner.run,
         and means it already emitted an error message).
        """
        # figure out filename for trajectory or final-snapshot output from simulator
        # (for sim-movie or minimize op), and store it in movie.moviefile
        # (in some cases it's the name that was found there).
        
        if mflag == 1: # single-frame XYZ file
            if movie.filename and platform.atom_debug:
                print "atom_debug: warning: ignoring filename %r, bug??" % movie.filename
            movie.filename = self.tmp_file_prefix + ".xyz"  ## "sim-%d.xyz" % pid
            
        if mflag == 2: #multi-frame DPB file
            if movie.filename and platform.atom_debug:
                print "atom_debug: warning: ignoring filename %r, bug??" % movie.filename
            movie.filename = self.tmp_file_prefix + ".dpb"  ## "sim-%d.dpb" % pid
        
        if movie.filename: 
            moviefile = movie.filename
        else:
            msg = redmsg("Can't create movie.  Empty filename.")
            env.history.message(self.cmdname + ": " + msg)
            return -1
            
        # Check that the moviefile has a valid extension.
        ext = moviefile[-4:]
        if ext not in ['.dpb', '.xyz']:
            # Don't recognize the moviefile extension.
            msg = redmsg("Movie [" + moviefile + "] has unsupported extension.")
            env.history.message(self.cmdname + ": " + msg)
            print "writeMovie: " + msg
            return -1
        movie.filetype = ext #bruce 050404 added this

        # Figure out tracefile name, store in self.traceFileName,
        # and come up with sim-command argument for it, store that in self.traceFileArg.
        if mflag:
            #bruce 050407 comment: mflag true means "minimize" (value when true means output filetype).
            # Change: Always write tracefile, so Minimize can see warnings in it.
            # But let it have a different name depending on the output file extension,
            # so if you create xxx.dpb and xxx.xyz, the trace file names differ.
            # (This means you could save one movie and one minimize output for the same xxx,
            #  and both trace files would be saved too.) That change is now in movie.get_trace_filename().
            self.traceFileName = movie.get_trace_filename()
                # (same as in other case, but retval differs due to movie.filetype)
        else:
            # The trace filename will be the same as the movie filename, but with "-trace.txt" tacked on.
            self.traceFileName = movie.get_trace_filename() # presumably uses movie.filename we just stored
                # (I guess this needn't know self.tmp_file_prefix except perhaps via movie.filename [bruce 050401])

        if self.traceFileName:
            self.traceFileArg = "-q" + self.traceFileName #SIMOPT
        else:
            self.traceFileArg = ""
                
        # This was the old tracefile - obsolete as of 2005-03-08 - Mark
        ## traceFileArg = "-q"+ os.path.join(self.tmpFilePath, "sim-%d-trace.txt" % pid) #SIMOPT

        return None # no error

    def sim_input_filename(self):
        """Figure out the simulator input filename
        (previously set options might specify it or imply how to make it up;
         if not, make up a suitable temp name)
        and return it; don't record it (caller does that),
        and no need to be deterministic (only called once if that matters).
        """         
        # We always save the current part to an MMP file before starting
        # the simulator.  In the future, we may want to check if assy.filename
        # is an MMP file and use it if not assy.has_changed().
        # [bruce 050324 comment: our wanting this is unlikely, and becomes more so as time goes by,
        #  and in any case would only work for the main Part (assy.tree.part).]
        return self.tmp_file_prefix + ".mmp" ## "sim-%d.mmp" % pid
    
    def write_sim_input_file(self):
        """Write the appropriate data from self.part (as modified by self.simaspect)
        to an input file for the simulator (presently always in mmp format)
        using the filename self.sim_input_file
        (overwriting any existing file of the same name).
        """
        part = self.part
        mmpfile = self.sim_input_file # the filename to write to
        movie = self._movie # old-code compat kluge
        assert movie.alist is not None #bruce 050404
        
        if not self.simaspect: ## was: if movie.alist_fits_entire_part:
            if debug_sim: #bruce 051115 added this
                print "part.writemmpfile(%r)" % (mmpfile,)
            stats = {}
            part.writemmpfile( mmpfile, leave_out_sim_disabled_nodes = True, sim = True, dict_for_stats = stats)
                #bruce 051209 added options  (used to be hardcoded in files_mpp, see below), plus a new one, dict_for_stats
                # As of 051115 this is still called for Run Sim.
                # As of 050412 this didn't yet turn singlets into H;
                # but as of long before 051115 it does (for all calls -- so it would not be good to use for Save Selection!).
                #
                #bruce 051209 addendum:
                # It did this [until today] via these lines in files_mmp (copied here so text searches can find them):
                #   mapping = writemmp_mapping(assy, leave_out_sim_disabled_nodes = True, sim = True)
                #       #bruce 050811 added sim = True to fix bug 254 for sim runs, for A6.
                # It would be better if it did this by passing its own (better-named) options to this writing method.
                # So I made that change now, and I'll also pass a place to accumulate stats into,
                # so I can complete the fix to bug 254 (by printing messages about X->H, albeit by copying similar code
                #  and figuring out the count differently) without making the klugetower even worse.
            nsinglets_H = stats.get('nsinglets_H', 0)
            if nsinglets_H: #bruce 051209 this message code is approximately duplicated elsewhere in this file
                info = fix_plurals( "(Treating %d bondpoint(s) as Hydrogens, during simulation)" % nsinglets_H )
                env.history.message( info)
        else:
            #bruce 051209 comment: I believe this case can never run (and is obs), but didn't verify this.
            if debug_sim: #bruce 051115 added this
                print "simaspect.writemmpfile(%r)" % (mmpfile,)
            # note: simaspect has already been used to set up movie.alist; simaspect's own alist copy is used in following:
            self.simaspect.writemmpfile( mmpfile) # this also turns singlets into H
            # obs comments:
            # can't yet happen (until Minimize Selection) and won't yet work 
            # bruce 050325 revised this to use whatever alist was asked for above (set of atoms, and order).
            # But beware, this might only be ok right away for minimize, not simulate (since for sim it has to write all jigs as well).
        
        ## movie.natoms = natoms = len(movie.alist) # removed by bruce 050404 since now done in set_alist etc.
        ###@@@ why does that trash a movie param? who needs that param? it's now redundant with movie.alist
        return
    
    def set_waitcursor(self, on_or_off): # [WARNING: this code is now duplicated in at least one other place, as of 060705]
        """For on_or_off True, set the main window waitcursor.
        For on_or_off False, revert to the prior cursor.
        [It might be necessary to always call it in matched pairs, I don't know [bruce 050401]. #k]
        """
        if on_or_off:
            # == Change cursor to Wait (hourglass) cursor
            
            ##Huaicai 1/10/05, it's more appropriate to change the cursor
            ## for the main window, not for the progressbar window
            QApplication.setOverrideCursor( QCursor(Qt.WaitCursor) )
            #oldCursor = QCursor(win.cursor())
            #win.setCursor(QCursor(Qt.WaitCursor) )
        else:
            QApplication.restoreOverrideCursor() # Restore the cursor
            #win.setCursor(oldCursor)
        return
    
    def spawn_process(self): # misnamed, since (1) also includes monitor_progress, and (2) doesn't always use a process
        """Actually spawn the process [or the extension class object],
        making its args [or setting its params] based on some of self's attributes.
        Wait til we're done with this simulation, then record results in other self attributes.
        """
        if debug_sim: #bruce 051115 added this; confirmed this is always called for any use of sim (Minimize or Run Sim)
            print "calling spawn_process" 
        # First figure out process arguments
        # [bruce 050401 doing this later than before, used to come before writing sim-input file]
        self.setup_sim_args() # stores them in an attribute, whose name and value depends on self.use_dylib_sim
        # Now run the sim to completion (success or fail or user abort),
        # as well as whatever updates we do at the same time in the cad code
        # (progress bar, showing movie in real time [nim but being added circa 051231], ...)
        if self.use_dylib_sim:
            self.sim_loop_using_dylib() #bruce 051231 wrote this anew
        else:
            self.sim_loop_using_standalone_executable() #bruce 051231 made this from last part of old spawn_process code
        return

    def setup_sim_args(self): #bruce 051231 split this out of spawn_process, added dylib case
        """Set up arguments for the simulator, using one of two different interfaces:
        either constructing a command line for the standalone executable simulator,
        or creating and setting up an instance of an extension class defined in the
        sim module (a dynamic library). (But don't start it running.)
           We use the same method to set up both kinds of interface, so that it will
        be easier to keep them in sync as the code evolves.
           WARNING: We also set a few attributes of self which cause side effects later;
        in one case, the attribute looks just like a sim-executable command line option
        (purely for historical reasons).
        """
        # set one of the sim-interface-format flags
        use_dylib = self.use_dylib_sim
        use_command_line = not self.use_dylib_sim
        # (The rest of this method would permit both of these flags to be set together, if desired;
        #  that might be useful if we want to try one interface, and if it fails, try the other.)
        
        movie = self._movie # old-code compat kluge
        self.totalFramesRequested = movie.totalFramesRequested
        self.update_cond = movie.update_cond
        moviefile = movie.filename
        if use_command_line:
            program = self.program
            outfileArg = "-o%s" % moviefile #SIMOPT
            traceFileArg = self.traceFileArg
        infile = self.sim_input_file

        ext = movie.filetype #bruce 050404 added movie.filetype
        mflag = self.mflag
        
        # "formarg" = File format argument -- we need this even when use_dylib,
        # since it's also used as an internal flag via self._formarg
        if ext == ".dpb": formarg = ''
        elif ext == ".xyz": formarg = "-x" #SIMOPT (value also used as internal flag)
        else: assert 0
        self._formarg = formarg # kluge
        # the use_dylib code for formarg is farther below

        self._simopts = self._simobj = self._arguments = None # appropriate subset of these is set below

        use_timestep_arg = False
        if 1: ##@@ bruce 060503: add debug_pref to let user vary simulator timestep
            # (we also read the value on import, in separate code above, to make sure it gets into the debug menu right away)
            use_timestep_arg, timestep = timestep_flag_and_arg(mflag)
            # boolean and float (timestep in seconds)
            if use_timestep_arg:
                env.history.message(orangemsg("Note: using experimental non-default dynamics timestamp of %r femtoseconds" % (timestep * 1e15)))
        if use_command_line:
            # "args" = arguments for the simulator.
            #SIMOPT -- this appears to be the only place the entire standalone simulator command line is created.
            if mflag:
		#argument to enable or disable electrostatics
		electrostaticArg = '--enable-electrostatic='
		if self.cmd_type == 'Adjust' or self.cmd_type == 'Adjust Atoms':
		    electrostaticFlag = self.getElectrostaticPrefValueForAdjust()
		else:
		    electrostaticFlag = self.getElectrostaticPrefValueForMinimize()
		    
##		electrostaticArg.append(str(electrostaticFlag))
		electrostaticArg += str(electrostaticFlag) #bruce 070601 bugfix
		
                # [bruce 05040 infers:] mflag true means minimize; -m tells this to the sim.
                # (mflag has two true flavors, 1 and 2, for the two possible output filetypes for Minimize.)
                # [later, bruce 051231: I think only one of the two true mflag values is presently supported.]
                args = [program, '-m', str(formarg), 
			traceFileArg, outfileArg,
			electrostaticArg,
			infile] #SIMOPT
            else: 
                # THE TIMESTEP ARGUMENT IS MISSING ON PURPOSE.
                # The timestep argument "-s + (movie.timestep)" is not supported for Alpha. #SIMOPT
		
		electrostaticArg = '--enable-electrostatic='		
		electrostaticFlag = self.getElectrostaticPrefValueForDynamics()
##		electrostaticArg.append(str(electrostaticFlag))
		electrostaticArg += str(electrostaticFlag) #bruce 070601 bugfix
		
                args = [program, 
                            '-f' + str(movie.totalFramesRequested), #SIMOPT
                            '-t' + str(movie.temp),  #SIMOPT
                            '-i' + str(movie.stepsper),  #SIMOPT
                            '-r', #SIMOPT
			    electrostaticArg,
                            str(formarg),
                            traceFileArg,
                            outfileArg,
                            infile]
            if use_timestep_arg: #bruce 060503; I'm guessing that two separate arguments are needed for this, and that %f will work
                args.insert(1, '--time-step')
                args.insert(2, '%f' % timestep)
            if debug_sim:
                print  "program = ",program
                print  "Spawnv args are %r" % (args,) # note: we didn't yet remove args equal to "", that's done below
            arguments = QStringList()
            for arg in args:
                # wware 051213  sim's getopt doesn't like empty arg strings
                if arg != "":
                    arguments.append(arg)
            self._arguments = arguments
            del args, arguments
        if use_dylib:
            import sim # whether this will work was checked by a prior method
            if mflag:
                clas = sim.Minimize
            else:
                clas = sim.Dynamics
            simobj = clas(infile)
            if _sim_params_set:
                for attr, value in _sim_param_values.items():
                    setattr(simobj, attr, value)
            # order of set of remaining options should not matter;
            # for correspondence see sim/src files sim.pyx, simhelp.c, and simulator.c
            simopts = simobj # for now, use separate variable names to access params vs methods, in case this changes again [b 060102]
            if formarg == '-x':
                simopts.DumpAsText = 1 # xyz rather than dpb, i guess
            else:
                assert formarg == ''
                simopts.DumpAsText = 0
            if movie.print_energy:
                simopts.PrintPotentialEnergy = 1
            if self.traceFileName:
                simopts.TraceFileName = self.traceFileName # note spelling diff, 'T' vs 't' (I guess I like this difference [b 060102])
                #k not sure if this would be ok to do otherwise, since C code doesn't turn "" into NULL and might get confused
            simopts.OutFileName = moviefile
            if not mflag:
                # The timestep argument "-s + (movie.timestep)" or Dt is not supported for Alpha...
                if use_timestep_arg: #bruce 060503
                    simopts.Dt = timestep
                simopts.NumFrames = movie.totalFramesRequested   # SIMPARAMS
                simopts.Temperature = movie.temp
                simopts.IterPerFrame = movie.stepsper
                simopts.PrintFrameNums = 0
		simopts.EnableElectrostatic = self.getElectrostaticPrefValueForDynamics()
            if mflag:
                self.set_minimize_threshhold_prefs(simopts)
		if self.cmd_type == 'Adjust' or self.cmd_type == 'Adjust Atoms':		    
		    simopts.EnableElectrostatic = self.getElectrostaticPrefValueForAdjust()
		else:
		    simopts.EnableElectrostatic = self.getElectrostaticPrefValueForMinimize()
		    
            #e we might need other options to make it use Python callbacks (nim, since not needed just to launch it differently);
            # probably we'll let the later sim-start code set those itself.
            self._simopts = simopts
            self._simobj = simobj
        # return whatever results are appropriate -- for now, we stored each one in an attribute (above)
        return # from setup_sim_args
    
    def getElectrostaticPrefValueForAdjust(self):
	#ninad20070509
	#int EnableElectrostatic =1 implies electrostatic is enabled 
	#and 0 implies it is disabled. This sim arg is defined in sim.pyx in sim/src 
	if env.prefs[electrostaticsForDnaDuringAdjust_prefs_key]:
	    val = 1
	else:
	    val = 0	
	return val

    def getElectrostaticPrefValueForMinimize(self):
	#ninad20070509
	# int EnableElectrostatic =1 implies electrostatic is enabled 
	#and 0 implies it is disabled. This sim arg is defined in sim.pyx in sim/src 
	if env.prefs[electrostaticsForDnaDuringMinimize_prefs_key]:
	    val = 1
	else:
	    val = 0	
	return val
    

    def getElectrostaticPrefValueForDynamics(self):
	#ninad20070509
	# int EnableElectrostatic =1 implies electrostatic is enabled 
	#and 0 implies it is disabled. This sim arg is defined in sim.pyx in sim/src 
	if env.prefs[electrostaticsForDnaDuringDynamics_prefs_key]:
	    val = 1 
	else:
	    val = 0	
	return val
        
    def set_minimize_threshhold_prefs(self, simopts): #bruce 060628, revised 060705
        def warn(msg):
            env.history.message(orangemsg("Warning: ") + quote_html(msg))
        try:
            if env.debug():
                print "debug: running set_minimize_threshhold_prefs"
            ###obs design scratch:
            # we'll probably use different prefs keys depending on an arg that tells us which command-class to use,
            # Adjust, Minimize, or Adjust Atoms; maybe some function in prefs_constants will return the prefs_key,
            # so all the UI code can call it too. [bruce 060705]
            from prefs_constants import Adjust_endRMS_prefs_key, Adjust_endMax_prefs_key
            from prefs_constants import Adjust_cutoverRMS_prefs_key, Adjust_cutoverMax_prefs_key
            from prefs_constants import Minimize_endRMS_prefs_key, Minimize_endMax_prefs_key
            from prefs_constants import Minimize_cutoverRMS_prefs_key, Minimize_cutoverMax_prefs_key

            # kluge for A8 -- ideally these prefs keys or their prefs values
            # would be set as movie object attrs like all other sim params
            cmd_type = self.cmd_type
            if cmd_type == 'Adjust' or cmd_type == 'Adjust Atoms':
                endRMS_prefs_key = Adjust_endRMS_prefs_key
                endMax_prefs_key = Adjust_endMax_prefs_key
                cutoverRMS_prefs_key = Adjust_cutoverRMS_prefs_key
                cutoverMax_prefs_key = Adjust_cutoverMax_prefs_key
            elif cmd_type == 'Minimize':
                endRMS_prefs_key = Minimize_endRMS_prefs_key
                endMax_prefs_key = Minimize_endMax_prefs_key
                cutoverRMS_prefs_key = Minimize_cutoverRMS_prefs_key
                cutoverMax_prefs_key = Minimize_cutoverMax_prefs_key
            else:
                assert 0, "don't know cmd_type == %r" % (cmd_type,)

            # The following are partly redundant with the formulas,
            # which is intentional, for error checking of the formulas.
            # Only the first (endRMS) values are independent.
            if cmd_type == 'Adjust':
                defaults = (100.0, 500.0, 100.0, 500.0) # also hardcoded in prefs_constants.py
            elif cmd_type == 'Adjust Atoms':
                defaults = (50.0, 250.0, 50.0, 250.0)
            elif cmd_type == 'Minimize':
                defaults = (1.0, 5.0, 50.0, 250.0) # revised 060705, was (1.0, 10.0, 50.0, 300.0); also hardcoded in prefs_constants.py
            
            endRMS = env.prefs[endRMS_prefs_key]
            endMax = env.prefs[endMax_prefs_key]
            cutoverRMS = env.prefs[cutoverRMS_prefs_key]
            cutoverMax = orig_cutoverMax = env.prefs[cutoverMax_prefs_key]
            # -1 means left blank, use default; any 0 or negative value entered explicitly will have the same effect.
            # For an explanation of the logic of these formulas, see email from bruce to materialBuilder-all of 060619,
            # "test UI for minimizer thresholds". These are mainly for testing -- for final release (A8 or maybe A8.1)
            # we are likely to hide all but the first from the UI by default, with the others always being -1.
            #   Revising formulas for A8 release, bruce 060705.

            if cmd_type == 'Adjust Atoms':
                # kluge, because it doesn't have its own prefs values, and has its own defaults, but needs to be adjustable:
                # use fixed values, but if Adjust prefs are made stricter, let those limit these fixed values too
                endRMS = min( endRMS, defaults[0] )
                endMax = min( endMax, defaults[1] )
                cutoverRMS = min( cutoverRMS, defaults[2] )
                cutoverMax = min( cutoverMax, defaults[3] )
                
            if endRMS <= 0:
                endRMS = defaults[0] # e.g. 1.0; note, no other defaults[i] needs to appear in these formulas
            if endMax <= 0:
                endMax = 5.0 * endRMS # revised 060705 (factor was 10, now 5)
            elif endMax < endRMS:
                warn("endMax < endRMS is not allowed, using endMax = endRMS")
                endMax = endRMS # sim C code would use 5.0 * endRMS if we didn't fix this here
            if cutoverRMS <= 0:
                cutoverRMS = max( 50.0, endRMS ) # revised 060705
            if cutoverMax <= 0:
                cutoverMax = 5.0 * cutoverRMS # revised 060705, was 300.0
            if cutoverRMS < endRMS:
                warn("cutoverRMS < endRMS is not allowed, using cutoverRMS,Max = endRMS,Max")
                cutoverRMS = endRMS
                cutoverMax = endMax
            elif cutoverMax < endMax:
                warn("cutoverMax < endMax is not allowed, using cutoverRMS,Max = endRMS,Max")
                cutoverRMS = endRMS
                cutoverMax = endMax
            if cutoverMax < cutoverRMS:
                if orig_cutoverMax <= 0:
                    warn("cutoverMax < cutoverRMS is not allowed, using cutoverMax = 5.0 * cutoverRMS")
                        # revised 060705 (factor was 6, now 5)
                    cutoverMax = 5.0 * cutoverRMS # sim C code would use 5.0 * cutoverRMS if we didn't fix this here
                else:
                    warn("cutoverMax < cutoverRMS is not allowed, using cutoverMax = cutoverRMS")
                    cutoverMax = cutoverRMS # sim C code would use 5.0 * cutoverRMS if we didn't fix this here
            if (endRMS, endMax, cutoverRMS, cutoverMax) != defaults or env.debug():
                msg = "convergence criteria: endRMS = %0.2f, endMax = %0.2f, cutoverRMS = %0.2f, cutoverMax = %0.2f" % \
                      (endRMS, endMax, cutoverRMS, cutoverMax)
                if (endRMS, endMax, cutoverRMS, cutoverMax) == defaults:
                    msg += " (default values -- only printed since ATOM_DEBUG is set)"
                    msg = _graymsg( msg)
                env.history.message( msg)
            simopts.MinimizeThresholdEndRMS = endRMS # for sim.so, but also grabbed from here later by other code in this file
            simopts.MinimizeThresholdEndMax = endMax # ditto
            simopts.MinimizeThresholdCutoverRMS = cutoverRMS
            simopts.MinimizeThresholdCutoverMax = cutoverMax
##            # only some of the following are needed elsewhere; maybe they could be grabbed from simopts but I'm not sure
##            self.endRMS = endRMS
##            self.endMax = endMax
##            self.cutoverRMS = cutoverRMS
##            self.cutoverMax = cutoverMax
        except:
            print_compact_traceback("error in set_minimize_threshhold_prefs (the ones from the last run might be used): ")
            warn("internal error setting convergence criteria; the wrong ones might be used.")
            pass
        return
            
    def sim_loop_using_standalone_executable(self): #bruce 051231 made this from part of spawn_process; compare to sim_loop_using_dylib
        "#doc"
        movie = self._movie
        arguments = self._arguments
        
        #bruce 050404 let simProcess be instvar so external code can abort it [this is still used as of 051231]
        self.simProcess = None
        try:
            self.remove_old_moviefile(movie.filename) # can raise exceptions #bruce 051230 split this out
            self.remove_old_tracefile(self.traceFileName)
            ## Start the simulator in a different process 
            self.simProcess = QProcess()
            simProcess = self.simProcess
            if debug_sim: #bruce 051115 revised this debug code
                # wware 060104  Create a shell script to re-run simulator
		outf = open("args", "w")
                # On the Mac, "-f" prevents running .bashrc
                # On Linux it disables filename wildcards (harmless)
                outf.write("#!/bin/sh -f\n")
                for a in arguments:
                    outf.write(str(a) + " \\\n")
                outf.write("\n")
                outf.close()
                def blabout():
                    print "stdout:", simProcess.readStdout()
                def blaberr():
                    print "stderr:", simProcess.readStderr()
                QObject.connect(simProcess, SIGNAL("readyReadStdout()"), blabout)
                QObject.connect(simProcess, SIGNAL("readyReadStderr()"), blaberr)
            simProcess.setArguments(arguments)
                ###BUG: the above line may have never been ported to Qt4; for me it's saying AttributeError: setArguments.
                # (One way to make it happen is to remove sim.so but leave the simulator executable accessible.)
                # [bruce 070601 comment]
            if self._movie.watch_motion:
                env.history.message(orangemsg("(watch motion in real time is only implemented for pyrex interface to simulator)"))
                # note: we have no plans to change that; instead, the pyrex interface will become the usual one
                # except for background or remote jobs. [bruce 060109]
            if not self._movie.create_movie_file:
                env.history.message(orangemsg("(option to not create movie file is not yet implemented)")) # for non-pyrex sim
                # NFR/bug 1286 not useful for non-pyrex sim, won't be implemented, this msg will be revised then
                # to say "not supported for command-line simulator"
            start = time.time() #bruce 060103 compute duration differently
            simProcess.start()
            # Launch the progress bar, and let it monitor and show progress and wait until
            # simulator is finished or user aborts it.
            self.monitor_progress_by_file_growth(movie) #bruce 060103 made this no longer help us compute duration
            duration = time.time() - start
            movie.duration = duration #bruce 060103 (more detailed comment in other place this occurs)

        except: # We had an exception.
            print_compact_traceback("exception in simulation; continuing: ")
            if simProcess:
                #simProcess.tryTerminate()
                simProcess.kill()
                simProcess = None
            self.errcode = -1 # simulator failure

        # now sim is done (or abort was pressed and it has not yet been killed)
        # and self.errcode is error code or (for a specific hardcoded value)
        # says abort was pressed.
        # what all cases have in common is that user wants us to stop now
        # (so we might or might not already be stopped, but we will be soon)
        # and self.errcode says what's going on.

        # [bruce 050407:]
        # For now:
        # Since we're not always stopped yet, we won't scan the tracefile
        # for error messages here... let the caller do that.
        # Later:
        # Do it continuously as we monitor progress (in fact, that will be
        # *how* we monitor progress, rather than watching the filesize grow).
        
        return

    def remove_old_moviefile(self, moviefile): #bruce 051230 split this out of spawn_process
        "remove the moviefile if it exists, after warning existing Movie objects that we'll do so; can raise exceptions"
        if os.path.exists(moviefile):
            #bruce 050428: do something about this being the moviefile for an existing open movie.
            try:
                ## print "calling apply2movies",moviefile
                self.assy.apply2movies( lambda movie: movie.fyi_reusing_your_moviefile( moviefile) )
                # note that this is only correct if we're sure it won't be called for the new Movie
                # we're making right now! For now, this is true. Later we might need to add an "except for this movie" arg.
            except:
                #e in future they might tell us to lay off this way... for now it's a bug, but we'll ignore it.
                print_compact_traceback("exception in preparing to reuse moviefile for new movie ignored: ")
                pass
            #bruce 050407 moving this into the try, since it can fail if we lack write permission
            # (and it's a good idea to give up then, so we're not fooled by an old file)
            if debug_sim:
                print "deleting moviefile: [",moviefile,"]"
            os.remove (moviefile) # Delete before spawning simulator.
        return        
        #bruce 051231: here is an old comment related to remove_old_moviefile;
        # I don't know whether it's obsolete regarding the bug it warns about:
        # delete old moviefile we're about to write on, and warn anything that might have it open
        # (only implemented for the same movie obj, THIS IS A BUG and might be partly new... ####@@@@)
    
    def remove_old_tracefile(self, tracefile): #bruce 060101
        "remove the tracefile if it exists, after warning anything that might care [nim]; can raise exceptions"
        if os.path.exists(tracefile):
                os.remove(tracefile) # can raise exception, e.g. due to directory permission error
        return
    
    def monitor_progress_by_file_growth(self, movie): #bruce 051231 split this out of sim_loop_using_standalone_executable
        filesize, pbarCaption, pbarMsg = self.old_guess_filesize_and_progbartext( movie)
            # only side effect: history message [bruce 060103 comment]
        # pbarCaption and pbarMsg are not used any longer.  [mark 060105 comment]
        # (but they or similar might be used again soon, eg for cmdname in tooltip -- bruce 060112 comment)
        from StatusBar import show_progressbar_and_stop_button
        self.errcode = show_progressbar_and_stop_button(
                            self.win,
                            filesize,
                            filename = movie.filename,
                            cmdname = self.cmdname, #bruce 060112
                            show_duration = 1 )
            # that 'launch' method is misnamed, since it also waits for completion;
            # its only side effects [as of bruce 060103] are showing/updating/hiding progress dialog, abort button, etc.
        return
    
    def old_guess_filesize_and_progbartext(self, movie):
        "#doc [return a triple of useful values for a progressbar, and emit a related history msg]"
        #bruce 060103 added docstring
        #bruce 050401 now calling this after spawn not before? not sure... note it emits a history msg.
        # BTW this is totally unclean, all this info should be supplied by the subclass
        # or caller that knows what's going on, not guessed by this routine
        # and the filesize tracking is bogus for xyz files, etc etc, should be
        # tracking status msgs in trace file. ###@@@
        formarg = self._formarg # old-code kluge
        mflag = self.mflag
        natoms = len(movie.alist)
        moviefile = movie.filename
        # We cannot determine the exact final size of an XYZ trajectory file.
        # This formula is an estimate.  "filesize" must never be larger than the
        # actual final size of the XYZ file, or the progress bar will never hit 100%,
        # even though the simulator finished writing the file.
        # - Mark 050105
        #bruce 050407: apparently this works backwards from output file file format and minimizeQ (mflag)
        # to figure out how to guess the filesize, and the right captions and text for the progressbar.
        if formarg == "-x": #SIMOPT (used as internal flag, review if we change how this is passed to sim executable!)
            # Single shot minimize.
            if mflag: # Assuming mflag = 2. If mflag = 1, filesize could be wrong.  Shouldn't happen, tho.
                filesize = natoms * 16 # single-frame xyz filesize (estimate)
                pbarCaption = "Adjust" # might be changed below
                    #bruce 050415: this string used to be tested in ProgressBar.py, so it couldn't have "All" or "Selection".
                    # Now it can have them (as long as it starts with Minimize, for now) --
                    # so we change it below (to caption from caller), or use this value if caller didn't provide one.
                pbarMsg = "Adjusting..."
            # Write XYZ trajectory file.
            else:
                filesize = movie.totalFramesRequested * ((natoms * 28) + 25) # multi-frame xyz filesize (estimate)
                pbarCaption = "Save File" # might be changed below
                pbarMsg = "Saving XYZ trajectory file " + os.path.basename(moviefile) + "..."
        else: 
            # Multiframe minimize
            if mflag:
                filesize = (max(100, int(sqrt(natoms))) * natoms * 3) + 4
                pbarCaption = "Adjust" # might be changed below
                pbarMsg = None #bruce 050401 added this
            # Simulate
            else:
                filesize = (movie.totalFramesRequested * natoms * 3) + 4
                pbarCaption = "Simulator" # might be changed below
                pbarMsg = "Creating movie file " + os.path.basename(moviefile) + "..."
                msg = "Simulation started: Total Frames: " + str(movie.totalFramesRequested)\
                        + ", Steps per Frame: " + str(movie.stepsper)\
                        + ", Temperature: " + str(movie.temp)
                env.history.message(self.cmdname + ": " + msg)
        #bruce 050415: let caller specify caption via movie object's _cmdname
        # (might not be set, depending on caller) [needs cleanup].
        # For important details see same-dated comment above.
        try:
            caption_from_movie = movie._cmdname
        except AttributeError:
            caption_from_movie = None
        if caption_from_movie:
            pbarCaption = caption_from_movie
        return filesize, pbarCaption, pbarMsg

#bruce 060103 pared this old comment down to its perhaps-useful parts:
##        handle abort button (in progress bar or maybe elsewhere, maybe a command key)
##        (btw abort or sim-process-crash does not imply failure, since there might be
##         usable partial results, even for minimize with single-frame output);
##        process other user events (or some of them) (maybe);
##        and eventually return when the process is done,
##        whether by abort, crash, or success to end;
##        return True if there are any usable results,
##        and have a results object available in some public attribute.

    def sim_loop_using_dylib(self): #bruce 051231; compare to sim_loop_using_standalone_executable
        # 051231 6:29pm: works, except no trace file is written so results in history come from prior one (if any)
        """#doc
        """
        movie = self._movie
        if platform.atom_debug and movie.duration:
            print "atom_debug: possible bug: movie.duration was already set to", movie.duration
        movie.duration = 0.0 #k hopefully not needed
        # provide a reference frame for later movie-playing (for complete fix of bug 1297) [bruce 060112]
        movie.ref_frame = (self.__frame_number,  A(map(lambda a: a.sim_posn(), movie.alist))) # see similar code in class Movie
            #e this could be slow, and the simobj already knows it, but I don't think getFrame has access to it [bruce 060112]
        simopts = self._simopts
        simobj = self._simobj
        if not self.mflag:
            # wware 060310, bug 1294
            numframes = simopts.NumFrames
            self.win.status_pbar.reset()
            self.win.status_pbar.setRange(0, numframes)
            self.win.status_pbar.setValue(0)
            self.win.status_pbar.show()
        from StatusBar import AbortButtonForOneTask
            #bruce 060106 try to let pyrex sim share some abort button code with non-pyrex sim
        self.abortbutton_controller = abortbutton = AbortButtonForOneTask(self.cmdname)
        abortbutton.start()
        
        try:
            self.remove_old_moviefile(movie.filename) # can raise exceptions #bruce 051230 split this out
        except:
            #bruce 060705 do this here -- try not to prevent the upcoming sim
            print_compact_traceback("problem removing old moviefile, continuing anyway: ")
            env.history.message(orangemsg("problem removing old moviefile, continuing anyway"))

        try:
            self.remove_old_tracefile(self.traceFileName)
        except:
            #bruce 060705 do this here -- try not to prevent the upcoming sim
            print_compact_traceback("problem removing old tracefile, continuing anyway: ")
            env.history.message(orangemsg("problem removing old tracefile, continuing anyway"))

        try:
            if not self._movie.create_movie_file:
                env.history.message(orangemsg("(option to not create movie file is not yet implemented)")) # for pyrex sim
                # NFR/bug 1286; other comments describe how to implement it; it would need a warning
                # (esp if both checkboxes unchecked, since no frame output in that case, tho maybe tracef warnings alone are useful)
            editwarning = "Warning: editing structure while watching motion causes tracebacks; cancelling an abort skips some real time display time"
            if self._movie.watch_motion: #bruce 060705 added this condition
                if not seen_before(editwarning): #bruce 060317 added this condition
                    env.history.message(orangemsg( editwarning ))
            env.call_qApp_processEvents() # so user can see that history message

            ###@@@ SIM CLEANUP desired: [bruce 060102]
            # (items 1 & 2 & 4 have been done)
            # 3. if callback caller in C has an exception from callback, it should not *keep* calling it, but reset it to NULL

            # wware 060309, bug 1343
            self.startTime = start = time.time()
            
            if not abortbutton.aborting():
                # checked here since above processEvents can take time, include other tasks

                # do these before entering the "try" clause
                # note: we need the frame callback even if not self._movie.watch_motion,
                # since it's when we check for user aborts and process all other user events.
                frame_callback = self.sim_frame_callback
                trace_callback = self.tracefile_callback
                
                simgo = simobj.go

                minflag = movie.minimize_flag
                    ###@@@ should we merge this logic with how we choose the simobj class? [bruce 060112]
                
                self.tracefileProcessor = TracefileProcessor(self, minimize = minflag, simopts = simopts)
                    # so self.tracefile_callback does something [bruce 060109]

                from sim import SimulatorInterrupted #bruce 060112 - not sure this will work here vs outside 'def' ###k
                self.sim_frame_callback_prep()
                if _sim_params_set:
                    for attr, expected in _sim_param_values.items():
                        found = getattr(simobj, attr)
                        if found != expected:
                            env.history.message(orangemsg(attr + ' expected=' + str(expected) + ' found=' + str(found)))
                try:
                    simgo( frame_callback = frame_callback, trace_callback = trace_callback )
                        # note: if this calls a callback which raises an exception, that exception gets
                        # propogated out of this call, with correct traceback info (working properly as of sometime on 060111).
                        # If a callback sets simobj.Interrupted (but doesn't raise an exception),
                        # this is turned into an exception like "sim.SimulatorInterrupted: simulator was interrupted".
                        # It also generates a tracefile line "# Warning: minimizer run was interrupted "
                        # (presumably before that exception gets back to here,
                        #  which means a tracefile callback would presumably see it if we set one --
                        #  but as of 060111 there's a bug in which that doesn't happen since all callbacks
                        #  are turned off by Interrupted).
                    if platform.atom_debug:
                        print "atom_debug: pyrex sim: returned normally"
                except SimulatorInterrupted:
                    self.pyrexSimInterrupted = True   # wware 060323 bug 1725
                    # This is the pyrex sim's new usual exit from a user abort, as of sometime 060111.
                    # Before that it was RuntimeError, but that could overlap with exceptions raised by Python callbacks
                    # (in fact, it briefly had a bug where all such exceptions turned into RuntimeErrors).
                    #
                    # I didn't yet fully clean up this code for the new exception. [bruce 060112] ####@@@@
                    if debug_sim_exceptions: #bruce 060111
                        print_compact_traceback("fyi: sim.go aborted with this: ")
                    # following code is wrong unless this was a user abort, but I'm too lazy to test for that from the exception text,
                    # better to wait until it's a new subclass of RuntimeError I can test for [bruce 060111]
                    env.history.statusbar_msg("Aborted")
                    if platform.atom_debug:
                        print "atom_debug: pyrex sim: aborted"
                    if self.PREPARE_TO_CLOSE:
                        # wware 060406 bug 1263 - exiting the program is an acceptable way to leave this loop
                        self.errcode = -1
                    elif not abortbutton.aborting():
                        if not debug_sim_exceptions:
                            #bruce 060712
                            print_compact_traceback("fyi: sim.go aborted with this: ")
                        msg3 = "possible bug in simulator: abort not caused by abortbutton"
                        env.history.message(redmsg(msg3)) #bruce 060712
                        print "error: abort without abortbutton doing it (did a subtask intervene and finish it?)"
                        print " (or this can happen due to sim bug in which callback exceptions turn into RuntimeErrors)"####@@@@
                        from StatusBar import ABORTING #bruce 060111 9:16am PST bugfix of unreported bug
                        abortbutton.status = ABORTING ###@@@ kluge, should clean up, or at least use a method and store an error string too
                        assert abortbutton.aborting()
                    ## bug: this fails to cause an abort to be reported by history. might relate to bug 1303.
                    # or might only occur due to current bugs in the pyrex sim, since I think user abort used to work. [bruce 060111]
                    # Initial attempt to fix that -- need to improve errcode after reviewing them all
                    # (check for errorcode spelling error too? or rename it?) ####@@@@
                    if not self.errcode:
                        print "self.errcode was not set, using -1"
                        self.errcode = -1 # simulator failure [wrong errorcode for user abort, fix this]
                    pass
                pass
            if 1: # even if aborting
                duration = time.time() - start
                #e capture and print its stdout and stderr [not yet possible via pyrex interface]
                movie.duration = duration #bruce 060103
            
        except: # We had an exception.
            print_compact_traceback("exception in simulation; continuing: ")
            ##e terminate it, if it might be in a different thread; destroy object; etc
            # show the exception message in the history window - wware 060314
            type, value, traceback = sys.exc_info()
            msg = redmsg("%s: %s" % (type, value))
            env.history.message(msg)
            self.errcode = _FAILURE_ALREADY_DOCUMENTED
            abortbutton.finish() # whether or not there was an exception and/or it aborted
            return

        if not self.mflag:
            # wware 060310, bug 1294
            self.win.status_pbar.setValue(numframes)
            self.win.status_pbar.reset()
            self.win.status_pbar.hide()
        env.history.progress_msg("") # clear out elapsed time messages
        env.history.statusbar_msg("Done.") # clear out transient statusbar messages

        abortbutton.finish() # whether or not there was an exception and/or it aborted
        return

    __last_3dupdate_time = -1
    __last_progress_update_time = -1
    __frame_number = 0 # starts at 0 so incrementing it labels first frame as 1 (since initial frame is not returned)
        #k ought to verify that in sim code -- seems correct, looking at coords and total number of frames
        # note: we never need to reset __frame_number since this is a single-use object.
        # could this relate to bug 1297? [bruce 060110] (apparently not [bruce 060111])
##    __sim_work_time = 0.05 # initial value -- we'll run sim_frame_callback_worker 20 times per second, with this value
    __last_3dupdate_frame = 0
    __last_pytime = 0.03 # guess (this is a duration)

    def sim_frame_callback_prep(self):
        self.__last_3dupdate_time = self.__last_progress_update_time = time.time()

    def sim_frame_callback_update_check(self, simtime, pytime, nframes):
        "[#doc is in SimSetup.py and in caller]"
        #bruce 060705 revised this, so self.update_cond of None is not an error, so it can be the usual way to say "never update"
        res = True # whether to update this time
        use_default_cond = False
        if self.update_cond == '__default__':
            use_default_cond = True
        elif self.update_cond:
            try:
                res = self.update_cond(simtime, pytime, nframes) # res should be a boolean value
            except:
                self.update_cond = '__default__' # was None
                print_compact_traceback("exception in self.update_cond ignored, reverting to default cond: ")
                use_default_cond = True
        else:
            res = False # was: use_default_cond = True
        if use_default_cond:
            try:
                res = (simtime >= max(0.05, min(pytime * 4, 2.0)))
            except:
                print_compact_traceback("exception in default cond, just always updating: ")
                res = True
##        if res and platform.atom_debug: # DO NOT COMMIT THIS, even with 'if res' -- might print too often and slow it down
##            print "debug: %d sim_frame_callback_update_check returns %r, args" % (self.__frame_number,res), \
##                  simtime, pytime, nframes #bruce 060712
        return res
        
    def sim_frame_callback(self, last_frame):
        "Per-frame callback function for simulator object."
        from sim import SimulatorInterrupted
        if last_frame and env.debug():
            print "debug: last_frame is true" #bruce 060712
        # Note: this was called 3550 times for minimizing a small C3 sp3 hydrocarbon... better check the elapsed time quickly.
        #e Maybe we should make this into a lambda, or even code it in C, to optimize it.
        if self.PREPARE_TO_CLOSE:
            # wware 060406 bug 1263 - if exiting the program, interrupt the simulator
            from sim import SimulatorInterrupted
            raise SimulatorInterrupted
        self.__frame_number += 1
        if debug_all_frames:
            from sim import getFrame
            if debug_sim_exceptions:
                # intentionally buggy code
                print "frame %d" % self.__frame_number, self._simobj.getFrame() # this is a bug, that attr should not exist
            else:
                # correct code
                print "frame %d" % self.__frame_number, getFrame()[debug_all_frames_atom_index]
            pass
        try:
            # Decide whether to update the 3D view and/or the progress indicators.
            # Original code: let sim use up most of the real time used, measuring redraw timing in order to let that happen.
            # see below for more info.
            #bruce 060530 generalizing this to ask self.update_cond how to decide.
            now = time.time() # real time
            simtime = now - self.__last_3dupdate_time # time the sim has been churning away since the last update was completed
            pytime = self.__last_pytime
            nframes = self.__frame_number - self.__last_3dupdate_frame
            update_3dview = self.sim_frame_callback_update_check( simtime, pytime, nframes ) # call this even if later code overrides it
            # always show the last frame - wware 060314
            if last_frame or debug_all_frames:
                update_3dview = True
            
            # now we know whether we want to update the 3d view (and save new values for the __last variables used above).
            if update_3dview:
                if debug_pyrex_prints:
                    print "sim hit frame %d in" % self.__frame_number, simtime
                        #e maybe let frame number be an arg from C to the callback in the future?
                self.__last_3dupdate_frame = self.__frame_number
                self.__last_3dupdate_time = now_start = now
                    # this gets set again below, and again [060712] after all time spent in this function when update_3dview is true;
                    # this set is probably not needed, but it may help with debugging or exceptions sometimes;
                    # the later intermediate one is the same, except it's more likely that it may help with those things.
                    # [bruce 060712 revised this comment & related code]
                try:
                    self.sim_frame_callback_worker( self.__frame_number) # might call self.abort_sim_run() or set self.need_process_events
                except:
                    print_compact_traceback("exception in sim_frame_callback_worker, aborting run: ")
                    self.abort_sim_run("exception in sim_frame_callback_worker(%d)" % self.__frame_number ) # sets flag inside sim object
                self.__last_3dupdate_time = time.time() # this will be set yet again (see comment above)
                # [following comment might be #obs, but I don't understand the claim of an effect on abortability -- bruce 060712]
                # use this difference to adjust 0.05 above, for the upcoming period of sim work;
                # note, in current code this also affects abortability

                # pytime code moved from here to end of method, bruce 060712, to fix bad logic bug introduced 060601,
                # which caused A8 watch realtime "as fast as possible" to be far slower than in A7, due to rendering time
                # being counted as simtime (which was because rendering was moved out of sim_frame_callback_worker on 060601)

                # update 'now' for use in progress_update decision
                now = self.__last_3dupdate_time
                pass
            
            if now >= self.__last_progress_update_time + 1.0 or update_3dview and now >= self.__last_progress_update_time + 0.2:
                # update progressbar [wware 060310, bug 1343]
                # [optim by bruce 060530 -- at most once per second when not updating 3d view, or 5x/sec when updating it often]
                self.need_process_events = True
                self.__last_progress_update_time = now
                from platform import hhmmss_str
                msg = None
                # wware 060309, bug 1343, 060628, bug 1898
                tp = self.tracefileProcessor
                if tp:
                    pt = tp.progress_text()
                    if pt:
                        msg = self.cmdname + ": " + pt
                if msg is not None:
                    env.history.statusbar_msg(msg)
                if self.mflag:
                    # Minimization, give "Elapsed Time" message
                    msg = "Elapsed time: " + hhmmss_str(int(time.time() - self.startTime))
                else:
                    # Dynamics, give simulation frame number, total frames, and time, wware 060419
                    msg = (("Frame %d/%d, T=" % (self.__frame_number, self.totalFramesRequested)) +
                           hhmmss_str(int(time.time() - self.startTime)))
                env.history.progress_msg(msg)
                if not self.mflag:
                    # wware 060310, bug 1294
                    self.win.status_pbar.setValue(self.__frame_number)
                pass

            # do the Qt redrawing for either the GLPane or the status bar (or anything else that might need it),
            # only if something done above set a flag requesting it
            self.sim_frame_callback_updates() # checks/resets self.need_process_events, might call call_qApp_processEvents
                #bruce 060601 bug 1970

            if update_3dview:
                #bruce 060712 fix logic bug introduced on 060601 [for Mac/Linux A8, though the bug surely affects Windows A8 too] --
                # measure pytime only now, so it includes GLPane redraw time as it needs to.
                # (This also means it includes sbar updates and redraw, but only when update_3dview occurred;
                #  that makes sense, since what it controls is the frequency of the redraws of all kinds that happen then,
                #  but not the frequency of the progress_update sbar redraws that sometimes happen not then (at most one per second).)
                self.__last_3dupdate_time = time.time() # this is the last time we set this, in this method run
                pytime = self.__last_3dupdate_time - now_start
                self.__last_pytime = pytime
                if debug_pyrex_prints:
                    print "python stuff when update_3dview took", pytime
                    # old results of that, before we did nearly so much sbar updating:
                    # python stuff took 0.00386619567871 -- for when no real work done, just overhead; small real egs more like 0.03
                if debug_timing_loop_on_sbar:
                    # debug: show timing loop properties on status bar
                    msg = "sim took %0.3f, hit frame %03d, py took %0.3f" % \
                          (simtime, self.__frame_number, pytime)
                    env.history.statusbar_msg(msg)
                pass
            pass

        except SimulatorInterrupted, e:
            # With the precautions on the sim side, in sim.pyx and simhelp.c, the only time we'll
            # ever get a SimulatorInterrupted exception is as the result of an actual interruption
            # of the simulator, not as a result of any exception thrown by a Python callback or by
            # any anomalous occurrence in the simulator C code. We don't want a traceback printed
            # for a simulator interruption so in this event, just ignore the exception.
            # wware, bug 2022, 060714
            pass
        except:
            #bruce 060530 -- ideally we'd propogate the exception up to our caller the sim,
            # and it would propogate it back to the python calling code in this object,
            # so there would be no need to print it here. But that seems to be broken now,
            # whether in the sim or in the calling Python I don't know, so I'll print it here too.
            # But then I'll reraise it for when that gets fixed, and since even now it does succeed
            # in aborting the sim.
            print_compact_traceback("exception in sim_frame_callback (will be propogated to sim): ")
            raise
        return # from sim_frame_callback

    aborting = False #bruce 060601
    need_process_events = False #bruce 060601
    
    def sim_frame_callback_worker(self, frame_number): #bruce 060102
        """Do whatever should be done on frame_callbacks that don't return immediately
           (due to not enough time passing), EXCEPT for Qt-related progress updates other than gl_update --
           caller must do those separately in sim_frame_callback_updates, if this method sets self.need_process_events.
           Might raise exceptions -- caller should protect itself from them until the sim does.
           + stuff new frame data into atom positions
             +? fix singlet positions, if not too slow
           + gl_update
        """
        if not self.aborting: #bruce 060601 replaced 'if 1'
            if self.abortbutton_controller.aborting():
                # extra space to distinguish which line got it -- this one is probably rarer, mainly gets it if nested task aborted(??)
                self.abort_sim_run("got real  abort at frame %d" % frame_number) # this sets self.aborting flag
            # mflag=1 -> minimize, user preference determines whether we watch it in real time
            # mflag=0 -> dynamics, watch_motion (from movie setup dialog) determines real time
##            elif ((not self.mflag and self._movie.watch_motion) or
##                  (self.mflag and env.prefs[Adjust_watchRealtimeMinimization_prefs_key])):
            elif self._movie.watch_motion:
                from sim import getFrame
                frame = getFrame()
                # stick the atom posns in, and adjust the singlet posns
                newPositions = frame
                movie = self._movie
                #bruce 060102 note: following code is approximately duplicated somewhere else in this file.
                try:
                    movie.moveAtoms(newPositions)
                except ValueError: #bruce 060108
                    # wrong number of atoms in newPositions (only catches a subset of possible model-editing-induced errors)
                    self.abort_sim_run("can't apply frame %d, model has changed" % frame_number)
                else:
                    if 1: #bruce 060108 part of fixing bug 1273
                        movie.realtime_played_framenumber = frame_number
                        movie.currentFrame = frame_number
                    self.part.changed() #[bruce 060108 comment: moveAtoms should do this ###@@@]
                    self.part.gl_update()
                # end of approx dup code
                self.need_process_events = True #bruce 060601
        return

    def sim_frame_callback_updates(self): #bruce 060601 split out of sim_frame_callback_worker so it can be called separately
        """Do Qt-related updates which are needed after something has updated progress bar displays or done gl_update
        or printed history messages, if anything has set self.need_process_events to indicate it needs this
        (and reset that flag):
        - tell Qt to process events
        - see if user aborted, if so, set flag in simulator object so it will abort too 
          (but for now, separate code will also terminate the sim run in the usual way, 
           reading redundantly from xyz file)
        """
        if self.need_process_events:
            # tell Qt to process events (for progress bar, its abort button, user moving the dialog or window, changing display mode,
            #  and for gl_update)
            self.need_process_events = False
            env.call_qApp_processEvents()
            self.need_process_events = False # might not be needed; precaution in case of recursion
            #e see if user aborted
            if self.abortbutton_controller.aborting():
                self.abort_sim_run("frame %d" % self.__frame_number) # this also sets self.aborting [bruce 06061 revised text]
        return

    def tracefile_callback(self, line): #bruce 060109, revised 060112; needs to be fast; should optim by passing step method to .go
        tp = self.tracefileProcessor
        if tp:
            tp.step(line)

    def abort_sim_run(self, why = "(reason not specified by internal code)" ): #bruce 060102
        "#doc"
        wasaborting = self.aborting
        self.aborting = True #bruce 060601
        self.need_process_events = True #bruce 060601 precaution; might conceivably improve bugs in which abort confirm dialog is not taken down
        self._simopts.Interrupted = True
        if not self.errcode:
            self.errcode = -1
            ####@@@@ temporary kluge in case of bugs in RuntimeError from that or its handler;
            # also needed until we clean up our code to use the new sim.SimulatorInterrupt instead of RuntimeError [bruce 060111]
        if not wasaborting: #bruce 060601 precaution
            env.history.message( redmsg( "aborting sim run: %s" % why ))
        return

    tracefileProcessor = None
    
    def print_sim_warnings(self): #bruce 050407; revised 060109, used whether or not we're not printing warnings continuously
        """Print warnings and errors from tracefile (if this was not already done);
        then print summary/finishing info related to tracefile.
        Note: this might change self.said_we_are_done to False or True, or leave it alone.
        """
        # Note: this method is sometimes called after errors, and that is usually a bug but might sometimes be good;
        # caller needs cleanup about this.
        # Meanwhile, possible bug -- not sure revisions of 060109 (or prior state) is fully safe when called after errors.
        if not self.tracefileProcessor:
            # we weren't printing tracefile warnings continuously -- print them now
            try:
                simopts = self._simopts
            except:
                # I don't know if this can happen, no time to find out, not safe for A8 to assume it can't [bruce 060705]
                print "no _simopts"
                simopts = None
            self.tracefileProcessor = TracefileProcessor(self, simopts = simopts)
                # this might change self.said_we_are_done and/or use self.traceFileName, now and/or later
            try:
                tfile = self.traceFileName
            except AttributeError:
                return # sim never ran (not always an error, I suspect)
            if not tfile:
                return # no trace file was generated using a name we provide
                       # (maybe the sim wrote one using a name it made up... nevermind that here)
            try:
                ff = open(tfile, "rU") # "U" probably not needed, but harmless
            except:
                #bruce 051230 fix probably-unreported bug when sim program is missing
                # (tho ideally we'd never get into this method in that case)
                print_compact_traceback("exception opening trace file %r: " % tfile)
                env.history.message( redmsg( "Error: simulator trace file not found at [%s]." % tfile ))
                self.tracefileProcessor.mentioned_sim_trace_file = True #k not sure if this is needed or has any effect
                return
            lines = ff.readlines()
            ## remove this in case those non-comment lines matter for the summary (unlikely, so add it back if too slow) [bruce 060112]
##            lines = filter( lambda line: line.startswith("#"), lines )
##                # not just an optimization, since TracefileProcessor tracks non-# lines for status info
            ff.close()
            for line in lines:
                self.tracefileProcessor.step(line)
        # print summary/done
        self.tracefileProcessor.finish()
        return

    pass # end of class SimRunner

# ==

print_sim_comments_to_history = False

'''
Date: 12 Jan 2006 20:57:05 -0000
From: ericm
To: bruce
Subject: Minimize trace file format

Here\'s the code that writes the trace file during minimize:

    write_traceline("%4d %20f %20f %s %s\n", frameNumber, rms, max_force, callLocation, message);

You can count on the first three not changing.

Note that with some debugging flags on you get extra lines of this
same form that have other info in the same places.  I think you can
just use the rms value for progress and it will do strange things if
you have that debugging flag on.  If you want to ignore those lines,
you can only use lines that have callLocation=="gradient", and that
should work well.

-eric
'''

class TracefileProcessor: #bruce 060109 split this out of SimRunner to support continuous tracefile line processing
    findRmsForce = re.compile("rms ([0-9.]+) pN")
    findHighForce = re.compile("high ([0-9.]+) pN")
    "Helper object to filter tracefile lines and print history messages as they come and at the end"
    def __init__(self, owner, minimize = False, simopts = None):
        "store owner so we can later set owner.said_we_are_done = True; also start"
        self.owner = owner
        self.simopts = simopts #bruce 060705 for A8
        self.minimize = minimize # whether to check for line syntax specific to Minimize
        self.__last_plain_line_words = None # or words returned from string.split(None, 4)
        self.start() # too easy for client code to forget to do this
    def start(self):
        "prepare to loop over lines"
        self.seen = {} # whether we saw each known error or warning tracefile-keyword
        self.donecount = 0 # how many Done keywords we saw in there
        self.mentioned_sim_trace_file = False # public, can be set by client code
    def step(self, line): #k should this also be called by __call__ ? no, that would slow down its use as a callback.
        """do whatever should be done immediately with this line, and save things to do later;
        this bound method might be used directly as a trace_callback [but isn't, for clarity, as of 060109]
        """
        if not line.startswith("#"):
            # this happens a lot, needs to be as fast as possible
            if self.minimize:
                # check for "gradient" seems required based on current syntax (and will usually be true)
                # (as documented in email from ericm today) (if too slow, deferring until line used is tolerable,
                #  but might result in some missed lines, at least if sim internal debug flags are used) [bruce 060112]
                words = line.split(None, 4) # split in at most 4 places
                if len(words) >= 4 and words[3] == 'gradient': # 4th word -- see also self.progress_text()
                    self.__last_plain_line_words = words
                elif platform.atom_debug:
                    print "atom_debug: weird tracef line:", line ####@@@@ remove this? it happens normally at the end of many runs
            return 
        if print_sim_comments_to_history: #e add checkbox or debug-pref for this??
            env.history.message("tracefile: " + line)
        # don't discard initial "#" or "# "
        for start in ["# Warning:", "# Error:", "# Done:"]:
            if line.startswith(start):
                if start != "# Done:":
                    self.owner.said_we_are_done = False # not needed if lines come in their usual order
                    if not self.seen:
                        env.history.message( "Messages from simulator trace file:") #e am I right to not say this just for Done:?
                        self.mentioned_sim_trace_file = True
                    if start == "# Warning:":
                        cline = orangemsg(line)
                    else:
                        cline = redmsg(line)
                    env.history.message( cline) # leave in the '#' I think
                    self.seen[start] = True
                else:
                    # "Done:" line - emitted iff it has a message on it; doesn't trigger mention of tracefile name
                    # if we see high forces, color the Done message orange, bug 1238, wware 060323
                    if 1:
                        #bruce 060705
                        simopts = self.simopts
                        try:
                            endRMS = simopts.MinimizeThresholdEndRMS
                        except AttributeError:
                            print "simopts %r had no MinimizeThresholdEndRMS"
                            endRMS = 1.0 # was 2.0
                        try:
                            endMax = simopts.MinimizeThresholdEndMax
                        except AttributeError:
                            print "simopts %r had no MinimizeThresholdEndMax"
                            endMax = 5.0 # was 2.0
                        epsilon = 0.000001 # guess; goal is to avoid orangemsg due to roundoff when printing/reading values
                        pass
                    foundRms = self.findRmsForce.search(line)
                    if foundRms: foundRms = float(foundRms.group(1))
                    foundHigh = self.findHighForce.search(line)
                    if foundHigh: foundHigh = float(foundHigh.group(1))
                    highForces = ((foundRms != None and foundRms > endRMS + epsilon) or
                                  (foundHigh != None and foundHigh > endMax + epsilon))
                    self.donecount += 1
                    text = line[len(start):].strip()
                    if text:
                        if "# Error:" in self.seen:
                            line = redmsg(line)
                        elif highForces or ("# Warning:" in self.seen):
                            line = orangemsg(line)
                        env.history.message( line) #k is this the right way to choose the color?
                        ## I don't like how it looks to leave out the main Done in this case [bruce 050415]:
                        ## self.owner.said_we_are_done = True # so we don't have to say it again [bruce 050415]
        return
    def progress_text(self): ####@@@@ call this instead of printing that time stuff
        "Return some brief text suitable for periodically displaying on statusbar to show progress"
        words = self.__last_plain_line_words
        if not words:
            return ""
        if len(words) == 4: #k needed?
            words = list(words) + [""]
        try:
            frameNumber, rms, max_force, callLocation, message = words
            assert callLocation == 'gradient'
        except:
            return "?"
        return "frame %s: rms force = %s; high force = %s" % (frameNumber, rms, max_force)
            # 'high' instead of 'max' is to match Done line syntax (by experiment as of 060112)
    def finish(self):
        if not self.donecount:
            self.owner.said_we_are_done = False # not needed unless other code has bugs
            # Note [bruce 050415]: this happens when user presses Abort,
            # since we don't abort the sim process gently enough. This should be fixed.
            #bruce 051230 changed following from redmsg to orangemsg
            env.history.message( orangemsg( "Warning: simulator trace file should normally end with \"# Done:\", but it doesn't."))
            self.mentioned_sim_trace_file = True
        if self.mentioned_sim_trace_file:
            # sim trace file was mentioned; user might wonder where it is...
            # but [bruce 050415] only say this if the location has changed since last time we said it,
            # and only include the general advice once per session.
            global last_sim_tracefile
            tfile = self.owner.traceFileName #bruce 060110 try to fix bug 1299
            if last_sim_tracefile != tfile:
                preach = (last_sim_tracefile is None)
                last_sim_tracefile = tfile
                msg = "(The simulator trace file was [%s]." % tfile
                if preach:
                    msg += " It might be overwritten the next time you run a similar command."
                msg += ")"
                env.history.message( msg)
        return
        
    pass # end of class TracefileProcessor

# this global needs to preserve its value when we reload!
try:
    last_sim_tracefile
except:
    last_sim_tracefile = None
else:
    pass

# ==

# writemovie used to be here, but is now split into methods of class SimRunner above [bruce 050401]

# ... here's a compat stub... i guess ###doit

#obs comment:
# Run the simulator and tell it to create a dpb or xyz trajectory file.
# [bruce 050324 moved this here from fileIO.py. It should be renamed to run_simulator,
#  since it does not always try to write a movie, but always tries to run the simulator.
#  In fact (and in spite of not always making a movie file),
#  maybe it should be a method of the Movie object,
#  which is used before the movie file is made to hold the params for making it.
#  (I'm not sure how much it's used when we'll make an .xyz file for Minimize.)
#  If it's not made a Movie method, then at least it should be revised
#  to accept the movie to use as an argument; and, perhaps, mainly called by a Movie method.
#  For now, I renamed assy.m -> assy.current_movie, and never grab it here at all
#  but let it be passed in instead.] ###@@@
def writemovie(part, movie, mflag = 0, simaspect = None, print_sim_warnings = False, cmdname = "Simulator", cmd_type = 'Minimize'):
        #bruce 060106 added cmdname
    """Write an input file for the simulator, then run the simulator,
    in order to create a moviefile (.dpb file), or an .xyz file containing all
    frames(??), or an .xyz file containing what would have
    been the moviefile's final frame.  The name of the file it creates is found in
    movie.filename (it's made up here for mflag != 0, but must be inserted by caller
    for mflag == 0 ###k). The movie is created for the atoms in the movie's alist,
    or the movie will make a new alist from part if it doesn't have one yet
    (for Minimize Selection, it will probably already have one when this is called ###@@@).
    (This should be thought of as a Movie method even though it isn't one yet.)
    DPB = Differential Position Bytes (binary file)
    XYZ = XYZ trajectory file (text file)
    mflag: [note: mflag is called mtype in some of our callers!]
        0 = default, runs a full simulation using parameters stored in the movie object.
        1 = run the simulator with -m and -x flags, creating a single-frame XYZ file.
        2 = run the simulator with -m flags, creating a multi-frame DPB moviefile.
    Return value: false on success, true (actually an error code but no caller uses that)
    on failure (error message already emitted).
      Either way (success or not), also copy errors and warnings from tracefile to history,
    if print_sim_warnings = True. Someday this should happen in real time;
    for now [as of 050407] it happens once when we're done.
    """
    #bruce 050325 Q: why are mflags 0 and 2 different, and how? this needs cleanup.

    simrun = SimRunner( part, mflag, simaspect = simaspect, cmdname = cmdname, cmd_type = cmd_type)
        #e in future mflag should choose subclass (or caller should)
    movie._simrun = simrun #bruce 050415 kluge... see also the related movie._cmdname kluge
    movie.currentFrame = 0 #bruce 060108 moved this here, was in some caller's success cases
    movie.realtime_played_framenumber = 0 #bruce 060108
    movie.minimize_flag = not not mflag # whether we're doing some form of Minimize [bruce 060112]
    # wware 060420 - disable atom/bond highlighting while simulating, improves simulator performance
    part.assy.o.is_animating = True
    simrun.run_using_old_movie_obj_to_hold_sim_params(movie)
    part.assy.o.is_animating = False
    if 1:
        #bruce 060108 part of fixing bug 1273
        fn = movie.realtime_played_framenumber
        if fn:
            if not movie.minimize_flag: #bruce 060112
                #e a more accurate condition would be something like "if we made a movie file and bragged about it"
                env.history.message(greenmsg("(current atom positions correspond to movie frame %d)" % fn))
        assert movie.currentFrame == fn
    if print_sim_warnings and simrun.errcode != _FAILURE_ALREADY_DOCUMENTED:
        # If there was a clear error then don't print a lot of lower-priority less urgent stuff
        # after the bright red error message.
        try:
            simrun.print_sim_warnings()
                #bruce 051230 comment: this runs even if sim executable was not found; why?? ####@@@@
                # guess: need to check error code from run_using_old_movie_obj_to_hold_sim_params;
                # that's done by checking simrun.errcode, but I wonder if for some values (like user aborted sim)
                # we should still print the warnings? So I'll refrain from not trying to print them on errcode, for now.
                # Instead I made it (print_sim_warnings) handle the error of not finding the trace file,
                # instead of raising an exception then.
        except:
            print_compact_traceback("bug in print_sim_warnings, ignored: ")
    return simrun.errcode

# ==

#bruce 050324 moved readxyz here from fileIO, added filename and alist args,
# removed assy arg (though soon we'll need it or a history arg),
# standardized indentation, revised docstring [again, 050404] and some comments.
#bruce 050404 reworded messages & revised their printed info,
# and changed error return to return the error message string
# (so caller can print it to history if desired).
# The original in fileIO was by Huaicai shortly after 050120.
#bruce 050406 further revisions (as commented).
def readxyz(filename, alist):
    """Read a single-frame XYZ file created by the simulator, typically for
    minimizing a part. Check file format, check element types against those
    in alist (the number of atoms and order of their elements must agree).
    [As of 050406, also permit H in the file to match a singlet in alist.]
       This test will probably fail unless the xyz file was created
    using the same atoms (in the same order) as in alist. If the atom set
    is the same (and the same session, or the same chunk in an mmp file,
    is involved), then the fact that we sort atoms by key when creating
    alists for writing sim-input mmp files might make this order likely to match.
       On error, print a message to stdout and also return it to the caller.
       On success, return a list of atom new positions
    in the same order as in the xyz file (hopefully the same order as in alist).
    """
    xyzFile = filename ## was assy.m.filename
    lines = open(xyzFile, "rU").readlines()
    
    if len(lines) < 3: ##Invalid file format
        msg = "readxyz: %s: File format error (fewer than 3 lines)." % xyzFile
        print msg
        return msg
    
    atomList = alist ## was assy.alist, with assy passed as an arg
        # bruce comment 050324: this list or its atoms are not modified in this function
    ## stores the new position for each atom in atomList
    newAtomsPos = [] 
    
    try:     
        numAtoms = int(lines[0]) # bruce comment 050324: numAtoms is not used
        rms = float(lines[1][4:]) # bruce comment 050324: rms is not used
    except ValueError:
        msg = "readxyz: %s: File format error in Line 1 and/or Line 2" % xyzFile
        print msg
        return msg
    
    atomIndex = 0
    for line in lines[2:]:
        words = line.split()
        if len(words) != 4:
            msg = "readxyz: %s: Line %d format error." % (xyzFile, lines.index(line) + 1)
                #bruce 050404 fixed order of printfields, added 1 to index
            print msg
            return msg
        try:        
            if words[0] != atomList[atomIndex].element.symbol:
                if words[0] == 'H' and atomList[atomIndex].element == Singlet:
                    #bruce 050406 permit this, to help fix bug 254 by writing H to sim for Singlets in memory
                    pass
                else:
                    msg = "readxyz: %s: atom %d (%s) has wrong element type." % (xyzFile, atomIndex+1, atomList[atomIndex])
                        #bruce 050404: atomIndex is not very useful, so I added 1
                        # (to make it agree with likely number in mmp file)
                        # and the atom name from the model.
                        ###@@@ need to fix this for H vs singlet (then do we revise posn here or in caller?? probably in caller)
                    print msg
                    return msg
            newAtomsPos += [map(float, words[1:])]
        except ValueError:
            msg = "readxyz: %s: atom %d (%s) position number format error." % (xyzFile, atomIndex+1, atomList[atomIndex])
                #bruce 050404: same revisions as above.
            print msg
            return msg
        except:
            #bruce 060108 added this case (untested) since it looks necessary to catch atomList[atomIndex] attributeerrors 
            msg = "readxyz: %s: error (perhaps fewer atoms in model than in xyz file)" % (xyzFile,)
            print msg
            return msg
        
        atomIndex += 1
    
    if (len(newAtomsPos) != len(atomList)): #bruce 050225 added some parameters to this error message
        msg = "readxyz: The number of atoms from %s (%d) is not matching with the current model (%d)." % \
              (xyzFile, len(newAtomsPos), len(atomList))
        print msg
        return msg #bruce 050404 added error return after the above print statement; not sure if its lack was new or old bug
    
    return newAtomsPos

# == user-visible commands for running the simulator, for simulate or minimize

class CommandRun: # bruce 050324; mainly a stub for future use when we have a CLI
    """Class for single runs of commands.
    Commands themselves (as opposed to single runs of them)
    don't yet have objects to represent them in a first-class way,
    but can be coded and invoked as subclasses of CommandRun.
    """
    def __init__(self, win, *args, **kws):
        self.win = win
        self.args = args # often not needed; might affect type of command (e.g. for Minimize)
        self.kws = kws # ditto; as of 060705, this contains 'type' for Minimize_CommandRun, for basic command name in the UI
        self.assy = win.assy
        self.part = win.assy.part
            # current Part (when the command is invoked), on which most commands will operate
        self.glpane = win.assy.o #e or let it be accessed via part??
        return
    # end of class CommandRun

class simSetup_CommandRun(CommandRun):
    """Class for single runs of the simulator setup command; create it
    when the command is invoked, to prep to run the command once;
    then call self.run() to actually run it.
    """
    cmdname = 'Simulator' #bruce 060106 temporary hack, should be set by subclass ###@@@
    def run(self):
        #bruce 050324 made this method from the body of MWsemantics.simSetup
        # and cleaned it up a bit in terms of how it finds the movie to use.
        if not self.part.molecules: # Nothing in the part to simulate.
            msg = redmsg("Nothing to simulate.")
            env.history.message(self.cmdname + ": " + msg)
	    self.win.simSetupAction.setChecked(0) # toggle the Simulator icon ninad061113
            return
        
        env.history.message(self.cmdname + ": " + "Enter simulation parameters and select <b>Run Simulation.</b>")

        ###@@@ we could permit this in movie player mode if we'd now tell that mode to stop any movie it's now playing
        # iff it's the current mode.

        previous_movie = self.assy.current_movie
            # might be None; will be used only to restore self.assy.current_movie if we don't make a valid new one
        self.movie = None
        r = self.makeSimMovie( ) # will store self.movie as the one it made, or leave it as None if cancelled
        movie = self.movie
        self.assy.current_movie = movie or previous_movie
            # (this restores assy.current_movie if there was an error in making new movie, though perhaps nothing changed it anyway)

        if not r: # Movie file saved successfully; movie is a newly made Movie object just for the new file
            assert movie
            # if duration took at least 10 seconds, print msg.
##            self.progressbar = self.win.progressbar ###k needed???
##            duration = self.progressbar.duration [bruce 060103 zapped this kluge]
            try:
                duration = movie.duration #bruce 060103
            except:
                # this might happen if earlier exceptions prevented us storing one, so nevermind it for now
                duration = 0.0
            if duration >= 10.0: 
                spf = "%.2f" % (duration / movie.totalFramesRequested)
                    ###e bug in this if too few frames were written; should read and use totalFramesActual
                from platform import hhmmss_str
                estr = hhmmss_str(duration)
                msg = "Total time to create movie file: " + estr + ", Seconds/frame = " + spf
                env.history.message(self.cmdname + ": " + msg) 
            msg = "Movie written to [" + movie.filename + "]." \
		"<br>To play the movie, select <b>Simulation > Play Movie</b>"
            env.history.message(self.cmdname + ": " + msg)
	    self.win.simSetupAction.setChecked(0)
            self.win.simMoviePlayerAction.setEnabled(1) # Enable "Movie Player"
            self.win.simPlotToolAction.setEnabled(1) # Enable "Plot Tool"
            #bruce 050324 question: why are these enabled here and not in the subr or even if it's cancelled? bug? ####@@@@
        else:
            assert not movie
            # Don't allow uninformative messages to obscure informative ones - wware 060314
            if r == _FAILURE_ALREADY_DOCUMENTED:
                env.history.message(self.cmdname + ": " + "Cancelled.")
                # (happens for any error; more specific message (if any) printed earlier)
        return

    def makeSimMovie(self): ####@@@@ some of this should be a Movie method since it uses attrs of Movie...
        #bruce 050324 made this from the Part method makeSimMovie.
        # It's called only from self.run() above; not clear it should be a separate method,
        # or if it is, that it's split from the caller at the right boundary.
        suffix = self.part.movie_suffix()
        if suffix is None: #bruce 050316 temporary kluge
            msg = redmsg( "Simulator is not yet implemented for clipboard items.")
            env.history.message(self.cmdname + ": " + msg)
            return -1
        ###@@@ else use suffix below!
        
        self.simcntl = SimSetup(self.part, suffix = suffix)
            # this now has its own sticky params, doesn't need previous_movie [bruce 060601, fixing bug 1840]
            # Open SimSetup dialog [and run it until user dismisses it]
        movie = self.simcntl.movie # always a Movie object, even if user cancelled the dialog
        
        if movie.cancelled:
            # user hit Cancel button in SimSetup Dialog. No history msg went out; caller will do that.
            movie.destroy()
            return -1
        r = writemovie(self.part, movie, print_sim_warnings = True, cmdname = self.cmdname) # not passing mtype means "run dynamic sim (not minimize), make movie"
            ###@@@ bruce 050324 comment: maybe should do following in that function too
        if not r: 
            # Movie file created. Initialize. ###@@@ bruce 050325 comment: following mods private attrs, needs cleanup.
            movie.IsValid = True # Movie is valid.###@@@ bruce 050325 Q: what exactly does this (or should this) mean?
                ###@@@ bruce 050404: need to make sure this is a new obj-- if not always and this is not init False, will cause bugs
            self.movie = movie # bruce 050324 added this
            # it's up to caller to store self.movie in self.assy.current_movie if it wants to.
        return r

    pass # end of class simSetup_CommandRun



def capitalize_first_word(words): #bruce 060705 ##e refile sometime
    res = words[0].upper() + words[1:]
    if res == words:
        if env.debug():
            print "debug warning: %r did not change in capitalize_first_word" % (words,)
    return res

MIN_ALL, LOCAL_MIN, MIN_SEL = range(3) # internal codes for minimize command subtypes (bruce 051129)
    # this is a kluge compared to using command-specific subclasses, but better than testing something else like cmdname
    
class Minimize_CommandRun(CommandRun):
    """Class for single runs of the Minimize Selection or Minimize All commands
    (which one is determined by an __init__ arg, stored in self.args by superclass);
    create it when the command is invoked, to prep to run the command once;
    then call self.run() to actually run it.
    [#e A future code cleanup might split this into a Minimize superclass
    and separate subclasses for 'All' vs 'Sel' -- or it might not.
    As of 050412 the official distinction is stored in entire_part.]
    """
    def run(self):
        """Minimize the Selection or the current Part"""
        #bruce 050324 made this method from the body of MWsemantics.modifyMinimize
        # and cleaned it up a bit in terms of how it finds the movie to use.
        
        #bruce 050412 added 'Sel' vs 'All' now that we have two different Minimize buttons.
        # In future the following code might become subclass-specific (and cleaner):
        
        ## fyi: this old code was incorrect, I guess since 'in' works by 'is' rather than '==' [not verified]:
        ## assert self.args in [['All'], ['Sel']], "%r" % (self.args,)

        #bruce 051129 revising this to clarify it, though command-specific subclasses would be better
        assert len(self.args) >= 1
        cmd_subclass_code = self.args[0]
        cmd_type = self.kws.get('type','Minimize')
            # one of 'Minimize' or 'Adjust' or 'Adjust Atoms'; determines conv criteria, name [bruce 060705]
        self.cmd_type = cmd_type # kluge, see comment where used
        
        assert cmd_subclass_code in ['All','Sel','Atoms'] #e and len(args) matches that?

        # These words and phrases are used in history messages and other UI text;
        # they should be changed by specific commands as needed.
        # See also some computed words and phrases, e.g. self.word_Minimize,
        # below the per-command if stamements. [bruce 060705]
        if cmd_type.startswith('Adjust'):            
            self.word_minimize = "adjust"
            self.word_minimization = "adjustment"
            self.word_minimizing = "adjusting"
        else:
            assert cmd_type.startswith('Minimize') ####@@@@ remove when works
            self.word_minimize = "minimize"
            self.word_minimization = "minimization"
            self.word_minimizing = "minimizing"
            
        self.word_Minimize = capitalize_first_word( self.word_minimize)
        self.word_Minimizing = capitalize_first_word( self.word_minimizing)
        
        entire_part = (cmd_subclass_code == 'All')
            # (a self attr for entire_part is not yet needed)
            #e someday, entire_part might also be set later if selection happens to include everything, to permit optims,
            # but only for internal use, not for messages to user distinguishing the two commands.
            # Probably that would be a bad idea. [bruce 051129 revised this comment]
        
        if cmd_subclass_code == 'All':
            cmdtype = MIN_ALL
            cmdname = "%s All" % self.word_Minimize
        
        elif cmd_subclass_code == 'Sel':
            cmdtype = MIN_SEL
            cmdname = "%s Selection" % self.word_Minimize
        
        elif cmd_subclass_code == 'Atoms':
            #bruce 051129 added this case for Local Minimize (extending a kluge -- needs rewrite to use command-specific subclass)
            cmdtype = LOCAL_MIN
            cmdname = "%s Atoms"  % self.word_Minimize #bruce 060705; some code may assume this is always Adjust Atoms, as it is
            # self.args is parsed later
        
        else:
            assert 0, "unknown cmd_subclass_code %r" % (cmd_subclass_code,)
        self.cmdname = cmdname #e in principle this should come from a subclass for the specific command [bruce 051129 comment]
        startmsg = cmdname + ": ..."
        del cmd_subclass_code

        # redundant, in case these got changed in the if-statements:
        self.word_Minimize = capitalize_first_word( self.word_minimize)
        self.word_Minimizing = capitalize_first_word( self.word_minimizing)

        # Make sure some chunks are in the part.
        # (Valid for all cmdtypes -- Minimize only moves atoms, even if affected by jigs.)
        if not self.part.molecules: # Nothing in the part to minimize.
            env.history.message(greenmsg(cmdname + ": ") + redmsg("Nothing to %s." % self.word_minimize))
            return

        if cmdtype == MIN_SEL:
            selection = self.part.selection_from_glpane() # compact rep of the currently selected subset of the Part's stuff
            if not selection.nonempty():
                msg = greenmsg(cmdname + ": ") + redmsg("Nothing selected.") + \
                      " (Use %s All to %s the entire Part.)" % (self.word_Minimize, self.word_minimize)
                      #e might need further changes for Minimize Energy, if it's confusing that Sel/All is a dialog setting then
                env.history.message( msg)
                return
        elif cmdtype == LOCAL_MIN:
            from ops_select import selection_from_atomlist
            junk, atomlist, ntimes_expand = self.args
            selection = selection_from_atomlist( self.part, atomlist) #e in cleaned up code, selection object might come from outside
            selection.expand_atomset(ntimes = ntimes_expand) # ok if ntimes == 0

            # Rationale for adding monovalent atoms to the selection before
            # instantiating the sim_aspect
            #
            # (Refer to comments for sim_aspect.__init__.) Why is it safe to add
            # monovalent atoms to a selection? Let's look at what happens during a
            # local minimization.
            #
            # While minimiziing, we want to simulate as if the entire rest of the
            # part is grounded, and only our selection of atoms is free to move. The
            # most obvious approach would be to minimize all the atoms in the part
            # while applying anchors to the atoms that aren't in the selection. But
            # minimizing all the atoms, especially if the selection is small, is very
            # wasteful. Applying the simulator to atoms is expensive and we want to
            # minimize as few atoms as possible.
            #
            # A more economical approach is to anchor the atoms for two layers going
            # out from the selection. The reason for going out two layers, and not just
            # one layer, is that we need bond angle terms to simulate accurately. When
            # we get torsion angles we will probably want to bump this up to three
            # layers.
            #
            # Imagine labeling all the atoms in the selection with zero. Then take the
            # set of unlabeled atoms that are bonded to a zero-labeled atom, and label
            # all the atoms in that set with one. Next, take the set of yet-unlabeled
            # atoms that are bonded to a one-labeled atom, and label the atoms in that
            # set with two. The atoms labeled one and two become our first and second
            # layers, and we anchor them during the minimization.
            #
            # In sim_aspect.__init__, the labels for zero, one and two correspond
            # respectively to membership in the dictionaries self.moving_atoms,
            # self.boundary1_atoms, and self.boundary2_atoms.
            #
            # If an atom in the selection is anchored, we don't need to go two layers
            # out from that atom, only one layer. So we can label it with one, even
            # though it's a member of the selection and would normally be labeled with
            # zero. The purpose in doing this is to give the simulator a few less atoms
            # to worry about.
            #
            # If a jig includes one of the selected atoms, but additionally includes
            # atoms outside the selection, then it may not be obvious how to simulate
            # that jig. For the present, the only jig that counts in a local
            # minimization is an anchor, because all the other jigs are too complicated
            # to simulate.
            #
            # The proposed fix here has the effect that monovalent atoms bonded to
            # zero-labeled atoms are also labeled zero, rather than being labeled one,
            # so they are allowed to move. Why is this OK to do?
            #
            # (1) Have we violated the assumption that the rest of the part is locked
            # down? Yes, as it applies to those monovalent atoms, but they are
            # presumably acceptable violations, since bug 1240 is regarded as a bug.
            #
            # (2) Have we unlocked any bond lengths or bond angles that should remain
            # locked? Again, only those which involve (and necessarily end at) the
            # monovalent atoms in question. The same will be true when we introduce
            # torsion terms.
            #
            # (3) Have we lost any ground on the jig front? If a jig includes one or
            # more of the monovalent atoms, possibly - but the only jigs we are
            # simulating in this case is anchors, and those will be handled correctly.
            # Remember that anchored atoms are only extended one layer, not two, but
            # with a monovalent atom bonded to a selected atom, no extension is
            # possible at all.
            #
            # One can debate about whether bug 1240 should be regarded as a bug. But
            # having accepted it as a bug, one cannot object to adding these monovalents
            # to the original selection.
            #
            # wware 060410 bug 1240
            atoms = selection.selatoms
            for atm in atoms.values():
                # enumerate the monovalents bonded to atm
                for atm2 in filter(lambda atm: not atm.is_singlet(), atm.baggageNeighbors()):
                    atoms[atm2.key] = atm2

        else:
            assert cmdtype == MIN_ALL
            selection = self.part.selection_for_all()
                # like .selection_from_glpane() but for all atoms presently in the part [bruce 050419]
            # no need to check emptiness, this was done above
        
        self.selection = selection #e might become a feature of all CommandRuns, at some point

        # At this point, the conditions are met to try to do the command.
        env.history.message(greenmsg( startmsg)) #bruce 050412 doing this earlier
        
        # Disable some QActions (menu items/toolbar buttons) during minimize.
        self.win.disable_QActions_for_sim(True)
        try:
            simaspect = sim_aspect( self.part, selection.atomslist(), cmdname_for_messages = cmdname ) #bruce 051129 passing cmdname
                # note: atomslist gets atoms from selected chunks, not only selected atoms
                # (i.e. it gets atoms whether you're in Select Atoms or Select Chunks mode)
            # history message about singlets written as H (if any);
            #bruce 051115 updated comment: this is used for both Minimize All and Minimize Selection as of long before 051115;
            # for Run Sim this code is not used (so this history message doesn't go out for it, though it ought to)
            # but the bug254 X->H fix is done (though different code sets the mapping flag that makes it happen).
            nsinglets_H = simaspect.nsinglets_H()
            if nsinglets_H: #bruce 051209 this message code is approximately duplicated elsewhere in this file
                info = fix_plurals( "(Treating %d bondpoint(s) as Hydrogens, during %s)" % (nsinglets_H, self.word_minimization) )
                env.history.message( info)
            nsinglets_leftout = simaspect.nsinglets_leftout()
            assert nsinglets_leftout == 0 # for now
            # history message about how much we're working on; these atomcounts include singlets since they're written as H
            nmoving = simaspect.natoms_moving()
            nfixed  = simaspect.natoms_fixed()
            info = fix_plurals( "(%s %d atom(s)" % (self.word_Minimizing, nmoving))
            if nfixed:
                them_or_it = (nmoving == 1) and "it" or "them"
                info += fix_plurals(", holding %d atom(s) fixed around %s" % (nfixed, them_or_it) )
            info += ")"
            env.history.message( info) 
            self.doMinimize(mtype = 1, simaspect = simaspect) # 1 = single-frame XYZ file. [this also sticks results back into the part]
            #self.doMinimize(mtype = 2) # 2 = multi-frame DPB file.
        finally:
            self.win.disable_QActions_for_sim(False)
        simrun = self._movie._simrun #bruce 050415 klugetower
        if not simrun.said_we_are_done:
            env.history.message("Done.")
        return
    def doMinimize(self, mtype = 1, simaspect = None):
        #bruce 051115 renamed method from makeMinMovie
        #bruce 051115 revised docstring to fit current code #e should clean it up more
        """Minimize self.part (if simaspect is None -- no longer used)
        or its given simaspect (simulatable aspect) (used for both Minimize Selection and Minimize All),
        generating and showing a movie (no longer asked for) or generating and applying to part an xyz file.
           The mtype flag means:
            1 = tell writemovie() to create a single-frame XYZ file.
            2 = tell writemovie() to create a multi-frame DPB moviefile. [###@@@ not presently used, might not work anymore]
        """
        assert mtype == 1 #bruce 051115
        assert simaspect is not None #bruce 051115
        #bruce 050324 made this from the Part method makeMinMovie.
        suffix = self.part.movie_suffix()
        if suffix is None: #bruce 050316 temporary kluge; as of circa 050326 this is not used anymore
            env.history.message( redmsg( "%s is not yet implemented for clipboard items." % self.word_Minimize))
            return
        #e use suffix below? maybe no need since it's ok if the same filename is reused for this.

        # bruce 050325 change: don't use or modify self.assy.current_movie,
        # since we're not making a movie and don't want to prevent replaying
        # the one already stored from some sim run.
        # [this is for mtype == 1 (always true now) and might affect writemovie ###@@@ #k.]

        # NOTE: the movie object is used to hold params and results from minimize, even if it makes an xyz file rather than a movie file.
        # And at the moment it never makes a movie file when called from this code. [bruce 051115 comment about months-old situation]
        
        movie = Movie(self.assy) # do this in writemovie? no, the other call of it needs it passed in from the dialog... #k
            # note that Movie class is misnamed since it's really a SimRunnerAndResultsUser... which might use .xyz or .dpb results
            # (maybe rename it SimRun? ###e also, it needs subclasses for the different kinds of sim runs and their results...
            #  or maybe it needs a subobject which has such subclasses -- not yet sure. [bruce 050329])

        self._movie = movie #bruce 050415 kluge; note that class SimRun does the same thing.
            # Probably it means that this class, SimRun, and this way of using Movie should all be the same,
            # or at least have more links than they do now. ###@@@

        # Set update_cond for controlling realtime update settings for watching this "movie" (an ongoing sim).
        # There are three possible ways (soon after A8 only the first one will be used) [bruce 060705]:
        # - caller specified it.
        # - if it didn't, use new common code to get it from General Prefs page.
        # - if that fails, use older code for that.
        #
        # WARNING: it turns out this happens whether or not the checkbox pref says it should --
        # that is checked separately elsewhere! And that's a bug, since we need to use a different checkbox
        # depending on the command.
        # let's see if we can consolidate the "enabling flag" into update_cond itself? so it is None or False if we won't update.
        # this is now attempted...
        if env.debug():
            print "debug fyi: runSim watch_motion update_cond computed here (even if not watching motion)" #bruce 060705
        try:
            # Only the client code knows where to find the correct realtime update settings widgets
            # (or someday, knows whether these values come from widgets at all, vs from a script).
            # It should figure out the update_cond (False if we should not watch motion), and tell us in self.kws['update_cond'].
            update_cond = self.kws['update_cond']
            assert update_cond or (update_cond is False) # a callable or False [remove when works]
        except:
            ## print_compact_traceback("bug ...: ")
            if env.debug():
                print "debug: fyi: runSim grabbing uprefs data"
            # For A8, this is normal, since only (at most) Minimize Energy sets self.kws['update_cond'] itself.
            # This will be used routinely in A8 by Adjust All and Adjust Selection, and maybe Adjust Atoms (not sure).
            #
            # Just get the values from the General Prefs page.
            # But at least try to do that using new common code.
            try:
                from widget_controllers import realtime_update_controller
                uprefs = env.mainwindow().uprefs
                from prefs_constants import Adjust_watchRealtimeMinimization_prefs_key ###@@@ should depend on command, or be in movie...
                ruc = realtime_update_controller(
                    ( uprefs.update_btngrp_group, ###k name
                      uprefs.update_number_spinbox, uprefs.update_units_combobox ),
                    None, # checkbox ###@@@ maybe not needed, since UserPrefs sets up the connection #k
                    Adjust_watchRealtimeMinimization_prefs_key )
                update_cond = ruc.get_update_cond_from_widgets()
                # note, if those widgets are connected to env.prefs, that's not handled here or in ruc;
                # I'm not sure if they are. Ideally we'd tell ruc the prefs_keys and have it handle that too,
                # perhaps making it a long-lived object (though that might not be necessary).
                assert update_cond or (update_cond is False) # a callable or False
            except:
                # even that didn't work. Complain, then fall back to otherwise-obsolete old code.
                print_compact_traceback("bug using realtime_update_controller in runSim, will use older code instead: ")
                # This code works (except for always using the widgets from the General Prefs page,
                # even for Minimize Energy), but I'll try to replace it with calls to common code.
                # [bruce 060705]
                # This code for setting update_cond is duplicated (inexactly) in SimSetup.createMoviePressed() in SimSetup.py.
                uprefs = env.mainwindow().uprefs
                update_units = uprefs.update_units_combobox.currentText()
                update_number = uprefs.update_number_spinbox.value()
                if uprefs.update_asap_rbtn.isChecked():
                    update_cond = ( lambda simtime, pytime, nframes:
                                    simtime >= max(0.05, min(pytime * 4, 2.0)) )
                elif update_units == 'frames':
                    update_cond = ( lambda simtime, pytime, nframes, _nframes = update_number:  nframes >= _nframes )
                elif update_units == 'seconds':
                    update_cond = ( lambda simtime, pytime, nframes, _timelimit = update_number:  simtime + pytime >= _timelimit )
                elif update_units == 'minutes':
                    update_cond = ( lambda simtime, pytime, nframes, _timelimit = update_number * 60:  simtime + pytime >= _timelimit )
                elif update_units == 'hours':
                    update_cond = ( lambda simtime, pytime, nframes, _timelimit = update_number * 3600:  simtime + pytime >= _timelimit )
                else:
                    print "don't know how to set update_cond from (%r, %r)" % (update_number, update_units)
                    update_cond = None
                # new as of 060705, in this old code
                if not env.prefs[Adjust_watchRealtimeMinimization_prefs_key]:
                    update_cond = False
            pass
        # now do this with update_cond, however it was computed
        movie.update_cond = update_cond
        
        # semi-obs comment, might still be useful [as of 050406]:
        # Minimize Selection [bruce 050330] (ought to be a distinct command subclass...)
        # this will use the spawning code in writemovie but has its own way of writing the mmp file.
        # to make this clean, we need to turn writemovie into more than one method of a class
        # with more than one subclass, so we can override one of them (writing mmp file)
        # and another one (finding atom list). But to get it working I might just kluge it
        # by passing it some specialized options... ###@@@ not sure

        movie._cmdname = self.cmdname #bruce 050415 kluge so writemovie knows proper progress bar caption to use
            # (not really wrong -- appropriate for only one of several
            # classes Movie should be split into, i.e. one for the way we're using it here, to know how to run the sim,
            # which is perhaps really self (a SimRunner), once the code is fully cleaned up.

        r = writemovie(self.part, movie, mtype, simaspect = simaspect, print_sim_warnings = True,
                       cmdname = self.cmdname, cmd_type = self.cmd_type) # write input for sim, and run sim
            # this also sets movie.alist from simaspect
        if r:
            # We had a problem writing the minimize file.
            # Simply return (error message already emitted by writemovie). ###k
            return
        
        if mtype == 1:  # Load single-frame XYZ file.
            newPositions = readxyz( movie.filename, movie.alist ) # movie.alist is now created in writemovie [bruce 050325]
            # retval is either a list of atom posns or an error message string.
            assert type(newPositions) in [type([]),type("")]
            if type(newPositions) == type([]):
                #bruce 060102 note: following code is approximately duplicated somewhere else in this file.
                movie.moveAtoms(newPositions)
                # bruce 050311 hand-merged mark's 1-line bugfix in assembly.py (rev 1.135):
                self.part.changed() # Mark - bugfix 386
                self.part.gl_update()
            else:
                #bruce 050404: print error message to history
                env.history.message(redmsg( newPositions))
        else: # Play multi-frame DPB movie file.
            ###@@@ bruce 050324 comment: can this still happen? [no] is it correct [probably not]
            # (what about changing mode to movieMode, does it ever do that?) [don't know]
            # I have not reviewed this and it's obviously not cleaned up (since it modifies private movie attrs).
            # But I will have this change the current movie, which would be correct in theory, i think, and might be needed
            # before trying to play it (or might be a side effect of playing it, this is not reviewed either).
            ###e bruce 050428 comment: if self.assy.current_movie exists, should do something like close or destroy it... need to review
            self.assy.current_movie = movie
            # If _setup() returns a non-zero value, something went wrong loading the movie.
            if movie._setup(): return
            movie._play()
            movie._close()
        return
    pass # end of class Minimize_CommandRun

# ==

def LocalMinimize_function( atomlist, nlayers ): #bruce 051207
    win = atomlist[0].molecule.part.assy.w # kluge!
    #e should probably add in monovalent real atom neighbors -- but before finding neighbors layers, or after?
    # (note that local min will always include singlets... we're just telling it to also treat attached H the same way.
    #  that would suggest doing it after, as an option to Minimize. Hmm, should even Min Sel do it? Discuss.)
    cmdrun = Minimize_CommandRun( win, 'Atoms', atomlist, nlayers, type = 'Adjust Atoms')
    cmdrun.run()
    return

# == helper code for Minimize Selection [by bruce, circa 050406] [also used for Minimize All, probably as of 050419, as guessed 051115]

from elements import Singlet

#obs comment:
###@@@ this will be a subclass of SimRun, like Movie will be... no, that's wrong.
# Movie will be subclass of SimResults, or maybe not since those need not be a class
# it's more like an UnderstoodFile and also an UndoableContionuousOperation...
# and it needn't mix with simruns not related to movies.
# So current_movie maybe split from last_simrun? might fix some bugs from aborted simruns...
# for prefs we want last_started_simrun, for movies we want last_opened_movie (only if valid? not sure)...

def atom_is_anchored(atm):
    "is an atm anchored in space, when simulated?"
    ###e refile as atom method?
    #e permit filtering set of specific jigs (instances) that can affect it?
    #e really a Part method??
    res = False
    for jig in atm.jigs:
        if jig.anchors_atom(atm): # as of 050321, true only for Anchor jigs
            res = True # but continue, so as to debug this new method anchors_atom for all jigs
    return res
    
class sim_aspect: # as of 051115 this is used for Min Sel and Min All but not Run Sim; verified by debug_sim output.
    # warning: it also assumes this internally -- see comment below about "min = True".
    """Class for a "simulatable aspect" of a Part.
    For now, there's only one kind (a subset of atoms, some fixed in position),
    so we won't split out an abstract class for now.
    Someday there would be other kinds, like when some chunks were treated
    as rigid bodies or jigs and the sim was not told about all their atoms.
    """
    def __init__(self, part, atoms, cmdname_for_messages = "Minimize" ): #bruce 051129 passing cmdname_for_messages
        """atoms is a list of atoms within the part (e.g. the selected ones,
        for Minimize Selection); we copy it in case caller modifies it later.
        [Note that this class has no selection object and does not look at
        (or change) the "currently selected" state of any atoms,
        though some of its comments are worded as if it did.]
           We become a simulatable aspect for simulating motion of those atoms
        (and of any singlets bonded to them, since user has no way to select
        those explicitly),
        starting from their current positions, with a "boundary layer" of other
        directly bonded atoms (if any) held fixed during the simulation.
        [As of 050408 this boundary will be changed from thickness 1 to thickness 2
         and its own singlets, if any, will also be grounded rather than moving.
         This is because we're approximating letting the entire rest of the Part
         be grounded, and the 2nd layer of atoms will constrain bond angles on the
         first layer, so leaving it out would be too different from what we're
         approximating.]
        (If any given atoms have Anchor jigs, those atoms are also treated as
        boundary atoms and their own bonds are only explored to an additional depth
        of 1 (in terms of bonds) to extend the boundary.
        So if the user explicitly selects a complete boundary of Anchored atoms,
        only their own directly bonded real atoms will be additionally grounded.)
           All atoms not in our list or its 2-thick boundary are ignored --
        so much that our atoms might move and overlap them in space.
           We look at jigs which attach to our atoms,
        but only if we know how to sim them -- we might not, if they also
        touch other atoms. For now, we only look at Anchor jigs (as mentioned
        above) since this initial implem is only for Minimize. When we have
        Simulate Selection, this will need revisiting. [Update: we also look at
        other jigs, now that we have Enable In Minimize for motors.]
           If we ever need to emit history messages
        (e.g. warnings) we'll do it using a global history variable (NIM)
        or via part.assy. For now [050406] none are emitted.
        """
        if debug_sim: #bruce 051115 added this
            print "making sim_aspect for %d atoms (maybe this only counts real atoms??)" % len(atoms) ###@@@ only counts real atoms??
        self.part = part
        self.cmdname_for_messages = cmdname_for_messages
        self.moving_atoms = AtomDict()
        self.boundary1_atoms = AtomDict()
        self.boundary2_atoms = AtomDict()
        assert atoms, "no atoms in sim_aspect"
        for atm in atoms:
            assert atm.molecule.part == part
            assert atm.element != Singlet # when singlets are selectable, this whole thing needs rethinking
            if atom_is_anchored(atm):
                self.boundary1_atoms[atm.key] = atm
            else:
                self.moving_atoms[atm.key] = atm
            # pretend that all singlets of selected atoms were also selected
            # (but were not grounded, even if atm was)
            for sing in atm.singNeighbors():
                self.moving_atoms[sing.key] = sing
        del atoms
        # now find the boundary1 of the moving_atoms
        for movatm in self.moving_atoms.values():
            for atm2 in movatm.realNeighbors():
                # (not covering singlets is just an optim, since they're already in moving_atoms)
                # (in fact, it's probably slower than excluding them here! I'll leave it in, for clarity.)
                if atm2.key not in self.moving_atoms:
                    self.boundary1_atoms[atm2.key] = atm2 # might already be there, that's ok
        # now find the boundary2 of the boundary1_atoms;
        # treat singlets of boundary1 as ordinary boundary2 atoms (unlike when we found boundary1);
        # no need to re-explore moving atoms since we already covered their real and singlet neighbors
        for b1atm in self.boundary1_atoms.values():
            for atm2 in b1atm.neighbors():
                if (atm2.key not in self.moving_atoms) and (atm2.key not in self.boundary1_atoms):
                    self.boundary2_atoms[atm2.key] = atm2 # might be added more than once, that's ok
        # no need to explore further -- not even for singlets on boundary2 atoms.

        # Finally, come up with a global atom order, and enough info to check our validity later if the Part changes.
        # We include all atoms (real and singlet, moving and boundary) in one list, sorted by atom key,
        # so later singlet<->H conversion by user wouldn't affect the order.
        items = self.moving_atoms.items() + self.boundary1_atoms.items() + self.boundary2_atoms.items()
        items.sort()
        self._atoms_list = [atom for key, atom in items]
            # make that a public attribute? nah, use an access method
        for i in range(1,len(self._atoms_list)):
            assert self._atoms_list[i-1] != self._atoms_list[i]
            # since it's sorted, that proves no atom or singlet appears twice
        # anchored_atoms alone (for making boundary jigs each time we write them out)
        items = self.boundary1_atoms.items() + self.boundary2_atoms.items()
        items.sort()
        self.anchored_atoms_list = [atom for key, atom in items]
        #e validity checking info is NIM, except for the atom lists themselves
        return
    def atomslist(self):
        return list(self._atoms_list)
    def natoms_moving(self):
        return len(self._atoms_list) - len(self.anchored_atoms_list)
    def natoms_fixed(self):
        return len(self.anchored_atoms_list)
    def nsinglets_H(self):
        "return number of singlets to be written as H for the sim"
        singlets = filter( lambda atm: atm.is_singlet(), self._atoms_list )
        return len(singlets)
    def nsinglets_leftout(self):
        "return number of singlets to be entirely left out of the sim input file"
        return 0 # for now
    def writemmpfile(self, filename):
        #bruce 050404 (for most details). Imitates some of Part.writemmpfile aka files_mmp.writemmpfile_part.
        #e refile into files_mmp so the mmp format code is in the same place? maybe just some of it.
        # in fact the mmp writing code for atoms and jigs is not in files_mmp anyway! tho the reading code is.
        """write our data into an mmp file; only include just enough info to run the sim
        [###e Should we make this work even if the atoms have moved but not restructured since we were made? I think yes.
         That means the validity hash is really made up now, not when we're made.]
        """
        ## do we need to do a part.assy.update_parts() as a precaution?? if so, have to do it earlier, not now.
        from files_mmp import writemmp_mapping
        assy = self.part.assy
        fp = open(filename, "w")
        mapping = writemmp_mapping(assy, min = True)
            #e rename min option? (for minimize; implies sim as well;
            #   affects mapping attrnames in chem.py atom.writemmp)
            #bruce 051031 comment: it seems wrong that this class assumes min = True (rather than being told this in __init__). ###@@@
        mapping.set_fp(fp)    
        # note that this mmp file doesn't need any grouping or chunking info at all.
        try:
            mapping.write_header() ###e header should differ in this case
            ## node.writemmp(mapping)
            self.write_atoms(mapping)
            self.write_grounds(mapping)
            self.write_minimize_enabled_jigs(mapping)
            mapping.write("end mmp file for %s (%s)\n" % (self.cmdname_for_messages, assy.name) ) #bruce 051129 revised this
                # sim & cad both ignore text after 'end'
                #bruce 051115: fixed this file comment, since this code is also used for Minimize All.
        except:
            mapping.close(error = True)
            raise
        else:
            mapping.close()
        return
    def write_atoms(self, mapping):
        assert mapping.sim
        for atm in self._atoms_list: # includes both real atoms and singlets, both moving and anchored, all sorted by key
            atm.writemmp( mapping) # mapping.sim means don't include any info not relevant to the sim
                # note: this method knows whether & how to write a Singlet as an H (repositioned)!
    def write_grounds(self, mapping):
        from jigs import fake_Anchor_mmp_record
        atoms = self.anchored_atoms_list
        nfixed = len(atoms)
        max_per_jig = 20
        for i in range(0, nfixed, max_per_jig): # starting indices of jigs for fixed atoms
            indices = range( i, min( i + max_per_jig, nfixed ) )
            if debug_sim:
                print "debug_sim: writing Anchor for these %d indices: %r" % (len(indices), indices)
            # now write a fake Anchor which has just the specified atoms
            these_atoms = [atoms[i] for i in indices]
            line = fake_Anchor_mmp_record( these_atoms, mapping) # includes \n at end
            mapping.write(line)
            if debug_sim:
                print "debug_sim: wrote %r" % (line,)           
        return
        
    def write_minimize_enabled_jigs(self, mapping): # Mark 051006
        '''Writes any jig to the mmp file which has the attr "enable_minimize"=True
        '''
        assert mapping.min #bruce 051031; detected by writemmp call, below; this scheme is a slight kluge
        
        from jigs import Jig
        def func_write_jigs(nn):
            if isinstance(nn, Jig) and nn.enable_minimize:
                #bruce 051031 comment: should we exclude the ones written by write_grounds?? doesn't matter for now. ####@@@@
                if debug_sim:
                    print "The jig [", nn.name, "] was written to minimize MMP file.  It is enabled for minimize."
                nn.writemmp(mapping)
            return # from func_write_jigs only
            
        self.part.topnode.apply2all( func_write_jigs)
        return
        
    pass # end of class sim_aspect

# end
