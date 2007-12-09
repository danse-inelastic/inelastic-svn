# Copyright 2006-2007 Brandon Keith  See LICENSE file for details. 
"""
state_constants.py -- constants for declaring attributes' roles in
holding state or referring to objects that hold state.

$Id: state_constants.py,v 1.6 2007/05/17 18:16:18 emessick Exp $

See state_utils.py for more info and related classes/utilities.
(It's undecided whether these declarations make sense
in objects that don't inherit from one of the mixins defined in
state_utils.py.)

These declarations are used by Undo to know what attributes' changes
should be recorded and later undone, and to find objects which need to
be watched for changes.

Someday they might also be used for automatically knowing
how to save objects to files, how to copy or diff or delete them,
how to browse or edit their state from a UI, etc.
"""

__author__ = "bruce"


# This is presently imported by constants.py and thus by most modules,
# so it should not import much, or define anything unsuitable for
# being a global in all modules.


# Possible values for _s_attr_xxx attribute declarations (needed by Undo)
# (defining these in constants.py might be temporary; for now it does "import *" from here)

S_DATA = 'S_DATA' # for attributes whose value changes should be saved or undone.


S_CHILD = 'S_CHILD' # like S_DATA, but for attributes whose value is None or a "child object" which might also contain undoable state.

S_CHILDREN = 'S_CHILDREN' # like S_CHILD, but value might be a list or dict (etc) containing one or more child objects.

S_CHILDREN_NOT_DATA = 'S_CHILDREN_NOT_DATA' # scan for children, but not for state or diffs [bruce 060313, experimental but used]


# ref and parent options are not yet needed, and will be treated the same as S_DATA,
# which itself will be treated more like S_REFS anyway if it hits any objects.
# We'll still define them so we can see if you want to declare any attrs using them, mainly S_PARENT.

S_REF = 'S_REF' # like S_DATA, but for attributes whose value is None or a "referenced object",
    # which might or might not be encountered in a scan of undoable objects going only into children.
    # (It's not yet clear exactly how this differs from S_DATA, or whether it matters if ref'd objects are encountered
    #  in a scan into children. Are these "siblings or cousins" (like a jig's atoms) or "foreign objects" (like some QDialog)
    #  or "other state-holders" (like GLPane or MainWindow) or "constants" (like Elements and Atomtypes)?)
    
S_REFS = 'S_REFS' # like S_REF, but value might be a list or dict (etc) containing one or more referenced objects.


S_PARENT = 'S_PARENT' # like S_DATA, but for attributes whose value is None or a "parent object"
    # (one which should be encountered in a scan of undoable objects going only into children,
    #  and of which this object is a child or grandchild etc).
    
S_PARENTS = 'S_PARENTS' # like S_PARENT, but value might be a list or dict (etc) containing one or more parent objects.


S_CACHE = 'S_CACHE' # for attributes which should be deleted (or otherwise invalidated) when other attributes' changes are undone.

S_IGNORE = 'S_IGNORE' # state system should pretend this attr doesn't exist (i.e. never look at it or change it or delete it).
    # (This is equivalent to providing no state declaration for the attr, unless we add a future "default decl" for all attrs
    #  not declared individually, in which case this will let you exclude an attr from that.
    #  It's also useful for subclasses wanting to override state decls inherited from a superclass.)

# end
