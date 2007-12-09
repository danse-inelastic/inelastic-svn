# Copyright 2004-2007 Brandon Keith  See LICENSE file for details. 
"""
bonds.py -- class Bond, for any supported type of chemical bond between two atoms
(one of which might be a "singlet" to represent an "open bond" in the UI),
and related code

$Id: bonds.py,v 1.85 2007/07/01 17:27:32 emessick Exp $


History:

- originally by Josh

- lots of changes, by various developers

- split out of chem.py by bruce 050502

- support for higher-valence bonds added by bruce 050502 - ??? [ongoing]

- bruce optimized some things, including using 'is' and 'is not' rather than '==', '!='
  for atoms, molecules, elements, parts, assys in many places (not all commented individually); 050513

- bruce split bond_constants.py into a separate module; 050707

- 050727 bruce moved bond drawing code into a separate module, bond_drawer.py
  (also removed some imports not needed here, even though chem.py still does "from bonds import *"
   and some other modules import * from chem, so there is no guarantee these were not needed indirectly)

"""
__author__ = "Josh"

# a lot of these imports might not be needed here in bonds.py,
# but note that as of 050502 they are all imported into chem.py (at end of that file)
# and everything from it is imported into some other modules.
# [bruce comment 050502] ###@@@

debug_1951 = False # DO NOT COMMIT with True

import struct
from Numeric import floor

from VQT import Q, vlen, norm

from mdldata import marks, links, filler

from debug import print_compact_stack, compact_stack, print_compact_traceback

import platform # for atom_debug; note that uses of atom_debug should all grab it
  # from platform.atom_debug since it can be changed at runtime

from elements import DIRECTIONAL_BOND_ELEMENTS, Singlet

# bonds, chem, and chunk form an import loop
import chem

from bond_constants import V_SINGLE
from bond_constants import BOND_VALENCES
from bond_constants import BOND_MMPRECORDS
from bond_constants import BOND_VALENCES_HIGHEST_FIRST
from bond_constants import bond_params
from bond_constants import bonded_atoms_summary
from bond_constants import bond_type_names

import env
from state_utils import StateMixin #bruce 060223
from changes import register_changedict, register_class_changedicts
from debug_prefs import debug_pref, Choice_boolean_False #bruce 060307
from HistoryWidget import redmsg, quote_html #bruce 070601

from state_constants import S_CACHE, S_DATA, S_PARENT

# Linus Pauling
# http://www.pubmedcentral.gov/articlerender.fcgi?artid=220148
CC_GRAPHITIC_BONDLENGTH = 1.421   # page 1647
BN_GRAPHITIC_BONDLENGTH = 1.446   # page 1650

try:
    if not debug_pref('Enable pyrex atoms next time', Choice_boolean_False, prefs_key=True):
        raise ImportError
    from atombase import BondSetBase, BondBase
    class BondSet(BondSetBase):
        def __init__(self):
            BondSetBase.__init__(self)
            self.key = atKey.next()
except ImportError:
    def BondSet():
        return { }
    class BondBase:
        def __init__(self):
            pass
        def __getattr__(self, attr):
            raise AttributeError, attr

# ==

def bonded(a1, a2): #bruce 041119 #e optimized by bruce 050502 (this indirectly added "assert a1 != a2")
    "are these atoms (or singlets) already directly bonded? [AssertionError if they are the same atom.]"
    ## return a2 in a1.neighbors()
    return not not find_bond(a1, a2)

atoms_are_bonded = bonded # this is a better name (given that it only works for atoms, not e.g. for chunks) --
    # we should replace the old name with it sometime #bruce 070601

def find_bond(a1, a2): #bruce 050502; there might be an existing function in some other file, to merge this with
    "If a1 and a2 are bonded, return their Bond object; if not, return None. [AssertionError if they are the same atom.]"
    assert a1 is not a2
    for bond in a1.bonds:
        if bond.atom1 is a2 or bond.atom2 is a2:
            return bond
    return None

bond_atoms_oldversion_noops_seen = {} #bruce 051216

def bond_atoms_oldversion(a1,a2): #bruce 050502 renamed this from bond_atoms; it's called from the newer version of bond_atoms
    """Make a new bond between atoms a1 and a2 (and add it to their lists of bonds),
    if they are not already bonded; if they are already bonded do nothing. Return None.
    (The new bond object, if one is made, can't be found except by scanning the bonds
    of one of the atoms.)
       If a1 == a2, this is an error; print a warning and do nothing.
       This increases the number of bonds on each atom (when it makes a new bond) --
    it never removes any singlets. Therefore it is mostly for low-level use.
    It could be called directly, but is usually called via the method molecule.bond,
    purely for historical reasons.
    """
    # bruce 041109 split this out of molecule.bond. Since it's the only caller of
    # Bond.__init__, what it does to the atoms could (and probably should) be put
    # inside the constructor. However, it should not simply be replaced with calls
    # to the constructor, in case we someday want it to return the bond which it
    # either makes (as the constructor does) or doesn't make (when the atoms are
    # already bonded). The test for a prior bond makes more sense outside of the
    # Bond constructor.
    if a1 is a2: #bruce 041119, partial response to bug #203
        print "BUG: bond_atoms was asked to bond %r to itself." % a1
        print "Doing nothing (but further bugs may be caused by this)."
        print_compact_stack("stack when same-atom bond attempted: ")
        return

    #bruce 051216 rewriting this to be faster and avoid console warning
    # when bond already exists (re bug 1226), but still verify bond is on both atoms or neither
    b1 = find_bond(a1,a2) # a Bond or None
    b2 = find_bond(a2,a1)
    if b1 is not b2:
        print "bug warning: bond between %r and %r inconsistent in their .bonds lists; %r (id %#x) vs %r (id %#x)" \
              % (a1,a2, b1, id(b1), b2, id(b2))
        print_compact_stack("will remove one or both existing bonds, then make the requested new one: ")
        if b1:
            a1.bonds.remove(b1)
            # probably no need for a1._changed_structure() since we'll do it in Bond(a1,a2) below; probably same for a2;
            # but as a precaution in case of bugs (or misanalysis or future change of this code),
            # I'll do it anyway. [bruce 060322]
            a1._changed_structure()
            b1 = None
        if b2:
            a2.bonds.remove(b2)
            a2._changed_structure()
            b2 = None
    if b1:
        # these atoms are already bonded
        ###e should we verify bond order is 1, otherwise complain more loudly??
        if platform.atom_debug:
            # print debug warning
            #e refile this code -- only print warning once for each place in the code it can happen from
            blame = compact_stack() # slow, but should be ok since this case should be rare
                # known cases as of 051216 include only one: reading pdb files with redundant CONECT records
            if not bond_atoms_oldversion_noops_seen.has_key(blame):
                print_compact_stack( "atom_debug: note: bond_atoms_oldversion doing nothing since %r and %r already bonded: " % (a1,a2))
                if not bond_atoms_oldversion_noops_seen:
                    print "(above message (bond_atoms_oldversion noop) is only printed once for each compact_stack that calls it)"
                bond_atoms_oldversion_noops_seen[blame] = None
            pass
        return
    b = Bond(a1,a2) # (this does all necessary invals, including a1 and a2._changed_structure())
    a1.bonds.append(b)
    a2.bonds.append(b)
    return

##    # pre-051216 code (starting from where new code starts above)
##    at1,at2 = a1,a2
##    b = Bond(at1,at2) # (this does all necessary invals)
##    
##    #bruce 041029 precautionary change -- I find in debugging that the bond
##    # can be already in one but not the other of at1.bonds and at2.bonds,
##    # as a result of prior bugs. To avoid worsening those bugs, we should
##    # change this... but for now I'll just print a message about it.
##    #bruce 041109: when this happens I'll now also remove the obsolete bond.
##    if (b in at1.bonds) != (b in at2.bonds):
##        print "fyi: debug: for new bond %r, (b in at1.bonds) != (b in at2.bonds); removing old bond" % b
##        try:
##            at1.bonds.remove(b)
##        except:
##            pass
##        try:
##            at2.bonds.remove(b)
##        except:
##            pass
##    if not b in at2.bonds:
##        at1.bonds.append(b)
##        at2.bonds.append(b)
##    else:
##        # [bruce comment 041115: I don't know if this ever happens,
##        #  or if it's a good idea for it to be allowed, but it is allowed.
##        #  #e should it inval the old bond? I think so, but didn't add that.
##        #  later: it happens a lot when entering Extrude; guess: mol.copy copies
##        #  each internal bond twice (sounds right, but I did not verify this).]
##        #
##        # [addendum, bruce 051018: I added a message for when a new bond is equal to
##        #  an existing one, but entering Extrude does not print that, so either it's
##        #  been changed or mol.copy has or I misunderstand the above code (which
##        #  I predict would hit that message). Just to check, I'll print a debug message here (below);
##        #  that message is not happening either, so maybe this deprecated feature is no longer used at all. #k ####@@@@
##        #  (Should also try reading a pdb file with the same bond listed twice... ###k) [like bug 1226!]
##        if platform.atom_debug:
##            print "atom_debug: fyi (possible bug): bond_atoms_oldversion is a noop since an equal bond exists:", b
##        pass
##    return

def bond_atoms_faster(at1, at2, v6): #bruce 050513; docstring corrected 050706
    """Bond two atoms, which must not be already bonded (this might not be checked).
    Doesn't remove singlets. [###k should verify that by a test]
    Return the new bond object (which is given the valence v6, which must be specified).
    """
    b = Bond(at1, at2, v6) # (this does all necessary invals, including _changed_structure on atoms, and asserts at1 is not at2)
    at1.bonds.append(b)
    at2.bonds.append(b)
    return b

def bond_copied_atoms(at1, at2, oldbond, origat1): #bruce 050524; revised 070424
    """Bond the given atoms, at1 and at2 (and return the new bond object),
    copying whatever bond state is relevant from oldbond,
    which is presumably a bond between the originals of the same atoms,
    or it might be a half-copied bond if at1 or at2 is a singlet
    (whether to use this function like that is not yet decided).
    As of 050727 this is also used in Atom.unbond to copy bond types
    onto open bonds which replace broken real bonds.
       If oldbond might be "directional" (and thus might have state
    which is directional, i.e. which looks different depending on which
    of its atoms you're looking at), the caller must pass origat1,
    an atom of oldbond corresponding to at1 in the new bond.
    """
    newbond = bond_atoms_faster(at1, at2, oldbond.v6)
    if origat1 is not None:
        #bruce 070424 also copy bond_direction, if newbond is directional
        # (which can be false in practice when at2 is a bondpoint) 
        if oldbond._direction and newbond.is_directional():
            direction = oldbond.bond_direction_from(origat1)
            newbond.set_bond_direction_from(at1, direction)
    else:
        # this case is deprecated, and thought never to happen, as of bruce 070424
        ## if oldbond._direction and platform.atom_debug:
        print_compact_stack( "debug: bond_copied_atoms%r needs origat1: " % ((at1, at2, oldbond, origat1),) )
    return newbond

# == helper functions related to bonding (I might move these lower in the file #e)

def bonds_mmprecord( valence, atomcodes ):
    """Return the mmp record line (not including its terminating '\n')
    which represents one or more bonds of the same (given) valence
    (which must be a supported valence)
    from the prior atom in the mmp file to each of the listed atoms
    (given as atomcodes, a list of the strings used to encode them
     in the mmp file being written).
    """
    ind = BOND_VALENCES.index(valence) # exception if not a supported valence
    recname = BOND_MMPRECORDS[ind]
    return recname + " " + " ".join(atomcodes)

def bond_atoms(a1, a2, vnew = None, s1 = None, s2 = None, no_corrections = False):
    """WARNING: If vnew is not provided, this function behaves differently and is
    much less safe for general use (details below).
    
       Behavior when vnew is provided:
    Bond atoms a1 and a2 by making a new bond of valence vnew (which must be one
    of the constants in chem.BOND_VALENCES, not a numerically expressed valence;
    for the effect of not providing vnew, see below).
       The new bond is returned. If for some reason it can't be made, None is returned
    (but if that can happen, we should revise the API so an error message can be returned).
       Error if these two atoms are already bonded. [Question: is this detected? ###k]
       If provided, s1 and s2 are the existing singlets on a1 and a2 (respectively)
    whose valence should be reduced (or eliminated, in which case they are deleted)
    to provide valence for the new bond. (If they don't have enough, other adjustments
    will be made; this function is free to alter, remove, or replace any existing
    singlets on either atom.)
       For now, this function will never alter the valence of any existing bonds
    to real atoms. If necessary, it will introduce valence errors on a1 and/or a2.
    (Or if they already had valence errors, it might remove or alter those.)
       If no_corrections = True, this function will not alter singlets on a1 or a2,
    but will either completely ignore issues of total valence of these atoms, or will
    limit itself to tracking valence errors or setting related flags (this is undecided).
    (This might be useful for code which builds new atoms rather than modifying
    existing ones, such as when reading mmp files or copying existing atoms.)

       Behavior when vnew is not provided (less safe in general):
    For backwards compatibility, when vnew is not provided, this function calls the
    old code [pre-higher-valence-bonds, pre-050502] which acts roughly as if
    vnew = V_SINGLE, s1 = s2 = None, no_corrections = True, except that it returns
    None rather than the newly made bond, and unlike this function doesn't mind
    if there's an existing bond, but does nothing in that case; this behavior might
    be relied on by the current code for copying bonds when copying a chunk, which
    might copy some of them twice.
       Using the old bond_atoms code by not providing vnew is deprecated,
    and might eventually be made impossible after all old calling code is converted
    for higher-valence bonds. [However, as of 051216 it's still called in lots of places.]
    """
    if vnew is None:
        assert s1 is s2 is None
        assert no_corrections == False
        bond_atoms_oldversion( a1, a2) # warning [obs??#k]: mol.copy might rely on this being noop when bond already exists!
        return
    # quick hack for new version, using optimized/stricter old version
    ## assert vnew in BOND_VALENCES
    assert not bonded(a1,a2)
    ## bond_atoms_oldversion(a1,a2)
    ## bond = find_bond(a1,a2)
    ## assert bond
    bond = bond_atoms_faster(a1,a2, vnew) #bruce 050513 using this in place of surrounding commented-out code
    assert bond is not None
    ## if vnew != V_SINGLE:
    ##     bond.increase_valence_noupdate( vnew - V_SINGLE)
    if not no_corrections:
        if s1 is not None:
            s1.singlet_reduce_valence_noupdate(vnew)
        if s2 is not None:
            s2.singlet_reduce_valence_noupdate(vnew) ###k
        a1.update_valence() ###k [bruce comment 050728: to fix bug 823, this needs to merge singlets to match atomtype; now it does]
        a2.update_valence()
    return bond

def bond_v6(bond):
    "Return bond.v6. Useful in map, filter, etc."
    return bond.v6

def bond_direction(atom1, atom2): #bruce 070601
    """The atoms must be bonded (assertion failure if not);
    return the bond_direction (-1, 0, or 1)
    of their bond (in the given order of atoms).
    """
    bond = find_bond(atom1, atom2)
    assert bond, "the atoms %s and %s must be bonded" % (atom1, atom2)
    return bond.bond_direction_from(atom1)

# This is an order(N) operation that produces a function which gets a
# list of potential neighbors in order(1) time. This is handy for
# inferring bonds for PDB files that lack any bonding information.
class NeighborhoodGenerator:
    """Given a list of atoms and a radius, be able to quickly take a
    point and generate a neighborhood, which is a list of the atoms
    within that radius of the point.

    Reading in the list of atoms is done in O(n) time, where n is the
    number of atoms in the list. Generating a neighborhood around a
    point is done in O(1) time. So this is a pretty efficient method
    for finding neighborhoods, especially if the same generator can
    be used many times.
    """
    def __init__(self, atomlist, maxradius, include_singlets=False):
        self._buckets = { }
        self._oldkeys = { }
        self._maxradius = 1.0 * maxradius
        self.include_singlets = include_singlets
        for atom in atomlist:
            self.add(atom)

    def _quantize(self, vec):
        """Given a point in space, partition space into little cubes
        so that when the time comes, it will be quick to locate and
        search the cubes right around a point.
        """
        maxradius = self._maxradius
        return (int(floor(vec[0] / maxradius)),
                int(floor(vec[1] / maxradius)),
                int(floor(vec[2] / maxradius)))

    def add(self, atom, _pack=struct.pack):
        buckets = self._buckets
        if self.include_singlets or not atom.is_singlet():
            # The keys of the _buckets dictionary are 12-byte strings.
            # Comparing them when doing lookups should be quicker than
            # comparisons between tuples of integers, so dictionary
            # lookups will go faster.
            i, j, k = self._quantize(atom.posn())
            key = _pack('lll', i, j, k)
            buckets.setdefault(key, []).append(atom)
            self._oldkeys[atom.key] = key

    def atom_moved(self, atom):
        """If an atom has been added to a neighborhood generator and
        is later moved, this method must be called to refresh the
        generator's position information. This only needs to be done
        during the useful lifecycle of the generator.
        """
        oldkey = self._oldkeys[atom.key]
        self._buckets[oldkey].remove(atom)
        self.add(atom)

    def region(self, center, _pack=struct.pack):
        """Given a position in space, return the list of atoms that
        are within the neighborhood radius of that position.
        """
        buckets = self._buckets
        def closeEnough(atm, radius=self._maxradius):
            return vlen(atm.posn() - center) < radius
        lst = [ ]
        x0, y0, z0 = self._quantize(center)
        for x in range(x0 - 1, x0 + 2):
            for y in range(y0 - 1, y0 + 2):
                for z in range(z0 - 1, z0 + 2):
                    # keys are 12-byte strings, see rationale above
                    key = _pack('lll', x, y, z)
                    if buckets.has_key(key):
                        lst += filter(closeEnough, buckets[key])
        return lst

    def remove(self, atom):
        key = self._quantize(atom.posn())
        try:
            self._buckets[key].remove(atom)
        except:
            pass

def inferBonds(mol):
    # not sure how big a margin we should have for "coincident"
    maxBondLength = 2.0
    # first remove any coincident singlets
    singlets = filter(lambda a: a.is_singlet(), mol.atoms.values())
    removable = { }
    sngen = NeighborhoodGenerator(singlets, maxBondLength)
    for sing1 in singlets:
        key1 = sing1.key
        pos1 = sing1.posn()
        for sing2 in sngen.region(pos1):
            key2 = sing2.key
            dist = vlen(pos1 - sing2.posn())
            if key1 != key2:
                removable[key1] = sing1
                removable[key2] = sing2
    for badGuy in removable.values():
        badGuy.kill()
    from bonds_from_atoms import make_bonds
    make_bonds(mol.atoms.values())

# ==

_changed_Bonds = {} # tracks all changes to Bonds: existence/liveness (maybe not needed), which atoms, bond order
    # (for now, maps id(bond) -> bond, since a bond's atoms and .key can change)
    #
    # Note: we don't yet have any explicit way to kill or destroy a Bond, and perhaps no Bond attrs change when a
    # Bond is removed from its atoms (I'm not sure, and it might depend on which code does it);
    # for now, this is ok, and it means those events needn't be tracked as changes to a Bond.
    # If a Bond is later given a destroy method, that should remove it from this dict;
    # If it has a kill or delete method (or one that's called when it's not on its atoms),
    # that should count as a change in this dict (and perhaps it should also change its atom attrs).
    #
    #bruce 060322 for Undo change-tracking; the related env._changed_bond_types global dict should perhaps become a subscriber

    ##e see comments about similar dicts in in chem.py for how this will end up being used

register_changedict( _changed_Bonds, '_changed_Bonds', ()) ###k related attrs arg?? #bruce 060329

_Bond_global_dicts = [_changed_Bonds]

# ==

#bruce 041109:
# Capitalized name of class Bond, so we can find all uses of it in the code;
# as of now there is only one use, in bond_atoms (used by molecule.bond).
# I also rewrote lots of the code in class Bond.

class Bond(BondBase, StateMixin):
    """A Bond is essentially a record pointing to two atoms
    (either one of which might be a real atom or a "singlet"),
    representing a bond between them if it also occurs in atom.bonds
    for each atom. It should occur in both or neither of atom.bonds
    of its two atoms, except transiently.
       The two atoms in a bond should always be different objects.
       We don't support more than one bond between the same two
    atoms; trying to add the second one will do nothing, because
    of Bond.__eq__. We don't yet support double or triple bonds...
    but [bruce 050429 addendum] soon after Alpha 5 we'll start
    supporting those, and I'll start prototyping them right now --
    DO NOT COMMIT until post-Alpha5.
       Bonds have a private member 'key' so they can be compared equal
    whenever they involve the same pair of atoms (in either order).
       Bonds sometimes store geometric info used to draw them; see
    the method setup_invalidate, which must be called when the atoms
    are changed in certain ways. Bonds don't store any selection
    state or display-mode state, and they record no info about the
    bonded molecules (but each bonded atom knows its molecule).
       Bonds are called "external" if they connect atoms in two
    different molecules, or "internal" if they connect two atoms
    in the same molecule. This affects what kind of info is
    invalidated by the private method invalidate_bonded_mols, which
    should be called by internal code whenever the bond is actually
    added to or removed from its atoms
    (or is probably about to be added or removed).
       Bonds can be removed from their atoms by Bond.bust, and then
    forgotten about (no need to kill or otherwise explicitly destroy
    them after they're not on their atoms).
    """

    pi_bond_obj = None #bruce 050718; used to memoize a perceived PiBondSpChain object (if any) which covers this bond
        # sometimes I search for pi_bond_info when I want this; see also get_pi_info and pi_info

    _s_attr_pi_bond_obj = S_CACHE # see comments in pi_bond_sp_chain.py. [bruce 060224]

    _s_attr_v6 = S_DATA
    _s_attr__direction = S_DATA #bruce 070414
    _s_attr_atom1 = S_PARENT # too bad these can change, or we might not need them (not sure, might need them for saving a file... #k)
    _s_attr_atom2 = S_PARENT

    atom1 = atom2 = _valid_data = None # make sure these attrs always have values!
    _saved_geom = None
    _direction = 0 # default value of private (except known to Atom.writemmp) instance variable for bond_direction [bruce 070414]
        # _direction is 0 for most bonds; for directional bonds [###e term to be defined elsewhere] it will be 1 if atom1 comes first,
        # or -1 if atom2 comes first, or 0 if the direction is not known.
        #    I think no code destructively swaps the atoms in a bond; if it ever does, it needs to invert self._direction too.
        # That goes for the process of mmp save/load as well, and for copying of a bond (which *might* reverse the atoms) --
        # write and read this info with care, since it's the first time in NE1 that the order of a bond's atoms will matter.
        #    This is a private attr, since its meaning depends on atom order; public access methods must be
        # passed one of self's atoms, so they can accept or return directions relative to that atom.
        #    For comments about how chains/rings of directional bonds might best be perceived,
        # for purposes of inferring directions or warning about inconsistencies,
        # see pi_bond_sp_chain.py's module docstring.
        # [bruce 070414, mostly nim ###]

    _s_attr_key = S_DATA #bruce 060405, not sure why this wasn't needed before (or if it will help now)
        # (update 060407: I don't if it did help, but it still seems needed in principle.
        #  It's change-tracked by self.changed_atoms.)

    # this default value is needed for repeated destroy [bruce 060322]
    glname = 0 
    
    def _undo_update(self): #bruce 060223 guess
        self.changed_atoms()
        self.changed_valence()
        self._changed_bond_direction() #bruce 070415
        ## self.invalidate_bonded_mols() # probably not needed, leave out at first
        # not setup_invalidate, that needs calling by our Atom's _undo_update methods ##k
        StateMixin._undo_update(self)
        
    def __init__(self, at1, at2, v6 = V_SINGLE): # no longer also called from self.rebond()
        """create a bond from atom at1 to atom at2.
        the key created will be the same whichever order the atoms are
        given, and is used to compare bonds.
        [further comments by bruce 041029:]
        Private method (that is, creating of bond objects is private, for
        affected molecules and/or atoms). Note: the bond is not actually added
        to the atoms' molecules! Caller must do that. But [new feature 041109]
        we will do all necessary invalidations, in case the new bond is indeed
        added to those atoms (as I think it always will be in the current code).
        """
        BondBase.__init__(self)
        self.atom1 = at1 ###k are these public attributes? For now I'll assume yes. [bruce 050502]
        self.atom2 = at2
        self.v6 = v6 # bond-valence times 6, as exact int; a public attribute
        assert v6 in BOND_VALENCES
        self.changed_atoms()
        self.invalidate_bonded_mols() #bruce 041109 new feature
        self.glname = env.alloc_my_glselect_name( self) #bruce 050610

    def _undo_aliveQ(self, archive): #bruce 060405, rewritten 060406; see also new_Bond_oursQ in undo_archive.py
        "[see docstring of Atom version]"
        # there are two ways to reach a bond (one per atom), so return True if either one would reach it,
        # but also report an error if one would and one would not.
        a1 = self.atom1
        a2 = self.atom2
        atm = a1; res1 = atm is not None and archive.trackedobj_liveQ(atm) and self in atm.bonds
        atm = a2; res2 = atm is not None and archive.trackedobj_liveQ(atm) and self in atm.bonds
        if res1 != res2:
            print "bug: Bond._undo_aliveQ gets different answer on each atom; relevant data:", res1, res2, self
            return True # not sure if this or False would be safer; using True so we're covered if any live atom refers to us
        return res1
##        # I don't recall if a1 and a2 can ever be None, so be safe.
##        # Warning: the following inlines Atom._undo_aliveQ for a1 and a2. [but does so wrongly as of 060406]
##        # The requirement of being in a1.bonds and a2.bonds seems necessary (and might make the __killed checks redundant),
##        # but could be removed by changing atom.unbond (and other methods??)
##        # to change us appropriately (maybe this is already done, I didn't check).
##        return a1 is not None and a2 is not None \
##               and not a1._Atom__killed and not a2._Atom__killed \
##               and self in a1.bonds and self in a2.bonds

    def bond_direction_from(self, atom): #bruce 070414
        """Assume self is a directional bond (not checked);
        return its direction, starting from the given atom
        (which must be one of its atoms).
           This is 1 if the bond direction points away from that atom,
        -1 if it points towards it, and 0 if no direction has been set.
        """
        if atom is self.atom1:
            return self._direction
        elif atom is self.atom2:
            return - self._direction
        else:
            assert 0, "%r.bond_direction_from(%r), but that bond doesn't have that atom" % (self, atom)
        return

    def bond_direction_vector(self): #bruce 070417
        """Return self's bond direction vector (in abs coords)."""
        return self._direction * (self.atom2.posn() - self.atom1.posn())

    def set_bond_direction_from(self, atom, direction, propogate = False): #bruce 070415
        """Assume self is a directional bond (not checked);
        set its direction (from atom to the other atom) to the given direction.
        The given direction must be -1, 0, or 1 (not checked);
        atom must be one of self's atoms. (The direction from the other atom
        will be the negative of the direction from the given atom.)
           If propogate is True, call this recursively in both directions
        in a chain of directional bonds, stopping only when the chain ends
        or loops back to self. This will set an entire strand or ring of
        directional bonds to the same direction.
        """
        old = self._direction
        if atom is self.atom1:
            self._direction = direction
        elif atom is self.atom2:
            self._direction = - direction
        else:
            assert 0, "%r.set_bond_direction_from(%r, %r), but that bond doesn't have that atom" % (self, atom, direction)
        if 1 or platform.atom_debug:
            # after Qt4 port and after some testing without atom_debug, this can be relaxed to "if platform.atom_debug"
            assert self.bond_direction_from(atom) == direction
            assert self.bond_direction_from(self.other(atom)) == - direction
        if old != self._direction:
            if 0 and platform.atom_debug:
                print "fyi: changed direction of %r from %r to %r" % (self, old, self._direction)
            self._changed_bond_direction()
        if propogate:
            # propogate self's direction both ways, as far as possible, overwriting any prior directions encountered
            # (and do this even if this bond's direction was already the same as the one we're setting)
            # (note: the direction being set here can be 0)
            # (note: if self can ever be a bond which *silently ignores* sets of direction,
            #  then for the following to be correct, we'd need to pass the initial direction to use,
            #  which would be an opposite one to each call. Not doing that now makes direction-switching bugs less likely
            #  or tests the default direction used by propogate_bond_direction_towards.)
            ringQ = self.propogate_bond_direction_towards(self.atom1)
            if not ringQ:
                self.propogate_bond_direction_towards(self.atom2)
        return

    def _clear_bond_direction(self): #bruce 070415
        if self._direction:
            del self._direction # let default value (0) show through
            assert not self._direction
            self._changed_bond_direction()
        return

    def _changed_bond_direction(self): #bruce 070415
        """[private method]
        Do whatever invalidations or change-notices are needed due to an internal change to self._direction.
        (See also _undo_update, which calls this, and the other self.changed*() methods.)
        """        
        # For Undo, we only worry about changes to "definitive" (not derived) state. That's only in self.
        # Since Bonds use an optimized system for changetracking, we have to store self in a dictionary.
        _changed_Bonds[id(self)] = self # tells Undo that something in this bond has changed
        
        # Someday, doing that should also cover all modification notices to model object containers that contain us,
        # such as the file we're saved in. It might already do that, but I'm not sure, so do that explicitly:
        self.changed()
        
        # For appearance changes, we need to be far-reaching enough
        # to hit Ax atoms which color themselves based on attached strand directions.
        #
        # In all, the bonds that need to know (re appearance or warnings) are self and the touching non-directional bonds,
        # and the atoms that need to know are all the atoms on that set of bonds.
        # [And *maybe* the touching directional bonds should know, if they (not just atoms in the middle)
        # might draw differently if their direction is inconsistent with that of a neighboring directional bond.
        # For now I'll assume that won't happen and leave it out.]
        #
        # I think there are no Atom and Bond methods for "changed appearance for miscellaneous causes",
        # so for the atoms we just tell their Chunk that they need redrawing, and for bonds we just tell their atoms
        # (i.e. their atoms' chunks). That should be fixed (or better yet, this whole scheme scrapped and replaced
        #  with per-attr change/usage tracking, like in the exprs module), but for now, just handle it directly
        # on the set of atoms we need to change. [BTW, this is inefficient compared to extending something
        # like bond_updater to do this in a batch manner from a global dictionary of changed bonds. That's ok for now. #e]
        dict1 = {}
        def collect(atom):
            dict1[id(atom)] = atom
        for atom in (self.atom1, self.atom2):
            for bond in atom.bonds:
                #e don't bother checking bond.is_directional(), just catch them all,
                # tho as explained above we only need the non-directional ones for now
                #k Need to inval anything directly on the bond? I don't think so --
                # geometric info has not changed, appearance is not cached except
                # by whatever draws the atoms (handled by the changeapp calls below).
                collect(bond.atom1)
                collect(bond.atom2)
        for atom in dict1.itervalues():
            atom.molecule.changeapp(0) # why is this not an Atom method?
            #e need to call anything else?
            # What about atom._changed_structure? I think it's not related.
        return

    def propogate_bond_direction_towards(self, atom): #bruce 070414
        """Copy the bond_direction on self (which must be a directional bond)
        onto all bonds in the same chain or ring of directional bonds
        in the direction (from self) of atom (which must be one of self's atoms).
           Stop when reaching self (in a ring) or the last bond in a chain.
        (Note that this means we *don't* change bonds *before* self in a chain,
         unless it's a ring; to change all bonds in a chain we have to be called twice.)
        Don't modify self's own direction.
        Do all necessary change-notification.
           Return ringQ, a boolean which is True if self is part of a ring
        (as opposed to a linear chain) of directional bonds.
        """
        backdir = self.bond_direction_from(atom) # measured backwards, relative to direction in which we're propogating
        ringQ, listb, lista = grow_directional_bond_chain(self, atom)
        for b, a in zip(listb, lista):
            b.set_bond_direction_from(a, backdir)
        return ringQ

    def is_directional(self): #bruce 070415  #e this might be replaced with an auto-updated attribute, self.directional
        """Does self have the atomtypes and bond order that make it want to have a direction?
        Note: open bonds never count as directional, since that can lead to them getting directions
        which become illegal when something is deposited on them (like Ax), and can lead to an atom with
        three directional bonds but no errors (which confuses or needlessly complicates related algorithms).
        """
        if self.atom1.element.symbol in DIRECTIONAL_BOND_ELEMENTS and \
           self.atom2.element.symbol in DIRECTIONAL_BOND_ELEMENTS:
            return True
        return False

    def mmprecord_bond_direction(self, atom, mapping): #bruce 070415
        """Return an mmp record line or lines (not including terminating \n)
        which identifies self (which has already been written into the mmp file,
        along with both its atoms, just after the given atom was written),
        and encodes the direction of self,
        using mapping (a writemmp_mapping(sp?) object) to find atom codes.
           Note that this API makes no provision for writing one record
        to encode the direction of more than one bond at a time
        (e.g. an entire strand). However, the record format we're writing
        could support that, and the mmp reading code we're adding at the same time
        does support that.
        """
        # We'll support a bond_direction record which only writes atoms in bond_direction order.
        # That way we needn't write out the direction itself, and the record format permits encoding
        # a bond-chain in one record listing a chain of atomcodes
        # (though we don't yet take advantage of that when writing).
        other = self.other(atom)
        direction = self.bond_direction_from(atom)
        assert direction # otherwise we should not be writing this record (#e could extend API to let us return "" in this case)
        if direction < 0:
            atom, other = other, atom
        atomcodes = map( mapping.encode_atom, (atom, other) )
        return "bond_direction " + " ".join(atomcodes)
    
    def getToolTipInfo(self, glpane, isBondChunkInfo, isBondLength, atomDistPrecision): #Ninad 060830
        '''Returns a string that has bond related info ...used in DynamicTool Tip'''
        ###WARNING: this method uses both self and glpane.selobj, and appears to assume they are the same object. [bruce 070414 comment]
        #ninad060830 moved these methods from the class DynamicTip
        bondStr = str(glpane.selobj)
        bondInfoStr = bondStr
        # check for user pref 'bond_chunk_info'
        if isBondChunkInfo:
            bondChunkInfo = self.getBondChunkInfo(glpane)
            bondInfoStr +=  "\n" + bondChunkInfo
        #check for user pref 'bond length'
        if isBondLength:
            bondLength = self.getBondLength(glpane, atomDistPrecision)
            bondInfoStr += "\n" + bondLength #ninad060823  don't use "<br>" ..it is weird. doesn'tr break into a new line.
                                                                #perhaps because I am not using htmp stuff in getBonndLength etc functions??
        return bondInfoStr
            
    def getBondChunkInfo(self, glpane, quat = Q(1,0,0,0)): #Ninad 060830
        ''' returns chunk information of the atoms forming a bond. Returns none if Bond chunk user pref is unchecked.
        It uses some code of bonded_atoms_summary method
        '''
        ###WARNING: this method does not use self, and appears to assume glpane.selobj can stand in for self.  [bruce 070414 comment]
        a1 = glpane.selobj.atom1
        a2 = glpane.selobj.atom2
        chunk1 = a1.molecule.name
        chunk2 = a2.molecule.name
            
            #ninad060822 I am not checking if chunk 1 and 2 are the same.
            #I think it's not needed as the tooltip string won't be compact
            #even if it is implemented. so leaving it as is
        bondChunkInfo = str(a1) + " in [" + str(chunk1) + "]\n" + str(a2) + " in [" + str(chunk2) + "]"
        return bondChunkInfo
            
    def getBondLength(self, glpane, atomDistPrecision):#Ninad 060830
        '''returns the atom center distance between the atoms connected by the highlighted bond.
        Note that this does *not* return the covalent bondlength'''
        ###WARNING: this method does not use self, and appears to assume glpane.selobj can stand in for self.  [bruce 070414 comment]

        a1 = glpane.selobj.atom1
        a2 = glpane.selobj.atom2

        nuclearDist = str(round(vlen(a1.posn() - a2.posn()), atomDistPrecision))
        bondLength = "Distance " + str(a1) + "-" + str(a2) + ": " + nuclearDist + " A"
        return bondLength

    
    def destroy(self): #bruce 060322 (not yet called) ###@@@
        """[see comments in Atom.destroy docstring]
        """
        if self._direction:
            self._changed_bond_direction() #bruce 070415
        env.dealloc_my_glselect_name( self, self.glname )
        key = id(self)
        for dict1 in _Bond_global_dicts:
            dict1.pop(key, None)
        if self.pi_bond_obj is not None:
            self.pi_bond_obj.destroy() ###k is this safe, if that obj and ones its knows are destroyed?
            ##e is this also needed in self.changed_atoms or changed_valence??? see if bond orientation bugs are helped by that...
            #####@@@@@ [bruce 060322 comments]
        self.__dict__.clear() ###k is this safe??? [see comments in Atom.destroy implem for ways we might change this ##e]
        return
    
    def is_open_bond(self): #bruce 050727
        return self.atom1.element is Singlet or self.atom2.element is Singlet
    
    def set_v6(self, v6): #bruce 050717 revision: only call changed_valence when needed
        "#doc; can't be used for illegal valences, as some of our actual setters need to do..."
        assert v6 in BOND_VALENCES
        if self.v6 != v6:
            self.v6 = v6
            self.changed_valence()
        return

    def reduce_valence_noupdate(self, vdelta, permit_illegal_valence = False):
        # option permits in-between, 0, or negative(?) valence
        """Decrease this bond's valence by at most vdelta (which must be nonnegative),
        but always to a supported value in BOND_VALENCES (unless permit_illegal_valence is true);
        return the actual amount of decrease (maybe 0; in the same scale as BOND_VALENCES).
           When permit_illegal_valence is true, any valence can be reached, even one which
        is lower than any permitted valence, zero, or negative (###k not sure that's good, or ever tried).
           [The starting valence (self.v6) need not be a legal one(??); but by default
        the final valence must be legal; not sure what should happen if no delta in [0,vdelta] makes
        it legal! For now, raise an AssertionError(?) exception then. #####@@@@@]
        """
        # we want the lowest permitted valence which is at least v_have - vdelta, i.e. in the range v_want to v_have.
        # This code is very similar to that of increase_valence_noupdate, but differs in a few important places!
        assert vdelta >= 0
        v_have = self.v6
        v_want = v_have - vdelta
        if not permit_illegal_valence:
            # make v_want legal (or raise exception if that's not possible)
            did_break = else_reached = 0
            for v_to_try in BOND_VALENCES: # this list is in lowest-to-highest order
                if v_want <= v_to_try <= v_have: # warning: order of comparison will differ in the sister method for "increase"
                    v_want = v_to_try # good thing we'll break now, since this assignment alters the meaning of the loop-test
                    did_break = 1
                    break
            else:
                else_reached = 1
                if platform.atom_debug:
                    print "atom_debug: else clause reached"
                    # i don't know python's rules about this; it might relate to #iters == 0
            if platform.atom_debug:
                if not (did_break != else_reached):
                    # this is what I hope it means (whether we fell out the end or not) but fear it doesn't
                    print "atom_debug: i hoped for did_break != else_reached but it's not true"
            if not did_break:
                # no valence is legal! Not yet sure what to do in this case. (Or whether it ever happens.)
                assert 0, "no valence reduction of %r from 0 to vdelta %r is legal!" % (v_have, vdelta)
            assert v_want in BOND_VALENCES # sanity check
        # now set valence to v_want
        if v_want != v_have:
            self.v6 = v_want
            self.changed_valence()
        return v_have - v_want # return actual decrease (warning: order of subtraction will differ in sister method)

    def increase_valence_noupdate(self, vdelta, permit_illegal_valence = False): #k is that option needed?
        """Increase this bond's valence by at most vdelta (which must be nonnegative),
        but always to a supported value in BOND_VALENCES (unless permit_illegal_valence is true);
        return the actual amount of increase (maybe 0; in the same scale as BOND_VALENCES).
           When permit_illegal_valence is true, any valence can be reached, even one which
        is higher than any permitted valence (###k not sure that's good, or ever tried).
           [The starting valence (self.v6) need not be a legal one(??); but by default
        the final valence must be legal; not sure what should happen if no delta in [0,vdelta] makes
        it legal! For now, raise an AssertionError(?) exception then. #####@@@@@]
        """
        # we want the highest permitted valence which is at most v_have + vdelta, i.e. in the range v_have to v_want.
        # This code is very similar to that of reduce_valence_noupdate but several things are reversed.
        assert vdelta >= 0
        v_have = self.v6
        v_want = v_have + vdelta
        if not permit_illegal_valence:
            # make v_want legal (or raise exception if that's not possible)
            did_break = else_reached = 0
            for v_to_try in BOND_VALENCES_HIGHEST_FIRST: # this list is in highest-to-lowest order, unlike BOND_VALENCES
                if v_have <= v_to_try <= v_want: # warning: order of comparison differs in sister method
                    v_want = v_to_try # good thing we'll break now, since this assignment alters the meaning of the loop-test
                    did_break = 1
                    break
            else:
                else_reached = 1
                if platform.atom_debug:
                    print "atom_debug: else clause reached in increase_valence_noupdate"
            if platform.atom_debug:
                if not (did_break != else_reached):
                    print "atom_debug: i hoped for did_break != else_reached but it's not true, in increase_valence_noupdate"
            if not did_break:
                # no valence is legal! Not yet sure what to do in this case. (Or whether it ever happens.)
                assert 0, "no valence increase of %r from 0 to vdelta %r is legal!" % (v_have, vdelta)
            assert v_want in BOND_VALENCES # sanity check
        # now set valence to v_want
        if v_want != v_have:
            self.v6 = v_want
            if debug_1951:
                print "debug_1951: increase_valence_noupdate changes %r.v6 from %r to %r, returns %r" % \
                      (self, v_have, v_want, v_want - v_have)
            self.changed_valence()
        return v_want - v_have # return actual increase (warning: order of subtraction differs in sister method)

    def changed_valence(self):
        """[private method]
        This should be called whenever this bond's valence is changed
        (whether to a legal or (presumably temporary) illegal value).
        It does whatever invalidations that requires, but does no "updates".
        """
        ###e update geometric things, using setup_invalidate?? ###@@@
        self.setup_invalidate() # not sure this is needed, but let's do it to make sure it's safe if/when it's needed [bruce 050502]
            # as of 060324, it's needed, since sim.getEquilibriumDistanceForBond depends on it
        # tell the atoms we're doing this
        self.atom1._modified_valence = self.atom2._modified_valence = True # (this uses a private attr of class atom; might be revised)
        if self.atom1.molecule is self.atom2.molecule:
            # we're in that molecule's display list, so it needs to know we'll look different when redrawn
            self.atom1.molecule.changeapp(0)
        else:
            # Fix for bug 886 [bruce 050811]:
            # Both atoms might look different if whether they have valence errors changes (re bug 886),
            # so if valence errors are presently being displayed, invalidate both of their display lists.
            # If valence errors are not being displayed, I think we don't have to inval either display list,
            # but I'm not sure, so to be safe for A6, just do it regardless. Potential optim: check whether
            # presence of valence error actually changes, for each atom. (But it often does, so nevermind for now.)
            self.atom1.molecule.changeapp(0)
            self.atom2.molecule.changeapp(0)
        from env import _changed_bond_types #bruce 050726
        _changed_bond_types[id(self)] = self
        _changed_Bonds[id(self)] = self #bruce 060322 (covers changes to self.v6)
        return

    def changed(self): #bruce 050719
        """Mark this bond's atoms (and thus their chunks, part, and mmp file) as changed.
        (As of 050719, only the file (actually the assy object) records this fact.)
        """
        self.atom1.changed()
        self.atom2.changed() # for now, only the file (assy) records this, so 2nd call is redundant, but someday that will change.
        return

    def numeric_valence(self): # has a long name so you won't be tempted to use it when you should use .v6 ###@@@ not yet used?
        return self.v6 / 6.0
    
    def changed_atoms(self):
        """Private method to call when the atoms assigned to this bond are changed.
        WARNING: does not call setup_invalidate(), though that would often also
        be needed, as would invalidate_bonded_mols() both before and after the change.
        """
        _changed_Bonds[id(self)] = self #bruce 060322 (covers changes to atoms, and __init__)
        at1 = self.atom1
        at2 = self.atom2
        at1._changed_structure() #bruce 050725
        at2._changed_structure()
        assert at1 is not at2
        self.key = 65536*min(at1.key,at2.key)+max(at1.key,at2.key) # used only in __eq__ as of 051018; problematic (see comments there)
        
##        #bruce 050608: kluge (in how it finds glpane and thus assumes just one of them is used; and since key is not truly unique)
##        self.atom1.molecule.assy.w.glpane.glselect_objs[self.key] = self #e dict should be stored in assy (or so) instead
##            ###@@@ not key, use other attr name for that, obj.glname or glselect_name or so...
        #bruce 050317: debug warning for interpart bonds, or bonding killed atoms/chunks,
        # or bonding to chunks not yet added to any Part (but not warning about internal
        # bonds, since mol.copy makes those before a copied chunk is added to any Part).
        #   This covers new bonds (no matter how made) and the .rebond method.
        #   Maybe this should be an actual error, or maybe it should set a flag so that
        # involved chunks are checked for interpart bonds when the user event is done
        # (in case caller plans to move the chunks into the same part, but hasn't yet).
        # It might turn out this happens a lot (and is not a bug), if callers make a
        # new chunk, bond to it, and only then add it into the tree of Nodes.
        if platform.atom_debug and at1.molecule is not at2.molecule:
            if (at1.molecule.assy is None) or (at2.molecule.assy is None): #bruce 050519 fixed 'is not' -> 'is' (recent typo, i presume)
                print_compact_stack( "atom_debug: bug?: bonding to a killed chunk(?); atoms are: %r, %r" % (at1,at2))
            elif (at1.molecule.part is None) or (at2.molecule.part is None): #bruce 050519 fixed 'is not' -> 'is'
                if 0: #bruce 050321 this happens a lot when reading an mmp file, so disable it for now
                    print_compact_stack( "atom_debug: bug or fyi: one or both Parts None when bonding atoms: %r, %r" % (at1,at2))
            elif at1.molecule.part is not at2.molecule.part:
                print_compact_stack( "atom_debug: likely bug: bonding atoms whose parts differ: %r, %r" % (at1,at2))

        if self._direction and not self.is_directional(): #bruce 070415
            self._clear_bond_direction()
        return
    
    def invalidate_bonded_mols(self): #bruce 041109
        """Private method to call when a bond is made or destroyed;
        knows which kinds of bonds are put into a display list by molecule.draw
        (internal bonds) or put into mol.externs (external bonds),
        though this knowledge should ideally be private to class molecule.
        """
        # assume mols are not None (they might be _nullMol, that's ok);
        # if they are, we'll detect the error with exceptions in either case below
        mol1 = self.atom1.molecule
        mol2 = self.atom2.molecule
        if mol1 is not mol2:
            # external bond
            mol1.invalidate_attr('externs')
            mol2.invalidate_attr('externs')
        else:
            # internal bond
            mol1.havelist = 0
        return

    # ==
    
    def setup_invalidate(self): # revised 050516
        """Semi-private method for bonds -- used by code in Bond, atom and chunk classes.
        Invalidates cached geometric values related to drawing the bond.
           This must be called whenever the position or element of either bonded
        atom is changed, or when either atom's molecule changes if this affects
        whether it's an external bond (since the coordinate system used for drawing
        is different in each case), UNLESS either bonded chunk's invalidate_all_bonds()
        methods is called (which increment a counter checked by our __getattr__).
         (FYI: It need not be called for other changes that might affect bond
        appearance, like disp or color of bonded molecules, though for internal
        bonds, the molecule's .havelist should be reset when those things change.)
         (It's not yet clear whether this needs to be called when bond-valence is changed.
        If it does, that will be done from one place, the changed_valence() method. [bruce 050502])
          Note that before the "inval/update" revisions [bruce 041104],
        self.setup() (the old name for this method, from point of view of callers)
        did the recomputation now done on demand by __setup_update; now this method
        only does the invalidation which makes sure that recomputation will happen
        when it's needed.
        """
        self._valid_data = None
        # For internal bonds, or bonds that used to be internal,
        # callers need to have reset havelist of affected mols,
        # but the changes in atoms that required them to call setup_invalidate
        # mean they should have done that anyway (except for bond making and
        # breaking, in this file, which does this in invalidate_bonded_mols).
        # Bruce 041207 scanned all callers and concluded they do this as needed,
        # so I'm removing the explicit resets of havelist here, which were often
        # more than needed since they hit both mols of external bonds.
        # This change might speed up some redraws, esp. in move or deposit modes.
        return

    def bond_to_abs_coords_quat(self): #bruce 050722
        """Return a quat which can be used (via .rot) to rotate vectors from this bond's drawing coords into absolute coords.
        (There is no method abs_to_bond_coords_quat which goes the other way -- just use .unrot for that.)
        FYI: as of 050722, this is identity for external bonds, and chunk.quat for internal bonds.
        """
        atom1 = self.atom1
        atom2 = self.atom2
        if atom1.molecule is not atom2.molecule:
            return Q(1,0,0,0)
        return atom1.molecule.quat
        
    def _recompute_geom(self, abs_coords = False): #bruce 050516 made this from __setup_update
        """[private method meant for our __getattr__ method, and for writepov]
        Recompute and return (but don't store)
        the 6-tuple (a1pos, c1, center, c2, a2pos, toolong),
        which describes this bond's geometry, useful for drawing (OpenGL or writepov)
        and for self.ubp().
           If abs_coords is true, always use absolute coords;
        otherwise, use them only for external bonds, and for internal bonds
        (i.e. between atoms in the same mol) use mol-relative coords.
        """
        atom1 = self.atom1
        atom2 = self.atom2
        if abs_coords or (atom1.molecule is not atom2.molecule):
            # external bond; use absolute positions for all attributes.
            a1pos = atom1.posn()
            a2pos = atom2.posn()
        else:
            # internal bond; use mol-relative positions for all attributes.
            # Note [bruce 041115]: this means any change to mol's coordinate system
            # (basecenter and quat) requires calling setup_invalidate
            # in this bond! That's a pain (and inefficient), so I might
            # replace it by a __getattr__ mol-coordsys-version-number check...
            # [and sometime after that, before 050719, I did.]
            a1pos = atom1.baseposn() #e could optim, since their calcs of whether basepos is present are the same
            a2pos = atom2.baseposn()
        return self.geom_from_posns(a1pos, a2pos)

    def geom_from_posns(self, a1pos, a2pos): #bruce 050727 split this out
        """Return a geometry tuple from the given atom positions
        (ignoring our actual atom positions but using our actual atomtypes/bondtype).
        Correct for either absolute or mol-relative positions
        (return value will be in same coordinate system as arg positions).
        """
        vec = a2pos - a1pos
        leng = 0.98 * vlen(vec) # 0.98 makes it a bit less common that we set toolong below [bruce 050516 comment]
        vec = norm(vec)
            #e possible optim, don't know if it matters:
            # norm could be inlined, since we already have vlen;
            # but what would really be faster (I suspect) is to compute these
            # bond params for all internal bonds in an entire chunk at once, using Numeric. ###@@@
            # [bruce 050516]
        # (note: as of 041217 rcovalent is always a number; it's 0.0 for Helium,
        #  etc, so for nonsense bonds like He-He the entire bond is drawn as if "too long".)
##        rcov1 = self.atom1.atomtype.rcovalent
##        rcov2 = self.atom2.atomtype.rcovalent
        rcov1, rcov2 = bond_params(self.atom1.atomtype, self.atom2.atomtype, self.v6)
            #bruce 060324 experiment re bug 900
        c1 = a1pos + vec*rcov1
        c2 = a2pos - vec*rcov2
        toolong = (leng > rcov1 + rcov2)
        center = (c1 + c2) / 2.0 # before 041112 this was None when toolong
        return a1pos, c1, center, c2, a2pos, toolong
    
    def __getattr__(self, attr): # Bond.__getattr__ #bruce 041104; totally revised 050516
        """Return attributes related to bond geometry, recomputing them if they
        are not stored or if the stored ones are no longer valid.
           For all other attr names, raise an AttributeError (quickly, for __xxx__ names).
        """
        try:
            return BondBase.__getattr__(self, attr)
        except AttributeError:
            pass
        if attr[0] == '_':
            raise AttributeError, attr # be fast since probably common for __xxx__
        # after this, attr is either an updated_attr or a bug, so it's ok to assume we need to recompute if invalid...
        # if any of the attrs used by recomputing geom are missing, we'll get infinite recursion;
        # these are just atom1, atom2, and the ones used herein.
        current_data = (self.atom1.molecule.bond_inval_count, self.atom2.molecule.bond_inval_count)
        if self._valid_data != current_data:
            # need to recompute
            # (note: to inval this bond alone, set self._valid_data = None; this is required if you
            #  change anything used by _recompute_geom, unless you change bond_inval_count for one of
            #  the bonded chunks.)
            self._valid_data = current_data # do this first, even if exception in _recompute_geom()
            self._saved_geom = geom = self._recompute_geom()
        else:
            geom = self._saved_geom # when valid, should always have been computed, thus be of proper length
        if attr == 'geom':
            return geom # callers desiring speed should use this case, to get several attrs but only check validity once
        elif attr == 'a1pos':
            return geom[0]
        elif attr == 'c1':
            return geom[1]
        elif attr == 'center':
            return geom[2]
        elif attr == 'c2':
            return geom[3]
        elif attr == 'a2pos':
            return geom[4]
        elif attr == 'toolong':
            return geom[5]
        elif attr == 'axis': # a2pos - a1pos (not normalized); in relative coords [bruce 050719 new feature]
            return geom[4] - geom[0]
        else:
            raise AttributeError, attr
        pass

    # ==
    
    def get_pi_info(self, **kws): #bruce 050718
        """Return the pi orbital orientation/occupancy info for this bond, if any [#doc the format], or None
        if this is a single bond (which is not always a bug, e.g. in -C#C- chains, if we someday extend the
        subrs this calls to do any bond inference -- presently they just trust the existing bond order, self.v6).
           This info might be computed, and perhaps stored, or stored info might be used. It has to be computed
        all at once for all pi bonds in a chain connected by sp atoms with 2 bonds.
           If computed, and if it's partly arbitrary, **kws (out/up) might be used.
        """
        if platform.atom_debug:
            import pi_bond_sp_chain, debug
            debug.reload_once_per_event(pi_bond_sp_chain) #bruce 050825 use reload_once_per_event to remove intolerable slowdown
        from pi_bond_sp_chain import bond_get_pi_info
        return bond_get_pi_info(self, **kws) # no need to pass an index -- that method can find one on self if it stored one
    
    def potential_pi_bond(self): #bruce 050718
        "given our atomtypes, are we a potential pi bond?"
        return self.atom1.atomtype.spX < 3 and self.atom2.atomtype.spX < 3
    
    # ==
    
    def other(self, atm):
        """Given one atom the bond is connected to, return the other one
        """
        if self.atom1 is atm: return self.atom2
        assert self.atom2 is atm #bruce 041029
        return self.atom1

    def othermol(self, mol): #bruce 041123; not yet used or tested
        """Given the molecule of one atom of this bond, return the mol
        of the other one. Error if mol is not one of the bonded mols.
        Note that this implies that for an internal bond within mol,
        the input must be mol and we always return mol.
        """
        if mol is self.atom1.molecule:
            return self.atom2.molecule
        elif mol is self.atom2.molecule:
            return self.atom1.molecule
        else:
            assert mol in [self.atom1.molecule, self.atom2.molecule]
            # this always fails (so it's ok if it's slow) -- it's just our "understandable error message"
        pass
    
    def ubp(self, atom):
        """unbond point (atom must be one of the bond's atoms)
        [Note: this is used to make replacement
        singlets in atom.unbond and atom.kill methods, even if they'll be
        discarded right away as all atoms in some big chunk are killed 1 by 1.]
        """
        #bruce 041115 bugfixed this for when mol.quat is not 1,
        # tho i never looked for or saw an effect from the bug in that case
        if atom is self.atom1:
            point = self.c1 # this might call self.__setup_update()
        else:
            assert atom is self.atom2
            point = self.c2
        # now figure out what coord system that's in
        if self.atom1.molecule is not self.atom2.molecule:
            return point
        else:
            # convert to absolute position for caller
            # (note: this never recomputes basepos/atpos or modifies the mol-
            #  relative coordinate system)
            return self.atom1.molecule.base_to_abs(point)
        pass

    # "break" is a python keyword
    def bust(self, make_bondpoints = True): #bruce 070601 added make_bondpoints feature (was effectively always True before)
        """Destroy this bond, modifying the bonded atoms as needed
        (by adding singlets in place of this bond, in most cases (unless make_bondpoints is false) --
         note that the newly added singlets might overlap in space!),
        and invalidating the bonded molecules as needed.
           Return the added singlets as a 2-tuple.
        (This method is named 'bust' since 'break' is a python keyword.)
        If either atom is a singlet, kill that atom.
        (Note: as of 041115 bust is never called with either atom a singlet.
        If it ever is, retval remains a 2-tuple but has None in 1 or both
        places ... precise effect needs review in that case.)
        """
        # bruce 041115: bust is never called with either atom a singlet,
        # but since atom.unbond now kills singlets lacking any bonds,
        # and since not doing that would be bad, I added a note about that
        # to the docstring.
        self._clear_bond_direction() #bruce 070415
        x1 = self.atom1.unbond(self, make_bondpoint = make_bondpoints) # does all needed invals
        x2 = self.atom2.unbond(self, make_bondpoint = make_bondpoints)
        ###e do we want to also change our atoms and key to None, for safety?
        ###e check all callers and decide -- in case some callers reuse the bond or for some reason still need its atoms
        return x1, x2 # retval is new feature, bruce 041222

    def rebond(self, old, new):
        """Self is a bond between old (typically a singlet) and some atom A;
        replace old with new in this same bond (self),
        so that old no longer bonds to A but new does.
           The bond-valence of self is not used or changed, even if it would be
        incorrect for the new atomtypes used in the bond.
           Unlike some other bonding methods, the number of bonds on new increases
        by 1, since no singlet on new is removed -- new is intended to be
        a just-created atom, not one with the right number of existing bonds.
        If old is a singlet, then kill it since it now has no bonds.
        Do the necessary invalidations in self and all involved molecules.
           Warning: this can make a duplicate of an existing bond (so that
        atoms A and B are connected by two equal copies of a bond). That
        situation is an error, not supported by the code as of 041203,
        and is drawn exactly as if it was a single bond. Avoiding this is
        entirely up to the caller.
        """
        # [bruce 041109 added docstring and rewrote Josh's code:]
        # Josh said: intended for use on singlets, other uses may have bugs.
        # bruce 041109: I think that means "old" is intended to be a singlet.
        # I will try to make it safe for any atoms, and do all needed invals.
        if self.atom1 is old:
            old.unbond(self) # also kills old if it's a singlet, as of 041115
            ## if len(old.bonds) == 1: del old.molecule.atoms[old.key] --
            ## the above code removed the singlet, old, without killing it.
            self.atom1 = new
        elif self.atom2 is old:
            old.unbond(self)
            self.atom2 = new
        else:
            print "fyi: bug: rebond: %r doesn't contain atom %r to replace with atom %r" % (self, old, new)
            # no changes in the structure
            return
        # bruce 041109 worries slightly about order of the following:
        # invalidate this bond itself
        self.changed_atoms()
        self.setup_invalidate()
        # add this bond to new (it's already on A, i.e. in the list A.bonds)
        new.bonds.append(self)
            #e put this in some private method on new, new.add_new_bond(self)??
            #  Note that it's intended to increase number of bonds on new,
            #  not to zap a singlet already bonded to new.
        # Invalidate molecules (of both our atoms) as needed, due to our existence
        self.invalidate_bonded_mols()
        #bruce 050728: this is needed so depositmode (in atom.make_enough_bondpoints)
        # can depend on bond.get_pi_info() being up to date:
        if self.pi_bond_obj is not None:
            self.pi_bond_obj.destroy() ###e someday this might be more incremental if that obj provides a method for it;
                # or we could call changed_structure on the two atoms of self, like bond updating code will do upon next redraw.
        if 1:
            # This debug code helped catch bug 232, but seems useful in general:
            # warn if this bond is a duplicate of an existing bond on A or new.
            # (Usually it will have the same count on each atom, but other bugs
            #  could make that false, so we check both.) [bruce 041203]
            A = self.other(new)
            if A.bonds.count(self) > 1:
                print "rebond bug (%r): A.bonds.count(self) == %r" % (self, A.bonds.count(self))
            if new.bonds.count(self) > 1:
                print "rebond bug (%r): new.bonds.count(self) == %r" % (self, new.bonds.count(self))
        return

    ####@@@@ bruce 050513 comment: should seriously consider removing these __eq__/__ne__ methods
    # and revising bond_atoms accordingly (as an optim). One use of them is probably in a .count method in another file.
    #
    #bruce 051018 comment: I think this __eq__ might have bugs, once enough atoms have been defined (not nec. all at once)
    # to overflow the constant 65536 used to compute self.key! For example, if the atkeys are (2,3) or (1,65536+3) we'll
    # think the bonds are equal! OTOH, does this matter unless the bonds share an atom? But even if it only matters then,
    # it might hurt us if the shared atom is min in one bond and max in the other... I didn't yet find an example, nor prove
    # there isn't one. Surely the whole thing should be removed unless it can be made clearly correct... #####@@@@@
    # Would it be just as good, and provably ok (given the assumption that only bonds on the same atom are compared),
    # if the key was just the sum of the atom keys?? I think so!
    #
    #bruce 060209 comment: these now override different defs in UndoStateMixin. This is wrong in theory (since the undo system
    # assumes those defs will be used), but I can't yet think of bugs it will cause, and it's probably also still necessary
    # due to how the atom-bonding code works. Wait, I bet the debug print in here would print if it could ever make a difference,
    # which means, I could probably take them out... ok, I'll try that soon, but not exactly now. #######@@@@@@@
    
    def __eq__(self, ob):
        if not isinstance(ob, Bond): return False
        if (self is not ob) and ob.key == self.key:
            # This seems to never happen, so let's find out if anyone ever sees it (by printing stack even when not atom_debug).
            # It could happen in two ways: a true bug (keys same but atoms different),
            # or an intentional use of the deprecated feature of two Bonds with same atoms comparing equal.
            # If it indeed never happens (or if it does and we fix that), then I'll remove or reimplement __eq__
            # to just return "self is ob". ####@@@@ [bruce 051018]
            # [as of bruce 060406, i never saw this, but today's changes to undo could bring it on,
            #  so i'll leave it in (msg and implem) for A7.]
            # update, bruce 070601: this does sometimes happen, for unknown reasons, but probably repeatably.
            # At least one bug report mention it. It has no known harmful effects (and by now I forget whether
            # it's predicted to have any -- the comment above suggests it's not, it just means a certain optimization
            # in __eq__ would be an illegal change). When it does happen it may not be an error (but this is not yet
            # known) -- it may involve some comparison by undo of old and new bonds between the same atoms
            # (a speculation; but the tracebacks seem to always mention undo, and the atoms in the bonds seem to be the same).
            # So -- I'll print a much worse message if the atoms differ, and if not only print it when ATOM_DEBUG.
            if (self.atom1 is ob.atom1 and self.atom2 is ob.atom2) or \
               (self.atom1 is ob.atom2 and self.atom2 is ob.atom1):
                # atoms same -- probably not a bug at all
                if platform.atom_debug:
                    print_compact_stack( "debug: fyi: different bond objects (on same atoms) equal: %r == %r: " % (self,ob) )
            else:
                # different atoms -- VERY bad (not known to ever happen, but I tested this error-reporting code anyway)
                msg = "BUG: different bond objects, between different atoms, compare equal: %r == %r" % (self,ob)
                print_compact_stack(msg + ": ")
                env.history.message(redmsg(quote_html(msg)))
        else:
            if 0 and platform.atom_debug: #bruce 051216; disabled it since immediately found a call (using Build mode)
                #bruce 070601 comment: I suspect this happens when asking "bond in atom.bonds" when making a new bond.
                print_compact_stack( "atom_debug: deprecated Bond.__eq__ was called on %r and %r: " % (self,ob) )
        return ob.key == self.key

    def __ne__(self, ob):
        # bruce 041028 -- python doc advises defining __ne__ whenever you define __eq__;
        # on 060228 i confirmed this is needed by test (otherwise != doesn't call __eq__)
        return not self.__eq__(ob)

##    def _check_assertions(self, whocalls = ""): #bruce for DEBUG_070602; WARNING: slow even when all is ok; only for debugging
##        if whocalls:
##            prefix = "bug (%s)" % whocalls
##        else:
##            prefix = "bug"
##        for atom in (self.atom1, self.atom2):
##            if self not in atom.bonds:
##                print "%s: %r not in %r.bonds" % (prefix, self, atom)
##        return
        
    def draw(self, glpane, dispdef, col, level, highlighted = False, bool_fullBondLength = False): #bruce 050727 moving implem to separate file
        """Draw the bond. Note that for external bonds, this is called twice,
        once for each bonded molecule (in arbitrary order)
        (and is never cached in either mol's display list);
        each of these calls gets dispdef, col, and level from a different mol.
        [bruce, 041104, thinks that leads to some bugs in bond looks.]
           Bonds are drawn only in certain display modes (CPK, LINES, TUBES).
        The display mode is inherited from the atoms or molecule (as passed in
        via dispdef from the calling molecule -- this might cause bugs if some
        callers change display mode but don't set havelist = 0, but maybe they do).
        Lines or tubes change color from atom to atom, and are red in the middle
        for long bonds. CPK bonds are drawn in the calling molecule's color or
        in the user pref color whose default value used to be called bondColor (which is light gray).
           Note that all drawing coords are based on either .posn or .baseposn
        of the atoms, according to whether this is an external or internal bond,
        and the caller has to draw those kinds of bonds in the proper coordinate
        system (absolute or mol-relative for external or internal bonds respectively).
        """
        #Note: bool_fullBondLength represent whether full bond length to be drawn
        #it is used only in select Chunks mode while highlighting the whole chunk and when
        #the atom display is Tubes display -- ninad 070214
        
        #bruce 041104 revised docstring, added comments about possible bugs.
        # Note that this code depends on finding the attrs toolong, center,
        # a1pos, a2pos, c1, c2, as created by self.__setup_update().
        # As of 041109 this is now handled by bond.__getattr__.
        # The attr toolong is new as of 041112.
        if platform.atom_debug:
            import bond_drawer, debug
            debug.reload_once_per_event( bond_drawer) #bruce 050825 use reload_once_per_event to remove intolerable slowdown
        from bond_drawer import draw_bond
        draw_bond( self, glpane, dispdef, col, level, highlighted, bool_fullBondLength)
        return

    def legal_for_atomtypes(self): #bruce 050716
        v6 = self.v6
        return self.atom1.atomtype.permits_v6(v6) and self.atom2.atomtype.permits_v6(v6)
    
    def permits_v6(self, v6): #bruce 050806 #e should merge this somehow with self.legal_for_atomtypes()
        return self.atom1.atomtype.permits_v6(v6) and self.atom2.atomtype.permits_v6(v6)

    def draw_in_abs_coords(self, glpane, color, bool_fullBondLength = False): #bruce 050609
        """Draw this bond in absolute (world) coordinates (even if it's an internal bond),
        using the specified color (ignoring the color it would naturally be drawn with).
           This is only called for special purposes related to mouseover-highlighting,
        and should be renamed to reflect that, since its behavior can and should be specialized
        for that use. (E.g. it doesn't happen inside display lists; and it need not use glName at all.)
        """
        #Note: bool_fullBondLength represent whether full bond length to be drawn
        #it is used only in select Chunks mode while highlighting the whole chunk and when
        #the atom display is Tubes display -- ninad 070214
        
        highlighted = True  # ninad 070214 - passing 'highlghted' to bond.draw instead of highlighted = bool
        
        if self.killed():
            #bruce 050702, part of fix 2 of 2 redundant fixes for bug 716 (both fixes are desirable)
            return
        mol = self.atom1.molecule
        mol2 = self.atom2.molecule
        if mol is mol2:
            # internal bond; geometric info is stored in chunk-relative coords; we need mol's help to use those
            mol.pushMatrix()
            self.draw(glpane, mol.get_dispdef(glpane), color, mol.assy.drawLevel, 
                      highlighted , bool_fullBondLength )
                # sorry for all the kluges (e.g. 2 of those args) that beg for refactoring! The info passing in draw methods
                # is not designed for drawing leaf nodes by themselves in a clean way! (#e should clean up somehow)
                #bruce 050702 using shorten_tubes [as of 050727, this is done via highlighted = True]
                # to help make room to mouseover-highlight the atoms,
                # when in tubes mode (thus fixing bug 715-1); a remaining bug was that it's sometimes hard to
                # highlight the tube bonds, apparently due to selatom seeming bigger even when not visible (not sure).
                # In another commit, same day, GLPane.py (sort selobj candidates) and this file (don't shorten_tubes
                # next to singlets [later moved to bond_drawer.py]), this has been fixed.
            mol.popMatrix()
        else:
            # external bond -- draw it at max dispdef of those from its mols
            disp = max( mol.get_dispdef(glpane), mol2.get_dispdef(glpane) )
            self.draw(glpane, disp, color, mol.assy.drawLevel)
        return

    def killed(self): #bruce 050702
        try:
            return self.atom1.killed() or self.atom2.killed()
                # This last condition doesn't yet work right, not sure why:
                ## ... or not self in atom1.bonds
                # Problem: without it, this might be wrong if the bond was "busted"
                # without either atom being killed. For now, just leave it out; fix this sometime. #####@@@@@
                # Warning: that last condition is slow, too.
        except:
            # (if this can happen, it's probably from one of the atoms being None,
            #  though self.bust() doesn't presently set them to None)
            return True
        pass
    
    def writepov(self, file, dispdef, col): #bruce 050727 moving implem to separate file; 050730 fixed bug in this method's name
        "Write this bond to a povray file (always using absolute coords, even for internal bonds)."
        from bond_drawer import writepov_bond
        writepov_bond(self, file, dispdef, col)
        return

    def __str__(self): #bruce 050705 revised this; note that it contains chars not compatible with HTML unless quoted
        ## return str(self.atom1) + " <--> " + str(self.atom2)
        # No quat is easily available here; better results if you call that subr directly and pass one;
        # the right one is (in current code, AFAIK, 070415) glpane.quat for the glpane that will display the bond
        # (whether or not it's an internal bond); let's try to guess that:
        quat = Q(1,0,0,0)
        try:
            glpane = self.atom1.molecule.assy.o
            quat = glpane.quat
        except:
            if env.debug():
                print_compact_traceback("bug: exception in self.atom1.molecule.assy.o.quat: ") # don't print self here!
            pass
        return bonded_atoms_summary(self, quat = quat) #bruce 070415 added quat arg and above code to guess it ###UNTESTED

    def __repr__(self):
        return str(self.atom1) + "::" + str(self.atom2)

    # ==

    def bond_menu_section(self, quat = Q(1,0,0,0)): #bruce 050705 (#e add options??)
        """Return a menu_spec subsection for displaying info about a highlighted bond,
        changing its bond_type, offering commands about it, etc.
        If given, use the quat describing the rotation used for displaying it
        to order the atoms in the bond left-to-right (e.g. in text strings).
        """
        if platform.atom_debug:
            import bond_utils
            reload(bond_utils) # at least during development
        from bond_utils import bond_menu_section
        return bond_menu_section(self, quat = quat)

    pass # end of class Bond

register_class_changedicts( Bond, _Bond_global_dicts )
    # error if one class has two same-named changedicts (so be careful re module reload)

# ==

# some more bond-related functions

def grow_bond_chain(bond, atom, next_bond_in_chain): #bruce 070415; generalized from grow_pi_sp_chain
    """Given a bond and one of its atoms, grow the bond chain containing bond
    (of the kind defined by next_bond_in_chain, called on a bond and one of its atoms)
    in the direction of atom,
    adding newly found bonds and atoms to respective lists (listb, lista) which we'll return,
    until the chain ends or comes back to bond and forms a ring
    (in which case return as much of the chain as possible, but not another ref to bond or atom).
       Return value is the tuple (ringQ, listb, lista) where ringQ says whether a ring was detected
    and len(listb) == len(lista) == number of new (bond, atom) pairs found.
       Note that each (bond, atom) pair found (at corresponding positions in the lists)
    has a direction (in bond, from atom to bond.other(atom)) which is backwards along the direction of chain growth.
       Note that listb never includes the original bond, so it is never a complete list of bonds in the chain.
    In general, to form a complete chain, a caller must piece together a starting bond and two bond lists
    grown in opposite directions, or one bond list if bond is part of a ring.
    (See also XXX [nim, to be modified from make_pi_bond_obj], which calls us twice and does this.)
       The function next_bond_in_chain(bond, atom) must return another bond containing atom
    in the same chain or ring, or None if the chain ends at bond (on the end of bond which is atom),
    and must be defined in such a way that its progress from bond to bond, through any atom, is consistent from
    either direction. (I.e., if given bond1 and atom1 it returns bond2 and atom2, then given bond2 and atom1 it
    must return bond1 and bond1.other(atom1).) However, we don't promise to do full checking on whether the function
    satisfies this requirement.
       That requirement means it's not possible to find a ring which comes back to bond
    but does not include bond (by coming back to atom before coming to bond's other atom),
    so if that happens, we raise an exception.
    """
    listb, lista = [], []
    origbond = bond # for detecting a ring
    origatom = atom # for error checking
    while 1:
        nextbond = next_bond_in_chain(bond, atom) # the function called here is the main difference from grow_pi_sp_chain
        if nextbond is None:
            return False, listb, lista
        if nextbond is origbond:
            assert atom is not origatom, "grow_bond_chain(%r, %r, %r): can't have 3 bonds in chain at atom %r; data: %r" % \
                   (origbond, origatom, next_bond_in_chain, atom, (nextbond, listb, lista)) #revised to fix bug 2328 [bruce 070424]
            assert nextbond.other(atom) is origatom
            return True, listb, lista
        nextatom = nextbond.other(atom)
        listb.append(nextbond)
        lista.append(nextatom)
        bond, atom = nextbond, nextatom
    pass

def grow_directional_bond_chain(bond, atom): #bruce 070415
    "Grow a chain of directional bonds. For details, see docstring of grow_bond_chain."
    return grow_bond_chain(bond, atom, next_directional_bond_in_chain)

def next_directional_bond_in_chain(bond, atom): #bruce 070415
    assert bond.is_directional()
    bonds = filter(lambda bond1: bond1 is not bond and bond1.is_directional(), atom.bonds)
    assert len(bonds) <= 1, "atom %r has more than two directional bonds: %r and %r" % (atom, bond, bonds)
    if len(bonds) == 1:
        return bonds[0]
    return None

# [bruce 050502 moved bond_at_singlets from chunk.py to here]

def bond_at_singlets(s1, s2, **opts):
    """[Public function; does all needed invalidations.]
    s1 and s2 are singlets; make a bond between their real atoms in
    their stead.
       If the real atoms are in different molecules, and if move = 1
    (the default), move s1's molecule to match the bond, and
    [bruce 041109 observes that this last part is not yet implemented]
    set its center to the bond point and its axis to the line of the bond.
       It's an error if s1 == s2, or if they're on the same atom. It's a
    warning (no error, but no bond made) if the real atoms of the singlets
    are already bonded, unless we're able to make the existing bond have
    higher valence, which we'll only attempt if increase_bond_order = True,
    and [bruce 050702] which is only possible if the bonded elements have suitable atomtypes.
    If the singlets are bonded to their base atoms with different valences,
    it's an error if we're unable to adjust those to match... #####@@@@@ #k.
    (We might add more error or warning conditions later.)
       The return value says whether there was an error, and what was done:
    we return (flag, status) where flag is 0 for ok (a bond was made or an
    existing bond was given a higher valence, and s1 and s2 were killed)
    or 1 or 2 for no bond made (1 = not an error, 2 = an error),
    and status is a string explaining what was done, or why nothing was
    done, suitable for displaying in a status bar.
       If no bond is made due to an error, and if print_error_details = 1
    (the default), then we also print a nasty warning with the details
    of the error, saying it's a bug. 
    """
    obj = bonder_at_singlets(s1, s2, **opts)
    return obj.retval

class bonder_at_singlets:
    "handles one call of bond_at_singlets"
    #bruce 041109 rewrote this, added move arg, renamed it from makeBonded
    #bruce 041119 added args and retvals to help fix bugs #203 and #121
    #bruce 050429 plans to permit increasing the valence of an existing bond, #####@@@@@doit
    # and also checking for matched valences of s1 and s2. #####@@@@@doit
    # also changed it from function to class
    def __init__(self, s1, s2, move = True, print_error_details = True, increase_bond_order = False):
        self.s1 = s1
        self.s2 = s2
        self.move = move
        self.print_error_details = print_error_details
        self.increase_bond_order = increase_bond_order
        self.retval = self.main()
        return
    def do_error(self, status, error_details):
        if self.print_error_details and error_details:
            print "BUG: bond_at_singlets:", error_details
            print "Doing nothing (but further bugs may be caused by this)."
            print_compact_stack()
        if error_details: # i.e. if it's an error
            flag = 2
        else:
            flag = 1
        status = status or "can't bond here"
        return (flag, status)
    def main(self):
        s1 = self.s1
        s2 = self.s2
        do_error = self.do_error
        if not s1.is_singlet():
            return do_error("not both singlets", "not a singlet: %r" % s1)
        if not s2.is_singlet():
            return do_error("not both singlets", "not a singlet: %r" % s2)
        a1 = self.a1 = chem.singlet_atom(s1)
        a2 = self.a2 = chem.singlet_atom(s2)
        if s1 is s2: #bruce 041119
            return do_error("can't bond a singlet to itself",
              "asked to bond atom %r to itself,\n"
              " from the same singlet %r (passed twice)" % (a1, s1)) # untested formatting
        if a1 is a2: #bruce 041119, part of fix for bug #203
            ###@@@ should we permit this as a way of changing the bonding pattern by summing the valences of these bonds? YES! [doit]
            # [later comment, 050702:] this is low-priority, since it's difficult to do for a free atom
            # (the atom tries to rotate to make it impossible) (tho I have to admit, for a bound C(sp3)
            #  with 2 open bonds left, it's not too hard, due to the arguable-bug in which only one of them moves)
            # and since the context menu lets you do it more directly. ... even so, let's try it:
            if self.increase_bond_order and a1.can_reduce_numbonds():
                return self.merge_open_bonds() #bruce 050702 new feature
            else:
                return do_error("can't bond an atom (%r) to itself" % a1,
                  "asked to bond atom %r to itself,\n"
                  " from different singlets, %r and %r." % (a1, s1, s2))
        if bonded(a1,a2):
            #bruce 041119, part of fix for bug #121
            # not an error (so arg2 is None)
            if self.increase_bond_order and a1.can_reduce_numbonds() and a2.can_reduce_numbonds():
                # we'll try that -- it might or might not work, but it has its own error messages if it fails
                #bruce 050702 added can_reduce_numbonds conditions, which check whether the atoms can change their atomtypes appropriately
                return self.upgrade_existing_bond()
            else:
                if a1.can_reduce_numbonds() and a2.can_reduce_numbonds():
                    why = "won't"
                else:
                    why = "can't"
                return do_error("%s increase bond order between already-bonded atoms %r and %r" % (why,a1,a2), None)
        #####@@@@@ worry about s1 and s2 valences being different
            # [much later, 050702: that might be obs, but worrying about their *permitted* valences might not be...]
            # (not sure exactly what we'll do then!
            #  do bonds want to keep track of a range of permissible valences??
            #  it's a real concept (I think) and it's probably expensive to recompute.
            #  BTW, if there is more than one way to resolve the error, they might want to
            #  permit the linkage but not pick the way to resolve it, but wait for you
            #  to drag the v-error indicator (or whatever).)
        #####@@@@@ worry about s1 and s2 valences being not V_SINGLE
        
        # ok, now we'll really do it.
        return self.bond_unbonded_atoms()
    def bond_unbonded_atoms(self):
        s1, a1 = self.s1, self.a1
        s2, a2 = self.s2, self.a2
        status = "bonded atoms %r and %r" % (a1, a2) #e maybe subr should make this?? #e subr might prefix it with bond-type made ###@@@
        # we only consider "move m1" in the case of no preexisting bond,
        # so we only need it in this submethod (in fact, if it was in
        # the other one, it would never run, due to the condition about
        # sep mols and no externs)
        m1 = a1.molecule
        m2 = a2.molecule
        if m1 is not m2 and self.move:
            # Comments by bruce 041123, related to fix for bug #150:
            #
            # Move m1 to an ideal position for bonding to m2, but [as bruce's fix
            # to comment #1 of bug 150, per Josh suggestion; note that this bug will
            # be split and what we're fixing might get a new bug number] only if it
            # has no external bonds except the one we're about to make. (Even a bond
            # to the other of m1 or m2 will disqualify it, since that bond might get
            # messed up by a motion. This might be a stricter limit than Josh meant
            # to suggest, but it seems right. If bonds back to the same mol should
            # not prevent the motion, we can use 'externs_except_to' instead.)
            #
            # I am not sure if moving m2 rather than m1, in case m1 is not qualified
            # to be moved, would be a good UI feature, nor whether it would be safe
            # for the calling code (a drag event processor in Build mode), so for now
            # I won't permit that, though it would be easy to do.
            #
            # Note that this motion feature will be much more useful once we fix
            # another bug about not often enough merging atoms into single larger
            # molecules, in Build mode. [end of bruce 041123 comments]
            def ok_to_move(mol1, mol2):
                "ok to move mol1 if we're about to bond it to mol2?"
                return mol1.externs == []
                #e you might prefer externs_except_to(mol1, [mol2]), but probably not
            if ok_to_move(m1,m2):
                status += ", and moved %r to match" % m1.name
                m1.rot(Q(a1.posn()-s1.posn(), s2.posn()-a2.posn()))
                m1.move(s2.posn()-s1.posn())
            else:
                status += " (but didn't move %r -- it already has a bond)" % m1.name
        self.status = status
        return self.actually_bond()
    def actually_bond(self):
        "#doc... (if it succeeds, uses self.status to report what it did)"
        #e [bruce 041109 asks: does it matter that the following code forgets which
        #   singlets were involved, before bonding?]
        #####@@@@@ this needs to worry about valence of s1 and s2 bonds, and thus of new bond
        s1, a1 = self.s1, self.a1
        s2, a2 = self.s2, self.a2
        try: # use old code until new code works and unless new code is needed; CHANGE THIS SOON #####@@@@@
            v1, v2 = s1.singlet_v6(), s2.singlet_v6() # new code available
            assert v1 != V_SINGLE or v2 != V_SINGLE # new code needed
        except:
            # old code can be used for now
            if platform.atom_debug and env.once_per_event("using OLD code for actually_bond"):
                print "atom_debug: fyi (once per event): using OLD code for actually_bond"
            s1.kill()
            s2.kill()
            bond_atoms(a1,a2)
            return (0, self.status) # effectively from bond_at_singlets
        # new code, handles any valences for s1, s2
        if platform.atom_debug:
            print "atom_debug: NEW code used for actually_bond" #####@@@@@
        vnew = min(v1,v2)
        bond = bond_atoms(a1,a2,vnew,s1,s2) # tell it the singlets to replace or reduce; let this do everything now, incl updates
        # can that fail? I don't think so; if it could, it'd need to have new API and return us an error message explaining why.
        vused = bond.v6 # this will be the created bond
        prefix = bond_type_names[vused] + '-'
        status = prefix + self.status # use prefix even for single bond, for now #k
        # add something to status message if not all valence from s1 or s2 was used
        # (can this happen for both singlets at once? maybe 'a' vs 'g' can do that -- not sure.)
        if v1 > vused or v2 > vused:
            status += "; some bond-valence unused on "
            if v1 > vused:
                status += "%r" % a1
            if v1 > vused and v2 > vused:
                status += " and " #e could rewrite this like this: " and ".join(atomreprs)
            if v2 > vused:
                status += "%r" % a2
        return (0, status)
    def upgrade_existing_bond(self):
        s1, a1 = self.s1, self.a1
        s2, a2 = self.s2, self.a2
        v1, v2 = s1.singlet_v6(), s2.singlet_v6()
        if len(a1.bonds) == 2: # (btw, this method is only called when a1 and a2 have at least 2 bonds)
            # Since a1 will have only one bond after this (if it's able to use up all of s1's valence),
            # we might as well try to add even more valence to the bond, to correct any deficient valence on a1.
            # But we'll never do this if there are uninvolved bonds to a1, since user might be planning
            # to manually increase their valence after doing this operation.
            # [bruce 051215 new feature, which ought to also fix bug 1221; other possible fixes seem too hard to do in isolation.
            #  In that bug, -N-N- temporarily became N=N and was then "corrected" to N-N rather than to N#N as would be better.]
            v1 += a1.deficient_v6() # usually adds 0
        if len(a2.bonds) == 2:
            v2 += a2.deficient_v6()
        vdelta = min(v1,v2) # but depending on the existing bond, we might use less than this, or none
        bond = find_bond(a1, a2)
##        old_bond_v6 = bond.v6 #bruce 051215 debug code
        vdelta_used = bond.increase_valence_noupdate(vdelta)
            # increases as much as possible up to vdelta, to some legal value
            # (ignores elements and other bond orders -- "legal" just means for any conceivable bond);
            # returns actual amount of increase (maybe 0)
##        new_bond_v6 = bond.v6 #bruce 051215 debug code
        ###@@@ why didn't we use vdelta_used in place of vdelta, below? (a likely bug, which would erroneously reduce valence;
        # but so far I can't find a way to make it happen -- except dNdNd where it fixes preexisting valence errors!
        # I will fix it anyway, since it obviously should have been written that way to start with. [bruce 051215])
##        if platform.atom_debug: #bruce 051215
##            print "atom_debug: bond_v6 changed from %r to %r; vdelta_used (difference) is %r; vdelta is %r" % (old_bond_v6, new_bond_v6, vdelta_used, vdelta)
        if not vdelta_used:
            return self.do_error("can't increase order of bond between atoms %r and %r" % (a1,a2), None) #e say existing order? say why not?
        vdelta = vdelta_used #bruce 051215 fix unreported hypothetical bug (see comment above)
        s1.singlet_reduce_valence_noupdate(vdelta)
            # this might or might not kill it;
            # it might even reduce valence to 0 but not kill it,
            # letting base atom worry about that
            # (and letting it take advantage of the singlet's position, when it updates things)
        s2.singlet_reduce_valence_noupdate(vdelta)
        a1.update_valence()
            # repositions/alters existing singlets, updates bonding pattern, valence errors, etc;
            # might reorder bonds, kill singlets; but doesn't move the atom and doesn't alter
            # existing real bonds or other atoms; it might let atom record how it wants to move,
            # when it has a chance and wants to clean up structure, if this can ever be ambiguous
            # later when the current state (including positions of old singlets) is gone.
        a2.update_valence()
        return (0, "increased bond order between atoms %r and %r" % (a1,a2)) #e say existing and new order?
            # Note, bruce 060629: the new bond order would be hard to say, since later code in bond_updater is likely
            # to decrease the value, but in a way it might be hard to predict at this point (it depends on what happens
            # to the atomtypes which that code will also fix, and that depends on the other bonds we modify here;
            # in theory we have enough info here, but the code is not well structured for this -- unless we save up this
            # message here and somehow emit it later after that stuff has been resolved). Not an ideal situation....
    def merge_open_bonds(self): #bruce 050702 new feature; implem is a guess and might be partly obs when written
        "Merge the bond-valence of s1 into that of s2"
        s1, a1 = self.s1, self.a1
        s2, a2 = self.s2, self.a2
        v1, v2 = s1.singlet_v6(), s2.singlet_v6()
        vdelta = v1
        bond1 = s1.bonds[0]
        bond2 = s2.bonds[0]
        #e should following permit illegal values? be a singlet method?
        vdelta_used = bond2.increase_valence_noupdate(vdelta) # increases to legal value, returns actual amount of increase (maybe 0)
        if not vdelta_used:
            return self.do_error("can't merge these two bondpoints on atom %r" % (a1,), None) #e say existing orders? say why not?
        s1.singlet_reduce_valence_noupdate(vdelta)
        a1.update_valence() # this can change the atomtype of a1 to match the fact that it deletes a singlet [bruce comment 050728]
        return (0, "merged two bondpoints on atom %r" % (a1,))
    pass # end of class bonder_at_singlets, the helper for function bond_at_singlets

# ===

# some unused old code that would be premature to completely remove [moved here by bruce 050502]

##def externs_except_to(mol, others): #bruce 041123; not yet used or tested
##    # [written to help bond_at_singlets fix bug 150, but not used for that]
##    """Say whether mol has external bonds (bonds to other mols)
##    except to the mols in 'others' (a list).
##    In fact, return the list of such bonds
##    (which happens to be true when nonempty, so we can be used
##    as a boolean function as well).
##    """
##    res = []
##    for bon in mol.externs:
##        mol2 = bon.othermol(mol)
##        assert mol2 != mol, "an internal bond %r was in self.externs of %r" % (bon, mol)
##        if mol not in others:
##            if mol not in res:
##                res.append(mol)
##    return res

# ==

##class bondtype:
##    """not implemented
##    """
##    pass
##    # int at1, at2;    /* types of the elements */
##    # num r0,ks;           /* bond length and stiffness */
##    # num ediss;           /* dissociation (breaking) energy */
##    # int order;            /* 1 single, 2 double, 3 triple */
##    # num length;          // bond length from nucleus to nucleus
##    # num angrad1, aks1;        // angular radius and stiffness for at1
##    # num angrad2, aks2;        // angular radius and stiffness for at2

# ==

# this code knows where to place missing bonds in carbon
# sure to be used later
# [code and comment by Josh, in chem.py, long before 050502]
# [bruce adds, 050510: probably this was superseded by his depositMode code;
#  as of today it would fail since Carbon.bonds[0][1] is now
#  Carbon.atomtypes[0].rcovalent * 100.0, I think]

##         # length of Carbon-Hydrogen bond
##         lCHb = (Carbon.bonds[0][1] + Hydrogen.bonds[0][1]) / 100.0
##         for a in self.atoms.values():
##             if a.element == Carbon:
##                 valence = len(a.bonds)
##                 # lone atom, pick 4 directions arbitrarily
##                 if valence == 0:
##                     b=atom("H", a.xyz+lCHb*norm(V(-1,-1,-1)), self)
##                     c=atom("H", a.xyz+lCHb*norm(V(1,-1,1)), self)
##                     d=atom("H", a.xyz+lCHb*norm(V(1,1,-1)), self)
##                     e=atom("H", a.xyz+lCHb*norm(V(-1,1,1)), self)
##                     self.bond(a,b)
##                     self.bond(a,c)
##                     self.bond(a,d)
##                     self.bond(a,e)

##                 # pick an arbitrary tripod, and rotate it to
##                 # center away from the one bond
##                 elif valence == 1:
##                     bpos = lCHb*norm(V(-1,-1,-1))
##                     cpos = lCHb*norm(V(1,-1,1))
##                     dpos = lCHb*norm(V(1,1,-1))
##                     epos = V(-1,1,1)
##                     q1 = Q(epos, a.bonds[0].other(a).xyz - a.xyz)
##                     b=atom("H", a.xyz+q1.rot(bpos), self)
##                     c=atom("H", a.xyz+q1.rot(cpos), self)
##                     d=atom("H", a.xyz+q1.rot(dpos), self)
##                     self.bond(a,b)
##                     self.bond(a,c)
##                     self.bond(a,d)

##                 # for two bonds, the new ones can be constructed
##                 # as linear combinations of their sum and cross product
##                 elif valence == 2:
##                     b=a.bonds[0].other(a).xyz - a.xyz
##                     c=a.bonds[1].other(a).xyz - a.xyz
##                     v1 = - norm(b+c)
##                     v2 = norm(cross(b,c))
##                     bpos = lCHb*(v1 + sqrt(2)*v2)/sqrt(3)
##                     cpos = lCHb*(v1 - sqrt(2)*v2)/sqrt(3)
##                     b=atom("H", a.xyz+bpos, self)
##                     c=atom("H", a.xyz+cpos, self)
##                     self.bond(a,b)
##                     self.bond(a,c)

##                 # given 3, the last one is opposite their average
##                 elif valence == 3:
##                     b=a.bonds[0].other(a).xyz - a.xyz
##                     c=a.bonds[1].other(a).xyz - a.xyz
##                     d=a.bonds[2].other(a).xyz - a.xyz
##                     v = - norm(b+c+d)
##                     b=atom("H", a.xyz+lCHb*v, self)
##                     self.bond(a,b)

# end of bonds.py
