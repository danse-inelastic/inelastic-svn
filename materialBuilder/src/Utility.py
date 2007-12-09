# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
"""
Utility.py -- class Node (superclass for all model-tree objects), Group, and a few subclasses,
defining a uniform API to permit all Node subclasses to be shown in the model tree.

$Id: Utility.py,v 1.165 2007/07/04 05:04:41 bsmith Exp $

Other files define other subclasses of Node, such as molecule and Jig.

This file should eventually be split into separate modules for Node, Group and specialized Groups, and others.

History: originally by Josh; gradually has been greatly extended by Bruce,
but the basic structure of Nodes and Groups has not been changed.
"""
__author__ = "Josh"

import sys, os
from debug import print_compact_stack, print_compact_traceback
import platform
import env #bruce 050901
from constants import genKey, gensym
from state_utils import copy_val, StateMixin #bruce 060223

from state_constants import S_PARENT, S_DATA, S_CHILD, S_CHILDREN

from PyQt4 import QtGui
from GroupProp import GroupProp
from VQT import V, Q
from PartProp import PartProp

debug_undoable_attrs = False

def debug_pref_DND_drop_at_start_of_groups(): # not yet used, but will be
    #bruce 070525 -- this is so we can experiment with this NFR someday.
    # The code that needs to be affected by this is not yet implemented (but has a commented out call to it).
    # If we implement that and it works and we like it,
    # we'll change the default, or maybe even hardcode it, or maybe make it an official pref setting.
    from debug_prefs import debug_pref, Choice_boolean_False, Choice_boolean_True
        # not sure if toplevel import is safe, and needing a debug_pref is probably temporary
    return debug_pref("DND: drop at start of groups?", Choice_boolean_False, non_debug = True, prefs_key = True)

# utility function: global cache for QPixmaps (needed by most Node subclasses)

_pixmap_image_path = None
_pixmaps = {}
_icons = {}

_iconprefix = os.path.dirname(os.path.abspath(sys.argv[0]))
_iconprefix = os.sep.join(_iconprefix.split(os.sep)[:-1] + ["src"])

def image_directory(): #bruce 070604
    """Return the full pathname of the directory in which the image files
    (mostly icons) with names like ui/<subdir>/<file> exist.
       Note: As of 070604, for developers this path ends with cad/src
    and is also the main source directory, but in built releases it
    might be something different and might be platform-dependent or even
    build-system-dependent.
    """
    return _iconprefix

def geticon(name, _iconprefix = _iconprefix):
    path = os.path.join(_iconprefix, name)
    icon = QtGui.QIcon(path)
    if icon.isNull():
        print 'geticon - null icon for: ' + path
    return icon

def getpixmap(name, _iconprefix = _iconprefix):
    path = os.path.join(_iconprefix, name)
    pixmap = QtGui.QPixmap(path)
    if pixmap.isNull():
        print 'getpixmap - null pixmap for: ' + path
    return pixmap

def imagename_to_pixmap(imagename): #bruce 050108
    """Given the basename of a file in our cad/images directory [now cad/src/ui],
    return a QPixmap created from that file. Cache these
    (in our own Python directory, not Qt's QPixmapCache)
    so that at most one QPixmap is made from each file.
    If the imagename does not exist, a Null pixmap is returned.
    """
    global _pixmap_image_path, _pixmaps
    try:
        return _pixmaps[imagename]
    except KeyError:
        if not _pixmap_image_path:
            # This runs once per Atom session (unless this directory is missing).
            #
            # (We don't run it until needed, in case something modifies
            #  sys.argv[0] during init (we want the modified form in that case).
            #  As of 050108 this is not known to ever happen. Another reason:
            #  if we run it when this module is imported, we get the error message
            #  "QPaintDevice: Must construct a QApplication before a QPaintDevice".)
            #
            # We assume sys.argv[0] looks like .../cad/src/xxx.py
            # and we want .../cad/images. [note: this comment is out of date]
            from os.path import dirname, abspath
            cadpath = dirname(dirname(abspath(sys.argv[0]))) # ../cad
            _pixmap_image_path = os.path.join(cadpath, "src/ui/")
            assert os.path.isdir(_pixmap_image_path), "missing pixmap directory: \"%s\"" % _pixmap_image_path
        pixmappath = os.path.join( _pixmap_image_path, imagename)
        if not os.path.exists(pixmappath):
            print 'pixmap does not exist: ' + pixmappath
            import traceback
            traceback.print_stack(file=sys.stdout)
        pixmap = QtGui.QPixmap(pixmappath)
            # missing file prints a warning but doesn't cause an exception,
            # just makes a null pixmap [confirmed by mark 060202]
        _pixmaps[imagename] = pixmap
        return pixmap
    pass

def imagename_to_icon(imagename): #bruce 050108
    """Given the basename of a file in our cad/images directory,
    return a QPixmap created from that file. Cache these
    (in our own Python directory, not Qt's QPixmapCache)
    so that at most one QPixmap is made from each file.
    If the imagename does not exist, a Null pixmap is returned.
    """
    global _pixmap_image_path, _icons
    try:
        return _icons[imagename]
    except KeyError:
        if not _pixmap_image_path:
            # This runs once per Atom session (unless this directory is missing).
            #
            # (We don't run it until needed, in case something modifies
            #  sys.argv[0] during init (we want the modified form in that case).
            #  As of 050108 this is not known to ever happen. Another reason:
            #  if we run it when this module is imported, we get the error message
            #  "QPaintDevice: Must construct a QApplication before a QPaintDevice".)
            #
            # We assume sys.argv[0] looks like .../cad/src/xxx.py
            # and we want .../cad/images.
            from os.path import dirname, abspath
            cadpath = dirname(dirname(abspath(sys.argv[0]))) # ../cad
            _pixmap_image_path = os.path.join(cadpath, "src/ui/")
            assert os.path.isdir(_pixmap_image_path), "missing pixmap directory: \"%s\"" % _pixmap_image_path
        iconpath = os.path.join( _pixmap_image_path, imagename)
        if not os.path.exists(iconpath):
            print 'icon does not exist: ' + iconpath
        icon = QtGui.QIcon(iconpath)
            # missing file prints a warning but doesn't cause an exception,
            # just makes a null icon [confirmed by mark 060202]
        _icons[imagename] = icon
        return icon
    pass

# Unique id for all Nodes -- might generalize to other objects too.
# Unlike python builtin id(node), this one will never be reused when an old node dies.
nodekey = genKey(start = 1)
    # note: atoms are not nodes, so possible overlap of
    # atom.key and node._id should be ok for now.

def node_id(node):
    "session-unique id for a Node (never reused) (legal to call for None, then returns None)"
    if node is None:
        return None
    assert isinstance(node, Node) #e might relax this later
    try:
        node._id # make sure it exists already
    except AttributeError:
        node._id = nodekey.next()
    return node._id

# superclass of all Nodes

def node_name(node): # use in error or debug messages for safety, rather than node.name
    if node is None: return "<None>"
    try:
        return node.name
    except AttributeError:
        return "<node has no .name>"
    pass

_will_kill_count = 1 # this must start > 0, even though it's incremented when next used [bruce 060327]

class Node( StateMixin):
    """
    This is the basic object, inherited by groups, molecules, jigs,
    and some more specialized subclasses. The methods of Node are designed
    to be typical of "leaf Nodes" -- many of them are overridden by Group,
    and some of them by other Node subclasses.
    """

    featurename = "" # default value of per-subclass attribute -- wiki help featurename for Node subclass [bruce 051201]
    
    name = "" # for use before __init__ runs (used in __str__ of subclasses)
    
    # default values of instance variables
    picked = False # whether it's selected
        # (for highlighting in all views, and being affected by operations)
    hidden = False # whether to make it temporarily invisible in the glpane
        # (note: self.hidden is defined, but always False, for Groups;
        #  it might be set for any leaf node whether or not that node is ever actually
        #  shown in the glpane.)
    open = False # bruce 050125; kluge to make it easier to count open nodes in a tree
        # (this will never become True except for Groups)
        # (when more than one tree widget can show the same node, .open will need replacement
        #  with treewidget-specific state #e)
    dad = None
    part = None #bruce 050303
    prior_part = None #bruce 050527
    disabled_by_user_choice = False
        # [bruce 050505 made this default on all Nodes, tho only Jigs use the attr so far; see also is_disabled]
    
    is_movable = False #mark 060120

    copyable_attrs = ('name', 'hidden', 'open', 'disabled_by_user_choice') #bruce 050526
        # (see also __declare_undoable_attrs [bruce 060223])
        # subclasses need to extend this
        #e could someday use these to help make mmp writing and reading more uniform,
        # if we also listed the ones handled specially (so we can only handle the others in the new uniform way)

    _s_attr_dad = S_PARENT #obs cmt: overridden (bug) (doesn't matter for now) [i think that's fixed now, anyway, 060224]
    _s_attr_picked = S_DATA
    _s_categorize_picked = 'selection'
    _s_attr_part = S_CHILD
        # has to be child to be found (another way would be assy._s_scan_children); not S_CACHE since Parts store some defining state
    #e need anything to reset prior_part to None? yes, do it in _undo_update.
    _s_attr_assy = S_PARENT
        # assy can't be left out, since on some or all killed nodes it's foolishly set to None, which is
        # a change we need to undo when we revive them.

    def _undo_update(self): #bruce 060223
        # no change to .part, since that's declared as S_CHILD
        self.prior_part = None
        del self.prior_part # save RAM
        StateMixin._undo_update(self)
        return

    def __init__(self, assy, name, dad = None):
        #bruce 050216 fixed inconsistent arg order [re other leaf nodes -- Group is not yet fixed], made name required
        """Make a new node (Node or any subclass), in the given assembly (assy)
        (I think assy must always be supplied, but I'm not sure),
        with the given name (or "" if the supplied name is None),
        and with the optionally specified dad (a Group node or None),
        adding it to that dad as a new member (unless it's None or not specified, which is typical).
        All args are supplied positionally, even the optional one.
           Warning: arg order was revised by bruce 050216 to be more consistent with subclasses,
        but Group's arg order was and still is inconsistent with all other Node classes' arg order.
        """
        #bruce 050205 added docstring; bruce 050216 revised it

##bruce 051013: this is no longer needed (and neither is the _um_key argument I recently added to __init__):
##        if assy == '<not an assembly>':
##            # i.e. if we are _nullMol
##            pass # our changes get tracked into a garbage dict, from where they periodically get discarded
##        else:
##            self._um_init( assy._u_archive, _um_key )
##            # this is needed before any _um_xxx calls on self (used for recording or summarizing changes)

        self.name = name or "" # assumed to be a string by some code
        
        # assy -- as temporary kluge, permitted to be a Part as well [bruce 050223]
        from assembly import assembly # the class
        if assy is not None and not isinstance(assy, assembly) and assy != '<not an assembly>':
            assert 0, "Node assy must be an assembly, not a Part" # bruce 050527 stop permitting this
        # verify assy is not None (not sure if that's allowed in principle, but I think it never happens) [050223]
        if assy is None:
            if platform.atom_debug: # might not yet be safe to print self, esp if it's a subclass
                print_compact_stack("atom_debug: Node or Group constructed with null assy = %r" % assy)
        self.assy = assy
        if dad: # dad must be another Node (which must be a Group), or None
            dad.addchild(self) #bruce 050206 changed addmember to addchild, enforcing dad correctness
                # warning [bruce 050316]: this might call inherit_part; subclasses must be ready for this
                # by the time their inits call ours, e.g. a Group must have a members list by then.
            assert self.dad is dad
        if self.__declare_undoable_attrs is not None: #bruce 060223 (temporary kluge)
            # it's None except the first time in each Node subclass; is there a faster test? (Guess: boolean test is slower.)
            self.__declare_undoable_attrs()
        return

    def __repr__(self): #bruce 060220
        "[subclasses can override this, and often do]"
        classname = self.__class__.__name__
        try:
            name_msg = ", name = %r" % (self.name,)
        except:
            name_msg = " (exception in `self.name`)"
        return "<%s at %#x%s>" % (classname, id(self), name_msg)
    
    def setAssy(self, assy): #bruce 051227, Node method [used in depositMode; #e should rename to avoid confusion with GLPane method]
        "Change self.assy from its current value to assy, cleanly removing self from the prior self.assy if that is not assy."
        if self.assy is not assy:
            oldassy = self.assy
            if oldassy is not None:
                assert oldassy != '<not an assembly>' # simplest to just require this; nodes constructed that way shouldn't be moved
                from assembly import assembly # the class
                assert isinstance(oldassy, assembly)
                # some of the above conds might not be needed, or might be undesirable; others should be moved into following subr
                self.remove_from_parents()
                assert self.assy is None
            # now ok to replace self.assy, which is None or (ignoring the above assert) '<not an assembly>'
            # (safety of latter case unverified, but I think it will never happen, even without the assert that disallows it)
            assert self.assy is None
            self.assy = assy
            assert self.part is None
            assert self.dad is None
        return
    
    def get_featurename(self): #bruce 051201
        "Return the wiki-help featurename for this object's class, or '' if there isn't one."
        return self.__class__.featurename # intended to be a per-subclass constant... so enforce this until we need otherwise
    
    def _um_initargs(self): #bruce 051013 [in class Node]
        # [as of 060209 this is probably well-defined and correct (for most subclasses), but not presently used]
        """Return args and kws suitable for __init__.
        [Overrides an undo-related superclass method; see its docstring for details.]
        """
        return (self.assy, self.name), {}
            # self.dad (like most inter-object links) is best handled separately

    def _um_existence_permitted(self): #bruce 051005 [###@@@ as of 060209 it seems likely this should go away, but I'm not sure]
        """[overrides UndoStateMixin method]
        Return True iff it looks like we should be considered to exist in self.assy's model of undoable state.
        Returning False does not imply anything's wrong, or that we should be or should have been killed/destroyed/deleted/etc --
        just that changes in us should be invisible to Undo.
        """
        return self.assy is not None and self.part is not None and self.dad is not None
            ###e and we're under root? does that method exist? (or should viewpoint objects count here?)

    def __declare_undoable_attrs(self): #bruce 060223
        """[private method for internal use by Node.__init__ only; temporary kluge until individual _s_attr decls are added]
        Scan the perhaps-someday-to-be-deprecated per-class list, copyable_attrs,
        and add _s_attr decls for the attrs listed in them to self.__class__ (Node or any of its subclasses).
        Don't override any such decls already present, if possible [not sure if you can tell which class added them #k].
        Should be run only once per Node subclass, but needs an example object (self) to run on.
        Contains its own kluge to help cause it to be run only once.
        """
        subclass = self.__class__
        if debug_undoable_attrs:
            print "debug: running __declare_undoable_attrs in", subclass
        for attr in subclass.copyable_attrs:
            name = "_s_attr_" + attr
            if hasattr(subclass, name):
                if debug_undoable_attrs:
                    print " debug: not overwriting manual decl of %r as %r" % (name, getattr(subclass, name))
            else:
                setattr( subclass, name, S_DATA) # or S_REFS? If it needs to be S_CHILD, add an individual decl to override it.
        # prevent further runs on same subclass (in cooperation with the sole calling code)
        subclass.__declare_undoable_attrs = None # important to do this in subclass, not in self or Node
        return
        
    def set_disabled_by_user_choice(self, val): #bruce 050505 as part of fixing bug 593
        self.disabled_by_user_choice = val
        self.changed()

    def changed(self): #bruce 050505; not yet uniformly used (most code calls part.changed or assy.changed directly)
        """Call this whenever something in the node changes
        which would affect what gets written to an mmp file
        when the node gets written.
           Try to call it exactly when needed, since calling it
        when not needed leads to the user being told there are
        unsaved changes, and asked to confirm discards of the model
        upon loading a new one, even when there are no actual changes.
           But if you're not sure, calling it when not needed is better
        than not calling it when needed.
        """
        if self.part is not None:
            self.part.changed() #e someday we'll do self.changed which will do dad.changed....
        elif self.assy is not None:
            pass # not sure if it would be correct to call assy.changed in this case (when there's no part set) [bruce 060227 comment]
        return
    
    def is_group(self): #bruce 050216
        """Is self a Group node (i.e. an instance of Group or a subclass)?
        This is almost as deprecated as isinstance(self, Group),
        but not quite, since this would work if Utility was reloaded but that would not!
        (This doesn't yet matter in practice since there are probably other big obstacles
         to reloading Utility during debugging.)
        [overridden in Group]
        """
        return False # for a leaf node

    def readmmp_info_leaf_setitem( self, key, val, interp ): #bruce 050421, part of fixing bug 406
        """This is called when reading an mmp file, for each "info leaf" record
        which occurs right after this node is read and no other node has been read.
        (If this node is a group, we're called after it's closed, but groups should
        ignore this record.)
           Key is a list of words, val a string; the entire record format
        is presently [050421] "info leaf <key> = <val>".
        Interp is an object to help us translate references in <val>
        into other objects read from the same mmp file or referred to by it.
        See the calls of this method from files_mmp for the doc of interp methods.
           If key is recognized, set the attribute or property
        it refers to to val; otherwise do nothing (or for subclasses of Node
        which handle certain keys specially, call the same method in the superclass
        for other keys).
           (An unrecognized key, even if longer than any recognized key,
        is not an error. Someday it would be ok to warn about an mmp file
        containing unrecognized info records or keys, but not too verbosely
        (at most once per file per type of info).)
        """
        if self.is_group():
            if platform.atom_debug:
                print "atom_debug: mmp file error, ignored: a group got info leaf %r = ..." % (key,)
            return
        if key == ['hidden']:
            # val should be "True" or "False" (unrecognized vals are treated as False)
            val = (val == 'True')
            self.hidden = val
        elif key == ['disabled']: #bruce 050422
            # val should be "True" or "False" (unrecognized vals are treated as False)
            val = (val == 'True')
            self.disabled_by_user_choice = val
        elif key == ['forwarded']: #bruce 050422
            # this happens just after we read this leaf node (self) from an mmp file,
            # and means we should move it from where it was just placed (at the end of some Group still being read)
            # to a previous location indicated by val, and available via interp.
            interp.move_forwarded_node( self, val)
        else:
            if platform.atom_debug:
                print "atom_debug: fyi: info leaf (in Node) with unrecognized key %r (not an error)" % (key,)
        return
    
    def is_disabled(self): #bruce 050421 experiment related to bug 451-9 #e what Jig method does belongs here... [050505 comment]
        "Should this node look disabled when shown in model tree (but remain fully functional for selection)?"
        return False 
    
    def redmsg(self, msg): #bruce 050203; revised 050901 to work even after assy set to None in Node.kill
        from HistoryWidget import redmsg
        env.history.message( redmsg( msg ))

    def is_top_of_selection_group(self): #bruce 050131 for Alpha [#e rename is_selection_group?] [#e rename concept "selectable set"?]
        """Whether this node is the top of a "selection group".
        (This can be true of leaf nodes as well as group nodes, in spite of the name.)
        We enforce a rule that limits the selection to being entirely within
        one selection group at a time, since many operations on mixes
        of nodes from different selection groups are unsafe.
        [As of 050131, should be True of the PartGroup and any "clipboard item";
         this implem is not complete, so it's overridden by PartGroup.]
        """
        ###@@@ [General discussion of implem of selection groups, 050201:
        # in hindsight the implem should just store the selgroup
        # in each node, and maintain this when dad changes, like for .assy.
        # In fact, for Beta the selgroup probably *will* be the value of .assy,
        # which will be different for each clipboard item; or it might be a
        # separate field like .selgroup or .space or .part, depending on what
        # we end up calling "the part or any clipboard item, ie anything you
        # want to show in the glpane at once, and think of as being in one
        # physical space, where collisions and bonds are possible".]
        #
        # Following implem is correct for most nodes --
        # determine whether self is a "clipboard item".
        # [It could even work if we someday introduce "Groups of clipboard items".]
        # But it's wrong for PartGroup itself (thus is overridden by it).
        return self.dad and self.dad.is_selection_group_container()

    no_selgroup_is_ok = False
        #bruce 050612 class constant, could be overridden in some subclasses [not presently needed, but tested]
    
    def change_current_selgroup_to_include_self(self): #bruce 050131 for Alpha
        "#doc"
        # This might not be fast enough, so when there's time,
        # replace it with one that optims by stopping when dad is picked.
        foundselgroup, ours = self.find_selection_group_or_picked_dad()
        if not foundselgroup:
            # found a "picked dad"
            assert ours.picked
            return # no need to change (important optimization for recursive picking in groups)
        if ours is None:
            # this might happen for non-bugs since changed_dad calls it for picked nodes,
            # but it makes sense to skeptically review any way that can happen,
            # so the debug print is good even if it's not always a bug [bruce comment 050310]
            if self.no_selgroup_is_ok:
                return #bruce 050602
            if platform.atom_debug:
                print "atom_debug: bug(?): change_current_selgroup_to_include_self on node with no selgroup; ignored"
            return
        # ours is this node's selgroup, and might or might not already be the current one in self.assy
        prior = self.assy.current_selgroup_iff_valid() # might be None but otherwise is always valid; no side effects [revised 050310]
        if ours is not prior:
            self.assy.set_current_selgroup( ours)
                # this unpicks everything not in 'ours' and warns if it unpicked anything
        return

    def find_selection_group(self): #bruce 050131 for Alpha #####@@@@@ needs update/review for being called on deleted nodes; pass assy?
        """Return the selection group to which this node belongs, or None if none
        (as of 050131 that should happen only for Clipboard or Root).
        """
        node = self
        while node is not None:
            if node.is_top_of_selection_group():
                break
            node = node.dad # might be None; always is eventually, so loop always terminates by then
        return node # might be None

    def find_selection_group_or_picked_dad(self): #bruce 050131 for Alpha
        """Return (True, selgroup) where selgroup (maybe None) would be returned by find_selection_group,
        or (False, picked_dad) if you hit a "picked dad of self" (implying that self's selection group,
        whatever it is, is the current one, assuming no bugs in our new invariants).
        Prefer the picked_dad retval since it's faster.
        """
        node = self
        while node is not None:
            if node.is_top_of_selection_group():
                break
            node = node.dad # might be None; always is eventually, so loop always terminates by then
            if node is not None:
                # don't try this test for node is self, since it's not a "dad of self"
                if node.picked:
                    return False, node                
        return True, node # might be None
            
    def show_in_model_tree(self): #bruce 050127 ###e needs renaming, sounds like "scroll to make visible" [050310]
        #bruce 050417 warning: I think I never ended up honoring this. Not sure. #bruce 050527: It's not honored now, anyway.
        """Should this node be shown in the model tree widget?
        True for most nodes. Can be overridden by subclasses.
        [Added so that Datum Plane nodes won't be shown. Initially,
         it might not work much more generally than that.]
        """
        return True
    
    def haspicked(self): #bruce 050126
        """Whether node's subtree has any picked members.
        Faster than counting them with nodespicked or "maxing" them with hindmost,
        at least when anything is picked; just as slow when nothing is (still requires
        a full scan). [#e should we memoize hindmost data??]
        [overridden in Group, but this docstring applies to both methods together;
         should not be overridden elsewhere.]
        """
        return self.picked

    def permits_ungrouping(self): #bruce 050126 for Node; earlier for Group
        """[Leaf nodes can never (yet) be ungrouped. See Group.permits_ungrouping
        docstring for the general definition of this method.]
        """
        return False
    
    def kids(self, display_prefs): #bruce 050109
        """#doc; see Group.kids()
        [some subclasses should override this, especially Group]
        """
        return []
    
    def openable(self):
        """Say whether tree widgets should permit the user to open/close their view
        of this node (typically by displaying some sort of toggle icon for that state).
        (Note, if this is True then this does not specify whether the node view is
        initially open... #doc what does.)
        [Some subclasses should override this; if they add kids but don't
        override this, those kids will probably never be shown, but that might
        be undefined and depend on the model tree widget -- it's better to follow
        the rule of never having kids unless you are openable.]
        """
        # + If we decide this depends on the tree widget or on something about it,
        # we'll have to pass in some args... don't do that unless/until we need to.
        # + One reason we don't measure len(self.kids()) to decide on the default
        # value for this, is that some nodes might not want to compute self.kids()
        # until/unless it's needed, in case doing so is expensive. For example,
        # Qt's dirview example (also in PyQt examples3) computes kids only when
        # a node (representing a filesystem directory) is actually opened.
        return False

    ###e API and method/attr names related to "rename" needs review, since the text
    # shown by some nodes in a tree widget (in the future) might not be "their name".
    # [bruce 050128]
    
    def rename_enabled(self):
        """Should tree widgets permit the user to rename this node?
        (If so, they will call self.try_rename(newname) to actually request
        renaming for a specific new name.)
        [some subclasses should override this and/or try_rename]
        """
        return True

    def try_rename(self, name):
        """Given a new name for self, store it or reject it.
        Specifically, do one of these actions:
        - transform it into an acceptable name, store that in the node,
          do needed invals, and return (True, stored name);
        - or, reject it, and return (False, reason it's not ok).
          (The reason should be a string suitable for error messages.)
        """
        #e some of TreeWidget.slot_itemRenamed should be moved into a new caller of this in Node,
        # so other Qt widgets can also safely try to rename Nodes. [bruce 050527 comment]
        if not self.rename_enabled():
            return (False, "renaming this node is not permitted")
        #mark 051005 --  now name can be a python string or a QString
        try: 
            n = str(name)
        except:
            return (False, "illegal string")
        name = n.strip() # remove whitespace from both ends
        if not name:
            return (False, "blank name is not permitted")

        #bruce 050618 -- names containing ')' work now, so I can remove the ban on them in renaming.
##        if ')' in name and not permit_rparen_names:
##            #bruce 050508 bug-mitigation (these names can't yet be properly reloaded from mmp files)
##            return (False, "names containing ')' are not yet supported")
        
        # accept the new name.
##        self._um_will_change_attr('name') #bruce 051005; this might need to be called from a property-setter method for completeness
        self.name = name
        if self.assy:
            self.assy.changed()
        ###e should inval any observers (i.e. model tree) -- not yet needed, I think [bruce 050119]
        return (True, name)
        
    def drag_move_ok(self): # renamed/split from drag_enabled; docstring revised 050201
        """Say whether a drag_move which includes this node can be started (for "drag and drop").
        It's ok if only some drop-targets (nodes or inter-node gaps) can accept this node;
        we'll ask the targets if they'll take a specific drag_moved list of nodes (which includes this node).
           A tree widget asked to drag_move some selected nodes might filter them by drag_move_ok
        to get the ones to actually move, or it might refuse the whole operation unless all are ok to move --
        that's a UI decision, not a node semantics decision.
        [some subclasses should override this]
        """
        return True
        
    def drag_copy_ok(self): # renamed/split from drag_enabled; docstring revised 050201
        #bruce 050527 comment: this API needs revision, since the decision for jigs depends on what other nodes are included.
        # And we should revise it more, so we can construct a Copier object, let it "prep",
        # and use it for not only filtering out some nodes (like this does)
        # but getting the summary msg for the drag graphic, etc. #####@@@@@
        """Say whether a drag_copy which includes this node can be started (for "drag and drop").
        Same comments as for drag_move_ok apply.
        [some subclasses should override this]
        """
        return True
    
    def drop_on_ok(self, drag_type, nodes):
        """Say whether "drag and drop" can drop the given set of nodes onto this node,
        when they are dragged in the given way ('move' or 'copy' -- nodes arg has the originals).
        (Typically this node (if it says ok) would insert the moved or copied nodes inside itself
        as new members, but what it actually does with them is up to it;
        as an initial kluge before we support dropping into gaps (if we ever don't),
        dropping onto a leaf node might simulate dropping into the same-level gap below it
        (i.e. make a sibling, like addmember does).
        [some subclasses should override this]
        """
        #bruce 050216 add exception for cycle-forming request ###@@@ needs testing
        # (to fix bug 360 item 6 comment 9, which had been fixed in the old MT's DND code too)
        if drag_type == 'move':
            for node in nodes:
                if (node is not self and node.is_ascendant(self)) or (node is self and node.is_group()):
                    print "fyi: refusing drag-move since it would form a cycle"
                        #e should change retval-spec and get this into a redmsg
                    return False
        return True #e probably change to False for leaf nodes, once we support dropping into gaps

    def drop_on(self, drag_type, nodes): ###@@@ needs a big cleanup
        """After a "drag and drop" of type 'move' or 'copy' (according to drag_type),
        perform the drop of the given list of nodes onto this node.
        Exactly how to do this depends on whether this node is a leaf or group;
        subclasses can override this to change the UI behavior.
        (As of 050307, only the Clipboard override this.)
        Return value: if this operation creates new nodes
        (normal for copy, but also happens in some cases for move),
        return them in a list; otherwise return [].
        """
        #e rewrite to use copy_nodes (nim)? (also rewrite the assy methods? not for alpha)
        res = [] #bruce 050203: return any new nodes this creates (toplevel nodes only, for copied groups)
        #bruce 050216: order is correct if you're dropping on a group, but (for the ops used below)
        # wrong if you're dropping on a node. This needs a big cleanup, but for now, use this kluge
        # [revised to fix bug 2403 (most likely, this never worked as intended for copy until now), bruce 070525]:
        if not isinstance(self, Group):
            # drops on leaf nodes (like self) are placed after them,
            # when done by the methods named in the following flags,
            # so to drop several nodes in a row and preserve order,
            # drop them in reverse order -- but *when* we reverse them
            # (as well as which method we use) depends on whether we're
            # doing move or copy, so these flags are used in the right
            # place below.
            reverse_moveto = True
            reverse_addmember = True
        else:
            # drops on groups (like self) go at the end of their members,
            # when done by those methods, so *don't* reverse node order.
            #
            # [WARNING: this might change if we decide to put nodes dropped
            # on groups at the beginning of their members list. But implementing that
            # is not just a matter of changing these, but of calling different functions
            # to move or add the nodes. Also, a review might be needed to find other things
            # that need to be changed.]
            ## assert not debug_pref_DND_drop_at_start_of_groups()
            reverse_moveto = False
            reverse_addmember = False
            #bruce 060203 removing this, to implement one aspect of NFR 932:
            ## self.open = True # open groups which have nodes dropped on them [bruce 050528 new feature]
            pass
        if drag_type == 'move':
            if reverse_moveto:
                nodes = nodes[::-1]
            for node in nodes[:]:
                node.moveto(self)
        else:
            #bruce 050527 new code to "copy anything". Preliminary (probably not enough history messages, or maybe sometimes
            # too many). Would be better to create the Copier object (done in a subr here) earlier, when the drag is started,
            # for various reasons mentioned elsewhere.
            from ops_copy import copied_nodes_for_DND
            autogroup_at_top = isinstance(self, ClipboardShelfGroup)
                #####@@@@@ kluge! replace with per-group variable or func.
                #e or perhaps better, a per-group method to process the nodes list, eg to do the grouping
                # as the comment in copied_nodes_for_DND or its subr suggests.
            nodes = copied_nodes_for_DND(nodes, autogroup_at_top = autogroup_at_top)
                # Note: this ignores order within input list of nodes, using only their MT order
                # to affect the order of copied nodes which it returns. [bruce 070525 comment]
            if not nodes: # might be None
                return [] # return copied nodes
            res.extend(nodes)
            if reverse_addmember:
                nodes = nodes[::-1]
                    # note: if autogroup_at_top makes len(nodes) == 1, this has no effect,
                    # but it's harmless then, and logically best to do it whenever using
                    # addmember on list elements.
            for nc in nodes[:]:
                self.addmember(nc) # self is sometimes a Group, so this does need to be addmember (not addchild or addsibling)
        self.assy.update_parts() #e could be optimized to scan only what's needed (same for most other calls of update_parts)
        return res

    # Note: the methods drop_under_ok and drop_under are never called
    # (and drop_under is not fully implemented, as its comments indicate),
    # but they should be kept around -- they are a partly-done implementation
    # of a Node API extension to support Model Tree DND to points between nodes
    # (as opposed to DND to points on top of single nodes, which is all the MT
    #  can do now). [bruce 050203/070703]

    def drop_under_ok(self, drag_type, nodes, after = None): ###@@@ honor it!
        """Say whether it's ok to drag these nodes (using drag_type)
        into a child-position under self,
        either after the given child 'after'
        or (by default) as the new first child.
           Tree widgets can use this to offer drop-points shown in gaps
        between existing adjacent nodes.
        [some subclasses should override this]
        """
        return hasattr(self, 'addchild') # i.e. whether it's a Group!

    # See comment above for status of unused method 'drop_under', which should be kept around. [bruce 070703]
    def drop_under(self, drag_type, nodes, after = None): #e move to Group, implem subrs, use ###@@@
        "#doc"
        if drag_type == 'copy':
            from ops_copy import copy_nodes_in_order # might be recursive if done at toplevel
            nodes = copy_nodes_in_order(nodes) # make a homeless copy of the set (someday preserving inter-node bonds, etc)
        for node in nodes:
            self.addchildren(nodes, after = after) ###@@@ IMPLEM (and make it not matter if they are homeless? for addchild)
        return

    def node_icon(self, display_prefs):
        """#doc this - should return a cached icon
        [all Node subclasses should override this]
        """
        try:
            return self.const_pixmap # let simple nodes just set this in __init__ and be done with it [bruce 060523]
        except:
            msg = "bug - Node subclass %s forgot to override node_icon method or set self.const_pixmap" % self.__class__.__name__
            fake_filename = msg
            return imagename_to_pixmap( fake_filename)
                # should print msg, at most once per class
                # (some people might consider this a kluge)
        pass
    
    # most methods before this are by bruce [050108 or later] and should be reviewed when my rewrite is done ###@@@

    def addsibling(self, node, before = False):
        """Add the given node after (default) or before self, in self's Group.
        Node should not already be in any Group, since it is not removed from one.
        (Some existing code violates this; this is probably ok if node's old Group
        is never again used, but that practice should be deprecated, and then
        this method should detect the error of node.dad already being set,
        or perhaps be extended to remove node from its dad.)
        [Special case: legal and no effect if node is self. But this should be
        made into an error, since it violates the rule that node is not presently
        in any Group!]
        [It is unlikely that any subclass should override this, since its
        semantics should not depend on anything about self, only (perhaps)
        on things about its Group, i.e. self.dad.]
        [Before bruce 050113 this was called Node.addmember, but it had different
        semantics from Group.addmember, so I split that into two methods.]
        """
        if node is self:
            # bruce comment 010510: looks like an error, and not nearly the
            # only one possible... maybe we should detect more errors too,
            # and either work around them (as this does) or report them.
            #bruce comment 050216: probably no longer needed since probably done in addchild
            return
        if before:
            self.dad.addchild( node, before = self) # Insert node before self
        else:
            self.dad.addchild( node, after = self) # Insert node after self
        return
    
    def addmember(self, node, before_or_top = False):
        """[Deprecated public method:]
           Like addsibling or addchild, depending on whether self is
        a leaf node or a Group. (Also misnamed, since a sibling is not a member.)
           Any call to addmember whose node is known to be always a Group
        can be replaced with addchild (default option values are compatible),
        except that if a named option is supplied, it must be renamed.
           Any call whose node is *never* a Group can be changed to addsibling.
           Any call whose node is sometimes a Group and sometimes not might need
        to call this method, or might have a bug because it does, if the calling
        code was written with the wrong assumption about node's Groupness!
          [We might un-deprecate this by redefining it as what to do when you drop
        node onto self during drag-and-drop, but really that should be its own
        separate method, even if it's pretty similar to this one. This is one is
        used by a lot of old code as if it was always one or the other of the
        two methods it can call! This was sometimes justified but in other cases
        was wrong and caused bugs.]
        """
        if isinstance(self, Group):
            # (use isinstance (rather than overriding in a subclass)
            #  to emphasize the reason this method needs to be deprecated!)
            self.addchild( node, top = before_or_top)
        else:
            # for a leaf node, add it to the dad node just after us
            self.addsibling( node, before = before_or_top)
        return

    def genvisibleleaves(self, include_parents = False): #bruce 060220
        """Assuming self is visible in the MT (ignoring scrolling), return a generator which yields
        the set of self and/or its children which have no visible children (i.e. which are leaf nodes,
        or empty Group nodes (good??), or closed Group nodes).
           By default, skip anything which has children we'll yield, but if include_parents is True,
        include them anyway.
        [Note that this uses .open which might be considered model-tree-specific
        state -- if we ever let two MTs show the model hierarchy at once, this will need an argument
        which is the openness-dict, or need to become an MT method.]
        """
        if self.is_group() and self.open and self.members:
            if include_parents:
                yield self
                #e Do we want another option, for yielding parents before vs. after their kids?
                # I don't yet know of a use for it ('before' is what we want for MT arrow keys,
                # whether moving up or down, since for 'up' we reverse this entire sequence). 
            for m in self.members:
                for s in m.genvisibleleaves(include_parents = include_parents):
                    yield s
        else:
            yield self
        return
    
    def pick(self):
        """select the object
        [extended in many subclasses, notably in Group]
        [Note: only Node methods should directly alter self.picked,
         since in the future these methods will sometimes invalidate other state
         which needs to depend on which Nodes are picked.]
        """
        ###@@@ I don't know whether that new rule is yet followed by external code [bruce 050124].
        #bruce 050131 for Alpha: I tried to make sure it is; at least it's now followed in "pick" methods.
        if not self.picked:
            self.picked = True
            # bruce 050125: should we also call self.assy.permit_picked_parts() here? ###@@@ [not just in chunk.pick]
            #bruce 050131 for Alpha: I'm guessing we don't need to, for jigs or groups,
            # since they don't get into assy.molecules or selmols.
            # Whether doing it anyway would be good or bad, I don't know,
            # so no change for now.
            self.changed_selection() #bruce 060227
            self.change_current_selgroup_to_include_self()
                # note: stops at a picked dad, so should be fast enough during recursive use
        # we no longer call mode.UpdateDashboard() from here;
        # clipboard selection no longer affects Build mode dashboard. [bruce 050124]

    def unpick(self):
        """unselect the object, and all its ancestor nodes.
        [extended in many subclasses, notably in Group]
        [Note: only Node methods should directly alter self.picked,
         since in the future these methods will sometimes invalidate other state
         which needs to depend on which Nodes are picked.]
        """
        ###@@@ I don't know whether that new rule is yet followed by external code [bruce 050124].
        if self.picked:
            self.picked = False
            self.changed_selection() #bruce 060227
        # bruce 050126 change: also set *all its ancestors* to be unpicked.
        # this is required to strictly enforce the rule
        # "selected groupnode implies all selected members".
        # We'd do this inside the 'if' -- but only once we're sure all other code
        # no longer bypasses this method and sets node.picked = False directly;
        # this way, if that happens, we might happen to fix up the situation later.
        if self.dad and self.dad.picked:
            self.dad.unpick_top() # use the method, in case a Group subclass overrides it

    def changed_selection(self): #bruce 060227
        "Record the fact that the selection state of self or its contents (Group members or Chunk atoms) might have changed."
        if self.assy is not None:
            self.assy.changed_selection()
        return
    
    def unpick_all_except(self, node):
        """unpick all of self and its subtree except whatever is inside node and its subtree;
        return value says whether anything was actually unpicked
        """
        # this implem should work for Groups too, since self.unpick does.
        if self is node:
            return False
        res = self.picked # since no retval from unpick_top; this is a correct one if our invariants are always true
        self.unpick_top()
        res2 = self.unpick_all_members_except( node)
        # btw, during recursive use of this method,
        # unpick_top (either the Node or Group implem)
        # will see self.dad is not picked
        # and not need to keep calling unpick_top
        return res or res2

    def unpick_all_members_except(self, node):
        "[#doc; overridden in Group] return value says whether anything was actually unpicked"
        return False
    
    def pick_top(self): #bruce 050124
        #e ###@@@ needs fixing or zapping, because:
        # as of 050131, this is: illegal (since it violates an invariant),
        # incorrectly implemented (since it doesn't do leaf-specific pick funcs,
        # though this could probably be easily fixed just as I'll fix unpick_top),
        # and never called (since sole caller's group_select_kids is always True).
        """select the object -- but (unlike Group.pick) don't change selection state
        of its members. Note that this violates the principle "selected groupnode
        implies all selected members". This means it should be used either never
        or rarely (as of 050126 I don't know which).
        [unlike pick, this is generally NOT extended in subclasses]
        """
        Node.pick(self)

    def unpick_top(self): #bruce 050124 #bruce 050131 making it correct for chunk and jig
        """unselect the object -- but (unlike Group.unpick) don't change
        the selection state of its members. But do unselect all its ancestor nodes.
        [unlike unpick, this is generally NOT extended in subclasses, except in Group.]
        """
        # this implem is only correct for leaf nodes:
        self.unpick() # before 050131 was Node.unpick(self), which was wrong for chunk and jig.

    _old_dad = None ###k not yet used? #####@@@@@ review got to here, except: to chgdad added only cmts plus docstring plus new name

    def in_clipboard(self): #bruce 050205 temporary ###@@@ [should use a more general concept of assy.space]
        """For a leaf node: Are we definitely inside some clipboard item?
        For a Group node: Would new members added to us be, or be inside, a clipboard item?
        (I.e., in both cases, are we the Clipboard or in its tree?)
        [This only works as long as self.assy.shelf is the Clipboard and works like it does now, 050205.
         It's only useful as long as the rest of the code has special cases for clipboard vs main part --
         hopefully not for much longer. In other words, this method is "deprecated at birth".]
        """
        try:
            return self.assy.shelf.is_ascendant(self)
        except:
            return False # assume not, if e.g. we have no assy, it has no shelf, etc
    
    def changed_dad(self):
        """[private method]
        Must be called after self.dad might have changed, before again exposing
        modified node to the public. Keeps some things up to date continuously;
        records info to permit updating other things later.
        """
        node = self
        ## from changes import changed #bruce 050303, removed 050909
        ## not needed as of 050309:
        ## changed.dads.record(node) # make sure node's Part will be updated later if needed [bruce 050303]
        assert node.dad is not None #k not sure if good to need this, but seems to fit existing calls... that might change [050205 comment]
            #e if no dad: assy, space, selgroup is None.... or maybe keep prior ones around until new real dad, not sure
        assert node.assy is node.dad.assy or node.assy is None
            # bruce 050308, since following assy code & part code has no provision yet for coexisting assemblies
        node.assy = node.dad.assy # this might change soon, or might not... but if it's valid at all, it needs to be propogated down!
            # we leave it like this for now only in case it's ever being used to init the assy field from None.
        #bruce 050308: continually let assigned node.dad.part get inherited by unassigned node.part (recursively)
        if node.dad.part is not None:
            if node.part is None:
                # note, this is the usual way that newly made nodes acquire their .part for the first time!
                # they might be this node or one of its kids (if they were added to a homeless Group, which is this node).
                node.inherit_part(node.dad.part) # recurses only into kids with no .parts
        else:
            #bruce 050527 new feature: dad can also inherit from kid, but only prior_part
            if node.dad.prior_part is None: # as well as node.dad.part, already checked
                node.copy_prior_part_to(node.dad)
        if node.picked:
            # bruce 050131 for Alpha:
            # worry about whether node is in a different selection group than before;
            # don't know if this ever happens, but let's try to cooperate if it does:
            node.change_current_selgroup_to_include_self()
                # note: this has no effect if node doesn't have a selgroup
        if node.dad.picked:
            node.pick() #bruce 050126 - maintain the new invariant! (two methods need this)
            # warning: this might make some callers need to update glpane who didn't need to before.
            # possible bugs from this are not yet analyzed.
            # Note 050206: the clipboard can't be selected, and if it could be, our invariants would be inconsistent
            # if it had more than one item! (Since all items would be selected but only one selgroup should be.)
            # So, this line never picks a clipboard item as a whole.
        return

    def inherit_part(self, part): #bruce 050308
        "#doc (see Group method docstring) [overridden in Group]"
        # this implem is sufficient only for leaf nodes
        assert self.part is None
        part.add(self)
        assert self.part is part
    
    def hide(self):
        if not self.hidden:
            self.changed() #bruce 050512 part of fixing bug 614
        self.hidden = True
        self.unpick()
        
    def Hide(self): # called from a node's (Jig) "Hide" context menu item (in the GLPane, not MT). mark 060312.
        '''Hide self and update the mt and glpane.
        '''
        self.hide()
        if self is self.assy.o.selobj:
            # Without this, self will remain highlighted until the mouse moves.
            self.assy.o.selobj = None ###e shouldn't we use set_selobj instead?? [bruce 060726 question]
        self.assy.w.win_update()
        
    def unhide(self):
        if self.hidden:
            self.changed() #bruce 050512 part of fixing bug 614
        self.hidden = False

    def apply2all(self, fn):
        """Apply fn to self and (as overridden in Group) all its members;
        see Group.apply2all docstring for details.
        """
        fn(self)

    def apply2tree(self, fn): ###@@@ should rename (both defs)
        """Like apply2all, but only applies fn to all Group nodes (at or under self)."""
        pass

    def apply2picked(self, fn):
        """Apply fn to the topmost picked nodes under (or equal to) self,
        but don't scan below picked nodes. See Group.apply2picked docstring for details.
        """
        if self.picked: fn(self)

    def hindmost(self):
        """[docstring is meant for both Node and Group methods taken together:]
        Thinking of nodes as subtrees of the model tree, return the smallest
        subtree of self which contains all picked nodes in this subtree, or None
        if there are no picked nodes in this subtree. Note that the result does
        not depend on the order of traversal of the members of a Group.
        """
        if self.picked: 
            return self
        return None

    def ungroup(self):
        """If this Node is a Group, dissolve it, letting its members
        join its dad, if this is possible and if it's permitted as a
        user-requested operation. See our Group implem for details.
        """
        #bruce 050121 inferred docstring from 2 implems and 1 call
        return

    # == copy methods -- by default, Nodes can't be copied, but all copyable Node subclasses
    # == should override these methods.

    def will_copy_if_selected(self, sel, realCopy): #bruce 050525; wware 060329 added realCopy arg
        """Will this node copy itself when asked (via copy_in_mapping or postcopy_in_mapping [#doc which one!])
        because it's selected in sel, which is being copied as a whole?
        [Node types which implement an appropriate copy method should override this method.]
        If the realCopy boolean is set (indicating this is a real copy operation and not
        just a test), and if this node will not copy, it may want to print a warning.
        """
        if realCopy:
            #bruce 060329 added this default message, since it's correct if the whole realCopy scheme is,
            # though I'm dubious about the whole scheme.
            msg = "Node [%s] won't be copied." % (self.name)
            from HistoryWidget import orangemsg
            env.history.message(orangemsg(msg))
        return False # conservative answer

    def will_partly_copy_due_to_selatoms(self, sel): #bruce 050525; docstring revised 050704
        """For nodes which say True to .confers_properties_on(atom) for one or more atoms
        which are part of a selection being copied, but when this node is not selected,
        will it nonetheless copy all or part of itself, when its copy_partial_in_mapping
        method is called, so that the copied atoms still have the property it confers?
        [Node types which implement an appropriate copy method should override this method too.]
        """
        return False # conservative answer

    def confers_properties_on(self, atom): #bruce 050524; docstring revised 050704, 070608
        """Does this Jig (or any node of a type that might appear in atom.jigs)
        confer a property on atom, so that it should be partly copied, if possible
        (by self.copy_partial_in_mapping) when atom is?
           Note: only Anchor overrides this (as of 070608), and the only new kinds
        of Nodes that might need to override it would be Jigs designed to alter the
        rendering or simulation properties of all their atoms, as a substitute for
        directly storing those properties on the atoms. If in doubt, don't override it.
        """
        return False # default value for most jigs and (for now) all other Nodes
        
    def copy_full_in_mapping(self, mapping): # Node method [bruce 050526]
        """
        If self can be fully copied, this method (as overridden in self's subclass) should do so,
        recording in mapping how self and all its components (eg chunk atoms, group members) get copied,
        and returning the copy of self, which must be created in mapping.assy (which may differ from self.assy).
           If self will refuse to be fully copied, this method should return None.
        ###k does it need to record that in mapping, too?? not for now.
           It can assume self and all its components have not been copied yet (except for shared components like bonds #k #doc).
        It can leave out some mapping records for components, if it knows nothing will need to know them
        (e.g. atoms only need them regarding some bonds and jigs).
           For references to things which might not have been copied yet, or might never be copied (e.g. atom refs in jigs),
        this method can make an incomplete copy and record a method in mapping to fix it up at the end. But it must decide
        now whether self will agree or refuse to be copied (using mapping.sel if necessary to know what is being copied in all).
           [All copyable subclasses should override this method.]
        """
        return None # conservative version

    copy_partial_in_mapping = copy_full_in_mapping # equivalent for all jigs which need it, as of 050526 [method name added 050704]
        # Note (bruce 060523): this might be wrong for jigs that overrode copy_full_in_mapping,
        # but since copy_partial_in_mapping is not presently called, I won't bother to clean it up for now.

    def copy_in_mapping_with_specified_atoms(self, mapping, atoms): #bruce circa 050525; docstring revised 050704
        "#doc; must honor mapping.assy; certain subclasses should override [e.g. chunk]; for use in copying selected atoms"
        return None

    def copy_copyable_attrs_to(self, target, own_mutable_state = True): #bruce 050526; behavior and docstring revised 051003
        """Copy all copyable attrs (as defined by a typically-subclass-specific constant tuple, self.copyable_attrs)
        from self to target (presumably a Node of the same subclass, but this is not checked,
        and violating it might not be an error, in principle; in particular, as of 051003 target is explicitly permitted
        to be a methodless attribute-holder).
           Target and self need not be in the same assy (i.e. need not have the same .assy attribute),
        and when this situation occurs, it must not be disturbed (e.g. setting target.assy = self.assy would be a bug).
        Doesn't do any invals or updates in target.
           This is not intended to be a full copy of self, since copyable_attrs (in current client code)
        should not contain object-valued attrs like Group.members, Node.dad, or Chunk.atoms, but only
        "parameter-like" attributes. It's meant to be used as a helper function for making full or partial copies
        of self, and related purposes. The exact set of attributes to include can be chosen somewhat
        arbitrarily by each subclass, but any which are left out will have to be handled separately by the copy methods;
        in practice, new attributes in subclasses should almost always be declared in copyable_attrs.
           As of 051003, this method (implem and spec) has been extended to "deep copy" any mutable objects
        found in attribute values (of the standard kinds defined by state_utils.copy_val), so that no
        mutable state is shared between copies and originals. This can be turned off by passing own_mutable_state = False,
        which is a useful optimization if serial copies are made and intermediate copies won't be kept.
           This is intended as a private helper method for subclass-specific copy methods,
        which may need to do further work to make these attribute-copies fully correct --
        for example, modifying the values of id- or (perhaps) name-like attributes,
        or doing appropriate invals or updates in target.
        """
        for attr in self.copyable_attrs:
            assert attr != 'assy' #e could optim by doing this once per class or once per instance
            val = getattr(self, attr)
            if own_mutable_state:
                val = copy_val(val)
            setattr(target, attr, val) # turns some default class attrs into unneeded instance attrs (nevermind for now)
        if isinstance(target, Node):
            # don't do this for non-Nodes, to permit target being just a methodless attribute-holder [new feature, bruce 051003]
            self.copy_prior_part_to( target)
        return

    def copyable_attrs_dict(self):
        """Returns a new dictionary containing copied values of attributes
        listed in self.copyable_attrs.
        """
        res = {}
        for attr in self.copyable_attrs:
            val = getattr(self, attr)
            val = copy_val(val)
            res[attr] = val
        return res
        
    def attr_update(self, dict1):
        """Updates the attribute values from dict1 to self
        """
        for attr, val in dict1.iteritems():
            setattr(self, attr, val)

    def copy_prior_part_to(self, target): #bruce 050527
        """If target (presumed to be a Node) has no part or prior_part, set its prior_part from self,
        for sake of initial views of new Parts containing target, if any such new Parts are yet to be made.
        """
        if target.part is None and target.prior_part is None:
            if self.part is not None:
                target.prior_part = self.part
            else:
                target.prior_part = self.prior_part
        return

    def own_mutable_copyable_attrs(self):
        #bruce 051003 revision: now that copy_copyable_attrs_to deepcopies mutable parameter values,
        # this method will only need overriding for mutable state of types that method can't handle
        # or which for some other reason is not declared in self.copyable_attrs.
        ##e note: docstring and perhaps method name should be changed; most calls should remain,
        # but all overridings of this method (and/or related decls of mutable_attrs) should be reviewed for removal.
        # [as of 060523, the only override is in jig_Gamess.py, and it could probably be removed but that requires analysis.]
        """[this docstring is out of date as of 051003]
        If any copyable_attrs of self are mutable and might be shared with another copy of self
        (by self.copy_copyable_attrs_to(target) -- where this method might then be called on self or target or both),
        replace them with copies so that they are no longer shared and can safely be independently changed.
        [some subclasses must extend this]
        """
        pass
    
    def copy(self, dad): # just for backwards compatibility until old code is changed [050527]
        self.redmsg("This cannot yet be copied")
        if platform.atom_debug:
            print_compact_stack("atom_debug: who's still calling this deprecated method? this is:\n ")
        return None # bruce 050131 changed this from "return 0"
    
    # ==
    
    def kill(self): # see also self.destroy()
        """Remove self from its parents and (maybe) destroy enough of its content that it takes little room (but be Undoable).
        [subclasses should extend this, but should call this Node method at the end of their own kill methods]
        """
        ###@@@ bruce 050214 changes and comments:
        #e needs docstring;
        #  as of now, intended to be called at end (not start middle or never) of all subclass kill methods
        #  ok to call twice on a node (i.e. to call on an already-killed node); subclass methods should preserve this property
        # also modified the Group.kill method, which extends this method
##        self._prekill() #bruce 060327 ##k not positive this is needed in Node (rather than just Group and Chunk being enough)
##        ###@@@ defect in this (important): jigs dying due to one or all their atoms dying will run this and mess up the counter.
        self.remove_from_parents()
    
    _will_kill = 0

    def _prekill(self): #bruce 060327 in Node (mainly to speed up Delete of chunks, also (short term purpose) to reduce memory leaks)
        """[private helper method for Node.kill and its subclass implems]
        Set self._will_kill = ++ _will_kill_count on self, all child nodes, and all other owned subobjects that self.kill() would kill,
        but only when it's not already set on self (to avoid exponential runtime in Node tree depth, when recursive kill calls this),
        and only on Node classes which might own objects which need it (currently Atoms and maybe Bonds and conceivably Parts).
           This flag tells Atoms being killed not to create new bondpoints on their neighbors when those are also being killed,
        which is a big optimization. It can do other similar things if we discover them -- in general, it means "I'm also being
        killed so don't spend lots of time healing my wounds when you're being killed".
           Note: Undo will revive killed objects, so kill needs to remove this flag from them when it returns,
        and Undo might assert that it's not set on revived objects.
           Note: We increment a counter when setting this, so as not to have to worry about whether leftover sets of it
        will cause trouble. This might make some of what's said above (about unsetting it) unnecessary.
        [subclasses should not extend this, but should extend _set_will_kill instead; at least Group and Chunk need to do that]
        """    
        global _will_kill_count
        if self._will_kill < _will_kill_count:
            _will_kill_count += 1
            self._set_will_kill( _will_kill_count) # sets it to this value (with no checks) on self, children, atoms
        return

    def _set_will_kill(self, val): #bruce 060327 in Node
        "[private helper method for _prekill; see its docstring for details; subclasses with owned objects should extend this]"
        self._will_kill = val
    
    glname = 0 # required class constant in case of repeated calls of self.destroy() #bruce 060322

    def destroy(self):
        "delete cyclic refs (so python refdecr can free self) and refs to large RAM-consuming attrs; and more [#doc, see code comments]"
        self.kill() #bruce 060117 guess at implem
        #bruce 060117 draft, experimental, not yet widely used; obs comment: not sure if it should differ from kill [but see below]
        #bruce 060322 comments:
        # Bugs: arbitrary-order calls (vs other obj destroy methods) are probably not yet safe
        # (for planned future calls of this method, to plug memory leaks).
        # Note: a potential difference of destroy from kill -- after kill, a Node might be revived by Undo;
        # after destroy, it won't be. Things like its entry in various global dicts for change-tracking, glname, undo objkey, etc,
        # should either be weak or should be explicitly removed by destroy. This is nim, but is important for plugging memory leaks.
        # These comments apply to the destroy methods of all model objects and their child or helper objects, not only to Nodes.
        # ###@@@ #e
        #
        # We want this dealloc_my_glselect_name, but first we have to review all calls to Node.destroy
        # to verify it's not called when it shouldn't be (e.g. when that node might still be revived by Undo). ###@@@
        # BTW, as of 060322 the appropriate init, alloc, and draw code for glname is only done (or needed) in Jig.

        ## env.dealloc_my_glselect_name( self, self.glname )

        ##e more is needed too... see Atom and Bond methods
        # do we want this:
        ## self.__dict__.clear() ###k is this safe???
        return

    def remove_from_parents(self): #bruce 051227 split this out of Node.kill for use in new Node.setAssy
        "Remove self from its parents of various kinds (part, dad, assy, selection) without otherwise altering it."
        ###@@@ bruce 050214 changes and comments:
        # added condition on self.dad existing, before delmember
        # added unpick (*after* dad.delmember)
        # added self.assy = None
##        self._um_deinit() #bruce 051005 #k this is not good enough unless this is always called when a node is lost from the MT!
        if self.dad:
            self.dad.delmember(self)
                # this does assy.changed (if assy), dad = None, and unpick,
                # but the unpick might be removed someday, so we do it below too
                # [bruce 050214]
        self.unpick() # must come after delmember (else would unpick dad) and before forgetting self.assy
        self.reset_subtree_part_assy()

    def reset_subtree_part_assy(self): #bruce 051227 split this out
        """Cleanly reset self.part and self.assy to None, in self and its node-subtree
        (removing self and kids from those containers in whatever ways are needed).
        Assume self is not picked.
        [Subclasses (especially Group) must extend this as needed.]
        """
        assert not self.picked
        if self.part: #bruce 050303; bruce 051227 moved from start of routine (before delmember) to here (after unpick), not sure ok
            self.part.remove(self)
        env.node_departing_assy(self, self.assy) #bruce 060315 for Undo
        self.assy = None #bruce 050214 added this ###k review more
            #bruce 060315 comments about this old code:
            # reasons to set assy to None:
            # - helps avoid cycles when destroying Nodes
            # - logical part of setAssy (but could wait til new assy is stored)
            # reasons not to:
            # - Undo-tracked changes might like to use it to find the right AssyUndoArchive to tell about the change
            #   (can we fix that by telling it right now? Not sure... in theory, more than one assy could claim it if we Undo in some!)
            # - we might avoid needing to scan it and store it as undoable state
            # - some bugs are caused by code that tries to find win, glpane, etc from assy
            # tentative conclusion:
            # - don't stop doing this for A7
            # - but tell Undo about the change, as part of letting it know which atoms are changing
            #   (namely, all those still in this Node, if it's a chunk -- perhaps this will usually be no atoms?);
            #   other changes on atoms can safely only tell the assy they refer to (via atom.molecule.assy) (or no assy if that's None).

    def is_ascendant(self, node): # implem corrected by bruce 050121; was "return None"
        """Is node in the subtree of nodes headed by self?
        [Optimization of Group.is_ascendant for leaf nodes; see its docstring for more info.]
        """
        return self is node # only correct for self being a leaf node

    def moveto(self, node, before=False): #e should be renamed for d&d, and cleaned up; has several external calls
        """Move self to a new location in the model tree, before or after node,
        or if node is a Group, somewhere inside it (reinterpreting 'before' flag
        as 'top' flag, to decide where inside it). Special case: if self is node,
        return with no effect (even if node is a Group).
        """
        #bruce 050110 updated docstring to fit current code.
        # (Note that this makes it even more clear, beyond what's said in addmember
        #  docstrings, that addmember interface mixes two things that ought to be
        #  separated.)
        
        #bruce 050205 change: just go directly to addmember, after my addchild upgrades today.
        # note, this 'before' is a positional arg for the before_or_top flag,
        # not the named arg 'before' of addchild! Btw we *do* need to call addmember
        # (with its dual personality dependending on node being leaf or not)
        # for now, while DND uses drop_on groups to mean drop_under them.
        node.addmember(self, before_or_top = before) # this needs to be addmember, not addchild or addsibling

    def nodespicked(self):
        """Return the number of nodes currently selected in this subtree.
        [subclasses must override this!]
        Warning (about current subclass implementations [050113]):
        scans the entire tree... calling this on every node in the tree
        might be slow (every node scanned as many times as it is deep in the tree).
        """
        if self.picked:
            return 1 # number, not boolean!
        else:
            return 0

    def edit(self): #e should be renamed to edit_props (in several files)
        """[should be overridden in most subclasses]
        If this kind of Node has properties that can be edited
        with some sort of interactive dialog, do that
        (put up the dialog, wait for user to dismiss it, change the properties
        as requested, and do all needed invals or updates),
        and then return None (regardless of Cancel, Apply, Revert, etc).
           If this kind of Node *doesn't* support editing of properties,
        return a suitable text string for use in an error message.
        """
        #bruce 050121 inferred docstring from all 7 implems and 1 call.
        # Also added feature of refusing and returning error message, used in 2 implems so far.
        #bruce 050425 revised this error message.
        return "Edit Properties is not available for %s." % self.__class__.__name__

    def edit_props_enabled(self): #bruce 050121 added this feature
        """Subclasses should override this and make it return False
        if their edit method would refuse to put up an editing dialog.
        """
        # i don't know if they all do that yet...
        #e should we check here to see if they override Node.edit?? nah.
        return True # wrong for an abstract Node, but there is no such thing!
    
    def dumptree(self, depth=0):
        print depth*"...", self.name

    def node_must_follow_what_nodes(self): #bruce 050422 made Node and Jig implems of this from function of same name
        """[should be overridden by Jig]
        If this node is a leaf node which must come after some other leaf nodes
        due to limitations in the mmp file format, then return a list of those nodes
        it must follow; otherwise return []. For all Groups, return [].
        If we upgrade the mmp file format to permit forward refs to atoms,
        then this function could return [] for all nodes
        (unless by then there are nodes needing prior-refs to things other than atoms).
        """
        return []

    def writemmp(self, mapping): #bruce 050322 revised interface to use mapping
        """Write this Node to an mmp file, as controlled by mapping,
        which should be an instance of files_mmp.writemmp_mapping.
        [subclasses must override this to be written into an mmp file;
         we print a debug warning if they don't.]
        """
        # bruce 050322 revising this; this implem used to be the normal way
        # to write Jigs; now it's basically an error to call this implem,
        # but it's harmless -- it puts a comment in the mmp file and prints a debug warning.
        line = "# not yet implemented: mmp record for %r" % self.__class__.__name__
        mapping.write(line + '\n')
        if platform.atom_debug:
            print "atom_debug:", line
        return

    def writemmp_info_leaf(self, mapping): #bruce 050421
        """leaf node subclasses should call this in their writemmp methods,
        after writing enough that the mmp file reader will have created a Node for them
        and added it to its current group (at the end is always safe, if they write no sub-nodes)
        [could be overridden by subclasses with more kinds of "info leaf" keys to write]
        """
        assert not self.is_group()
        if self.hidden:
            mapping.write("info leaf hidden = True\n")
        if self.disabled_by_user_choice: # [bruce 050505 revised this so all Nodes have the attribute, tho so far only Jigs use it]
            mapping.write("info leaf disabled = True\n") #bruce 050422
        return
        
    def writemdl(self, alist, f, dispdef): #bruce 050430 added Node default method to fix bug reported by Ninad for A5
        pass

    def writepov(self, file, dispdef): #bruce 050208 added Node default method
        pass

    def draw(self, glpane, dispdef):
        pass
    
    def draw_in_abs_coords(self, glpane, color): #bruce 050729 to fix some bugs caused by Huaicai's jig-selection code
        """Default implementation of draw_in_abs_coords. Some implem is needed by any nodes or other drawable objects
        which get registered with env.alloc_my_glselect_name. [#doc the API]
        [Subclasses which are able to use color for highlighting in Build mode,
         or which want to look different when highlighted in Build mode,
         or which are ever drawn in non-absolute modelview coordinates,
         or for which glpane.displayMode is not what would be passed to their draw method,
         should override this method.]
        """
        dispdef = glpane.displayMode
        del color
        self.draw(glpane, dispdef)
        return

    def killed(self): #bruce 050729 to fix some bugs caused by Huaicai's jig-selection code
        alive = self.dad is not None and self.assy is not None
        return not alive # probably not correct, but should be good enough for now
    
    def getinfo(self):
        pass

    def init_statistics(self, stats):
        'Initialize statistics for this Node'
        # Currently, this is only used by "part" and "group" nodes.
        # See PartProp.__init__() or GroupProp.__init__().
        # Mark 050911.
        stats.nchunks = 0
        stats.natoms = 0
        stats.nsinglets = 0
        stats.nrmotors = 0
        stats.nlmotors = 0
        stats.nanchors = 0
        stats.nstats = 0
        stats.nthermos = 0
        stats.ngamess = 0
        stats.num_espimage = 0
        stats.num_gridplane = 0
        stats.num_mdistance = 0
        stats.num_mangle = 0
        stats.num_mdihedral = 0
        stats.ngroups = -1 # Must subtract self.
        
    def getstatistics(self, stats):
        pass

    def break_interpart_bonds(self): #bruce 050308 for assy/part split, and to fix bug 371 and related bugs for Jigs
        """Break all illegal bonds (atom-atom or atom-Jig or (in future) anything similar)
        between this node and other nodes in a different Part.
        [Note that as of 050513 and earlier, all atom-Jig interpart bonds are permitted; but we let the Jig decide that.] 
        Error if this node or nodes it bonds to have no .part.
        Subclasses with bonds must override this method as appropriate.
           It's ok if some kinds of nodes do this more fancily than mere "breakage",
        e.g. if some Jigs break into pieces so they can keep connecting
        to the same atoms without having any inter-Part bonds,
        as long as, after this is run on all nodes in any subtree using apply2all,
        no inter-part bonds are left, and it works whether or not newly
        created nodes (created by this method while apply2all runs)
        have this method called on them or not.
           The Group implem does *not* call this on its members --
        use apply2all for that.
        [As of 050308, this is overridden only in class molecule and
         class Jig and/or its subclasses.]
        """
        pass

    def move(self, offset): #bruce 070501 added this to Node API
        """translate self in 3d space (if applicable to self's class) by offset;
        do all necessary invalidations, but try to optimize those based on self's
        relative structure not having changed or reoriented.
        [subclasses with any content in 3d space should override this as needed]
        """
        return # correct for many kinds of nodes

    def pickatoms(self): #bruce 070501 added this to Node API [was defined only in Chunk]
        """Pick the atoms owned by self which are not already picked, and which the selection filter
        permits the user to pick (select). Return the number of newly picked atoms.
        [overridden in some subclasses]
        """
        return 0 # correct for most kinds of nodes

    # end of class Node

    
    #in addition, each Node should have the following methods:
    # draw, cut, copy, paste


class Group(Node):
    """The tree node class for the tree.
    Its members can be Groups, jigs, or molecules.
    """

    featurename = "" # (redundant with Node)
        # It's intentional that we don't provide this for Group itself, so a selected Group in the MT
        # doesn't bother you by offering wiki help on Group. Maybe we'll leave it off of Chunk as well...
        # but maybe a better system would be to let user turn it off for specific classes they're familiar with,
        # or to relegate it to a help submenu rather than MT context menu, or in some other way make it less visible...
        # [bruce 051201]
    
    _s_attr_members = S_CHILDREN

    def __init__(self, name, assy, dad, list = []): ###@@@ review inconsistent arg order
        self.members = [] # must come before Node.__init__ [bruce 050316]
        self.__cmfuncs = [] # funcs to call right after the next time self.members is changed
        Node.__init__(self, assy, name, dad)
        self.open = True
        for ob in list:
            self.addchild(ob)

    def _um_initargs(self): #bruce 051013 [in class Group]
        # [as of 060209 this is probably well-defined and correct (for most subclasses), but not presently used]
        "[Overrides Node._um_initargs; see its docstring.]"
        return (self.name, self.assy), {} # note reversed arg order from Node version
            # dad and members (like most inter-object links) are best handled separately

    def _undo_update(self): # in class Group [bruce 060306]
        self.changed_members() # part of fix for bug 1617; fixing it will also require separate changes in MMKit by Mark.
            ###k is this safe to do in arbitrary order vs. other Undo-related updates,
            # or do we need to only do it at the end, and/or in some order when several Groups changed??
            # I don't know, so for now I'll wait and see if we notice bugs from doing it in arbitrary order. [bruce 060306]
        Node._undo_update(self)
        return

    def is_group(self):
        """[overrides Node method; see its docstring]"""
        return True

    open_specified_by_mmp_file = False
    def readmmp_info_opengroup_setitem( self, key, val, interp ): #bruce 050421, to read group open state from mmp file
        """This is called when reading an mmp file, for each "info opengroup" record
        which occurs right after this node's "group" record is read and no other node
        (or "group" record) has been read.
           Key is a list of words, val a string; the entire record format
        is presently [050421] "info opengroup <key> = <val>".
        Interp is an object to help us translate references in <val>
        into other objects read from the same mmp file or referred to by it.
        See the calls of this method from files_mmp for the doc of interp methods.
           If key is recognized, set the attribute or property
        it refers to to val; otherwise do nothing (or for subclasses of Group
        which handle certain keys specially, call the same method in the superclass
        for other keys).
           (An unrecognized key, even if longer than any recognized key,
        is not an error. Someday it would be ok to warn about an mmp file
        containing unrecognized info records or keys, but not too verbosely
        (at most once per file per type of info).)
        """
        if key == ['open']:
            # val should be "True" or "False" (unrecognized vals are ignored)
            if val == 'True':
                self.open = True
                self.open_specified_by_mmp_file = True # so code to close the clipboard won't override it
            elif val == 'False':
                self.open = False
                self.open_specified_by_mmp_file = True
            elif platform.atom_debug:
                print "atom_debug: maybe not an error: \"info opengroup open\" ignoring unrecognized val %r" % (val,)
        else:
            if platform.atom_debug:
                print "atom_debug: fyi: info opengroup (in Group) with unrecognized key %r (not an error)" % (key,)
        return

    def drag_move_ok(self): return True # same as for Node
    def drag_copy_ok(self): return True # for my testing... maybe make it False for Alpha though ###e ####@@@@ 050201
    def is_selection_group_container(self): #bruce 050131 for Alpha
        """Whether this group causes each of its direct members to be treated
        as a "selection group" (see another docstring for what that means,
        but note that it can be true of leaf nodes too, in spite of the name).
        [Intended to be overridden only by the Clipboard.]
        """
        return False # for most groups

    def haspicked(self): # bruce 050126
        """Whether node's subtree has any picked members.
        [See comments in Node.haspicked docstring.]
        """
        if self.picked: return True
        for m in self.members:
            if m.haspicked(): return True
        return False
    
    def changed_members(self): #bruce 050121 new feature, now needed by depositMode
        """Whenever something changes self.members in any way (insert, delete, reorder),
        it MUST call this method to inform us (but only *after* it makes the change);
        we'll inform other interested parties, if any.
        (To tell us you're an interested party, use call_after_next_changed_members.)
           Notes: This need not be called after changes in membership *within* our members,
        only after direct changes to our members list. Our members list is public, but
        whether it's incrementally changed (the same mutable list object) or replaced is
        not defined (and for whatever wants to change it, either one is acceptable).
        It is deprecated for anything other than a Group (or subclass) method to directly
        change self.members, but if it does, calling this immediately afterwards is required.
        [As of 050121 I don't know for sure if all code yet follows this rule, but I think it does. ##k]
        """
        if self.part:
            self.part.changed() # does assy.changed too
        elif self.assy:
            # [bruce 050429 comment: I'm suspicious this is needed or good if we have no part (re bug 413),
            #  but it's too dangerous to change it just before a release, so bug 413 needs a different fix
            #  (and anyway this is not the only source of assy.changed() from opening a file -- at least
            #   chunk.setDisplay also does it). For Undo we might let .changed() propogate only into direct
            #   parents, and then those assy.changed() would not happen and bug 413 might be fixable differently.]
            self.assy.changed()
            # it is ok for something in part.changed() or assy.changed() to modify self.__cmfuncs
        cm = self.__cmfuncs
        if cm:
            self.__cmfuncs = [] # must do this first in case func appends to it
            for func in cm:
                try:
                    func(self)
                        # pass self, in case it's different from the object
                        # they subscribed to (due to kluge_change_class)
                except:
                    print_compact_traceback("error in some cmfunc, ignored by %r: " % self)
        return

    def call_after_next_changed_members(self, func, only_if_new = False):
        """Call func once, right after the next time anything changes self.members.
        At that time, pass it one argument, self; ignore its retval; print error message
        (in debug version only) if it has exceptions.
           If our members are taken over by another Group instance (see kluge_change_class),
        then it, not us, will call func and be the argument passed to func.
           Typically, func should be an "invalidation function", recording the need to
        update something; when that update later occurs, it uses self.members and again
        supplies a func to this method. (If every call of func did an update and gave us
        a new func to record, this might be inefficient when self.members is changed many
        times in a row; nevertheless this is explicitly permitted, which means that we
        explicitly permit func, when called from our code, to itself call this method,
        supplying either the same func or a new one.)
        """
        if only_if_new and (func in self.__cmfuncs):
            return
        self.__cmfuncs.append( func) # might occur during use of same func!
    
    def openable(self): # overrides Node.openable()
        "whether tree widgets should permit the user to open/close their view of this node"
        # if we decide this depends on the tree widget or on something about it,
        # we'll have to pass in some args... don't do that unless/until we need to.
        return True

    # methods before this are by bruce 050108 and should be reviewed when my rewrite is done ###@@@

    def kluge_change_class(self, subclass):
        #bruce 050109 ###@@@ temporary [until files_mmp & assy make this kind of assy.root, shelf, tree on their own]
        """Return a new Group with this one's members but of the specified subclass
        (and otherwise just like this Group, which must be in class Group itself,
        not a subclass). This won't be needed once class assembly is fixed to make
        the proper subclasses directly.
        """
        assert self.__class__ is Group
        new = subclass(self.name, self.assy, self.dad) # no members yet
        assert isinstance(new, Group) # (but usually it's also some subclass of Group, unlike self)
        if self.dad:
            # don't use addmember, it tells the assy it changed
            # (and doesn't add new in right place either) --
            # just directly patch dad's members list to replace self with new
            ind = self.dad.members.index(self)
            self.dad.members[ind] = new
                # don't tell dad its members changed, until new is finished (below)
            self.dad = None # still available in new.dad if we need it
        new.members = self.members # let new steal our members directly
        new.__cmfuncs = self.__cmfuncs # and take responsibility for our members changing...
        self.__cmfuncs = []
        # self should no longer be used; enforce this
        self.members = 333 # not a sequence
        self.node_icon = "<bug if this is called>"
        for mem in new.members:
            mem.dad = new
            # bruce 050205:
            # should we now call mem.changed_dad()? reasons yes: new's new class might differ in rules for selgroup or space
            # (e.g. be the top of a selgroup) and change_dad might be noticing and responding to that change,
            # so this might turn out to be required if something has cached that info in mem already.
            # reasons no: ... some vague uneasiness. Oh, it might falsely tell assy it changed, but I think our caller
            # handles that. So yes wins, unless bugs show up!
            # BUT: don't do this until we're all done (so new is entirely valid).
            ## mem.changed_dad()
        for attr in ['open','hidden','picked']:
            # not name, assy, dad (done in init or above), selgroup, space (done in changed_dad)
            try:
                val = getattr(self, attr)
            except AttributeError:
                pass # .open will go away soon;
                # others are probably always defined but I'm not sure
                # (and should not care here, as long as I get them all)
            else:
                setattr(new, attr, val)
        for mem in new.members:
            mem.changed_dad() # reason is explained above [bruce 050205]
        new.dad.changed_members() # since new class is different from self.class, this might be needed ###@@@ is it ok?
        return new

    # bruce 050113 deprecated addmember and confined it to Node; see its docstring.

    def addchild(self, newchild, _guard_ = 050201, top = False, after = None, before = None): # [renamed from addmember - bruce 050113]
        """Add the given node, newchild, to the end (aka. bottom) of this Group's members list,
        or to the specified place (top aka. beginning, or after some child or index,
        or before some child or index) if one of the named arguments is given.
        Ok even if newchild is already a member of self, in same or different
        location than requested (it will be moved), or a member of some other Group
        (it will be removed). (Behavior with more than one named argument is undefined.)
           Note: the existence of this method (as an attribute) might be used as a check
        for whether a Node can be treated like a Group [as of 050201].
           Special case: legal and no effect if newchild is None or 0 (or anything false);
        this turns out to be needed by assy.copy_sel/Group.copy or Jig.copy! [050131 comment]
        [Warning (from when this was called addmember):
         semantics (place of insertion, and optional arg name/meaning)
         are not consistent with Node.addmember; see my comments in its docstring.
         -- bruce 050110]
        [note, 050315: during low-level node-tree methods like addchild and delmember,
         and also during pick and unpick methods,
         there is no guarantee that the Part structure of our assy's node tree is correct,
         so checkparts should not be called, and assy.part should not be asked for;
         in general, these methods might need to know that each node has a part (perhaps None),
         but they should treat the mapping from nodes to parts as completely arbitrary,
         except for calling inherit_part to help maintain it.]
        """
        #bruce 050110/050206 updated docstring based on current code
        # Note: Lots of changes implemented at home 050201-050202 but not committed until
        # 050206 (after Alpha out); most dates 050201-050202 below are date of change at home.
        #bruce 050201 added _guard_, after, before
        assert _guard_ == 050201
        if newchild is None:
            #bruce 050201 comment: sometimes newchild was the number 0,
            # since Group.copy returned that as a failure code!!!
            # Or it can be None (Jig.copy, or Group.copy after I changed it).
            return

        #bruce 050205:
        # adding several safety checks (and related new feature of auto-delmember)
        # for help with MT DND; they're a good idea anyway.
        # See also today's changes to changed_dad().
        if newchild.dad and not (newchild in newchild.dad.members):
            # This is really a bug or a very deprecated behavior, but we tolerate it for now.
            # Details: some node-creating methods like molecule.copy and/or Group.copy
            # have the unpleasant habit of setting dad in the newly made node
            # without telling the dad! This almost certainly means the other
            # dad-related aspects of the node are wrong... probably best to just pretend
            # those methods never did that. Soon after Alpha we should fix them all and then
            # make this a detected error and no longer tolerate it.
            if platform.atom_debug:
                msg = "atom_debug: addchild setting newchild.dad to None since newchild not in dad's members: %s, %s" % (self,newchild)
                print_compact_stack(msg)
            newchild.dad = None
        if newchild.is_ascendant(self):
            #bruce 050205 adding this for safety (should prevent DND-move cycles as a last resort, tho might lose moved nodes)
            if platform.atom_debug:
                # this msg covers newchild is self too since that's a length-1 cycle
                print "atom_debug: addchild refusing to form a cycle, doing nothing; this indicates a bug in the caller:",self,newchild
            return
        if newchild.dad:
            # first cleanly remove newchild from its prior home.
            # (Callers not liking this can set newchild.dad = None before calling us.
            #  But doing so (or not liking this) is deprecated.)
            if newchild.dad is self:
                # this might be wanted (as a way of moving a node within self.members)
                # (and a caller might request it by accident when moving a node from a general position,
                #  so we want to cooperate), but the general-case code won't work
                # if the before or after options were used, whether as nodes (if the node used as a marker is newchild itself)
                # or as indices (since removal of newchild will change indices of subsequent nodes).
                # So instead, if those options were used, we fix them to work.
                # We print a debug msg just as fyi; that can be removed once this is stable and tested.
                if platform.atom_debug and 0:
                    # i'll remove this msg soon after i first see it.
                    print "atom_debug: fyi: addchild asked to move newchild within self.members, might need special cases",self,newchild
                    print "...options: top = %r, after = %r, before = %r" % (top , after , before)
                if type(before) is type(1):
                     # indices will change, use real nodes instead
                     # (ok even if real node is 'newchild'! we detect that below)
                    before = self.members[before]
                if type(after) is type(1):
                    after = self.members[after]
                if before is newchild or after is newchild:
                    # this is a noop, and it's basically a valid request, so just do it now (i.e. return immediately);
                    # note that general-case code would fail since these desired-position-markers
                    # would be gone once we remove newchild from self.members.
                    return
                # otherwise (after our fixes above) the general-case code should be ok.
                # Fall thru to removing newchild from prior home (in this case, self),
                # before re-adding it in a new place.
            # remove newchild from its prior home (which may or may not be self):
            newchild.dad.delmember(newchild) # this sets newchild.dad to None, but doesn't mess with its .part, .assy, etc
        # Only now will we actually insert newchild into self.
        # [end of this part of bruce 050205 changes]
        
        ## self.assy.changed() # now done by changed_members below
            #e (and what about informing the model tree, if it's displaying us?
            #   probably we need some subscription-to-changes or modtime system...)
        if top:
            self.members.insert(0, newchild) # Insert newchild at the very top
        elif after is not None: # 0 has different meaning than None!
            if type(after) is not type(0):
                after = self.members.index(after) # raises ValueError if not found, that's fine
            if after == -1:
                self.members += [newchild] # Add newchild to the bottom (.insert at -1+1 doesn't do what we want for this case)
            else:
                self.members.insert(after+1, newchild) # Insert newchild after the given position #k does this work for negative indices?
        elif before is not None:
            if type(before) is not type(0):
                before = self.members.index(before) # raises ValueError if not found, that's fine
            self.members.insert(before, newchild) # Insert newchild before the given position #k does this work for negative indices?
        else:
            self.members.append(newchild) # Add newchild to the bottom, i.e. end (default case)
        newchild.dad = self
        newchild.changed_dad()
        newchild.dad.changed_members() # must be done *after* they change and *after* changed_dad has made them acceptable for new dad
        # note: if we moved newchild from one place to another in self,
        # changed_members is called twice, once after deletion and once after re-insertion.
        # probably ok, but I should #doc this in the related subscriber funcs
        # so callers are aware of it. [bruce 050205]
        return

    def delmember(self, obj):
        if obj.dad is not self: # bruce 050205 new feature -- check for this (but do nothing about it)
            if platform.atom_debug:
                print_compact_stack( "atom_debug: fyi: delmember finds obj.dad is not self: ") #k does this ever happen?
        obj.unpick() #bruce 041029 fix bug 145 [callers should not depend on this happening! see below]
            #k [bruce 050202 comment, added 050205]: review this unpick again sometime, esp re DND drag_move
            # (it might be more relevant for addchild than for here; more likely it should be made not needed by callers)
            # [bruce 050203 review: still needed, to keep killed obj out of selmols,
            #  unless we revise things enough to let us invalidate selmols here, or the like;
            #  and [050206] we should, since this side effect is sometimes bad
            #  (though I forget which recent case of it bugged me a lot).]
        ## self.assy.changed() # now done by changed_members below
        try:
            self.members.remove(obj)
        except:
            # relying on this being permitted is deprecated [bruce 050121]
            if platform.atom_debug:
                print_compact_stack( "atom_debug: fyi: delmember finds obj not in members list: ") #k does this ever happen?
            return
        obj.dad = None # bruce 050205 new feature
        self.changed_members() # must be done *after* they change
        return

    def steal_members(self): #bruce 050526
        """Remove all of this group's members (like delmember would do)
        and return them as a list. Assume self doesn't yet have a dad and no members are picked.
        [Private method, for copy -- not reviewed for general use!]
        """
        res = self.members
        self.members = []
        for obj in res:
            if obj.dad is not self: # error, debug-reported but ignored
                if platform.atom_debug:
                    print_compact_stack( "atom_debug: fyi: steal_members finds obj.dad is not self: ") #k does this ever happen?
            obj.dad = None
        ## assume not needed for our private purpose, though it would be needed in general: self.changed_members()
        return res

    def pick(self):
        """select the Group -- and all its members! [see also pick_top]
        [overrides Node.pick]
        """
        Node.pick(self)
            # bruce 050131 comment: important for speed to do Node.pick first,
            # so ob.pick() sees it's picked when its subr scans up the tree
        for ob in self.members:
            ob.pick()
        from debug_prefs import debug_pref_History_print_every_selected_object
        if debug_pref_History_print_every_selected_object(): #bruce 070504 added this condition
            # bruce 050131 comment:
            # I'm very skeptical of doing this history.message
            # recursively, but I'm not changing it for Alpha
            msg = self.description_for_history() # bruce 050121 let subclass decide on this
            env.history.message( msg )
        return

    def description_for_history(self):
        """Return something to print in the history whenever we are selected
        [some subclasses should override this]
        """
        return "Group Name: [" + self.name +"]"
    
    def unpick(self):
        """unselect the Group -- and all its members! [see also unpick_top]
        """
        Node.unpick(self)
        for ob in self.members:
            ob.unpick()

    def unpick_top(self): #bruce 050131 for Alpha: bugfix
        "[Group implem -- go up but don't go down]" #redoc, and clean it all up
        Node.unpick(self)

    def unpick_all_members_except(self, node): #bruce 050131 for Alpha
        "[private method; #doc; overrides Node method]"
        #e should probably inline into unpick_all_except and split that for Node/Group
        res = False
        for ob in self.members:
            res1 = ob.unpick_all_except( node)
            res = res or res1
            # note: the above is *not* equivalent (in side effects)
            # to res = res or ob.unpick_all_except( node)!
        return res

    def inherit_part(self, part): # Group method; bruce 050308
        """Self (a Group) is inheriting part from its dad.
        Set this part in self and all partless kids
        (assuming those are all at the top of the nodetree under self).
        [overrides Node method]
        """
        Node.inherit_part(self, part)
        for m in self.members:
            if m.part is None:
                m.inherit_part(part)
        return

    def hide(self):
        for ob in self.members:
            ob.hide()

    def unhide(self):
        for ob in self.members:
            ob.unhide()
                
    def apply2all(self, fn):
        """Apply fn to self and (as overridden here in Group) all its members.
        It's safe for fn to modify self.members list (since we scan a copy),
        but if members of not-yet-scanned nodes are modified, that will affect
        what nodes are reached by our scan, since each nodes' members list is
        copied only when we reach it. For example, if fn moves a node to a later
        subtree, then the same apply2all scan will reach the same node again
        in its new position.
        """
        fn(self)
        for ob in self.members[:]:
            ob.apply2all(fn)

    def apply2tree(self, fn): #e rename?
        """Like apply2all, but only applies fn to all Group nodes (at or under self)."""
        fn(self)
        for ob in self.members[:]:
            ob.apply2tree(fn)
             
    def apply2picked(self, fn):
        """Apply fn to the topmost picked nodes under (or equal to) self.
        That is, scan the tree of self and its members (to all levels including leaf nodes),
        applying fn to all picked nodes seen, but not scanning into the members of picked nodes.
        Thus, for any node, fn is never applied to both that node and any of its ancestors.
        For effect of fn modifying a members list, see comments in apply2all docstring.
        [An example of (i hope) a safe way of modifying it, as of 050121, is in Group.ungroup.]
        """
        if self.picked: fn(self)
        else:
            for ob in self.members[:]:
                ob.apply2picked(fn)

    def hindmost(self): ###@@@ should rename
        """[docstring is meant for both Node and Group methods taken together:]
        Thinking of nodes as subtrees of the model tree, return the smallest
        subtree of self which contains all picked nodes in this subtree, or None
        if there are no picked nodes in this subtree. Note that the result does
        not depend on the order of traversal of the members of a Group.
        """ #bruce 041208 added docstring, inferred from code
        if self.picked: return self
        node = None
        for x in self.members:
            h = x.hindmost()
            if node and h: return self
            node = node or h
        return node
 
    def permits_ungrouping(self): #bruce 050121
        """Should the user interface permit users to dissolve this Group
        using self.ungroup?
        [Some subclasses should override this.]
        """
        return True # yes, for normal groups.
    
    def ungroup(self):
        """If this Node is a Group, dissolve it, letting its members
        join its dad, if this is possible and if it's permitted as a
        user-requested operation. [bruce 050121 thinks this should be
        split into whether this is permitted, and doing it whether or
        not it's permitted; the present method is really a UI operation
        rather than a structural primitive.]
        [overrides Node.ungroup]
        """
        #bruce 050121 inferred docstring from 2 implems and 1 call
        #bruce 050121 revised: use permits_ungrouping;
        # add kids in place of self within dad (rather than at end)
        if self.dad and self.permits_ungrouping():
            ## if self.name == self.assy.name: return
            ## (that's now covered by permits_ungrouping)
            for x in self.members[:]:
                ## x.moveto(self.dad) #e should probably put them before self in there
                self.delmember(x)
                self.addsibling(x, before = True)
                    # put them before self, to preserve order [bruce 050126]
            self.kill()

    # == Group copy methods [revised/added by bruce 050524-050526]

    def will_copy_if_selected(self, sel, realCopy): # wware 060329 added realCopy arg
        if realCopy:
            # [bruce 060329 comment on wware code:]
            # This recursion is just to print warnings.
            # It's safe for now, since this function is apparently not itself called recursively
            # while copying Group members, but that might change, and if it does this will also need to change.
            # It also appears to be incorrect, at least in some cases, e.g. a Measure Distance jig in a Group
            # gets copied even if only one atom does (in spite of having printed this message),
            # though the produced object gives a traceback when displayed.
            # And the easiest fix for that might be for copying to do a recursive call of this,
            # which is exactly what would make this method's own recursion unneeded and unsafe
            # (it would become exponential in number of nested Groups, in runtime and number of redundant warnings).
            for x in self.members:
                x.will_copy_if_selected(sel, True)
        return True

    def copy_full_in_mapping(self, mapping): # Group method [bruce 050526]
        """
        #doc; overrides Node method; copies any subclass of Group as if it was a plain Group
        [subclasses can override or extend that behavior if desired]
        """
        new = Group(self.name, mapping.assy, None)
        self.copy_copyable_attrs_to(new)
            # redundantly copies .name; also copies .open
            # (This might be wrong for some Group subclasses! Not an issue for now, but someday
            #  it might be better to use attrlist from target, or intersection of their attrlists...)
        mapping.record_copy(self, new) # asserts it was not already copied
        for mem in self.members:
            memcopy = mem.copy_full_in_mapping(mapping) # can be None, if mem refused to be copied
            if memcopy is not None:
                new.addchild(memcopy)
        return new

    # ==
    
    def kill(self): # in class Group
        #bruce 050214: called Node.kill instead of inlining it; enhanced Node.kill;
        # and fixed bug 381 by killing all members first.
        self._prekill() # this has to be done before killing the members, even though Node.kill might do it too [bruce 060327]
        for m in self.members[:]:
            m.kill()
        Node.kill(self)

    def _set_will_kill(self, val): #bruce 060327 in Group
        "[private helper method for _prekill; see its docstring for details; subclasses with owned objects should extend this]"
        Node._set_will_kill( self, val)
        for m in self.members:
            m._set_will_kill( val)
        return

    def reset_subtree_part_assy(self): #bruce 051227
        "[overrides Node method]"
        for m in self.members[:]:
            m.reset_subtree_part_assy()
        Node.reset_subtree_part_assy(self)
        return
    
    def is_ascendant(self, node):
            #e rename nodetree_contains? is_ancestor? (tho true of self too)
            #e or just contains? (no, not obvious arg is a node)
        """[overrides Node.is_ascendant, which is a very special case of the same semantics]
        Returns True iff self is an ascendant of node,
        i.e. if the subtree of nodes headed by self contains node.
        (node must be a Node or None (for None we return False);
         thus it's legal to call this for node being any node's dad.)
        """
        while node is not None:
            if node is self: return True
            node = node.dad
        return False
        
    def nodespicked(self):
        """Return the number of nodes currently selected in this subtree.
        [Overrides Node.nodespicked()]
        Warning (about current implementation [050113]):
        scans the entire tree... calling this on every node in the tree
        might be slow (every node scanned as many times as it is deep in the tree).
        """
        npick = Node.nodespicked(self)
            # bruce 050126 bugfix: was 0 (as if this was called leavespicked)
        for ob in self.members: 
            npick += ob.nodespicked()
        return npick
        
    def node_icon(self, display_prefs):
        open = display_prefs.get('open', False)
        if open:
            return imagename_to_pixmap("modeltree/group-expanded.png")
        else:
            return imagename_to_pixmap("modeltree/group-collapsed.png")

    def kids(self, display_prefs): #bruce 050109 [#k is this used?]
        """[Overrides Node.kids()]
        Return the ordered list of our kids which should be displayed in a model
        tree widget which is using (for this node itself) the given display prefs
        (which might include the boolean pref 'open', default False, telling us
         whether the tree widget plans to show our kids or not).
        (Don't include inter-kid gaps for drag&drop explicitly; see another method
         for that. ###nim)
        Subclasses can override this; this version is valid for any Group whose .members
        don't need filtering or updating, or augmenting (like PartGroup does as of 050109).
         [Note that it is (probably) perfectly ok for subclasses to have a set of kids which is
        not related to their members, provided callers (tree widgets) never assume node.dad
        corresponds to the parent relation in their own tree of display items. I don't know
        how well the existing caller (modelTree.py) follows this so far. -- bruce 050113]
        """
        if not self.openable() or not display_prefs.get('open',False):
            ###@@@ I suspect this check should always be done in the tree widget,
            # so we don't have to do it in Group methods. [bruce 050113]
            return []
        # Historical note: self.members used to be stored in reversed order, but
        # Mark fixed that some time ago. Some callers in modelTree needed reversed
        # members list, after that, not because it was stored in reverse order as
        # it had been, but because modeltree methods added tree items in reverse
        # order (which I fixed yesterday).
        # [bruce 050110 inference from addmember implems/usage]
        return list(self.members)
    
    def edit(self):
        "[this is overridden in some subclasses of Group]"
        cntl = GroupProp(self) # Normal group prop
        cntl.exec_()
        self.assy.mt.mt_update()

    def dumptree(self, depth=0):
        print depth*"...", self.name
        for x in self.members:
            if x.dad is not self: print "bad thread:", x, self, x.dad
            x.dumptree(depth+1)

        
    def draw(self, glpane, dispdef): #bruce 050615 revised this
        if self.hidden:
            #k does this ever happen? This state might only be stored on the kids... [bruce 050615 question]
            return
        self.draw_begin(glpane, dispdef)
        from jigs_planes import ESPImage
    
        try:
            for ob in self.members[:]:
                if not isinstance(ob, ESPImage): #Exclude any ESP image drawing here because of its translucency. [Huaicai 9/28/05]
                    ob.draw(glpane, dispdef)
            #k Do they actually use dispdef? I know some of them sometimes circumvent it (i.e. look directly at outermost one).
            #e I might like to get them to honor it, and generalize dispdef into "drawing preferences".
            # Or it might be easier for drawing prefs to be separately pushed and popped in the glpane itself...
            # we have to worry about things which are drawn before or after main drawing loop --
            # they might need to figure out their dispdef (and coords) specially, or store them during first pass
            # (like renderpass.py egcode does when it stores modelview matrix for transparent objects).
            # [bruce 050615 comments]
        except:
            print_compact_traceback("exception in drawing some Group member; skipping to end: ")
        self.draw_end(glpane, dispdef)
        return

    def draw_begin(self, glpane, dispdef): #bruce 050615
        "Subclasses can override this to change how their child nodes are drawn."
        pass


    def draw_end(self, glpane, dispdef): #bruce 050615
        """Subclasses which override draw_begin should also override draw_end
        to undo whatever changes were made by draw_begin
        (preferably by popping stacks, rather than by doing inverse transformations,
         which only work if nothing was messed up by child nodes or exceptions from them,
         and which might be subject to numerical errors).
        """
        pass
    
    
    def getstatistics(self, stats):
        """add group to part stats
        """
        stats.ngroups += 1
        for ob in self.members:
            ob.getstatistics(stats)
  
    def writemmp(self, mapping): #bruce 050322 revised interface
        mapping.write("group (" + mapping.encode_name(self.name) + ")\n")
        mapping.write("info opengroup open = %s\n" % (self.open and "True" or "False")) #bruce 050421
            # All "info opengroup" records should be written before we write any of our members.
            # If Group subclasses override this method (and don't call it), they'll need to behave similarly.
        # [bruce 050422: this is where we'd write out "jigs moved forward" if they should come at start of this group...]
        for xx in mapping.pop_forwarded_nodes_after_opengroup(self):
            mapping.write_forwarded_node_for_real(xx)
        for x in self.members:
            x.writemmp(mapping)
            # [bruce 050422: ... and this is where we'd write them, to put them after some member leaf or group.]
            for xx in mapping.pop_forwarded_nodes_after_child(x):
                mapping.write_forwarded_node_for_real(xx)
        mapping.write("egroup (" + mapping.encode_name(self.name) + ")\n")
        
    def writepov(self, f, dispdef):
        if self.hidden: return
        for x in self.members: x.writepov(f, dispdef)

    def writemdl(self, alist, f, dispdef):
        if self.hidden: return
        for x in self.members: x.writemdl(alist, f, dispdef)
            
    def __str__(self):
        return "<group " + self.name +">"

    def move(self, offset): # in Group [bruce 070501 added this to Node API]
        """[overrides Node.move]
        """
        for m in self.members:
            m.move(offset)
        return
    
    def pickatoms(self): # in Group [bruce 070501 added this to Node API]
        """[overrides Node method]
        """
        npicked = 0
        for m in self.members:
            npicked += m.pickatoms()
        return npicked

    pass # end of class Group


# everything below here is fairly specialized and probably belongs in other files.
# [bruce 050121 comment]

class SimpleCopyMixin(Node):
    # This will probably just become the default implems for these methods in Node, rather than its own class...
    # but first, test it in Comment and View. When it's stable, also see if the copy methods in Jig and even Chunk
    # can make use of these methods somehow (perhaps with these modified to call new optional subclass methods).
    # [bruce 060523]
    """Node subclasses that want to be copyable via their _s_attr or copyable_attrs decls,
    and that don't need any optimizations for atoms or bonds or for avoiding full copy_val of all attrs,
    and that don't need any special cases like worrying about refs to other copied things needing to be
    transformed through the mapping (i.e. for which all copyable attrs are pure data, not node or atom refs),
    can mix in this class, BEFORE Node, provided they contain a correct definition of _um_initargs
    for use in creating the copy-stub.
    """
    def will_copy_if_selected(self, sel, realCopy):
        "[overrides Node method]"
        return True

    def copy_full_in_mapping(self, mapping): # warning: most of this code is copied from the Jig method.
        clas = self.__class__
        method = self._um_initargs # fyi: for Node, the returned args are assy, name
        args, kws = method()
        # replace self.assy with mapping.assy in args [new requirement of this method API, bruce 070430]
        newargs = list(args)
        for i in range(len(args)):
            if args[i] is self.assy:
                newargs[i] = mapping.assy
        args = tuple(newargs)
        new = clas(*args, **kws)
        # store special info to help _copy_fixup_at_end
        # (note: these attrnames don't start with __ since name-mangling would prevent
        #  subclasses from overriding _copy_fixup_at_end or this method;
        #  that means all subclasses have to take care not to use those attrnames!
        #  It might be better to let them be "manually name-mangled". ##e FIX)
        new._orig = self
        new._mapping = mapping
        new.name = "[being copied]" # should never be seen
        mapping.do_at_end( new._copy_fixup_at_end)
        #k any need to call mapping.record_copy?? probably not for now, but maybe later if these nodes can be ref'd by others
        # (or maybe the general copy code that calls this will take care of that then).
        return new

    def _copy_fixup_at_end(self): # warning: most of this code is copied from the Jig method.
        """[Private method]
        This runs at the end of a copy operation to copy attributes from the old node
        (which could have been done at the start but might as well be done now for most of them).
        Self is the copy, self._orig is the original.
        """
        orig = self._orig
        del self._orig
        mapping = self._mapping
        del self._mapping
        copy = self
        orig.copy_copyable_attrs_to(copy) # this uses copy_val on all attrs
        return

    pass # end of class SimpleCopyMixin

    
class Csys(SimpleCopyMixin, Node):
    """The Csys is used to store all the parameters needed to save and restore a view.
    It is used in two distinct ways:
        1) as a Named View created by the user and visible as a node in the model tree
        2) internal use for storing the LastView and HomeView for every part
    """
    
    sym = "View"
    featurename = "Named View" #bruce 070604 added this

    copyable_attrs = Node.copyable_attrs + ('scale', 'pov', 'zoomFactor', 'quat') #bruce 060523
        # (note: for copy, this is redundant with _um_initargs (that's ok),
        #  but for Undo, it's important to list these here or give them _s_attr decls.
        #  This fixes a presumed bug (perhaps unreported -- now bug 1942) in Undo of Set_to_Current_View.
        #  Bug 1369 (copy) is fixed by _um_initargs and SimpleCopyMixin, not by this.)

    scale = pov = zoomFactor = quat = None # Undo might require these to have default values (not sure) [bruce 060523]

    def __init__(self, assy, name, scale, pov, zoomFactor, w, x = None, y = None, z = None):
        self.const_pixmap = imagename_to_pixmap("modeltree/csys.png")
        if name:
            Node.__init__(self, assy, name)
        else:
            Node.__init__(self, assy, gensym("%s-" % self.sym))
                #bruce 070604 genViewNum -> gensym [##e can we someday teach superclass to do this?]
        self.scale = scale
        assert type(pov) is type(V(1, 0, 0))
        self.pov = V(pov[0], pov[1], pov[2])
        self.zoomFactor = zoomFactor

        #bruce 050516 probable bugfix, using "is None" rather than "if not x and not y and not z:"
        if x is None and y is None and z is None:
            self.quat = Q(w)
            #bruce 050518 comment: this form is used with w an array of 4 floats (in same order
            # as in mmp file's csys record), when parsing csys mmprecords,
            # or with w a quat in other places.
        else:
            self.quat = Q(x, y, z, w)
            #bruce 050518 question: why are these in different order than in arglist? bug?? ###k
            # ... this is used with wxyz = 0.0, 1.0, 0.0, 0.0 to initialize both views for any Part. No other uses.
            # And order is not consistent with mmp record, either. Therefore I can and should revise it. Later.
            # Looks like the main error is that the vars are misnamed/misordered, both here and in init arglist.
            # Best revision would probably just be to disallow this form! #e 
        return

    def _um_initargs(self): #bruce 060523 to help make it copyable from the UI (fixes bug 1369 along with SimpleCopyMixin)
        "#doc [warning: see comment where this is called in this class -- it has to do more than its general spec requires]"
        # (split out of self.copy)
        if "a kluge is ok since I'm in a hurry":
            # the data in this Csys might not be up-to-date, since the glpane "caches it"
            # (if we're the Home or Last View of its current Part)
            # and doesn't write it back after every user event!
            # probably it should... but until it does, do it now, before copying it!
            self.assy.o.saveLastView()
        return (self.assy, self.name, self.scale, self.pov, self.zoomFactor, self.quat), {}
    
    def show_in_model_tree(self):
        #bruce 050128; nothing's wrong with showing them, except that they are unselectable
        # and useless for anything except being renamed by dblclick (which can lead to bugs
        # if the names are still used when files_mmp reads the mmp file again). For Beta we plan
        # to make them useful and safe, and then make them showable again.
        "[overrides Node method]"
        return True # changed retval to True to support Named Views.  mark 060124.

    def writemmp(self, mapping):
        v = (self.quat.w, self.quat.x, self.quat.y, self.quat.z, self.scale,
             self.pov[0], self.pov[1], self.pov[2], self.zoomFactor)
        mapping.write("csys (" + mapping.encode_name(self.name) +
                ") (%f, %f, %f, %f) (%f) (%f, %f, %f) (%f)\n" % v)
        self.writemmp_info_leaf(mapping) #bruce 050421 (only matters once these are present in main tree)

    def copy(self, dad = None): #bruce 060523 revised this (should be equivalent)
        #bruce 050420 -- revise this (it was a stub) for sake of Part view propogation upon topnode ungrouping;
        # note that various Node.copy methods are not yet consistent, and I'm not fixing this now.
        # (When I do, I think they will not accept "dad" but will accept a "mapping", and will never rename the copy.)
        # The data copied is the same as what can be passed to init and what writemmp writes.
        # Note that the copy needs to have the same exact name, not a variant (since the name
        # is meaningful for the internal uses of this object, in the present implem).
        assert dad is None
        args, kws = self._um_initargs()
            # note: we depend on our own _um_initargs returning enough info for a full copy,
            # though it doesn't have to in general.
        if 0 and platform.atom_debug:
            print "atom_debug: copying csys:", self
        return Csys( *args, **kws )

    def __str__(self):
        #bruce 050420 comment: this is inadequate, but before revising it
        # I'd have to verify it's not used internally, like Jig.__repr__ used to be!!
        return "<csys " + self.name + ">"

    def __CM_Change_View(self): #mark 060122
        self.change_view()
        
    def change_view(self): #mark 060122
        '''Change the view to self.
        '''
        self.assy.o.animateToView(self.quat, self.scale, self.pov, self.zoomFactor, animate=True)
        
        from HistoryWidget import greenmsg
        cmd = greenmsg("Change View: ")
        msg = 'View changed to "%s".' % (self.name)
        env.history.message( cmd + msg )
        
    def __CM_Set_to_Current_View(self): #mark 060122
        self.set_to_current_view()
    
    def set_to_current_view(self): #mark 060122
        '''Set self to current view.
        '''
        self.scale = self.assy.o.scale
        self.pov = V(self.assy.o.pov[0], self.assy.o.pov[1], self.assy.o.pov[2])
        self.zoomFactor = self.assy.o.zoomFactor
        self.quat = Q(self.assy.o.quat)
        self.assy.changed() ###e we should make this check whether it really changed? (or will Undo do that??)
        
        from HistoryWidget import greenmsg
        cmd = greenmsg("Set View: ")
        msg = 'View "%s" now set to the current view.' % (self.name)
        env.history.message( cmd + msg )

    def move(self, offset): # in class Csys (Named View) [bruce 070501, used when these are deposited from partlib]
        "[properly implements Node API method]"
        self.pov = self.pov - offset # minus, because what we move is the center of view, defined as -1 * self.pov
        self.changed()
        return

    pass # end of class Csys

# bruce 050417: commenting out class Datum (and ignoring its mmp record "datum"),
# since it has no useful effect.
# bruce 060523: removing the commented out code. In case it's useful for Datum Planes,
# it can be found in cvs rev 1.149 or earlier. It referred to cad/images/datumplane.png.


# rest of file added by bruce 050108/050109, needs review when done ###@@@

# specialized kinds of Groups:

class PartGroup(Group):
    """A specialized Group for holding the entire "main model" of an assembly,
    with provisions for including the "assy.viewdata" elements as initial kids, but not in self.members
    (which is a kluge, and hopefully can be removed reasonably soon, though perhaps not for Alpha).
    """
    _initialkids = [] #bruce 050302
    # These revised definitions are the non-kluge reason we need this subclass: ###@@@ also some for menus...
    def is_top_of_selection_group(self): return True #bruce 050131 for Alpha
    def rename_enabled(self): return False
    def drag_move_ok(self): return False
    # ... but drag_copy is permitted! (someday, when copying groups is permitted)
    # drop methods should be the same as for any Group
    def permits_ungrouping(self): return False
    def node_icon(self, display_prefs):
        # same whether closed or open
        return imagename_to_pixmap("modeltree/part.png")
##    # And this temporary kluge makes it possible to use this subclass where it's
##    # needed, without modifying assembly.py or files_mmp.py:
##    def kluge_set_initial_nonmember_kids(self, lis): #bruce 050302 comment: no longer used, for now
##        """[This kluge lets the csys and datum plane model tree items
##        show up in the PartGroup, without their nodes being in its members list,
##        since other code wants their nodes to remain in assy.viewdata, but they can
##        only have one .dad at a time. Use of it means you can't assume node.dad
##        corresponds to model tree item parent!]
##        """
##        lis = filter( lambda node: node.show_in_model_tree(), lis)
##            # bruce 050127; for now this is the only place that honors node.show_in_model_tree()!
##        self._initialkids = list(lis)
    def kids(self, display_prefs):
        "overrides Group.kids"
        if not self.openable() or not display_prefs.get('open',False):
            return []
        regularkids = Group.kids(self, display_prefs)
        return list(self._initialkids + regularkids)
    def edit(self):
        cntl = PartProp(self.assy)
            #bruce comment 050420: PartProp is passed assy and gets its stats from assy.tree.
            # This needs revision if it should someday be available for Parts on the clipboard.
        cntl.exec_()
        self.assy.mt.mt_update()
    def description_for_history(self):
        """[overridden from Group method]"""
        return "Part Name: [" + self.name +"]"
    pass

class ClipboardShelfGroup(Group):
    """A specialized Group for holding the Clipboard (aka Shelf). [This will be revised... ###@@@]
    """
    def postcopy_in_mapping(self, mapping): #bruce 050524
        assert 0, "RootGroup.postcopy_in_mapping should never be called!"
    def pick(self): #bruce 050131 for Alpha
        msg = "Clipboard can't be selected or dragged. (Individual clipboard items can be.)"
        ## bruce 050316: no longer do this: self.redmsg( msg)
        env.history.statusbar_msg( msg)
    def is_selection_group_container(self): return True #bruce 050131 for Alpha
    def rename_enabled(self): return False
    def drag_move_ok(self): return False
    def drag_copy_ok(self): return False
    ## def drop_enabled(self): return True # not needed since default; drop on clipboard makes a new clipboard item
    def drop_on(self, drag_type, nodes):
        #bruce 050203: nodes dropped onto the clipboard come from one "space"
        # and ought to stay that way by default; user can drag them one-at-a-time if desired.
        # (In theory this grouping need only be done for the subsets of them which are bonded;
        #  for now that's too hard -- maybe not for long, similar to bug 371.)
        if len(nodes) > 1 and drag_type == 'move': #####@@@@@ desired for copy too, but below implem would be wrong for that...
            name = self.assy.name_autogrouped_nodes_for_clipboard( nodes, howmade = drag_type )
            new = Group(name, self.assy, None)
            for node in nodes[:]: #bruce 050216 don't reverse the order, it's already correct
                node.unpick() #bruce 050216; don't know if needed or matters; 050307 moved from after to before moveto
                node.moveto(new) ####@@@@ guess, same as in super.drop_on (move here, regardless of drag_type? no, not correct!)
            nodes = [new] # a new length-1 list of nodes
            env.history.message( "(fyi: Grouped some nodes to keep them in one clipboard item)" ) ###e improve text
        return Group.drop_on(self, drag_type, nodes)
    def permits_ungrouping(self): return False
    ##bruce 050316: does always being openable work around the bugs in which this node is not open when it should be?
    ###e btw we need to make sure it becomes open whenever it contains the current part. ####@@@@
##    def openable(self): # overrides Node.openable()
##        "whether tree widgets should permit the user to open/close their view of this node"
##        non_empty = (len(self.members) > 0)
##        return non_empty
    def node_icon(self, display_prefs):
        del display_prefs # unlike most Groups, we don't even care about 'open'
        non_empty = (len(self.members) > 0)
        if non_empty:
            kluge_pixmap = imagename_to_pixmap("modeltree/clipboard-full.png")
            res = imagename_to_pixmap("modeltree/clipboard-full.png")
        else:
            kluge_pixmap = imagename_to_pixmap("modeltree/clipboard-gray.png")
            res = imagename_to_pixmap("modeltree/clipboard-empty.png")
        # kluge: guess: makes paste tool look enabled or disabled
        ###@@@ clean this up somehow?? believe it or not, it might actually be ok...
        self.assy.w.editPasteAction.setIcon(QtGui.QIcon(kluge_pixmap))
        return res
    def edit(self):
        return "The Clipboard does not yet provide a property-editing dialog."
    def edit_props_enabled(self):
        return False
    def description_for_history(self):
        """[overridden from Group method]"""
        return "Clipboard"
    def get_pastable_chunks(self): # mark 060305
        '''Returns a list of all top-level pastable chunks in the clipboard,
        excluding chunks that are members of another group.'''
        pastable_chunks = []
        from chunk import molecule
        for m in self.members:
            if isinstance(m, molecule):
                pastable_chunks += [m]
        
        return pastable_chunks

    pass

class RootGroup(Group):
    """A specialized Group for holding the entire model tree's toplevel nodes,
    which (by coincidence? probably more like a historical non-coincidence)
    imitates the assy.root member of the pre-050109 code. [This will be revised... ###@@@]
    [btw i don't know for sure that this is needed at all...]
    ###obs doc, but reuse some of it:
    This is what the pre-050108 code made or imitated in modelTree as a Group called ROOT. ###k i think
    This will be revised soon, because
    (1) the assembly itself might as well be this Node,
    (2)  the toplevel members of an assembly will differ from what they are now.
    """
    def postcopy_in_mapping(self, mapping): #bruce 050524
        assert 0, "RootGroup.postcopy_in_mapping should never be called!"
    def pick(self): #bruce 050131 for Alpha
        self.redmsg( "Internal error: tried to select assy.root (ignored)" )
    #e does this need to differ from a Group? maybe in some dnd/rename attrs...
    # or maybe not, since only its kids are shown ###@@@
    # (we do use the fact that it differs in class from a Group
    #  as a signal that we might need to replace it... not sure if this is needed)
    pass

# the next few functions belong in assembly.py and/or in a different form

def kluge_patch_assy_toplevel_groups(assy, assert_this_was_not_needed = False): #bruce 050109
    ####@@@@ should be turned into mods to assembly.py, or a method in it
    """This kluge is needed until we do the same thing inside assy
    or whatever makes the toplevel groups in it (eg files_mmp).
    Call it as often as you want (at least once before updating model tree
    if assy might be newly loaded); it only changes things when it needs to
    (once for each newly loaded file or inited assy, basically);
    in theory it makes assy "look right in the model tree"
    without changing what will be saved in an mmp file,
    or indeed what will be seen by any other old code looking at
    the 3 attrs of assy this function replaces (shelf, tree, root).
    Note: if any of them is None, or not an instance object, we'll get an exception here.
    """
    #bruce 050131 for Alpha:
    # this is now also called in assembly.__init__ and in readmmp,
    # not only from the mtree.
    
    ## oldmod = assy_begin_suspend_noticing_changes(assy)
    oldmod = assy.begin_suspend_noticing_changes()
    # does doing it this soon help? don't know why, was doing before root mod...
    # now i am wondering if i was wrong and bug of wrongly reported assy mod
    # got fixed even by just doing this down below, just before remaking root.
    # anyway that bug *is* fixed now, so ok for now, worry about it later. ###@@@
    fixroot = 0
    try:
        if assy.shelf.__class__ is Group:
            assy.shelf = assy.shelf.kluge_change_class( ClipboardShelfGroup)
            fixroot = 1
        if assy.tree.__class__ is Group:
            assy.tree = assy.tree.kluge_change_class( PartGroup)
            ##bruce 050302 removing use of 'viewdata' here,
            # since its elements are no longer shown in the modelTree,
            # and I might as well not figure them out re assy/part split until we want
            # them back and know how we want them to behave regarding parts.
##            lis = list(assy.viewdata.members)
##            # are these in the correct order (CSys XY YZ ZX)? I think so. [bruce 050110]
##            assy.tree.kluge_set_initial_nonmember_kids( lis )
            fixroot = 1
        if assy.root.__class__ is Group or fixroot:
            fixroot = 1 # needed for the "assert_this_was_not_needed" check
            #e make new Root Group in there too -- and btw, use it in model tree widgets for the entire tree...
            # would it work better to use kluge_change_class for this?
            # academic Q, since it would not be correct, members are not revised ones we made above.
            assy.root = RootGroup("ROOT", assy, None, [assy.tree, assy.shelf]) #k ok to not del them from the old root??
            ###@@@ BUG (suspected caused here): fyi: too early for this status msg: (fyi: part now has unsaved changes)
            # is it fixed now by the begin/end funcs? at leastI don't recall seeing it recently [bruce 050131]
            ## removed this, 050310: assy.current_selection_group = assy.tree #bruce 050131 for Alpha
            assy.root.unpick() #bruce 050131 for Alpha, not yet 100% sure it's safe or good, but probably it prevents bugs
            ## revised this, 050310:
            ## assy.current_selection_group = assy.tree # do it both before and after unpick (though in theory either alone is ok)
            ## assy.current_selgroup_changed()
            ## assy.set_current_selgroup( assy.tree) -- no, checks are not needed and history message is bad
            assy.init_current_selgroup() #050315
    finally:
        ## assy_end_suspend_noticing_changes(assy,oldmod)
        assy.end_suspend_noticing_changes(oldmod)
        if fixroot and assert_this_was_not_needed: #050315
            if platform.atom_debug:
                print_compact_stack("atom_debug: fyi: kluge_patch_assy_toplevel_groups sees fixroot and assert_this_was_not_needed: ")
    return

# ==

##descendents? spelling..
def topmost_nodes( nodes): #bruce 050303
    """Given 0 or more nodes (as a python sequence), return a list
    of the given nodes that are not descendents of other given nodes.
    [See also hindmost and topmost_selected_nodes, but those only work for
    the set of selected nodes.]
       WARNING: current implem is quadratic time in len(retval).
    """
    res = {} # from id(node) to node
    for node in nodes:
        assert node is not None # incorrect otherwise -- None won't have .is_ascendant method
        dad = node # not node.dad, that way we remove dups as well (might never be needed, but good)
        while dad is not None:
            if id(dad) in res:
                break
            dad = node.dad
        if dad is None:
            # node and its dads (all levels) were not in res
            # add node, but also remove any members that are below it (how?)
            #e (could be more efficient if we sorted nodes by depth in tree,
            #  or perhaps even sorted the tree-paths from root to each node)
            for other in res.values():
                if node.is_ascendant(other):
                    del res[id(other)]
            res[id(node)] = node
    return res.values()
    
# end
