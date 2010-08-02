# Vimm: Visual Interface to Materials Manipulation
#
# Copyright 2010 Caltech.  Copyright 2005 Sandia Corporation.  Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government
# retains certain rights in this sofware.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  
# USA


####################################################################
#
# class: TowheeInput
#
# Description: Contains the variables for reading a towhee_input
#   file.
#
# Notes:
#   None
#
####################################################################

class TowheeInput:
    def __init__(self):
        self.iformat = "Towhee"

        self.randomseed = 6282003
        self.nmolty = 1
        self.numboxes = 1 
        self.ensemble = "nvt"

        self.temperature = "300.0d0"
        self.pressure = "300.0d0"
        self.nmolectyp = []
        self.chempot = []
        self.stepstyle = "cycles"
        self.nstep = 10
        self.optstyle = 0
        self.mintol = ""
        self.printfreq = 1000
        self.blocksize = 1000
        self.moviefreq = 1000
        self.backupfreq = 1000
        self.runoutput = "full"
        self.pdb_output_freq = 0
        self.loutdft = True
        self.loutlammps = True
        self.louthist = True
        self.histcalcfreq = 0
        self.histdumpfreq = 0
        self.pressurefreq = 10000
        self.trmaxdispfreq = 10
        self.volmaxdispfreq = 10
        self.chempotperstep = []
        
        self.potentialstyle = "classical"
        self.isolvtype = 0
        self.ffnumber = 1
        self.ff_filename = []
        self.classical_potential = "Lennard-Jones"
        self.classical_mixrule = "Lorentz-Berthelot"
        self.lshift = True
        self.ltailc = True
        self.rmin = "0.5"
        self.rcut = "1.0"
        self.rcutin = "10"
        self.interpolatestyle = "linear"
        self.radial_pressure_delta = "0.0d0"
        self.cmix_rescaling_style = "none"
        self.cmix_lambda = "0.0d0"
        self.cmix_npair = 0
        self.cmix_pair_list = []
        self.coulombstyle = "none"
        self.kalp = "5.6"
        self.kmax = 5
        self.ewald_prec = "1.0d-4"
        self.rcelect = "1.0"
        self.dielect = "1.0"
        self.functional = ""
        self.quantum_code = "Seqquest"
        self.atom_types = 1
        self.atom_filenames = []
        self.grid_multiplier = ""
        self.kgrid_product = ""
        
        self.nfield = 0
        self.externalfields = []

        self.linit = True
        self.initstyle = []
        self.initlattice = []
        self.helix = []
        self.initboxtype = "dimensions"
        self.hmatrix = []
        self.box_number_density = []
        self.initmol = []
        self.inix = []
        self.iniy = []
        self.iniz = []
        self.inimix = []

        self.ivm = IsotropicVolumeMove()
        self.avm = AnisotropicVolumeMove()
        self.rb2bmtm = RotationalBias2BoxMoleculeTransferMove()
        self.cb2bmtm = ConfigurationalBias2BoxMoleculeTransferMove()
        self.cbgcidm = ConfigurationalBiasGrandCanonicalInsertionDeletionMove()
        self.cbsbmrm = ConfigurationalBiasSingleBoxMoleculeReinsertionMove()
        self.avbmt1 = AggregationVolumeBiasMoveType1()
        self.avbmt2 = AggregationVolumeBiasMoveType2()
        self.avbmt3 = AggregationVolumeBiasMoveType3()
        self.cbpmr = ConfigurationalBiasPartialMoleculeRegrowth()
        self.cbpbr = ConfigurationalBiasProteinBackboneRegrowth()
        self.tpm = TorsionalPivotMove()
        self.crnmoanpb = ConcertedRotationMoveOnANonPeptideBackbone()
        self.crnmoa3pbs = ConcertedRotationMoveOverA3PeptidesBackboneSequence()
        self.psm = PlaneShiftMove()
        self.rsm = RowShiftMove()
        self.isatm = IntramolecularSingleAtomTranslationMove()
        self.cofmmtm = CenterOfMassMoleculeTranslationMove()
        self.ratcomm = RotationAboutTheCenterOfMassMove()

        self.tor_cbstyle = 0
        self.bend_cbstyle = 0
        self.vib_cbstyle = 0
        self.sdevtor = "20.0"
        self.sdevbena = "10.0"
        self.sdevbenb = "20.0"
        self.sdevvib = "0.1"
        self.vibrang = ("0.85","1.15")
        self.cdform = 0
        self.nch_nb_one = []
        self.nch_nb = []
        self.nch_tor_out = []
        self.nch_tor_in = [] 
        self.nch_tor_in_con = []
        self.nch_bend_a = []
        self.nch_bend_b = []
        self.nch_vib = []

        self.inputs = []
        return

    def get_iformat(self):
        return self.iformat

    def get_randomseed(self):
        return self.randomseed

    def set_randomseed(self, seed):
        self.randomseed = seed
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.nmolectyp[nmolty:]
            del self.chempot[nmolty:]
            del self.chempotperstep[nmolty:]
            for initmol in self.initmol:
                del initmol[nmolty:]
            for initstyle in self.initstyle:
                del initstyle[nmolty:]
            del self.nch_nb_one[nmolty:]
            del self.nch_nb[nmolty:]
            del self.nch_tor_out[nmolty:]
            del self.nch_tor_in[nmolty:] 
            del self.nch_tor_in_con[nmolty:]
            del self.nch_bend_a[nmolty:]
            del self.nch_bend_b[nmolty:]
            del self.nch_vib[nmolty:]
            del self.inputs[nmolty:]

        self.rb2bmtm.set_nmolty(nmolty)
        self.cb2bmtm.set_nmolty(nmolty)
        self.cbgcidm.set_nmolty(nmolty)
        self.cbsbmrm.set_nmolty(nmolty)
        self.avbmt1.set_nmolty(nmolty)
        self.avbmt2.set_nmolty(nmolty)
        self.avbmt3.set_nmolty(nmolty)
        self.cbpmr.set_nmolty(nmolty)
        self.cbpbr.set_nmolty(nmolty)
        self.tpm.set_nmolty(nmolty)
        self.crnmoanpb.set_nmolty(nmolty)
        self.crnmoa3pbs.set_nmolty(nmolty)
        self.isatm.set_nmolty(nmolty)
        self.cofmmtm.set_nmolty(nmolty)
        self.ratcomm.set_nmolty(nmolty)
        self.nmolty = nmolty
        return

    def get_numboxes(self):
        return self.numboxes

    def set_numboxes(self, numboxes):
        if numboxes < self.numboxes:
            del self.initmol[numboxes:]
            del self.initstyle[numboxes:]
            del self.hmatrix[numboxes:]
            del self.box_number_density[numboxes:]
            del self.inix[numboxes:]
            del self.iniy[numboxes:]
            del self.iniz[numboxes:]
            del self.inimix[numboxes:]

        self.ivm.set_numboxes(numboxes)
        self.avm.set_numboxes(numboxes)
        self.rb2bmtm.set_numboxes(numboxes)
        self.cb2bmtm.set_numboxes(numboxes)
        self.psm.set_numboxes(numboxes)
        self.rsm.set_numboxes(numboxes)
        self.numboxes = numboxes
        return

    def get_ensemble(self):
        return self.ensemble

    def set_ensemble(self, ensemble):
        self.ivm.set_ensemble(ensemble)
        self.avm.set_ensemble(ensemble)
        self.ensemble = ensemble
        return

    def get_temperature(self):
        return self.temperature

    def set_temperature(self, temperature):
        self.temperature = temperature
        return

    def get_pressure(self):
        return self.pressure

    def set_pressure(self, pressure):
        self.pressure = pressure
        return

    def get_nmolectyp(self):
        return self.nmolectyp

    def set_nmolectyp(self, nmolectyp):
        self.nmolectyp = nmolectyp
        return

    def append_nmolectyp(self, nmolectyp):
        self.nmolectyp.append(nmolectyp)
        return

    def get_single_nmolectyp(self, index):
        return self.nmolectyp[index]

    def clear_nmolectyp(self):
        self.nmolectyp = []
        return

    def get_chempot(self):
        return self.chempot

    def set_chempot(self, chempot):
        self.chempot = chempot
        return

    def append_chempot(self, chempot):
        self.chempot.append(chempot)
        return

    def clear_chempot(self):
        self.chempot = []
        return

    def get_stepstyle(self):
        return self.stepstyle

    def set_stepstyle(self, stepstyle):
        self.stepstyle = stepstyle
        return

    def get_nstep(self):
        return self.nstep

    def set_nstep(self, nstep):
        self.nstep = nstep
        return

    def get_optstyle(self):
        return self.optstyle

    def set_optstyle(self, optstyle):
        self.optstyle = optstyle
        return

    def get_mintol(self):
        return self.mintol

    def set_mintol(self, mintol):
        self.mintol = mintol
        return

    def get_printfreq(self):
        return self.printfreq

    def set_printfreq(self, printfreq):
        self.printfreq = printfreq
        return

    def get_blocksize(self):
        return self.blocksize

    def set_blocksize(self, blocksize):
        self.blocksize = blocksize
        return

    def get_moviefreq(self):
        return self.moviefreq

    def set_moviefreq(self, moviefreq):
        self.moviefreq = moviefreq
        return

    def get_backupfreq(self):
        return self.backupfreq

    def set_backupfreq(self, backupfreq):
        self.backupfreq = backupfreq
        return

    def get_runoutput(self):
        return self.runoutput

    def set_runoutput(self, runoutput):
        self.runoutput = runoutput
        return

    def get_pdb_output_freq(self):
        return self.pdb_output_freq

    def set_pdb_output_freq(self, pdb_output_freq):
        self.pdb_output_freq = pdb_output_freq
        return

    def get_loutdft(self):
        return self.loutdft

    def set_loutdft_true(self):
        self.loutdft = True
        return

    def set_loutdft_false(self):
        self.loutdft = False
        return

    def get_loutlammps(self):
        return self.loutlammps

    def set_loutlammps_true(self):
        self.loutlammps = True
        return

    def set_loutlammps_false(self):
        self.loutlammps = False
        return

    def get_louthist(self):
        return self.louthist

    def set_louthist_true(self):
        self.louthist = True
        return

    def set_louthist_false(self):
        self.louthist = False
        return

    def get_histcalcfreq(self):
        return self.histcalcfreq

    def set_histcalcfreq(self, histcalcfreq):
        self.histcalcfreq = histcalcfreq
        return

    def get_histdumpfreq(self):
        return self.histdumpfreq

    def set_histdumpfreq(self, histdumpfreq):
        self.histdumpfreq = histdumpfreq
        return

    def get_pressurefreq(self):
        return self.pressurefreq

    def set_pressurefreq(self, pressurefreq):
        self.pressurefreq = pressurefreq
        return

    def get_trmaxdispfreq(self):
        return self.trmaxdispfreq

    def set_trmaxdispfreq(self, trmaxdispfreq):
        self.trmaxdispfreq = trmaxdispfreq
        return

    def get_volmaxdispfreq(self):
        return self.volmaxdispfreq

    def set_volmaxdispfreq(self, volmaxdispfreq):
        self.volmaxdispfreq = volmaxdispfreq
        return

    def get_chempotperstep(self):
        return self.chempotperstep

    def set_chempotperstep(self, chempotperstep):
        self.chempotperstep = chempotperstep
        return

    def append_chempotperstep(self, chempotperstep):
        self.chempotperstep.append(chempotperstep)
        return

    def get_single_chempotperstep(self, index):
        return self.chempotperstep[index]

    def clear_chempotperstep(self):
        self.chempotperstep = []
        return

    def get_potentialstyle(self):
        return self.potentialstyle

    def set_potentialstyle(self, potentialstyle):
        self.potentialstyle = potentialstyle
        return

    def get_ffnumber(self):
        return self.ffnumber

    def set_ffnumber(self, ffnumber):
        if(self.ffnumber > ffnumber):
            del self.ff_filename[ffnumber:]
        self.ffnumber = ffnumber
        return

    def get_ff_filename(self):
        return self.ff_filename

    def set_ff_filename(self, ff_filename):
        self.ff_filename = ff_filename
        return

    def append_ff_filename(self, ff_filename):
        if len(self.ff_filename) == self.ffnumber:
            raise "ff_filename array is full"

        self.ff_filename.append(ff_filename)
        return

    def get_single_ff_filename(self, index):
        return self.ff_filename[index]

    def clear_ff_filename(self):
        self.ff_filename = []
        return

    def get_classical_potential(self):
        return self.classical_potential

    def set_classical_potential(self, classical_potential):
        self.classical_potential = classical_potential
        return

    def get_classical_mixrule(self):
        return self.classical_mixrule

    def set_classical_mixrule(self, classical_mixrule):
        self.classical_mixrule = classical_mixrule
        return

    def get_lshift(self):
        return self.lshift

    def set_lshift_true(self):
        self.lshift = True
        return

    def set_lshift_false(self):
        self.lshift = False
        return

    def get_ltailc(self):
        return self.ltailc

    def set_ltailc_true(self):
        self.ltailc = True
        return

    def set_ltailc_false(self):
        self.ltailc = False
        return

    def get_rmin(self):
        return self.rmin

    def set_rmin(self, rmin):
        self.rmin = rmin
        return

    def get_rcut(self):
        return self.rcut

    def set_rcut(self, rcut):
        self.rcut = rcut
        return

    def get_rcutin(self):
        return self.rcutin

    def set_rcutin(self, rcutin):
        self.rcutin = rcutin
        return

    def get_interpolatestyle(self):
        return self.interpolatestyle

    def set_interpolatestyle(self, interpolatestyle):
        self.interpolatestyle = interpolatestyle
        return

    def get_radial_pressure_delta(self):
        return self.radial_pressure_delta

    def set_radial_pressure_delta(self, radial_pressure_delta):
        self.radial_pressure_delta = radial_pressure_delta
        return

    def get_cmix_rescaling_style(self):
        return self.cmix_rescaling_style

    def set_cmix_rescaling_style(self, cmix_rescaling_style):
        self.cmix_rescaling_style = cmix_rescaling_style
        return

    def get_cmix_lambda(self):
        return self.cmix_lambda

    def set_cmix_lambda(self, cmix_lambda):
        self.cmix_lambda = cmix_lambda
        return

    def get_cmix_npair(self):
        return self.cmix_npair

    def set_cmix_npair(self, cmix_npair):
        self.cmix_npair = cmix_npair
        return

    def get_cmix_pair_list(self):
        return self.cmix_pair_list

    def set_cmix_pair_list(self, cmix_pair_list):
        self.cmix_pair_list = cmix_pair_list
        return

    def append_cmix_pair_list(self, cmix_pair_list):
        if len(self.cmix_pair_list) == self.cmix_npair:
            raise "cmix_pair_list array is full"

        self.cmix_pair_list.append(cmix_pair_list)
        return

    def get_single_cmix_pair_list(self, index):
        return self.cmix_pair_list[index]

    def set_single_cmix_pair_list(self, cmix_pair_list, index):
        self.cmix_pair_list[index] = cmix_pair_list
        return

    def clear_cmix_pair_list(self):
        self.cmix_pair_list = []
        return

    def get_coulombstyle(self):
        return self.coulombstyle

    def set_coulombstyle(self, coulombstyle):
        self.coulombstyle = coulombstyle
        return

    def get_kalp(self):
        return self.kalp

    def set_kalp(self, kalp):
        self.kalp = kalp
        return

    def get_kmax(self):
        return self.kmax

    def set_kmax(self, kmax):
        self.kmax = kmax
        return

    def get_ewald_prec(self):
        return self.ewald_prec

    def set_ewald_prec(self, ewald_prec):
        self.ewald_prec = ewald_prec
        return

    def get_rcelect(self):
        return self.rcelect

    def set_rcelect(self, rcelect):
        self.rcelect = rcelect
        return

    def get_dielect(self):
        return self.dielect

    def set_dielect(self, dielect):
        self.dielect = dielect
        return

    def get_quantum_code(self):
        return self.quantum_code

    def set_quantum_code(self, quantum_code):
        self.quantum_code = quantum_code
        return

    def get_functional(self):
        return self.functional

    def set_functional(self, functional):
        self.functional = functional
        return

    def get_atom_types(self):
        return self.atom_types

    def set_atom_types(self, atom_types):
        self.atom_types = atom_types
        return

    def get_atom_filenames(self):
        return self.atom_filenames

    def set_atom_filenames(self, atom_filenames):
        self.atom_filenames = atom_filenames
        return

    def append_atom_filenames(self, atom_filenames):
        if len(self.atom_filenames) == self.atom_types:
            raise "atom_types array is full"

        self.atom_filenames.append(atom_filenames)
        return

    def get_grid_multiplier(self):
        return self.grid_multiplier

    def set_grid_multiplier(self, grid_multiplier):
        self.grid_multiplier = grid_multiplier
        return

    def get_kgrid_product(self):
        return self.kgrid_product

    def set_kgrid_product(self, kgrid_product):
        self.kgrid_product = kgrid_product
        return

    def get_nfield(self):
        return self.nfield

    def set_nfield(self, nfield):
        if nfield < self.nfield:
            del self.externalfields[nfield:]
        self.nfield = nfield
        return

    def get_externalfields(self):
        return self.externalfields

    def set_externalfields(self, externalfields):
        self.externalfields = externalfields
        return

    def append_externalfields(self, externalfields):
        self.externalfields.append(externalfields)
        return

    def get_single_externalfield(self, index):
        return self.externalfields[index]

    def set_single_externalfield(self, index, externalfield):
        self.externalfields[index] = externalfield
        return

    def create_externalfield(self, type):
        if type == "Hard Wall":
            return HardWall()
        elif type == "Harmonic Attractor":
            return HarmonicAttractor()
        elif type == "Hooper Umbrella":
            return HooperUmbrella()
        elif type == "LJ 9-3 Wall":
            return LJWall()
        elif type == "Steele Wall":
            return SteeleWall()
        else:
            return None

    def get_single_type_externalfield(self, type, index):
        # returns the index'th externalfield of type type
        i = 0
        for ef in self.externalfields:
            if ef.get_fieldtype() == type:
                i+=1
            if i == index:
                return ef
        return None

    def set_single_type_externalfield(self, type, index, efield):
        # returns the index'th externalfield of type type
        i = 0
        for j in range(len(self.externalfields)):
            if self.externalfields[j].get_fieldtype() == type:
                i+=1
            if i == index:
                self.externalfields[j] = efield
                return
        return

    def clear_externalfields(self):
        self.externalfields = [] 

    def get_isolvtype(self):
        return self.isolvtype

    def set_isolvtype(self, isolvtype):
        self.isolvtype = isolvtype
        return

    def get_linit(self):
        return self.linit

    def set_linit_true(self):
        self.linit = True
        return

    def set_linit_false(self):
        self.linit = False
        return

    def get_initstyle(self):
        return self.initstyle

    def set_initstyle(self, initstyle):
        self.initstyle = initstyle
        return

    def append_initstyle(self, initstyle):
        self.initstyle.append(initstyle)
        return

    def set_single_initstyle(self, box, nmolty, initstyle):
        self.initstyle[box][nmolty] = initstyle
        return

    def get_single_initstyle(self, box, nmolty):
        return self.initstyle[box][nmolty]

    def clear_initstyle(self):
        self.initstyle = []
        return

    def get_initlattice(self):
        return self.initlattice

    def set_initlattice(self, initlattice):
        self.initlattice = initlattice
        return

    def append_initlattice(self, initlattice):
        self.initlattice.append(initlattice)
        return

    def set_single_initlattice(self, box, nmolty, initlattice):
        self.initlattice[box][nmolty] = initlattice
        return

    def get_single_initlattice(self, box, nmolty):
        return self.initlattice[box][nmolty]

    def clear_initlattice(self):
        self.initlattice = []
        return

    def get_helix(self):
        return self.helix

    def set_helix(self, helix):
        self.helix = helix
        return

    def append_helix(self, helix):
        nmolty = helix.get_nmolty()
        for helixes in self.helix:
            if helix.get_nmolty() < helixes.get_nmolty():
                index = self.helix.index(helixes)
                self.helix.insert(index, helix)
                return
        self.helix.append(helix)
        return

    def create_helix(self):
        helix = Helix()
        return helix

    def clear_helix(self):
        self.helix = []
        return

    def get_initboxtype(self):
        return self.initboxtype

    def set_initboxtype(self, initboxtype):
        self.initboxtype = initboxtype
        return

    def get_hmatrix(self):
        return self.hmatrix

    def set_hmatrix(self, hmatrix):
        self.hmatrix = hmatrix
        return

    def append_hmatrix(self, hmatrix):
        self.hmatrix.append(hmatrix)
        return

    def get_single_hmatrix(self, index):
        return self.hmatrix[index]

    def create_hmatrix(self):
        hmatrix = Hmatrix()
        return hmatrix

    def clear_hmatrix(self):
        self.hmatrix = []
        return

    def get_box_number_density(self):
        return self.box_number_density

    def set_box_number_density(self, box_number_density):
        self.box_number_density = box_number_density
        return

    def append_box_number_density(self, box_number_density):
        self.box_number_density.append(box_number_density)
        return

    def get_single_box_number_density(self, index):
        return self.box_number_density[index]

    def clear_box_number_density(self):
        self.box_number_density = []
        return

    def get_initmol(self):
        return self.initmol

    def set_initmol(self, initmol):
        self.initmol = initmol
        return

    def append_initmol(self, initmol):
        self.initmol.append(initmol)
        return

    def set_single_initmol(self, box, nmolty, initmol):
        self.initmol[box][nmolty] = initmol
        return

    def get_single_initmol(self, box, nmolty):
        return self.initmol[box][nmolty]

    def clear_initmol(self):
        self.initmol = []
        return

    def get_inix(self):
        return self.inix

    def set_inix(self, inix):
        self.inix = inix
        return

    def append_inix(self, inix):
        self.inix.append(inix)
        return

    def get_single_inix(self, index):
        return self.inix[index]

    def clear_inix(self):
        self.inix = []
        return

    def get_iniy(self):
        return self.iniy

    def set_iniy(self, iniy):
        self.iniy = iniy
        return

    def append_iniy(self, iniy):
        self.iniy.append(iniy)
        return

    def get_single_iniy(self, index):
        return self.iniy[index]

    def clear_iniy(self):
        self.iniy = []
        return

    def get_iniz(self):
        return self.iniz

    def set_iniz(self, iniz):
        self.iniz = iniz
        return

    def append_iniz(self, iniz):
        self.iniz.append(iniz)
        return

    def get_single_iniz(self, index):
        return self.iniz[index]

    def clear_iniz(self):
        self.iniz = []
        return

    def get_inimix(self):
        return self.inimix

    def set_inimix(self, inimix):
        self.inimix = inimix
        return

    def append_inimix(self, inimix):
        self.inimix.append(inimix)
        return

    def get_single_inimix(self, index):
        return self.inimix[index]

    def clear_inimix(self):
        self.inimix = []
        return

    def get_ivm(self):
        return self.ivm

    def set_ivm(self, ivm):
        self.ivm = ivm
        return

    def get_avm(self):
        return self.avm

    def set_avm(self, avm):
        self.avm = avm
        return

    def get_rb2bmtm(self):
        return self.rb2bmtm

    def set_rb2bmtm(self, rb2bmtm):
        self.rb2bmtm = rb2bmtm
        return

    def get_cb2bmtm(self):
        return self.cb2bmtm

    def set_cb2bmtm(self, cb2bmtm):
        self.cb2bmtm = cb2bmtm
        return
        
    def get_cbgcidm(self):
        return self.cbgcidm

    def set_cbgcidm(self, cbgcidm):
        self.cbgcidm = cbgcidm
        return

    def get_cbsbmrm(self):
        return self.cbsbmrm

    def set_cbsbmrm(self, cbsbmrm):
        self.cbsbmrm = cbsbmrm
        return

    def get_avbmt1(self):
        return self.avbmt1

    def set_avbmt1(self, avbmt1):
        self.avbmt1 = avbmt1
        return

    def get_avbmt2(self):
        return self.avbmt2

    def set_avbmt2(self, avbmt2):
        self.avbmt2 = avbmt2
        return

    def get_avbmt3(self):
        return self.avbmt3

    def set_avbmt3(self, avbmt3):
        self.avbmt3 = avbmt3
        return

    def get_cbpmr(self):
        return self.cbpmr

    def set_cbpmr(self, cbpmr):
        self.cbpmr = cbpmr
        return

    def get_cbpbr(self):
        return self.cbpbr

    def set_cbpbr(self, cbpbr):
        self.cbpbr = cbpbr
        return

    def get_tpm(self):
        return self.tpm

    def set_tpm(self, tpm):
        self.tpm = tpm
        return

    def get_crnmoanpb(self):
        return self.crnmoanpb

    def set_crnmoanpb(self, crnmoanpb):
        self.crnmoanpb = crnmoanpb
        return

    def get_crnmoa3pbs(self):
        return self.crnmoa3pbs

    def set_crnmoa3pbs(self, crnmoa3pbs):
        self.crnmoa3pbs = crnmoa3pbs
        return

    def get_psm(self):
        return self.psm

    def set_psm(self, psm):
        self.psm = psm
        return

    def get_rsm(self):
        return self.rsm

    def set_rsm(self, rsm):
        self.rsm = rsm
        return

    def get_isatm(self):
        return self.isatm

    def set_isatm(self, isatm):
        self.isatm = isatm
        return

    def get_cofmmtm(self):
        return self.cofmmtm

    def set_cofmmtm(self, cofmmtm):
        self.cofmmtm = cofmmtm
        return

    def get_ratcomm(self):
        return self.ratcomm

    def set_ratcomm(self, ratcomm):
        self.ratcomm = ratcomm
        return

    def get_tor_cbstyle(self):
        return self.tor_cbstyle

    def set_tor_cbstyle(self, tor_cbstyle):
        self.tor_cbstyle = tor_cbstyle
        return

    def get_sdevtor(self):
        return self.sdevtor

    def set_sdevtor(self, sdevtor):
        self.sdevtor = sdevtor
        return

    def get_bend_cbstyle(self):
        return self.bend_cbstyle

    def set_bend_cbstyle(self, bend_cbstyle):
        self.bend_cbstyle = bend_cbstyle
        return

    def get_sdevbena(self):
        return self.sdevbena

    def set_sdevbena(self, sdevbena):
        self.sdevbena = sdevbena
        return

    def get_sdevbenb(self):
        return self.sdevbenb

    def set_sdevbenb(self, sdevbenb):
        self.sdevbenb = sdevbenb
        return

    def get_vib_cbstyle(self):
        return self.vib_cbstyle

    def set_vib_cbstyle(self, vib_cbstyle):
        self.vib_cbstyle = vib_cbstyle
        return

    def get_vibrang(self):
        return self.vibrang

    def set_vibrang(self, vibrang):
        self.vibrang = vibrang
        return

    def get_sdevvib(self):
        return self.sdevvib

    def set_sdevvib(self, sdevvib):
        self.sdevvib = sdevvib
        return

    def get_cdform(self):
        return self.cdform

    def set_cdform(self, cdform):
        self.cdform = cdform
        return

    def get_nch_nb_one(self):
        return self.nch_nb_one

    def set_nch_nb_one(self, nch_nb_one):
        self.nch_nb_one = nch_nb_one
        return

    def append_nch_nb_one(self, nch_nb_one):
        self.nch_nb_one.append(nch_nb_one)
        return

    def get_single_nch_nb_one(self, index):
        return self.nch_nb_one[index]

    def clear_nch_nb_one(self):
        self.nch_nb_one = []
        return

    def get_nch_nb(self):
        return self.nch_nb

    def set_nch_nb(self, nch_nb):
        self.nch_nb = nch_nb
        return

    def append_nch_nb(self, nch_nb):
        self.nch_nb.append(nch_nb)
        return

    def get_single_nch_nb(self, index):
        return self.nch_nb[index]

    def clear_nch_nb(self):
        self.nch_nb = []
        return

    def get_nch_tor_out(self):
        return self.nch_tor_out

    def set_nch_tor_out(self, nch_tor_out):
        self.nch_tor_out = nch_tor_out
        return

    def append_nch_tor_out(self, nch_tor_out):
        self.nch_tor_out.append(nch_tor_out)
        return

    def get_single_nch_tor_out(self, index):
        return self.nch_tor_out[index]

    def clear_nch_tor_out(self):
        self.nch_tor_out = []
        return

    def get_nch_tor_in(self):
        return self.nch_tor_in

    def set_nch_tor_in(self, nch_tor_in):
        self.nch_tor_in = nch_tor_in
        return

    def append_nch_tor_in(self, nch_tor_in):
        self.nch_tor_in.append(nch_tor_in)
        return

    def get_single_nch_tor_in(self, index):
        return self.nch_tor_in[index]

    def clear_nch_tor_in(self):
        self.nch_tor_in = []
        return

    def get_nch_tor_in_con(self):
        return self.nch_tor_in_con

    def set_nch_tor_in_con(self, nch_tor_in_con):
        self.nch_tor_in_con = nch_tor_in_con
        return

    def append_nch_tor_in_con(self, nch_tor_in_con):
        self.nch_tor_in_con.append(nch_tor_in_con)
        return

    def get_single_nch_tor_in_con(self, index):
        return self.nch_tor_in_con[index]

    def clear_nch_tor_in_con(self):
        self.nch_tor_in_con = []
        return

    def get_nch_bend_a(self):
        return self.nch_bend_a

    def set_nch_bend_a(self, nch_bend_a):
        self.nch_bend_a = nch_bend_a
        return

    def append_nch_bend_a(self, nch_bend_a):
        self.nch_bend_a.append(nch_bend_a)
        return

    def get_single_nch_bend_a(self, index):
        return self.nch_bend_a[index]

    def clear_nch_bend_a(self):
        self.nch_bend_a = []
        return

    def get_nch_bend_b(self):
        return self.nch_bend_b

    def set_nch_bend_b(self, nch_bend_b):
        self.nch_bend_b = nch_bend_b
        return

    def append_nch_bend_b(self, nch_bend_b):
        self.nch_bend_b.append(nch_bend_b)
        return

    def get_single_nch_bend_b(self, index):
        return self.nch_bend_b[index]

    def clear_nch_bend_b(self):
        self.nch_bend_b = []
        return

    def get_nch_vib(self):
        return self.nch_vib

    def set_nch_vib(self, nch_vib):
        self.nch_vib = nch_vib
        return

    def append_nch_vib(self, nch_vib):
        self.nch_vib.append(nch_vib)
        return

    def get_single_nch_vib(self, index):
        return self.nch_vib[index]

    def clear_nch_vib(self):
        self.nch_vib = []
        return

    def get_inputs(self):
        return self.inputs

    def set_inputs(self, inputs):
        self.inputs = inputs
        return

    def append_input(self, input):
        self.inputs.append(input)
        return

    def get_single_input(self, index):
        return self.inputs[index]

    def set_single_input(self, index, input):
        self.inputs[index] = input
        return

    def create_input(self, inpstyle):
        if inpstyle == 0:
            return ExplicitDeclaration()
        elif inpstyle == 1:
            return PolypeptideBuilder()
        elif inpstyle == 2:
            return AtomBasedConnectivityMap()
        elif inpstyle == 3:
            return NucleicAcidBuilder()
        elif inpstyle == 4:
            return NanotubeBuilder()
        else:
            return None
# End of class TowheeInput


####################################################################
#
# class: Helix
#
# Description: Contains the variables for one Helix
#
# Notes:
#   None
#
####################################################################
class Helix:
    def __init__(self):
        self.nmolty = 1
        self.moltyp = 1
        self.radius = "0.0d0"
        self.angle = "0.0d0"
        self.keytype = "element"
        self.keyname = ""
        self.conlen = "0.0d0"
        self.phase = "0.0d0"
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        self.nmolty = nmolty
        return

    def get_moltyp(self):
        return self.moltyp

    def set_moltyp(self, moltyp):
        self.moltyp = moltyp
        return

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius
        return

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle
        return

    def get_keytype(self):
        return self.keytype

    def set_keytype(self, keytype):
        self.keytype = keytype
        return

    def get_keyname(self):
        return self.keyname

    def set_keyname(self, keyname):
        self.keyname = keyname
        return

    def get_conlen(self):
        return self.conlen

    def set_conlen(self, conlen):
        self.conlen = conlen
        return

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        return
# End of class Helix


####################################################################
#
# class: Hmatrix
#
# Description: Contains the variables for one Hmatrix
#
# Notes:
#   None
#
####################################################################
class Hmatrix:
    def __init__(self):
        self.row1 = ["100.0d0", "0.0d0",   "0.0d0"]
        self.row2 = ["0.0d0",   "100.0d0", "0.0d0"]
        self.row3 = ["0.0d0",   "0.0d0",   "100.0d0"]
        return

    def get_row1(self):
        return self.row1

    def set_row1(self, row1):
        self.row1 = row1
        return

    def set_row1_xyz(self, index, value):
        self.row1[index] = value
        return

    def get_row2(self):
        return self.row2

    def set_row2(self, row2):
        self.row2 = row2
        return

    def set_row2_xyz(self, index, value):
        self.row2[index] = value
        return

    def get_row3(self):
        return self.row3

    def set_row3(self, row3):
        self.row3 = row3
        return

    def set_row3_xyz(self, index, value):
        self.row3[index] = value
        return
# End of class Hmatrix


####################################################################
#
# class: HardWall
#
# Description: Contains the variables for one Hard Wall
#
# Notes:
#   None
#
####################################################################
class HardWall:
    def __init__(self):
        self.box = 1
        self.xyz = "x"
        self.cen = "0.0d0"
        self.rad = "0.0d0"
        self.energy_type = "infinite"
        self.wall_energy = ""
        self.fieldtype = "Hard Wall"
        return

    def get_fieldtype(self):
        return self.fieldtype

    def get_box(self):
        return self.box

    def set_box(self, box):
        self.box = box
        return

    def get_xyz(self):
        return self.xyz

    def set_xyz(self, xyz):
        self.xyz = xyz
        return

    def get_cen(self):
        return self.cen

    def set_cen(self, cen):
        self.cen = cen
        return

    def get_rad(self):
        return self.rad

    def set_rad(self, rad):
        self.rad = rad
        return

    def get_energy_type(self):
        return self.energy_type

    def set_energy_type(self, energy_type):
        self.energy_type = energy_type
        return

    def get_wall_energy(self):
        return self.wall_energy

    def set_wall_energy(self, wall_energy):
        self.wall_energy = wall_energy
        return
# End of class HardWall


####################################################################
#
# class: HarmonicAttractor
#
# Description: Contains the variables for one Harmonic Attractor
#
# Notes:
#   None
#
####################################################################
class HarmonicAttractor:
    def __init__(self):
        self.box = 1
        self.k = "0.0d0"
        self.nentries = 1
        self.refpos = "Initial"
        self.globx = "0.0d0"
        self.globy = "0.0d0"
        self.globz = "0.0d0"
        self.key = "Element"
        self.molec = []
        self.element = []
        self.name = []
        self.fieldtype = "Harmonic Attractor"
        return

    def get_fieldtype(self):
        return self.fieldtype

    def get_box(self):
        return self.box

    def set_box(self, box):
        self.box = box
        return

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k
        return

    def get_nentries(self):
        return self.nentries

    def set_nentries(self, nentries):
        self.nentries = nentries
        return

    def get_refpos(self):
        return self.refpos

    def set_refpos(self, refpos):
        self.refpos = refpos
        return

    def get_globx(self):
        return self.globx

    def set_globx(self, globx):
        self.globx = globx
        return

    def get_globy(self):
        return self.globy

    def set_globy(self, globy):
        self.globy = globy
        return

    def get_globz(self):
        return self.globz

    def set_globz(self, globz):
        self.globz = globz
        return

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key
        return

    def get_molec(self):
        return self.molec

    def set_molec(self, molec):
        self.molec = molec
        return

    def append_molec(self, molec):
        self.molec.append(molec)
        return

    def get_single_molec(self, index):
        return self.molec[index]

    def clear_molec(self):
        self.molec = []
        return

    def get_element(self):
        return self.element

    def set_element(self, element):
        self.element = element
        return

    def append_element(self, element):
        self.element.append(element)
        return

    def get_single_element(self, index):
        return self.element[index]

    def clear_element(self):
        self.element = []
        return

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return

    def append_name(self, name):
        self.name.append(name)
        return

    def get_single_name(self, index):
        print
        return self.name[index]

    def clear_name(self):
        self.name = []
        return
# End of class HarmonicAttractor

        
####################################################################
#
# class: HooperUmbrella
#
# Description: Contains the variables for one Hooper Umbrella
#
# Notes:
#   None
#
####################################################################
class HooperUmbrella:
    def __init__(self):
        self.box = 1
        self.xyz = "x"
        self.center = "0.0d0"
        self.a = "0.0d0"
        self.fieldtype = "Hooper Umbrella"
        return

    def get_fieldtype(self):
        return self.fieldtype

    def get_box(self):
        return self.box

    def set_box(self, box):
        self.box = box
        return

    def get_xyz(self):
        return self.xyz

    def set_xyz(self, xyz):
        self.xyz = xyz
        return

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        return

    def get_a(self):
        return self.a

    def set_a(self, a):
        self.a = a
        return
# End of class HooperUmbrella


####################################################################
#
# class: LJWall
#
# Description: Contains the variables for one LJ 9-3 Wall
#
# Notes:
#   When you reduce the value in ntypes, the class automatically
#   removes variables at the end of the name, sig, and eps
#   sequences until the new length is reached.  However, when you
#   increase the value in ntypes, the length of the sequences are
#   not automatically  increased.  This is so you can use
#   append_(name,sig,eps) to add the value without specifying
#   the index
#
####################################################################
class LJWall:
    def __init__(self):
        self.box = 1
        self.xyz = "x"
        self.cen = "0.0d0"
        self.dir = 1
        self.cut = "0.0d0"
        self.shift = True
        self.rho = "0.0d0"
        self.ntypes = 1
        self.name = []
        self.sig = []
        self.eps = []
        self.fieldtype = "LJ 9-3 Wall"
        return

    def get_fieldtype(self):
        return self.fieldtype

    def get_box(self):
        return self.box

    def set_box(self, box):
        self.box = box
        return

    def get_xyz(self):
        return self.xyz

    def set_xyz(self, xyz):
        self.xyz = xyz
        return

    def get_cen(self):
        return self.cen

    def set_cen(self, cen):
        self.cen = cen
        return

    def get_dir(self):
        return self.dir

    def set_dir(self, dir):
        self.dir = dir
        return

    def get_cut(self):
        return self.cut

    def set_cut(self, cut):
        self.cut = cut
        return

    def get_shift(self):
        return self.shift

    def set_shift_true(self):
        self.shift = True
        return

    def set_shift_false(self):
        self.shift = False
        return

    def get_rho(self):
        return self.rho

    def set_rho(self, rho):
        self.rho = rho
        return

    def get_ntypes(self):
        return self.ntypes

    def set_ntypes(self, ntypes):
        if self.ntypes > ntypes:
            del self.name[ntypes:]
            del self.sig[ntypes:]
            del self.eps[ntypes:]
        self.ntypes = ntypes
        return

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return

    def append_name(self, name):
        self.name.append(name)
        return

    def get_single_name(self, index):
        return self.name[index]

    def get_sig(self):
        return self.sig

    def set_sig(self, sig):
        self.sig = sig
        return

    def append_sig(self, sig):
        self.sig.append(sig)
        return

    def get_single_sig(self, index):
        return self.sig[index]

    def get_eps(self):
        return self.eps

    def set_eps(self, eps):
        self.eps = eps
        return

    def append_eps(self, eps):
        self.eps.append(eps)
        return

    def get_single_eps(self, index):
        return self.eps[index]
# End of class LJWall


####################################################################
#
# class: SteeleWall
#
# Description: Contains the variables for one Steele Wall
#
# Notes:
#   When you reduce the value in ntype, the class automatically
#   removes variables at the end of the name, sigma_sf, and 
#   epsilon_sf sequences until the new length is reached.  However,
#   when you increase the value in ntype, the length of the
#   sequences are not automatically increased.  This is so you can
#   use append_(name,sigma_sf,epsilon_sf) to add the value without
#   specifying the index
#
####################################################################
class SteeleWall:
    def __init__(self):
        self.box = 1
        self.xyz = "x"
        self.surface = "0.0d0"
        self.dir = 1
        self.cutoff = "0.0d0"
        self.shift = True
        self.delta = "0.0d0"
        self.rho_s = "0.0d0"
        self.ntype = 1
        self.name = []
        self.sigma_sf = []
        self.epsilon_sf = []
        self.fieldtype = "Steele Wall"
        return

    def get_fieldtype(self):
        return self.fieldtype

    def get_box(self):
        return self.box

    def set_box(self, box):
        self.box = box
        return

    def get_xyz(self):
        return self.xyz

    def set_xyz(self, xyz):
        self.xyz = xyz
        return

    def get_surface(self):
        return self.surface

    def set_surface(self, surface):
        self.surface = surface
        return

    def get_dir(self):
        return self.dir

    def set_dir(self, dir):
        self.dir = dir
        return

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        return

    def get_shift(self):
        return self.shift

    def set_shift_true(self):
        self.shift = True
        return

    def set_shift_false(self):
        self.shift = False
        return

    def get_delta(self):
        return self.delta

    def set_delta(self, delta):
        self.delta = delta
        return

    def get_rho_s(self):
        return self.rho_s

    def set_rho_s(self, rho_s):
        self.rho_s = rho_s
        return

    def get_ntype(self):
        return self.ntype

    def set_ntype(self, ntype):
        if(self.ntype > ntype):
            del self.name[ntype:]
            del self.sigma_sf[ntype:]
            del self.epsilon_sf[ntype:]
        self.ntype = ntype
        return

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return

    def append_name(self, name):
        self.name.append(name)
        return

    def get_single_name(self, index):
        return self.name[index]

    def get_sigma_sf(self):
        return self.sigma_sf

    def set_sigma_sf(self, sigma_sf):
        self.sigma_sf = sigma_sf
        return

    def append_sigma_sf(self, sigma_sf):
        self.sigma_sf.append(sigma_sf)
        return

    def get_single_sigma_sf(self, index):
        return self.sigma_sf[index]

    def get_epsilon_sf(self):
        return self.epsilon_sf

    def set_epsilon_sf(self, epsilon_sf):
        self.epsilon_sf = epsilon_sf
        return

    def append_epsilon_sf(self, epsilon_sf):
        self.epsilon_sf.append(epsilon_sf)
        return

    def get_single_epsilon_sf(self, index):
        return self.epsilon_sf[index]
# End of class SteeleWall


####################################################################
#
# class: IsotropicVolumeMove
#
# Description:
#
# Notes:
#
####################################################################
class IsotropicVolumeMove:
    def __init__(self):
        self.ensemble = "nvt"
        self.numboxes = 1
        self.pmvol = "0.0d0"
        self.pmvlpr = []
        self.rmvol = "0.0d0"
        self.tavol = "0.5"
        self.length = 1
        return

    def get_pmvlpr_length(self):
        return self.length

    def get_ensemble(self):
        return self.ensemble

    def set_ensemble(self, ensemble):
        self.ensemble = ensemble
        self.update_pmvlpr()
        return

    def get_numboxes(self):
        return self.numboxes

    def set_numboxes(self, numboxes):
        self.numboxes = numboxes
        self.update_pmvlpr()
        return

    def get_move_probability(self):
        return self.pmvol

    def set_move_probability(self, probability):
        self.pmvol = probability
        return

    def get_pmvlpr(self):
        return self.pmvlpr

    def set_pmvlpr(self, pmvlpr):
        self.pmvlpr = pmvlpr
        return

    def append_pmvlpr(self, pmvlpr):
        if len(self.pmvlpr) == self.length:
            raise "pmvlpr array is full"
            
        self.pmvlpr.append(pmvlpr)
        return

    def get_single_pmvlpr(self, index):
        return self.pmvlpr[index]

    def update_pmvlpr(self):
        current_length = self.length

        if self.ensemble == "nvt":
            new_length = (self.numboxes*(self.numboxes-1))/2
        else:
            new_length = self.numboxes

        if new_length < current_length:
            del self.pmvlpr[new_length:]

        self.length = new_length
        return

    def get_rmvol(self):
        return self.rmvol

    def set_rmvol(self, rmvol):
        self.rmvol = rmvol
        return

    def get_tavol(self):
        return self.tavol

    def set_tavol(self, tavol):
        self.tavol = tavol
        return
# End of class IsotropicVolumeMove


####################################################################
#
# class: AnisotropicVolumeMove
#
# Description:
#
# Notes:
#
####################################################################
class AnisotropicVolumeMove:
    def __init__(self):
        self.ensemble = "nvt"
        self.numboxes = 1
        self.pmcell = "0.0d0"
        self.pmcellpr = []
        self.pmcellpt = []
        self.rmcell = "0.0d0"
        self.tacell = "0.5"
        self.length = 1
        return

    def get_length(self):
        return self.length

    def get_ensemble(self):
        return self.ensemble

    def set_ensemble(self, ensemble):
        self.ensemble = ensemble
        self.update_avm()
        return

    def get_numboxes(self):
        return self.numboxes

    def set_numboxes(self, numboxes):
        self.numboxes = numboxes
        self.update_avm()
        return

    def get_move_probability(self):
        return self.pmcell

    def set_move_probability(self, probability):
        self.pmcell = probability
        return

    def get_pmcellpr(self):
        return self.pmcellpr

    def set_pmcellpr(self, pmcellpr):
        self.pmcellpr = pmcellpr
        return

    def append_pmcellpr(self, pmcellpr):
        if self.ensemble == "nvt":
            length = (self.numboxes*(self.numboxes-1))/2
        else:
            length = self.numboxes

        if len(self.pmcellpr) == length:
            raise "pmcellpr array is full"
            
        self.pmcellpr.append(pmcellpr)
        return

    def get_single_pmcellpr(self, index):
        return self.pmcellpr[index]

    def update_avm(self):
        current_length = self.length

        if self.ensemble == "nvt":
            new_length = (self.numboxes*(self.numboxes-1))/2
        else:
            new_length = self.numboxes

        if new_length < current_length:
            del self.pmcellpr[new_length:]
            del self.pmcellpt[new_length:]

        self.length = new_length
        return

    def get_pmcellpt(self):
        return self.pmcellpt

    def set_pmcellpt(self, pmcellpt):
        self.pmcellpt = pmcellpt
        return

    def append_pmcellpt(self, pmcellpt):
        self.pmcellpt.append(pmcellpt)
        return

    def get_single_pmcellpt(self, index):
        return self.pmcellpt[index]

    def get_rmcell(self):
        return self.rmcell

    def set_rmcell(self, rmcell):
        self.rmcell = rmcell
        return

    def get_tacell(self):
        return self.tacell

    def set_tacell(self, tacell):
        self.tacell = tacell
        return
# End of class AnisotropicVolumeMove


####################################################################
#
# class: RotationalBias2BoxMoleculeTransferMove
#
# Description:
#
# Notes:
#
####################################################################
class RotationalBias2BoxMoleculeTransferMove:
    def __init__(self):
        self.numboxes = 2
        self.nmolty = 1
        self.pm2boxrbswap = "0.0d0"
        self.pm2rbswmt = []
        self.pm2rbswpr = []
        self.nbp = 1
        return

    def get_nbp(self):
        return self.nbp

    def get_numboxes(self):
        return self.numboxes

    def set_numboxes(self, numboxes):
        if numboxes > 1:
            new_length = (numboxes*(numboxes-1))/2

            if new_length < self.nbp:
                del self.pm2rbswpr[new_length:]

            self.nbp = new_length
            self.numboxes = numboxes
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pm2rbswmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pm2boxrbswap

    def set_move_probability(self, probability):
        self.pm2boxrbswap = probability
        return

    def get_pm2rbswmt(self):
        return self.pm2rbswmt

    def set_pm2rbswmt(self, pm2rbswmt):
        self.pm2rbswmt = pm2rbswmt
        return

    def append_pm2rbswmt(self, pm2rbswmt):
        if len(self.pm2rbswmt) == self.nmolty:
            raise "pm2rbswmt array full"
            
        self.pm2rbswmt.append(pm2rbswmt)
        return

    def get_pm2rbswpr(self):
        return self.pm2rbswpr

    def set_pm2rbswpr(self, pm2rbswpr):
        self.pm2rbswpr = pm2rbswpr
        return

    def append_pm2rbswpr(self, pm2rbswpr):
        if len(self.pm2rbswpr) == self.nbp:
            raise "pm2rbswpr array full"
            
        self.pm2rbswpr.append(pm2rbswpr)
        return
# End of class RotationalBias2BoxMoleculeTransferMove
 

####################################################################
#
# class: ConfigurationalBias2BoxMoleculeTransferMove
#
# Description:
#
# Notes:
#
####################################################################
class ConfigurationalBias2BoxMoleculeTransferMove:
    def __init__(self):
        self.numboxes = 2
        self.nmolty = 1
        self.pm2boxcbswap = "0.0d0"
        self.pm2cbswmt = []
        self.pm2cbswpr = []
        self.nbp = 1
        return

    def get_nbp(self):
        return self.nbp

    def get_numboxes(self):
        return self.numboxes

    def set_numboxes(self, numboxes):
        if numboxes > 1:
            new_nbp = (numboxes*(numboxes-1))/2

            if new_nbp < self.nbp:
                del self.pm2cbswpr[new_nbp:]

            self.numboxes = numboxes
            self.nbp = new_nbp
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pm2cbswmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pm2boxcbswap

    def set_move_probability(self, probability):
        self.pm2boxcbswap = probability
        return

    def get_pm2cbswmt(self):
        return self.pm2cbswmt

    def set_pm2cbswmt(self, pm2cbswmt):
        self.pm2cbswmt = pm2cbswmt
        return

    def append_pm2cbswmt(self, pm2cbswmt):
        if len(self.pm2cbswmt) == self.nmolty:
            raise "pm2cbswmt array full"
            
        self.pm2cbswmt.append(pm2cbswmt)
        return

    def get_pm2cbswpr(self):
        return self.pm2cbswpr

    def set_pm2cbswpr(self, pm2cbswpr):
        self.pm2cbswpr = pm2cbswpr
        return

    def append_pm2cbswpr(self, pm2cbswpr):
        length = (self.numboxes*(self.numboxes-1))/2

        if len(self.pm2cbswpr) == length:
            raise "pm2cbswpr array full"
            
        self.pm2cbswpr.append(pm2cbswpr)
        return
# End of class ConfigurationalBias2BoxMoleculeTransferMove
 

####################################################################
#
# class: ConfigurationalBiasGrandCanonicalInsertionDeletionMove
#
# Description:
#
# Notes:
#
####################################################################
class ConfigurationalBiasGrandCanonicalInsertionDeletionMove:
    def __init__(self):
        self.nmolty = 1
        self.pmuvtcbswap = "0.0d0"
        self.pmuvtcbmt = []
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmuvtcbmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmuvtcbswap

    def set_move_probability(self, probability):
        self.pmuvtcbswap = probability
        return

    def get_pmuvtcbmt(self):
        return self.pmuvtcbmt

    def set_pmuvtcbmt(self, pmuvtcbmt):
        self.pmuvtcbmt = pmuvtcbmt
        return

    def append_pmuvtcbmt(self, pmuvtcbmt):
        if len(self.pmuvtcbmt) == self.nmolty:
            raise "pmuvtcbmt array full"
            
        self.pmuvtcbmt.append(pmuvtcbmt)
        return
# End of class ConfigurationalBiasGrandCanonicalInsertionDeletionMove
 

####################################################################
#
# class: ConfigurationalBiasSingleBoxMoleculeReinsertionMove
#
# Description:
#
# Notes:
#
####################################################################
class ConfigurationalBiasSingleBoxMoleculeReinsertionMove:
    def __init__(self):
        self.nmolty = 1
        self.pm1boxcbswap = "0.0d0"
        self.pm1cbswmt = []
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pm1cbswmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pm1boxcbswap

    def set_move_probability(self, probability):
        self.pm1boxcbswap = probability
        return

    def get_pm1cbswmt(self):
        return self.pm1cbswmt

    def set_pm1cbswmt(self, pm1cbswmt):
        self.pm1cbswmt = pm1cbswmt
        return

    def append_pm1cbswmt(self, pm1cbswmt):
        if len(self.pm1cbswmt) == self.nmolty:
            raise "pm1cbswmt array full"
            
        self.pm1cbswmt.append(pm1cbswmt)
        return
# End of class ConfigurationalBiasSingleBoxMoleculeReinsertionMove
 

####################################################################
#
# class: AggregationVolumeBiasMoveType1
#
# Description:
#
# Notes:
#
####################################################################
class AggregationVolumeBiasMoveType1:
    def __init__(self):
        self.nmolty = 1
        self.pmavb1 = "0.0d0"
        self.pmavb1in = "0.0d0"
        self.pmavb1mt = []
        self.pmavb1ct = []
        self.avb1rad = "0.0d0"
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmavb1mt[nmolty:]
            del self.pmavb1ct[nmolty:]
            for x in self.pmavb1ct:
                del x[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmavb1

    def set_move_probability(self, probability):
        self.pmavb1 = probability
        return

    def get_pmavb1in(self):
        return self.pmavb1in

    def set_pmavb1in(self, pmavb1in):
        self.pmavb1in = pmavb1in
        return

    def get_pmavb1mt(self):
        return self.pmavb1mt

    def set_pmavb1mt(self, pmavb1mt):
        self.pmavb1mt = pmavb1mt
        return

    def append_pmavb1mt(self, pmavb1mt):
        if len(self.pmavb1mt) == self.nmolty:
            raise "pmavb1mt array full"
            
        self.pmavb1mt.append(pmavb1mt)
        return

    def get_pmavb1ct(self):
        return self.pmavb1ct

    def set_pmavb1ct(self, pmavb1ct):
        self.pmavb1ct = pmavb1ct
        return

    def append_pmavb1ct(self, pmavb1ct):
        if len(pmavb1ct) != self.nmolty:
            raise "Not adding the right size array to pmavb1ct"

        if len(self.pmavb1ct) == self.nmolty:
            raise "pmavb1ct array full"
            
        self.pmavb1ct.append(pmavb1ct)
        return

    def get_single_pmavb1ct(self, x, y):
        return self.pmavb1ct[x][y]

    def set_single_pmavb1ct(self, x, y, pmavb1ct):
        self.pmavb1ct[x][y] = pmavb1ct
        return

    def append_single_pmavb1ct(self, index, pmavb1ct):
        if len(self.pmavb1ct[index]) == self.nmolty:
            raise "pmavb1ct subarray full"
            
        self.pmavb1ct[index].append(pmavb1ct)
        return

    def get_avb1rad(self):
        return self.avb1rad

    def set_avb1rad(self, avb1rad):
        self.avb1rad = avb1rad
        return
# End of class AggregationVolumeBiasMoveType1
 

####################################################################
#
# class: AggregationVolumeBiasMoveType2
#
# Description:
#
# Notes:
#
####################################################################
class AggregationVolumeBiasMoveType2:
    def __init__(self):
        self.nmolty = 1
        self.pmavb2 = "0.0d0"
        self.pmavb2in = "0.0d0"
        self.pmavb2mt = []
        self.pmavb2ct = []
        self.avb2rad = "0.0d0"
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmavb2mt[nmolty:]
            del self.pmavb2ct[nmolty:]
            for x in self.pmavb2ct:
                del x[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmavb2

    def set_move_probability(self, probability):
        self.pmavb2 = probability
        return

    def get_pmavb2in(self):
        return self.pmavb2in

    def set_pmavb2in(self, pmavb2in):
        self.pmavb2in = pmavb2in
        return

    def get_pmavb2mt(self):
        return self.pmavb2mt

    def set_pmavb2mt(self, pmavb2mt):
        self.pmavb2mt = pmavb2mt
        return

    def append_pmavb2mt(self, pmavb2mt):
        if len(self.pmavb2mt) == self.nmolty:
            raise "pmavb2mt array full"
            
        self.pmavb2mt.append(pmavb2mt)
        return

    def get_pmavb2ct(self):
        return self.pmavb2ct

    def set_pmavb2ct(self, pmavb2ct):
        self.pmavb2ct = pmavb2ct
        return

    def append_pmavb2ct(self, pmavb2ct):
        if len(pmavb2ct) != self.nmolty:
            raise "Not adding the right size array to pmavb2ct"

        if len(self.pmavb2ct) == self.nmolty:
            raise "pmavb2ct array full"
            
        self.pmavb2ct.append(pmavb2ct)
        return

    def get_single_pmavb2ct(self, x, y):
        return self.pmavb2ct[x][y]

    def set_single_pmavb2ct(self, x, y, pmavb2ct):
        self.pmavb2ct[x][y] = pmavb2ct
        return

    def append_single_pmavb2ct(self, index, pmavb2ct):
        if len(self.pmavb2ct[index]) == self.nmolty:
            raise "pmavb2ct subarray full"
            
        self.pmavb2ct[index].append(pmavb2ct)
        return

    def get_avb2rad(self):
        return self.avb2rad

    def set_avb2rad(self, avb2rad):
        self.avb2rad = avb2rad
        return
# End of class AggregationVolumeBiasMoveType2
 

####################################################################
#
# class: AggregationVolumeBiasMoveType3
#
# Description:
#
# Notes:
#
####################################################################
class AggregationVolumeBiasMoveType3:
    def __init__(self):
        self.nmolty = 1
        self.pmavb3 = "0.0d0"
        self.pmavb3mt = []
        self.pmavb3ct = []
        self.avb3rad = "0.0d0"
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmavb3mt[nmolty:]
            del self.pmavb3ct[nmolty:]
            for x in self.pmavb3ct:
                del x[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmavb3

    def set_move_probability(self, probability):
        self.pmavb3 = probability
        return

    def get_pmavb3mt(self):
        return self.pmavb3mt

    def set_pmavb3mt(self, pmavb3mt):
        self.pmavb3mt = pmavb3mt
        return

    def append_pmavb3mt(self, pmavb3mt):
        if len(self.pmavb3mt) == self.nmolty:
            raise "pmavb3mt array full"
            
        self.pmavb3mt.append(pmavb3mt)
        return

    def get_pmavb3ct(self):
        return self.pmavb3ct

    def set_pmavb3ct(self, pmavb3ct):
        self.pmavb3ct = pmavb3ct
        return

    def append_pmavb3ct(self, pmavb3ct):
        if len(pmavb3ct) != self.nmolty:
            raise "Not adding the right size array to pmavb3ct"

        if len(self.pmavb3ct) == self.nmolty:
            raise "pmavb3ct array full"
            
        self.pmavb3ct.append(pmavb3ct)
        return

    def get_single_pmavb3ct(self, x, y):
        return self.pmavb3ct[x][y]

    def set_single_pmavb3ct(self, x, y, pmavb3ct):
        self.pmavb3ct[x][y] = pmavb3ct
        return

    def append_single_pmavb3ct(self, index, pmavb3ct):
        if len(self.pmavb3ct[index]) == self.nmolty:
            raise "pmavb3ct subarray full"
            
        self.pmavb3ct[index].append(pmavb3ct)
        return

    def get_avb3rad(self):
        return self.avb3rad

    def set_avb3rad(self, avb3rad):
        self.avb3rad = avb3rad
        return
# End of class AggregationVolumeBiasMoveType3
 

####################################################################
#
# class: ConfigurationalBiasPartialMoleculeRegrowth
#
# Description:
#
# Notes:
#
####################################################################
class ConfigurationalBiasPartialMoleculeRegrowth:
    def __init__(self):
        self.nmolty = 1
        self.pmcb = "0.0d0"
        self.pmcbmt = []
        self.pmall = []
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmcbmt[nmolty:]
            del self.pmall[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmcb

    def set_move_probability(self, probability):
        self.pmcb = probability
        return

    def get_pmcbmt(self):
        return self.pmcbmt

    def set_pmcbmt(self, pmcbmt):
        self.pmcbmt = pmcbmt
        return

    def append_pmcbmt(self, pmcbmt):
        if len(self.pmcbmt) == self.nmolty:
            raise "pmcbmt array full"
            
        self.pmcbmt.append(pmcbmt)
        return

    def get_pmall(self):
        return self.pmall

    def set_pmall(self, pmall):
        self.pmall = pmall
        return

    def append_pmall(self, pmall):
        if len(self.pmall) == self.nmolty:
            raise "pmall array full"
            
        self.pmall.append(pmall)
        return
# End of class ConfigurationalBiasPartialMoleculeRegrowth
 

####################################################################
#
# class: ConfigurationalBiasProteinBackboneRegrowth
#
# Description:
#
# Notes:
#
####################################################################
class ConfigurationalBiasProteinBackboneRegrowth:
    def __init__(self):
        self.nmolty = 1
        self.pmback = "0.0d0"
        self.pmbkmt = []
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmbkmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmback

    def set_move_probability(self, probability):
        self.pmback = probability
        return

    def get_pmbkmt(self):
        return self.pmbkmt

    def set_pmbkmt(self, pmbkmt):
        self.pmbkmt = pmbkmt
        return

    def append_pmbkmt(self, pmbkmt):
        if len(self.pmbkmt) == self.nmolty:
            raise "pmbkmt array full"
            
        self.pmbkmt.append(pmbkmt)
        return
# End of class ConfigurationalBiasProteinBackboneRegrowth
 

####################################################################
#
# class: TorsionalPivotMove
#
# Description:
#
# Notes:
#
####################################################################
class TorsionalPivotMove:
    def __init__(self):
        self.nmolty = 1
        self.pmpivot = "0.0d0"
        self.pmpivmt = []
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmpivmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmpivot

    def set_move_probability(self, probability):
        self.pmpivot = probability
        return

    def get_pmpivmt(self):
        return self.pmpivmt

    def set_pmpivmt(self, pmpivmt):
        self.pmpivmt = pmpivmt
        return

    def append_pmpivmt(self, pmpivmt):
        if len(self.pmpivmt) == self.nmolty:
            raise "pmpivmt array full"
            
        self.pmpivmt.append(pmpivmt)
        return
# End of class TorsionalPivotMove
 

####################################################################
#
# class: ConcertedRotationMoveOnANonPeptideBackbone
#
# Description:
#
# Notes:
#
####################################################################
class ConcertedRotationMoveOnANonPeptideBackbone:
    def __init__(self):
        self.nmolty = 1
        self.pmconrot = "0.0d0"
        self.pmcrmt = []
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmcrmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmconrot

    def set_move_probability(self, probability):
        self.pmconrot = probability
        return

    def get_pmcrmt(self):
        return self.pmcrmt

    def set_pmcrmt(self, pmcrmt):
        self.pmcrmt = pmcrmt
        return

    def append_pmcrmt(self, pmcrmt):
        if len(self.pmcrmt) == self.nmolty:
            raise "pmcrmt array full"
            
        self.pmcrmt.append(pmcrmt)
        return
# End of class ConcertedRotationMoveOnANonPeptideBackbone
 

####################################################################
#
# class: ConcertedRotationMoveOverA3PeptidesBackboneSequence
#
# Description:
#
# Notes:
#
####################################################################
class ConcertedRotationMoveOverA3PeptidesBackboneSequence:
    def __init__(self):
        self.nmolty = 1
        self.pmcrback = "0.0d0"
        self.pmcrbmt = []
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmcrbmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmcrback

    def set_move_probability(self, probability):
        self.pmcrback = probability
        return

    def get_pmcrbmt(self):
        return self.pmcrbmt

    def set_pmcrbmt(self, pmcrbmt):
        self.pmcrbmt = pmcrbmt
        return

    def append_pmcrbmt(self, pmcrbmt):
        if len(self.pmcrbmt) == self.nmolty:
            raise "pmcrbmt array full"
            
        self.pmcrbmt.append(pmcrbmt)
        return
# End of class ConcertedRotationMoveOverA3PeptidesBackboneSequence
 

####################################################################
#
# class: PlaneShiftMove
#
# Description:
#
# Notes:
#
####################################################################
class PlaneShiftMove:
    def __init__(self):
        self.numboxes = 1
        self.pmplane = "0.0d0"
        self.pmplanebox = []
        self.planewidth = "0.0d0"
        return

    def get_numboxes(self):
        return self.numboxes

    def set_numboxes(self, numboxes):
        if numboxes < self.numboxes:
            del self.pmplanebox[numboxes:]

        self.numboxes = numboxes
        return

    def get_move_probability(self):
        return self.pmplane

    def set_move_probability(self, probability):
        self.pmplane = probability
        return

    def get_pmplanebox(self):
        return self.pmplanebox

    def set_pmplanebox(self, pmplanebox):
        self.pmplanebox = pmplanebox
        return

    def append_pmplanebox(self, pmplanebox):
        if len(self.pmplanebox) == self.numboxes:
            raise "pmplanebox array full"
            
        self.pmplanebox.append(pmplanebox)
        return

    def get_planewidth(self):
        return self.planewidth

    def set_planewidth(self, planewidth):
        self.planewidth = planewidth
        return
# End of class PlaneShiftMove
 

####################################################################
#
# class: RowShiftMove
#
# Description:
#
# Notes:
#
####################################################################
class RowShiftMove:
    def __init__(self):
        self.numboxes = 1
        self.pmrow = "0.0d0"
        self.pmrowbox = []
        self.rowwidth = "0.0d0"
        return

    def get_numboxes(self):
        return self.numboxes

    def set_numboxes(self, numboxes):
        if numboxes < self.numboxes:
            del self.pmrowbox[numboxes:]

        self.numboxes = numboxes
        return

    def get_move_probability(self):
        return self.pmrow

    def set_move_probability(self, probability):
        self.pmrow = probability
        return

    def get_pmrowbox(self):
        return self.pmrowbox

    def set_pmrowbox(self, pmrowbox):
        self.pmrowbox = pmrowbox
        return

    def append_pmrowbox(self, pmrowbox):
        if len(self.pmrowbox) == self.numboxes:
            raise "pmrowbox array full"
            
        self.pmrowbox.append(pmrowbox)
        return

    def get_rowwidth(self):
        return self.rowwidth

    def set_rowwidth(self, rowwidth):
        self.rowwidth = rowwidth
        return
# End of class RowShiftMove
 

####################################################################
#
# class: IntramolecularSingleAtomTranslationMove
#
# Description:
#
# Notes:
#
####################################################################
class IntramolecularSingleAtomTranslationMove:
    def __init__(self):
        self.nmolty = 1
        self.pmtraat = "0.0d0"
        self.pmtamt = []
        self.rmtraa = "0.0d0"
        self.tatraa = "0.5"
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmtamt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmtraat

    def set_move_probability(self, probability):
        self.pmtraat = probability
        return

    def get_pmtamt(self):
        return self.pmtamt

    def set_pmtamt(self, pmtamt):
        self.pmtamt = pmtamt
        return

    def append_pmtamt(self, pmtamt):
        if len(self.pmtamt) == self.nmolty:
            raise "pmtamt array full"
            
        self.pmtamt.append(pmtamt)
        return

    def get_rmtraa(self):
        return self.rmtraa

    def set_rmtraa(self, rmtraa):
        self.rmtraa = rmtraa
        return

    def get_tatraa(self):
        return self.tatraa

    def set_tatraa(self, tatraa):
        self.tatraa = tatraa
        return
# End of class IntramolecularSingleAtomTranslationMove
 

####################################################################
#
# class: CenterOfMassMoleculeTranslationMove
#
# Description:
#
# Notes:
#
####################################################################
class CenterOfMassMoleculeTranslationMove:
    def __init__(self):
        self.nmolty = 1
        self.pmtracm = "0.0d0"
        self.pmtcmt = []
        self.rmtrac = "0.0d0"
        self.tatrac = "0.5"
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmtcmt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmtracm

    def set_move_probability(self, probability):
        self.pmtracm = probability
        return

    def get_pmtcmt(self):
        return self.pmtcmt

    def set_pmtcmt(self, pmtcmt):
        self.pmtcmt = pmtcmt
        return

    def append_pmtcmt(self, pmtcmt):
        if len(self.pmtcmt) == self.nmolty:
            raise "pmtcmt array full"
            
        self.pmtcmt.append(pmtcmt)
        return

    def get_rmtrac(self):
        return self.rmtrac

    def set_rmtrac(self, rmtrac):
        self.rmtrac = rmtrac
        return

    def get_tatrac(self):
        return self.tatrac

    def set_tatrac(self, tatrac):
        self.tatrac = tatrac
        return
# End of class CenterOfMassMoleculeTranslationMove
 

####################################################################
#
# class: RotationAboutTheCenterOfMassMove
#
# Description:
#
# Notes:
#
####################################################################
class RotationAboutTheCenterOfMassMove:
    def __init__(self):
        self.nmolty = 1
        self.pmrotate = "0.0d0"
        self.pmromt = []
        self.rmrot = "0.0d0"
        self.tarot = "0.5"
        return

    def get_nmolty(self):
        return self.nmolty

    def set_nmolty(self, nmolty):
        if nmolty < self.nmolty:
            del self.pmromt[nmolty:]

        self.nmolty = nmolty
        return

    def get_move_probability(self):
        return self.pmrotate

    def set_move_probability(self, probability):
        self.pmrotate = probability
        return

    def get_pmromt(self):
        return self.pmromt

    def set_pmromt(self, pmromt):
        self.pmromt = pmromt
        return

    def append_pmromt(self, pmromt):
        if len(self.pmromt) == self.nmolty:
            raise "pmromt array full"
            
        self.pmromt.append(pmromt)
        return

    def get_rmrot(self):
        return self.rmrot

    def set_rmrot(self, rmrot):
        self.rmrot = rmrot
        return

    def get_tarot(self):
        return self.tarot

    def set_tarot(self, tarot):
        self.tarot = tarot
        return
# End of class RotationAboutTheCenterOfMassMove
 

####################################################################
#
# class: Vibrations
#
# Description:
#
# Notes:
#
####################################################################
class Vibrations:
    def __init__(self):
        self.vib_num = 0
        self.vibrations = []
        return

    def get_number_vibrations(self):
        return self.vib_num

    def set_number_vibrations(self, vib_num):
        self.vib_num = vib_num
        return

    def get_vibrations(self):
        return self.vibrations

    def set_vibrations(self, vibrations):
        self.vibrations = vibrations
        return

    def append_vibrations(self, vibrations):
        self.vibrations.append(vibrations)
        return
# End of class Vibrations


####################################################################
#
# class: Bendings
#
# Description:
#
# Notes:
#
####################################################################
class Bendings:
    def __init__(self):
        self.bending_num = 0
        self.bendings = []
        return

    def get_number_bendings(self):
        return self.bending_num

    def set_number_bendings(self, bending_num):
        self.bending_num = bending_num
        return

    def get_bendings(self):
        return self.bendings

    def set_bendings(self, bendings):
        self.bendings = bendings
        return

    def append_bendings(self, bendings):
        self.bendings.append(bendings)
        return
# End of class Bendings


####################################################################
#
# class: Torsions
#
# Description:
#
# Notes:
#
####################################################################
class Torsions:
    def __init__(self):
        self.tor_num = 0
        self.torsions = []
        return

    def get_number_torsions(self):
        return self.tor_num

    def set_number_torsions(self, tor_num):
        self.tor_num = tor_num
        return

    def get_torsions(self):
        return self.torsions

    def set_torsions(self, torsions):
        self.torsions = torsions
        return

    def append_torsions(self, torsions):
        self.torsions.append(torsions)
        return
# End of class Torsions


####################################################################
#
# class: AngleAngles
#
# Description:
#
# Notes:
#
####################################################################
class AngleAngles:
    def __init__(self):
        self.angle_num = 0
        self.angles = []
        return

    def get_number_angles(self):
        return self.angle_num

    def set_number_angles(self, angle_num):
        self.angle_num = angle_num
        return

    def get_angles(self):
        return self.angles

    def set_angles(self, angles):
        self.angles = angles
        return

    def append_angles(self, angles):
        self.angles.append(angles)
        return
# End of class AngleAngles


####################################################################
#
# class: ImproperTorsions
#
# Description:
#
# Notes:
#
####################################################################
class ImproperTorsions:
    def __init__(self):
        self.imptor_num = 0
        self.improper_torsions = []
        return

    def get_number_improper_torsions(self):
        return self.imptor_num

    def set_number_improper_torsions(self, imptor_num):
        self.imptor_num = imptor_num
        return

    def get_improper_torsions(self):
        return self.improper_torsions

    def set_improper_torsions(self, improper_torsions):
        self.improper_torsions = improper_torsions
        return

    def append_improper_torsions(self, improper_torsion):
        self.improper_torsions.append(improper_torsion)
        return
# End of class ImproperTorsions


####################################################################
#
# class: ExplicitDeclaration
#
# Description:
#
# Notes:
#
####################################################################
class ExplicitDeclaration:
    def __init__(self):
        self.nunit = 1
        self.nmaxcbmc = 1
        self.lpdb = "true"
        self.unit = []
        self.type = []
        self.qqatom = []
        self.pdbname = []
        self.aminonum = []
        self.aminoshort = []
        self.vibrations = []
        self.bendings = []
        self.torsions = []
        self.angles = []
        self.improper_torsions = []
        self.inpstyle = 0
        return

    def get_inpstyle(self):
        return self.inpstyle

    def get_nunit(self):
        return self.nunit

    def set_nunit(self, nunit):
        if(self.nunit > nunit):
            del self.unit[nunit:]
            del self.type[nunit:]
            del self.qqatom[nunit:]
            del self.pdbname[nunit:]
            del self.aminonum[nunit:]
            del self.aminoshort[nunit:]
            del self.vibrations[nunit:]
            del self.bendings[nunit:]
            del self.torsions[nunit:]
            del self.angles[nunit:]
            del self.improper_torsions[nunit:]
        self.nunit = nunit
        return

    def get_nmaxcbmc(self):
        return self.nmaxcbmc

    def set_nmaxcbmc(self, nmaxcbmc):
        self.nmaxcbmc = nmaxcbmc
        return

    def get_lpdb(self):
        return self.lpdb

    def set_lpdb_true(self):
        self.lpdb = True
        return

    def set_lpdb_false(self):
        self.lpdb = False
        return

    def get_unit(self):
        return self.unit

    def set_unit(self, unit):
        self.unit = unit
        return

    def append_unit(self, unit):
        self.unit.append(unit)
        return

    def get_single_unit(self, index):
        return self.unit[index]

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type
        return

    def append_type(self, type):
        self.type.append(type)
        return

    def get_single_type(self, index):
        return self.type[index]

    def get_qqatom(self):
        return self.qqatom

    def set_qqatom(self, qqatom):
        self.qqatom = qqatom
        return

    def append_qqatom(self, qqatom):
        self.qqatom.append(qqatom)
        return

    def get_single_qqatom(self, index):
        return self.qqatom[index]

    def get_pdbname(self):
        return self.pdbname

    def set_pdbname(self, pdbname):
        self.pdbname = pdbname
        return

    def append_pdbname(self, pdbname):
        self.pdbname.append(pdbname)
        return

    def get_single_pdbname(self, index):
        return self.pdbname[index]

    def get_aminonum(self):
        return self.aminonum

    def set_aminonum(self, aminonum):
        self.aminonum = aminonum
        return

    def get_single_aminonum(self, index):
        return self.aminonum[index]

    def append_aminonum(self, aminonum):
        self.aminonum.append(aminonum)
        return

    def get_aminoshort(self):
        return self.aminoshort

    def set_aminoshort(self, aminoshort):
        self.aminoshort = aminoshort
        return

    def append_aminoshort(self, aminoshort):
        self.aminoshort.append(aminoshort)
        return

    def get_single_aminoshort(self, index):
        return self.aminoshort[index]

    def get_vibrations(self):
        return self.vibrations

    def set_vibrations(self, vibrations):
        self.vibrations = vibrations
        return

    def append_vibrations(self, vibrations):
        self.vibrations.append(vibrations)
        return

    def create_vibrations(self):
        return Vibrations()

    def get_single_vibration(self, index):
        return self.vibrations[index]

    def clear_vibrations(self):
        self.vibrations = []

    def get_bendings(self):
        return self.bendings

    def set_bendings(self, bendings):
        self.bendings = bendings
        return

    def append_bendings(self, bendings):
        self.bendings.append(bendings)
        return

    def create_bendings(self):
        return Bendings()

    def get_single_bending(self, index):
        return self.bendings[index]

    def clear_bendings(self):
        self.bendings = []

    def get_torsions(self):
        return self.torsions

    def set_torsions(self, torsions):
        self.torsions = torsions
        return

    def append_torsions(self, torsions):
        self.torsions.append(torsions)
        return

    def create_torsions(self):
        return Torsions()

    def get_single_torsion(self, index):
        return self.torsions[index]

    def clear_torsions(self):
        self.torsions = []

    def get_angles(self):
        return self.angles

    def set_angles(self, angles):
        self.angles = angles
        return

    def append_angles(self, angles):
        self.angles.append(angles)
        return

    def create_angles(self):
        return AngleAngles()

    def get_single_angle(self, index):
        return self.angles[index]

    def clear_angles(self):
        self.angles = []

    def get_improper_torsions(self):
        return self.improper_torsions

    def set_improper_torsions(self, improper_torsions):
        self.improper_torsions = improper_torsions
        return

    def append_improper_torsions(self, improper_torsions):
        self.improper_torsions.append(improper_torsions)
        return

    def create_improper_torsions(self):
        return ImproperTorsions()

    def get_single_improper_torsion(self, index):
        return self.improper_torsions[index]

    def clear_improper_torsions(self):
        self.improper_torsions = []
# End of class ExplicitDeclaration


####################################################################
#
# class: PolypeptideBuilder
#
# Description:
#
# Notes:
#
####################################################################
class PolypeptideBuilder:
    def __init__(self):
        self.nunit = 1
        self.nmaxcbmc = 1
        self.forcefield = ""
        self.protgeom = "linear"
        self.pepname = []
        self.stereochem = []
        self.bondpartner = []
        self.terminus = []
        self.inpstyle = 1
        return

    def get_inpstyle(self):
        return self.inpstyle

    def get_nunit(self):
        return self.nunit

    def set_nunit(self, nunit):
        if(self.nunit > nunit):
            del self.pepname[nunit:]
            del self.stereochem[nunit:]
            del self.bondpartner[nunit:]
            del self.terminus[nunit:]
        self.nunit = nunit
        return

    def get_nmaxcbmc(self):
        return self.nmaxcbmc

    def set_nmaxcbmc(self, nmaxcbmc):
        self.nmaxcbmc = nmaxcbmc
        return

    def get_forcefield(self):
        return self.forcefield

    def set_forcefield(self, forcefield):
        self.forcefield = forcefield
        return

    def get_protgeom(self):
        return self.protgeom

    def set_protgeom(self, protgeom):
        self.protgeom = protgeom
        return

    def get_pepname(self):
        return self.pepname

    def set_pepname(self, pepname):
        self.pepname = pepname
        return

    def append_pepname(self, pepname):
        self.pepname.append(pepname)
        return

    def get_single_pepname(self, index):
        return self.pepname[index]

    def clear_pepname(self):
        self.pepname = []
        return

    def get_stereochem(self):
        return self.stereochem

    def set_stereochem(self, stereochem):
        self.stereochem = stereochem
        return

    def append_stereochem(self, stereochem):
        self.stereochem.append(stereochem)
        return

    def get_single_stereochem(self, index):
        return self.stereochem[index]

    def clear_stereochem(self):
        self.stereochem = []
        return

    def get_bondpartner(self):
        return self.bondpartner

    def set_bondpartner(self, bondpartner):
        self.bondpartner = bondpartner
        return

    def append_bondpartner(self, bondpartner):
        self.bondpartner.append(bondpartner)
        return

    def get_single_bondpartner(self, index):
        return self.bondpartner[index]

    def clear_bondpartner(self):
        self.bondpartner = []
        return

    def get_terminus(self):
        return self.terminus

    def set_terminus(self, terminus):
        self.terminus = terminus
        return

    def append_terminus(self, terminus):
        self.terminus.append(terminus)
        return

    def get_single_terminus(self, index):
        return self.terminus[index]

    def clear_terminus(self):
        self.terminus = []
        return
# End of class PolypeptideBuilder


####################################################################
#
# class: AtomBasedConnectivityMap
#
# Description:
#
# Notes:
#
####################################################################
class AtomBasedConnectivityMap:
    def __init__(self):
        self.nunit = 1
        self.nmaxcbmc = 1
        self.forcefield = ""
        self.charge_assignment = "manual"
        self.unit = []
        self.type = []
        self.qqatom = []
        self.vibrations = []
        self.improper_torsions = []
        self.inpstyle = 2
        return

    def get_inpstyle(self):
        return self.inpstyle

    def get_nunit(self):
        return self.nunit

    def set_nunit(self, nunit):
        if(self.nunit > nunit):
            del self.unit[nunit:]
            del self.type[nunit:]
            del self.qqatom[nunit:]
            del self.vib_num[nunit:]
            del self.vibrations[nunit:]
            del self.imptor_num[nunit:]
            del self.improper_torsions[nunit:]
        self.nunit = nunit
        return

    def get_nmaxcbmc(self):
        return self.nmaxcbmc

    def set_nmaxcbmc(self, nmaxcbmc):
        self.nmaxcbmc = nmaxcbmc
        return

    def get_forcefield(self):
        return self.forcefield

    def set_forcefield(self, forcefield):
        self.forcefield = forcefield
        return

    def get_charge_assignment(self):
        return self.charge_assignment

    def set_charge_assignment(self, charge_assignment):
        self.charge_assignment = charge_assignment
        return

    def get_unit(self):
        return self.unit

    def set_unit(self, unit):
        self.unit = unit
        return

    def append_unit(self, unit):
        self.unit.append(unit)
        return

    def get_single_unit(self, index):
        return self.unit[index]

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type
        return

    def append_type(self, type):
        self.type.append(type)
        return

    def get_single_type(self, index):
        return self.type[index]

    def get_qqatom(self):
        return self.qqatom

    def set_qqatom(self, qqatom):
        self.qqatom = qqatom
        return

    def append_qqatom(self, qqatom):
        self.qqatom.append(qqatom)
        return

    def get_single_qqatom(self, index):
        return self.qqatom[index]

    def get_vibrations(self):
        return self.vibrations

    def set_vibrations(self, vibrations):
        self.vibrations = vibrations
        return

    def append_vibrations(self, vibrations):
        self.vibrations.append(vibrations)
        return
        
    def create_vibrations(self):
        return Vibrations()

    def get_single_vibration(self, index):
        return self.vibrations[index]

    def clear_vibrations(self):
        self.vibrations = []

    def get_improper_torsions(self):
        return self.improper_torsions

    def set_improper_torsions(self, improper_torsions):
        self.improper_torsions = improper_torsions
        return

    def append_improper_torsions(self, improper_torsions):
        self.improper_torsions.append(improper_torsions)
        return

    def create_improper_torsions(self):
        return ImproperTorsions()

    def get_single_improper_torsion(self, index):
        return self.improper_torsions[index]

    def clear_improper_torsions(self):
        self.improper_torsions = []
# End of class AtomBasedConnectivityMap


####################################################################
#
# class: NucleicAcidBuilder
#
# Description: Contains the variables for one Nucleic Acid
#
# Notes:
#   When you reduce the value in nunit, the classautomatically
#   removes variables at the end of the monomername until the new
#   length is reached.  However, when you increase the value in
#   nunit, the length of the sequences are not automatically
#   increased.  This is so you can use append_monomername to add
#   the value without specifying the index
#
####################################################################
class NucleicAcidBuilder:
    def __init__(self):
        self.nunit = 1
        self.nmaxcbmc = 1
        self.terminus = 3
        self.forcefield = ""
        self.monomername=[]
        self.inpstyle = 3
        return

    def get_inpstyle(self):
        return self.inpstyle

    def get_nunit(self):
        return self.nunit

    def set_nunit(self, nunit):
        if(self.nunit > nunit):
            del self.monomername[nunit:]
        self.nunit = nunit
        return

    def get_nmaxcbmc(self):
        return self.nmaxcbmc

    def set_nmaxcbmc(self, nmaxcbmc):
        self.nmaxcbmc = nmaxcbmc
        return

    def get_terminus(self):
        return self.terminus

    def set_terminus(self, terminus):
        self.terminus = terminus
        return

    def get_forcefield(self):
        return self.forcefield

    def set_forcefield(self, forcefield):
        self.forcefield = forcefield
        return

    def get_monomername(self):
        return self.monomername

    def set_monomername(self, monomername):
        self.monomername = monomername
        return

    def append_monomername(self, monomername):
        self.monomername.append(monomername)
        return
# End of class NucleicAcidBuilder

####################################################################
#
# class: NanotubeBuilder
#
# Description: Contains the variables for one Nanotube
#
# Notes:
#   None
#
####################################################################
class NanotubeBuilder:
    def __init__(self):
        self.forcefield = ""
        self.atomname = ""
        self.qqatom = "0.0d0"
        self.n = 0
        self.m = 0
        self.ncells = 0
        self.bondlength="0.0d0"
        self.inpstyle = 4
        return

    def get_nunit(self):
        return ""

    def get_nmaxcbmc(self):
        return ""

    def get_inpstyle(self):
        return self.inpstyle

    def get_forcefield(self):
        return self.forcefield

    def set_forcefield(self, forcefield):
        self.forcefield = forcefield
        return

    def get_atomname(self):
        return self.atomname

    def set_atomname(self, atomname):
        self.atomname = atomname
        return

    def get_qqatom(self):
        return self.qqatom

    def set_qqatom(self, qqatom):
        self.qqatom = qqatom
        return

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n
        return

    def get_m(self):
        return self.m

    def set_m(self, m):
        self.m = m
        return

    def get_ncells(self):
        return self.ncells

    def set_ncells(self, ncells):
        self.ncells = ncells
        return

    def get_bondlength(self):
        return self.bondlength

    def set_bondlength(self, bondlength):
        self.bondlength = bondlength
        return
# End of class NanotubeBuilder
