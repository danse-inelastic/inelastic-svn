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



from vimm.Material import Material
from vimm.Utilities import path_split,cleansym
from vimm.IO.TowheeInputFile import load_towhee_file, save_towhee_file
from vimm.IO.TowheeLammpFile import load_lammp_file, save_lammp_file
from vimm.IO.TowheeDatabaseFile import load_database_file, save_database_file
from vimm.IO.TowheeInput import TowheeInput

extensions = [""]
filetype = "Towhee Input"

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    file=open(fullfilename, 'r')
    #
    # Initialize atom data
    #
    material = Material(fileprefix)
    material.name = fileprefix
    material.towhee_options = None
    #
    # These 2 are at the beginning of every file format
    # Random Number Seed
    #
    line = file.readline()
    line = file.readline()
    randomseed = int(line.strip())
    #
    # Input Format
    #
    line = file.readline()
    templine = file.readline()
    line = templine.strip()
    iformat = line[1:-1]

    # 3 different input formats
    if iformat == "Towhee":
        towhee = load_towhee_file(file)
        if towhee:
           towhee.set_randomseed(randomseed)
    elif iformat == "LAMMPS":
        # Close towhee_input file and open lammps_data
        file.close()
        towhee = load_lammp_file(filedir)
    elif iformat == "Database":
        towhee = load_database_file(file, filedir)
    else:
        print "Invalid format: " + iformat

    material.towhee_options = towhee
    return material

def save(fullfilename, material):
    filedir, fileprefix, fileext = path_split(fullfilename)
    file=open(fullfilename, 'w')
    
    towhee = material.towhee_options

    if towhee.get_iformat() == "Towhee":
        save_towhee_file(file, towhee)
    elif towhee.get_iformat() == "LAMMPS":
        # Close towhee_input file and open lammps_data
        save_lammp_file(file, towhee)
    elif towhee.get_iformat() == "Database":
        save_database_file(file, towhee)
    else:
        print "Invalid towhee format"

    return

def new():
    material = Material("towhee_input")
    material.towhee_options = TowheeInput()
    material.towhee_options.append_nmolectyp(1)
    material.towhee_options.append_chempot("")
    material.towhee_options.append_chempotperstep("10")
    material.towhee_options.append_ff_filename("")
    material.towhee_options.set_initstyle([[""]])
    material.towhee_options.set_initlattice([[""]])
    material.towhee_options.set_initmol([[1]])
    hm = material.towhee_options.create_hmatrix()
    material.towhee_options.append_hmatrix(hm)
    material.towhee_options.append_inix(1)
    material.towhee_options.append_iniy(1)
    material.towhee_options.append_iniz(1)
    material.towhee_options.append_inimix(0)
    material.towhee_options.append_box_number_density("")
    material.towhee_options.set_cmix_npair(1)
    material.towhee_options.append_cmix_pair_list("")
    mcm = material.towhee_options.get_rb2bmtm()
    mcm.append_pm2rbswmt("1.00d0")
    material.towhee_options.set_rb2bmtm(mcm)
    mcm = material.towhee_options.get_cb2bmtm()
    mcm.append_pm2cbswmt("1.00d0")
    material.towhee_options.set_cb2bmtm(mcm)
    mcm = material.towhee_options.get_cbgcidm()
    mcm.append_pmuvtcbmt("1.00d0")
    material.towhee_options.set_cbgcidm(mcm)
    mcm = material.towhee_options.get_cbsbmrm()
    mcm.append_pm1cbswmt("1.00d0")
    material.towhee_options.set_cbsbmrm(mcm)
    mcm = material.towhee_options.get_avbmt1()
    mcm.append_pmavb1mt("1.00d0")
    mcm.append_pmavb1ct(["1.00d0"])
    material.towhee_options.set_avbmt1(mcm)
    mcm = material.towhee_options.get_avbmt2()
    mcm.append_pmavb2mt("1.00d0")
    mcm.append_pmavb2ct(["1.00d0"])
    material.towhee_options.set_avbmt2(mcm)
    mcm = material.towhee_options.get_avbmt3()
    mcm.append_pmavb3mt("1.00d0")
    mcm.append_pmavb3ct(["1.00d0"])
    material.towhee_options.set_avbmt3(mcm)
    mcm = material.towhee_options.get_cbpmr()
    mcm.append_pmcbmt("1.00d0")
    mcm.append_pmall("1.00d0")
    material.towhee_options.set_cbpmr(mcm)
    mcm = material.towhee_options.get_cbpbr()
    mcm.append_pmbkmt("1.00d0")
    material.towhee_options.set_cbpbr(mcm)
    mcm = material.towhee_options.get_tpm()
    mcm.append_pmpivmt("1.00d0")
    material.towhee_options.set_tpm(mcm)
    mcm = material.towhee_options.get_crnmoanpb()
    mcm.append_pmcrmt("1.00d0")
    material.towhee_options.set_crnmoanpb(mcm)
    mcm = material.towhee_options.get_crnmoa3pbs()
    mcm.append_pmcrbmt("1.00d0")
    material.towhee_options.set_crnmoa3pbs(mcm)
    mcm = material.towhee_options.get_psm()
    mcm.append_pmplanebox("1.00d0")
    material.towhee_options.set_psm(mcm)
    mcm = material.towhee_options.get_rsm()
    mcm.append_pmrowbox("1.00d0")
    material.towhee_options.set_rsm(mcm)
    mcm = material.towhee_options.get_isatm()
    mcm.append_pmtamt("1.00d0")
    material.towhee_options.set_isatm(mcm)
    mcm = material.towhee_options.get_cofmmtm()
    mcm.append_pmtcmt("1.00d0")
    material.towhee_options.set_cofmmtm(mcm)
    mcm = material.towhee_options.get_ratcomm()
    mcm.append_pmromt("1.00d0")
    material.towhee_options.set_ratcomm(mcm)

    material.towhee_options.append_nch_nb_one(10)
    material.towhee_options.append_nch_nb(10)
    material.towhee_options.append_nch_tor_out(10)
    material.towhee_options.append_nch_tor_in(10) 
    material.towhee_options.append_nch_tor_in_con(100)
    material.towhee_options.append_nch_bend_a(1000)
    material.towhee_options.append_nch_bend_b(1000)
    material.towhee_options.append_nch_vib(1000)

    inp = material.towhee_options.create_input(4)
    material.towhee_options.append_input(inp)
    return material
