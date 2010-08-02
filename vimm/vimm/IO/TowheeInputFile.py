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

from vimm.IO.TowheeInput import *

###############################################################################
#
# Function: load_towhee_file
#
# This functon reads in the file and loads the data into a
# TowheeInput object.  It also pads certain variables with
# dummy data to make it easier on the GUI.  If you are using
# vimmLib with your towhee_input files, you should be aware
# of this when you are changing the file around.
#
###############################################################################
def load_towhee_file(file):
    towhee = TowheeInput()

    # Add all the valid variable names to a big array
    good_strings = load_good_strings()

    location = file.tell()
    line = file.readline()
    if verify_line(line, "ensemble"):
        templine = file.readline()
        line = filter_line(templine)
        towhee.set_ensemble(line)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "ensemble")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "temperature"):
        line = file.readline()
        towhee.set_temperature(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "temperature")
            return None

    if towhee.get_ensemble() == "npt":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "pressure"):
            line = file.readline()
            towhee.set_pressure(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "pressure")
                return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nmolty"):
        line = file.readline()
        towhee.set_nmolty(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "nmolty")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nmolectyp"):
        line = file.readline()
        nmolectyp = map(int, line.split())
        towhee.set_nmolectyp(nmolectyp)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nmolectyp(0)
        else:
            error_message(line, "nmolectyp")
            return None
    #
    # Chemical Potential... maybe.. if not, add a bunch of blanks
    # This makes it easier on the editor
    #
    if towhee.get_ensemble() == "uvt":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "chempot"):
            line = file.readline()
            chempot = line.split()
            towhee.set_chempot(chempot)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_nmolty()):
                    towhee.append_chempot("")
            else:
                error_message(line, "chempot")
                return None
    else:
        for i in range(towhee.get_nmolty()):
            towhee.append_chempot("")

    location = file.tell()
    line = file.readline()
    if verify_line(line, "numboxes"):
        line = file.readline()
        towhee.set_numboxes(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "numboxes")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "stepstyle"):
        templine = file.readline()
        line = filter_line(templine)
        towhee.set_stepstyle(line)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "stepstyle")
            return None

    if towhee.get_stepstyle() == "cycles" or towhee.get_stepstyle() == "moves":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "nstep"):
            line = file.readline()
            towhee.set_nstep(int(line.strip()))
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "nstep")
                return None
    elif towhee.get_stepstyle() == "minimize":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "optstyle"):
            line = file.readline()
            towhee.set_optstyle(int(line.strip()))
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "optstyle")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "mintol"):
            line = file.readline()
            towhee.set_mintol(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "mintol")
                return None
    else:
        print "Invalid stepstyle: " + towhee.get_stepstyle()
        return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "printfreq"):
        line = file.readline()
        towhee.set_printfreq(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "printfreq")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "blocksize"):
        line = file.readline()
        towhee.set_blocksize(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "blocksize")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "moviefreq"):
        line = file.readline()
        towhee.set_moviefreq(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "moviefreq")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "backupfreq"):
        line = file.readline()
        towhee.set_backupfreq(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "backupfreq")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "runoutput"):
        templine = file.readline()
        line = filter_line(templine)
        towhee.set_runoutput(line)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "runoutput")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pdb_output_freq"):
        line = file.readline()
        towhee.set_pdb_output_freq(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pdb_output_freq")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "loutdft"):
        line = file.readline()
        tf = is_it_true(line)
        if tf:
            towhee.set_loutdft_true()
        else:
            towhee.set_loutdft_false()
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "loutdft")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "loutlammps"):
        line = file.readline()
        tf = is_it_true(line)
        if tf:
            towhee.set_loutlammps_true()
        else:
            towhee.set_loutlammps_false()
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "loutlammps")
            return None

    if towhee.get_ensemble() == "uvt":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "louthist"):
            line = file.readline()
            tf = is_it_true(line)
            if tf:
                towhee.set_louthist_true()
            else:
                towhee.set_louthist_false()
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "louthist")
                return None

        if towhee.get_louthist():
            location = file.tell()
            line = file.readline()
            if verify_line(line, "histcalcfreq"):
                line = file.readline()
                towhee.set_histcalcfreq(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "histcalcfreq")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "histdumpfreq"):
                line = file.readline()
                towhee.set_histdumpfreq(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "histdumpfreq")
                    return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pressurefreq"):
        line = file.readline()
        towhee.set_pressurefreq(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pressurefreq")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "trmaxdispfreq"):
        line = file.readline()
        towhee.set_trmaxdispfreq(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "trmaxdispfreq")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "volmaxdispfreq"):
        line = file.readline()
        towhee.set_volmaxdispfreq(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "volmaxdispfreq")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "chempotperstep"):
        line = file.readline()
        chempotperstep = map(int, line.split())
        towhee.set_chempotperstep(chempotperstep)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(self.get_nmolty()):
                towhee.append_chempotperstep(0)
        else:
            error_message(line, "chempotperstep")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "potentialstyle"):
        templine = file.readline()
        line = filter_line(templine)
        towhee.set_potentialstyle(line)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "potentialstyle")
            return None

    if towhee.get_potentialstyle() == "classical" or\
    towhee.get_potentialstyle() == "quantum//classical":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "ffnumber"):
            line = file.readline()
            towhee.set_ffnumber(int(line.strip()))
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "ffnumber")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "ff_filename"):
            for i in range(towhee.get_ffnumber()):
                line = file.readline()
                towhee.append_ff_filename(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_ffnumber()):
                    towhee.append_ff_filename("")
            else:
                error_message(line, "ff_filename")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "classical_potential"):
            templine = file.readline()
            line = filter_line(templine)
            towhee.set_classical_potential(line)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "classical_potential")
                return None

        read_mixrule = False
        read_lshift = False
        read_ltailc = False
        read_rmin = False
        read_rcut = False
        read_rcutin = False
        read_interpolatestyle = False
        read_rpd = False
        
        if towhee.get_classical_potential() == "Lennard-Jones" or\
        towhee.get_classical_potential() == "9-6" or\
        towhee.get_classical_potential() == "12-6 plus solvation" or\
        towhee.get_classical_potential() == "12-6 plus 12-10 H-bond" or\
        towhee.get_classical_potential() == "12-9-6" or\
        towhee.get_classical_potential() == "Exponential-12-6" or\
        towhee.get_classical_potential() == "Gordon n-6":
            read_mixrule = True
            read_lshift = True
            read_ltailc = True
            read_rmin = True
            read_rcut = True
            read_rcutin = True
        elif towhee.get_classical_potential() == "Exponential-6":
            read_mixrule = True
            read_lshift = True
            read_ltailc = True
            read_rcut = True
            read_rcutin = True
        elif towhee.get_classical_potential() == "Hard Sphere" or\
        towhee.get_classical_potential() == "Square Well":
            read_mixrule = True
            read_rpd = True
        elif towhee.get_classical_potential() == "Repulsive Sphere" or\
        towhee.get_classical_potential() == "Repulsive Well" or\
        towhee.get_classical_potential() == "Multiwell" or\
        towhee.get_classical_potential() == "Repulsive Multiwell":
            read_mixrule = True
        elif towhee.get_classical_potential() == "Stillinger-Weber":
            read_mixrule = True
        elif towhee.get_classical_potential() == "Embedded Atom Method":
            read_interpolatestyle = True
            read_rcut = True
        elif towhee.get_classical_potential() == "Tabulated Pair":
            read_interpolatestyle = True
        else:
            print "Invalid classical_potential!"
            return None

        if read_mixrule:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "classical_mixrule"):
                templine = file.readline()
                line = filter_line(templine)
                towhee.set_classical_mixrule(line)
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "classical_mixrule")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "cmix_rescaling_style"):
                templine = file.readline()
                line = filter_line(templine)
                towhee.set_cmix_rescaling_style(line)
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "cmix_rescaling_style")
                    return None

            if towhee.get_cmix_rescaling_style() == "grossfield 2003":
                location = file.tell()
                line = file.readline()
                if verify_line(line, "cmix_lambda"):
                    templine = file.readline()
                    line = filter_line(templine)
                    towhee.set_cmix_lambda(line)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "cmix_lambda")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "cmix_npair"):
                    line = file.readline()
                    towhee.set_cmix_npair(int(line))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "cmix_npair")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "cmix_pair_list"):
                    for i in range(towhee.get_cmix_npair()):
                        templine = file.readline()
                        line = filter_line(templine)
                        towhee.append_cmix_pair_list(line)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                        towhee.append_cmix_pair_list(line)
                    else:
                        error_message(line, "cmix_pair_list")
                        return None

            elif towhee.get_cmix_rescaling_style() == "none":
                towhee.set_cmix_lambda("0.0d0")
                towhee.set_cmix_npair(1)
                towhee.append_cmix_pair_list("")
            else:
                print "This is not a valid value", towhee.get_cmix_rescaling_style()

        if read_interpolatestyle:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "interpolatestyle"):
                line = file.readline()
                towhee.set_interpolatestyle(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "interpolatestyle")
                    return None

        if read_lshift:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "lshift"):
                line = file.readline()
                tf = is_it_true(line)
                if tf:
                    towhee.set_lshift_true()
                else:
                    towhee.set_lshift_false()
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "lshift")
                    return None

        if read_ltailc:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "ltailc"):
                line = file.readline()
                tf = is_it_true(line)
                if tf:
                    towhee.set_ltailc_true()
                else:
                    towhee.set_ltailc_false()
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "ltailc")
                    return None

        if read_rmin:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "rmin"):
                line = file.readline()
                towhee.set_rmin(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "rmin")
                    return None

        if read_rcut:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "rcut"):
                line = file.readline()
                towhee.set_rcut(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "rcut")
                    return None

        if read_rcutin:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "rcutin"):
                line = file.readline()
                towhee.set_rcutin(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "rcutin")
                    return None

        if read_rpd:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "radial_pressure_delta"):
                line = file.readline()
                towhee.set_radial_pressure_delta(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "radial_pressure_delta")
                    return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "coulombstyle"):
            templine = file.readline()
            line = filter_line(templine)
            towhee.set_coulombstyle(line)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "coulombstyle")
                return None

        if towhee.get_coulombstyle() == "ewald_fixed_kmax":
            location = file.tell()
            line = file.readline()
            if verify_line(line, "kalp"):
                line = file.readline()
                towhee.set_kalp(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "kalp")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "kmax"):
                line = file.readline()
                towhee.set_kmax(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "kmax")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "dielect"):
                line = file.readline()
                towhee.set_dielect(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "dielect")
                    return None
        elif towhee.get_coulombstyle() == "ewald_fixed_cutoff":
            location = file.tell()
            line = file.readline()
            if verify_line(line, "ewald_prec"):
                line = file.readline()
                towhee.set_ewald_prec(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "ewald_prec")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "rcelect"):
                line = file.readline()
                towhee.set_rcelect(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "rcelect")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "dielect"):
                line = file.readline()
                towhee.set_dielect(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "dielect")
                    return None
        elif towhee.get_coulombstyle() == "minimum image":
            location = file.tell()
            line = file.readline()
            if verify_line(line, "dielect"):
                line = file.readline()
                towhee.set_dielect(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "dielect")
                    return None

        elif towhee.get_coulombstyle() != "none":
            print "Invalid coulombstyle: ", towhee.get_coulombstyle()
            return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "nfield"):
            line = file.readline()
            towhee.set_nfield(int(line.strip()))
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                towhee.set_nfield(0)
            else:
                error_message(line, "nfield")
                return None

        for i in range(towhee.get_nfield()):
            location = file.tell()
            line = file.readline()
            if verify_line(line, "fieldtype"):
                templine = file.readline()
                line = filter_line(templine)
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                    line = "Hard Wall"
                else:
                    error_message(line, "fieldtype")
                    return None

            if line == "Hard Wall":
                hardwall = HardWall()

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hrdbox"):
                    line = file.readline()
                    hardwall.set_box(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hrdbox")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hrdxyz"):
                    line = file.readline()
                    hardwall.set_xyz(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hrdxyz")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hrdcen"):
                    line = file.readline()
                    hardwall.set_cen(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hrdcen")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hrdrad"):
                    line = file.readline()
                    hardwall.set_rad(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hrdrad")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hrd_energy_type"):
                    templine = file.readline()
                    line = filter_line(templine)
                    hardwall.set_energy_type(line)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hrd_energy_type")
                        return None

                if hardwall.get_energy_type() == "finite":
                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "hrd_wall_energy"):
                        line = file.readline()
                        hardwall.set_wall_energy(line.strip())
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                        else:
                            error_message(line, "hrd_wall_energy")
                            return None

                towhee.append_externalfields(hardwall)
            elif line == "LJ 9-3 Wall":
                ljwall = LJWall()

                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfbox"):
                    line = file.readline()
                    ljwall.set_box(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfbox")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfxyz"):
                    line = file.readline()
                    ljwall.set_xyz(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfxyz")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfcen"):
                    line = file.readline()
                    ljwall.set_cen(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfcen")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfdir"):
                    line = file.readline()
                    ljwall.set_dir(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfbox")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfcut"):
                    line = file.readline()
                    ljwall.set_cut(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfcut")
                        return None
                
                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfshift"):
                    line = file.readline()
                    tf = is_it_true(line)
                    if tf:
                        ljwall.set_shift_true()
                    else:
                        ljwall.set_shift_false()
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfshift")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfrho"):
                    line = file.readline()
                    ljwall.set_rho(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfrho")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "ljfntypes"):
                    line = file.readline()
                    ljwall.set_ntypes(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "ljfntypes")
                        return None

                for j in range(ljwall.get_ntypes()):
                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "ljfname"):
                        line = file.readline()
                        ljwall.append_name(line.strip())
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                            ljwall.append_name("")
                        else:
                            error_message(line, "ljfname")
                            return None

                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "ljfsig"):
                        line = file.readline()
                        ljwall.append_sig(line.strip())
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                            ljwall.append_sig("")
                        else:
                            error_message(line, "ljfsig")
                            return None

                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "ljfeps"):
                        line = file.readline()
                        ljwall.append_eps(line.strip())
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                            ljwall.append_eps("")
                        else:
                            error_message(line, "ljfeps")
                            return None
                towhee.append_externalfields(ljwall)
            elif line == "Hooper Umbrella":
                umb = HooperUmbrella()

                location = file.tell()
                line = file.readline()
                if verify_line(line, "umbbox"):
                    line = file.readline()
                    umb.set_box(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "umbbox")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "umbxyz"):
                    line = file.readline()
                    umb.set_xyz(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "umbxyz")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "umbcenter"):
                    line = file.readline()
                    umb.set_center(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "umbcenter")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "umba"):
                    line = file.readline()
                    umb.set_a(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "umba")
                        return None
                towhee.append_externalfields(umb)
            elif line == "Steele Wall":
                steele = SteeleWall()

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele box"):
                    line = file.readline()
                    steele.set_box(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steelebox")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele xyz"):
                    line = file.readline()
                    steele.set_xyz(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steelexyz")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele surface"):
                    line = file.readline()
                    steele.set_surface(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steelesurface")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele dir"):
                    line = file.readline()
                    steele.set_dir(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steeledir")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele cutoff"):
                    line = file.readline()
                    steele.set_cutoff(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steelecutoff")
                        return None
                
                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele shift"):
                    line = file.readline()
                    tf = is_it_true(line)
                    if tf:
                        steele.set_shift_true()
                    else:
                        steele.set_shift_false()
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steeleshift")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele delta"):
                    line = file.readline()
                    steele.set_delta(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steeledelta")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele rho_s"):
                    line = file.readline()
                    steele.set_rho_s(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steelerho_s")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "steele ntype"):
                    line = file.readline()
                    steele.set_ntype(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "steele ntype")
                        return None

                for j in range(steele.get_ntype()):
                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "steele name"):
                        line = file.readline()
                        steele.append_name(line.strip())
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                            steele.append_name("")
                        else:
                            error_message(line, "steele name")
                            return None

                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "sigma_sf"):
                        line = file.readline()
                        steele.append_sigma_sf(line.strip())
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                            steele.append_sigma_sf("")
                        else:
                            error_message(line, "sigma_sf")
                            return None

                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "epsilon_sf"):
                        line = file.readline()
                        steele.append_epsilon_sf(line.strip())
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                            steele.append_epsilon_sf("")
                        else:
                            error_message(line, "epsilon_sf")
                            return None
                towhee.append_externalfields(steele)
            elif line == "Harmonic Attractor":
                ha = HarmonicAttractor()

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hafbox"):
                    line = file.readline()
                    ha.set_box(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hafbox")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hafk"):
                    line = file.readline()
                    ha.set_k(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hafk")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hafnentries"):
                    line = file.readline()
                    ha.set_nentries(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hafnentries")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hafrefpos"):
                    templine = file.readline()
                    line = filter_line(templine)
                    ha.set_refpos(line)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hafrefpos")
                        return None

                if ha.get_refpos() == "Global":
                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "hafglobxyz"):
                        line = file.readline()
                        globxyz = line.split()
                        ha.set_globx(globxyz[0])
                        ha.set_globy(globxyz[1])
                        ha.set_globz(globxyz[2])
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                        else:
                            error_message(line, "hafglobxyz")
                            return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "hafkey"):
                    templine = file.readline()
                    line = filter_line(templine)
                    ha.set_key(line)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "hafkey")
                        return None

                for i in range(ha.get_nentries()):
                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "hafmolec"):
                        line = file.readline()
                        ha.append_molec(int(line.strip()))
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                        else:
                            error_message(line, "hafmolec")
                            return None

                    print ha.get_key()
                    if ha.get_key() == "Element":
                        location = file.tell()
                        line = file.readline()
                        if verify_line(line, "hafelement"):
                            line = file.readline()
                            ha.append_element(line.strip())
                            ha.append_name("")
                        else:
                            if check_all_strings(line, good_strings):
                                file.seek(location)
                            else:
                                error_message(line, "hafelement")
                                return None
                    elif ha.get_key() == "FFtype":
                        location = file.tell()
                        line = file.readline()
                        if verify_line(line, "hafname"):
                            line = file.readline()
                            ha.append_name(line.strip())
                            ha.append_element("")
                        else:
                            if check_all_strings(line, good_strings):
                                file.seek(location)
                            else:
                                error_message(line, "hafname")
                                return None
                    else:
                        print "Weirded out! hafkey = ", ha.get_key()
                # End of for i in range(ha.get_nentries())
                towhee.append_externalfields(ha)
            else:
                print "Unrecognized external field:", line
                return None
        # End of loop over nfields                    

        location = file.tell()
        line = file.readline()
        if verify_line(line, "isolvtype"):
            line = file.readline()
            towhee.set_isolvtype(int(line.strip()))
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "isolvtype")
                return None
    # End if potentialstyle == classical or classical//quantum

    if towhee.get_potentialstyle() == "quantum" or\
    towhee.get_potentialstyle() == "quantum//classical":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "quantum code"):
            templine = file.readline()
            line = filter_line(templine)
            towhee.set_quantumcode(line)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "quantum code")
                return None
        
        if towhee.get_quantumcode() == "Seqquest":
            location = file.tell()
            line = file.readline()
            if verify_line(line, "functional"):
                line = file.readline()
                towhee.set_functional(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "functional")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "atom types"):
                line = file.readline()
                towhee.set_atomtypes(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "atom types")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "atom filenames"):
                for i in range(towhee.get_atomtypes()):
                    line = file.readline()
                    towhee.append_atom_filenames(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                    towhee.append_atom_filenames("")
                else:
                    error_message(line, "atom filenames")
                    return None
                
            location = file.tell()
            line = file.readline()
            if verify_line(line, "grid multiplier"):
                line = file.readline()
                towhee.set_grid_multiplier(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "grid multiplier")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "kgrid product"):
                line = file.readline()
                towhee.set_kgrid_product(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "kgrid product")
                    return None
        # end of if quantumcode == 'Seqquest'
    # end of if potientialstyle == quantum or quantum//classical
    
    location = file.tell()
    line = file.readline()
    if verify_line(line, "linit"):
        line = file.readline()
        tf = is_it_true(line)
        if tf:
            towhee.set_linit_true()
        else:
            towhee.set_linit_false()
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "linit")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "initboxtype"):
        templine = file.readline()
        line = filter_line(templine)
        towhee.set_initboxtype(line)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "initboxtype")
            return None

    get_initstyle = False
    if towhee.get_initboxtype() == "dimensions":
        get_initstyle = True
    elif towhee.get_initboxtype() == "number density":
        get_initstyle = True
    elif towhee.get_initboxtype() == "unit cell":
        get_initstyle = False
        for i in range(towhee.get_numboxes()):
            style = []
            lattice = []
            mol = []
            for j in range(towhee.get_nmolty()):
                style.append("unit cell")
                lattice.append("none")
                mol.append("")
            towhee.append_initstyle(style)
            towhee.append_initlattice(lattice)
            towhee.append_initmol(mol)

    if get_initstyle:
        location = file.tell()
        line = file.readline()
        if verify_line(line, "initstyle"):
            for i in range(towhee.get_numboxes()):
                line = file.readline()
                tempinitstyle = line.split()
                initstyle = fix_initstyle(tempinitstyle)
                if len(initstyle) != towhee.get_nmolty():
                    print "Error with initstyle\nnmolty = " + str(towhee.get_nmolty())
                    print "Len of initstyle array = " + str(len(initstyle))
                    return None

                for i in range(len(initstyle)):
                    initstyle[i] = filter_line(initstyle[i])
                towhee.append_initstyle(initstyle)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_numboxes()):
                    t = []
                    for j in range(towhee.get_nmolty()):
                        t.append(0)
                    towhee.append_initstyle(t)
            else:
                error_message(line, "initstyle")
                return None

        for i in range(towhee.get_nmolty()):
            helix_exists = False
            for j in range(towhee.get_numboxes()):
                if towhee.get_single_initstyle(j, i) == "helix":
                    helix_exists = True

            if helix_exists == True:
                helix = Helix()
                helix.set_nmolty(i)

                location = file.tell()
                line = file.readline()
                if verify_line(line, "helix_moltyp"):
                    line = file.readline()
                    helix.set_moltyp(int(line.strip()))
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "helix_moltyp")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "helix_radius"):
                    line = file.readline()
                    helix.set_radius(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "helix_radius")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "helix_angle"):
                    line = file.readline()
                    helix.set_angle(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "angle")
                        return None
                #
                # From 3.16 to 3.17, helix_element changed to helix_keyname and related helix_keytype
                #
                location = file.tell()
                line = file.readline()
                if verify_line(line, "helix_keytype"):
                    templine = file.readline()
                    line = filter_line(templine)
                    helix.set_keytype(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "helix_keytype")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "helix_keyname"):
                    line = file.readline()
                    helix.set_keyname(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                        helix.set_keyname("")
                    else:
                        error_message(line, "helix_keyname")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "helix_conlen"):
                    line = file.readline()
                    helix.set_conlen(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "helix_conlen")
                        return None

                location = file.tell()
                line = file.readline()
                if verify_line(line, "helix_phase"):
                    line = file.readline()
                    helix.set_phase(line.strip())
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "helix_conlen")
                        return None
                towhee.append_helix(helix)
            # end of for j in range(towhee.get_numboxes())
        # end of for i in range(towhee.get_nmolty())

        location = file.tell()
        line = file.readline()
        if verify_line(line, "initlattice"):
            for i in range(towhee.get_numboxes()):
                line = file.readline()
                tempinitlattice = line.split()
                initlattice = fix_initlattice(tempinitlattice)
                if len(initlattice) != towhee.get_nmolty():
                    print "Error with initlattice"
                    return None

                for i in range(len(initlattice)):
                    initlattice[i] = filter_line(initlattice[i])
                towhee.append_initlattice(initlattice)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_numboxes()):
                    t = []
                    for j in range(towhee.get_nmolty()):
                        t.append(0)
                    towhee.append_initlattice(t)
            else:
                error_message(line, "initlattice")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "initmol"):
            for i in range(towhee.get_numboxes()):
                line = file.readline()
                initmol = map(int,line.split())
                if len(initmol) != towhee.get_nmolty():
                    print "Error with initmol"
                    return None
                    
                towhee.append_initmol(initmol)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_numboxes()):
                    t = []
                    for j in range(towhee.get_nmolty()):
                        t.append(0)
                    towhee.append_initmol(t)
            else:
                error_message(line, "initmol")
                return None
    # end if get_initstyle

    location = file.tell()
    line = file.readline()
    if verify_line(line, "inix"):
        for i in range(towhee.get_numboxes()):
            line = file.readline()
            xyz = map(int,line.split())
            towhee.append_inix(xyz[0])
            towhee.append_iniy(xyz[1])
            towhee.append_iniz(xyz[2])
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_numboxes()):
                towhee.append_inix(0)
                towhee.append_iniy(0)
                towhee.append_iniz(0)
        else:
            error_message(line, "inixyz")
            return None

    if towhee.get_initboxtype() == "dimensions":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "hmatrix"):
            for i in range(towhee.get_numboxes()):
                hmatrix = Hmatrix()        
                line = file.readline()
                h = line.split()
                hmatrix.set_row1(h)
                line = file.readline()
                h = line.split()
                hmatrix.set_row2(h)
                line = file.readline()
                h = line.split()
                hmatrix.set_row3(h)
                towhee.append_hmatrix(hmatrix)
                towhee.append_box_number_density("")
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                hmatrix = Hmatrix()
                towhee.append_hmatrix(Hmatrix())
            else:
                error_message(line, "hmatrix")
                return None
    elif towhee.get_initboxtype() == "number density":
        location = file.tell()
        line = file.readline()
        if verify_line(line, "box_number_density"):
            for i in range(towhee.get_numboxes()):
                line = file.readline()
                towhee.append_box_number_density(line.strip())
                towhee.append_hmatrix(Hmatrix())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "box_number_density")
                return None
    elif towhee.get_initboxtype() == "unit cell":
        for i in range(towhee.get_numboxes()):
            towhee.append_hmatrix(Hmatrix())
            towhee.append_box_number_density("")
    else:
        print "Invalid initboxtype:", towhee.get_initboxtype()
        return None
    #
    # Monte Carlo Moves
    #
    if towhee.get_ensemble() == "npt":
        nbp = towhee.get_numboxes()
    elif towhee.get_ensemble() == "nvt":
        nbp = towhee.get_numboxes()*(towhee.get_numboxes()-1)/2

    if (towhee.get_ensemble() == "nvt" and towhee.get_numboxes() > 1) or\
    towhee.get_ensemble() == "npt":
        #
        # Isotropic Volume Move
        #
        mcm = towhee.get_ivm()
        mcm.set_ensemble(towhee.get_ensemble())
        mcm.set_numboxes(towhee.get_numboxes())

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pmvol"):
            line = file.readline()
            mcm.set_move_probability(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "pmvol")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pmvlpr"):
            line = file.readline()
            pmvlpr = line.split()
            mcm.set_pmvlpr(pmvlpr)
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(nbp):
                    mcm.append_pmvlpr("1.0d0")
            else:
                error_message(line, "pmvlpr")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "rmvol"):
            line = file.readline()
            mcm.set_rmvol(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "rmvol")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "tavol"):
            line = file.readline()
            mcm.set_tavol(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "tavol")
                return None
        towhee.set_ivm(mcm)
        #
        # Anisotropic Volume Move
        #
        mcm = towhee.get_avm()
        mcm.set_ensemble(towhee.get_ensemble())
        mcm.set_numboxes(towhee.get_numboxes())

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pmcell"):
            line = file.readline()
            mcm.set_move_probability(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "pmcell")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pmcellpr"):
            line = file.readline()
            mcm.set_pmcellpr(line.split())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(nbp):
                    mcm.append_pmcellpr("1.0d0")
            else:
                error_message(line, "pmcellpr")
                return None

        if towhee.get_ensemble() == "npt":
            location = file.tell()
            line = file.readline()
            if verify_line(line, "pmcellpt"):
                line = file.readline()
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "pmcellpt")
                    return None
        else:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "pmcellpt"):
                for i in range(nbp):
                    line = file.readline()
                    mcm.append_pmcellpt(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                    for i in range(nbp):
                        mcm.append_pmcellpt("1.0d0")
                else:
                    error_message(line, "pmcellpt")
                    return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "rmcell"):
            line = file.readline()
            mcm.set_rmcell(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "rmcell")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "tacell"):
            line = file.readline()
            mcm.set_tacell(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "tacell")
                return None
        towhee.set_avm(mcm)

    if towhee.get_numboxes() > 1:
        #
        # Rotational-bias 2 box molecule Transfer Move
        #
        mcm = towhee.get_rb2bmtm()
        mcm.set_numboxes(towhee.get_numboxes())
        mcm.set_nmolty(towhee.get_nmolty())

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pm2boxrbswap"):
            line = file.readline()
            mcm.set_move_probability(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "pm2boxrbswap")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pm2rbswmt"):
            line = file.readline()
            mcm.set_pm2rbswmt(line.split())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_nmolty()):
                    mcm.append_pm2rbswmt("1.0d0")
            else:
                error_message(line, "pm2rbswmt")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pm2rbswpr"):
            line = file.readline()
            mcm.set_pm2rbswpr(line.split())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(nbp):
                    mcm.append_pm2rbswpr("1.0d0")
            else:
                error_message(line, "pm2rbswpr")
                return None
        towhee.set_rb2bmtm(mcm)
        #
        # Configurational-bias 2 box molecule Transfer Move
        #
        mcm = towhee.get_cb2bmtm()
        mcm.set_numboxes(towhee.get_numboxes())
        mcm.set_nmolty(towhee.get_nmolty())
        
        location = file.tell()
        line = file.readline()
        if verify_line(line, "pm2boxcbswap"):
            line = file.readline()
            mcm.set_move_probability(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "pm2boxcbswap")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pm2cbswmt"):
            line = file.readline()
            mcm.set_pm2cbswmt(line.split())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_nmolty()):
                    mcm.append_pm2cbswmt("1.0d0")
            else:
                error_message(line, "pm2cbswmt")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pm2cbswpr"):
            line = file.readline()
            mcm.set_pm2cbswpr(line.split())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(nbp):
                    mcm.append_pm2cbswpr("1.0d0")
            else:
                error_message(line, "pm2cbswpr")
                return None
        towhee.set_cb2bmtm(mcm)

    if towhee.get_ensemble() == "uvt":
        #
        # Configurational-bias grand-canonical insertion/deletion Move
        #
        mcm = towhee.get_cbgcidm()
        mcm.set_nmolty(towhee.get_nmolty())

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pmuvtcbswap"):
            line = file.readline()
            mcm.set_move_probability(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "pmuvtcbswap")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "pmuvtcbmt"):
            line = file.readline()
            mcm.set_pmuvtcbmt(line.split())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                for i in range(towhee.get_nmolty()):
                    mcm.append_pmuvtcbmt("1.0d0")
            else:
                error_message(line, "pmuvtcbmt")
                return None
        towhee.set_cbgcidm(mcm)
    #
    # Configurational-bias single box molecule Reinsertion Move
    #
    mcm = towhee.get_cbsbmrm()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pm1boxcbswap"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pm1boxcbswap")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pm1cbswmt"):
        line = file.readline()
        mcm.set_pm1cbswmt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pm1cbswmt("1.0d0")
        else:
            error_message(line, "pm1cbswmt")
            return None
    towhee.set_cbsbmrm(mcm)
    #
    # Aggregation Volume Bias Move Type 1
    #
    mcm = towhee.get_avbmt1()
    mcm.set_nmolty(towhee.get_nmolty())
 
    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb1"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmabv1")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb1in"):
        line = file.readline()
        mcm.set_pmavb1in(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmabv1in")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb1mt"):
        line = file.readline()
        mcm.set_pmavb1mt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmavb1mt("1.0d0")
        else:
            error_message(line, "pmabv1mt")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb1ct"):
        for i in range(towhee.get_nmolty()):
            line = file.readline()
            mcm.append_pmavb1ct(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                t = []
                for i in range(towhee.get_nmolty()):
                    t.append("1.0d0")
                mcm.append_pmavb1ct(t)
        else:
            error_message(line, "pmabv1ct")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "avb1rad"):
        line = file.readline()
        mcm.set_avb1rad(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "abv1rad")
            return None
    towhee.set_avbmt1(mcm)
    #
    # Aggregation Volume Bias Move Type 2
    #
    mcm = towhee.get_avbmt2()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb2"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmabv2")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb2in"):
        line = file.readline()
        mcm.set_pmavb2in(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmabv2in")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb2mt"):
        line = file.readline()
        mcm.set_pmavb2mt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmavb2mt("1.0d0")
        else:
            error_message(line, "pmabv2mt")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb2ct"):
        for i in range(towhee.get_nmolty()):
            line = file.readline()
            mcm.append_pmavb2ct(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                t = []
                for j in range(towhee.get_nmolty()):
                    t.append("1.0d0")
                mcm.append_pmavb2ct(t)
        else:
            error_message(line, "pmabv2ct")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "avb2rad"):
        line = file.readline()
        mcm.set_avb2rad(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "abv2rad")
            return None
    towhee.set_avbmt2(mcm)
    #
    # Aggregation Volume Bias Move Type 3
    #
    mcm = towhee.get_avbmt3()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb3"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmabv3")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb3mt"):
        line = file.readline()
        mcm.set_pmavb3mt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmavb3mt("1.0d0")
        else:
            error_message(line, "pmabv3mt")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmavb3ct"):
        for i in range(towhee.get_nmolty()):
            line = file.readline()
            mcm.append_pmavb3ct(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                t = []
                for i in range(towhee.get_nmolty()):
                    t.append("1.0d0")
                mcm.append_pmavb3ct(t)
        else:
            error_message(line, "pmabv3ct")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "avb3rad"):
        line = file.readline()
        mcm.set_avb3rad(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "abv3rad")
            return None
    towhee.set_avbmt3(mcm)
    #
    # Configurational-Bias Partial Molecule Regrowth
    #
    mcm = towhee.get_cbpmr()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmcb"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmcb")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmcbmt"):
        line = file.readline()
        mcm.set_pmcbmt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmcbmt("1.0d0")
        else:
            error_message(line, "pmcbmt")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmall"):
        line = file.readline()
        mcm.set_pmall(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmall("1.0d0")
        else:
            error_message(line, "pmall")
            return None
    towhee.set_cbpmr(mcm)
    #
    # Configurational-Bias Protein backbone Regrowth
    #
    mcm = towhee.get_cbpbr()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmback"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmback")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmbkmt"):
        line = file.readline()
        mcm.set_pmbkmt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmbkmt("1.0d0")
        else:
            error_message(line, "pmbkmt")
            return None
    towhee.set_cbpbr(mcm)
    #
    # Torsional Pivot Move
    #
    mcm = towhee.get_tpm()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmpivot"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmpivot")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmpivmt"):
        line = file.readline()
        mcm.set_pmpivmt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmpivmt("1.0d0")
        else:
            error_message(line, "pmpivmt")
            return None
    towhee.set_tpm(mcm)
    #
    # Concerted Rotation Move on a non-peptide backbone
    #
    mcm = towhee.get_crnmoanpb()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmconrot"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmconrot")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmcrmt"):
        line = file.readline()
        mcm.set_pmcrmt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmcrmt("1.0d0")
        else:
            error_message(line, "pmcrmt")
            return None
    towhee.set_crnmoanpb(mcm)
    #
    # Concerted Rotation Move over a 3 peptides backbone sequence
    #
    mcm = towhee.get_crnmoa3pbs()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmcrback"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmcrback")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmcrbmt"):
        line = file.readline()
        mcm.set_pmcrbmt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmcrbmt("1.0d0")
        else:
            error_message(line, "pmcrbmt")
            return None
    towhee.set_crnmoa3pbs(mcm)
    #
    # Plane Shift Move
    #
    mcm = towhee.get_psm()
    mcm.set_numboxes(towhee.get_numboxes())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmplane"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmplane")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmplanebox"):
        line = file.readline()
        mcm.set_pmplanebox(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_numboxes()):
                mcm.append_pmplanebox("1.0d0")
        else:
            error_message(line, "pmplanebox")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "planewidth"):
        line = file.readline()
        mcm.set_planewidth(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "planewidth")
            return None
    towhee.set_psm(mcm)
    #
    # Row Shift Move
    #
    mcm = towhee.get_rsm()
    mcm.set_numboxes(towhee.get_numboxes())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmrow"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmrow")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmrowbox"):
        line = file.readline()
        mcm.set_pmrowbox(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_numboxes()):
                mcm.append_pmrowbox("1.0d0")
        else:
            error_message(line, "pmrowbox")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "rowwidth"):
        line = file.readline()
        mcm.set_rowwidth(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "rowwidth")
            return None
    towhee.set_rsm(mcm)
    #
    # Intramolecular Single Atom Translation Move
    #
    mcm = towhee.get_isatm()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmtraat"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmtraat")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmtamt"):
        line = file.readline()
        mcm.set_pmtamt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmtamt("1.0d0")
        else:
            error_message(line, "pmtamt")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "rmtraa"):
        line = file.readline()
        mcm.set_rmtraa(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "rmtraa")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "tatraa"):
        line = file.readline()
        mcm.set_tatraa(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "tatraa")
            return None
    towhee.set_isatm(mcm)
    #
    # Center-of-Mass Molecule Translation Move
    #
    mcm = towhee.get_cofmmtm()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmtracm"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmtracm")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmtcmt"):
        line = file.readline()
        mcm.set_pmtcmt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmtcmt("1.0d0")
        else:
            error_message(line, "pmtcmt")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "rmtrac"):
        line = file.readline()
        mcm.set_rmtrac(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "rmtrac")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "tatrac"):
        line = file.readline()
        mcm.set_tatrac(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "tatrac")
            return None
    towhee.set_cofmmtm(mcm)
    #
    # Rotation about the Center-of-Mass Move
    #
    mcm = towhee.get_ratcomm()
    mcm.set_nmolty(towhee.get_nmolty())

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmrotate"):
        line = file.readline()
        mcm.set_move_probability(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "pmrotate")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "pmromt"):
        line = file.readline()
        mcm.set_pmromt(line.split())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                mcm.append_pmromt("1.0d0")
        else:
            error_message(line, "pmromt")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "rmrot"):
        line = file.readline()
        mcm.set_rmrot(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "rmrot")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "tarot"):
        line = file.readline()
        mcm.set_tarot(line.strip())
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "tarot")
            return None
    #
    # End of Monte Carlo Moves
    #
    location = file.tell()
    line = file.readline()
    if verify_line(line, "tor_cbstyle"):
        line = file.readline()
        towhee.set_tor_cbstyle(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "tor_cbstyle")
            return None

    if towhee.get_tor_cbstyle() == 1:
        location = file.tell()
        line = file.readline()
        if verify_line(line, "sdevtor"):
            line = file.readline()
            towhee.set_sdevtor(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "sdevtor")
                return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "bend_cbstyle"):
        line = file.readline()
        towhee.set_bend_cbstyle(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "bend_cbstyle")
            return None

    if towhee.get_bend_cbstyle() == 1:
        location = file.tell()
        line = file.readline()
        if verify_line(line, "sdevbena"):
            line = file.readline()
            towhee.set_sdevbena(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "sdevbena")
                return None

        location = file.tell()
        line = file.readline()
        if verify_line(line, "sdevbenb"):
            line = file.readline()
            towhee.set_sdevbenb(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "sdevbenb")
                return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "vib_cbstyle"):
        line = file.readline()
        towhee.set_vib_cbstyle(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "vib_cbstyle")
            return None

    if towhee.get_vib_cbstyle() == 0:
        location = file.tell()
        line = file.readline()
        if verify_line(line, "vibrang"):
            line = file.readline()
            towhee.set_vibrang(line.split())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "vibrang")
                return None
    elif towhee.get_vib_cbstyle() == 1:
        location = file.tell()
        line = file.readline()
        if verify_line(line, "sdevvib"):
            line = file.readline()
            towhee.set_sdevvib(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
            else:
                error_message(line, "sdevvib")
                return None
    else:
        print "Invalid input: vib_cbstyle = " + str(towhee.get_vib_cbstyle())
        return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "cdform"):
        line = file.readline()
        towhee.set_cdform(int(line.strip()))
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
        else:
            error_message(line, "cdform")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_nb_one"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_nb_one(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_nb_one(10)
        else:
            error_message(line, "nch_nb_one")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_nb"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_nb(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_nb(10)
        else:
            error_message(line, "nch_nb")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_tor_out"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_tor_out(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_tor_out(10)
        else:
            error_message(line, "nch_tor_out")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_tor_in"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_tor_in(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_tor_in(10)
        else:
            error_message(line, "nch_tor_in")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_tor_in_con"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_tor_in_con(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_tor_in_con(100)
        else:
            error_message(line, "nch_tor_in_con")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_bend_a"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_bend_a(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_bend_a(1000)
        else:
            error_message(line, "nch_bend_a")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_bend_b"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_bend_b(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_bend_b(1000)
        else:
            error_message(line, "nch_bend_b")
            return None

    location = file.tell()
    line = file.readline()
    if verify_line(line, "nch_vib"):
        line = file.readline()
        value = map(int, line.split())
        towhee.set_nch_vib(value)
    else:
        if check_all_strings(line, good_strings):
            file.seek(location)
            for i in range(towhee.get_nmolty()):
                towhee.append_nch_vib(1000)
        else:
            error_message(line, "nch_vib")
            return None
    #
    # Time to do the inputs
    #
    for i in range(towhee.get_nmolty()):
        location = file.tell()
        line = file.readline()
        if verify_line(line, "inpstyle"):
            line = file.readline()
            inpstyle = int(line.strip())
        else:
            if check_all_strings(line, good_strings):
                file.seek(location)
                inpstyle = 4
            else:
                error_message(line, "inpstyle")
                return None

        inp = towhee.create_input(inpstyle)

        if inpstyle != 4:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "nunit"):
                line = file.readline()
                inp.set_nunit(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "nunit")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "nmaxcbmc"):
                line = file.readline()
                inp.set_nmaxcbmc(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "nmaxcbmc")
                    return None

        if inpstyle == 0:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "lpdb"):
                line = file.readline()
                tf = is_it_true(line)
                if tf:
                    inp.set_lpdb_true()
                else:
                    inp.set_lpdb_false()
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "lpdb")
                    return None

            for j in range(inp.get_nunit()):
                location = file.tell()
                line = file.readline()
                if verify_line(line, "unit"):
                    line = file.readline()
                    unit,type,qqatom = line.split()
                    inp.append_unit(int(unit))
                    inp.append_type(int(type))
                    inp.append_qqatom(qqatom)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                        inp.append_unit(j+1)
                        inp.append_type(0)
                        inp.append_qqatom("0.0d0")
                    else:
                        error_message(line, "unit")
                        return None

                if inp.get_lpdb():
                    location = file.tell()
                    line = file.readline()
                    if verify_line(line, "pdbname"):
                        line = file.readline()
                        pdbname,aminonum,aminoshort = line.split()
                        inp.append_pdbname(pdbname)
                        inp.append_aminonum(int(aminonum))
                        inp.append_aminoshort(aminoshort)
                    else:
                        if check_all_strings(line, good_strings):
                            file.seek(location)
                            inp.append_pdbname("")
                            inp.append_aminonum(0)
                            inp.append_aminoshort("")
                        else:
                            error_message(line, "pdbname")
                            return None
                #
                # Read in bond vibrations
                #
                location = file.tell()
                line = file.readline()
                vibs = inp.create_vibrations()
                if verify_line(line, "vibration"):
                    line = file.readline()
                    num_vibs = int(line.strip())
                    vibs.set_number_vibrations(num_vibs)
                    for k in range(num_vibs):
                        line = file.readline()
                        vibrations = map(int, line.split())
                        vibs.append_vibrations(vibrations)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "vibration")
                        return None
                inp.append_vibrations(vibs)
                #
                # Read in bond bending
                #
                location = file.tell()
                line = file.readline()
                bends = inp.create_bendings()
                if verify_line(line, "bending"):
                    line = file.readline()
                    num_bends = int(line.strip())
                    bends.set_number_bendings(num_bends)
                    for k in range(num_bends):
                        line = file.readline()
                        bendings = map(int, line.split())
                        bends.append_bendings(bendings)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "bending")
                        return None
                inp.append_bendings(bends)
                #
                # Read in bond torsions
                #
                location = file.tell()
                line = file.readline()
                tors = inp.create_torsions()
                if verify_line(line, "torsion"):
                    line = file.readline()
                    num_tor = int(line.strip())
                    tors.set_number_torsions(num_tor)
                    for k in range(num_tor):
                        line = file.readline()
                        torsions = map(int, line.split())
                        tors.append_torsions(torsions)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "torsion")
                        return None
                inp.append_torsions(tors)
                #
                # Read in angle-angle
                #
                location = file.tell()
                line = file.readline()
                ang = inp.create_angles()
                if verify_line(line, "angle-angle"):
                    line = file.readline()
                    num_angles = int(line.strip())
                    ang.set_number_angles(num_angles)
                    for k in range(num_angles):
                        line = file.readline()
                        angles = map(int, line.split())
                        ang.append_angles(angles)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "angle-angle")
                        return None
                inp.append_angles(ang)
                #
                # Read in improper torsions
                #
                location = file.tell()
                line = file.readline()
                imp = inp.create_improper_torsions()
                if verify_line(line, "improper torsion"):
                    line = file.readline()
                    num_imps = int(line.strip())
                    imp.set_number_improper_torsions(num_imps)
                    for k in range(num_imps):
                        line = file.readline()
                        imp_tors = map(int, line.split())
                        imp.append_improper_torsions(imp_tors)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "improper_torsion")
                        return None
                inp.append_improper_torsions(imp)
            # end of for j in nunits
            towhee.append_input(inp)
        elif inpstyle == 1:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "forcefield"):
                line = file.readline()
                inp.set_forcefield(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "forcefield")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "protgeom"):
                templine = file.readline()
                line = filter_line(templine)
                inp.set_protgeom(line)
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "protgeom")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "pepname"):
                for j in range(inp.get_nunit()):
                    line = file.readline()
                    if inp.get_protgeom() == "cyclic":
                        p,s,b = line.split()
                        inp.append_pepname(p)
                        inp.append_stereochem(s)
                        inp.append_bondpartner(int(b))
                        inp.append_terminus("")
                    elif inp.get_protgeom() == "linear":
                        p,s,b,t = line.split()
                        inp.append_pepname(p)
                        inp.append_stereochem(s)
                        inp.append_bondpartner(int(b))
                        inp.append_terminus(t)
                    else:
                        print "Invalid pepname"
                        return None
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "pepname")
                    return None
            towhee.append_input(inp)
        elif inpstyle == 2:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "forcefield"):
                line = file.readline()
                inp.set_forcefield(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "forcefield")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "charge_assignment"):
                templine = file.readline()
                line = filter_line(templine)
                inp.set_charge_assignment(line)
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "charge_assignment")
                    return None

            for j in range(inp.get_nunit()):
                location = file.tell()
                line = file.readline()
                if verify_line(line, "unit"):
                    line = file.readline()
                    if inp.get_charge_assignment() == "manual":
                        u,n,q = line.split()
                        inp.append_unit(int(u))
                        inp.append_type(n)
                        inp.append_qqatom(q)
                    else:
                        u,n = line.split()
                        inp.append_unit(int(u))
                        inp.append_type(n)
                        inp.append_qqatom("")
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                        inp.append_unit(j+1)
                        inp.append_type("")
                        inp.append_qqatom("")
                    else:
                        error_message(line, "unit")
                        return None

                # Vibrations
                location = file.tell()
                line = file.readline()
                vib = inp.create_vibrations()
                if verify_line(line, "vibration"):
                    line = file.readline()
                    vib.set_number_vibrations(int(line.strip()))
                    if vib.get_number_vibrations() != 0:
                        line = file.readline()
                        vibrations = map(int, line.split())
                        vib.set_vibrations(vibrations)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "vibration")
                        return None
                inp.append_vibrations(vib)

                # Improper Torsions
                location = file.tell()
                line = file.readline()
                imp = inp.create_improper_torsions()
                if verify_line(line, "improper"):
                    line = file.readline()
                    num_imptor = int(line.strip())
                    imp.set_number_improper_torsions(num_imptor)
                    for k in range(num_imptor):
                        line = file.readline()
                        imptors = map(int, line.split())
                        imp.append_improper_torsions(imptors)
                else:
                    if check_all_strings(line, good_strings):
                        file.seek(location)
                    else:
                        error_message(line, "improper_torsion")
                        return None
                inp.append_improper_torsions(imp)
            towhee.append_input(inp)
        elif inpstyle == 3:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "terminus"):
                line = file.readline()
                inp.set_terminus(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "hterm")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "forcefield"):
                line = file.readline()
                inp.set_forcefield(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "forcefield")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "monomername"):
                for j in range(inp.get_nunit()):
                    line = file.readline()
                    inp.append_monomername(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                    for j in range(towhee.get_nunit()):
                        inp.append_monomername("")
                else:
                    error_message(line, "monomername")
                    return None
            towhee.append_input(inp)
        elif inpstyle == 4:
            location = file.tell()
            line = file.readline()
            if verify_line(line, "forcefield"):
                line = file.readline()
                inp.set_forcefield(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "forcefield")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "atomname"):
                line = file.readline()
                inp.set_atomname(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "atomname")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "qqatom"):
                line = file.readline()
                inp.set_qqatom(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "qqatom")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "nanotube_n"):
                line = file.readline()
                inp.set_n(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "nanotube_n")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "nanotube_m"):
                line = file.readline()
                inp.set_m(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "nanotube_m")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "nanotube_ncells"):
                line = file.readline()
                inp.set_ncells(int(line.strip()))
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "nanotube_ncells")
                    return None

            location = file.tell()
            line = file.readline()
            if verify_line(line, "nanotube_bondlength"):
                line = file.readline()
                inp.set_bondlength(line.strip())
            else:
                if check_all_strings(line, good_strings):
                    file.seek(location)
                else:
                    error_message(line, "nanotube_bondlength")
                    return None
            towhee.append_input(inp)
        else:
            print "Invalid input type"
    return towhee


def save_towhee_file(file, towhee):
    file.write('randomseed\n%d\n' % towhee.get_randomseed())
    file.write('inputformat\n\'%s\'\n' % towhee.get_iformat())
    file.write('ensemble\n\'%s\'\n' % towhee.get_ensemble())
    file.write('temperature\n%s\n' % towhee.get_temperature())

    if towhee.get_ensemble() == "npt":
        file.write('pressure\n%s\n' % towhee.get_pressure())

    file.write('nmolty\n%d\n' % towhee.get_nmolty())

    nmolectyp = towhee.get_nmolectyp()
    file.write('nmolectyp\n%d' % nmolectyp[0])
    for i in nmolectyp[1:]:
        file.write(' %d' % i)
    file.write('\n')

    if towhee.get_ensemble() == "uvt":
        chempot = towhee.get_chempot()
        file.write('chempot\n%s' % chempot[0])
        for stuff in chempot[1:]:
            file.write(' %s' % stuff)
        file.write('\n')

    file.write('numboxes\n%d\n' % towhee.get_numboxes())
    file.write('stepstyle\n\'%s\'\n' % towhee.get_stepstyle())

    if towhee.get_stepstyle() == "cycles" or\
    towhee.get_stepstyle() == "moves":
        file.write('nstep\n%d\n' % towhee.get_nstep())
    elif towhee.get_stepstyle() == "minimize":
        file.write('optstyle\n%d\n' % towhee.get_optstyle())
        file.write('mintol\n%s\n' % towhee.get_mintol())
    else:
        print "How did stepstyle = " + towhee.get_stepstyle() + " happen??"

    file.write('printfreq\n%d\n' % towhee.get_printfreq())
    file.write('blocksize\n%d\n' % towhee.get_blocksize())
    file.write('moviefreq\n%d\n' % towhee.get_moviefreq())
    file.write('backupfreq\n%d\n' % towhee.get_backupfreq())
    file.write('runoutput\n\'%s\'\n' % towhee.get_runoutput())
    file.write('pdb_output_freq\n%d\n' % towhee.get_pdb_output_freq())
    file.write('loutdft\n%s\n' % truth_string(towhee.get_loutdft()))
    file.write('loutlammps\n%s\n' % truth_string(towhee.get_loutlammps()))

    if towhee.get_ensemble() == "uvt":
        file.write('louthist\n%s\n' % truth_string(towhee.get_louthist()))

        if towhee.get_louthist():
            file.write('histcalcfreq\n%d\n' % towhee.get_histcalcfreq())
            file.write('histdumpfreq\n%d\n' % towhee.get_histdumpfreq())

    file.write('pressurefreq\n%d\n' % towhee.get_pressurefreq())
    file.write('trmaxdispfreq\n%d\n' % towhee.get_trmaxdispfreq())
    file.write('volmaxdispfreq\n%d\n' % towhee.get_volmaxdispfreq())

    chempotperstep = towhee.get_chempotperstep()
    file.write('chempotperstep\n%d' % chempotperstep[0])
    for stuff in chempotperstep[1:]:
        file.write(' %d' % stuff)
    file.write('\n')

    file.write('potentialstyle\n\'%s\'\n' % towhee.get_potentialstyle())

    if towhee.get_potentialstyle() == "classical" or\
    towhee.get_potentialstyle() == "quantum//classical":
        file.write('ffnumber\n%d\n' % towhee.get_ffnumber())

        file.write('ff_filename\n')
        for fn in towhee.get_ff_filename():
            file.write('%s\n' % fn)

        file.write('classical_potential\n\'%s\'\n' % towhee.get_classical_potential())
        write_mixrule = False
        write_lshift = False
        write_ltailc = False
        write_rmin = False
        write_rcut = False
        write_rcutin = False
        write_interpolatestyle = False
        write_rpd = False

        if towhee.get_classical_potential() == "Lennard-Jones" or\
        towhee.get_classical_potential() == "9-6" or\
        towhee.get_classical_potential() == "12-6 plus solvation" or\
        towhee.get_classical_potential() == "12-6 plus 12-10 H-bond" or\
        towhee.get_classical_potential() == "12-9-6" or\
        towhee.get_classical_potential() == "Exponential-12-6" or\
        towhee.get_classical_potential() == "Gordon n-6":
            write_mixrule = True
            write_lshift = True
            write_ltailc = True
            write_rmin = True
            write_rcut = True
            write_rcutin = True
        elif towhee.get_classical_potential() == "Exponential-6":
            write_mixrule = True
            write_lshift = True
            write_ltailc = True
            write_rcut = True
            write_rcutin = True
        elif towhee.get_classical_potential() == "Hard Sphere" or\
        towhee.get_classical_potential() == "Square Well":
            write_mixrule = True
            write_rpd = True
        elif towhee.get_classical_potential() == "Repulsive Sphere" or\
        towhee.get_classical_potential() == "Repulsive Well" or\
        towhee.get_classical_potential() == "Multiwell" or\
        towhee.get_classical_potential() == "Repulsive Multiwell":
            write_mixrule = True
        elif towhee.get_classical_potential() == "Stillinger-Weber":
            write_mixrule = True
        elif towhee.get_classical_potential() == "Embedded Atom Method":
            write_interpolatestyle = True
            write_rcut = True
        elif towhee.get_classical_potential() == "Tabulated Pair":
            write_interpolatestyle = True
        else:
            print "Invalid classical_potential!"

        if write_mixrule:
            file.write('classical_mixrule\n\'%s\'\n' % towhee.get_classical_mixrule())
            file.write('cmix_rescaling_style\n\'%s\'\n' % towhee.get_cmix_rescaling_style())
            if towhee.get_cmix_rescaling_style() == "grossfield 2003":
                file.write('cmix_lambda\n%s\n' % towhee.get_cmix_lambda())
                file.write('cmix_npair\n%d\n' % towhee.get_cmix_npair())
                file.write('cmix_pair_list\n')
                for cpl in towhee.get_cmix_pair_list():
                    file.write('\'%s\'\n' % cpl)

        if write_interpolatestyle:
            file.write('interpolatestyle\n%s\n' % towhee.get_interpolatestyle())

        if write_lshift:
            file.write('lshift\n%s\n' % truth_string(towhee.get_lshift()))

        if write_ltailc:
            file.write('ltailc\n%s\n' % truth_string(towhee.get_ltailc()))

        if write_rmin:
            file.write('rmin\n%s\n' % towhee.get_rmin())

        if write_rcut:
            file.write('rcut\n%s\n' % towhee.get_rcut())

        if write_rcutin:
            file.write('rcutin\n%s\n' % towhee.get_rcutin())

        if write_rpd:
            file.write('radial_pressure_delta\n%s\n' % towhee.get_radial_pressure_delta())

        file.write('coulombstyle\n\'%s\'\n' % towhee.get_coulombstyle())
        if towhee.get_coulombstyle() == "ewald_fixed_kmax":
            file.write('kalp\n%s\n' % towhee.get_kalp())
            file.write('kmax\n%d\n' % towhee.get_kmax())
            file.write('dielect\n%s\n' % towhee.get_dielect())
        elif towhee.get_coulombstyle() == "ewald_fixed_cutoff":
            file.write('ewald_prec\n%s\n' % towhee.get_ewald_prec())
            file.write('rcelect\n%s\n' % towhee.get_rcelect())
            file.write('dielect\n%s\n' % towhee.get_dielect())
        elif towhee.get_coulombstyle() == "minimum image":
            file.write('dielect\n%s\n' % towhee.get_dielect())

        file.write('nfield\n%d\n' % towhee.get_nfield())
        for ef in towhee.get_externalfields():
            file.write('fieldtype\n\'%s\'\n' % ef.get_fieldtype())

            if ef.get_fieldtype() == "Hard Wall":
                file.write('hrdbox\n%d\n' % ef.get_box())
                file.write('hrdxyz\n%s\n' % ef.get_xyz())
                file.write('hrdcen\n%s\n' % ef.get_cen())
                file.write('hrdrad\n%s\n' % ef.get_rad())
                file.write('hrd_energy_type\n\'%s\'\n' % ef.get_energy_type())
                if ef.get_energy_type() == "finite":
                    file.write('hrd_wall_energy\n%s\n' % ef.get_wall_energy())
            elif ef.get_fieldtype() == "LJ 9-3 Wall":
                file.write('ljfbox\n%d\n' % ef.get_box())
                file.write('ljfxyz\n%s\n' % ef.get_xyz())
                file.write('ljfcen\n%s\n' % ef.get_cen())
                file.write('ljfdir\n%d\n' % ef.get_dir())
                file.write('ljfcut\n%s\n' % ef.get_cut())
                file.write('ljfshift\n%s\n' % truth_string(ef.get_shift()))
                file.write('ljfrho\n%s\n' % ef.get_rho())
                file.write('ljfntypes\n%d\n' % ef.get_ntypes())
                for j in range(ef.get_ntypes()):
                    file.write('ljfname\n%s\n' % ef.get_single_name(j))
                    file.write('ljfsig\n%s\n' % ef.get_single_sig(j))
                    file.write('ljfeps\n%s\n' % ef.get_single_eps(j))
            elif ef.get_fieldtype() == "Hooper Umbrella":
                file.write('umbbox\n%d\n' % ef.get_box())
                file.write('umbxyz\n%s\n' % ef.get_xyz())
                file.write('umbcenter\n%s\n' % ef.get_center())
                file.write('umba\n%s\n' % ef.get_a())
            elif ef.get_fieldtype() == "Steele Wall":
                file.write('steele box\n%d\n' % ef.get_box())
                file.write('steele xyz\n%s\n' % ef.get_xyz())
                file.write('steele surface\n%s\n' % ef.get_surface())
                file.write('steele dir\n%d\n' % ef.get_dir())
                file.write('steele cutoff\n%s\n' % ef.get_cutoff())
                file.write('steele shift\n%s\n' % truth_string(ef.get_shift()))
                file.write('steele delta\n%s\n' % ef.get_delta())
                file.write('steele rho_s\n%s\n' % ef.get_rho_s())
                file.write('steele ntype\n%d\n' % ef.get_ntype())
                for j in range(ef.get_ntype()):
                    file.write('steele name\n%s\n' % ef.get_single_name(j))
                    file.write('sigma_sf\n%s\n' % ef.get_single_sigma_sf(j))
                    file.write('epsilon_sf\n%s\n' % ef.get_single_epsilon_sf(j))
            elif ef.get_fieldtype() == "Harmonic Attractor":
                file.write('hafbox\n%d\n' % ef.get_box())
                file.write('hafk\n%s\n' % ef.get_k())
                file.write('hafnentries\n%d\n' % ef.get_nentries())
                file.write('hafrefpos\n\'%s\'\n' % ef.get_refpos())
                if ef.get_refpos() == "Global":
                    file.write('hafglobxyz\n%s %s %s\n' % (ef.get_globx(), ef.get_globy(), ef.get_globz()))
                file.write('hafkey\n%s\n' % ef.get_key())
                for j in range(ef.get_nentries()):
                    file.write('hafmolec\n%d\n' % ef.get_single_molec(j))
                    if ef.get_key() == "Element":
                        file.write('hafelement\n%s\n' % ef.get_single_element(j))
                    else:
                        file.write('hafname\n%s\n' % ef.get_single_name(j))
            else:
                print "fieldtype error: " + ef.get_fieldtype()

        file.write('isolvtype\n%d\n' % towhee.get_isolvtype())
    # end of "if potentialstyle == classic or quantum//classical

    if towhee.get_potentialstyle() == "quantum" or\
    towhee.get_potentialstyle() == "quantum//classical":
        file.write('quantum code\n\'%s\'\n' % towhee.get_quantumcode())
        if towhee.get_quantumcode() == "Seqquest":
            file.write('functional\n%s\n' % towhee.get_functional())
            file.write('atom types\n%d\n' % towhee.get_atomtypes())

            file.write('atom filenames\n')
            for i in (towhee.get_atomfilenames()):
                file.write('%s\n' % i)
                
            file.write('grid multiplier\n%s\n' % towhee.get_gridmultiplier())
            file.write('kgridproduct\n%s\n' % towhee.get_kgridproduct())
        # if quantumcode == 'Seqquest'
    # if potientialstyle == quantum or quantum//classical

    file.write('linit\n%s\n' % towhee.get_linit())
    file.write('initboxtype\n\'%s\'\n' % towhee.get_initboxtype())

    write_initstyle = False
    if towhee.get_initboxtype() == "dimensions":
        write_initstyle = True
    elif towhee.get_initboxtype() == "number density":
        write_initstyle = True
    elif towhee.get_initboxtype() == "unit cell":
        write_initstyle = False

    if write_initstyle:
        file.write('initstyle\n')
        for i in range(towhee.get_numboxes()):
            file.write('\'%s\'' % towhee.get_single_initstyle(i, 0))
            for j in range(1, towhee.get_nmolty()):
                file.write(' \'%s\'' % towhee.get_single_initstyle(i, j))
            file.write('\n')

        for helix in towhee.get_helix():
            file.write('helix_moltyp\n%s\n' % helix.get_moltyp())
            file.write('helix_radius\n%s\n' % helix.get_radius())
            file.write('helix_angle\n%s\n' % helix.get_angle())
            file.write('helix_keytype\n%s\n' % helix.get_keytype())
            file.write('helix_keyname\n%s\n' % helix.get_keyname())
            file.write('helix_conlen\n%s\n' % helix.get_conlen())
            file.write('helix_phase\n%s\n' % helix.get_phase())

        file.write('initlattice\n')
        for i in range(towhee.get_numboxes()):
            file.write('\'%s\'' % towhee.get_single_initlattice(i, 0))
            for j in range(1, towhee.get_nmolty()):
                file.write(' \'%s\'' % towhee.get_single_initlattice(i, j))
            file.write('\n')

        file.write('initmol\n')
        for i in range(towhee.get_numboxes()):
            file.write('%d' % towhee.get_single_initmol(i, 0))
            for j in range(1, towhee.get_nmolty()):
                file.write(' %d' % towhee.get_single_initmol(i, j))
            file.write('\n')
    # End of if write_initstyle:

    file.write('inix\n')
    inix = towhee.get_inix()
    iniy = towhee.get_iniy()
    iniz = towhee.get_iniz()
    for xyz in range(len(inix)):
        file.write('%d %d %d\n' %  (inix[xyz], iniy[xyz], iniz[xyz]))

    if towhee.get_initboxtype() == "dimensions":
        file.write('hmatrix\n')
        for hm in towhee.get_hmatrix():
            file.write("%s %s %s\n" % tuple(hm.get_row1()))
            file.write("%s %s %s\n" % tuple(hm.get_row2()))
            file.write("%s %s %s\n" % tuple(hm.get_row3()))
    elif towhee.get_initboxtype() == "number density":
        file.write('box_number_density\n')
        for bnd in towhee.get_box_number_density():
            file.write("%s\n" % bnd)
    elif towhee.get_initboxtype() != "unit cell":
        print "Something went horribly wrong\n"
    #
    # Monte Carlo Moves
    #
    if (towhee.get_ensemble() == "nvt" and towhee.get_numboxes() > 1) or\
    towhee.get_ensemble() == "npt":
        #
        # Isotropic Volume Move
        #
        mcm = towhee.get_ivm()
        file.write('pmvol\n%s\n' % mcm.get_move_probability())
       
        pmvlpr = mcm.get_pmvlpr()
        file.write('          pmvlpr\n          %s' % pmvlpr[0])
        for pmv in pmvlpr[1:]:
            file.write(' %s' % pmv)
        file.write('\n')
        file.write('          rmvol\n          %s\n' % mcm.get_rmvol())
        file.write('          tavol\n          %s\n' % mcm.get_tavol())
        #
        # Anisotropic Volume Move
        #
        mcm = towhee.get_avm()
        file.write('pmcell\n%s\n' % mcm.get_move_probability())

        pmcellpr = mcm.get_pmcellpr()
        file.write('          pmcellpr\n          %s' % pmcellpr[0])
        for pmc in pmcellpr[1:]:
            file.write(' %s' % pmc)
        file.write('\n')

        if towhee.get_ensemble() == "npt":
            file.write('          pmcellpt\n          0.0\n')
        else:
            file.write('          pmcellpt\n')
            for stuff in mcm.get_pmcellpt():
                file.write('          %s\n' % stuff)
        file.write('          rmcell\n          %s\n' % mcm.get_rmcell())
        file.write('          tacell\n          %s\n' % mcm.get_tacell())

    if towhee.get_numboxes() > 1:
        #
        # Rotational-bias 2 box molecule Transfer Move
        #
        mcm = towhee.get_rb2bmtm()
        file.write('pm2boxrbswap\n%s\n' % mcm.get_move_probability())
        
        value = mcm.get_pm2rbswmt()
        file.write('          pm2rbswmt\n          %s' % value[0])
        for stuff in value[1:]:
            file.write(' %s' % stuff)
        file.write('\n')

        value = mcm.get_pm2rbswpr()
        file.write('          pm2rbswpr\n          %s' % value[0])
        for stuff in value[1:]:
            file.write(' %s' % stuff)
        file.write('\n')
        #
        # Configurational-bias 2 box molecule Transfer Move
        #
        mcm = towhee.get_cb2bmtm()
        file.write('pm2boxcbswap\n%s\n' % mcm.get_move_probability())

        value = mcm.get_pm2cbswmt()
        file.write('          pm2cbswmt\n          %s' % value[0])
        for stuff in value[1:]:
            file.write(' %s' % stuff)
        file.write('\n')

        value = mcm.get_pm2cbswpr()
        file.write('          pm2cbswpr\n          %s' % value[0])
        for stuff in value[1:]:
            file.write(' %s' % stuff)
        file.write('\n')

    if towhee.get_ensemble() == "'uvt'":
        #
        # Configurational-bias grand-canonical insertion/deletion Move
        #
        mcm = towhee.get_cbgcidm()
        file.write('pmuvcbswap\n%s\n' % mcm.get_move_probability())

        value = mcm.get_pmuvtcbmt()
        file.write('          pmuvtcbmt\n          %s' % value[0])
        for stuff in value[1:]:
            file.write(' %s' % stuff)
        file.write('\n')
    #
    # Configurational-bias single box molecule Reinsertion Move
    #
    mcm = towhee.get_cbsbmrm()
    file.write('pm1boxcbswap\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pm1cbswmt()
    file.write('          pm1cbswmt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')
    #
    # Aggregation Volume Bias Move Type 1
    #
    mcm = towhee.get_avbmt1()
    file.write('pmavb1\n%s\n' % mcm.get_move_probability())
    file.write('          pmavb1in\n          %s\n' % mcm.get_pmavb1in())

    value = mcm.get_pmavb1mt()
    file.write('          pmavb1mt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    file.write('          pmavb1ct\n')
    for i in range(towhee.get_nmolty()):
        file.write('          %s' % mcm.get_single_pmavb1ct(i, 0))
        for j in range(1, towhee.get_nmolty()):
            file.write(' %s' % mcm.get_single_pmavb1ct(i, j))
        file.write('\n')

    file.write('          avb1rad\n          %s\n' % mcm.get_avb1rad())
    #
    # Aggregation Volume Bias Move Type 2
    #
    mcm = towhee.get_avbmt2()
    file.write('pmavb2\n%s\n' % mcm.get_move_probability())
    file.write('          pmavb2in\n          %s\n' % mcm.get_pmavb2in())

    value = mcm.get_pmavb2mt()
    file.write('          pmavb2mt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    file.write('          pmavb2ct\n')
    for i in range(towhee.get_nmolty()):
        file.write('          %s' % mcm.get_single_pmavb2ct(i, 0))
        for j in range(1, towhee.get_nmolty()):
            file.write(' %s' % mcm.get_single_pmavb2ct(i, j))
        file.write('\n')

    file.write('          avb2rad\n          %s\n' % mcm.get_avb2rad())
    #
    # Aggregation Volume Bias Move Type 3
    #
    mcm = towhee.get_avbmt3()
    file.write('pmavb3\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmavb3mt()
    file.write('          pmavb3mt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    file.write('          pmavb3ct\n')
    for i in range(towhee.get_nmolty()):
        file.write('          %s' % mcm.get_single_pmavb3ct(i, 0))
        for j in range(1, towhee.get_nmolty()):
            file.write(' %s' % mcm.get_single_pmavb3ct(i, j))
        file.write('\n')

    file.write('          avb3rad\n          %s\n' % mcm.get_avb3rad())
    #
    # Configurational-Bias Partial Molecule Regrowth
    #
    mcm = towhee.get_cbpmr()

    file.write('pmcb\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmcbmt()
    file.write('          pmcbmt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = mcm.get_pmall()
    file.write('          pmall\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')
    #
    # Configurational-Bias Protein backbone Regrowth
    #
    mcm = towhee.get_cbpbr()

    file.write('pmback\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmbkmt()
    file.write('          pmbkmt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')
    #
    # Torsional Pivot Move
    #
    mcm = towhee.get_tpm()
    
    file.write('pmpivot\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmpivmt()
    file.write('          pmpivmt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')
    #
    # Concerted Rotation Move on a non-peptide backbone
    #
    mcm = towhee.get_crnmoanpb()

    file.write('pmconrot\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmcrmt()
    file.write('          pmcrmt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')
    #
    # Concerted Rotation Move over a 3 peptides backbone sequence
    #
    mcm = towhee.get_crnmoa3pbs()

    file.write('pmcrback\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmcrbmt()
    file.write('          pmcrbmt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')
    #
    # Plane Shift Move
    #
    mcm = towhee.get_psm()

    file.write('pmplane\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmplanebox()
    file.write('          pmplanebox\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    file.write('          planewidth\n          %s\n' % mcm.get_planewidth())
    #
    # Row Shift Move
    #
    mcm = towhee.get_rsm()

    file.write('pmrow\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmrowbox()
    file.write('          pmrowbox\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    file.write('          rowwidth\n          %s\n' % mcm.get_rowwidth())
    #
    # Intramolecular Single Atom Translation Move
    #
    mcm = towhee.get_isatm()

    file.write('pmtraat\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmtamt()
    file.write('          pmtamt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')
    file.write('          rmtraa\n          %s\n' % mcm.get_rmtraa())
    file.write('          tatraa\n          %s\n' % mcm.get_tatraa())
    #
    # Center-of-Mass Molecule Translation Move
    #
    mcm = towhee.get_cofmmtm()

    file.write('pmtracm\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmtcmt()
    file.write('          pmtcmt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    file.write('          rmtrac\n          %s\n' % mcm.get_rmtrac())
    file.write('          tatrac\n          %s\n' % mcm.get_tatrac())
    #
    # Rotation about the Center-of-Mass Move
    #
    mcm = towhee.get_ratcomm()

    file.write('pmrotate\n%s\n' % mcm.get_move_probability())

    value = mcm.get_pmromt()
    file.write('          pmromt\n          %s' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    file.write('          rmrot\n          %s\n' % mcm.get_rmrot())
    file.write('          tarot\n          %s\n' % mcm.get_tarot())
    #
    # End of Monte Carlo Moves
    #
    file.write('tor_cbstyle\n%d\n' % towhee.get_tor_cbstyle())
    if towhee.get_tor_cbstyle() == 1:
        file.write('sdevtor\n%s\n' % towhee.get_sdevtor())
    
    file.write('bend_cbstyle\n%d\n' % towhee.get_bend_cbstyle())
    if towhee.get_bend_cbstyle() == 1: 
        file.write('sdevbena\n%s\n' % towhee.get_sdevbena())
        file.write('sdevbenb\n%s\n' % towhee.get_sdevbenb())
        
    file.write('vib_cbstyle\n%d\n' % towhee.get_vib_cbstyle())
    if towhee.get_vib_cbstyle() == 0:
        file.write('vibrang\n%s %s\n' % tuple(towhee.get_vibrang()))
    elif towhee.get_vib_cbstyle() == 1:
        file.write('sdevvib\n%s\n' % towhee.get_sdevvib())
    else:
        print "vib_cbstyle error:  vib_cbstyle = " + str(towhee.get_vib_cbstyle())

    file.write('cdform\n%d\n' % towhee.get_cdform())

    value = towhee.get_nch_nb_one()
    file.write('nch_nb_one\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = towhee.get_nch_nb()
    file.write('nch_nb\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = towhee.get_nch_tor_out()
    file.write('nch_tor_out\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = towhee.get_nch_tor_in()
    file.write('nch_tor_in\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = towhee.get_nch_tor_in_con()
    file.write('nch_tor_in_con\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = towhee.get_nch_bend_a()
    file.write('nch_bend_a\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = towhee.get_nch_bend_b()
    file.write('nch_bend_b\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    value = towhee.get_nch_vib()
    file.write('nch_vib\n%d' % value[0])
    for stuff in value[1:]:
        file.write(' %s' % stuff)
    file.write('\n')

    for input in towhee.get_inputs():
        file.write('inpstyle\n%d\n' % input.get_inpstyle())

        if input.get_inpstyle() != 4:
            file.write('nunit\n%d\n' % input.get_nunit())
            file.write('nmaxcbmc\n%d\n' % input.get_nmaxcbmc())

        if input.get_inpstyle() == 0:
            file.write('lpdb\n%s\n' % truth_string(input.get_lpdb()))

            for i in range(input.get_nunit()):
                unit = input.get_single_unit(i)
                type = input.get_single_type(i)
                qqatom = input.get_single_qqatom(i)
                file.write('unit\n')
                file.write('%d %d %s\n' % (unit, type, qqatom))

                if input.get_lpdb():
                    file.write('pdbname\n')
                    pdbname = input.get_single_pdbname(i)
                    aminonum = input.get_single_aminonum(i)
                    aminoshort = input.get_single_aminoshort(i)
                    file.write('%s %d %s\n' % (pdbname, aminonum, aminoshort))

                # Write bond vibrations
                vib = input.get_single_vibration(i)
                file.write('vibration\n%d\n' % vib.get_number_vibrations())
                for vibes in vib.get_vibrations():
                    file.write("%d %d\n" % tuple(vibes))
                
                # Write bond bending
                bend = input.get_single_bending(i)
                file.write('bending\n%d\n' % bend.get_number_bendings())
                for bendings in bend.get_bendings():
                    file.write('%d %d %d\n' % tuple(bendings))

                # Write bond torsions
                tors = input.get_single_torsion(i)
                file.write('torsion\n%d\n' % tors.get_number_torsions())
                for torsions in tors.get_torsions():
                    file.write('%d %d %d %d\n' % tuple(torsions))

                # Write angle-angle
                angs = input.get_single_angle(i)
                file.write('angle-angle\n%d\n' % angs.get_number_angles())
                for angles in angs.get_angles():
                    file.write('%d %d %d %d\n' % tuple(angles))

                # Write improper torsions
                imptors = input.get_single_improper_torsion(i)
                file.write('improper torsion\n%d\n' % imptors.get_number_improper_torsions())
                for impropers in imptors.get_improper_torsions():
                    file.write('%d %d %d %d\n' % tuple(impropers))
                # End of loop of nunits
            # End if
        elif input.get_inpstyle() == 1:
            file.write('forcefield\n%s\n' % input.get_forcefield())
            file.write('protgeom\n\'%s\'\n' % input.get_protgeom())

            file.write('pepname\n')

            for i in range(input.get_nunit()):
                if input.get_protgeom() == "cyclic":
                    pep = input.get_single_pepname(i)
                    stereo = input.get_single_stereochem(i)
                    bond = input.get_single_bondpartner(i)
                    file.write('%s %s %d\n' % (pep, stereo, bond))
                elif input.get_protgeom() == "linear":
                    pep = input.get_single_pepname(i)
                    stereo = input.get_single_stereochem(i)
                    bond = input.get_single_bondpartner(i)
                    term = input.get_single_terminus(i)
                    file.write('%s %s %d %s\n' % (pep, stereo, bond, term))
                else:
                    print "Save Error: Invalid protgeom"

        elif input.get_inpstyle() == 2:
            file.write('forcefield\n%s\n' % input.get_forcefield())
            file.write('charge_assignment\n\'%s\'\n' % input.get_charge_assignment())

            for i in range(input.get_nunit()):
                if input.get_charge_assignment() == "manual":
                    unit = input.get_single_unit(i)
                    type = input.get_single_type(i)
                    qqatom = input.get_single_qqatom(i)
                    file.write('unit\n%d %s %s\n' % (unit, type, qqatom))
                else:
                    unit = input.get_single_unit(i)
                    type = input.get_single_type(i)
                    file.write('unit\n%d %s\n' % (unit, type))

                # Vibrations
                vibs = input.get_single_vibration(i)
                file.write('vibration\n%d\n' % vibs.get_number_vibrations())
                if vibs.get_number_vibrations() != 0:
                    vibes = vibs.get_vibrations()
                    file.write('%d' % vibes[0])
                    for stuff in vibes[1:]:
                        file.write(' %d' % stuff)
                    file.write('\n') 

                # Improper Torsions
                imptors = input.get_single_improper_torsion(i)
                file.write('improper\n%d\n' % imptors.get_number_improper_torsions())
                for improper in imptors.get_improper_torsions():
                    file.write('%d %d %d %d\n' % tuple(improper))

        elif input.get_inpstyle() == 3:
            file.write('terminus\n%d\n' % input.get_terminus())
            file.write('forcefield\n%s\n' % input.get_forcefield())
            file.write('monomername\n')
            for stuff in input.get_monomername():
                file.write('%s\n' % stuff)

        elif input.get_inpstyle() == 4:
            file.write('forcefield\n%s\n' % input.get_forcefield())
            file.write('atomname\n%s\n' % input.get_atomname())
            file.write('qqatom\n%s\n' % input.get_qqatom())
            file.write('nanotube_n\n%d\n' % input.get_n())
            file.write('nanotube_m\n%d\n' % input.get_m())
            file.write('nanotube_ncells\n%d\n' % input.get_ncells())
            file.write('nanotube_bondlength\n%s\n' % input.get_bondlength())
        else:
            print "Saving Error: Invalid inpstyle"
    return

def load_good_strings():
    good_strings = []
    good_strings.append("ensemble")
    good_strings.append("temperature")
    good_strings.append("pressure")
    good_strings.append("nmolty")
    good_strings.append("nmolectyp")
    good_strings.append("chempot")
    good_strings.append("numboxes")
    good_strings.append("stepstyle")
    good_strings.append("nstep")
    good_strings.append("optstyle")
    good_strings.append("mintol")
    good_strings.append("printfreq")
    good_strings.append("blocksize")
    good_strings.append("moviefreq")
    good_strings.append("backupfreq")
    good_strings.append("runoutput")
    good_strings.append("pdb_output_freq")
    good_strings.append("loutdft")
    good_strings.append("loutlammps")
    good_strings.append("louthist")
    good_strings.append("histcalcfreq")
    good_strings.append("histcalcdump")
    good_strings.append("pressurefreq")
    good_strings.append("trmaxdispfreq")
    good_strings.append("volmaxdispfreq")
    good_strings.append("potentialstyle")
    good_strings.append("ffnumber")
    good_strings.append("ff_filename")
    good_strings.append("classical_potential")
    good_strings.append("classical_mixrule")
    good_strings.append("cmix_rescaling_style")
    good_strings.append("cmix_lambda")
    good_strings.append("cmix_npair")
    good_strings.append("cmix_pair_list")
    good_strings.append("lshift")
    good_strings.append("ltailc")
    good_strings.append("rmin")
    good_strings.append("rcut")
    good_strings.append("rcutin")
    good_strings.append("interpolatestyle")
    good_strings.append("radial_pressure_delta")
    good_strings.append("coulombstyle")
    good_strings.append("kalp")
    good_strings.append("kmax")
    good_strings.append("dielect")
    good_strings.append("ewald_prec")
    good_strings.append("rcelect")
    good_strings.append("dielect")
    good_strings.append("nfield")
    good_strings.append("fieldtype")
    good_strings.append("nhrdfld")
    good_strings.append("hrdbox")
    good_strings.append("hrdxyz")
    good_strings.append("hrdcen")
    good_strings.append("hrdrad")
    good_strings.append("hrd_energy_type")
    good_strings.append("hrd_wall_energy")
    good_strings.append("nljfld")
    good_strings.append("ljfbox")
    good_strings.append("ljfxyz")
    good_strings.append("ljfcen")
    good_strings.append("ljfdir")
    good_strings.append("ljfcut")
    good_strings.append("ljfshift")
    good_strings.append("ljfrho")
    good_strings.append("ljfntypes")
    good_strings.append("ljfname")
    good_strings.append("ljfsig")
    good_strings.append("ljfeps")
    good_strings.append("steele box")
    good_strings.append("steele xyz")
    good_strings.append("steele surface")
    good_strings.append("steele dir")
    good_strings.append("steele cutoff")
    good_strings.append("steele shift")
    good_strings.append("steele delta")
    good_strings.append("steele rho_s")
    good_strings.append("steele ntype")
    good_strings.append("steele name")
    good_strings.append("sigma_sf")
    good_strings.append("epsilon_sf")
    good_strings.append("numbfld")
    good_strings.append("umbbox")
    good_strings.append("umbxyz")
    good_strings.append("umbcenter")
    good_strings.append("umba")
    good_strings.append("isolvtype")
    good_strings.append("quantum code")
    good_strings.append("functional")
    good_strings.append("atom types")
    good_strings.append("atom filenames")
    good_strings.append("grid multiplier")
    good_strings.append("kgrid product")
    good_strings.append("linit")
    good_strings.append("initstyle")
    good_strings.append("helix_moltyp")
    good_strings.append("helix_radius")
    good_strings.append("helix_angle")
    good_strings.append("helix_keytype")
    good_strings.append("helix_keyname")
    good_strings.append("helix_conlen")
    good_strings.append("helix_phase")
    good_strings.append("hmatrix")
    good_strings.append("initlattice")
    good_strings.append("initmol")
    good_strings.append("inix")
    good_strings.append("initboxtype")
    good_strings.append("pmvol")
    good_strings.append("pmvlpr")
    good_strings.append("rmvol")
    good_strings.append("tavol")
    good_strings.append("pmcell")
    good_strings.append("pmcellpr")
    good_strings.append("pmcellpt")
    good_strings.append("rmcell")
    good_strings.append("tacell")
    good_strings.append("pm2boxrbswap")
    good_strings.append("pm2rbswmt")
    good_strings.append("pm2rbswpr")
    good_strings.append("pm2boxcbswap")
    good_strings.append("pm2cbswmt")
    good_strings.append("pm2cbswpr")
    good_strings.append("pmuvtcbswap")
    good_strings.append("pmuvtcbmt")
    good_strings.append("pm1boxcbswap")
    good_strings.append("pm1cbswmt")
    good_strings.append("pmavb1")
    good_strings.append("pmavb1in")
    good_strings.append("pmavb1mt")
    good_strings.append("pmavb1ct")
    good_strings.append("avb1rad")
    good_strings.append("pmavb2")
    good_strings.append("pmavb2in")
    good_strings.append("pmavb2mt")
    good_strings.append("pmavb2ct")
    good_strings.append("avb2rad")
    good_strings.append("pmavb3")
    good_strings.append("pmavb3mt")
    good_strings.append("pmavb3ct")
    good_strings.append("avb3rad")
    good_strings.append("pmcb")
    good_strings.append("pmcbmt")
    good_strings.append("pmall")
    good_strings.append("pmback")
    good_strings.append("pmbkmt")
    good_strings.append("pmpivot")
    good_strings.append("pmpivmt")
    good_strings.append("pmconrot")
    good_strings.append("pmcrmt")
    good_strings.append("pmcrback")
    good_strings.append("pmcrbmt")
    good_strings.append("pmplane")
    good_strings.append("pmplanebox")
    good_strings.append("planewidth")
    good_strings.append("pmrow")
    good_strings.append("pmrowbox")
    good_strings.append("rowwidth")
    good_strings.append("pmtraat")
    good_strings.append("pmtamt")
    good_strings.append("rmtraa")
    good_strings.append("tatraa")
    good_strings.append("pmtracm")
    good_strings.append("pmtcmt")
    good_strings.append("rmtrac")
    good_strings.append("tatrac")
    good_strings.append("pmrotate")
    good_strings.append("pmromt")
    good_strings.append("rmrot")
    good_strings.append("tarot")
    good_strings.append("tor_cbstyle")
    good_strings.append("bend_cbstyle")
    good_strings.append("vib_cbstyle")
    good_strings.append("sdevtor")
    good_strings.append("sdevbena")
    good_strings.append("sdevbenb")
    good_strings.append("sdevvib")
    good_strings.append("vibrang")
    good_strings.append("cdform")
    good_strings.append("nch_nb_one")
    good_strings.append("nch_nb")
    good_strings.append("nch_tor_out")
    good_strings.append("nch_tor_in")
    good_strings.append("nch_tor_in_con")
    good_strings.append("nch_bend_a")
    good_strings.append("nch_bend_b")
    good_strings.append("nch_vib")
    good_strings.append("inpstyle")
    good_strings.append("nunit")
    good_strings.append("nmaxcbmc")
    good_strings.append("lpdb")
    good_strings.append("unit")
    good_strings.append("pdbname")
    good_strings.append("vibration")
    good_strings.append("bending")
    good_strings.append("torsion")
    good_strings.append("angle-angle")
    good_strings.append("improper torsion")
    good_strings.append("forcefield")
    good_strings.append("protgeom")
    good_strings.append("pepname")
    good_strings.append("forcefield")
    good_strings.append("unit")
    good_strings.append("vibration")
    good_strings.append("improper")
    good_strings.append("terminus")
    good_strings.append("forcefield")
    good_strings.append("charge_assignment")
    good_strings.append("monomername")
    good_strings.append("forcefield")
    good_strings.append("atomname")
    good_strings.append("qqatom")
    good_strings.append("nanotube_n")
    good_strings.append("nanotube_m")
    good_strings.append("nanotube_ncells")
    good_strings.append("nanotube_bondlength")
    return good_strings

def verify_line(read_line, good_string):
    line = read_line.strip()
    if line.rfind(good_string) != -1:
        return True
    else:
        return False

def check_all_strings(line, good_strings):
    line = line.strip()
    if line in good_strings:
        return True
    else:
        return False

def error_message(line, good_string):
    import wx
    line = line.strip()
    d = wx.MessageDialog(None,
        "Variable not found\n"
        "Observed = " + line + "\n"
        "Expected = " + good_string + "\n",
        "Variable not found",
        wx.ICON_ERROR)
    d.ShowModal()
    d.Destroy()
    return
   
def filter_line(line):
    filtered_line = line.strip()
    if filtered_line[0] == "'":
        filtered_line = filtered_line[1:]

    if filtered_line[-1] == "'":
        filtered_line = filtered_line[0:-1]

    return filtered_line

def is_it_true(line):
    if line.rfind("t") != -1 or line.rfind("T") != -1:
        return True
    else:
        return False

def truth_string(tf):
    if tf:
        return ".true."
    else:
        return ".false."

#
# When the line gets split, it gets split by spaces (" ").  This has
# the side effect of splitting full cmbc and partial cmbc even though
# they are one value. This code puts them back together and returns the
# array of initstyle values
#
def fix_initstyle(t):
    init = []
    for i in range(len(t)):
        if t[i] == "'full" or t[i] == "'partial":
            value = t[i] + " " + t[i+1]
            init.append(value)
        elif t[i] != "cbmc'":
            init.append(t[i])
    return init

#
# When the line gets split, it gets split by spaces (" ").  This has
# the side effect of splitting simple cubic even though it is one value.
# This code puts them back together and returns the array of
# initlattice values
#
def fix_initlattice(t):
    init = []
    for i in range(len(t)):
        if t[i] == "'simple":
            value = t[i] + " " + t[i+1]
            init.append(value)
        elif t[i] != "cubic'":
            init.append(t[i])
    return init
        
