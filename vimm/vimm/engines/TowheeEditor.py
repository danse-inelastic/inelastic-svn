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


import copy
import wx

class TowheeEditor(wx.Frame):
    def __init__(self, parent, ID, title, towhee, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, ID, title, **kwds)
     
        self.parent = parent
        self.towhee = towhee
        self.old_towhee = copy.deepcopy(towhee)

        self.helix_failure = False
        self.ivm_failure = False
        self.avm_failure = False
        self.cbsbmrm_failure = False
        self.rb2bmtm_failure = False
        self.cb2bmtm_failure = False
        self.gcid_failure = False
        self.avbmt1_failure = False
        self.avbmt2_failure = False
        self.avbmt3_failure = False
        self.cbpmr_failure = False
        self.cbpbr_failure = False
        self.tpm_failure = False
        self.crmnpb_failure = False
        self.crm3pbs_failure = False
        self.psm_failure = False
        self.rsm_failure = False
        self.isatm_failure = False
        self.cmmtm_failure = False
        self.rcmm_failure = False

        self.nbTowheeEditor = wx.Notebook(self, -1)
        #
        # Create each Notebook tab
        #
        self.pnInputs = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        self.pnCBMC = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        self.pnMCM = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        self.pnInit = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        self.pnExternalFields = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        self.pnFF = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        self.pnRunInfo = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        self.pnBasic = wx.ScrolledWindow(self.nbTowheeEditor, -1, style=wx.TAB_TRAVERSAL)
        #
        # Create widgets to go on Basic tab
        #
        self.lblRandomseed = wx.StaticText(self.pnBasic, -1, "Random Seed", style=wx.ALIGN_RIGHT)
        basic_size = self.lblRandomseed.GetSize()
        self.txtRandomseed = wx.TextCtrl(self.pnBasic, -1, str(self.towhee.get_randomseed()))
        self.lblEnsemble = wx.StaticText(self.pnBasic, -1, "Ensemble", size=basic_size, style=wx.ALIGN_RIGHT)
        self.cboEnsemble = wx.ComboBox(self.pnBasic, -1, choices=["npt", "nvt", "uvt"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1))
        self.cboEnsemble.SetStringSelection(self.towhee.get_ensemble())
        self.lblNmolty = wx.StaticText(self.pnBasic, -1, "nmolty", size=basic_size, style=wx.ALIGN_RIGHT)
        self.txtNmolty = wx.TextCtrl(self.pnBasic, -1, str(self.towhee.get_nmolty()))
        self.lblNumboxes = wx.StaticText(self.pnBasic, -1, "numboxes", size=basic_size, style=wx.ALIGN_RIGHT)
        self.txtNumboxes = wx.TextCtrl(self.pnBasic, -1, str(self.towhee.get_numboxes()))
        #
        # Create widgets to go on Run Information tab
        # Run Information Column 1
        #
        self.lblPdbOutputFreq = wx.StaticText(self.pnRunInfo, -1, "pdb_output_freq", style=wx.ALIGN_RIGHT)
        ri1size = self.lblPdbOutputFreq.GetSize()
        self.lblTemperature = wx.StaticText(self.pnRunInfo, -1, "temperature", size=ri1size, style=wx.ALIGN_RIGHT)
        self.txtTemperature = wx.TextCtrl(self.pnRunInfo, -1, self.towhee.get_temperature())
        self.lblPressure = wx.StaticText(self.pnRunInfo, -1, "pressure", size=ri1size, style=wx.ALIGN_RIGHT)
        self.txtPressure = wx.TextCtrl(self.pnRunInfo, -1, self.towhee.get_pressure())
        self.lblChempot = wx.StaticText(self.pnRunInfo, -1, "chempot", size=ri1size, style=wx.ALIGN_RIGHT)
        self.txtChempot = []
        for chempot in self.towhee.get_chempot():
            self.txtChempot.append(wx.TextCtrl(self.pnRunInfo, -1, chempot))
        self.txtPdbOutputFreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_pdb_output_freq()))
        self.lblnmolectype = wx.StaticText(self.pnRunInfo, -1, "nmolectyp", size=ri1size, style=wx.ALIGN_RIGHT)
        self.txtNmolectype = []
        for nm in self.towhee.get_nmolectyp():
            self.txtNmolectype.append(wx.TextCtrl(self.pnRunInfo, -1, str(nm)))
        self.lblLoutdft = wx.StaticText(self.pnRunInfo, -1, "loutdft", size=ri1size, style=wx.ALIGN_RIGHT)
        self.rbLoutdft = wx.RadioBox(self.pnRunInfo, -1, "", choices=["True", "False"],\
            majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        if self.towhee.get_loutdft():
            self.rbLoutdft.SetSelection(0)
        else:
            self.rbLoutdft.SetSelection(1)
        self.lblLoutlammps = wx.StaticText(self.pnRunInfo, -1, "loutlammps", size=ri1size, style=wx.ALIGN_RIGHT)
        self.rbLoutlammps = wx.RadioBox(self.pnRunInfo, -1, "", choices=["True", "False"],\
            majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        if self.towhee.get_loutlammps():
            self.rbLoutlammps.SetSelection(0)
        else:
            self.rbLoutlammps.SetSelection(1)
        self.lblStepstyle = wx.StaticText(self.pnRunInfo, -1, "stepstyle", size=ri1size, style=wx.ALIGN_RIGHT)
        self.cboStepstyle = wx.ComboBox(self.pnRunInfo, -1, choices=["cycles", "moves", "minimize"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cboStepstyle.SetStringSelection(self.towhee.get_stepstyle())
        self.lblNstep = wx.StaticText(self.pnRunInfo, -1, "nstep", size=ri1size, style=wx.ALIGN_RIGHT)
        self.txtNstep = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_nstep()))
        self.lblOptstyle = wx.StaticText(self.pnRunInfo, -1, "optstyle", size=ri1size, style=wx.ALIGN_RIGHT)
        self.txtOptstyle = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_optstyle()))
        self.lblMintol = wx.StaticText(self.pnRunInfo, -1, "mintol", size=ri1size, style=wx.ALIGN_RIGHT)
        self.txtMintol = wx.TextCtrl(self.pnRunInfo, -1, self.towhee.get_mintol())
        #
        # Run Information Column 2
        #
        self.lblChempotperstep = wx.StaticText(self.pnRunInfo, -1, "chempotperstep", style=wx.ALIGN_RIGHT)
        ri2size = self.lblChempotperstep.GetSize()
        self.txtChempotperstep = []
        for i in self.towhee.get_chempotperstep():
            self.txtChempotperstep.append(wx.TextCtrl(self.pnRunInfo, -1, str(i)))
        self.lblRunoutput = wx.StaticText(self.pnRunInfo, -1, "runoutput", size=ri2size, style=wx.ALIGN_RIGHT)
        self.cboRunoutput = wx.ComboBox(self.pnRunInfo, -1,
            choices=["full", "blocks", "updates", "none"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cboRunoutput.SetStringSelection(self.towhee.get_runoutput())
        self.lblPrintfreq = wx.StaticText(self.pnRunInfo, -1, "printfreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtPrintfreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_printfreq()))
        self.lblMoviefreq = wx.StaticText(self.pnRunInfo, -1, "moviefreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtMoviefreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_moviefreq()))
        self.lblBackupfreq = wx.StaticText(self.pnRunInfo, -1, "backupfreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtBackupfreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_backupfreq()))
        self.lblPressurefreq = wx.StaticText(self.pnRunInfo, -1, "pressurefreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtPressurefreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_pressurefreq()))
        self.lblTrmaxdispfreq = wx.StaticText(self.pnRunInfo, -1, "trmaxdispfreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtTrmaxdispfreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_trmaxdispfreq()))
        self.lblVolmaxdispfreq = wx.StaticText(self.pnRunInfo, -1, "volmaxdispfreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtVolmaxdispfreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_volmaxdispfreq()))
        self.lblBlocksize = wx.StaticText(self.pnRunInfo, -1, "blocksize", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtBlocksize = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_blocksize()))
        self.lblLouthist = wx.StaticText(self.pnRunInfo, -1, "louthist", size=ri2size, style=wx.ALIGN_RIGHT)
        self.rbLouthist = wx.RadioBox(self.pnRunInfo, -1, "", choices=["True", "False"],\
            majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        if self.towhee.get_louthist():
            self.rbLouthist.SetSelection(0)
        else:
            self.rbLouthist.SetSelection(1)
        self.lblHistcalcfreq = wx.StaticText(self.pnRunInfo, -1, "histcalcfreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtHistcalcfreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_histcalcfreq()))
        self.lblHistdumpfreq = wx.StaticText(self.pnRunInfo, -1, "histdumpfreq", size=ri2size, style=wx.ALIGN_RIGHT)
        self.txtHistdumpfreq = wx.TextCtrl(self.pnRunInfo, -1, str(self.towhee.get_histdumpfreq()))
        #
        # Create widgets to go on Force Field tab
        # Column 1
        #
        self.lblRadialPressureDelta = wx.StaticText(self.pnFF, -1, "radial pressure delta", style=wx.ALIGN_RIGHT)
        self.txtRadialPressureDelta = wx.TextCtrl(self.pnFF, -1, self.towhee.get_radial_pressure_delta())
        ff1size = self.lblRadialPressureDelta.GetSize()
        self.lblClassicalPotential = wx.StaticText(self.pnFF, -1, "classical potential", size=ff1size, style=wx.ALIGN_RIGHT)
        self.lblPotentialStyle = wx.StaticText(self.pnFF, -1, "potentialstyle", size=ff1size, style=wx.ALIGN_RIGHT)
        self.cboPotentialStyle = wx.ComboBox(self.pnFF, -1, choices=[\
            "classical",\
            ], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cboPotentialStyle.SetStringSelection(self.towhee.get_potentialstyle())
        self.lblIsolvtype = wx.StaticText(self.pnFF, -1, "Isolvtype", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtIsolvtype = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_isolvtype()))
        self.cboClassicalPotential = wx.ComboBox(self.pnFF, -1, size=(225,-1), choices=[\
            "Lennard-Jones",\
            "9-6",\
            "Exponential-6",\
            "Hard Sphere",\
            "Gordon n-6",\
            "Repulsive Sphere",\
            "Exponential-12-6",\
            "Stillinger-Weber",\
            "Embedded Atom Method",\
            "12-6 plus solvation",\
            "12-6 plus 12-10 H-bond",\
            "12-9-6",\
            "Square Well",\
            "Tabulated Pair",\
            "Repulsive Well",\
            "Multiwell",\
            "Repulsive Multiwell"\
            ], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cboClassicalPotential.SetStringSelection(self.towhee.get_classical_potential())
        self.lblCmixRescalingStyle = wx.StaticText(self.pnFF, -1, "cmix rescaling style", size=ff1size, style=wx.ALIGN_RIGHT)
        self.cboCmixRescalingStyle = wx.ComboBox(self.pnFF, -1, size=(225,-1), choices=[\
            "none",\
            "grossfield 2003",\
            ], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cboCmixRescalingStyle.SetStringSelection(self.towhee.get_cmix_rescaling_style())
        self.lblCmixLambda = wx.StaticText(self.pnFF, -1, "cmix lambda", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtCmixLambda = wx.TextCtrl(self.pnFF, -1, self.towhee.get_cmix_lambda())
        self.lblCmixNpair = wx.StaticText(self.pnFF, -1, "cmix npair", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtCmixNpair = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_cmix_npair()))
        self.lblCmixPairList = wx.StaticText(self.pnFF, -1, "cmix pair list", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtCmixPairList = []
        for cpl in self.towhee.get_cmix_pair_list():
            self.txtCmixPairList.append(wx.TextCtrl(self.pnFF, -1, cpl))
        self.lblClassicalMixrule = wx.StaticText(self.pnFF, -1, "classical mixrule", size=ff1size, style=wx.ALIGN_RIGHT)
        self.cboClassicalMixrule = wx.ComboBox(self.pnFF, -1, size=(175,-1), choices=[\
            "Lorentz-Berthelot",\
            "Geometric",\
            "Compass",\
            "Gromos",\
            "Explicit",\
            "Arithmetic"\
            ], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.cboClassicalMixrule.SetStringSelection(self.towhee.get_classical_mixrule())
        self.lblLshift = wx.StaticText(self.pnFF, -1, "lshift", size=ff1size, style=wx.ALIGN_RIGHT)
        self.rbLshift = wx.RadioBox(self.pnFF, -1, "", choices=["True", "False"],\
            majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        if self.towhee.get_lshift():
            self.rbLshift.SetSelection(0)
        else:
            self.rbLshift.SetSelection(1)
        self.lblLtailc = wx.StaticText(self.pnFF, -1, "ltailc", size=ff1size, style=wx.ALIGN_RIGHT)
        self.rbLtailc = wx.RadioBox(self.pnFF, -1, "", choices=["True", "False"],\
            majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        if self.towhee.get_ltailc():
            self.rbLtailc.SetSelection(0)
        else:
            self.rbLtailc.SetSelection(1)
        self.lblRmin = wx.StaticText(self.pnFF, -1, "rmin", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtRmin = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_rmin()))
        self.lblRcut = wx.StaticText(self.pnFF, -1, "rcut", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtRcut = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_rcut()))
        self.lblRcutin = wx.StaticText(self.pnFF, -1, "rcutin", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtRcutin = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_rcutin()))
        self.lblInterpolatestyle = wx.StaticText(self.pnFF, -1, "interpolatestyle", size=ff1size, style=wx.ALIGN_RIGHT)
        self.txtInterpolatestyle = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_interpolatestyle()))
        #
        # Forcefield Tab Column 2
        #
        self.lblCoulombstyle = wx.StaticText(self.pnFF, -1, "coulombstyle", style=wx.ALIGN_RIGHT)
        ff2size = self.lblCoulombstyle.GetSize()
        self.cboCoulombstyle = wx.ComboBox(self.pnFF, -1,\
            choices=["none", "ewald_fixed_kmax", "ewald_fixed_cutoff", "minimum image"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(250,-1))
        self.cboCoulombstyle.SetStringSelection(self.towhee.get_coulombstyle())
        self.lblFfnumber = wx.StaticText(self.pnFF, -1, "ffnumber", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtFfnumber = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_ffnumber()))
        self.lblFf_filename = wx.StaticText(self.pnFF, -1, "ff_filename", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtFf_filename = []
        for ff in self.towhee.get_ff_filename():
            self.txtFf_filename.append(wx.TextCtrl(self.pnFF, -1, ff, size=(400,-1)))
        self.lblKalp = wx.StaticText(self.pnFF, -1, "kalp", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtKalp = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_kalp()))
        self.lblKmax = wx.StaticText(self.pnFF, -1, "kmax", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtKmax = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_kmax()))
        self.lblEwald_prec = wx.StaticText(self.pnFF, -1, "ewald_prec", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtEwald_prec = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_ewald_prec()))
        self.lblRcelect = wx.StaticText(self.pnFF, -1, "rcelect", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtRcelect = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_rcelect()))
        self.lblDielectric = wx.StaticText(self.pnFF, -1, "dielectric", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtDielectric = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_dielect()))
        self.lblNfield = wx.StaticText(self.pnFF, -1, "nfield", size=ff2size, style=wx.ALIGN_RIGHT)
        self.txtNfield = wx.TextCtrl(self.pnFF, -1, str(self.towhee.get_nfield()))
        #
        # Create widgets to go on External Fields tab
        #
        self.lblFieldType = []
        self.cboFieldType = []
        self.fieldtypeID = []
        # Hard Wall
        self.lblHrdbox = []
        self.txtHrdbox = []
        self.lblHrdxyz = []
        self.txtHrdxyz = []
        self.lblHrdcen = []
        self.txtHrdcen = []
        self.lblHrdrad = []
        self.txtHrdrad = []
        self.lblHrdEnergyType = []
        self.cboHrdEnergyType = []
        self.hrdenergytypeID = []
        self.lblHrdWallEnergy = []
        self.txtHrdWallEnergy = []
        # Harmonic Attractor
        self.lblHafbox = []
        self.txtHafbox = []
        self.lblHafk = []
        self.txtHafk = []
        self.lblHafnentries = []
        self.txtHafnentries = []
        self.hafnentriesID = []
        self.lblHafrefpos = []
        self.cboHafrefpos = []
        self.hafrefposID = []
        self.lblHafglobxyz = []
        self.txtHafglobx = []
        self.txtHafgloby = []
        self.txtHafglobz = []
        self.lblHafkey = []
        self.cboHafkey = []
        self.hafkeyID = []
        self.lblHafmolec = []
        self.txtHafmolec = []
        self.lblHafelement = []
        self.txtHafelement = []
        self.lblHafname = []
        self.txtHafname = []
        # LJ 9-3 Wall
        self.lblLjfbox = []
        self.txtLjfbox = []
        self.lblLjfxyz = []
        self.txtLjfxyz = []
        self.lblLjfcen = []
        self.txtLjfcen = []
        self.lblLjfdir = []
        self.txtLjfdir = []
        self.lblLjfcut = []
        self.txtLjfcut = []
        self.lblLjfshift = []
        self.rbLjfshift = []
        self.lblLjfrho = []
        self.txtLjfrho = []
        self.lblLjfntypes = []
        self.txtLjfntypes = []
        self.lblLjfname = []
        self.txtLjfname = []
        self.lblLjfsig = []
        self.txtLjfsig = []
        self.lblLjfeps = []
        self.txtLjfeps = []
        self.ljfntypesID = []
        # Hooper Umbrella
        self.lblUmbbox = []
        self.txtUmbbox = []
        self.lblUmbxyz = []
        self.txtUmbxyz = []
        self.lblUmbcenter = []
        self.txtUmbcenter = []
        self.lblUmba = []
        self.txtUmba = []
        # Steele Wall
        self.lblSteelebox = []
        self.txtSteelebox = []
        self.lblSteelexyz = []
        self.txtSteelexyz = []
        self.lblSteelesurface = []
        self.txtSteelesurface = []
        self.lblSteeledir = []
        self.txtSteeledir = []
        self.lblSteelecutoff = []
        self.txtSteelecutoff = []
        self.lblSteeleshift = []
        self.rbSteeleshift = []
        self.lblSteeledelta = []
        self.txtSteeledelta = []
        self.lblSteelerho_s = []
        self.txtSteelerho_s = []
        self.lblSteelentype = []
        self.txtSteelentype = []
        self.lblSteelename = []
        self.txtSteelename = []
        self.lblSteelesigma_sf = []
        self.txtSteelesigma_sf = []
        self.lblSteeleepsilon_sf = []
        self.txtSteeleepsilon_sf = []
        self.steelentypeID = []
        for ef in self.towhee.get_externalfields():
            self.lblFieldType.append(wx.StaticText(self.pnExternalFields, -1, "Field Type",\
                size=(80,-1), style=wx.ALIGN_RIGHT))
            self.cboFieldType.append(wx.ComboBox(self.pnExternalFields, -1, choices=[\
                "Hard Wall",\
                "Harmonic Attractor",\
                "LJ 9-3 Wall",\
                "Hooper Umbrella",\
                "Steele Wall"],\
                style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(200,-1)))
            self.cboFieldType[-1].SetStringSelection(ef.get_fieldtype())
            self.fieldtypeID.append(self.cboFieldType[-1].GetId())
            if ef.get_fieldtype() == "Hard Wall":
                self.lblHrdEnergyType.append(wx.StaticText(self.pnExternalFields, -1, "hrd_energy_type", style=wx.ALIGN_RIGHT))
                hrdsize = self.lblHrdEnergyType[0].GetSize()
                self.lblHrdbox.append(wx.StaticText(self.pnExternalFields, -1, "hrdbox", size=hrdsize, style=wx.ALIGN_RIGHT))
                self.txtHrdbox.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_box())))
                self.lblHrdxyz.append(wx.StaticText(self.pnExternalFields, -1, "hrdxyz", size=hrdsize, style=wx.ALIGN_RIGHT))
                self.txtHrdxyz.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_xyz()))
                self.lblHrdcen.append(wx.StaticText(self.pnExternalFields, -1, "hrdcen", size=hrdsize, style=wx.ALIGN_RIGHT))
                self.txtHrdcen.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_cen()))
                self.lblHrdrad.append(wx.StaticText(self.pnExternalFields, -1, "hrdrad", size=hrdsize, style=wx.ALIGN_RIGHT))
                self.txtHrdrad.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_rad()))
                self.cboHrdEnergyType.append(wx.ComboBox(self.pnExternalFields, -1,\
                    choices=["infinite", "finite"],\
                    style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
                self.cboHrdEnergyType[-1].SetStringSelection(ef.get_energy_type())
                self.hrdenergytypeID.append(self.cboHrdEnergyType[-1].GetId())
                self.lblHrdWallEnergy.append(wx.StaticText(self.pnExternalFields, -1, "hrd_wall_energy", size=hrdsize, style=wx.ALIGN_RIGHT))
                self.txtHrdWallEnergy.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_wall_energy()))
            elif ef.get_fieldtype() == "Harmonic Attractor":
                self.lblHafnentries.append(wx.StaticText(self.pnExternalFields, -1, "hafnentries", style=wx.ALIGN_RIGHT))
                hasize = self.lblHafnentries[0].GetSize()
                self.lblHafbox.append(wx.StaticText(self.pnExternalFields, -1, "hafbox", size=hasize, style=wx.ALIGN_RIGHT))
                self.txtHafbox.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_box())))
                self.lblHafk.append(wx.StaticText(self.pnExternalFields, -1, "hafk", size=hasize, style=wx.ALIGN_RIGHT))
                self.txtHafk.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_k()))
                self.txtHafnentries.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_nentries())))
                self.hafnentriesID.append(self.txtHafnentries[-1].GetId())
                self.lblHafrefpos.append(wx.StaticText(self.pnExternalFields, -1, "hafrefpos", size=hasize, style=wx.ALIGN_RIGHT))
                self.cboHafrefpos.append(wx.ComboBox(self.pnExternalFields, -1,\
                    choices=["Global", "Initial"],\
                    style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
                self.cboHafrefpos[-1].SetStringSelection(ef.get_refpos())
                self.hafrefposID.append(self.cboHafrefpos[-1].GetId())
                self.lblHafglobxyz.append(wx.StaticText(self.pnExternalFields, -1, "hafglobxyz", size=hasize, style=wx.ALIGN_RIGHT))
                self.txtHafglobx.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_globx()))
                self.txtHafgloby.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_globy()))
                self.txtHafglobz.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_globz()))
                self.lblHafkey.append(wx.StaticText(self.pnExternalFields, -1, "hafkey", size=hasize, style=wx.ALIGN_RIGHT))
                self.cboHafkey.append(wx.ComboBox(self.pnExternalFields, -1,\
                    choices=["Element", "FFtype"],\
                    style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
                self.cboHafkey[-1].SetStringSelection(ef.get_key())
                self.hafkeyID.append(self.cboHafkey[-1].GetId())

                TlblMolec = []
                TtxtMolec = []
                for molec in ef.get_molec():
                    TlblMolec.append(wx.StaticText(self.pnExternalFields, -1, "hafmolec", size=hasize, style=wx.ALIGN_RIGHT))
                    TtxtMolec.append(wx.TextCtrl(self.pnExternalFields, -1, str(molec)))
                self.lblHafmolec.append(TlblMolec)
                self.txtHafmolec.append(TtxtMolec)

                TlblElement = []
                TtxtElement = []
                for ele in ef.get_element():
                    TlblElement.append(wx.StaticText(self.pnExternalFields, -1, "hafelement", size=hasize, style=wx.ALIGN_RIGHT))
                    TtxtElement.append(wx.TextCtrl(self.pnExternalFields, -1, ele))
                self.lblHafelement.append(TlblElement)
                self.txtHafelement.append(TtxtElement)

                TlblName = []
                TtxtName = []
                for name in ef.get_name():
                    TlblName.append(wx.StaticText(self.pnExternalFields, -1, "hafname", size=hasize, style=wx.ALIGN_RIGHT))
                    TtxtName.append(wx.TextCtrl(self.pnExternalFields, -1, name))
                self.lblHafname.append(TlblName)
                self.txtHafname.append(TtxtName)
            elif ef.get_fieldtype() == "LJ 9-3 Wall":
                self.lblLjfntypes.append(wx.StaticText(self.pnExternalFields, -1, "ljfntypes", style=wx.ALIGN_RIGHT))
                ljfsize = self.lblLjfntypes[0].GetSize()
                self.lblLjfbox.append(wx.StaticText(self.pnExternalFields, -1, "ljfbox", size=ljfsize, style=wx.ALIGN_RIGHT))
                self.txtLjfbox.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_box())))
                self.lblLjfxyz.append(wx.StaticText(self.pnExternalFields, -1, "ljfxyz", size=ljfsize, style=wx.ALIGN_RIGHT))
                self.txtLjfxyz.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_xyz()))
                self.lblLjfcen.append(wx.StaticText(self.pnExternalFields, -1, "ljfcen", size=ljfsize, style=wx.ALIGN_RIGHT))
                self.txtLjfcen.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_cen()))
                self.lblLjfdir.append(wx.StaticText(self.pnExternalFields, -1, "ljfdir", size=ljfsize, style=wx.ALIGN_RIGHT))
                self.txtLjfdir.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_dir())))
                self.lblLjfcut.append(wx.StaticText(self.pnExternalFields, -1, "ljfcut", size=ljfsize, style=wx.ALIGN_RIGHT))
                self.txtLjfcut.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_cut()))
                self.lblLjfshift.append(wx.StaticText(self.pnExternalFields, -1, "ljfshift", size=ljfsize, style=wx.ALIGN_RIGHT))
                self.rbLjfshift.append(wx.RadioBox(self.pnExternalFields, -1, "", choices=["True", "False"],\
                    majorDimension=1, style=wx.RA_SPECIFY_ROWS))
                if ef.get_shift():
                    self.rbLjfshift[-1].SetSelection(0)
                else:
                    self.rbLjfshift[-1].SetSelection(1)
                self.lblLjfrho.append(wx.StaticText(self.pnExternalFields, -1, "ljfrho", size=ljfsize, style=wx.ALIGN_RIGHT))
                self.txtLjfrho.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_rho()))
                self.txtLjfntypes.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_ntypes())))
                self.ljfntypesID.append(self.txtLjfntypes[-1].GetId())
                TlblLjfname = []
                TtxtLjfname = []
                TlblLjfsig = [] 
                TtxtLjfsig = []
                TlblLjfeps = []
                TtxtLjfeps = []
                for name in ef.get_name():
                    TlblLjfname.append(wx.StaticText(self.pnExternalFields, -1, "ljfname", size=ljfsize, style=wx.ALIGN_RIGHT))
                    TtxtLjfname.append(wx.TextCtrl(self.pnExternalFields, -1, name))
                self.lblLjfname.append(TlblLjfname)
                self.txtLjfname.append(TtxtLjfname)
                for sig in ef.get_sig():
                    TlblLjfsig.append(wx.StaticText(self.pnExternalFields, -1, "ljfsig", size=ljfsize, style=wx.ALIGN_RIGHT))
                    TtxtLjfsig.append(wx.TextCtrl(self.pnExternalFields, -1, sig))
                self.lblLjfsig.append(TlblLjfsig)
                self.txtLjfsig.append(TtxtLjfsig)
                for eps in ef.get_eps():
                    TlblLjfeps.append(wx.StaticText(self.pnExternalFields, -1, "ljfeps", size=ljfsize, style=wx.ALIGN_RIGHT))
                    TtxtLjfeps.append(wx.TextCtrl(self.pnExternalFields, -1, eps))
                self.lblLjfeps.append(TlblLjfeps)
                self.txtLjfeps.append(TtxtLjfeps)
            elif ef.get_fieldtype() == "Hooper Umbrella":
                self.lblUmbcenter.append(wx.StaticText(self.pnExternalFields, -1, "umbcenter", style=wx.ALIGN_RIGHT))
                umbsize = self.lblUmbcenter[0].GetSize()
                self.txtUmbcenter.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_center()))
                self.lblUmbbox.append(wx.StaticText(self.pnExternalFields, -1, "umbbox", size=umbsize, style=wx.ALIGN_RIGHT))
                self.txtUmbbox.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_box())))
                self.lblUmbxyz.append(wx.StaticText(self.pnExternalFields, -1, "umbxyz", size=umbsize, style=wx.ALIGN_RIGHT))
                self.txtUmbxyz.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_xyz()))
                self.lblUmba.append(wx.StaticText(self.pnExternalFields, -1, "umba", size=umbsize, style=wx.ALIGN_RIGHT))
                self.txtUmba.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_a()))
            elif ef.get_fieldtype() == "Steele Wall":
                self.lblSteelesurface.append(wx.StaticText(self.pnExternalFields, -1, "steele surface", style=wx.ALIGN_RIGHT))
                steelesize = self.lblSteelesurface[0].GetSize()
                self.txtSteelesurface.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_surface()))
                self.lblSteelebox.append(wx.StaticText(self.pnExternalFields, -1, "steele box", size=steelesize, style=wx.ALIGN_RIGHT))
                self.txtSteelebox.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_box())))
                self.lblSteelexyz.append(wx.StaticText(self.pnExternalFields, -1, "steele xyz", size=steelesize, style=wx.ALIGN_RIGHT))
                self.txtSteelexyz.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_xyz()))
                self.lblSteeledir.append(wx.StaticText(self.pnExternalFields, -1, "steele dir", size=steelesize, style=wx.ALIGN_RIGHT))
                self.txtSteeledir.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_dir())))
                self.lblSteelecutoff.append(wx.StaticText(self.pnExternalFields, -1, "steele cutoff", size=steelesize, style=wx.ALIGN_RIGHT))
                self.txtSteelecutoff.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_cutoff()))
                self.lblSteeleshift.append(wx.StaticText(self.pnExternalFields, -1, "steele shift", size=steelesize, style=wx.ALIGN_RIGHT))
                self.rbSteeleshift.append(wx.RadioBox(self.pnExternalFields, -1, "", choices=["True", "False"],\
                    majorDimension=1, style=wx.RA_SPECIFY_ROWS))
                if ef.get_shift():
                    self.rbSteeleshift[-1].SetSelection(0)
                else:
                    self.rbSteeleshift[-1].SetSelection(1)
                self.lblSteeledelta.append(wx.StaticText(self.pnExternalFields, -1, "steele delta", size=steelesize, style=wx.ALIGN_RIGHT))
                self.txtSteeledelta.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_delta()))
                self.lblSteelerho_s.append(wx.StaticText(self.pnExternalFields, -1, "steele rho_s", size=steelesize, style=wx.ALIGN_RIGHT))
                self.txtSteelerho_s.append(wx.TextCtrl(self.pnExternalFields, -1, ef.get_rho_s()))
                self.lblSteelentype.append(wx.StaticText(self.pnExternalFields, -1, "steele ntype", size=steelesize, style=wx.ALIGN_RIGHT))
                self.txtSteelentype.append(wx.TextCtrl(self.pnExternalFields, -1, str(ef.get_ntype())))
                self.steelentypeID.append(self.txtSteelentype[-1].GetId())
                TlblSteelename = []
                TtxtSteelename = []
                TlblSteelesig = [] 
                TtxtSteelesig = []
                TlblSteeleeps = []
                TtxtSteeleeps = []
                for eps in ef.get_epsilon_sf():
                    TlblSteeleeps.append(wx.StaticText(self.pnExternalFields, -1, "steele epsilon_sf", style=wx.ALIGN_RIGHT))
                    TtxtSteeleeps.append(wx.TextCtrl(self.pnExternalFields, -1, eps))
                ntypesize = TlblSteeleeps[0].GetSize()
                self.lblSteeleepsilon_sf.append(TlblSteeleeps)
                self.txtSteeleepsilon_sf.append(TtxtSteeleeps)
                for name in ef.get_name():
                    TlblSteelename.append(wx.StaticText(self.pnExternalFields, -1, "steele name", size=ntypesize, style=wx.ALIGN_RIGHT))
                    TtxtSteelename.append(wx.TextCtrl(self.pnExternalFields, -1, name))
                self.lblSteelename.append(TlblSteelename)
                self.txtSteelename.append(TtxtSteelename)
                for sigma in ef.get_sigma_sf():
                    TlblSteelesig.append(wx.StaticText(self.pnExternalFields, -1, "steele sigma_sf", size=ntypesize, style=wx.ALIGN_RIGHT))
                    TtxtSteelesig.append(wx.TextCtrl(self.pnExternalFields, -1, sigma))
                self.lblSteelesigma_sf.append(TlblSteelesig)
                self.txtSteelesigma_sf.append(TtxtSteelesig)
        #
        # Create widgets to go on Initialization tab
        #
        self.rbLinit = wx.RadioBox(self.pnInit, -1, "linit", choices=["True", "False"], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        if self.towhee.get_linit():
            self.rbLinit.SetSelection(0)
        else:
            self.rbLinit.SetSelection(1)

        self.cboInitstyle = []
        self.lblInitstyleBox = []
        self.lblInitstyleMolty = []
        for i in range(self.towhee.get_numboxes()):
            self.lblInitstyleBox.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
            T = []
            for j in range(self.towhee.get_nmolty()):
                T.append(\
                    wx.ComboBox(self.pnInit, -1, choices=[\
                    "full cbmc",\
                    "template",\
                    "coords",\
                    "nanotube",\
                    "helix",\
                    "partial cbmc"\
                    ], style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(120,-1)))
                T[j].SetStringSelection(self.towhee.get_single_initstyle(i, j))
            self.cboInitstyle.append(T)
        for i in range(self.towhee.get_nmolty()):
            self.lblInitstyleMolty.append(wx.StaticText(self.pnInit, -1, "Mol " + str(i+1), size=(120,-1), style=wx.ALIGN_CENTER))
        self.lblInitstyleSpacer = wx.StaticText(self.pnInit, -1, "", size=self.lblInitstyleBox[0].GetSize())

        self.cboInitlattice = []
        self.lblInitlatticeBox = []
        self.lblInitlatticeMolty = []
        for i in range(self.towhee.get_numboxes()):
            self.lblInitlatticeBox.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
            T = []
            for j in range(self.towhee.get_nmolty()):
                T.append(\
                    wx.ComboBox(self.pnInit, -1, choices=[\
                    "center",\
                    "none",\
                    "simple cubic"\
                    ], style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(120,-1)))
                T[j].SetStringSelection(self.towhee.get_single_initlattice(i, j))
            self.cboInitlattice.append(T)
        for i in range(self.towhee.get_nmolty()):
            self.lblInitlatticeMolty.append(wx.StaticText(self.pnInit, -1, "Mol " + str(i+1), size=(120,-1), style=wx.ALIGN_CENTER))
        self.lblInitlatticeSpacer = wx.StaticText(self.pnInit, -1, "", size=self.lblInitlatticeBox[0].GetSize())

        self.btnHelix = wx.Button(self.pnInit, -1, "Enter Helix Info") 

        self.txtInitmol = []
        self.lblInitmolBox = []
        self.lblInitmolMolty = []
        for i in range(self.towhee.get_numboxes()):
            self.lblInitmolBox.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
            T = []
            for j in range(self.towhee.get_nmolty()):
                T.append(wx.TextCtrl(self.pnInit, -1, str(towhee.get_single_initmol(i, j)), size=(40,-1)))
            self.txtInitmol.append(T)
        for i in range(self.towhee.get_nmolty()):
            self.lblInitmolMolty.append(wx.StaticText(self.pnInit, -1, "Mol " + str(i+1), size=(40,-1), style=wx.ALIGN_CENTER))
        self.lblInitmolSpacer = wx.StaticText(self.pnInit, -1, "", size=self.lblInitmolBox[0].GetSize())

        self.lblInitboxtype = wx.StaticText(self.pnInit, -1, "Initboxtype", style=wx.ALIGN_RIGHT)
        self.cboInitboxtype = wx.ComboBox(self.pnInit, -1, choices=[\
            "dimensions",\
            "number density",\
            "unit cell"\
            ], style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(150,-1))
        self.cboInitboxtype.SetStringSelection(towhee.get_initboxtype())

        self.txtHmatrix = []
        for hm in self.towhee.get_hmatrix():
            for h in hm.get_row1():
                self.txtHmatrix.append(wx.TextCtrl(self.pnInit, -1, h, size=(60,-1)))
            for h in hm.get_row2():
                self.txtHmatrix.append(wx.TextCtrl(self.pnInit, -1, h, size=(60,-1)))
            for h in hm.get_row3():
                self.txtHmatrix.append(wx.TextCtrl(self.pnInit, -1, h, size=(60,-1)))

        self.lblBoxNumberDensity = []
        self.txtBoxNumberDensity = []
        for i in range(self.towhee.get_numboxes()):
            self.lblBoxNumberDensity.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1)))
            self.txtBoxNumberDensity.append(wx.TextCtrl(self.pnInit, -1,\
                self.towhee.get_single_box_number_density(i), size=(40,-1)))

        self.lblInix = wx.StaticText(self.pnInit, -1, "inix", size=(60,-1), style=wx.ALIGN_CENTER)
        self.lblIniy = wx.StaticText(self.pnInit, -1, "iniy", size=(60,-1), style=wx.ALIGN_CENTER)
        self.lblIniz = wx.StaticText(self.pnInit, -1, "iniz", size=(60,-1), style=wx.ALIGN_CENTER)
        self.lblInixyz = []
        self.txtInixyz = []
        for i in range(self.towhee.get_numboxes()):
            self.lblInixyz.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
            self.txtInixyz.append(wx.TextCtrl(self.pnInit, -1, str(towhee.get_single_inix(i)), size=(60,-1)))
            self.txtInixyz.append(wx.TextCtrl(self.pnInit, -1, str(towhee.get_single_iniy(i)), size=(60,-1)))
            self.txtInixyz.append(wx.TextCtrl(self.pnInit, -1, str(towhee.get_single_iniz(i)), size=(60,-1)))
        spacersize = self.lblInixyz[0].GetSize()
        self.lblInixyzSpacer = wx.StaticText(self.pnInit, -1, "", size=spacersize)
        #
        # Create widgets to go on Monte Carlo Moves tab
        #
        mcm = self.towhee.get_cbsbmrm()
        self.lblPm1boxcbswap = wx.StaticText(self.pnMCM, -1, "pm1boxcbswap", style=wx.ALIGN_RIGHT)
        mcmsize = self.lblPm1boxcbswap.GetSize()
        self.txtPm1boxcbswap = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnCBSBMRM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_ivm()
        self.lblPmvol = wx.StaticText(self.pnMCM, -1, "pmvol", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmvol = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnIVM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_avm()
        self.lblPmcell = wx.StaticText(self.pnMCM, -1, "pmcell", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmcell = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnAVM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_rb2bmtm()
        self.lblPm2boxrbswap = wx.StaticText(self.pnMCM, -1, "pm2boxrbswap", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPm2boxrbswap = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnRB2BTM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_cbgcidm()
        self.lblPmuvtcbswap = wx.StaticText(self.pnMCM, -1, "pmuvtcbswap", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmuvtcbswap = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnGCID = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_cb2bmtm()
        self.lblPm2boxcbswap = wx.StaticText(self.pnMCM, -1, "pm2boxcbswap", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPm2boxcbswap = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnCB2BTM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_avbmt1()
        self.lblPmavb1 = wx.StaticText(self.pnMCM, -1, "pmavb1", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmavb1 = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnAVBMT1 = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_avbmt2()
        self.lblPmavb2 = wx.StaticText(self.pnMCM, -1, "pmavb2", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmavb2 = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnAVBMT2 = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_avbmt3()
        self.lblPmavb3 = wx.StaticText(self.pnMCM, -1, "pmavb3", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmavb3 = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnAVBMT3 = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_cbpmr()
        self.lblPmcb = wx.StaticText(self.pnMCM, -1, "pmcb", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmcb = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnCBPMR = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_cbpbr()
        self.lblPmback = wx.StaticText(self.pnMCM, -1, "pmback", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmback = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnCBPBR = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_tpm()
        self.lblPmpivot = wx.StaticText(self.pnMCM, -1, "pmpivot", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmpivot = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnTPM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_crnmoanpb()
        self.lblPmconrot = wx.StaticText(self.pnMCM, -1, "pmconrot", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmconrot = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnCRMNPB = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_crnmoa3pbs()
        self.lblPmcrback = wx.StaticText(self.pnMCM, -1, "pmcrback", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmcrback = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnCRM3PBS = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_psm()
        self.lblPmplane = wx.StaticText(self.pnMCM, -1, "pmplane", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmplane = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnPSM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_rsm()
        self.lblPmrow = wx.StaticText(self.pnMCM, -1, "pmrow", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmrow = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnRSM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_isatm()
        self.lblPmtraat = wx.StaticText(self.pnMCM, -1, "pmtraat", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmtraat = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnISATM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_cofmmtm()
        self.lblPmtracm = wx.StaticText(self.pnMCM, -1, "pmtracm", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmtracm = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnCMMTM = wx.Button(self.pnMCM, -1, "Move Info")
        mcm = self.towhee.get_ratcomm()
        self.lblPmrotate = wx.StaticText(self.pnMCM, -1, "pmrotate", size=mcmsize, style=wx.ALIGN_RIGHT)
        self.txtPmrotate = wx.TextCtrl(self.pnMCM, -1, mcm.get_move_probability())
        self.btnRCMM = wx.Button(self.pnMCM, -1, "Move Info")
        #
        # Create widgets to go on CBMC Information tab
        #
        self.lblBend = wx.StaticText(self.pnCBMC, -1, "bend_cbstyle", style=wx.ALIGN_RIGHT)
        cbmc1size = self.lblBend.GetSize()
        self.cboBend = wx.ComboBox(self.pnCBMC, -1, choices=["0", "1"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1))
        self.cboBend.SetStringSelection(str(towhee.get_bend_cbstyle()))
        self.lblTor = wx.StaticText(self.pnCBMC, -1, "tor_cbstyle", size=cbmc1size, style=wx.ALIGN_RIGHT)
        self.cboTor = wx.ComboBox(self.pnCBMC, -1, choices=["0", "1"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1))
        self.cboTor.SetStringSelection(str(towhee.get_tor_cbstyle()))
        self.lblVib = wx.StaticText(self.pnCBMC, -1, "vib_cbstyle", size=cbmc1size, style=wx.ALIGN_RIGHT)
        self.cboVib = wx.ComboBox(self.pnCBMC, -1, choices=["0", "1"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1))
        self.cboVib.SetStringSelection(str(towhee.get_vib_cbstyle()))
        self.lblSdevtor = wx.StaticText(self.pnCBMC, -1, "sdevtor", size=cbmc1size, style=wx.ALIGN_RIGHT)
        self.txtSdevtor = wx.TextCtrl(self.pnCBMC, -1, self.towhee.get_sdevtor())
        self.lblSdevbena = wx.StaticText(self.pnCBMC, -1, "sdevbena", size=cbmc1size, style=wx.ALIGN_RIGHT)
        self.txtSdevbena = wx.TextCtrl(self.pnCBMC, -1, self.towhee.get_sdevbena())
        self.lblSdevbenb = wx.StaticText(self.pnCBMC, -1, "sdevbenb", size=cbmc1size, style=wx.ALIGN_RIGHT)
        self.txtSdevbenb = wx.TextCtrl(self.pnCBMC, -1, self.towhee.get_sdevbenb())
        self.lblSdevvib = wx.StaticText(self.pnCBMC, -1, "sdevvib", size=cbmc1size, style=wx.ALIGN_RIGHT)
        self.txtSdevvib = wx.TextCtrl(self.pnCBMC, -1, self.towhee.get_sdevvib())
        self.lblVibrang = wx.StaticText(self.pnCBMC, -1, "vibrang", size=cbmc1size, style=wx.ALIGN_RIGHT)
        vibrang = self.towhee.get_vibrang()
        self.txtVibrang1 = wx.TextCtrl(self.pnCBMC, -1, vibrang[0])
        self.txtVibrang2 = wx.TextCtrl(self.pnCBMC, -1, vibrang[1])
        self.lblCdform = wx.StaticText(self.pnCBMC, -1, "cdform", size=cbmc1size, style=wx.ALIGN_RIGHT)
        self.txtCdform = wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_cdform()))
        self.lblNch_tor_in_con = wx.StaticText(self.pnCBMC, -1, "nch_tor_in_con", style=wx.ALIGN_RIGHT)
        nchsize = lblNch_tor_in_con = self.lblNch_tor_in_con.GetSize()
        self.lblNch_nb_one = wx.StaticText(self.pnCBMC, -1, "nch_nb_one", size=nchsize, style=wx.ALIGN_RIGHT)
        self.lblNch_nb = wx.StaticText(self.pnCBMC, -1, "nch_nb", size=nchsize, style=wx.ALIGN_RIGHT)
        self.lblNch_tor_out = wx.StaticText(self.pnCBMC, -1, "nch_tor_out", size=nchsize, style=wx.ALIGN_RIGHT)
        self.lblNch_tor_in = wx.StaticText(self.pnCBMC, -1, "nch_tor_in", size=nchsize, style=wx.ALIGN_RIGHT)
        self.lblNch_bend_a = wx.StaticText(self.pnCBMC, -1, "nch_bend_a", size=nchsize, style=wx.ALIGN_RIGHT)
        self.lblNch_bend_b = wx.StaticText(self.pnCBMC, -1, "nch_bend_b", size=nchsize, style=wx.ALIGN_RIGHT)
        self.lblNch_vib = wx.StaticText(self.pnCBMC, -1, "nch_vib", size=nchsize, style=wx.ALIGN_RIGHT)
        self.txtNch_nb_one = []
        self.txtNch_nb = []
        self.txtNch_tor_out = []
        self.txtNch_tor_in = []
        self.txtNch_tor_in_con = []
        self.txtNch_bend_a = []
        self.txtNch_bend_b = []
        self.txtNch_vib = []
        for i in range(self.towhee.get_nmolty()):
            self.txtNch_nb_one.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_nb_one(i)), size=(50,-1)))
            self.txtNch_nb.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_nb(i)), size=(50,-1)))
            self.txtNch_tor_out.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_tor_out(i)), size=(50,-1)))
            self.txtNch_tor_in.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_tor_in(i)), size=(50,-1)))
            self.txtNch_tor_in_con.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_tor_in_con(i)), size=(50,-1)))
            self.txtNch_bend_a.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_bend_a(i)), size=(50,-1)))
            self.txtNch_bend_b.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_bend_b(i)), size=(50,-1)))
            self.txtNch_vib.append(wx.TextCtrl(self.pnCBMC, -1, str(self.towhee.get_single_nch_vib(i)), size=(50,-1)))
        #
        # Create widgets to go on Inputs tab
        #
        self.lblL1 = wx.StaticText(self.pnInputs, -1, "Molecule Number")
        self.lblL2 = wx.StaticText(self.pnInputs, -1, "inpstyle")
        self.lblL3 = wx.StaticText(self.pnInputs, -1, "nunit")
        self.lblL4 = wx.StaticText(self.pnInputs, -1, "nmaxcbmc")
        mnsize = self.lblL1.GetSize()
        inpsize = self.lblL2.GetSize()
        nunitsize = self.lblL3.GetSize()
        nmaxsize = self.lblL4.GetSize()
        self.lblM = []
        self.cboInpstyle = []
        self.txtNunit = []
        self.txtNmaxcbmc = []
        self.btnM = []
        self.btnIDs = []
        self.input_error = []
        for i in range(self.towhee.get_nmolty()):
            self.input_error.append(False)
            self.lblM.append(wx.StaticText(self.pnInputs, -1, "Molecule " + str(i+1), size=mnsize))
            input = self.towhee.get_single_input(i)
            self.cboInpstyle.append(wx.ComboBox(self.pnInputs, -1, choices=["0", "1", "2", "3", "4"],\
                style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(inpsize[0],-1)))
            self.cboInpstyle[-1].SetSelection(input.get_inpstyle())
            self.txtNunit.append(wx.TextCtrl(self.pnInputs, -1, str(input.get_nunit()), size=(nunitsize[0], -1)))
            self.txtNmaxcbmc.append(wx.TextCtrl(self.pnInputs, -1, str(input.get_nmaxcbmc()), size=(nmaxsize[0], -1)))
            self.btnM.append(wx.Button(self.pnInputs, -1, "Molecule Info"))
            self.btnIDs.append(self.btnM[i].GetId())
        #
        # Main Buttons
        #
        self.btnSave = wx.Button(self, -1, "Save")
        self.btnCancel = wx.Button(self, -1, "Cancel")
        #
        # If towhee_input was created from selecting new from the File Menu, the input Nanotube
        # isn't complete... set self.input_error[0] to True so they are forced to put in data.
        # To check for this, check if self.towhee.get_filename() is "" because I don't set that
        # value if they create the file from scratch
        #
        if self.towhee.get_single_ff_filename(0) == "":
            self.input_error[0] = True

        self.__set_properties()
        self.__do_layout()
        self.__setup_logic()
        self.DynamicUpdate_RI()
        self.DynamicUpdate_FF()
        self.DynamicUpdate_MCM()
        self.DynamicUpdate_CBMC()
        self.InitboxtypeChanged()
        self.Refresh()
        self.Center()
        return

    def __set_properties(self):
        self.SetTitle("Towhee File Editor")
        self.SetSize((1000, 600))
        #
        # Set Scroll Rates
        #
        self.pnBasic.SetScrollRate(10,10)
        self.pnRunInfo.SetScrollRate(50,50)
        self.pnFF.SetScrollRate(10,10)
        self.pnExternalFields.SetScrollRate(10, 50)
        self.pnInit.SetScrollRate(50,50)
        self.pnMCM.SetScrollRate(00, 50)
        self.pnCBMC.SetScrollRate(10,10)
        self.pnInputs.SetScrollRate(0, 50)
        #
        # Hide Fields tab if there is nothing to show
        #
        if self.towhee.get_nfield() == 0:
            self.pnExternalFields.Hide()
        return

    def __do_layout(self):
        #
        # Create all the sizers for stuff that will always be
        # there - Wow, there's a lot
        #
        # Main sizer for everything
        #
        self.szrTowheeEditor = wx.BoxSizer(wx.VERTICAL)
        #
        # Sizers for Inputs
        #
        self.szrInputs = wx.BoxSizer(wx.VERTICAL)
        self.szrData = []
        for i in range(self.towhee.get_nmolty()):
            self.szrData.append(wx.BoxSizer(wx.HORIZONTAL))
        self.szrLabels = wx.BoxSizer(wx.HORIZONTAL)
        #
        # Sizers for CBMC Information
        #
        self.szrCBMC = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCBMCc2rows = wx.BoxSizer(wx.VERTICAL)
        self.szrNch_vib = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNch_bend_b = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNch_bend_a = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNch_tor_in_con = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNch_tor_in = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNch_tor_out = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNch_nb = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNch_nb_one = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCBMCc1rows = wx.BoxSizer(wx.VERTICAL)
        self.szrCdform = wx.BoxSizer(wx.HORIZONTAL)
        self.szrVibrang = wx.BoxSizer(wx.HORIZONTAL)
        self.szrSdevvib = wx.BoxSizer(wx.HORIZONTAL)
        self.szrSdevbenb = wx.BoxSizer(wx.HORIZONTAL)
        self.szrSdevbena = wx.BoxSizer(wx.HORIZONTAL)
        self.szrSdevtor = wx.BoxSizer(wx.HORIZONTAL)
        self.szrVib = wx.BoxSizer(wx.HORIZONTAL)
        self.szrBend = wx.BoxSizer(wx.HORIZONTAL)
        self.szrTor = wx.BoxSizer(wx.HORIZONTAL)
        #
        # Sizers for Monte Carlo Moves
        #
        self.szrMCM = wx.BoxSizer(wx.VERTICAL)
        self.szrRCMM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Rotation About The Center-of-Mass Move"), wx.HORIZONTAL)
        self.szrCMMTM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Center-of-Mass Molecule Translation Move"), wx.HORIZONTAL)
        self.szrISATM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Intramolecular Single Atom Translation Move"), wx.HORIZONTAL)
        self.szrRSM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Row Shift Move"), wx.HORIZONTAL)
        self.szrPSM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Plane Shift Move"), wx.HORIZONTAL)
        self.szrCRM3PBS = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Concerted Rotation Move over a 3 Peptides Backbone Sequence"), wx.HORIZONTAL)
        self.szrCRMNPB = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Concerted Rotation Move on a Non-Peptide Backbone"), wx.HORIZONTAL)
        self.szrTPM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Torsional Pivot Move"), wx.HORIZONTAL)
        self.szrCBPBR = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Configurational-Bias Protein Backbone Regrowth"), wx.HORIZONTAL)
        self.szrCBPMR = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Configurational-Bias Partial Molecule Regrowth"), wx.HORIZONTAL)
        self.szrAVBMT3 = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Aggregation Volume Bias Move Type 3"), wx.HORIZONTAL)
        self.szrAVBMT2 = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Aggregation Volume Bias Move Type 2"), wx.HORIZONTAL)
        self.szrAVBMT1 = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Aggregation Volume Bias Move Type 1"), wx.HORIZONTAL)
        self.szrCB2BTM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Configurational-bias 2 Box Molecule Transfer Move"), wx.HORIZONTAL)
        self.szrRB2BTM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Rotational-bias 2 Box Molecule Transfer Move"), wx.HORIZONTAL)
        self.szrCBSBMRM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Configurational-bias Single Box Molecule Reinsertion Move"), wx.HORIZONTAL)
        self.szrGCID = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Configurational-bias Grand-Canonical Insertion/Deletion Move"), wx.HORIZONTAL)
        self.szrAVM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Anisotropic Volume Move"), wx.HORIZONTAL)
        self.szrIVM = wx.StaticBoxSizer(wx.StaticBox(self.pnMCM, -1, "Isotropic Volume Move"), wx.HORIZONTAL)
        #
        # Sizers for Initialization
        #
        self.szrInit = wx.BoxSizer(wx.HORIZONTAL)
        self.szrInitC1 = wx.BoxSizer(wx.VERTICAL)
        self.szrInitC2 = wx.BoxSizer(wx.VERTICAL)
        self.szrInitmol = wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Initmol"), wx.VERTICAL)
        self.szrInitstyle = wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Initstyle"), wx.VERTICAL)
        self.szrInitlattice = wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Initlattice"), wx.VERTICAL)
        self.szrInitmolValues = []
        self.szrInitstyleValues = []
        self.szrInitlatticeValues = []
        for i in range(self.towhee.get_numboxes()+1):
            self.szrInitmolValues.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrInitstyleValues.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrInitlatticeValues.append(wx.BoxSizer(wx.HORIZONTAL))
        self.szrInitboxtype = wx.BoxSizer(wx.HORIZONTAL)
        self.szrHmatrix = wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Hmatrix"), wx.VERTICAL)
        self.szrHmatrixBox = []
        for i in range(self.towhee.get_numboxes()):
            self.szrHmatrixBox.append(wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Simulation Box " + str(i+1)), wx.VERTICAL))
        self.szrHmatrixRows = []
        for i in range(self.towhee.get_numboxes()*3):
            self.szrHmatrixRows.append(wx.BoxSizer(wx.HORIZONTAL))
        self.szrBoxNumberDensity = wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Box Number Density"), wx.VERTICAL)
        self.szrBoxNumberDensityValues = []
        for i in range(self.towhee.get_numboxes()):
            self.szrBoxNumberDensityValues.append(wx.BoxSizer(wx.HORIZONTAL))
        self.szrInixyz = wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Inix, Iniy, Iniz"), wx.VERTICAL)
        self.szrInixyzValues = []
        for i in range(self.towhee.get_numboxes()+1):
            self.szrInixyzValues.append(wx.BoxSizer(wx.HORIZONTAL))
        #
        # Sizers for External Fields
        #
        self.szrExternalFieldList = wx.BoxSizer(wx.VERTICAL)
        self.szrExternalField = []
        self.szrFieldType = []
        self.szrField = []
        self.szrHrdbox = []
        self.szrHrdxyz = []
        self.szrHrdcen = []
        self.szrHrdrad = []
        self.szrHrdEnergyType = []
        self.szrHrdWallEnergy = []
        self.szrHafbox = []
        self.szrHafk = []
        self.szrHafnentries = []
        self.szrHafrefpos = []
        self.szrHafglobxyz = []
        self.szrHafkey = []
        self.szrHafkeyList = []
        self.szrHafkeyValues = []
        self.szrHafmolec = []
        self.szrHafelement = []
        self.szrHafname = []
        self.szrLjfbox = []
        self.szrLjfxyz = []
        self.szrLjfcen = []
        self.szrLjfdir = []
        self.szrLjfcut = []
        self.szrLjfshift = []
        self.szrLjfrho = []
        self.szrLjfntypes = []
        self.szrLjfntypesList = []
        self.szrLjfntypesValues = []
        self.szrLjfname = []
        self.szrLjfsig = []
        self.szrLjfeps = []
        self.szrUmbbox = []
        self.szrUmbxyz = []
        self.szrUmbcenter = []
        self.szrUmba = []
        self.szrSteelebox = []
        self.szrSteelexyz = []
        self.szrSteelesurface = []
        self.szrSteeledir = []
        self.szrSteelecutoff = []
        self.szrSteeleshift = []
        self.szrSteeledelta = []
        self.szrSteelerho_s = []
        self.szrSteelentype = []
        self.szrSteelentypeList = []
        self.szrSteelentypeValues = []
        self.szrSteelename = []
        self.szrSteelesigma_sf = []
        self.szrSteeleepsilon_sf = []
        for i in range(self.towhee.get_nfield()):
            self.szrExternalField.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                "External Field " + str(i+1)), wx.VERTICAL))
            self.szrFieldType.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrField.append(wx.BoxSizer(wx.VERTICAL))
            ef = self.towhee.get_single_externalfield(i)
            if ef.get_fieldtype() == "Hard Wall":
                self.szrHrdbox.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHrdxyz.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHrdcen.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHrdrad.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHrdEnergyType.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHrdWallEnergy.append(wx.BoxSizer(wx.HORIZONTAL))
            elif ef.get_fieldtype() == "Harmonic Attractor":
                self.szrHafbox.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHafk.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHafnentries.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHafrefpos.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHafglobxyz.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHafkey.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHafkeyList.append(wx.BoxSizer(wx.VERTICAL))
                TszrKeyValues = []
                TszrMolec = []
                TszrElement = []
                TszrName = []
                for j in range(ef.get_nentries()):
                    TszrKeyValues.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                        "Entry " + str(j+1)), wx.VERTICAL))
                    TszrMolec.append(wx.BoxSizer(wx.HORIZONTAL))
                    TszrElement.append(wx.BoxSizer(wx.HORIZONTAL))
                    TszrName.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrHafkeyValues.append(TszrKeyValues)
                self.szrHafmolec.append(TszrMolec)
                self.szrHafelement.append(TszrElement)
                self.szrHafname.append(TszrName)
            elif ef.get_fieldtype() == "LJ 9-3 Wall":
                self.szrLjfbox.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfxyz.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfcen.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfdir.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfcut.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfshift.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfrho.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfntypes.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfntypesList.append(wx.BoxSizer(wx.VERTICAL))
                TszrLjfntypesValues = []
                TszrLjfname = []
                TszrLjfsig = []
                TszrLjfeps = []
                for j in range(ef.get_ntypes()):
                    TszrLjfntypesValues.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                        "ljfntype " + str(j+1)), wx.VERTICAL))
                    TszrLjfname.append(wx.BoxSizer(wx.HORIZONTAL))
                    TszrLjfsig.append(wx.BoxSizer(wx.HORIZONTAL))
                    TszrLjfeps.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrLjfntypesValues.append(TszrLjfntypesValues)
                self.szrLjfname.append(TszrLjfname)
                self.szrLjfsig.append(TszrLjfsig)
                self.szrLjfeps.append(TszrLjfeps)
            elif ef.get_fieldtype() == "Hooper Umbrella":
                self.szrUmbbox.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrUmbxyz.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrUmbcenter.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrUmba.append(wx.BoxSizer(wx.HORIZONTAL))
            elif ef.get_fieldtype() == "Steele Wall":
                self.szrSteelebox.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteelexyz.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteelesurface.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteeledir.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteelecutoff.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteeleshift.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteeledelta.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteelerho_s.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteelentype.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteelentypeList.append(wx.BoxSizer(wx.VERTICAL))
                TszrSteelentypeValues = []
                TszrSteelename = []
                TszrSteelesig = []
                TszrSteeleeps = []
                for j in range(ef.get_ntype()):
                    TszrSteelentypeValues.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                        "steele ntype " + str(j+1)), wx.VERTICAL))
                    TszrSteelename.append(wx.BoxSizer(wx.HORIZONTAL))
                    TszrSteelesig.append(wx.BoxSizer(wx.HORIZONTAL))
                    TszrSteeleeps.append(wx.BoxSizer(wx.HORIZONTAL))
                self.szrSteelentypeValues.append(TszrSteelentypeValues)
                self.szrSteelename.append(TszrSteelename)
                self.szrSteelesigma_sf.append(TszrSteelesig)
                self.szrSteeleepsilon_sf.append(TszrSteeleeps)
        #
        # Sizers for Force Field
        #
        self.szrFFMainColumns = wx.BoxSizer(wx.HORIZONTAL)
        self.szrFFc1rows = wx.BoxSizer(wx.VERTICAL)
        self.szrNfield = wx.BoxSizer(wx.HORIZONTAL)
        self.szrDielectric = wx.BoxSizer(wx.HORIZONTAL)
        self.szrEwald_prec = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRcelect = wx.BoxSizer(wx.HORIZONTAL)
        self.szrKmax = wx.BoxSizer(wx.HORIZONTAL)
        self.szrKalp = wx.BoxSizer(wx.HORIZONTAL)
        self.szrFf_filename = wx.BoxSizer(wx.HORIZONTAL)
        self.szrFilenames = wx.BoxSizer(wx.VERTICAL)
        self.szrCoulombstyle = wx.BoxSizer(wx.HORIZONTAL)
        self.szrFfnumber = wx.BoxSizer(wx.HORIZONTAL)
        self.szrFFc2rows = wx.BoxSizer(wx.VERTICAL)
        self.szrInterpolatestyle = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRadialPressureDelta = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRcutin = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRcut = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRmin = wx.BoxSizer(wx.HORIZONTAL)
        self.szrLtailc = wx.BoxSizer(wx.HORIZONTAL)
        self.szrLshift = wx.BoxSizer(wx.HORIZONTAL)
        self.szrClassicalMixrule = wx.BoxSizer(wx.HORIZONTAL)
        self.szrClassicalPotential = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCmixRescalingStyle = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCmixLambda = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCmixNpair = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCmixPairList = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCmixPairListData = wx.BoxSizer(wx.VERTICAL)
        self.szrPotentialStyle = wx.BoxSizer(wx.HORIZONTAL)
        self.szrIsolvtyp = wx.BoxSizer(wx.HORIZONTAL)
        #
        # Sizers for Run Information
        #
        self.szrRIMainColumns = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRIc2rows = wx.BoxSizer(wx.VERTICAL)
        self.szrEmpty = wx.BoxSizer(wx.HORIZONTAL)
        self.szrHistdumpfreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrHistcalcfreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrLouthist = wx.BoxSizer(wx.HORIZONTAL)
        self.szrBlocksize = wx.BoxSizer(wx.HORIZONTAL)
        self.szrVolmaxfreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrChempotperstep = wx.BoxSizer(wx.HORIZONTAL)
        self.szrChempotperstepData = wx.BoxSizer(wx.VERTICAL)
        self.szrTrmaxdispfreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrPressurefreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrBackupfreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrMoviefreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrPrintfreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRunoutput = wx.BoxSizer(wx.HORIZONTAL)
        self.szrRIc1rows = wx.BoxSizer(wx.VERTICAL)
        self.szrMintol = wx.BoxSizer(wx.HORIZONTAL)
        self.szrOptstyle = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNstep = wx.BoxSizer(wx.HORIZONTAL)
        self.szrStepstyle = wx.BoxSizer(wx.HORIZONTAL)
        self.szrLoutlammps = wx.BoxSizer(wx.HORIZONTAL)
        self.szrLoutdft = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNmolectype = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNmolectypeData = wx.BoxSizer(wx.VERTICAL)
        self.szrPdbOutputFreq = wx.BoxSizer(wx.HORIZONTAL)
        self.szrChempot = wx.BoxSizer(wx.HORIZONTAL)
        self.szrChempotData = wx.BoxSizer(wx.VERTICAL)
        self.szrPressure = wx.BoxSizer(wx.HORIZONTAL)
        self.szrTemperature = wx.BoxSizer(wx.HORIZONTAL)
        #
        # Sizers on Basic tab
        #
        self.szrRandomseed = wx.BoxSizer(wx.HORIZONTAL)
        self.szrEnsemble = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNmolty = wx.BoxSizer(wx.HORIZONTAL)
        self.szrNumboxes = wx.BoxSizer(wx.HORIZONTAL)
        self.szrBasicOpts = wx.BoxSizer(wx.VERTICAL)
        #
        # Layout Basic tab
        #
        self.szrRandomseed.Add(self.lblRandomseed, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRandomseed.Add(self.txtRandomseed, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrEnsemble.Add(self.lblEnsemble, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrEnsemble.Add(self.cboEnsemble, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNmolty.Add(self.lblNmolty, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNmolty.Add(self.txtNmolty, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNumboxes.Add(self.lblNumboxes, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNumboxes.Add(self.txtNumboxes, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrBasicOpts.Add(self.szrRandomseed, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 15)
        self.szrBasicOpts.Add(self.szrEnsemble, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 15)
        self.szrBasicOpts.Add(self.szrNmolty, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 15)
        self.szrBasicOpts.Add(self.szrNumboxes, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 15)
        self.pnBasic.SetAutoLayout(1)
        self.pnBasic.SetSizer(self.szrBasicOpts)
        self.szrBasicOpts.Fit(self.pnBasic)
        self.szrBasicOpts.SetSizeHints(self.pnBasic)
        #
        # Layout Run Information tab
        #
        self.szrPdbOutputFreq.Add(self.lblPdbOutputFreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPdbOutputFreq.Add(self.txtPdbOutputFreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLoutdft.Add(self.lblLoutdft, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLoutdft.Add(self.rbLoutdft, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLoutlammps.Add(self.lblLoutlammps, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLoutlammps.Add(self.rbLoutlammps, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrTemperature.Add(self.lblTemperature, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrTemperature.Add(self.txtTemperature, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPressure.Add(self.lblPressure, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPressure.Add(self.txtPressure, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrChempot.Add(self.lblChempot, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        for i in self.txtChempot:
            self.szrChempotData.Add(i, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrChempot.Add(self.szrChempotData, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        self.szrNmolectype.Add(self.lblnmolectype, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        for i in self.txtNmolectype:
            self.szrNmolectypeData.Add(i, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrNmolectype.Add(self.szrNmolectypeData, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        self.szrStepstyle.Add(self.lblStepstyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrStepstyle.Add(self.cboStepstyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNstep.Add(self.lblNstep, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNstep.Add(self.txtNstep, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrOptstyle.Add(self.lblOptstyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrOptstyle.Add(self.txtOptstyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrMintol.Add(self.lblMintol, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrMintol.Add(self.txtMintol, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRunoutput.Add(self.lblRunoutput, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRunoutput.Add(self.cboRunoutput, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPrintfreq.Add(self.lblPrintfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPrintfreq.Add(self.txtPrintfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrMoviefreq.Add(self.lblMoviefreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrMoviefreq.Add(self.txtMoviefreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrBackupfreq.Add(self.lblBackupfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrBackupfreq.Add(self.txtBackupfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPressurefreq.Add(self.lblPressurefreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPressurefreq.Add(self.txtPressurefreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrTrmaxdispfreq.Add(self.lblTrmaxdispfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrTrmaxdispfreq.Add(self.txtTrmaxdispfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrVolmaxfreq.Add(self.lblVolmaxdispfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrVolmaxfreq.Add(self.txtVolmaxdispfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrChempotperstep.Add(self.lblChempotperstep, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        for i in self.txtChempotperstep:
            self.szrChempotperstepData.Add(i, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrChempotperstep.Add(self.szrChempotperstepData, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        self.szrBlocksize.Add(self.lblBlocksize, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrBlocksize.Add(self.txtBlocksize, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLouthist.Add(self.lblLouthist, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLouthist.Add(self.rbLouthist, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrHistcalcfreq.Add(self.lblHistcalcfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrHistcalcfreq.Add(self.txtHistcalcfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrHistdumpfreq.Add(self.lblHistdumpfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrHistdumpfreq.Add(self.txtHistdumpfreq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrPdbOutputFreq, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrLoutdft, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrLoutlammps, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrTemperature, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrPressure, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrChempot, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrNmolectype, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrStepstyle, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrNstep, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrOptstyle, 0, wx.ALL, 5)
        self.szrRIc1rows.Add(self.szrMintol, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrRunoutput, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrPrintfreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrMoviefreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrBackupfreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrPressurefreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrTrmaxdispfreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrVolmaxfreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrChempotperstep, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrBlocksize, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrLouthist, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrHistcalcfreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrHistdumpfreq, 0, wx.ALL, 5)
        self.szrRIc2rows.Add(self.szrEmpty, 0, wx.ALL, 5)
        self.szrRIMainColumns.Add(self.szrRIc1rows, 1, wx.ALL, 15)
        self.szrRIMainColumns.Add(self.szrRIc2rows, 1, wx.ALL, 15)
        self.pnRunInfo.SetAutoLayout(1)
        self.pnRunInfo.SetSizer(self.szrRIMainColumns)
        self.szrRIMainColumns.Fit(self.pnRunInfo)
        self.szrRIMainColumns.SetSizeHints(self.pnRunInfo)
        #
        # Layout Force Field tab
        #
        self.szrPotentialStyle.Add(self.lblPotentialStyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrPotentialStyle.Add(self.cboPotentialStyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrIsolvtyp.Add(self.lblIsolvtype, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrIsolvtyp.Add(self.txtIsolvtype, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrClassicalPotential.Add(self.lblClassicalPotential, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrClassicalPotential.Add(self.cboClassicalPotential, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrClassicalMixrule.Add(self.lblClassicalMixrule, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrClassicalMixrule.Add(self.cboClassicalMixrule, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCmixRescalingStyle.Add(self.lblCmixRescalingStyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCmixRescalingStyle.Add(self.cboCmixRescalingStyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCmixLambda.Add(self.lblCmixLambda, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCmixLambda.Add(self.txtCmixLambda, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCmixNpair.Add(self.lblCmixNpair, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCmixNpair.Add(self.txtCmixNpair, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCmixPairList.Add(self.lblCmixPairList, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        for pld in self.txtCmixPairList:
            self.szrCmixPairListData.Add(pld, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCmixPairList.Add(self.szrCmixPairListData, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        self.szrLshift.Add(self.lblLshift, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLshift.Add(self.rbLshift, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLtailc.Add(self.lblLtailc, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrLtailc.Add(self.rbLtailc, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRmin.Add(self.lblRmin, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRmin.Add(self.txtRmin, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRcut.Add(self.lblRcut, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRcut.Add(self.txtRcut, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRcutin.Add(self.lblRcutin, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRcutin.Add(self.txtRcutin, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrInterpolatestyle.Add(self.lblInterpolatestyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrInterpolatestyle.Add(self.txtInterpolatestyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRadialPressureDelta.Add(self.lblRadialPressureDelta, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRadialPressureDelta.Add(self.txtRadialPressureDelta, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrFfnumber.Add(self.lblFfnumber, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrFfnumber.Add(self.txtFfnumber, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrFf_filename.Add(self.lblFf_filename, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        for i in self.txtFf_filename:
            self.szrFilenames.Add(i, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrFf_filename.Add(self.szrFilenames, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        self.szrCoulombstyle.Add(self.lblCoulombstyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCoulombstyle.Add(self.cboCoulombstyle, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrKalp.Add(self.lblKalp, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrKalp.Add(self.txtKalp, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrKmax.Add(self.lblKmax, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrKmax.Add(self.txtKmax, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrEwald_prec.Add(self.lblEwald_prec, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrEwald_prec.Add(self.txtEwald_prec, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRcelect.Add(self.lblRcelect, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrRcelect.Add(self.txtRcelect, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrDielectric.Add(self.lblDielectric, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrDielectric.Add(self.txtDielectric, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNfield.Add(self.lblNfield, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNfield.Add(self.txtNfield, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrPotentialStyle, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrIsolvtyp, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrClassicalPotential, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrClassicalMixrule, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrCmixRescalingStyle, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrCmixLambda, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrCmixNpair, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrCmixPairList, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrLshift, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrLtailc, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrRmin, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrRcut, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrRcutin, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrInterpolatestyle, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc1rows.Add(self.szrRadialPressureDelta, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrFfnumber, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrFf_filename, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrCoulombstyle, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrKalp, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrKmax, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrEwald_prec, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrRcelect, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrDielectric, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFc2rows.Add(self.szrNfield, 0, wx.EXPAND|wx.ALL, 5)
        self.szrFFMainColumns.Add(self.szrFFc1rows, 2, wx.EXPAND, 0)
        self.szrFFMainColumns.Add(self.szrFFc2rows, 3, wx.EXPAND, 0)
        self.pnFF.SetAutoLayout(1)
        self.pnFF.SetSizer(self.szrFFMainColumns)
        self.szrFFMainColumns.Fit(self.pnFF)
        self.szrFFMainColumns.SetSizeHints(self.pnFF)
        #
        # Layout External Field tab
        #
        hrdindex = 0
        hafindex = 0
        ljindex = 0
        umbindex = 0
        steeleindex = 0
        for i in range(self.towhee.get_nfield()):
            self.szrFieldType[i].Add(self.lblFieldType[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrFieldType[i].Add(self.cboFieldType[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            ef = self.towhee.get_single_externalfield(i)
            if ef.get_fieldtype() == "Hard Wall":
                self.szrHrdbox[hrdindex].Add(self.lblHrdbox[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdbox[hrdindex].Add(self.txtHrdbox[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdxyz[hrdindex].Add(self.lblHrdxyz[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdxyz[hrdindex].Add(self.txtHrdxyz[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdcen[hrdindex].Add(self.lblHrdcen[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdcen[hrdindex].Add(self.txtHrdcen[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdrad[hrdindex].Add(self.lblHrdrad[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdrad[hrdindex].Add(self.txtHrdrad[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdEnergyType[hrdindex].Add(self.lblHrdEnergyType[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdEnergyType[hrdindex].Add(self.cboHrdEnergyType[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdWallEnergy[hrdindex].Add(self.lblHrdWallEnergy[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHrdWallEnergy[hrdindex].Add(self.txtHrdWallEnergy[hrdindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrField[i].Add(self.szrHrdbox[hrdindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHrdxyz[hrdindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHrdcen[hrdindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHrdrad[hrdindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHrdEnergyType[hrdindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHrdWallEnergy[hrdindex], 0, wx.EXPAND, 0)
                if ef.get_energy_type() == "infinite":
                    self.szrField[i].Hide(self.szrHrdWallEnergy[hrdindex])
                hrdindex+=1
            elif ef.get_fieldtype() == "Harmonic Attractor":
                self.szrHafbox[hafindex].Add(self.lblHafbox[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafbox[hafindex].Add(self.txtHafbox[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafk[hafindex].Add(self.lblHafk[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafk[hafindex].Add(self.txtHafk[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafnentries[hafindex].Add(self.lblHafnentries[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafnentries[hafindex].Add(self.txtHafnentries[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafrefpos[hafindex].Add(self.lblHafrefpos[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafrefpos[hafindex].Add(self.cboHafrefpos[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafglobxyz[hafindex].Add(self.lblHafglobxyz[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafglobxyz[hafindex].Add(self.txtHafglobx[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafglobxyz[hafindex].Add(self.txtHafgloby[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafglobxyz[hafindex].Add(self.txtHafglobz[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafkey[hafindex].Add(self.lblHafkey[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrHafkey[hafindex].Add(self.cboHafkey[hafindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                for j in range(ef.get_nentries()):
                    self.szrHafmolec[hafindex][j].Add(self.lblHafmolec[hafindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafmolec[hafindex][j].Add(self.txtHafmolec[hafindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafelement[hafindex][j].Add(self.lblHafelement[hafindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafelement[hafindex][j].Add(self.txtHafelement[hafindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafname[hafindex][j].Add(self.lblHafname[hafindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafname[hafindex][j].Add(self.txtHafname[hafindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafkeyValues[hafindex][j].Add(self.szrHafmolec[hafindex][j], 0, wx.EXPAND, 0)
                    self.szrHafkeyValues[hafindex][j].Add(self.szrHafelement[hafindex][j], 0, wx.EXPAND, 0)
                    self.szrHafkeyValues[hafindex][j].Add(self.szrHafname[hafindex][j], 0, wx.EXPAND, 0)
                    self.szrHafkeyList[hafindex].Add(self.szrHafkeyValues[hafindex][j], 0, 0, 0)
                    if ef.get_key() == "Element":
                        self.szrHafkeyValues[hafindex][j].Hide(self.szrHafname[hafindex][j])
                    elif ef.get_key() == "FFtype":
                        self.szrHafkeyValues[hafindex][j].Hide(self.szrHafelement[hafindex][j])
                self.szrField[i].Add(self.szrHafbox[hafindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHafk[hafindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHafnentries[hafindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHafrefpos[hafindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHafglobxyz[hafindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHafkey[hafindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrHafkeyList[hafindex], 0, wx.EXPAND|wx.LEFT, 50)
                hafindex+=1
            elif ef.get_fieldtype() == "LJ 9-3 Wall":
                self.szrLjfbox[ljindex].Add(self.lblLjfbox[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfbox[ljindex].Add(self.txtLjfbox[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfxyz[ljindex].Add(self.lblLjfxyz[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfxyz[ljindex].Add(self.txtLjfxyz[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfcen[ljindex].Add(self.lblLjfcen[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfcen[ljindex].Add(self.txtLjfcen[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfdir[ljindex].Add(self.lblLjfdir[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfdir[ljindex].Add(self.txtLjfdir[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfcut[ljindex].Add(self.lblLjfcut[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfcut[ljindex].Add(self.txtLjfcut[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfshift[ljindex].Add(self.lblLjfshift[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfshift[ljindex].Add(self.rbLjfshift[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfrho[ljindex].Add(self.lblLjfrho[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfrho[ljindex].Add(self.txtLjfrho[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfntypes[ljindex].Add(self.lblLjfntypes[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrLjfntypes[ljindex].Add(self.txtLjfntypes[ljindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                for j in range(ef.get_ntypes()):
                    self.szrLjfname[ljindex][j].Add(self.lblLjfname[ljindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfname[ljindex][j].Add(self.txtLjfname[ljindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfsig[ljindex][j].Add(self.lblLjfsig[ljindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfsig[ljindex][j].Add(self.txtLjfsig[ljindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfeps[ljindex][j].Add(self.lblLjfeps[ljindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfeps[ljindex][j].Add(self.txtLjfeps[ljindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfntypesValues[ljindex][j].Add(self.szrLjfname[ljindex][j], 0, wx.EXPAND, 0)
                    self.szrLjfntypesValues[ljindex][j].Add(self.szrLjfsig[ljindex][j], 0, wx.EXPAND, 0)
                    self.szrLjfntypesValues[ljindex][j].Add(self.szrLjfeps[ljindex][j], 0, wx.EXPAND, 0)
                    self.szrLjfntypesList[ljindex].Add(self.szrLjfntypesValues[ljindex][j], 0, 0, 0)
                self.szrField[i].Add(self.szrLjfbox[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfxyz[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfcen[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfdir[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfcut[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfshift[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfrho[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfntypes[ljindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrLjfntypesList[ljindex], 0, wx.EXPAND|wx.LEFT, 50)
                ljindex+=1
            elif ef.get_fieldtype() == "Hooper Umbrella":
                self.szrUmbbox[umbindex].Add(self.lblUmbbox[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrUmbbox[umbindex].Add(self.txtUmbbox[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrUmbxyz[umbindex].Add(self.lblUmbxyz[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrUmbxyz[umbindex].Add(self.txtUmbxyz[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrUmbcenter[umbindex].Add(self.lblUmbcenter[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrUmbcenter[umbindex].Add(self.txtUmbcenter[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrUmba[umbindex].Add(self.lblUmba[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrUmba[umbindex].Add(self.txtUmba[umbindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrField[i].Add(self.szrUmbbox[umbindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrUmbxyz[umbindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrUmbcenter[umbindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrUmba[umbindex], 0, wx.EXPAND, 0)
                umbindex+=1
            elif ef.get_fieldtype() == "Steele Wall":
                self.szrSteelebox[steeleindex].Add(self.lblSteelebox[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelebox[steeleindex].Add(self.txtSteelebox[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelexyz[steeleindex].Add(self.lblSteelexyz[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelexyz[steeleindex].Add(self.txtSteelexyz[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelesurface[steeleindex].Add(self.lblSteelesurface[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelesurface[steeleindex].Add(self.txtSteelesurface[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteeledir[steeleindex].Add(self.lblSteeledir[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteeledir[steeleindex].Add(self.txtSteeledir[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelecutoff[steeleindex].Add(self.lblSteelecutoff[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelecutoff[steeleindex].Add(self.txtSteelecutoff[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteeleshift[steeleindex].Add(self.lblSteeleshift[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteeleshift[steeleindex].Add(self.rbSteeleshift[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteeledelta[steeleindex].Add(self.lblSteeledelta[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteeledelta[steeleindex].Add(self.txtSteeledelta[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelerho_s[steeleindex].Add(self.lblSteelerho_s[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelerho_s[steeleindex].Add(self.txtSteelerho_s[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelentype[steeleindex].Add(self.lblSteelentype[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                self.szrSteelentype[steeleindex].Add(self.txtSteelentype[steeleindex], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                for j in range(ef.get_ntype()):
                    self.szrSteelename[steeleindex][j].Add(self.lblSteelename[steeleindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelename[steeleindex][j].Add(self.txtSteelename[steeleindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelesigma_sf[steeleindex][j].Add(self.lblSteelesigma_sf[steeleindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelesigma_sf[steeleindex][j].Add(self.txtSteelesigma_sf[steeleindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteeleepsilon_sf[steeleindex][j].Add(self.lblSteeleepsilon_sf[steeleindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteeleepsilon_sf[steeleindex][j].Add(self.txtSteeleepsilon_sf[steeleindex][j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelentypeValues[steeleindex][j].Add(self.szrSteelename[steeleindex][j], 0, wx.EXPAND, 0)
                    self.szrSteelentypeValues[steeleindex][j].Add(self.szrSteelesigma_sf[steeleindex][j], 0, wx.EXPAND, 0)
                    self.szrSteelentypeValues[steeleindex][j].Add(self.szrSteeleepsilon_sf[steeleindex][j], 0, wx.EXPAND, 0)
                    self.szrSteelentypeList[steeleindex].Add(self.szrSteelentypeValues[steeleindex][j], 0, wx.EXPAND|wx.LEFT, 50)
                self.szrField[i].Add(self.szrSteelebox[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteelexyz[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteelesurface[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteeledir[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteelecutoff[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteeleshift[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteeledelta[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteelerho_s[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteelentype[steeleindex], 0, wx.EXPAND, 0)
                self.szrField[i].Add(self.szrSteelentypeList[steeleindex], 0, wx.EXPAND|wx.LEFT, 50)
                steeleindex+=1
            self.szrExternalField[i].Add(self.szrFieldType[i], 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
            self.szrExternalField[i].Add(self.szrField[i], 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
            self.szrExternalFieldList.Add(self.szrExternalField[i], 0, 0, 0)
        self.pnExternalFields.SetAutoLayout(1)
        self.pnExternalFields.SetSizer(self.szrExternalFieldList)
        self.szrExternalFieldList.FitInside(self.pnExternalFields)
        self.szrExternalFieldList.SetVirtualSizeHints(self.pnExternalFields)
        #
        # Layout Initialization tab
        #
        self.szrInitstyleValues[0].Add(self.lblInitstyleSpacer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        for i in range(self.towhee.get_nmolty()):
            self.szrInitstyleValues[0].Add(self.lblInitstyleMolty[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInitstyle.Add(self.szrInitstyleValues[0], 0, wx.ALIGN_CENTER_VERTICAL, 0)
        for i in range(self.towhee.get_numboxes()):
            self.szrInitstyleValues[i+1].Add(self.lblInitstyleBox[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            for j in range(self.towhee.get_nmolty()):
                self.szrInitstyleValues[i+1].Add(self.cboInitstyle[i][j], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrInitstyle.Add(self.szrInitstyleValues[i+1], 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.szrInitlatticeValues[0].Add(self.lblInitlatticeSpacer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        for i in range(self.towhee.get_nmolty()):
            self.szrInitlatticeValues[0].Add(self.lblInitlatticeMolty[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInitlattice.Add(self.szrInitlatticeValues[0], 0, wx.ALIGN_CENTER_VERTICAL, 0)
        for i in range(self.towhee.get_numboxes()):
            self.szrInitlatticeValues[i+1].Add(self.lblInitlatticeBox[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            for j in range(self.towhee.get_nmolty()):
                self.szrInitlatticeValues[i+1].Add(self.cboInitlattice[i][j], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrInitlattice.Add(self.szrInitlatticeValues[i+1], 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.szrInitmolValues[0].Add(self.lblInitmolSpacer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        for i in range(self.towhee.get_nmolty()):
            self.szrInitmolValues[0].Add(self.lblInitmolMolty[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInitmol.Add(self.szrInitmolValues[0], 0, wx.ALIGN_CENTER_VERTICAL, 0)
        for i in range(self.towhee.get_numboxes()):
            self.szrInitmolValues[i+1].Add(self.lblInitmolBox[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            for j in range(self.towhee.get_nmolty()):
                self.szrInitmolValues[i+1].Add(self.txtInitmol[i][j], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrInitmol.Add(self.szrInitmolValues[i+1], 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.szrInitboxtype.Add(self.lblInitboxtype, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInitboxtype.Add(self.cboInitboxtype, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

        self.szrInitC1.Add(self.rbLinit, 0, 0, 0)
        self.szrInitC1.Add(self.szrInitboxtype, 0, wx.EXPAND, 0)
        self.szrInitC1.Add(self.szrInitstyle, 0, wx.EXPAND, 0)
        self.szrInitC1.Add(self.btnHelix, 0, wx.ALL, 5)
        self.szrInitC1.Add(self.szrInitlattice, 0, wx.EXPAND, 0)
        self.szrInitC1.Add(self.szrInitmol, 0, wx.EXPAND, 0)
        self.szrInit.Add(self.szrInitC1, 1, wx.EXPAND, 0)

        j=0
        for i in range(0, len(self.txtHmatrix), 3):
            self.szrHmatrixRows[j].Add(self.txtHmatrix[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrHmatrixRows[j].Add(self.txtHmatrix[i+1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrHmatrixRows[j].Add(self.txtHmatrix[i+2], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            j+=1
        j=0
        for i in range(0, len(self.szrHmatrixRows), 3):
            self.szrHmatrixBox[j].Add(self.szrHmatrixRows[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrHmatrixBox[j].Add(self.szrHmatrixRows[i+1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrHmatrixBox[j].Add(self.szrHmatrixRows[i+2], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrHmatrix.Add(self.szrHmatrixBox[j], 0, wx.EXPAND, 0)
            j+=1

        for i in range(len(self.towhee.get_box_number_density())):
            self.szrBoxNumberDensityValues[i].Add(self.lblBoxNumberDensity[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrBoxNumberDensityValues[i].Add(self.txtBoxNumberDensity[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrBoxNumberDensity.Add(self.szrBoxNumberDensityValues[i], 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.szrInixyzValues[0].Add(self.lblInixyzSpacer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInixyzValues[0].Add(self.lblInix, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInixyzValues[0].Add(self.lblIniy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInixyzValues[0].Add(self.lblIniz, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrInixyz.Add(self.szrInixyzValues[0], 0, wx.EXPAND, 0)
        for i in range(self.towhee.get_numboxes()):
            self.szrInixyzValues[i+1].Add(self.lblInixyz[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrInixyzValues[i+1].Add(self.txtInixyz[i*3], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrInixyzValues[i+1].Add(self.txtInixyz[i*3+1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrInixyzValues[i+1].Add(self.txtInixyz[i*3+2], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            self.szrInixyz.Add(self.szrInixyzValues[i+1], 0, wx.EXPAND, 0)

        self.szrInitC2.Add(self.szrHmatrix, 0, wx.EXPAND, 0)
        self.szrInitC2.Add(self.szrBoxNumberDensity, 0, wx.EXPAND, 0)
        self.szrInitC2.Add(self.szrInixyz, 0, wx.EXPAND, 0)
        self.szrInit.Add(self.szrInitC2, 0, wx.EXPAND|wx.ALIGN_RIGHT, 0)

        self.pnInit.SetAutoLayout(1)
        self.pnInit.SetSizer(self.szrInit)
        self.szrInit.FitInside(self.pnInit)
        self.szrInit.SetVirtualSizeHints(self.pnInit)
        #
        # Layout Monte Carlo Moves tab
        #
        self.szrIVM.Add(self.lblPmvol, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrIVM.Add(self.txtPmvol, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrIVM.Add(self.btnIVM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrIVM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrAVM.Add(self.lblPmcell, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVM.Add(self.txtPmcell, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVM.Add(self.btnAVM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrAVM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrRB2BTM.Add(self.lblPm2boxrbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrRB2BTM.Add(self.txtPm2boxrbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrRB2BTM.Add(self.btnRB2BTM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrRB2BTM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrCB2BTM.Add(self.lblPm2boxcbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCB2BTM.Add(self.txtPm2boxcbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCB2BTM.Add(self.btnCB2BTM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrCB2BTM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrGCID.Add(self.lblPmuvtcbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrGCID.Add(self.txtPmuvtcbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrGCID.Add(self.btnGCID, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrGCID, 0, wx.EXPAND|wx.ALL, 5)
        self.szrCBSBMRM.Add(self.lblPm1boxcbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCBSBMRM.Add(self.txtPm1boxcbswap, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCBSBMRM.Add(self.btnCBSBMRM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrCBSBMRM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrAVBMT1.Add(self.lblPmavb1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVBMT1.Add(self.txtPmavb1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVBMT1.Add(self.btnAVBMT1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrAVBMT1, 0, wx.EXPAND|wx.ALL, 5)
        self.szrAVBMT2.Add(self.lblPmavb2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVBMT2.Add(self.txtPmavb2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVBMT2.Add(self.btnAVBMT2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrAVBMT2, 0, wx.EXPAND|wx.ALL, 5)
        self.szrAVBMT3.Add(self.lblPmavb3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVBMT3.Add(self.txtPmavb3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrAVBMT3.Add(self.btnAVBMT3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrAVBMT3, 0, wx.EXPAND|wx.ALL, 5)
        self.szrCBPMR.Add(self.lblPmcb, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCBPMR.Add(self.txtPmcb, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCBPMR.Add(self.btnCBPMR, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrCBPMR, 0, wx.EXPAND|wx.ALL, 5)
        self.szrCBPBR.Add(self.lblPmback, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCBPBR.Add(self.txtPmback, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCBPBR.Add(self.btnCBPBR, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrCBPBR, 0, wx.EXPAND|wx.ALL, 5)
        self.szrTPM.Add(self.lblPmpivot, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrTPM.Add(self.txtPmpivot, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrTPM.Add(self.btnTPM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrTPM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrCRMNPB.Add(self.lblPmconrot, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCRMNPB.Add(self.txtPmconrot, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCRMNPB.Add(self.btnCRMNPB, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrCRMNPB, 0, wx.EXPAND|wx.ALL, 5)
        self.szrCRM3PBS.Add(self.lblPmcrback, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCRM3PBS.Add(self.txtPmcrback, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCRM3PBS.Add(self.btnCRM3PBS, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrCRM3PBS, 0, wx.EXPAND|wx.ALL, 5)
        self.szrPSM.Add(self.lblPmplane, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrPSM.Add(self.txtPmplane, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrPSM.Add(self.btnPSM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrPSM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrRSM.Add(self.lblPmrow, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrRSM.Add(self.txtPmrow, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrRSM.Add(self.btnRSM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrRSM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrISATM.Add(self.lblPmtraat, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrISATM.Add(self.txtPmtraat, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrISATM.Add(self.btnISATM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrISATM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrCMMTM.Add(self.lblPmtracm, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCMMTM.Add(self.txtPmtracm, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrCMMTM.Add(self.btnCMMTM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrCMMTM, 0, wx.EXPAND|wx.ALL, 5)
        self.szrRCMM.Add(self.lblPmrotate, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrRCMM.Add(self.txtPmrotate, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrRCMM.Add(self.btnRCMM, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
        self.szrMCM.Add(self.szrRCMM, 0, wx.EXPAND|wx.ALL, 5)
        self.pnMCM.SetAutoLayout(1)
        self.pnMCM.SetSizer(self.szrMCM)
        self.szrMCM.Fit(self.pnMCM)
        self.szrMCM.SetSizeHints(self.pnMCM)
        #
        # Layout CBMC Information tab
        #
        self.szrTor.Add(self.lblTor, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrTor.Add(self.cboTor, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevtor.Add(self.lblSdevtor, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevtor.Add(self.txtSdevtor, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrBend.Add(self.lblBend, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrBend.Add(self.cboBend, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevbena.Add(self.lblSdevbena, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevbena.Add(self.txtSdevbena, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevbenb.Add(self.lblSdevbenb, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevbenb.Add(self.txtSdevbenb, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrVib.Add(self.lblVib, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrVib.Add(self.cboVib, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevvib.Add(self.lblSdevvib, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrSdevvib.Add(self.txtSdevvib, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrVibrang.Add(self.lblVibrang, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrVibrang.Add(self.txtVibrang1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrVibrang.Add(self.txtVibrang2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCdform.Add(self.lblCdform, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrCdform.Add(self.txtCdform, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        # Column 2
        self.szrNch_nb_one.Add(self.lblNch_nb_one, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNch_nb.Add(self.lblNch_nb, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNch_tor_out.Add(self.lblNch_tor_out, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNch_tor_in.Add(self.lblNch_tor_in, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNch_tor_in_con.Add(self.lblNch_tor_in_con, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNch_bend_a.Add(self.lblNch_bend_a, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNch_bend_b.Add(self.lblNch_bend_b, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.szrNch_vib.Add(self.lblNch_vib, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        for i in range(self.towhee.get_nmolty()):
            self.szrNch_nb_one.Add(self.txtNch_nb_one[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrNch_nb.Add(self.txtNch_nb[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrNch_tor_out.Add(self.txtNch_tor_out[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrNch_tor_in.Add(self.txtNch_tor_in[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrNch_tor_in_con.Add(self.txtNch_tor_in_con[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrNch_bend_a.Add(self.txtNch_bend_a[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrNch_bend_b.Add(self.txtNch_bend_b[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrNch_vib.Add(self.txtNch_vib[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.szrCBMCc1rows.Add(self.szrTor, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrSdevtor, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrBend, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrSdevbena, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrSdevbenb, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrVib, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrSdevvib, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrVibrang, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc1rows.Add(self.szrCdform, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_nb_one, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_nb, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_tor_out, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_tor_in, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_tor_in_con, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_bend_a, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_bend_b, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMCc2rows.Add(self.szrNch_vib, 0, wx.EXPAND|wx.ALL, 10)
        self.szrCBMC.Add(self.szrCBMCc1rows, 0, wx.EXPAND, 0)
        self.szrCBMC.Add(self.szrCBMCc2rows, 0, wx.EXPAND, 0)
        self.pnCBMC.SetAutoLayout(1)
        self.pnCBMC.SetSizer(self.szrCBMC)
        self.szrCBMC.Fit(self.pnCBMC)
        self.szrCBMC.SetSizeHints(self.pnCBMC)
        #
        # Layout Inputs tab
        #
        self.szrLabels.Add(self.lblL1, 0, wx.ALL, 5)
        self.szrLabels.Add(self.lblL2, 0, wx.ALL, 5)
        self.szrLabels.Add(self.lblL3, 0, wx.ALL, 5)
        self.szrLabels.Add(self.lblL4, 0, wx.ALL, 5)
        self.szrInputs.Add(self.szrLabels, 0, wx.EXPAND|wx.ALL, 5)
        for i in range(self.towhee.get_nmolty()):
            self.szrData[i].Add(self.lblM[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrData[i].Add(self.cboInpstyle[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrData[i].Add(self.txtNunit[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrData[i].Add(self.txtNmaxcbmc[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrData[i].Add(self.btnM[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrInputs.Add(self.szrData[i], 0, wx.EXPAND|wx.ALL, 5)
        self.pnInputs.SetAutoLayout(1)
        self.pnInputs.SetSizer(self.szrInputs)
        self.szrInputs.Fit(self.pnInputs)
        self.szrInputs.SetSizeHints(self.pnInputs)

        self.szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        self.szrButtons.Add(self.btnSave, 0, wx.EXPAND|wx.ALL, 5)
        self.szrButtons.Add(self.btnCancel, 0, wx.EXPAND|wx.ALL, 5)
        #
        # Add the pages to the notebook
        #
        self.nbTowheeEditor.AddPage(self.pnBasic, "Basic")
        self.nbTowheeEditor.AddPage(self.pnRunInfo, "Run Information")
        self.nbTowheeEditor.AddPage(self.pnFF, "Force Field")
        self.nbTowheeEditor.AddPage(self.pnExternalFields, "External Fields")
        self.nbTowheeEditor.AddPage(self.pnInit, "Initialization")
        self.nbTowheeEditor.AddPage(self.pnMCM, "Monte Carlo Moves")
        self.nbTowheeEditor.AddPage(self.pnCBMC, "CBMC Information")
        self.nbTowheeEditor.AddPage(self.pnInputs, "Inputs")
        self.szrTowheeEditor.Add(self.nbTowheeEditor, 1, wx.EXPAND, 0)
        self.szrTowheeEditor.Add(self.szrButtons, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
        self.SetAutoLayout(1)
        self.SetSizer(self.szrTowheeEditor)
        self.Layout()
        return

    def __setup_logic(self):
        #
        # Logic for Basic tab
        #
        wx.EVT_TEXT(self, self.txtNmolty.GetId(), self.NmoltyChanged)
        wx.EVT_TEXT(self, self.txtNumboxes.GetId(), self.NumboxesChanged)
        wx.EVT_COMBOBOX(self, self.cboEnsemble.GetId(), self.EnsembleChanged)
        #
        # Logic for Run Information tab
        #
        wx.EVT_RADIOBOX(self, self.rbLouthist.GetId(), self.LouthistChanged)
        wx.EVT_COMBOBOX(self, self.cboStepstyle.GetId(), self.StepstyleChanged)
        #
        # Logic for Force Field tab
        #
        wx.EVT_COMBOBOX(self, self.cboClassicalPotential.GetId(), self.ClassicalPotentialChanged)
        wx.EVT_COMBOBOX(self, self.cboCmixRescalingStyle.GetId(), self.CmixRescalingStyleChanged)
        wx.EVT_TEXT(self, self.txtCmixNpair.GetId(), self.CmixNpairChanged)
        wx.EVT_TEXT(self, self.txtFfnumber.GetId(), self.FfnumberChanged)
        wx.EVT_COMBOBOX(self, self.cboCoulombstyle.GetId(), self.CoulombstyleChanged)
        wx.EVT_TEXT(self, self.txtNfield.GetId(), self.NfieldChanged)
        #
        # Logic for External Fields
        #
        for i in self.cboFieldType:
            wx.EVT_COMBOBOX(self, i.GetId(), self.FieldTypeChanged)

        for i in self.cboHrdEnergyType:
            wx.EVT_COMBOBOX(self, i.GetId(), self.HrdEnergyTypeChanged)

        for i in self.txtHafnentries:
            wx.EVT_COMBOBOX(self, i.GetId(), self.HafnentriesChanged)

        for i in self.cboHafrefpos:
            wx.EVT_COMBOBOX(self, i.GetId(), self.HafrefposChanged)

        for i in self.cboHafkey:
            wx.EVT_COMBOBOX(self, i.GetId(), self.HafkeyChanged)

        for i in self.txtLjfntypes:
            wx.EVT_TEXT(self, i.GetId(), self.LjfntypesChanged)
            
        for i in self.txtSteelentype:
            wx.EVT_TEXT(self, i.GetId(), self.SteelentypeChanged)
        #
        # Logic for Initialization tab
        #
        wx.EVT_BUTTON(self, self.btnHelix.GetId(), self.ButtonHelix)
        wx.EVT_COMBOBOX(self, self.cboInitboxtype.GetId(), self.InitboxtypeChanged)
        #
        # Logic for Monte Carlo Moves tab
        #
        wx.EVT_BUTTON(self, self.btnIVM.GetId(), self.ButtonIVM)
        wx.EVT_BUTTON(self, self.btnAVM.GetId(), self.ButtonAVM)
        wx.EVT_BUTTON(self, self.btnGCID.GetId(), self.ButtonGCID)
        wx.EVT_BUTTON(self, self.btnCBSBMRM.GetId(), self.ButtonCBSBMRM)
        wx.EVT_BUTTON(self, self.btnRB2BTM.GetId(), self.ButtonRB2BMTM)
        wx.EVT_BUTTON(self, self.btnCB2BTM.GetId(), self.ButtonCB2BMTM)
        wx.EVT_BUTTON(self, self.btnAVBMT1.GetId(), self.ButtonAVBMT1)
        wx.EVT_BUTTON(self, self.btnAVBMT2.GetId(), self.ButtonAVBMT2)
        wx.EVT_BUTTON(self, self.btnAVBMT3.GetId(), self.ButtonAVBMT3)
        wx.EVT_BUTTON(self, self.btnCBPMR.GetId(), self.ButtonCBPMR)
        wx.EVT_BUTTON(self, self.btnCBPBR.GetId(), self.ButtonCBPBR)
        wx.EVT_BUTTON(self, self.btnTPM.GetId(), self.ButtonTPM)
        wx.EVT_BUTTON(self, self.btnCRMNPB.GetId(), self.ButtonCRMNPB)
        wx.EVT_BUTTON(self, self.btnCRM3PBS.GetId(), self.ButtonCRM3PBS)
        wx.EVT_BUTTON(self, self.btnPSM.GetId(), self.ButtonPSM)
        wx.EVT_BUTTON(self, self.btnRSM.GetId(), self.ButtonRSM)
        wx.EVT_BUTTON(self, self.btnISATM.GetId(), self.ButtonISATM)
        wx.EVT_BUTTON(self, self.btnCMMTM.GetId(), self.ButtonCMMTM)
        wx.EVT_BUTTON(self, self.btnRCMM.GetId(), self.ButtonRCMM)

        wx.EVT_SET_FOCUS(self.txtPmvol, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmcell, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmuvtcbswap, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPm1boxcbswap, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPm2boxrbswap, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPm2boxcbswap, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmavb1, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmavb2, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmavb3, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmcb, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmback, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmpivot, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmconrot, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmcrback, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmplane, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmrow, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmtraat, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmtracm, self.focusGain)
        wx.EVT_SET_FOCUS(self.txtPmrotate, self.focusGain)
        #
        # Logic for CMBC tab
        #
        wx.EVT_COMBOBOX(self, self.cboTor.GetId(), self.TorcbstyleChanged)
        wx.EVT_COMBOBOX(self, self.cboBend.GetId(), self.BendcbstyleChanged)
        wx.EVT_COMBOBOX(self, self.cboVib.GetId(), self.VibcbstyleChanged)
        #
        # Logic for Inputs tab
        #
        for i in range(self.towhee.get_nmolty()):
            wx.EVT_BUTTON(self, self.btnM[i].GetId(), self.InputSetup)
        #
        # Logic for Main buttons
        #
        wx.EVT_BUTTON(self, self.btnSave.GetId(), self.SaveAndExit)
        wx.EVT_BUTTON(self, self.btnCancel.GetId(), self.CancelAndExit)
        return

    def focusGain(self,event):
        xunit,yunit = self.pnMCM.GetScrollPixelsPerUnit()
        w=self.FindWindowById(event.GetId()) 
        x,y=w.GetPositionTuple() 
        hx,hy=w.GetSizeTuple() 
        cx,cy=self.pnMCM.GetClientSizeTuple() 
        sx,sy=self.pnMCM.GetViewStart() 
        sx=sx*50 
        sy=sy*50 
         
        if (y<sy): 
            self.pnMCM.Scroll(0,y/yunit) 
        if (x<sx): 
            self.pnMCM.Scroll(0,x/xunit) 
        if ((x+sx)>cx): 
            self.pnMCM.Scroll(0,x/xunit) 
        if ((y+hy-sy)>cy): 
            self.pnMCM.Scroll(0,y/yunit) 
 
        event.Skip()
        return
    #
    # Functions to handle the logic for the Basic tab
    #
    def NmoltyChanged(self, *args):
        l = self.txtNmolty.GetValue()
        if l.isdigit() and l > 0:
            l = int(l)
            old_nmolty = self.towhee.get_nmolty()
            self.towhee.set_nmolty(l)
            #
            # New nmolty value is larger than old value
            #
            if l > old_nmolty:
                #
                # These MCMs depend on nmolty, so add default data
                #
                mcm = self.towhee.get_rb2bmtm()
                for i in range(len(mcm.get_pm2rbswmt()), l):
                    mcm.append_pm2rbswmt("1.00d0")
                self.towhee.set_rb2bmtm(mcm)

                mcm = self.towhee.get_cb2bmtm()
                for i in range(len(mcm.get_pm2cbswmt()), l):
                    mcm.append_pm2cbswmt("1.00d0")
                self.towhee.set_cb2bmtm(mcm)

                mcm = self.towhee.get_cbgcidm()
                for i in range(len(mcm.get_pmuvtcbmt()), l):
                    mcm.append_pmuvtcbmt("1.00d0")
                self.towhee.set_cbgcidm(mcm)

                for i in range(old_nmolty, l):
                    mcm = self.towhee.get_cbsbmrm()
                    mcm.append_pm1cbswmt("1.00d0")
                    self.towhee.set_cbsbmrm(mcm)
                
                mcm = self.towhee.get_avbmt1()
                for i in range(old_nmolty, l):
                    mcm.append_pmavb1mt("1.00d0")
                for z in range(old_nmolty):
                    for y in range(old_nmolty, l):
                        mcm.append_single_pmavb1ct(z, "1.00d0")
                for y in range(old_nmolty, l):
                    T = []
                    for z in range(l):
                        T.append("1.00d0")
                    mcm.append_pmavb1ct(T)
                self.towhee.set_avbmt1(mcm)
                
                mcm = self.towhee.get_avbmt2()
                for i in range(old_nmolty, l):
                    mcm.append_pmavb2mt("1.00d0")
                for z in range(old_nmolty):
                    for y in range(old_nmolty, l):
                        mcm.append_single_pmavb2ct(z, "1.00d0")
                for y in range(old_nmolty, l):
                    T = []
                    for z in range(l):
                        T.append("1.00d0")
                    mcm.append_pmavb2ct(T)
                self.towhee.set_avbmt2(mcm)
                
                mcm = self.towhee.get_avbmt3()
                for i in range(old_nmolty, l):
                    mcm.append_pmavb3mt("1.00d0")
                for z in range(old_nmolty):
                    for y in range(old_nmolty, l):
                        mcm.append_single_pmavb3ct(z, "1.00d0")
                for y in range(old_nmolty, l):
                    T = []
                    for z in range(l):
                        T.append("1.00d0")
                    mcm.append_pmavb3ct(T)
                self.towhee.set_avbmt3(mcm)
                
                for i in range(old_nmolty, l):
                    mcm = self.towhee.get_cbpmr()
                    mcm.append_pmcbmt("1.00d0")
                    mcm.append_pmall("1.00d0")
                    self.towhee.set_cbpmr(mcm)
                
                    mcm = self.towhee.get_cbpbr()
                    mcm.append_pmbkmt("1.00d0")
                    self.towhee.set_cbpbr(mcm)
                
                    mcm = self.towhee.get_tpm()
                    mcm.append_pmpivmt("1.00d0")
                    self.towhee.set_tpm(mcm)
                    
                    mcm = self.towhee.get_crnmoanpb()
                    mcm.append_pmcrmt("1.00d0")
                    self.towhee.set_crnmoanpb(mcm)
                    
                    mcm = self.towhee.get_crnmoa3pbs()
                    mcm.append_pmcrbmt("1.00d0")
                    self.towhee.set_crnmoa3pbs(mcm)

                    mcm = self.towhee.get_isatm()
                    mcm.append_pmtamt("1.00d0")
                    self.towhee.set_isatm(mcm)
                    
                    mcm = self.towhee.get_cofmmtm()
                    mcm.append_pmtcmt("1.00d0")
                    self.towhee.set_cofmmtm(mcm)
                    
                    mcm = self.towhee.get_ratcomm()
                    mcm.append_pmromt("1.00d0")
                    self.towhee.set_ratcomm(mcm)

                for i in range(old_nmolty, l):
                    #
                    # Run Info Tab
                    #
                    self.txtNmolectype.append(wx.TextCtrl(self.pnRunInfo, -1, ""))
                    self.szrNmolectypeData.Add(self.txtNmolectype[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.txtChempot.append(wx.TextCtrl(self.pnRunInfo, -1, ""))
                    self.szrChempotData.Add(self.txtChempot[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.txtChempotperstep.append(wx.TextCtrl(self.pnRunInfo, -1, ""))
                    self.szrChempotperstepData.Add(self.txtChempotperstep[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    #
                    # CBMC Tab
                    #
                    self.txtNch_nb_one.append(wx.TextCtrl(self.pnCBMC, -1, "10", size=(50,-1)))
                    self.txtNch_nb.append(wx.TextCtrl(self.pnCBMC, -1, "10", size=(50,-1)))
                    self.txtNch_tor_out.append(wx.TextCtrl(self.pnCBMC, -1, "10", size=(50,-1)))
                    self.txtNch_tor_in.append(wx.TextCtrl(self.pnCBMC, -1, "10", size=(50,-1)))
                    self.txtNch_tor_in_con.append(wx.TextCtrl(self.pnCBMC, -1, "100", size=(50,-1)))
                    self.txtNch_bend_a.append(wx.TextCtrl(self.pnCBMC, -1, "1000", size=(50,-1)))
                    self.txtNch_bend_b.append(wx.TextCtrl(self.pnCBMC, -1, "1000", size=(50,-1)))
                    self.txtNch_vib.append(wx.TextCtrl(self.pnCBMC, -1, "1000", size=(50,-1)))
                    self.szrNch_nb_one.Add(self.txtNch_nb_one[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrNch_nb.Add(self.txtNch_nb[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrNch_tor_out.Add(self.txtNch_tor_out[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrNch_tor_in.Add(self.txtNch_tor_in[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrNch_tor_in_con.Add(self.txtNch_tor_in_con[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrNch_bend_a.Add(self.txtNch_bend_a[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrNch_bend_b.Add(self.txtNch_bend_b[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrNch_vib.Add(self.txtNch_vib[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    #
                    # Inputs Tab
                    #
                    mnsize = self.lblL1.GetSize()
                    inpsize = self.lblL2.GetSize()
                    nunitsize = self.lblL3.GetSize()
                    nmaxsize = self.lblL4.GetSize()
                    self.input_error.append(True)
                    self.szrData.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.lblM.append(wx.StaticText(self.pnInputs, -1, "Molecule " + str(i+1), size=mnsize))
                    self.cboInpstyle.append(wx.ComboBox(self.pnInputs, -1,\
                        choices=["0", "1", "2", "3", "4"],\
                        style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(inpsize[0],-1)))
                    self.txtNunit.append(wx.TextCtrl(self.pnInputs, -1, "", size=(nunitsize[0],-1)))
                    self.txtNmaxcbmc.append(wx.TextCtrl(self.pnInputs, -1, "",size=(nmaxsize[0],-1)))
                    self.btnM.append(wx.Button(self.pnInputs, -1, "Molecule Info"))
                    self.btnIDs.append(self.btnM[-1].GetId())
                    wx.EVT_BUTTON(self, self.btnM[-1].GetId(), self.InputSetup)
                    self.cboInpstyle[i].SetSelection(0)
                    temp_input = self.towhee.create_input(0)
                    self.towhee.append_input(temp_input)
                    self.szrData[i].Add(self.lblM[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrData[i].Add(self.cboInpstyle[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrData[i].Add(self.txtNunit[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrData[i].Add(self.txtNmaxcbmc[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrData[i].Add(self.btnM[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrInputs.Add(self.szrData[i], 0, wx.EXPAND|wx.ALL, 5)
                    #
                    # Initialization Tab
                    #
                    self.lblInitstyleMolty.append(wx.StaticText(self.pnInit, -1, "Mol " + str(i+1), size=(120,-1), style=wx.ALIGN_CENTER))
                    self.szrInitstyleValues[0].Add(self.lblInitstyleMolty[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.lblInitlatticeMolty.append(wx.StaticText(self.pnInit, -1, "Mol " + str(i+1), size=(120,-1), style=wx.ALIGN_CENTER))
                    self.szrInitlatticeValues[0].Add(self.lblInitlatticeMolty[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.lblInitmolMolty.append(wx.StaticText(self.pnInit, -1, "Mol " + str(i+1), size=(40,-1), style=wx.ALIGN_CENTER))
                    self.szrInitmolValues[0].Add(self.lblInitmolMolty[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    for j in range(self.towhee.get_numboxes()):
                        self.cboInitstyle[j].append(\
                            wx.ComboBox(self.pnInit, -1, choices=[\
                            "full cbmc",\
                            "template",\
                            "coords",\
                            "nanotube",\
                            "helix",\
                            "partial cbmc"\
                            ], style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(120,-1)))
                        self.szrInitstyleValues[j+1].Add(self.cboInitstyle[j][-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

                        self.cboInitlattice[j].append(\
                            wx.ComboBox(self.pnInit, -1, choices=[\
                            "center",\
                            "none",\
                            "simple cubic"\
                            ], style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(120,-1)))
                        self.szrInitlatticeValues[j+1].Add(self.cboInitlattice[j][-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                        self.txtInitmol[j].append(wx.TextCtrl(self.pnInit, -1, "", size=(40,-1)))
                        self.szrInitmolValues[j+1].Add(self.txtInitmol[j][-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            #
            # New nmolty value is smaller than old value
            #
            elif l < old_nmolty:
                for i in range(l, old_nmolty):
                    #
                    # Run Info Tab
                    #
                    self.szrNmolectypeData.Remove(self.txtNmolectype[-1])
                    self.txtNmolectype[-1].Destroy()
                    self.txtNmolectype.pop()
                    self.szrChempotData.Remove(self.txtChempot[-1])
                    self.txtChempot[-1].Destroy()
                    self.txtChempot.pop()
                    self.szrChempotperstepData.Remove(self.txtChempotperstep[-1])
                    self.txtChempotperstep[-1].Destroy()
                    self.txtChempotperstep.pop()
                    #
                    # CBMC Tab
                    #
                    self.szrNch_nb_one.Remove(self.txtNch_nb_one[-1])
                    self.szrNch_nb.Remove(self.txtNch_nb[-1])
                    self.szrNch_tor_out.Remove(self.txtNch_tor_out[-1])
                    self.szrNch_tor_in.Remove(self.txtNch_tor_in[-1])
                    self.szrNch_tor_in_con.Remove(self.txtNch_tor_in_con[-1])
                    self.szrNch_bend_a.Remove(self.txtNch_bend_a[-1])
                    self.szrNch_bend_b.Remove(self.txtNch_bend_b[-1])
                    self.szrNch_vib.Remove(self.txtNch_vib[-1])
                    self.txtNch_nb_one[-1].Destroy()
                    self.txtNch_nb[-1].Destroy()
                    self.txtNch_tor_out[-1].Destroy()
                    self.txtNch_tor_in[-1].Destroy()
                    self.txtNch_tor_in_con[-1].Destroy()
                    self.txtNch_bend_a[-1].Destroy()
                    self.txtNch_bend_b[-1].Destroy()
                    self.txtNch_vib[-1].Destroy()
                    self.txtNch_nb_one.pop()
                    self.txtNch_nb.pop()
                    self.txtNch_tor_out.pop()
                    self.txtNch_tor_in.pop()
                    self.txtNch_tor_in_con.pop()
                    self.txtNch_bend_a.pop()
                    self.txtNch_bend_b.pop()
                    self.txtNch_vib.pop()
                    #
                    # Inputs Tab
                    #
                    self.input_error.pop()
                    self.szrInputs.Remove(l+1)
                    self.lblM[-1].Destroy()
                    self.cboInpstyle[-1].Destroy()
                    self.txtNunit[-1].Destroy()
                    self.txtNmaxcbmc[-1].Destroy()
                    self.btnM[-1].Destroy()
                    self.lblM.pop()
                    self.cboInpstyle.pop()
                    self.txtNunit.pop()
                    self.txtNmaxcbmc.pop()
                    self.btnM.pop()
                    self.btnIDs.pop()
                    self.szrData.pop()
                #
                # Initialization Tab
                #
                for i in range(l, old_nmolty):
                    self.szrInitstyleValues[0].Remove(self.lblInitstyleMolty[-1])
                    self.szrInitmolValues[0].Remove(self.lblInitmolMolty[-1])
                    self.lblInitstyleMolty[-1].Destroy()
                    self.lblInitmolMolty[-1].Destroy()
                    self.lblInitstyleMolty.pop()
                    self.lblInitmolMolty.pop()
                    for j in range(self.towhee.get_numboxes()):
                        self.szrInitstyleValues[j+1].Remove(self.cboInitstyle[j][-1])
                        self.szrInitlatticeValues[j+1].Remove(self.cboInitlattice[j][-1])
                        self.szrInitmolValues[j+1].Remove(self.txtInitmol[j][-1])
                        self.cboInitstyle[j][-1].Destroy()
                        self.cboInitlattice[j][-1].Destroy()
                        self.txtInitmol[j][-1].Destroy()
                        self.cboInitstyle[j].pop()
                        self.cboInitlattice[j].pop()
                        self.txtInitmol[j].pop()
            self.InitboxtypeChanged()
            self.szrInit.Fit(self.pnInit)
            self.szrRIc1rows.Layout()
            self.szrCBMCc2rows.Layout()
            self.pnCBMC.Refresh()
            self.szrInputs.FitInside(self.pnInputs)
            self.szrInputs.Layout()
            self.pnInputs.Refresh()
            self.Refresh()
            self.DynamicUpdate_RI()
        return

    def NumboxesChanged(self, *args):
        l = self.txtNumboxes.GetValue()
        if l.isdigit() and l > 0:
            l = int(l)
            old_numboxes = self.towhee.get_numboxes()
            self.towhee.set_numboxes(l)
            if l > old_numboxes:
                #
                # These MCMs depend on numboxes, so add default data
                #
                mcm = self.towhee.get_ivm()
                for i in range(len(mcm.get_pmvlpr()), mcm.get_pmvlpr_length()):
                    mcm.append_pmvlpr("1.00d0")
                self.towhee.set_ivm(mcm)

                mcm = self.towhee.get_avm()
                for i in range(len(mcm.get_pmcellpr()), mcm.get_length()):
                    mcm.append_pmcellpr("1.00d0")
                for i in range(len(mcm.get_pmcellpt()), mcm.get_length()):
                    mcm.append_pmcellpt("1.00d0")
                self.towhee.set_avm(mcm)

                mcm = self.towhee.get_rb2bmtm()
                for i in range(len(mcm.get_pm2rbswpr()), mcm.get_nbp()):
                    mcm.append_pm2rbswpr("1.00d0")
                for i in range(len(mcm.get_pm2rbswmt()), mcm.get_nmolty()):
                    mcm.append_pm2rbswmt("1.00d0")
                self.towhee.set_rb2bmtm(mcm)

                mcm = self.towhee.get_cb2bmtm()
                for i in range(len(mcm.get_pm2cbswpr()), mcm.get_nbp()):
                    mcm.append_pm2cbswpr("1.00d0")
                for i in range(len(mcm.get_pm2cbswmt()), mcm.get_nmolty()):
                    mcm.append_pm2cbswmt("1.00d0")
                self.towhee.set_cb2bmtm(mcm)

                mcm = self.towhee.get_psm()
                for i in range(old_numboxes, l):
                    mcm.append_pmplanebox("1.00d0")
                self.towhee.set_psm(mcm)

                mcm = self.towhee.get_rsm()
                for i in range(old_numboxes, l):
                    mcm.append_pmrowbox("1.00d0")
                self.towhee.set_rsm(mcm)
                #
                # Initialization Tab
                #
                for i in range(old_numboxes, l):
                    self.lblInitstyleBox.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
                    self.lblInitlatticeBox.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
                    self.lblInitmolBox.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
                    
                    self.szrInitstyleValues.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrInitlatticeValues.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrInitmolValues.append(wx.BoxSizer(wx.HORIZONTAL))
                    
                    self.szrInitstyleValues[-1].Add(self.lblInitstyleBox[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrInitlatticeValues[-1].Add(self.lblInitlatticeBox[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrInitmolValues[-1].Add(self.lblInitmolBox[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

                    T1 = []
                    T2 = []
                    T3 = []
                    for j in range(self.towhee.get_nmolty()):
                        T1.append(\
                            wx.ComboBox(self.pnInit, -1, choices=[\
                            "full cbmc",\
                            "template",\
                            "coords",\
                            "nanotube",\
                            "helix",\
                            "partial cbmc"\
                            ], style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(120,-1)))
                        T2.append(wx.TextCtrl(self.pnInit, -1, "", size=(40,-1)))
                        T3.append(\
                            wx.ComboBox(self.pnInit, -1, choices=[\
                            "center",\
                            "none",\
                            "simple cubic"\
                            ], style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(120,-1)))
                    self.cboInitstyle.append(T1)
                    self.txtInitmol.append(T2)
                    self.cboInitlattice.append(T3)

                    for j in range(self.towhee.get_nmolty()):
                        self.szrInitstyleValues[-1].Add(self.cboInitstyle[-1][j], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                        self.szrInitlatticeValues[-1].Add(self.cboInitlattice[-1][j], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                        self.szrInitmolValues[-1].Add(self.txtInitmol[-1][j], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)

                    self.szrInitstyle.Add(self.szrInitstyleValues[-1], 0, wx.ALIGN_CENTER_VERTICAL, 0)
                    self.szrInitlattice.Add(self.szrInitlatticeValues[-1], 0, wx.ALIGN_CENTER_VERTICAL, 0)
                    self.szrInitmol.Add(self.szrInitmolValues[-1], 0, wx.ALIGN_CENTER_VERTICAL, 0)
                #
                # Add more Hmatrixes
                #
                for i in range((l-old_numboxes)*9):
                    self.txtHmatrix.append(wx.TextCtrl(self.pnInit, -1, "0.0d0", size=(60,-1)))
                for i in range(0, (l-old_numboxes)*9, 3):
                    j = old_numboxes*9+i
                    self.szrHmatrixRows.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHmatrixRows[-1].Add(self.txtHmatrix[j], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrHmatrixRows[-1].Add(self.txtHmatrix[j+1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrHmatrixRows[-1].Add(self.txtHmatrix[j+2], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                for i in range(old_numboxes, l):
                    self.szrHmatrixBox.append(wx.StaticBoxSizer(wx.StaticBox(self.pnInit, -1, "Simulation Box " + str(i+1)), wx.VERTICAL))
                    self.szrHmatrixBox[-1].Add(self.szrHmatrixRows[i*3], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
                    self.szrHmatrixBox[-1].Add(self.szrHmatrixRows[i*3+1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
                    self.szrHmatrixBox[-1].Add(self.szrHmatrixRows[i*3+2], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
                    self.szrHmatrix.Add(self.szrHmatrixBox[-1], 0, wx.EXPAND, 0)
                #
                # Add more box_number_density
                #
                for i in range(old_numboxes, l):
                    self.lblBoxNumberDensity.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
                    self.txtBoxNumberDensity.append(wx.TextCtrl(self.pnInit, -1, "", size=(40,-1)))
                    self.szrBoxNumberDensityValues.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrBoxNumberDensityValues[-1].Add(self.lblBoxNumberDensity[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrBoxNumberDensityValues[-1].Add(self.txtBoxNumberDensity[-1], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrBoxNumberDensity.Add(self.szrBoxNumberDensityValues[-1], 0, wx.ALIGN_CENTER_VERTICAL, 0)
                #
                # Add more inixyzs
                #
                for i in range(old_numboxes, l):
                    self.lblInixyz.append(wx.StaticText(self.pnInit, -1, "Simulation Box " + str(i+1), style=wx.ALIGN_RIGHT))
                    self.txtInixyz.append(wx.TextCtrl(self.pnInit, -1, "", size=(60,-1)))
                    self.txtInixyz.append(wx.TextCtrl(self.pnInit, -1, "", size=(60,-1)))
                    self.txtInixyz.append(wx.TextCtrl(self.pnInit, -1, "", size=(60,-1)))
                    self.szrInixyzValues.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrInixyzValues[-1].Add(self.lblInixyz[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrInixyzValues[-1].Add(self.txtInixyz[-3], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrInixyzValues[-1].Add(self.txtInixyz[-2], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrInixyzValues[-1].Add(self.txtInixyz[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
                    self.szrInixyz.Add(self.szrInixyzValues[-1], 0, wx.EXPAND, 0)
            elif l < old_numboxes:
                #
                # Initialization Tab
                #
                for i in range(l, old_numboxes):
                    self.szrInitstyle.Remove(self.szrInitstyleValues[-1])
                    self.szrInitmol.Remove(self.szrInitmolValues[-1])
                    for i in range(self.towhee.get_nmolty()):
                        self.cboInitstyle[-1][i].Destroy()
                        self.cboInitlattice[-1][i].Destroy()
                        self.txtInitmol[-1][i].Destroy()
                    self.lblInitstyleBox[-1].Destroy()
                    self.lblInitstyleBox.pop()
                    self.lblInitmolBox[-1].Destroy()
                    self.lblInitmolBox.pop()
                    self.cboInitstyle.pop()
                    self.cboInitlattice.pop()
                    self.txtInitmol.pop()
                    self.szrInitstyleValues.pop()
                    self.szrInitmolValues.pop()
                #
                # Remove the Hmatrixes
                #
                for i in range((old_numboxes-l)*9):
                    self.txtHmatrix[-1].Destroy()
                    self.txtHmatrix.pop()
                for i in range((old_numboxes-l)*3):
                    self.szrHmatrixRows.pop()
                for i in range(old_numboxes-l):
                    b = self.szrHmatrixBox[-1].GetStaticBox()
                    b.Destroy()
                    self.szrHmatrix.Remove(self.szrHmatrixBox[-1])
                    self.szrHmatrixBox.pop()
                #
                # Remove the box_number_density
                #
                for i in range(l, old_numboxes):
                    self.szrBoxNumberDensity.Remove(l)
                    self.lblBoxNumberDensity[-1].Destroy()
                    self.lblBoxNumberDensity.pop()
                    self.txtBoxNumberDensity[-1].Destroy()
                    self.txtBoxNumberDensity.pop()
                    self.szrBoxNumberDensityValues.pop()
                #
                # Remove inixyzs
                #
                for i in range(old_numboxes-l):
                    self.txtInixyz[-1].Destroy()
                    self.txtInixyz.pop()
                    self.txtInixyz[-1].Destroy()
                    self.txtInixyz.pop()
                    self.txtInixyz[-1].Destroy()
                    self.txtInixyz.pop()
                    self.lblInixyz[-1].Destroy()
                    self.lblInixyz.pop()
                    self.szrInixyz.Remove(self.szrInixyzValues[-1])
                    self.szrInixyzValues.pop()

            self.InitboxtypeChanged()
            self.szrInitC1.Layout()
            self.szrInit.Layout()
            self.szrInit.Fit(self.pnInit)
            self.pnInit.Refresh()
            self.Refresh()
        self.DynamicUpdate_MCM()
        return

    def EnsembleChanged(self, *args):
        l = self.cboEnsemble.GetStringSelection()
        self.towhee.set_ensemble(l)
        #
        # These MCMs depend on ensemble, so set them up
        #
        mcm = self.towhee.get_ivm()
        for i in range(len(mcm.get_pmvlpr()), mcm.get_pmvlpr_length()):
            mcm.append_pmvlpr("1.00d0")
        self.towhee.set_ivm(mcm)

        mcm = self.towhee.get_avm()
        for i in range(len(mcm.get_pmcellpr()), mcm.get_length()):
            mcm.append_pmcellpr("1.00d0")
        for i in range(len(mcm.get_pmcellpt()), mcm.get_length()):
            mcm.append_pmcellpt("1.00d0")
        self.towhee.set_avm(mcm)

        mcm = self.towhee.get_cbgcidm()
        for i in range(len(mcm.get_pmuvtcbmt()), mcm.get_nmolty()):
            mcm.append_pmuvtcbmt("1.00d0")
        self.towhee.set_cbgcidm(mcm)

        self.DynamicUpdate_RI()
        self.DynamicUpdate_FF()
        self.DynamicUpdate_MCM()
        return
    #
    # Functions to handle the logic for the Run Information tab
    #
    def LouthistChanged(self, *args):
        l = self.rbLouthist.GetSelection()
        if l == 1:
            self.szrRIc2rows.Hide(self.szrHistcalcfreq)
            self.szrRIc2rows.Hide(self.szrHistdumpfreq)
        else:
            self.szrRIc2rows.Show(self.szrHistcalcfreq)
            self.szrRIc2rows.Show(self.szrHistdumpfreq)
        self.szrRIc2rows.Layout()
        self.szrRIMainColumns.Fit(self.pnRunInfo)
        self.pnRunInfo.Refresh()
        return
        
    def StepstyleChanged(self, *args):
        l = self.cboStepstyle.GetStringSelection()
        if l == "minimize":
            self.szrRIc1rows.Hide(self.szrNstep)
            self.szrRIc1rows.Show(self.szrOptstyle)
            self.szrRIc1rows.Show(self.szrMintol)
        else:
            self.szrRIc1rows.Show(self.szrNstep)
            self.szrRIc1rows.Hide(self.szrOptstyle)
            self.szrRIc1rows.Hide(self.szrMintol)
        self.towhee.set_stepstyle(l)
        self.szrRIMainColumns.Fit(self.pnRunInfo)
        self.Layout()
        return
    #
    # Functions to handle the logic for the Force Field tab
    #
    def ClassicalPotentialChanged(self, *args):
        cp = self.cboClassicalPotential.GetStringSelection()
        self.towhee.set_classical_potential(cp)
        self.DynamicUpdate_FF()
        return
        
    def CoulombstyleChanged(self, *args):
        l = self.cboCoulombstyle.GetStringSelection()
        self.towhee.set_coulombstyle(l)
        self.DynamicUpdate_FF()
        return

    def FfnumberChanged(self, *args):
        l = self.txtFfnumber.GetValue()
        if l.isdigit():
            l = int(l)
            if l == 0:
                return
            ffnumber = self.towhee.get_ffnumber()
            if l > ffnumber:
                for i in range(ffnumber, l):
                    self.txtFf_filename.append(wx.TextCtrl(self.pnFF, -1, "", size=(400,-1)))
                    self.szrFilenames.Add(self.txtFf_filename[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            elif l < ffnumber:
                for i in range(l, ffnumber):
                    self.szrFilenames.Remove(self.txtFf_filename[-1])
                    self.txtFf_filename[-1].Destroy()
                    self.txtFf_filename.pop()
            
            self.towhee.set_ffnumber(l)
            self.szrFilenames.Layout()
            self.szrFf_filename.Layout()
            self.szrFFc2rows.Layout()
            self.pnFF.Refresh()
        return

    def NfieldChanged(self, *args):
        l = self.txtNfield.GetValue()
        if l.isdigit():
            l = int(l)
            if l == 0:
                self.pnExternalFields.Hide()
            elif l > 0:
                self.pnExternalFields.Show()

            if l > self.towhee.get_nfield():
                for i in range(self.towhee.get_nfield(), l):
                    self.lblFieldType.append(wx.StaticText(self.pnExternalFields, -1, "Field Type", size=(80,-1), style=wx.ALIGN_RIGHT))
                    self.cboFieldType.append(wx.ComboBox(self.pnExternalFields, -1, choices=[\
                        "Hard Wall",\
                        "Harmonic Attractor",\
                        "LJ 9-3 Wall",\
                        "Hooper Umbrella",\
                        "Steele Wall"],\
                        style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(200,-1)))
                    self.cboFieldType[i].SetValue("Hard Wall")
                    self.fieldtypeID.append(self.cboFieldType[i].GetId())
                    wx.EVT_COMBOBOX(self, self.fieldtypeID[-1], self.FieldTypeChanged)
                    new_ef = self.towhee.create_externalfield("Hard Wall")
                    self.towhee.append_externalfields(new_ef)
                    self.lblHrdEnergyType.append(wx.StaticText(self.pnExternalFields, -1, "hrd_energy_wall", style=wx.ALIGN_RIGHT))
                    hrdsize = self.lblHrdEnergyType[0].GetSize()
                    self.lblHrdbox.append(wx.StaticText(self.pnExternalFields, -1, "hrdbox", size=hrdsize, style=wx.ALIGN_RIGHT))
                    self.txtHrdbox.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblHrdxyz.append(wx.StaticText(self.pnExternalFields, -1, "hrdxyz", size=hrdsize, style=wx.ALIGN_RIGHT))
                    self.txtHrdxyz.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblHrdcen.append(wx.StaticText(self.pnExternalFields, -1, "hrdcen", size=hrdsize, style=wx.ALIGN_RIGHT))
                    self.txtHrdcen.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblHrdrad.append(wx.StaticText(self.pnExternalFields, -1, "hrdrad", size=hrdsize, style=wx.ALIGN_RIGHT))
                    self.txtHrdrad.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.cboHrdEnergyType.append(wx.ComboBox(self.pnExternalFields, -1,\
                        choices=["infinite", "finite"],\
                        style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
                    self.cboHrdEnergyType[-1].SetStringSelection("infinite")
                    self.hrdenergytypeID.append(self.cboHrdEnergyType[-1].GetId())
                    wx.EVT_COMBOBOX(self, self.hrdenergytypeID[-1], self.HrdEnergyTypeChanged)
                    self.lblHrdWallEnergy.append(wx.StaticText(self.pnExternalFields, -1, "hrd_wall_energy", size=hrdsize, style=wx.ALIGN_RIGHT))
                    self.txtHrdWallEnergy.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.szrExternalField.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                        "External Field " + str(i+1)), wx.VERTICAL))
                    self.szrFieldType.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrField.append(wx.BoxSizer(wx.VERTICAL))
                    self.szrHrdrad.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHrdcen.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHrdxyz.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHrdbox.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHrdEnergyType.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHrdWallEnergy.append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrFieldType[i].Add(self.lblFieldType[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrFieldType[i].Add(self.cboFieldType[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdbox[-1].Add(self.lblHrdbox[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdbox[-1].Add(self.txtHrdbox[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdxyz[-1].Add(self.lblHrdxyz[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdxyz[-1].Add(self.txtHrdxyz[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdcen[-1].Add(self.lblHrdcen[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdcen[-1].Add(self.txtHrdcen[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdrad[-1].Add(self.lblHrdrad[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdrad[-1].Add(self.txtHrdrad[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdEnergyType[-1].Add(self.lblHrdEnergyType[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdEnergyType[-1].Add(self.cboHrdEnergyType[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdWallEnergy[-1].Add(self.lblHrdWallEnergy[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHrdWallEnergy[-1].Add(self.txtHrdWallEnergy[-1], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrField[i].Add(self.szrHrdbox[-1], 0, wx.EXPAND, 0)
                    self.szrField[i].Add(self.szrHrdxyz[-1], 0, wx.EXPAND, 0)
                    self.szrField[i].Add(self.szrHrdcen[-1], 0, wx.EXPAND, 0)
                    self.szrField[i].Add(self.szrHrdrad[-1], 0, wx.EXPAND, 0)
                    self.szrField[i].Add(self.szrHrdEnergyType[-1], 0, wx.EXPAND, 0)
                    self.szrField[i].Add(self.szrHrdWallEnergy[-1], 0, wx.EXPAND, 0)
                    self.szrField[i].Hide(self.szrHrdWallEnergy[-1])
                    self.szrExternalField[i].Add(self.szrFieldType[i], 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
                    self.szrExternalField[i].Add(self.szrField[i], 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2)
                    self.szrExternalFieldList.Add(self.szrExternalField[i], 0, 0, 0)
            elif l < self.towhee.get_nfield():
                for i in range(l, self.towhee.get_nfield()):
                    field_type = self.cboFieldType[-1].GetValue()
                    if field_type == "Hard Wall":
                        self.lblHrdbox[-1].Destroy()
                        self.txtHrdbox[-1].Destroy()
                        self.lblHrdxyz[-1].Destroy()
                        self.txtHrdxyz[-1].Destroy()
                        self.lblHrdcen[-1].Destroy()
                        self.txtHrdcen[-1].Destroy()
                        self.lblHrdrad[-1].Destroy()
                        self.txtHrdrad[-1].Destroy()
                        self.lblHrdEnergyType[-1].Destroy()
                        self.cboHrdEnergyType[-1].Destroy()
                        self.lblHrdWallEnergy[-1].Destroy()
                        self.txtHrdWallEnergy[-1].Destroy()
                        self.szrHrdbox.pop()
                        self.szrHrdxyz.pop()
                        self.szrHrdcen.pop()
                        self.szrHrdrad.pop()
                        self.szrHrdEnergyType.pop()
                        self.szrHrdWallEnergy.pop()
                        self.lblHrdbox.pop()
                        self.txtHrdbox.pop()
                        self.lblHrdxyz.pop()
                        self.txtHrdxyz.pop()
                        self.lblHrdcen.pop()
                        self.txtHrdcen.pop()
                        self.lblHrdrad.pop()
                        self.txtHrdrad.pop()
                        self.lblHrdEnergyType.pop()
                        self.cboHrdEnergyType.pop()
                        self.lblHrdWallEnergy.pop()
                        self.txtHrdWallEnergy.pop()
                        self.hrdenergytypeID.pop()
                    elif field_type == "Hooper Umbrella":
                        self.lblUmbbox[-1].Destroy()
                        self.txtUmbbox[-1].Destroy()
                        self.lblUmbxyz[-1].Destroy()
                        self.txtUmbxyz[-1].Destroy()
                        self.lblUmbcenter[-1].Destroy()
                        self.txtUmbcenter[-1].Destroy()
                        self.lblUmba[-1].Destroy()
                        self.txtUmba[-1].Destroy()
                        self.szrUmbbox.pop()
                        self.szrUmbxyz.pop()
                        self.szrUmbcenter.pop()
                        self.szrUmba.pop()
                        self.lblUmbbox.pop()
                        self.txtUmbbox.pop()
                        self.lblUmbxyz.pop()
                        self.txtUmbxyz.pop()
                        self.lblUmbcenter.pop()
                        self.txtUmbcenter.pop()
                        self.lblUmba.pop()
                        self.txtUmba.pop()
                    elif field_type == "Harmonic Attractor":
                        for j in range(int(self.txtHafnentries[-1].GetValue())):
                            self.lblHafmolec[-1][j].Destroy()
                            self.txtHafmolec[-1][j].Destroy()
                            self.lblHafelement[-1][j].Destroy()
                            self.txtHafelement[-1][j].Destroy()
                            self.lblHafname[-1][j].Destroy()
                            self.txtHafname[-1][j].Destroy()
                            b = self.szrHafkeyValues[-1][j].GetStaticBox()
                            b.Destroy()
                        self.lblHafbox[-1].Destroy()
                        self.txtHafbox[-1].Destroy()
                        self.lblHafk[-1].Destroy()
                        self.txtHafk[-1].Destroy()
                        self.lblHafnentries[-1].Destroy()
                        self.txtHafnentries[-1].Destroy()
                        self.lblHafrefpos[-1].Destroy()
                        self.cboHafrefpos[-1].Destroy()
                        self.lblHafglobxyz[-1].Destroy()
                        self.txtHafglobx[-1].Destroy()
                        self.txtHafgloby[-1].Destroy()
                        self.txtHafglobz[-1].Destroy()
                        self.lblHafkey[-1].Destroy()
                        self.cboHafkey[-1].Destroy()

                        self.lblHafbox.pop()
                        self.txtHafbox.pop()
                        self.lblHafk.pop()
                        self.txtHafk.pop()
                        self.lblHafnentries.pop()
                        self.txtHafnentries.pop()
                        self.lblHafrefpos.pop()
                        self.cboHafrefpos.pop()
                        self.lblHafglobxyz.pop()
                        self.txtHafglobx.pop()
                        self.txtHafgloby.pop()
                        self.txtHafglobz.pop()
                        self.lblHafkey.pop()
                        self.cboHafkey.pop()
                        self.lblHafmolec.pop()
                        self.txtHafmolec.pop()
                        self.lblHafelement.pop()
                        self.txtHafelement.pop()
                        self.lblHafname.pop()
                        self.txtHafname.pop()

                        self.szrHafbox.pop()
                        self.szrHafk.pop()
                        self.szrHafnentries.pop()
                        self.szrHafrefpos.pop()
                        self.szrHafglobxyz.pop()
                        self.szrHafkey.pop()
                        self.szrHafkeyList.pop()
                        self.szrHafkeyValues.pop()
                        self.szrHafmolec.pop()
                        self.szrHafelement.pop()
                        self.szrHafname.pop()
                        self.hafnentriesID.pop()
                        self.hafrefposID.pop()
                        self.hafkeyID.pop()
                    elif field_type == "LJ 9-3 Wall":
                        for j in range(int(self.txtLjfntypes[-1].GetValue())):
                            self.lblLjfname[-1][j].Destroy()
                            self.txtLjfname[-1][j].Destroy()
                            self.lblLjfsig[-1][j].Destroy()
                            self.txtLjfsig[-1][j].Destroy()
                            self.lblLjfeps[-1][j].Destroy()
                            self.txtLjfeps[-1][j].Destroy()
                            b = self.szrLjfntypesValues[-1][j].GetStaticBox()
                            b.Destroy()
                        self.lblLjfbox[-1].Destroy()
                        self.txtLjfbox[-1].Destroy()
                        self.lblLjfxyz[-1].Destroy()
                        self.txtLjfxyz[-1].Destroy()
                        self.lblLjfcen[-1].Destroy()
                        self.txtLjfcen[-1].Destroy()
                        self.lblLjfdir[-1].Destroy()
                        self.txtLjfdir[-1].Destroy()
                        self.lblLjfcut[-1].Destroy()
                        self.txtLjfcut[-1].Destroy()
                        self.lblLjfshift[-1].Destroy()
                        self.rbLjfshift[-1].Destroy()
                        self.lblLjfrho[-1].Destroy()
                        self.txtLjfrho[-1].Destroy()
                        self.lblLjfntypes[-1].Destroy()
                        self.txtLjfntypes[-1].Destroy()
                        self.lblLjfbox.pop()
                        self.txtLjfbox.pop()
                        self.lblLjfxyz.pop()
                        self.txtLjfxyz.pop()
                        self.lblLjfcen.pop()
                        self.txtLjfcen.pop()
                        self.lblLjfdir.pop()
                        self.txtLjfdir.pop()
                        self.lblLjfcut.pop()
                        self.txtLjfcut.pop()
                        self.lblLjfshift.pop()
                        self.rbLjfshift.pop()
                        self.lblLjfrho.pop()
                        self.txtLjfrho.pop()
                        self.lblLjfntypes.pop()
                        self.txtLjfntypes.pop()
                        self.lblLjfname.pop()
                        self.txtLjfname.pop()
                        self.lblLjfsig.pop()
                        self.txtLjfsig.pop()
                        self.lblLjfeps.pop()
                        self.txtLjfeps.pop()
                        self.szrLjfbox.pop()
                        self.szrLjfxyz.pop()
                        self.szrLjfcen.pop()
                        self.szrLjfdir.pop()
                        self.szrLjfcut.pop()
                        self.szrLjfshift.pop()
                        self.szrLjfrho.pop()
                        self.szrLjfntypes.pop()
                        self.szrLjfntypesList.pop()
                        self.szrLjfntypesValues.pop()
                        self.szrLjfname.pop()
                        self.szrLjfsig.pop()
                        self.szrLjfeps.pop()
                        self.ljfntypesID.pop()
                    elif field_type == "Steele Wall":
                        for j in range(int(self.txtSteelentype[-1].GetValue())):
                            self.lblSteelename[-1][j].Destroy()
                            self.txtSteelename[-1][j].Destroy()
                            self.lblSteelesigma_sf[-1][j].Destroy()
                            self.txtSteelesigma_sf[-1][j].Destroy()
                            self.lblSteeleepsilon_sf[-1][j].Destroy()
                            self.txtSteeleepsilon_sf[-1][j].Destroy()
                            b = self.szrSteelentypeValues[-1][j].GetStaticBox()
                            b.Destroy()
                        self.lblSteelebox[-1].Destroy()
                        self.txtSteelebox[-1].Destroy()
                        self.lblSteelexyz[-1].Destroy()
                        self.txtSteelexyz[-1].Destroy()
                        self.lblSteelesurface[-1].Destroy()
                        self.txtSteelesurface[-1].Destroy()
                        self.lblSteeledir[-1].Destroy()
                        self.txtSteeledir[-1].Destroy()
                        self.lblSteelecutoff[-1].Destroy()
                        self.txtSteelecutoff[-1].Destroy()
                        self.lblSteeleshift[-1].Destroy()
                        self.rbSteeleshift[-1].Destroy()
                        self.lblSteeledelta[-1].Destroy()
                        self.txtSteeledelta[-1].Destroy()
                        self.lblSteelerho_s[-1].Destroy()
                        self.txtSteelerho_s[-1].Destroy()
                        self.lblSteelentype[-1].Destroy()
                        self.txtSteelentype[-1].Destroy()
                        self.lblSteelebox.pop()
                        self.txtSteelebox.pop()
                        self.lblSteelexyz.pop()
                        self.txtSteelexyz.pop()
                        self.lblSteelesurface.pop()
                        self.txtSteelesurface.pop()
                        self.lblSteeledir.pop()
                        self.txtSteeledir.pop()
                        self.lblSteelecutoff.pop()
                        self.txtSteelecutoff.pop()
                        self.lblSteeleshift.pop()
                        self.rbSteeleshift.pop()
                        self.lblSteeledelta.pop()
                        self.txtSteeledelta.pop()
                        self.lblSteelerho_s.pop()
                        self.txtSteelerho_s.pop()
                        self.lblSteelentype.pop()
                        self.txtSteelentype.pop()
                        self.lblSteelename.pop()
                        self.txtSteelename.pop()
                        self.lblSteelesigma_sf.pop()
                        self.txtSteelesigma_sf.pop()
                        self.lblSteeleepsilon_sf.pop()
                        self.txtSteeleepsilon_sf.pop()
                        self.szrSteelebox.pop()
                        self.szrSteelexyz.pop()
                        self.szrSteelesurface.pop()
                        self.szrSteeledir.pop()
                        self.szrSteelecutoff.pop()
                        self.szrSteeleshift.pop()
                        self.szrSteeledelta.pop()
                        self.szrSteelerho_s.pop()
                        self.szrSteelentype.pop()
                        self.szrSteelentypeList.pop()
                        self.szrSteelentypeValues.pop()
                        self.szrSteelename.pop()
                        self.szrSteelesigma_sf.pop()
                        self.szrSteeleepsilon_sf.pop()
                        self.steelentypeID.pop()

                    b = self.szrExternalField[-1].GetStaticBox()
                    b.Destroy()
                    self.szrExternalFieldList.Remove(self.szrExternalField[-1])
                    self.cboFieldType[-1].Destroy()
                    self.cboFieldType.pop()
                    self.lblFieldType[-1].Destroy()
                    self.lblFieldType.pop()
                    self.szrFieldType.pop()
                    self.szrField.pop()
                    self.szrExternalField.pop()
                    self.fieldtypeID.pop()

            self.towhee.set_nfield(l)
            self.szrExternalFieldList.FitInside(self.pnExternalFields)
            self.szrExternalFieldList.Layout()
            self.pnExternalFields.Refresh()
            self.Refresh()
        return

    def FindExternalFieldIndex(self, type, howFar):
        index = 0
        for i in range(howFar):
            ef = self.towhee.get_single_externalfield(i)
            if ef.get_fieldtype() == type:
                index+=1
        return index

    def FindFieldIndex(self, type, which_one):
        field_type_index = 0
        external_field_index = 0
        for i in range(self.towhee.get_nfield()):
            ef = self.cboFieldType[i].GetValue()
            if ef == type:
                external_field_index+=1
                if (which_one+1) == external_field_index:
                    return field_type_index
            field_type_index+=1

    def FieldTypeChanged(self, *args):
        field_type_index = self.fieldtypeID.index(args[0].GetId())
        newFieldType = self.cboFieldType[field_type_index].GetStringSelection()
        ef = self.towhee.get_single_externalfield(field_type_index)
        oldFieldType = ef.get_fieldtype()
        if oldFieldType == newFieldType:
            return

        if oldFieldType == "Hard Wall":
            field_index = self.FindExternalFieldIndex("Hard Wall", field_type_index)
            self.szrField[field_type_index].Remove(self.szrHrdbox[field_index])
            self.szrField[field_type_index].Remove(self.szrHrdxyz[field_index])
            self.szrField[field_type_index].Remove(self.szrHrdcen[field_index])
            self.szrField[field_type_index].Remove(self.szrHrdrad[field_index])
            self.szrField[field_type_index].Remove(self.szrHrdEnergyType[field_index])
            self.szrField[field_type_index].Remove(self.szrHrdWallEnergy[field_index])
            self.lblHrdbox[field_index].Destroy()
            self.txtHrdbox[field_index].Destroy()
            self.lblHrdxyz[field_index].Destroy()
            self.txtHrdxyz[field_index].Destroy()
            self.lblHrdcen[field_index].Destroy()
            self.txtHrdcen[field_index].Destroy()
            self.lblHrdrad[field_index].Destroy()
            self.txtHrdrad[field_index].Destroy()
            self.lblHrdEnergyType[field_index].Destroy()
            self.cboHrdEnergyType[field_index].Destroy()
            self.lblHrdWallEnergy[field_index].Destroy()
            self.txtHrdWallEnergy[field_index].Destroy()
            del self.lblHrdbox[field_index]
            del self.txtHrdbox[field_index]
            del self.lblHrdxyz[field_index]
            del self.txtHrdxyz[field_index]
            del self.lblHrdcen[field_index]
            del self.txtHrdcen[field_index]
            del self.lblHrdrad[field_index]
            del self.txtHrdrad[field_index]
            del self.lblHrdEnergyType[field_index]
            del self.cboHrdEnergyType[field_index]
            del self.lblHrdWallEnergy[field_index]
            del self.txtHrdWallEnergy[field_index]
            del self.szrHrdbox[field_index]
            del self.szrHrdxyz[field_index]
            del self.szrHrdcen[field_index]
            del self.szrHrdrad[field_index]
            del self.szrHrdEnergyType[field_index]
            del self.szrHrdWallEnergy[field_index]
            del self.hrdenergytypeID[field_index]
        elif oldFieldType == "Harmonic Attractor":
            field_index = self.FindExternalFieldIndex("Harmonic Attractor", field_type_index)
            for j in range(ef.get_nentries()):
                self.lblHafmolec[field_index][j].Destroy()
                self.txtHafmolec[field_index][j].Destroy()
                self.lblHafelement[field_index][j].Destroy()
                self.txtHafelement[field_index][j].Destroy()
                self.lblHafname[field_index][j].Destroy()
                self.txtHafname[field_index][j].Destroy()
                b = self.szrHafkeyValues[field_index][j].GetStaticBox()
                b.Destroy()
            self.szrField[field_type_index].Remove(self.szrHafbox[field_index])
            self.szrField[field_type_index].Remove(self.szrHafk[field_index])
            self.szrField[field_type_index].Remove(self.szrHafnentries[field_index])
            self.szrField[field_type_index].Remove(self.szrHafrefpos[field_index])
            self.szrField[field_type_index].Remove(self.szrHafglobxyz[field_index])
            self.szrField[field_type_index].Remove(self.szrHafkey[field_index])
            self.szrField[field_type_index].Remove(self.szrHafkeyList[field_index])
            self.lblHafbox[field_index].Destroy()
            self.txtHafbox[field_index].Destroy()
            self.lblHafk[field_index].Destroy()
            self.txtHafk[field_index].Destroy()
            self.lblHafnentries[field_index].Destroy()
            self.txtHafnentries[field_index].Destroy()
            self.lblHafrefpos[field_index].Destroy()
            self.cboHafrefpos[field_index].Destroy()
            self.lblHafglobxyz[field_index].Destroy()
            self.txtHafglobx[field_index].Destroy()
            self.txtHafgloby[field_index].Destroy()
            self.txtHafglobz[field_index].Destroy()
            self.lblHafkey[field_index].Destroy()
            self.cboHafkey[field_index].Destroy()
            del self.lblHafbox[field_index]
            del self.txtHafbox[field_index]
            del self.lblHafk[field_index]
            del self.txtHafk[field_index]
            del self.lblHafnentries[field_index]
            del self.txtHafnentries[field_index]
            del self.lblHafrefpos[field_index]
            del self.cboHafrefpos[field_index]
            del self.lblHafglobxyz[field_index]
            del self.txtHafglobx[field_index]
            del self.txtHafgloby[field_index]
            del self.txtHafglobz[field_index]
            del self.lblHafkey[field_index]
            del self.cboHafkey[field_index]
            del self.lblHafmolec[field_index]
            del self.txtHafmolec[field_index]
            del self.lblHafelement[field_index]
            del self.txtHafelement[field_index]
            del self.lblHafname[field_index]
            del self.txtHafname[field_index]
            del self.szrHafbox[field_index]
            del self.szrHafk[field_index]
            del self.szrHafnentries[field_index]
            del self.szrHafrefpos[field_index]
            del self.szrHafglobxyz[field_index]
            del self.szrHafkey[field_index]
            del self.szrHafkeyList[field_index]
            del self.szrHafkeyValues[field_index]
            del self.szrHafmolec[field_index]
            del self.szrHafelement[field_index]
            del self.szrHafname[field_index]
            del self.hafnentriesID[field_index]
            del self.hafrefposID[field_index]
            del self.hafkeyID[field_index]
        elif oldFieldType == "LJ 9-3 Wall":
            field_index = self.FindExternalFieldIndex("LJ 9-3 Wall", field_type_index)
            for j in range(ef.get_ntypes()):
                self.lblLjfname[field_index][j].Destroy()
                self.txtLjfname[field_index][j].Destroy()
                self.lblLjfsig[field_index][j].Destroy()
                self.txtLjfsig[field_index][j].Destroy()
                self.lblLjfeps[field_index][j].Destroy()
                self.txtLjfeps[field_index][j].Destroy()
                b = self.szrLjfntypesValues[field_index][j].GetStaticBox()
                b.Destroy()
            self.szrField[field_type_index].Remove(self.szrLjfbox[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfxyz[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfcen[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfdir[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfcut[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfshift[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfrho[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfntypes[field_index])
            self.szrField[field_type_index].Remove(self.szrLjfntypesList[field_index])
            self.lblLjfbox[field_index].Destroy()
            self.txtLjfbox[field_index].Destroy()
            self.lblLjfxyz[field_index].Destroy()
            self.txtLjfxyz[field_index].Destroy()
            self.lblLjfcen[field_index].Destroy()
            self.txtLjfcen[field_index].Destroy()
            self.lblLjfdir[field_index].Destroy()
            self.txtLjfdir[field_index].Destroy()
            self.lblLjfcut[field_index].Destroy()
            self.txtLjfcut[field_index].Destroy()
            self.lblLjfshift[field_index].Destroy()
            self.rbLjfshift[field_index].Destroy()
            self.lblLjfrho[field_index].Destroy()
            self.txtLjfrho[field_index].Destroy()
            self.lblLjfntypes[field_index].Destroy()
            self.txtLjfntypes[field_index].Destroy()
            del self.lblLjfbox[field_index]
            del self.txtLjfbox[field_index]
            del self.lblLjfxyz[field_index]
            del self.txtLjfxyz[field_index]
            del self.lblLjfcen[field_index]
            del self.txtLjfcen[field_index]
            del self.lblLjfdir[field_index]
            del self.txtLjfdir[field_index]
            del self.lblLjfcut[field_index]
            del self.txtLjfcut[field_index]
            del self.lblLjfshift[field_index]
            del self.rbLjfshift[field_index]
            del self.lblLjfrho[field_index]
            del self.txtLjfrho[field_index]
            del self.lblLjfntypes[field_index]
            del self.txtLjfntypes[field_index]
            del self.lblLjfname[field_index]
            del self.txtLjfname[field_index]
            del self.lblLjfsig[field_index]
            del self.txtLjfsig[field_index]
            del self.lblLjfeps[field_index]
            del self.txtLjfeps[field_index]
            del self.szrLjfbox[field_index]
            del self.szrLjfxyz[field_index]
            del self.szrLjfcen[field_index]
            del self.szrLjfdir[field_index]
            del self.szrLjfcut[field_index]
            del self.szrLjfshift[field_index]
            del self.szrLjfrho[field_index]
            del self.szrLjfntypes[field_index]
            del self.szrLjfntypesList[field_index]
            del self.szrLjfntypesValues[field_index]
            del self.szrLjfname[field_index]
            del self.szrLjfsig[field_index]
            del self.szrLjfeps[field_index]
            del self.ljfntypesID[field_index]
        elif oldFieldType == "Hooper Umbrella":
            field_index = self.FindExternalFieldIndex("Hooper Umbrella", field_type_index)
            self.szrField[field_type_index].Remove(self.szrUmbbox[field_index])
            self.szrField[field_type_index].Remove(self.szrUmbxyz[field_index])
            self.szrField[field_type_index].Remove(self.szrUmbcenter[field_index])
            self.szrField[field_type_index].Remove(self.szrUmba[field_index])
            self.lblUmbbox[field_index].Destroy()
            self.txtUmbbox[field_index].Destroy()
            self.lblUmbxyz[field_index].Destroy()
            self.txtUmbxyz[field_index].Destroy()
            self.lblUmbcenter[field_index].Destroy()
            self.txtUmbcenter[field_index].Destroy()
            self.lblUmba[field_index].Destroy()
            self.txtUmba[field_index].Destroy()
            del self.lblUmbbox[field_index]
            del self.txtUmbbox[field_index]
            del self.lblUmbxyz[field_index]
            del self.txtUmbxyz[field_index]
            del self.lblUmbcenter[field_index]
            del self.txtUmbcenter[field_index]
            del self.lblUmba[field_index]
            del self.txtUmba[field_index]
            del self.szrUmbbox[field_index]
            del self.szrUmbxyz[field_index]
            del self.szrUmbcenter[field_index]
            del self.szrUmba[field_index]
        elif oldFieldType == "Steele Wall":
            field_index = self.FindExternalFieldIndex("Steele Wall", field_type_index)
            for j in range(ef.get_ntype()):
                self.lblSteelename[field_index][j].Destroy()
                self.txtSteelename[field_index][j].Destroy()
                self.lblSteelesigma_sf[field_index][j].Destroy()
                self.txtSteelesigma_sf[field_index][j].Destroy()
                self.lblSteeleepsilon_sf[field_index][j].Destroy()
                self.txtSteeleepsilon_sf[field_index][j].Destroy()
                b = self.szrSteelentypeValues[field_index][j].GetStaticBox()
                b.Destroy()
            self.szrField[field_type_index].Remove(self.szrSteelebox[field_index])
            self.szrField[field_type_index].Remove(self.szrSteelexyz[field_index])
            self.szrField[field_type_index].Remove(self.szrSteelesurface[field_index])
            self.szrField[field_type_index].Remove(self.szrSteeledir[field_index])
            self.szrField[field_type_index].Remove(self.szrSteelecutoff[field_index])
            self.szrField[field_type_index].Remove(self.szrSteeleshift[field_index])
            self.szrField[field_type_index].Remove(self.szrSteeledelta[field_index])
            self.szrField[field_type_index].Remove(self.szrSteelerho_s[field_index])
            self.szrField[field_type_index].Remove(self.szrSteelentype[field_index])
            self.szrField[field_type_index].Remove(self.szrSteelentypeList[field_index])
            self.lblSteelebox[field_index].Destroy()
            self.txtSteelebox[field_index].Destroy()
            self.lblSteelexyz[field_index].Destroy()
            self.txtSteelexyz[field_index].Destroy()
            self.lblSteelesurface[field_index].Destroy()
            self.txtSteelesurface[field_index].Destroy()
            self.lblSteeledir[field_index].Destroy()
            self.txtSteeledir[field_index].Destroy()
            self.lblSteelecutoff[field_index].Destroy()
            self.txtSteelecutoff[field_index].Destroy()
            self.lblSteeleshift[field_index].Destroy()
            self.rbSteeleshift[field_index].Destroy()
            self.lblSteeledelta[field_index].Destroy()
            self.txtSteeledelta[field_index].Destroy()
            self.lblSteelerho_s[field_index].Destroy()
            self.txtSteelerho_s[field_index].Destroy()
            self.lblSteelentype[field_index].Destroy()
            self.txtSteelentype[field_index].Destroy()
            del self.lblSteelebox[field_index]
            del self.txtSteelebox[field_index]
            del self.lblSteelexyz[field_index]
            del self.txtSteelexyz[field_index]
            del self.lblSteelesurface[field_index]
            del self.txtSteelesurface[field_index]
            del self.lblSteeledir[field_index]
            del self.txtSteeledir[field_index]
            del self.lblSteelecutoff[field_index]
            del self.txtSteelecutoff[field_index]
            del self.lblSteeleshift[field_index]
            del self.rbSteeleshift[field_index]
            del self.lblSteeledelta[field_index]
            del self.txtSteeledelta[field_index]
            del self.lblSteelerho_s[field_index]
            del self.txtSteelerho_s[field_index]
            del self.lblSteelentype[field_index]
            del self.txtSteelentype[field_index]
            del self.lblSteelename[field_index]
            del self.txtSteelename[field_index]
            del self.lblSteelesigma_sf[field_index]
            del self.txtSteelesigma_sf[field_index]
            del self.lblSteeleepsilon_sf[field_index]
            del self.txtSteeleepsilon_sf[field_index]
            del self.szrSteelebox[field_index]
            del self.szrSteelexyz[field_index]
            del self.szrSteelesurface[field_index]
            del self.szrSteeledir[field_index]
            del self.szrSteelecutoff[field_index]
            del self.szrSteeleshift[field_index]
            del self.szrSteeledelta[field_index]
            del self.szrSteelerho_s[field_index]
            del self.szrSteelentype[field_index]
            del self.szrSteelentypeList[field_index]
            del self.szrSteelentypeValues[field_index]
            del self.szrSteelename[field_index]
            del self.szrSteelesigma_sf[field_index]
            del self.szrSteeleepsilon_sf[field_index]
            del self.steelentypeID[field_index]

        if newFieldType == "Hard Wall":
            field_index = self.FindExternalFieldIndex("Hard Wall", field_type_index)
            self.lblHrdEnergyType.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hrd_energy_type", style=wx.ALIGN_RIGHT))
            hrdsize = self.lblHrdEnergyType[0].GetSize()
            self.lblHrdbox.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hrdbox", size=hrdsize, style=wx.ALIGN_RIGHT))
            self.txtHrdbox.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHrdxyz.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hrdxyz", style=wx.ALIGN_RIGHT, size=hrdsize))
            self.txtHrdxyz.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHrdcen.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hrdcen", style=wx.ALIGN_RIGHT, size=hrdsize))
            self.txtHrdcen.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHrdrad.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hrdrad", style=wx.ALIGN_RIGHT, size=hrdsize))
            self.txtHrdrad.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.cboHrdEnergyType.insert(field_index, wx.ComboBox(self.pnExternalFields, -1,\
                choices=["infinite", "finite"],\
                style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
            self.cboHrdEnergyType[field_index].SetStringSelection("infinite")
            self.hrdenergytypeID.insert(field_index, self.cboHrdEnergyType[field_index].GetId())
            wx.EVT_COMBOBOX(self, self.hrdenergytypeID[field_index], self.HrdEnergyTypeChanged)
            self.lblHrdWallEnergy.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hrd_wall_energy", size=hrdsize, style=wx.ALIGN_RIGHT))
            self.txtHrdWallEnergy.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.szrHrdrad.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHrdcen.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHrdxyz.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHrdbox.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHrdEnergyType.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHrdWallEnergy.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHrdbox[field_index].Add(self.lblHrdbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdbox[field_index].Add(self.txtHrdbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdxyz[field_index].Add(self.lblHrdxyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdxyz[field_index].Add(self.txtHrdxyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdcen[field_index].Add(self.lblHrdcen[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdcen[field_index].Add(self.txtHrdcen[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdrad[field_index].Add(self.lblHrdrad[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdrad[field_index].Add(self.txtHrdrad[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdEnergyType[field_index].Add(self.lblHrdEnergyType[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdEnergyType[field_index].Add(self.cboHrdEnergyType[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdWallEnergy[field_index].Add(self.lblHrdWallEnergy[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHrdWallEnergy[field_index].Add(self.txtHrdWallEnergy[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrField[field_type_index].Add(self.szrHrdbox[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHrdxyz[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHrdcen[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHrdrad[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHrdEnergyType[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHrdWallEnergy[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Hide(self.szrHrdWallEnergy[field_index])
        if newFieldType == "Harmonic Attractor":
            field_index = self.FindExternalFieldIndex("Harmonic Attractor", field_type_index)
            self.lblHafnentries.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hafnentries", style=wx.ALIGN_RIGHT))
            hasize = self.lblHafnentries[0].GetSize()
            self.lblHafbox.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hafbox", size=hasize, style=wx.ALIGN_RIGHT))
            self.txtHafbox.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHafk.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hafk", size=hasize, style=wx.ALIGN_RIGHT))
            self.txtHafk.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.txtHafnentries.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, "1"))
            self.hafnentriesID.insert(field_index, self.txtHafnentries[field_index].GetId())
            wx.EVT_TEXT(self, self.hafnentriesID[field_index], self.HafnentriesChanged)
            self.lblHafrefpos.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hafrefpos", size=hasize, style=wx.ALIGN_RIGHT))
            self.cboHafrefpos.insert(field_index, wx.ComboBox(self.pnExternalFields, -1,\
                choices=["Global", "Initial"],\
                style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
            self.cboHafrefpos[field_index].SetStringSelection("Initial")
            self.hafrefposID.insert(field_index, self.cboHafrefpos[field_index].GetId())
            wx.EVT_COMBOBOX(self, self.hafrefposID[field_index], self.HafrefposChanged)
            self.lblHafglobxyz.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hafglobxyz", size=hasize, style=wx.ALIGN_RIGHT))
            self.txtHafglobx.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.txtHafgloby.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.txtHafglobz.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHafkey.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "hafkey", size=hasize, style=wx.ALIGN_RIGHT))
            self.cboHafkey.insert(field_index, wx.ComboBox(self.pnExternalFields, -1,\
                choices=["Element", "FFtype"],\
                style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
            self.cboHafkey[field_index].SetStringSelection("Element")
            self.hafkeyID.insert(field_index, self.cboHafkey[field_index].GetId())
            wx.EVT_COMBOBOX(self, self.hafkeyID[field_index], self.HafkeyChanged)
            TlblMolec = []
            TtxtMolec = []
            TlblMolec.append(wx.StaticText(self.pnExternalFields, -1, "hafmolec", size=hasize, style=wx.ALIGN_RIGHT))
            TtxtMolec.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHafmolec.insert(field_index, TlblMolec)
            self.txtHafmolec.insert(field_index, TtxtMolec)
            TlblElement = []
            TtxtElement = []
            TlblElement.append(wx.StaticText(self.pnExternalFields, -1, "hafelement", size=hasize, style=wx.ALIGN_RIGHT))
            TtxtElement.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHafelement.insert(field_index, TlblElement)
            self.txtHafelement.insert(field_index, TtxtElement)
            TlblName = []
            TtxtName = []
            TlblName.append(wx.StaticText(self.pnExternalFields, -1, "hafname", size=hasize, style=wx.ALIGN_RIGHT))
            TtxtName.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblHafname.insert(field_index, TlblName)
            self.txtHafname.insert(field_index, TtxtName)

            self.szrHafbox.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHafk.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHafnentries.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHafrefpos.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHafglobxyz.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHafkey.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrHafkeyList.insert(field_index, wx.BoxSizer(wx.VERTICAL))
            TszrhafkeyValues = []
            Tszrhafmolec = []
            Tszrhafelement = []
            Tszrhafname = []
            TszrhafkeyValues.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                "Entry 1"), wx.VERTICAL))
            Tszrhafmolec.append(wx.BoxSizer(wx.HORIZONTAL))
            Tszrhafelement.append(wx.BoxSizer(wx.HORIZONTAL))
            Tszrhafname.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrHafkeyValues.insert(field_index, TszrhafkeyValues)
            self.szrHafmolec.insert(field_index, Tszrhafmolec)
            self.szrHafelement.insert(field_index, Tszrhafelement)
            self.szrHafname.insert(field_index, Tszrhafname)
            
            self.szrHafbox[field_index].Add(self.lblHafbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafbox[field_index].Add(self.txtHafbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafk[field_index].Add(self.lblHafk[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafk[field_index].Add(self.txtHafk[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafnentries[field_index].Add(self.lblHafnentries[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafnentries[field_index].Add(self.txtHafnentries[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafrefpos[field_index].Add(self.lblHafrefpos[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafrefpos[field_index].Add(self.cboHafrefpos[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafglobxyz[field_index].Add(self.lblHafglobxyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafglobxyz[field_index].Add(self.txtHafglobx[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafglobxyz[field_index].Add(self.txtHafgloby[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafglobxyz[field_index].Add(self.txtHafglobz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafkey[field_index].Add(self.lblHafkey[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafkey[field_index].Add(self.cboHafkey[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafmolec[field_index][0].Add(self.lblHafmolec[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafmolec[field_index][0].Add(self.txtHafmolec[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafelement[field_index][0].Add(self.lblHafelement[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafelement[field_index][0].Add(self.txtHafelement[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafname[field_index][0].Add(self.lblHafname[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafname[field_index][0].Add(self.txtHafname[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrHafkeyValues[field_index][0].Add(self.szrHafmolec[field_index][0], 0, wx.EXPAND, 0)
            self.szrHafkeyValues[field_index][0].Add(self.szrHafelement[field_index][0], 0, wx.EXPAND, 0)
            self.szrHafkeyValues[field_index][0].Add(self.szrHafname[field_index][0], 0, wx.EXPAND, 0)
            self.szrHafkeyList[field_index].Add(self.szrHafkeyValues[field_index][0], 0, wx.LEFT, 50)

            self.szrField[field_type_index].Add(self.szrHafbox[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHafk[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHafnentries[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHafrefpos[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHafglobxyz[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHafkey[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrHafkeyList[field_index], 0, wx.EXPAND, 0)
            
            self.szrField[field_type_index].Hide(self.szrHafglobxyz[field_index])
            self.szrHafkeyValues[field_index][0].Hide(self.szrHafname[field_index][0])
        elif newFieldType == "LJ 9-3 Wall":
            field_index = self.FindExternalFieldIndex("LJ 9-3 Wall", field_type_index)
            self.lblLjfntypes.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfntypes",\
                style=wx.ALIGN_RIGHT))
            ljsize = self.lblLjfntypes[0].GetSize()
            self.txtLjfntypes.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, "1"))
            self.ljfntypesID.insert(field_index, self.txtLjfntypes[field_index].GetId())
            self.lblLjfbox.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfbox",\
                style=wx.ALIGN_RIGHT, size=ljsize))
            self.txtLjfbox.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblLjfxyz.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfxyz",\
                style=wx.ALIGN_RIGHT, size=ljsize))
            self.txtLjfxyz.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblLjfcen.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfcen",\
                style=wx.ALIGN_RIGHT, size=ljsize))
            self.txtLjfcen.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblLjfdir.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfdir",\
                style=wx.ALIGN_RIGHT, size=ljsize))
            self.txtLjfdir.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblLjfcut.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfcut",\
                style=wx.ALIGN_RIGHT, size=ljsize))
            self.txtLjfcut.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblLjfshift.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfshift", style=wx.ALIGN_RIGHT, size=ljsize))
            self.rbLjfshift.insert(field_index, wx.RadioBox(self.pnExternalFields, -1, "", choices=["True", "False"],\
                majorDimension=1, style=wx.RA_SPECIFY_ROWS))
            self.lblLjfrho.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "ljfrho", style=wx.ALIGN_RIGHT, size=ljsize))
            self.txtLjfrho.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            wx.EVT_TEXT(self, self.txtLjfntypes[field_index].GetId(), self.LjfntypesChanged)
            TlblLjfname = []
            TtxtLjfname = []
            TlblLjfsig = [] 
            TtxtLjfsig = []
            TlblLjfeps = []
            TtxtLjfeps = []
            TlblLjfname.append(wx.StaticText(self.pnExternalFields, -1, "ljfname", style=wx.ALIGN_RIGHT, size=ljsize))
            TtxtLjfname.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            TlblLjfsig.append(wx.StaticText(self.pnExternalFields, -1, "ljfsig", style=wx.ALIGN_RIGHT, size=ljsize))
            TtxtLjfsig.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            TlblLjfeps.append(wx.StaticText(self.pnExternalFields, -1, "ljfeps", style=wx.ALIGN_RIGHT, size=ljsize))
            TtxtLjfeps.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblLjfname.insert(field_index, TlblLjfname)
            self.txtLjfname.insert(field_index, TtxtLjfname)
            self.lblLjfsig.insert(field_index, TlblLjfsig)
            self.txtLjfsig.insert(field_index, TtxtLjfsig)
            self.lblLjfeps.insert(field_index, TlblLjfeps)
            self.txtLjfeps.insert(field_index, TtxtLjfeps)

            self.szrLjfbox.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfxyz.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfcen.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfdir.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfcut.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfshift.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfrho.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfntypes.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfntypesList.insert(field_index, wx.BoxSizer(wx.VERTICAL))
            TszrLjfntypesValues = []
            TszrLjfeps = []
            TszrLjfsig = []
            TszrLjfname = []
            TszrLjfntypesValues.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                "ljfntype 1"), wx.VERTICAL))
            TszrLjfeps.append(wx.BoxSizer(wx.HORIZONTAL))
            TszrLjfsig.append(wx.BoxSizer(wx.HORIZONTAL))
            TszrLjfname.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrLjfntypesValues.insert(field_index, TszrLjfntypesValues)
            self.szrLjfeps.insert(field_index, TszrLjfeps)
            self.szrLjfsig.insert(field_index, TszrLjfsig)
            self.szrLjfname.insert(field_index, TszrLjfname)
            
            self.szrLjfbox[field_index].Add(self.lblLjfbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfbox[field_index].Add(self.txtLjfbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfxyz[field_index].Add(self.lblLjfxyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfxyz[field_index].Add(self.txtLjfxyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfcen[field_index].Add(self.lblLjfcen[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfcen[field_index].Add(self.txtLjfcen[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfdir[field_index].Add(self.lblLjfdir[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfdir[field_index].Add(self.txtLjfdir[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfcut[field_index].Add(self.lblLjfcut[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfcut[field_index].Add(self.txtLjfcut[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfshift[field_index].Add(self.lblLjfshift[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfshift[field_index].Add(self.rbLjfshift[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfrho[field_index].Add(self.lblLjfrho[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfrho[field_index].Add(self.txtLjfrho[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfntypes[field_index].Add(self.lblLjfntypes[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfntypes[field_index].Add(self.txtLjfntypes[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfname[field_index][0].Add(self.lblLjfname[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfname[field_index][0].Add(self.txtLjfname[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfsig[field_index][0].Add(self.lblLjfsig[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfsig[field_index][0].Add(self.txtLjfsig[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfeps[field_index][0].Add(self.lblLjfeps[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfeps[field_index][0].Add(self.txtLjfeps[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrLjfntypesValues[field_index][0].Add(self.szrLjfname[field_index][0], 0, wx.EXPAND, 0)
            self.szrLjfntypesValues[field_index][0].Add(self.szrLjfsig[field_index][0], 0, wx.EXPAND, 0)
            self.szrLjfntypesValues[field_index][0].Add(self.szrLjfeps[field_index][0], 0, wx.EXPAND, 0)
            self.szrLjfntypesList[field_index].Add(self.szrLjfntypesValues[field_index][0], 0, wx.LEFT, 50)

            self.szrField[field_type_index].Add(self.szrLjfbox[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfxyz[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfcen[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfdir[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfcut[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfshift[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfrho[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfntypes[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrLjfntypesList[field_index], 0, wx.EXPAND, 0)
        elif newFieldType == "Hooper Umbrella":
            field_index = self.FindExternalFieldIndex("Hooper Umbrella", field_type_index)
            self.lblUmbcenter.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "umbcenter", style=wx.ALIGN_RIGHT))
            umbsize = self.lblUmbcenter[0].GetSize()
            self.txtUmbcenter.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblUmbbox.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "umbbox", style=wx.ALIGN_RIGHT, size=umbsize))
            self.txtUmbbox.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblUmbxyz.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "umbxyz", style=wx.ALIGN_RIGHT, size=umbsize))
            self.txtUmbxyz.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblUmba.insert(field_index, wx.StaticText(self.pnExternalFields, -1, "umba", style=wx.ALIGN_RIGHT, size=umbsize))
            self.txtUmba.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.szrUmba.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrUmbcenter.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrUmbxyz.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrUmbbox.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrUmbbox[field_index].Add(self.lblUmbbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrUmbbox[field_index].Add(self.txtUmbbox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrUmbxyz[field_index].Add(self.lblUmbxyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrUmbxyz[field_index].Add(self.txtUmbxyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrUmbcenter[field_index].Add(self.lblUmbcenter[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrUmbcenter[field_index].Add(self.txtUmbcenter[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrUmba[field_index].Add(self.lblUmba[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrUmba[field_index].Add(self.txtUmba[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrField[field_type_index].Add(self.szrUmbbox[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrUmbxyz[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrUmbcenter[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrUmba[field_index], 0, wx.EXPAND, 0)
        elif newFieldType == "Steele Wall":
            field_index = self.FindExternalFieldIndex("Steele Wall", field_type_index)
            self.lblSteelesurface.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele surface", style=wx.ALIGN_RIGHT))
            steelesize = self.lblSteelesurface[0].GetSize()
            self.txtSteelesurface.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteelebox.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele box", style=wx.ALIGN_RIGHT, size=steelesize))
            self.txtSteelebox.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteelexyz.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele xyz", style=wx.ALIGN_RIGHT, size=steelesize))
            self.txtSteelexyz.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteeledir.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele dir", style=wx.ALIGN_RIGHT, size=steelesize))
            self.txtSteeledir.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteelecutoff.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele cutoff", style=wx.ALIGN_RIGHT, size=steelesize))
            self.txtSteelecutoff.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteeleshift.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele shift", style=wx.ALIGN_RIGHT, size=steelesize))
            self.rbSteeleshift.insert(field_index, wx.RadioBox(self.pnExternalFields, -1, "",\
                choices=["True", "False"], majorDimension=1, style=wx.RA_SPECIFY_ROWS))
            self.lblSteeledelta.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele delta", style=wx.ALIGN_RIGHT, size=steelesize))
            self.txtSteeledelta.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteelerho_s.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele rho_s", style=wx.ALIGN_RIGHT, size=steelesize))
            self.txtSteelerho_s.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteelentype.insert(field_index, wx.StaticText(self.pnExternalFields, -1,\
                "steele ntype", style=wx.ALIGN_RIGHT, size=steelesize))
            self.txtSteelentype.insert(field_index, wx.TextCtrl(self.pnExternalFields, -1, "1"))
            self.steelentypeID.insert(field_index, self.txtSteelentype[field_index].GetId())
            wx.EVT_TEXT(self, self.txtSteelentype[field_index].GetId(), self.SteelentypeChanged)
            TlblSteelename = []
            TtxtSteelename = []
            TlblSteelesigma_sf = [] 
            TtxtSteelesigma_sf = []
            TlblSteeleepsilon_sf = []
            TtxtSteeleepsilon_sf = []
            TlblSteeleepsilon_sf.append(wx.StaticText(self.pnExternalFields, -1, "steele epsilon_sf",\
                style=wx.ALIGN_RIGHT))
            typesize = TlblSteeleepsilon_sf[0].GetSize()
            TtxtSteeleepsilon_sf.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            TlblSteelename.append(wx.StaticText(self.pnExternalFields, -1, "steele name",\
                style=wx.ALIGN_RIGHT, size=typesize))
            TtxtSteelename.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            TlblSteelesigma_sf.append(wx.StaticText(self.pnExternalFields, -1, "steele sigma_sf",\
                style=wx.ALIGN_RIGHT, size=typesize))
            TtxtSteelesigma_sf.append(wx.TextCtrl(self.pnExternalFields, -1, ""))
            self.lblSteelename.insert(field_index, TlblSteelename)
            self.txtSteelename.insert(field_index, TtxtSteelename)
            self.lblSteelesigma_sf.insert(field_index, TlblSteelesigma_sf)
            self.txtSteelesigma_sf.insert(field_index, TtxtSteelesigma_sf)
            self.lblSteeleepsilon_sf.insert(field_index, TlblSteeleepsilon_sf)
            self.txtSteeleepsilon_sf.insert(field_index, TtxtSteeleepsilon_sf)

            self.szrSteelebox.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteelexyz.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteelesurface.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteeledir.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteelecutoff.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteeleshift.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteeledelta.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteelerho_s.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteelentype.insert(field_index, wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteelentypeList.insert(field_index, wx.BoxSizer(wx.VERTICAL))
            TszrSteelentypeValues = []
            TszrSteeleeps = []
            TszrSteelesig = []
            TszrSteelename = []
            TszrSteelentypeValues.append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                "steele ntype 1"), wx.VERTICAL))
            TszrSteeleeps.append(wx.BoxSizer(wx.HORIZONTAL))
            TszrSteelesig.append(wx.BoxSizer(wx.HORIZONTAL))
            TszrSteelename.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrSteelentypeValues.insert(field_index, TszrSteelentypeValues)
            self.szrSteeleepsilon_sf.insert(field_index, TszrSteeleeps)
            self.szrSteelesigma_sf.insert(field_index, TszrSteelesig)
            self.szrSteelename.insert(field_index, TszrSteelename)
            
            self.szrSteelebox[field_index].Add(self.lblSteelebox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelebox[field_index].Add(self.txtSteelebox[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelexyz[field_index].Add(self.lblSteelexyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelexyz[field_index].Add(self.txtSteelexyz[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelesurface[field_index].Add(self.lblSteelesurface[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelesurface[field_index].Add(self.txtSteelesurface[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeledir[field_index].Add(self.lblSteeledir[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeledir[field_index].Add(self.txtSteeledir[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelecutoff[field_index].Add(self.lblSteelecutoff[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelecutoff[field_index].Add(self.txtSteelecutoff[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeleshift[field_index].Add(self.lblSteeleshift[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeleshift[field_index].Add(self.rbSteeleshift[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeledelta[field_index].Add(self.lblSteeledelta[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeledelta[field_index].Add(self.txtSteeledelta[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelerho_s[field_index].Add(self.lblSteelerho_s[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelerho_s[field_index].Add(self.txtSteelerho_s[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelentype[field_index].Add(self.lblSteelentype[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelentype[field_index].Add(self.txtSteelentype[field_index], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelename[field_index][0].Add(self.lblSteelename[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelename[field_index][0].Add(self.txtSteelename[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelesigma_sf[field_index][0].Add(self.lblSteelesigma_sf[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelesigma_sf[field_index][0].Add(self.txtSteelesigma_sf[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeleepsilon_sf[field_index][0].Add(self.lblSteeleepsilon_sf[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteeleepsilon_sf[field_index][0].Add(self.txtSteeleepsilon_sf[field_index][0], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.szrSteelentypeValues[field_index][0].Add(self.szrSteelename[field_index][0], 0, wx.EXPAND, 0)
            self.szrSteelentypeValues[field_index][0].Add(self.szrSteelesigma_sf[field_index][0], 0, wx.EXPAND, 0)
            self.szrSteelentypeValues[field_index][0].Add(self.szrSteeleepsilon_sf[field_index][0], 0, wx.EXPAND, 0)
            self.szrSteelentypeList[field_index].Add(self.szrSteelentypeValues[field_index][0], 0, wx.LEFT, 50)

            self.szrField[field_type_index].Add(self.szrSteelebox[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteelexyz[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteelesurface[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteeledir[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteelecutoff[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteeleshift[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteeledelta[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteelerho_s[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteelentype[field_index], 0, wx.EXPAND, 0)
            self.szrField[field_type_index].Add(self.szrSteelentypeList[field_index], 0, wx.EXPAND, 0)

        new_ef = self.towhee.create_externalfield(newFieldType)
        self.towhee.set_single_externalfield(field_type_index, new_ef)
        self.szrExternalFieldList.FitInside(self.pnExternalFields)
        self.szrExternalFieldList.Layout()
        self.pnExternalFields.Refresh()
        self.Refresh()
        return

    def HrdEnergyTypeChanged(self, *args):
        index = self.hrdenergytypeID.index(args[0].GetId())
        field_index = self.FindFieldIndex("Hard Wall", index)
        type = self.cboHrdEnergyType[index].GetStringSelection()
        if type == "infinite":
            self.szrField[field_index].Hide(self.szrHrdWallEnergy[index])
        else:
            self.szrField[field_index].Show(self.szrHrdWallEnergy[index])
        self.szrExternalFieldList.FitInside(self.pnExternalFields)
        self.szrExternalFieldList.Layout()
        self.pnExternalFields.Refresh()
        self.Refresh()
        return

    def HafnentriesChanged(self, *args):
        index = self.hafnentriesID.index(args[0].GetId())
        l = self.txtHafnentries[index].GetValue()
        if l.isdigit():
            l = int(l)
            ef = self.towhee.get_single_type_externalfield("Harmonic Attractor", index+1)
            old = ef.get_nentries()
            if l > old:
                for i in range(old, l):
                    hasize = self.lblHafelement[index][0].GetSize()
                    self.lblHafmolec[index].append(wx.StaticText(self.pnExternalFields, -1, "hafmolec",\
                        style=wx.ALIGN_RIGHT, size=hasize))
                    self.txtHafmolec[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblHafelement[index].append(wx.StaticText(self.pnExternalFields, -1, "hafelement",\
                        style=wx.ALIGN_RIGHT, size=hasize))
                    self.txtHafelement[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblHafname[index].append(wx.StaticText(self.pnExternalFields, -1, "hafname",\
                        style=wx.ALIGN_RIGHT, size=hasize))
                    self.txtHafname[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))

                    self.szrHafkeyValues[index].append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                       "Entry " + str(i+1)), wx.VERTICAL))
                    self.szrHafmolec[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHafelement[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrHafname[index].append(wx.BoxSizer(wx.HORIZONTAL))

                    self.szrHafmolec[index][i].Add(self.lblHafmolec[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafmolec[index][i].Add(self.txtHafmolec[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafelement[index][i].Add(self.lblHafelement[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafelement[index][i].Add(self.txtHafelement[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafname[index][i].Add(self.lblHafname[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrHafname[index][i].Add(self.txtHafname[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

                    self.szrHafkeyValues[index][i].Add(self.szrHafmolec[index][i], 1, wx.EXPAND, 0)
                    self.szrHafkeyValues[index][i].Add(self.szrHafelement[index][i], 1, wx.EXPAND, 0)
                    self.szrHafkeyValues[index][i].Add(self.szrHafname[index][i], 1, wx.EXPAND, 0)

                    if self.cboHafkey[index].GetValue() == "Element":
                        self.szrHafkeyValues[index][i].Hide(self.szrHafname[index][i])
                    elif self.cboHafkey[index].GetValue() == "FFtype":
                        self.szrHafkeyValues[index][i].Hide(self.szrHafelement[index][i])

                    self.szrHafkeyList[index].Add(self.szrHafkeyValues[index][i], 0, wx.LEFT, 50)
            elif l < old:
                for i in range(l, old):
                    b = self.szrHafkeyValues[index][-1].GetStaticBox()
                    b.Destroy()
                    self.szrHafkeyList[index].Remove(self.szrHafkeyValues[index][-1])
                    self.lblHafmolec[index][-1].Destroy()
                    self.txtHafmolec[index][-1].Destroy()
                    self.lblHafelement[index][-1].Destroy()
                    self.txtHafelement[index][-1].Destroy()
                    self.lblHafname[index][-1].Destroy()
                    self.txtHafname[index][-1].Destroy()
                    self.szrHafkeyValues[index].pop()
                    self.szrHafmolec[index].pop()
                    self.szrHafelement[index].pop()
                    self.szrHafname[index].pop()
                    self.lblHafmolec[index].pop()
                    self.txtHafmolec[index].pop()
                    self.lblHafelement[index].pop()
                    self.txtHafelement[index].pop()
                    self.lblHafname[index].pop()
                    self.txtHafname[index].pop()
            self.szrExternalFieldList.FitInside(self.pnExternalFields)
            self.szrHafkeyList[index].Layout()
            self.pnExternalFields.Refresh()
            self.Refresh()
            ef.set_nentries(l)
            self.towhee.set_single_type_externalfield("Harmonic Attractor", index+1, ef)
        return

    def HafrefposChanged(self, *args):
        index = self.hafrefposID.index(args[0].GetId())
        field_index = self.FindFieldIndex("Harmonic Attractor", index)
        type = self.cboHafrefpos[index].GetStringSelection()
        if type == "Initial":
            self.szrField[field_index].Hide(self.szrHafglobxyz[index])
        else:
            self.szrField[field_index].Show(self.szrHafglobxyz[index])
        self.szrExternalFieldList.FitInside(self.pnExternalFields)
        self.szrExternalFieldList.Layout()
        self.pnExternalFields.Refresh()
        self.Refresh()
        return

    def HafkeyChanged(self, *args):
        index = self.hafkeyID.index(args[0].GetId())
        type = self.cboHafkey[index].GetStringSelection()
        if type == "Element":
            for i in range(len(self.szrHafkeyValues[index])):
                self.szrHafkeyValues[index][i].Show(self.szrHafelement[index][i])
                self.szrHafkeyValues[index][i].Hide(self.szrHafname[index][i])
        else:
            for i in range(len(self.szrHafkeyValues[index])):
                self.szrHafkeyValues[index][i].Hide(self.szrHafelement[index][i])
                self.szrHafkeyValues[index][i].Show(self.szrHafname[index][i])
        self.szrExternalFieldList.FitInside(self.pnExternalFields)
        self.szrExternalFieldList.Layout()
        self.pnExternalFields.Refresh()
        self.Refresh()
        return

    def LjfntypesChanged(self, *args):
        index = self.ljfntypesID.index(args[0].GetId())
        l = self.txtLjfntypes[index].GetValue()
        if l.isdigit():
            l = int(l)
            ef = self.towhee.get_single_type_externalfield("LJ 9-3 Wall", index+1)
            old = ef.get_ntypes()
            if l > old:
                for i in range(old, l):
                    ljsize = self.lblLjfname[index][0].GetSize()
                    self.lblLjfname[index].append(wx.StaticText(self.pnExternalFields, -1, "ljfname",\
                        style=wx.ALIGN_RIGHT, size=ljsize))
                    self.txtLjfname[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblLjfsig[index].append(wx.StaticText(self.pnExternalFields, -1, "ljfsig",\
                        style=wx.ALIGN_RIGHT, size=ljsize))
                    self.txtLjfsig[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblLjfeps[index].append(wx.StaticText(self.pnExternalFields, -1, "ljfeps",\
                        style=wx.ALIGN_RIGHT, size=ljsize))
                    self.txtLjfeps[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.szrLjfntypesValues[index].append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields, -1,\
                       "ljfntype " + str(i+1)), wx.VERTICAL))
                    self.szrLjfname[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrLjfsig[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrLjfeps[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrLjfname[index][i].Add(self.lblLjfname[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfname[index][i].Add(self.txtLjfname[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfsig[index][i].Add(self.lblLjfsig[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfsig[index][i].Add(self.txtLjfsig[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfeps[index][i].Add(self.lblLjfeps[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfeps[index][i].Add(self.txtLjfeps[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrLjfntypesValues[index][i].Add(self.szrLjfname[index][i], 1, wx.EXPAND, 0)
                    self.szrLjfntypesValues[index][i].Add(self.szrLjfsig[index][i], 1, wx.EXPAND, 0)
                    self.szrLjfntypesValues[index][i].Add(self.szrLjfeps[index][i], 1, wx.EXPAND, 0)
                    self.szrLjfntypesList[index].Add(self.szrLjfntypesValues[index][i], 0, wx.LEFT, 50)
            elif l < old:
                for i in range(l, old):
                    b = self.szrLjfntypesValues[index][-1].GetStaticBox()
                    b.Destroy()
                    self.szrLjfntypesList[index].Remove(self.szrLjfntypesValues[index][-1])
                    self.lblLjfname[index][-1].Destroy()
                    self.txtLjfname[index][-1].Destroy()
                    self.lblLjfsig[index][-1].Destroy()
                    self.txtLjfsig[index][-1].Destroy()
                    self.lblLjfeps[index][-1].Destroy()
                    self.txtLjfeps[index][-1].Destroy()
                    self.szrLjfntypesValues[index].pop()
                    self.szrLjfname[index].pop()
                    self.szrLjfsig[index].pop()
                    self.szrLjfeps[index].pop()
                    self.lblLjfname[index].pop()
                    self.txtLjfname[index].pop()
                    self.lblLjfsig[index].pop()
                    self.txtLjfsig[index].pop()
                    self.lblLjfeps[index].pop()
                    self.txtLjfeps[index].pop()
            self.szrExternalFieldList.FitInside(self.pnExternalFields)
            self.szrLjfntypesList[index].Layout()
            self.pnExternalFields.Refresh()
            self.Refresh()
            ef.set_ntypes(l)
            self.towhee.set_single_type_externalfield("LJ 9-3 Wall", index+1, ef)
        return
        
    def SteelentypeChanged(self, *args):
        index = self.steelentypeID.index(args[0].GetId())
        l = self.txtSteelentype[index].GetValue()
        if l.isdigit():
            l = int(l)
            ef = self.towhee.get_single_type_externalfield("Steele Wall", index+1)
            old = ef.get_ntype()
            if l > old:
                for i in range(old, l):
                    steelesize = self.lblSteeleepsilon_sf[index][0].GetSize()
                    self.lblSteelename[index].append(wx.StaticText(self.pnExternalFields, -1,\
                        "steele name", style=wx.ALIGN_RIGHT, size=steelesize))
                    self.txtSteelename[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblSteelesigma_sf[index].append(wx.StaticText(self.pnExternalFields, -1,\
                        "steele sigma_sf", style=wx.ALIGN_RIGHT, size=steelesize))
                    self.txtSteelesigma_sf[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.lblSteeleepsilon_sf[index].append(wx.StaticText(self.pnExternalFields, -1\
                        , "steele epsilon_sf", style=wx.ALIGN_RIGHT, size=steelesize))
                    self.txtSteeleepsilon_sf[index].append(wx.TextCtrl(self.pnExternalFields, -1, ""))
                    self.szrSteelentypeValues[index].append(wx.StaticBoxSizer(wx.StaticBox(self.pnExternalFields,\
                        -1, "steele ntype " + str(i+1)), wx.VERTICAL))
                    self.szrSteelename[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrSteelesigma_sf[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrSteeleepsilon_sf[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrSteelename[index][i].Add(self.lblSteelename[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelename[index][i].Add(self.txtSteelename[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelesigma_sf[index][i].Add(self.lblSteelesigma_sf[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelesigma_sf[index][i].Add(self.txtSteelesigma_sf[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteeleepsilon_sf[index][i].Add(self.lblSteeleepsilon_sf[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteeleepsilon_sf[index][i].Add(self.txtSteeleepsilon_sf[index][i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                    self.szrSteelentypeValues[index][i].Add(self.szrSteelename[index][i], 1, wx.EXPAND, 0)
                    self.szrSteelentypeValues[index][i].Add(self.szrSteelesigma_sf[index][i], 1, wx.EXPAND, 0)
                    self.szrSteelentypeValues[index][i].Add(self.szrSteeleepsilon_sf[index][i], 1, wx.EXPAND, 0)
                    self.szrSteelentypeList[index].Add(self.szrSteelentypeValues[index][i], 0, wx.EXPAND|wx.LEFT, 50)
            elif l < old:
                for i in range(l, old):
                    b = self.szrSteelentypeValues[index][-1].GetStaticBox()
                    b.Destroy()
                    self.szrSteelentypeList[index].Remove(self.szrSteelentypeValues[index][-1])
                    self.lblSteelename[index][-1].Destroy()
                    self.txtSteelename[index][-1].Destroy()
                    self.lblSteelesigma_sf[index][-1].Destroy()
                    self.txtSteelesigma_sf[index][-1].Destroy()
                    self.lblSteeleepsilon_sf[index][-1].Destroy()
                    self.txtSteeleepsilon_sf[index][-1].Destroy()
                    self.szrSteelentypeValues[index].pop()
                    self.szrSteelename[index].pop()
                    self.szrSteelesigma_sf[index].pop()
                    self.szrSteeleepsilon_sf[index].pop()
                    self.lblSteelename[index].pop()
                    self.txtSteelename[index].pop()
                    self.lblSteelesigma_sf[index].pop()
                    self.txtSteelesigma_sf[index].pop()
                    self.lblSteeleepsilon_sf[index].pop()
                    self.txtSteeleepsilon_sf[index].pop()
            self.szrExternalFieldList.FitInside(self.pnExternalFields)
            self.szrSteelentypeList[index].Layout()
            self.pnExternalFields.Refresh()
            self.Refresh()
            ef.set_ntype(l)
            ef = self.towhee.set_single_type_externalfield("Steele Wall", index+1, ef)
        return
    #    
    # Call these to dynamically update the page based on the current properties
    #
    def DynamicUpdate_RI(self):
        self.StepstyleChanged()

        if self.towhee.get_ensemble() == "uvt":
            self.szrRIc1rows.Show(self.szrChempot)
            self.szrRIc2rows.Show(self.szrLouthist)
            self.LouthistChanged()
            self.pnRunInfo.Refresh()
        else:
            self.szrRIc1rows.Hide(self.szrChempot)
            self.szrRIc2rows.Hide(self.szrLouthist)
            self.szrRIc2rows.Hide(self.szrHistcalcfreq)
            self.szrRIc2rows.Hide(self.szrHistdumpfreq)

        if self.towhee.get_ensemble() == "npt":
            self.szrRIc1rows.Show(self.szrPressure)
        else:
            self.szrRIc1rows.Hide(self.szrPressure)

        self.szrRIc1rows.Layout()
        self.szrRIc2rows.Layout()
        self.szrRIMainColumns.Fit(self.pnRunInfo)
        self.pnRunInfo.Refresh()
        return

    def DynamicUpdate_FF(self):
        check_CmixRescalingStyle = True
        if self.towhee.get_classical_potential() == "Hard Sphere" or\
        self.towhee.get_classical_potential() == "Square Well":
            self.szrFFc1rows.Show(self.szrClassicalMixrule)
            self.szrFFc1rows.Show(self.szrCmixRescalingStyle)
            self.szrFFc1rows.Hide(self.szrLshift)
            self.szrFFc1rows.Hide(self.szrLtailc)
            self.szrFFc1rows.Hide(self.szrRmin)
            self.szrFFc1rows.Hide(self.szrRcut)
            self.szrFFc1rows.Hide(self.szrRcutin)
            self.szrFFc1rows.Hide(self.szrInterpolatestyle)
            self.szrFFc1rows.Show(self.szrRadialPressureDelta)
        elif self.towhee.get_classical_potential() == "Repulsive Sphere" or\
        self.towhee.get_classical_potential() == "Repulsive Well" or\
        self.towhee.get_classical_potential() == "Multiwell" or\
        self.towhee.get_classical_potential() == "Repulsive Multiwell":
            self.szrFFc1rows.Show(self.szrClassicalMixrule) 
            self.szrFFc1rows.Show(self.szrCmixRescalingStyle)
            self.szrFFc1rows.Hide(self.szrLshift)
            self.szrFFc1rows.Hide(self.szrLtailc)
            self.szrFFc1rows.Hide(self.szrRmin)
            self.szrFFc1rows.Hide(self.szrRcut)
            self.szrFFc1rows.Hide(self.szrRcutin)
            self.szrFFc1rows.Hide(self.szrInterpolatestyle)
            self.szrFFc1rows.Hide(self.szrRadialPressureDelta)
        elif self.towhee.get_classical_potential() == "Lennard-Jones" or\
        self.towhee.get_classical_potential() == "9-6" or\
        self.towhee.get_classical_potential() == "12-6 plus solvation" or\
        self.towhee.get_classical_potential() == "12-6 plus 12-10 H-bond" or\
        self.towhee.get_classical_potential() == "12-9-6" or\
        self.towhee.get_classical_potential() == "Exponential-12-6" or\
        self.towhee.get_classical_potential() == "Gordon n-6":
            self.szrFFc1rows.Show(self.szrClassicalMixrule) 
            self.szrFFc1rows.Show(self.szrCmixRescalingStyle)
            self.szrFFc1rows.Show(self.szrLshift)
            self.szrFFc1rows.Show(self.szrLtailc)
            self.szrFFc1rows.Show(self.szrRmin)
            self.szrFFc1rows.Show(self.szrRcut)
            self.szrFFc1rows.Show(self.szrRcutin)
            self.szrFFc1rows.Hide(self.szrInterpolatestyle)
            self.szrFFc1rows.Hide(self.szrRadialPressureDelta)
        elif self.towhee.get_classical_potential() == "Exponential-6":
            self.szrFFc1rows.Show(self.szrClassicalMixrule) 
            self.szrFFc1rows.Show(self.szrCmixRescalingStyle)
            self.szrFFc1rows.Show(self.szrLshift)
            self.szrFFc1rows.Show(self.szrLtailc)
            self.szrFFc1rows.Hide(self.szrRmin)
            self.szrFFc1rows.Show(self.szrRcut)
            self.szrFFc1rows.Show(self.szrRcutin)
            self.szrFFc1rows.Hide(self.szrInterpolatestyle)
            self.szrFFc1rows.Hide(self.szrRadialPressureDelta)
        elif self.towhee.get_classical_potential() == "Stillinger-Weber":
            self.szrFFc1rows.Show(self.szrClassicalMixrule) 
            self.szrFFc1rows.Show(self.szrCmixRescalingStyle)
            self.szrFFc1rows.Hide(self.szrLshift)
            self.szrFFc1rows.Hide(self.szrLtailc)
            self.szrFFc1rows.Hide(self.szrRmin)
            self.szrFFc1rows.Hide(self.szrRcut)
            self.szrFFc1rows.Hide(self.szrRcutin)
            self.szrFFc1rows.Hide(self.szrInterpolatestyle)
            self.szrFFc1rows.Hide(self.szrRadialPressureDelta)
        elif self.towhee.get_classical_potential() == "Embedded Atom Method":
            check_CmixRescalingStyle = False
            self.szrFFc1rows.Hide(self.szrClassicalMixrule) 
            self.szrFFc1rows.Hide(self.szrCmixRescalingStyle)
            self.szrFFc1rows.Hide(self.szrCmixLambda)
            self.szrFFc1rows.Hide(self.szrCmixNpair)
            self.szrFFc1rows.Hide(self.szrCmixPairList)
            self.szrFFc1rows.Hide(self.szrLshift)
            self.szrFFc1rows.Hide(self.szrLtailc)
            self.szrFFc1rows.Hide(self.szrRmin)
            self.szrFFc1rows.Show(self.szrRcut)
            self.szrFFc1rows.Hide(self.szrRcutin)
            self.szrFFc1rows.Show(self.szrInterpolatestyle)
            self.szrFFc1rows.Hide(self.szrRadialPressureDelta)
        elif self.towhee.get_classical_potential() == "Tabulated Pair":
            check_CmixRescalingStyle = False
            self.szrFFc1rows.Hide(self.szrClassicalMixrule) 
            self.szrFFc1rows.Hide(self.szrCmixRescalingStyle)
            self.szrFFc1rows.Hide(self.szrCmixLambda)
            self.szrFFc1rows.Hide(self.szrCmixNpair)
            self.szrFFc1rows.Hide(self.szrCmixPairList)
            self.szrFFc1rows.Hide(self.szrLshift)
            self.szrFFc1rows.Hide(self.szrLtailc)
            self.szrFFc1rows.Hide(self.szrRmin)
            self.szrFFc1rows.Hide(self.szrRcut)
            self.szrFFc1rows.Hide(self.szrRcutin)
            self.szrFFc1rows.Show(self.szrInterpolatestyle)
            self.szrFFc1rows.Hide(self.szrRadialPressureDelta)
        else:
            print "This isn't possible! Why is it " + self.towhee.get_classical_potential() + "???"

        if check_CmixRescalingStyle:
            value = self.cboCmixRescalingStyle.GetValue()
            if value == "grossfield 2003":
                self.szrFFc1rows.Show(self.szrCmixLambda)
                self.szrFFc1rows.Show(self.szrCmixNpair)
                self.szrFFc1rows.Show(self.szrCmixPairList)
            elif value == "none":
                self.szrFFc1rows.Hide(self.szrCmixLambda)
                self.szrFFc1rows.Hide(self.szrCmixNpair)
                self.szrFFc1rows.Hide(self.szrCmixPairList)
            else:
                print "Weirded out!"

        if self.towhee.get_coulombstyle() == "none":
            self.szrFFc2rows.Hide(self.szrKalp)
            self.szrFFc2rows.Hide(self.szrKmax)
            self.szrFFc2rows.Hide(self.szrEwald_prec)
            self.szrFFc2rows.Hide(self.szrRcelect)
            self.szrFFc2rows.Hide(self.szrDielectric)
        elif self.towhee.get_coulombstyle() == "ewald_fixed_kmax":
            self.szrFFc2rows.Show(self.szrKalp)
            self.szrFFc2rows.Show(self.szrKmax)
            self.szrFFc2rows.Hide(self.szrEwald_prec)
            self.szrFFc2rows.Hide(self.szrRcelect)
            self.szrFFc2rows.Show(self.szrDielectric)
        elif self.towhee.get_coulombstyle() == "ewald_fixed_cutoff":
            self.szrFFc2rows.Hide(self.szrKalp)
            self.szrFFc2rows.Hide(self.szrKmax)
            self.szrFFc2rows.Show(self.szrEwald_prec)
            self.szrFFc2rows.Show(self.szrRcelect)
            self.szrFFc2rows.Show(self.szrDielectric)
        elif self.towhee.get_coulombstyle() == "minimum image":
            self.szrFFc2rows.Hide(self.szrKalp)
            self.szrFFc2rows.Hide(self.szrKmax)
            self.szrFFc2rows.Hide(self.szrEwald_prec)
            self.szrFFc2rows.Hide(self.szrRcelect)
            self.szrFFc2rows.Show(self.szrDielectric)
        else:
            print "This isn't possible!  Why is it " + self.towhee.get_coulombstyle() + "?"

        self.szrFFMainColumns.FitInside(self.pnFF)
        self.szrFFc1rows.Layout()
        self.szrFFc2rows.Layout()
        self.pnFF.Refresh()
        return

    def DynamicUpdate_MCM(self):
        if self.towhee.get_ensemble() == "npt" or\
        (self.towhee.get_ensemble() == "nvt" and self.towhee.get_numboxes() > 1):
            b = self.szrIVM.GetStaticBox()
            b.Show()
            self.szrMCM.Show(self.szrIVM)
            self.szrMCM.Show(self.szrAVM)
            b = self.szrAVM.GetStaticBox()
            b.Show()
        else:
            self.szrMCM.Hide(self.szrIVM)
            b = self.szrIVM.GetStaticBox()
            b.Hide()
            self.szrMCM.Hide(self.szrAVM)
            b = self.szrAVM.GetStaticBox()
            b.Hide()

        if self.towhee.get_numboxes() > 1:
            self.szrMCM.Show(self.szrRB2BTM)
            b = self.szrRB2BTM.GetStaticBox()
            b.Show()
            self.szrMCM.Show(self.szrCB2BTM)
            b = self.szrCB2BTM.GetStaticBox()
            b.Show()
        else:
            self.szrMCM.Hide(self.szrRB2BTM)
            b = self.szrRB2BTM.GetStaticBox()
            b.Hide()
            self.szrMCM.Hide(self.szrCB2BTM)
            b = self.szrCB2BTM.GetStaticBox()
            b.Hide()

        if self.towhee.get_ensemble() == "uvt":
            self.szrMCM.Show(self.szrGCID)
            b = self.szrGCID.GetStaticBox()
            b.Show()
        else:
            self.szrMCM.Hide(self.szrGCID)
            b = self.szrGCID.GetStaticBox()
            b.Hide()

        self.szrMCM.Layout()
        self.szrMCM.Fit(self.pnMCM)
        self.pnMCM.Refresh()
        return

    def DynamicUpdate_CBMC(self):
        self.TorcbstyleChanged()
        self.BendcbstyleChanged()
        self.VibcbstyleChanged()
        return

    def CmixRescalingStyleChanged(self, *args):
        cmix = self.cboCmixRescalingStyle.GetStringSelection()
        if cmix == "grossfield 2003":
            self.szrFFc1rows.Show(self.szrCmixLambda)
            self.szrFFc1rows.Show(self.szrCmixNpair)
            self.szrFFc1rows.Show(self.szrCmixPairList)
        elif cmix == "none":
            self.szrFFc1rows.Hide(self.szrCmixLambda)
            self.szrFFc1rows.Hide(self.szrCmixNpair)
            self.szrFFc1rows.Hide(self.szrCmixPairList)
        self.szrFFMainColumns.FitInside(self.pnFF)
        self.szrFFc1rows.Layout()
        self.pnFF.Refresh()
        return

    def CmixNpairChanged(self, *args):
        l = self.txtCmixNpair.GetValue()
        if l.isdigit():
            l = int(l)
            if l == 0:
                return
            npair = self.towhee.get_cmix_npair()
            if l > npair:
                for i in range(npair, l):
                    npsize = self.txtCmixNpair.GetSize()
                    self.txtCmixPairList.append(wx.TextCtrl(self.pnFF, -1, "", size=npsize))
                    self.szrCmixPairListData.Add(self.txtCmixPairList[i], 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2)
            elif l < npair:
                for i in range(l, npair):
                    self.szrCmixPairListData.Remove(self.txtCmixPairList[-1])
                    self.txtCmixPairList[-1].Destroy()
                    self.txtCmixPairList.pop()
            
            self.towhee.set_cmix_npair(l)
            self.szrFFc1rows.Layout()
            self.pnFF.Refresh()
        return

    def TorcbstyleChanged(self, *args):
        l = int(self.cboTor.GetStringSelection())
        if l == 0:
            self.szrCBMCc1rows.Hide(self.szrSdevtor)
        else:
            self.szrCBMCc1rows.Show(self.szrSdevtor)
        self.szrCBMCc1rows.Layout()
        self.towhee.set_tor_cbstyle(l)
        return

    def BendcbstyleChanged(self, *args):
        l = int(self.cboBend.GetStringSelection())
        if l == 0:
            self.szrCBMCc1rows.Hide(self.szrSdevbena)
            self.szrCBMCc1rows.Hide(self.szrSdevbenb)
        else:
            self.szrCBMCc1rows.Show(self.szrSdevbena)
            self.szrCBMCc1rows.Show(self.szrSdevbenb)
        self.szrCBMCc1rows.Layout()
        self.towhee.set_bend_cbstyle(l)
        return

    def VibcbstyleChanged(self, *args):
        l = int(self.cboVib.GetStringSelection())
        if l == 0:
            self.szrCBMCc1rows.Show(self.szrVibrang)
            self.szrCBMCc1rows.Hide(self.szrSdevvib)
        else:
            self.szrCBMCc1rows.Hide(self.szrVibrang)
            self.szrCBMCc1rows.Show(self.szrSdevvib)
        self.szrCBMCc1rows.Layout()
        self.szrCBMC.Layout()
        self.towhee.set_vib_cbstyle(l)
        return

    def InputSetup(self, *args):
        index = self.btnIDs.index(args[0].GetId())
        inpstyle = int(self.cboInpstyle[index].GetSelection())
        if inpstyle == 0:
            if self.CheckNunitNmaxcbmc(index):
                self.HandleInpstyle0(index)
        elif inpstyle == 1:
            if self.CheckNunitNmaxcbmc(index):
                self.HandleInpstyle1(index)
        elif inpstyle == 2:
            if self.CheckNunitNmaxcbmc(index):
                self.HandleInpstyle2(index)
        elif inpstyle == 3:
            if self.CheckNunitNmaxcbmc(index):
                self.HandleInpstyle3(index)
        elif inpstyle == 4:
            self.HandleInpstyle4(index)
        else:
            print "wtf? inpstyle is " + str(inpstyle)
        return

    def CheckNunitNmaxcbmc(self, index):
        nunit = self.txtNunit[index].GetValue()
        if not nunit.isdigit():
            d = wx.MessageDialog(self,
                "Error:  nunit must be a positive integer",
                "Invalid nunit value",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return False
        nunit = int(nunit)
        if nunit < 1:
            d = wx.MessageDialog(self,
                "Error:  nunit must be a positive integer",
                "Invalid nunit value",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return False

        nmaxcbmc = self.txtNmaxcbmc[index].GetValue()
        if not nmaxcbmc.isdigit():
            d = wx.MessageDialog(self,
                "Please set nmaxcbmc",
                "Please set nmaxcbmc",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return False
        else:
            return True
    #
    # Buttons for the Helix
    #
    def InitboxtypeChanged(self, *args):
        l = self.cboInitboxtype.GetStringSelection()
        if l == "dimensions":
            self.szrInitC1.Show(self.szrInitstyle)
            self.szrInitC1.Show(self.szrInitlattice)
            self.szrInitC1.Show(self.szrInitmol)
            self.szrInitC1.Show(self.btnHelix)
            self.szrInitC2.Show(self.szrHmatrix)
            self.szrInitC2.Hide(self.szrBoxNumberDensity)
        elif l == "number density":
            self.szrInitC1.Show(self.szrInitstyle)
            self.szrInitC1.Show(self.szrInitlattice)
            self.szrInitC1.Show(self.szrInitmol)
            self.szrInitC1.Show(self.btnHelix)
            self.szrInitC2.Hide(self.szrHmatrix)
            self.szrInitC2.Show(self.szrBoxNumberDensity)
        elif l == "unit cell":
            self.szrInitC1.Hide(self.szrInitstyle)
            self.szrInitC1.Hide(self.szrInitlattice)
            self.szrInitC1.Hide(self.szrInitmol)
            self.szrInitC1.Hide(self.btnHelix)
            self.szrInitC2.Hide(self.szrHmatrix)
            self.szrInitC2.Hide(self.szrBoxNumberDensity)
        else:
            print "That does not compute", l, "!!"
        self.szrInitC1.Layout()
        self.szrInitC2.Layout()
        self.szrInit.Layout()
        self.szrInit.Fit(self.pnInit)
        self.towhee.set_initboxtype(l)
        return

    def ButtonHelix(self, *args):
        #
        # Save the nmolty value for where helixes should go
        #
        current_helixes = []
        for i in range(self.towhee.get_nmolty()):
            helix = False
            for j in range(self.towhee.get_numboxes()):
                initstyle = self.cboInitstyle[j][i].GetValue()
                if initstyle == "":
                    self.cboInitstyle[j][i].SetValue("full cbmc")
                elif initstyle == "helix":
                    helix = True
            if helix == True:
                current_helixes.append(i)

        if len(current_helixes) == 0:
            d = wx.MessageDialog(self,
                "No initstyles are set to helix",
                "No helix initstyles",
                wx.OK|wx.ICON_INFORMATION)
            d.ShowModal()
            d.Destroy()
            self.towhee.clear_helix()
        else:
            #
            # Find out if I need to add any helixes
            #
            for i in current_helixes:
                not_there = True
                for h in self.towhee.get_helix():
                    if i == h.get_nmolty():
                        not_there = False
                if not_there:
                    new_helix = self.towhee.create_helix()
                    new_helix.set_nmolty(i)
                    self.towhee.append_helix(new_helix)
            #
            # Find out what helixes need to be removed and remove them
            #
            index = []
            all_helixes = self.towhee.get_helix()
            keepGoing = True
            while(keepGoing):
                for i in range(len(all_helixes)):
                    if all_helixes[i].get_nmolty() not in current_helixes:
                        del all_helixes[i]
                        break
                    else:
                        keepGoing = False

            HelixDlg = HelixDlgBox(self, -1, "", all_helixes)
            if HelixDlg.ShowModal() == wx.ID_OK:
                failure = False
                for i in range(len(all_helixes)):
                    value = HelixDlg.txtMoltyp[i].GetValue()
                    if self.CheckValue(value, "helix_moltyp", True):
                        all_helixes[i].set_moltyp(int(value))
                    else:
                        failure = True
                        all_helixes[i].set_moltyp("????")

                    value = HelixDlg.txtRadius[i].GetValue()
                    if self.CheckValue(value, "helix_radius"):
                        all_helixes[i].set_radius(value)
                    else:
                        failure = True
                        all_helixes[i].set_radius("????")

                    value = HelixDlg.txtAngle[i].GetValue()
                    if self.CheckValue(value, "helix_angle"):
                        all_helixes[i].set_angle(value)
                    else:
                        failure = True
                        all_helixes[i].set_angle("????")

                    value = HelixDlg.cboKeytype[i].GetValue()
                    if self.CheckValue(value, "helix_keytype"):
                        all_helixes[i].set_keytype(value)
                    else:
                        failure = True
                        all_helixes[i].set_keytype("????")

                    value = HelixDlg.txtKeyname[i].GetValue()
                    if self.CheckValue(value, "helix_keyname"):
                        all_helixes[i].set_keyname(value)
                    else:
                        failure = True
                        all_helixes[i].set_keyname("????")

                    value = HelixDlg.txtConlen[i].GetValue()
                    if self.CheckValue(value, "helix_conlen"):
                        all_helixes[i].set_conlen(value)
                    else:
                        failure = True
                        all_helixes[i].set_conlen("????")

                    value = HelixDlg.txtPhase[i].GetValue()
                    if self.CheckValue(value, "helix_phase"):
                        all_helixes[i].set_phase(value)
                    else:
                        failure = True
                        all_helixes[i].set_phase("????")
                if failure == True:
                    self.helix_failure = True
                else:
                    self.helix_failure = False
                self.towhee.set_helix(all_helixes)
        return

    def ButtonIVM(self, *args):
        mcm = self.towhee.get_ivm()
        IVMdlg = IVM(self, -1, "", mcm)
        if IVMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmvol.GetValue()
            if self.CheckValue(value, "pmvol"):
                mcm.set_move_probability(value)
            else:
                self.txtPmvol.SetValue("????")
                mcm.set_move_probability("????")
                failure = True

            pmvlpr = []
            for i in IVMdlg.txtPmvlpr:
                value = i.GetValue()
                if self.CheckValue(value, "pmvlpr"):
                    pmvlpr.append(i.GetValue())
                else:
                    pmvlpr.append("????")
                    failure = True
            mcm.set_pmvlpr(pmvlpr)

            value = IVMdlg.txtRmvol.GetValue()
            if self.CheckValue(value, "rmvol"):
                mcm.set_rmvol(value)
            else:
                mcm.set_rmvol("????")
                failure = True

            value = IVMdlg.txtTavol.GetValue()
            if self.CheckValue(value, "tavol"):
                mcm.set_tavol(value)
            else:
                mcm.set_tavol("????")
                failure = True

            if failure:
                self.ivm_failure = True
            else:
                self.ivm_failure = False
            self.towhee.set_ivm(mcm)
        return

    def ButtonAVM(self, *args):
        mcm = self.towhee.get_avm()
        AVMdlg = AVM(self, -1, "", mcm)

        if AVMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmcell.GetValue()
            if self.CheckValue(value, "pmcell"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmcell.SetValue("????")
                failure = True

            pmcellpr = []
            for i in AVMdlg.txtPmcellpr:
                value = i.GetValue()
                if self.CheckValue(value, "pmcellpr"):
                    pmcellpr.append(value)
                else:
                    pmcellpr.append("????")
                    failure = True
            mcm.set_pmcellpr(pmcellpr)

            if self.towhee.get_ensemble() == "nvt":
                pmcellpt = []
                for i in AVMdlg.txtPmcellpt:
                    value = i.GetValue()
                    if self.CheckValue(value, "pmcellpt"):
                        pmcellpt.append(value)
                    else:
                        pmcellpt.append("????")
                        failure = True
                mcm.set_pmcellpt(pmcellpt)

            value = AVMdlg.txtRmcell.GetValue()
            if self.CheckValue(value, "rmcell"):
                mcm.set_rmcell(value)
            else:
                mcm.set_rmcell("????")
                failure = True

            value = AVMdlg.txtTacell.GetValue()
            if self.CheckValue(value, "tacell"):
                mcm.set_tacell(value)
            else:
                mcm.set_tacell("????")
                failure = True

            if failure:
                self.avm_failure = True
            else:
                self.avm_failure = False
            self.towhee.set_avm(mcm)
        return

    def ButtonCBSBMRM(self, *args):
        mcm = self.towhee.get_cbsbmrm()
        CBSBMRMdlg = CBSBMRM(self, -1, mcm)
        if CBSBMRMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPm1boxcbswap.GetValue()
            if self.CheckValue(value, "pm1boxcbswap"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPm1boxcbswap.SetValue("????")
                failure = True

            pm1cbswmt = []
            for i in CBSBMRMdlg.txtPm1cbswmt:
                value = i.GetValue()
                if self.CheckValue(value, "pm1cbswmt"):
                    pm1cbswmt.append(value)
                else:
                    pm1cbswmt.append("????")
                    failure = True
            mcm.set_pm1cbswmt(pm1cbswmt)

            if failure:
                self.cbsbmrm_failure = True
            else:
                self.cbsbmrm_failure = False
            self.towhee.set_cbsbmrm(mcm)
        return

    def ButtonRB2BMTM(self, *args):
        mcm = self.towhee.get_rb2bmtm()
        RB2BMTMdlg = RB2BMTM(self, -1, "", mcm)
        if RB2BMTMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPm2boxrbswap.GetValue()
            if self.CheckValue(value, "pm2boxrbswap"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPm2boxrbswap.SetValue("????")
                failure = True

            pm2rbswmt = []
            for i in RB2BMTMdlg.txtPm2rbswmt:
                value = i.GetValue()
                if self.CheckValue(value, "pm2rbswmt"):
                    pm2rbswmt.append(value)
                else:
                    pm2rbswmt.append("????")
                    failure = True
            mcm.set_pm2rbswmt(pm2rbswmt)

            pm2rbswpr = []
            for i in RB2BMTMdlg.txtPm2rbswpr:
                value = i.GetValue()
                if self.CheckValue(value, "pm2rbswpr"):
                    pm2rbswpr.append(value)
                else:
                    pm2rbswpr.append("????")
                    failure = True
            mcm.set_pm2rbswpr(pm2rbswpr)

            if failure:
                self.rb2bmtm_failure = True
            else:
                self.rb2bmtm_failure = False
            self.towhee.set_rb2bmtm(mcm)
        return

    def ButtonCB2BMTM(self, *args):
        mcm = self.towhee.get_cb2bmtm()
        CB2BMTMdlg = CB2BMTM(self, -1, "", mcm)
        if CB2BMTMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPm2boxcbswap.GetValue()
            if self.CheckValue(value, "pm2boxcbswap"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPm2boxcbswap.SetValue("????")
                failure = True

            pm2cbswmt = []
            for i in CB2BMTMdlg.txtPm2cbswmt:
                value = i.GetValue()
                if self.CheckValue(value, "pm2cbswmt"):
                    pm2cbswmt.append(value)
                else:
                    pm2cbswmt.append("????")
                    failure = True
            mcm.set_pm2cbswmt(pm2cbswmt)

            pm2cbswpr = []
            for i in CB2BMTMdlg.txtPm2cbswpr:
                value = i.GetValue()
                if self.CheckValue(value, "pm2cbswpr"):
                    pm2cbswpr.append(value)
                else:
                    pm2cbswpr.append("????")
                    failure = True
            mcm.set_pm2cbswpr(pm2cbswpr)

            if failure:
                self.cb2bmtm_failure = True
            else:
                self.cb2bmtm_failure = False
            self.towhee.set_cb2bmtm(mcm)
        return

    def ButtonGCID(self, *args):
        mcm = self.towhee.get_cbgcidm()
        GCIDdlg = GCID(self, -1, "", mcm)
        if GCIDdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmuvtcbswap.GetValue()
            if self.CheckValue(value, "pmuvtcbswap"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmuvtcbswap.SetValue("????")
                failure = True

            pmuvtcbmt = []
            for i in GCIDdlg.txtPmuvtcbmt:
                value = i.GetValue()
                if self.CheckValue(value, "pmuvtcbmt"):
                    pmuvtcbmt.append(value)
                else:
                    pmuvtcbmt.append("????")
                    failure = True
            mcm.set_pmuvtcbmt(pmuvtcbmt)

            if failure:
                self.gcid_failure = True
            else:
                self.gcid_failure = False
            self.towhee.set_cbgcidm(mcm)
        return

    def ButtonAVBMT1(self, *args):
        mcm = self.towhee.get_avbmt1()
        AVBMT1dlg = AVBMT1(self, -1, "", mcm)
        if AVBMT1dlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmavb1.GetValue()
            if self.CheckValue(value, "pmavb1"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmavb1.SetValue("????")
                failure = True

            value = AVBMT1dlg.txtPmavb1in.GetValue()
            if self.CheckValue(value, "pmavb1in"):
                mcm.set_pmavb1in(value)
            else:
                mcm.set_pmavb1in("????")
                failure = True

            pmavb1mt = []
            for i in AVBMT1dlg.txtPmavb1mt:
                value = i.GetValue()
                if self.CheckValue(value, "pmavb1mt"):
                    pmavb1mt.append(value)
                else:
                    pmavb1mt.append("????")
                    failure = True
            mcm.set_pmavb1mt(pmavb1mt)

            pmavb1ct = []
            for i in range(self.towhee.get_nmolty()):
                t = []
                for j in range(self.towhee.get_nmolty()):
                    index = i*self.towhee.get_nmolty()+j
                    value = AVBMT1dlg.txtPmavb1ct[index].GetValue()
                    if self.CheckValue(value, "pmavb1ct"):
                        t.append(value)
                    else:
                        t.append("????")
                        failure = True
                pmavb1ct.append(t)
            mcm.set_pmavb1ct(pmavb1ct)

            value = AVBMT1dlg.txtAvb1rad.GetValue()
            if self.CheckValue(value, "avb1rad"):
                mcm.set_avb1rad(value)
            else:
                mcm.set_avb1rad("????")
                failure = True

            if failure:
                self.avbmt1_failure = True
            else:
                self.avbmt1_failure = False
            self.towhee.set_avbmt1(mcm)
        return

    def ButtonAVBMT2(self, *args):
        mcm = self.towhee.get_avbmt2()
        AVBMT2dlg = AVBMT2(self, -1, "", mcm)
        if AVBMT2dlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmavb2.GetValue()
            if self.CheckValue(value, "pmavb2"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmavb2.SetValue("????")
                failure = True

            value = AVBMT2dlg.txtPmavb2in.GetValue()
            if self.CheckValue(value, "pmavb2in"):
                mcm.set_pmavb2in(value)
            else:
                mcm.set_pmavb2in("????")
                failure = True

            pmavb2mt = []
            for i in AVBMT2dlg.txtPmavb2mt:
                value = i.GetValue()
                if self.CheckValue(value, "pmavb2mt"):
                    pmavb2mt.append(value)
                else:
                    pmavb2mt.append("????")
                    failure = True
            mcm.set_pmavb2mt(pmavb2mt)

            pmavb2ct = []
            for i in range(self.towhee.get_nmolty()):
                t = []
                for j in range(self.towhee.get_nmolty()):
                    index = i*self.towhee.get_nmolty()+j
                    value = AVBMT2dlg.txtPmavb2ct[index].GetValue()
                    if self.CheckValue(value, "pmavb2ct"):
                        t.append(value)
                    else:
                        t.append("????")
                        failure = True
                pmavb2ct.append(t)
            mcm.set_pmavb2ct(pmavb2ct)

            value = AVBMT2dlg.txtAvb2rad.GetValue()
            if self.CheckValue(value, "avb2rad"):
                mcm.set_avb2rad(value)
            else:
                mcm.set_avb2rad("????")
                failure = True

            if failure:
                self.avbmt2_failure = True
            else:
                self.avbmt2_failure = False
            self.towhee.set_avbmt2(mcm)
        return

    def ButtonAVBMT3(self, *args):
        mcm = self.towhee.get_avbmt3()
        AVBMT3dlg = AVBMT3(self, -1, "", mcm)
        if AVBMT3dlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmavb3.GetValue()
            if self.CheckValue(value, "pmavb3"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmavb3.SetValue("????")
                failure = True

            pmavb3mt = []
            for i in AVBMT3dlg.txtPmavb3mt:
                value = i.GetValue()
                if self.CheckValue(value, "pmavb3mt"):
                    pmavb3mt.append(value)
                else:
                    pmavb3mt.append("????")
                    failure = True
            mcm.set_pmavb3mt(pmavb3mt)

            pmavb3ct = []
            for i in range(self.towhee.get_nmolty()):
                t = []
                for j in range(self.towhee.get_nmolty()):
                    index = i*self.towhee.get_nmolty()+j
                    value = AVBMT3dlg.txtPmavb3ct[index].GetValue()
                    if self.CheckValue(value, "pmavb3ct"):
                        t.append(value)
                    else:
                        t.append("????")
                        failure = True
                pmavb3ct.append(t)
            mcm.set_pmavb3ct(pmavb3ct)

            value = AVBMT3dlg.txtAvb3rad.GetValue()
            if self.CheckValue(value, "avb3rad"):
                mcm.set_avb3rad(value)
            else:
                mcm.set_avb3rad("????")
                failure = True

            if failure:
                self.avbmt3_failure = True
            else:
                self.avbmt3_failure = False
            self.towhee.set_avbmt3(mcm)
        return

    def ButtonCBPMR(self, *args):
        mcm = self.towhee.get_cbpmr()
        CBPMRdlg = CBPMR(self, -1, "", mcm)
        if CBPMRdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmcb.GetValue()
            if self.CheckValue(value, "pmcb"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmcb.SetValue("????")
                failure = True

            pmcbmt = []
            for i in CBPMRdlg.txtPmcbmt:
                value = i.GetValue()
                if self.CheckValue(value, "pmcbmt"):
                    pmcbmt.append(value)
                else:
                    pmcbmt.append("????")
                    failure = True
            mcm.set_pmcbmt(pmcbmt)

            pmall = []
            for i in CBPMRdlg.txtPmall:
                value = i.GetValue()
                if self.CheckValue(value, "pmall"):
                    pmall.append(value)
                else:
                    pmall.append("????")
                    failure = True
            mcm.set_pmall(pmall)

            if failure:
                self.cbpmr_failure = True
            else:
                self.cbpmr_failure = False
            self.towhee.set_cbpmr(mcm)
        return

    def ButtonCBPBR(self, *args):
        mcm = self.towhee.get_cbpbr()
        CBPBRdlg = CBPBR(self, -1, "", mcm)
        if CBPBRdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmback.GetValue()
            if self.CheckValue(value, "pmback"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmback.SetValue("????")
                failure = True

            pmbkmt = []
            for i in CBPBRdlg.txtPmbkmt:
                value = i.GetValue()
                if self.CheckValue(value, "pmbkmt"):
                    pmbkmt.append(value)
                else:
                    pmbkmt.append("????")
                    failure = True
            mcm.set_pmbkmt(pmbkmt)

            if failure:
                self.cbpbr_failure = True
            else:
                self.cbpbr_failure = False
            self.towhee.set_cbpbr(mcm)
        return
        
    def ButtonTPM(self, *args):
        mcm = self.towhee.get_tpm()
        TPMdlg = TPM(self, -1, "", mcm)
        if TPMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmpivot.GetValue()
            if self.CheckValue(value, "pmpivot"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmpivot.SetValue("????")
                failure = True

            pmpivmt = []
            for i in TPMdlg.txtPmpivmt:
                value = i.GetValue()
                if self.CheckValue(value, "pmpivmt"):
                    pmpivmt.append(value)
                else:
                    pmpivmt.append("????")
                    failure = True
            mcm.set_pmpivmt(pmpivmt)

            if failure:
                self.tpm_failure = True
            else:
                self.tpm_failure = False
            self.towhee.set_tpm(mcm)
        return

    def ButtonCRMNPB(self, *args):
        mcm = self.towhee.get_crnmoanpb()
        CRMNPBdlg = CRMNPB(self, -1, "", mcm)
        if CRMNPBdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmconrot.GetValue()
            if self.CheckValue(value, "pmconrot"):
                mcm.set_move_probability(value)
            else:
                mcm.set_move_probability("????")
                self.txtPmconrot.SetValue("????")
                failure = True
            
            pmcrmt = []
            for i in CRMNPBdlg.txtPmcrmt:
                value = i.GetValue()
                if self.CheckValue(value, "pmcrmt"):
                    pmcrmt.append(value)
                else:
                    pmcrmt.append("????")
                    failure = True
            mcm.set_pmcrmt(pmcrmt)

            if failure:
                self.crmnpb_failure = True
            else:
                self.crmnpb_failure = False
            self.towhee.set_crnmoanpb(mcm)
        return

    def ButtonCRM3PBS(self, *args):
        mcm = self.towhee.get_crnmoa3pbs()
        CRM3PBSdlg = CRM3PBS(self, -1, "", mcm)
        if CRM3PBSdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmcrback.GetValue()
            if self.CheckValue(value, "pmcrback"):
                mcm.set_move_probability(value)
            else:
                failure = True
                mcm.set_move_probability("????")
                self.txtPmcrback.SetValue("????")
            
            pmcrbmt = []
            for i in CRM3PBSdlg.txtPmcrbmt:
                value = i.GetValue()
                if self.CheckValue(value, "pmcrbmt"):
                    pmcrbmt.append(value)
                else:
                    failure = True
                    pmcrbmt.append("????")
            mcm.set_pmcrbmt(pmcrbmt)

            if failure:
                self.crm3pbs_failure = True
            else:
                self.crm3pbs_failure = False

            self.towhee.set_crnmoa3pbs(mcm)
        return

    def ButtonPSM(self, *args):
        mcm = self.towhee.get_psm()
        PSMdlg = PSM(self, -1, mcm)
        if PSMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmplane.GetValue()
            if self.CheckValue(value, "pmplane"):
                mcm.set_move_probability(value)
            else:
                failure = True
                mcm.set_probabilty("????")
                self.txtPmplane.SetValue("????")

            pmplanebox = []
            for i in PSMdlg.txtPmplanebox:
                value = i.GetValue()
                if self.CheckValue(value, "pmplanebox"):
                    pmplanebox.append(value)
                else:
                    failure = True
                    pmplanebox.append("????")
            mcm.set_pmplanebox(pmplanebox)

            value = PSMdlg.txtPlanewidth.GetValue()
            if self.CheckValue(value, "planewidth"):
                mcm.set_planewidth(value)
            else:
                failure = True
                mcm.set_planewidth("????")

            if failure:
                self.psm_failure = True
            else:
                self.psm_failure = False

            self.towhee.set_psm(mcm)
        return

    def ButtonRSM(self, *args):
        mcm = self.towhee.get_rsm()
        RSMdlg = RSM(self, -1, mcm)
        if RSMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmrow.GetValue()
            if self.CheckValue(value, "pmrow"):
                mcm.set_move_probability(value)
            else:
                failure = True
                mcm.set_move_probability("????")
                self.txtPmrow.SetValue("????")

            pmrowbox = []
            for i in RSMdlg.txtPmrowbox:
                value = i.GetValue()
                if self.CheckValue(value, "pmrowbox"):
                    pmrowbox.append(value)
                else:
                    failure = True
                    pmrowbox.append("????")
            mcm.set_pmrowbox(pmrowbox)

            value = RSMdlg.txtRowwidth.GetValue()
            if self.CheckValue(value, "rowwidth"):
                mcm.set_rowwidth(value)
            else:
                failure = True
                mcm.set_rowwidth("????")

            if failure:
                self.rsm_failure = True
            else:
                self.rsm_failure = False

            self.towhee.set_rsm(mcm)
        return

    def ButtonISATM(self, *args):
        mcm = self.towhee.get_isatm()
        ISATMdlg = ISATM(self, -1, "", mcm)
        if ISATMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmtraat.GetValue()
            if self.CheckValue(value, "pmtraat"):
                mcm.set_move_probability(value)
            else:
                failure = True
                mcm.set_move_probability("????")
                self.txtPmtraat.SetValue("????")

            pmtamt = []
            for i in ISATMdlg.txtPmtamt:
                value = i.GetValue()
                if self.CheckValue(value, "pmtamt"):
                    pmtamt.append(value)
                else:
                    failure = True
                    pmtamt.append("????")
            mcm.set_pmtamt(pmtamt)

            value = ISATMdlg.txtRmtraa.GetValue()
            if self.CheckValue(value, "rmtraa"):
                mcm.set_rmtraa(value)
            else:
                failure = True
                mcm.set_rmtraa("????")

            value = ISATMdlg.txtTatraa.GetValue()
            if self.CheckValue(value, "tatraa"):
                mcm.set_tatraa(value)
            else:
                failure = True
                mcm.set_tatraa("????")

            if failure:
                self.isatm_failure = True
            else:
                self.isatm_failure = False

            self.towhee.set_isatm(mcm)
        return

    def ButtonCMMTM(self, *args):
        mcm = self.towhee.get_cofmmtm()
        CMMTMdlg = CMMTM(self, -1, "", mcm)
        if CMMTMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmtracm.GetValue()
            if self.CheckValue(value, "pmtracm"):
                mcm.set_move_probability(value)
            else:
                failure = True
                mcm.set_move_probability("????")
                self.txtPmtracm.SetValue("????")

            pmtcmt = []
            for i in CMMTMdlg.txtPmtcmt:
                value = i.GetValue()
                if self.CheckValue(value, "pmtcmt"):
                    pmtcmt.append(value)
                else:
                    failure = True
                    pmtcmt.append("????")
            mcm.set_pmtcmt(pmtcmt)

            value = CMMTMdlg.txtRmtrac.GetValue()
            if self.CheckValue(value, "rmtrac"):
                mcm.set_rmtrac(value)
            else:
                failure = True
                mcm.set_rmtrac("????")

            value = CMMTMdlg.txtTatrac.GetValue()
            if self.CheckValue(value, "tatrac"):
                mcm.set_tatrac(value)
            else:
                failure = True
                mcm.set_tatrac("????")

            if failure:
                self.cmmtm_failure = True
            else:
                self.cmmtm_failure = False

            self.towhee.set_cofmmtm(mcm)
        return

    def ButtonRCMM(self, *args):
        mcm = self.towhee.get_ratcomm()
        RCMMdlg = RCMM(self, -1, "", mcm)
        if RCMMdlg.ShowModal() == wx.ID_OK:
            failure = False
            value = self.txtPmrotate.GetValue()
            if self.CheckValue(value, "pmrotate"):
                mcm.set_move_probability(value)
            else:
                failure = True
                mcm.set_move_probability("????")
                self.txtPmrotate.SetValue("????")

            pmromt = []
            for i in RCMMdlg.txtPmromt:
                value = i.GetValue()
                if self.CheckValue(value, "pmromt"):
                    pmromt.append(value)
                else:
                    failure = True
                    pmromt.append("????")
            mcm.set_pmromt(pmromt)

            value = RCMMdlg.txtRmrot.GetValue()
            if self.CheckValue(value, "rmrot"):
                mcm.set_rmrot(value)
            else:
                failure = True
                mcm.set_rmrot("????")

            value = RCMMdlg.txtTarot.GetValue()
            if self.CheckValue(value, "tarot"):
                mcm.set_tarot(value)
            else:
                failure = True
                mcm.set_tarot("????")

            if failure:
                self.rcmm_failure = True
            else:
                self.rcmm_failure = False

            self.towhee.set_ratcomm(mcm)
        return
    #
    # These functions will take care of each input style and saving them.
    #
    def HandleInpstyle0(self, index):
        nunit = int(self.txtNunit[index].GetValue())
        nmaxcbmc = int(self.txtNmaxcbmc[index].GetValue())
        input = self.towhee.get_single_input(index)

        if input.get_inpstyle() != 0:
            input = self.towhee.create_input(0)

        input.set_nunit(nunit)
        input.set_nmaxcbmc(nmaxcbmc)

        EDDlg = ExplicitDeclaration(self, -1, "", input)
        if EDDlg.ShowModal() == wx.ID_OK:
            self.input_error[index] = False
            if EDDlg.rbLPDB.GetSelection():
                input.set_lpdb_false()
            else:
                input.set_lpdb_true()

            unit = []
            for i in EDDlg.txtUnit:
                value = i.GetValue()
                if self.CheckValue(value, "unit ", True):
                    unit.append(int(value))
                else:
                    unit.append(EDDlg.txtUnit.index(i)+1)
                    d = wx.MessageDialog(self,
                        "Setting Unit to " + str(EDDlg.txtUnit.index(i)+1), 
                        "Changing Unit Automatically",
                        wx.ICON_INFORMATION)
                    d.ShowModal()
                    d.Destroy()
            input.set_unit(unit)

            type = []
            for i in EDDlg.txtType:
                value = i.GetValue()
                if self.CheckValue(value, "ntype", True):
                    type.append(int(value))
                else:
                    type.append("????")
                    self.input_error[index] = True
            input.set_type(type)

            qqatom = []
            for i in EDDlg.txtQqatom:
                value = i.GetValue()
                if self.CheckValue(value, "qqatom"):
                    qqatom.append(value)
                else:
                    qqatom.append("????")
                    self.input_error[index] = True
            input.set_qqatom(qqatom)

            if input.get_lpdb():
                pdbname = []
                for i in EDDlg.txtPdbname:
                    value = i.GetValue()
                    if self.CheckValue(value, "pdbname"):
                        pdbname.append(value)
                    else:
                        pdbname.append("????")
                        self.input_error[index] = True
                input.set_pdbname(pdbname)

                aminonum = []
                for i in EDDlg.txtAminonum:
                    value = i.GetValue()
                    if self.CheckValue(value, "aminonum", True):
                        aminonum.append(int(value))
                    else:
                        aminonum.append("????")
                        self.input_error[index] = True
                input.set_aminonum(aminonum)

                aminoshort = []
                for i in EDDlg.txtAminoshort:
                    value = i.GetValue()
                    if self.CheckValue(value, "aminoshort"):
                        aminoshort.append(value)
                    else:
                        aminoshort.append("????")
                        self.input_error[index] = True
                input.set_aminoshort(aminoshort)

            input.clear_vibrations()
            for i in range(nunit):
                vib = input.create_vibrations()
                value = EDDlg.txtInvib[i].GetValue()
                if self.CheckValue(value, "invib", True):
                    vib.set_number_vibrations(int(value))
                else:
                    vib.set_number_vibrations(0)
                    self.input_error[index] = True

                for j in range(vib.get_number_vibrations()):
                    vibtemp = []
                    value = EDDlg.txtIjvib[i][j].GetValue()
                    if self.CheckValue(value, "ijvib", True):
                        vibtemp.append(int(value))
                    else:
                        vibtemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtItvib[i][j].GetValue()
                    if self.CheckValue(value, "itvib", True):
                        vibtemp.append(int(value))
                    else:
                        vibtemp.append("????")
                        self.input_error[index] = True
                    vib.append_vibrations(vibtemp)
                input.append_vibrations(vib)

            input.clear_bendings()
            for i in range(nunit):
                bend = input.create_bendings()
                value = EDDlg.txtInben[i].GetValue()
                if self.CheckValue(value, "inben", True):
                    bend.set_number_bendings(int(value))
                else:
                    bend.set_number_bendings(0)
                    self.input_error[index] = True

                for j in range(bend.get_number_bendings()):
                    bendtemp = []
                    value = EDDlg.txtIjben2[i][j].GetValue()
                    if self.CheckValue(value, "inben2", True):
                        bendtemp.append(int(value))
                    else:
                        bendtemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIjben3[i][j].GetValue()
                    if self.CheckValue(value, "inben3", True):
                        bendtemp.append(int(value))
                    else:
                        bendtemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtItben[i][j].GetValue()
                    if self.CheckValue(value, "itben", True):
                        bendtemp.append(int(value))
                    else:
                        bendtemp.append("????")
                        self.input_error[index] = True
                    bend.append_bendings(bendtemp)
                input.append_bendings(bend)

            input.clear_torsions()
            for i in range(nunit):
                tor = input.create_torsions()
                value = EDDlg.txtIntor[i].GetValue()
                if self.CheckValue(value, "intor", True):
                    tor.set_number_torsions(int(value))
                else:
                    tor.set_number_torisions(0)
                    self.input_error[index] = True

                for j in range(tor.get_number_torsions()):
                    tortemp = []
                    value = EDDlg.txtIjtor2[i][j].GetValue()
                    if self.CheckValue(value, "ijtor2", True):
                        tortemp.append(int(value))
                    else:
                        tortemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIjtor3[i][j].GetValue()
                    if self.CheckValue(value, "ijtor3", True):
                        tortemp.append(int(value))
                    else:
                        tortemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIjtor4[i][j].GetValue()
                    if self.CheckValue(value, "ijtor4", True):
                        tortemp.append(int(value))
                    else:
                        tortemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIttor[i][j].GetValue()
                    if self.CheckValue(value, "ittor", True):
                        tortemp.append(int(value))
                    else:
                        tortemp.append("????")
                        self.input_error[index] = True
                    tor.append_torsions(tortemp)
                input.append_torsions(tor)

            input.clear_angles()
            for i in range(nunit):
                ang = input.create_angles()
                value = EDDlg.txtInaa[i].GetValue()
                if self.CheckValue(value, "inaa", True):
                    ang.set_number_angles(int(value))
                else:
                    ang.set_number_angles(0)
                    self.input_error[index] = True

                for j in range(ang.get_number_angles()):
                    angtemp = []
                    value = EDDlg.txtIjaa0[i][j].GetValue()
                    if self.CheckValue(value, "ijaa0", True):
                        angtemp.append(int(value))
                    else:
                        angtemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIjaa1[i][j].GetValue()
                    if self.CheckValue(value, "ijaa1", True):
                        angtemp.append(int(value))
                    else:
                        antemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIjaa2[i][j].GetValue()
                    if self.CheckValue(value, "ijaa2", True):
                        angtemp.append(int(value))
                    else:
                        angtemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtItaa[i][j].GetValue()
                    if self.CheckValue(value, "itaa", True):
                        angtemp.append(int(value))
                    else:
                        angtemp.append("????")
                        self.input_error[index] = True
                    ang.append_angles(angtemp)
                input.append_angles(ang)

            input.clear_improper_torsions()
            for i in range(nunit):
                imptor = input.create_improper_torsions()
                value = EDDlg.txtInimprop[i].GetValue()
                if self.CheckValue(value, "inimprop", True):
                    imptor.set_number_improper_torsions(int(value))
                else:
                    imptor.set_number_improper_torsions(0)
                    self.input_error[index] = True

                for j in range(imptor.get_number_improper_torsions()):
                    ittemp = []
                    value = EDDlg.txtIjimprop2[i][j].GetValue()
                    if self.CheckValue(value, "ijimprop2", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIjimprop3[i][j].GetValue()
                    if self.CheckValue(value, "ijimprop3", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtIjimprop4[i][j].GetValue()
                    if self.CheckValue(value, "ijimprop4", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True

                    value = EDDlg.txtItimprop[i][j].GetValue()
                    if self.CheckValue(value, "itimprop", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True
                    imptor.append_improper_torsions(ittemp)
                input.append_improper_torsions(imptor)

            self.towhee.set_single_input(index, input)
        return

    def HandleInpstyle1(self, index):
        nmaxcbmc = int(self.txtNmaxcbmc[index].GetValue())
        nunit = int(self.txtNunit[index].GetValue())
        input = self.towhee.get_single_input(index)

        if input.get_inpstyle() != 1:
            input = self.towhee.create_input(1)

        input.set_nunit(nunit)
        input.set_nmaxcbmc(nmaxcbmc)

        PBDlg = PolypeptideBuilder(self, -1, "", input)
        if PBDlg.ShowModal() == wx.ID_OK:
            self.input_error[index] = False
            value = PBDlg.txtForcefield.GetValue()
            if self.CheckValue(value, "forcefield"):
                input.set_forcefield(value)
            else:
                input.set_forcefield("????")
                self.input_error[index] = True

            input.set_protgeom(PBDlg.cboProtgeom.GetValue())
            input.clear_pepname()
            input.clear_stereochem()
            input.clear_bondpartner()
            input.clear_terminus()
            for i in range(nunit):
                value = PBDlg.txtPepname[i].GetValue()
                if self.CheckValue(value, "pepname"):
                    input.append_pepname(value)
                else:
                    input.append_pepname("????")
                    self.input_error[index] = True

                value = PBDlg.txtStereochem[i].GetValue()
                if self.CheckValue(value, "stereochem"):
                    input.append_stereochem(value)
                else:
                    input.append_stereochem("????")
                    self.input_error[index] = True

                value = PBDlg.txtBondpartner[i].GetValue()
                if self.CheckValue(value, "bondpartner", True):
                    input.append_bondpartner(int(value))
                else:
                    input.append_bondpartner("????")
                    self.input_error[index] = True

                if input.get_protgeom() == "linear":
                    value = PBDlg.txtTerminus[i].GetValue()
                    if self.CheckValue(value, "terminus"):
                        input.append_terminus(value)
                    else:
                        input.append_terminus("????")
                        self.input_error[index] = True
                else:
                    input.append_terminus("")

            self.towhee.set_single_input(index, input)
        return

    def HandleInpstyle2(self, index):
        nmaxcbmc = int(self.txtNmaxcbmc[index].GetValue())
        nunit = int(self.txtNunit[index].GetValue())
        input = self.towhee.get_single_input(index)

        if input.get_inpstyle() != 2:
            input = self.towhee.create_input(2)

        input.set_nunit(nunit)
        input.set_nmaxcbmc(nmaxcbmc)

        CMDlg = ConnectivityMap(self, -1, "", input)
        if CMDlg.ShowModal() == wx.ID_OK:
            self.input_error[index] = False
            value = CMDlg.txtForcefield.GetValue()
            if self.CheckValue(value, "forcefield"):
                input.set_forcefield(value)
            else:
                input.set_forcefield("????")
                self.input_error[index] = True

            input.set_charge_assignment(CMDlg.cboCharge_assignment.GetValue())

            unit =  []
            for i in CMDlg.txtUnit:
                value = i.GetValue()
                if self.CheckValue(value, "unit", True):
                    unit.append(int(value))
                else:
                    unit.append("????")
                    self.input_error[index] = True
            input.set_unit(unit)

            type = []
            for i in CMDlg.txtType:
                value = i.GetValue()
                if self.CheckValue(value, "type"):
                    type.append(value)
                else:
                    type.append("????")
                    self.input_error[index] = True
            input.set_type(type)

            if input.get_charge_assignment() == "manual":
                qqatom = []
                for i in CMDlg.txtQqatom:
                    value = i.GetValue()
                    if self.CheckValue(value, "qqatom"):
                        qqatom.append(value)
                    else:
                        qqatom.append("????")
                        self.input_error[index] = True
                input.set_qqatom(qqatom)

            input.clear_vibrations()
            for i in range(nunit):
                vib = input.create_vibrations()
                value = CMDlg.txtInvib[i].GetValue()
                if self.CheckValue(value, "invib", True):
                    vib.set_number_vibrations(int(value))
                else:
                    vib.set_number_vibrations(0)
                    self.input_error[index] = True

                for j in range(vib.get_number_vibrations()):
                    value = CMDlg.txtIjvib[i][j].GetValue()
                    if self.CheckValue(value, "ijvib", True):
                        vib.append_vibrations(int(value))
                    else:
                        vib.append_vibrations("????")
                        self.input_error[index] = True
                input.append_vibrations(vib)

            input.clear_improper_torsions()
            for i in range(nunit):
                imptor = input.create_improper_torsions()
                value = CMDlg.txtInimprop[i].GetValue()
                if self.CheckValue(value, "inimprop", True):
                    imptor.set_number_improper_torsions(int(value))
                else:
                    imptor.set_number_improper_torsions(0)
                    self.input_error[index] = True

                for j in range(imptor.get_number_improper_torsions()):
                    ittemp = []
                    value = CMDlg.txtIjimprop2[i][j].GetValue()
                    if self.CheckValue(value, "ijimprop2", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True

                    value = CMDlg.txtIjimprop3[i][j].GetValue()
                    if self.CheckValue(value, "ijimprop3", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True

                    value = CMDlg.txtIjimprop4[i][j].GetValue()
                    if self.CheckValue(value, "ijimprop4", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True

                    value = CMDlg.txtItimprop[i][j].GetValue()
                    if self.CheckValue(value, "itimprop", True):
                        ittemp.append(int(value))
                    else:
                        ittemp.append("????")
                        self.input_error[index] = True
                    imptor.append_improper_torsions(ittemp)
                input.append_improper_torsions(imptor)

            self.towhee.set_single_input(index, input)
        return

    def HandleInpstyle3(self, index):
        nmaxcbmc = int(self.txtNmaxcbmc[index].GetValue())
        nunit = int(self.txtNunit[index].GetValue())
        input = self.towhee.get_single_input(index)

        if input.get_inpstyle() != 3:
            input = self.towhee.create_input(3)

        input.set_nunit(nunit)
        input.set_nmaxcbmc(nmaxcbmc)

        NucleicAcidDlg = NucleicAcid(self, -1, "", input)
        if NucleicAcidDlg.ShowModal() == wx.ID_OK:
            self.input_error[index] = False
            value = NucleicAcidDlg.txtTerminus.GetValue()
            if self.CheckValue(value, "terminus", True):
                input.set_terminus(int(value))
            else:
                input.set_terminus("????")
                self.input_error[index] = True

            value = NucleicAcidDlg.txtForcefield.GetValue()
            if self.CheckValue(value, "forcefield"):
                input.set_forcefield(value)
            else:
                input.set_forcefield("????")
                self.input_error[index] = True

            monomername = []
            for i in NucleicAcidDlg.txtMonomername:
                value = i.GetValue()
                if self.CheckValue(value, "monomername"):
                    monomername.append(value)
                else:
                    monomername.append("????")
                    self.input_error[index] = True
            input.set_monomername(monomername)

            self.towhee.set_single_input(index, input)
        return

    def HandleInpstyle4(self, index):
        input = self.towhee.get_single_input(index)

        if input.get_inpstyle() != 4:
            input = self.towhee.create_input(4)

        NanotubeDlg = Nanotube(self, -1, "", input)
        if NanotubeDlg.ShowModal() == wx.ID_OK:
            self.input_error[index] = False
            value = NanotubeDlg.txtForcefield.GetValue()
            if self.CheckValue(value, "forcefield"):
                input.set_forcefield(value)
            else:
                input.set_forcefield("????")
                self.input_error[index] = True

            value = NanotubeDlg.txtAtomname.GetValue()
            if self.CheckValue(value, "atomname"):
                input.set_atomname(value)
            else:
                input.set_atomname("????")
                self.input_error[index] = True

            value = NanotubeDlg.txtQqatom.GetValue()
            if self.CheckValue(value, "qqatom"):
                input.set_qqatom(value)
            else:
                input.set_qqatom("????")
                self.input_error[index] = True

            value = NanotubeDlg.txtNanotube_n.GetValue()
            if self.CheckValue(value, "nanotube_n", True):
                input.set_n(int(value))
            else:
                input.set_n("????")
                self.input_error[index] = True

            value = NanotubeDlg.txtNanotube_m.GetValue()
            if self.CheckValue(value, "nanotube_m", True):
                input.set_m(int(value))
            else:
                input.set_m("????")
                self.input_error[index] = True

            value = NanotubeDlg.txtNanotube_ncells.GetValue()
            if self.CheckValue(value, "nanotube_ncells", True):
                input.set_ncells(int(value))
            else:
                input.set_ncells("????")
                self.input_error[index] = True

            value = NanotubeDlg.txtNanotube_bondlength.GetValue()
            if self.CheckValue(value, "nanotube_bondlength"):
                input.set_bondlength(value)
            else:
                input.set_bondlength("????")
                self.input_error[index] = True

            self.towhee.set_single_input(index, input)
        return

    def SaveAndExit(self, *args):
        #
        # Basic Tab
        #
        value = self.txtRandomseed.GetValue()
        if self.CheckValue(value, "randomseed", True):
            self.towhee.set_randomseed(int(value))
        else:
            self.txtRandomseed.SetValue("????")
            return

        self.towhee.set_ensemble(self.cboEnsemble.GetValue())
        
        value = self.txtNmolty.GetValue()
        if self.CheckValue(value, "nmolty", True):
            self.towhee.set_nmolty(int(value))
        else:
            self.txtNmolty.SetValue("????")
            return

        value = self.txtNumboxes.GetValue()
        if self.CheckValue(value, "numboxes", True):
            self.towhee.set_numboxes(int(value))
        else:
            self.txtNumboxes.SetValue("????")
            return
        #
        # Run Info Tab
        #
        value = self.txtTemperature.GetValue()
        if self.CheckValue(value, "temperature"):
            self.towhee.set_temperature(value)
        else:
            self.txtTemperature.SetValue("????")
            return
            
        if self.towhee.get_ensemble() == "npt":
            value = self.txtPressure.GetValue()
            if self.CheckValue(value, "pressure"):
                self.towhee.set_pressure(value)
            else:
                self.txtPressure.SetValue("????")
                return

        if self.towhee.get_ensemble() == "uvt":
            self.towhee.clear_chempot()
            for stuff in self.txtChempot:
                value = stuff.GetValue()
                if self.CheckValue(value, "chempot"):
                    self.towhee.append_chempot(value)
                else:
                    stuff.SetValue("????")
                    return

        self.towhee.clear_nmolectyp()
        for stuff in self.txtNmolectype:
            value = stuff.GetValue()
            if self.CheckValue(value, "nmolectyp", True):
                self.towhee.append_nmolectyp(int(value))
            else:
                stuff.SetValue("????")
                return

        self.towhee.set_stepstyle(self.cboStepstyle.GetValue())

        if self.towhee.get_stepstyle() == "minimize":
            value = self.txtOptstyle.GetValue()
            if self.CheckValue(value, "optstyle", True):
                self.towhee.set_optstyle(int(value))
            else:
                self.txtOptstyle.SetValue("????")
                return

            value = self.txtMintol.GetValue()
            if self.CheckValue(value, "mintol"):
                self.towhee.set_mintol(value)
            else:
                self.txtMintol.SetValue("????")
                return
        else:
            value = self.txtNstep.GetValue()
            if self.CheckValue(value, "nstep", True):
                self.towhee.set_nstep(int(value))
            else:
                self.txtNstep.SetValue("????")
                return

        value = self.cboRunoutput.GetValue()
        if self.CheckValue(value, "runoutput"):
            self.towhee.set_runoutput(value)
        else:
            self.cboRunoutput.SetValue("full")
            return

        value = self.txtPrintfreq.GetValue()
        if self.CheckValue(value, "printfreq", True):
            self.towhee.set_printfreq(int(value))
        else:
            self.txtPrintfreq.SetValue("????")
            return

        value = self.txtBlocksize.GetValue()
        if self.CheckValue(value, "blocksize", True):
            self.towhee.set_blocksize(int(value))
        else:
            self.txtBlocksize.SetValue("????")
            return

        value = self.txtMoviefreq.GetValue()
        if self.CheckValue(value, "moviefreq", True):
            self.towhee.set_moviefreq(int(value))
        else:
            self.txtMoviefreq.SetValue("????")
            return

        value = self.txtBackupfreq.GetValue()
        if self.CheckValue(value, "backupfreq", True):
            self.towhee.set_backupfreq(int(value))
        else:
            self.txtBackupfreq.SetValue("????")
            return

        value = self.txtPdbOutputFreq.GetValue()
        if self.CheckValue(value, "pdb_output_freq", True):
            self.towhee.set_pdb_output_freq(int(value))
        else:
            self.txtPdbOutputFreq.SetValue("????")
            return
            
        if self.rbLoutdft.GetSelection():
            self.towhee.set_loutdft_false()
        else:
            self.towhee.set_loutdft_true()

        if self.rbLoutlammps.GetSelection():
            self.towhee.set_loutlammps_false()
        else:
            self.towhee.set_loutlammps_true()

        if self.towhee.get_ensemble() == "uvt":
            if self.rbLouthist.GetSelection():
                self.towhee.set_louthist_false()
            else:
                self.towhee.set_louthist_true()

            if self.towhee.get_louthist():
                value = self.txtHistcalcfreq.GetValue()
                if self.CheckValue(value, "histcalcfreq", True):
                    self.towhee.set_histcalcfreq(int(value))
                else:
                    self.txtHistcalcfreq.SetValue("????")
                    return

                value = self.txtHistdumpfreq.GetValue()
                if self.CheckValue(value, "histdumpfreq", True):
                    self.towhee.set_histdumpfreq(int(value))
                else:
                    self.txtHistdumpfreq.SetValue("????")
                    return

        value = self.txtPressurefreq.GetValue()
        if self.CheckValue(value, "pressurefreq", True):
            self.towhee.set_pressurefreq(int(value))
        else:
            self.txtPressurefreq.SetValue("????")
            return

        value = self.txtTrmaxdispfreq.GetValue()
        if self.CheckValue(value, "trmaxdispfreq", True):
            self.towhee.set_trmaxdispfreq(int(value))
        else:
            self.txtTrmaxdispfreq.SetValue("????")
            return

        value = self.txtVolmaxdispfreq.GetValue()
        if self.CheckValue(value, "Volmaxdispfreq", True):
            self.towhee.set_volmaxdispfreq(int(value))
        else:
            self.txtVolmaxdispfreq.SetValue("????")
            return

        self.towhee.clear_chempotperstep()
        for stuff in self.txtChempotperstep:
            value = stuff.GetValue()
            if self.CheckValue(value, "chempotperstep", True):
                self.towhee.append_chempotperstep(int(value))
            else:
                stuff.SetValue("????")
                return
        #
        # Force Field Tab
        #
        value = self.cboPotentialStyle.GetValue()
        if self.CheckValue(value, "potientialstyle"):
            self.towhee.set_potentialstyle(value)
        else:
            self.cboPotentialStyle.SetValue("classical")
            return

        if self.towhee.get_potentialstyle() == "classical" or\
        self.towhee.get_potentialstyle() == "quantim//classical":
            value = self.txtFfnumber.GetValue()
            if self.CheckValue(value, "ffnumber", True):
                self.towhee.set_ffnumber(int(value))
            else:
                self.txtFfnumber.SetValue("????")
                return

            self.towhee.clear_ff_filename()
            for i in self.txtFf_filename:
                value = i.GetValue()
                if self.CheckValue(value, "ff_filename"):
                    self.towhee.append_ff_filename(value)
                else:
                    i.SetValue("????")
                    return

            value = self.txtIsolvtype.GetValue()
            if self.CheckValue(value, "isolvtype", True):
                self.towhee.set_isolvtype(int(value))
            else:
                self.txtIsolvtype.SetValue("????")
                return

            value = self.cboClassicalPotential.GetValue()
            if self.CheckValue(value, "classical_potential", False):
                self.towhee.set_classical_potential(value)
            else:
                self.cboClassicalPotential.SetValue("9-6")
                return

            read_mixrule = False
            read_interpolatestyle = False
            read_lshift = False
            read_ltailc = False
            read_rmin = False
            read_rcut = False
            read_rcutin = False
            read_rpd = False
            if self.towhee.get_classical_potential() == "Lennard-Jones" or\
            self.towhee.get_classical_potential() == "9-6" or\
            self.towhee.get_classical_potential() == "12-6 plus solvation" or\
            self.towhee.get_classical_potential() == "12-9-6" or\
            self.towhee.get_classical_potential() == "12-6 plus 12-10 H-bond" or\
            self.towhee.get_classical_potential() == "Exponential-12-6" or\
            self.towhee.get_classical_potential() == "Gordon n-6":
                read_mixrule = True
                read_lshift = True
                read_ltailc = True
                read_rmin = True
                read_rcut = True
                read_rcutin = True
            elif self.towhee.get_classical_potential() == "Exponential-6":
                read_mixrule = True
                read_lshift = True
                read_ltailc = True
                read_rcut = True
                read_rcutin = True
            elif self.towhee.get_classical_potential() == "Hard Sphere" or\
            self.towhee.get_classical_potential() == "Square Well":
                read_mixrule = True
                read_rpd = True
            elif self.towhee.get_classical_potential() == "Repulsive Sphere" or\
            self.towhee.get_classical_potential() == "Repulsive Well" or\
            self.towhee.get_classical_potential() == "Multiwell" or\
            self.towhee.get_classical_potential() == "Repulsive Multiwell":
                read_mixrule = True
            elif self.towhee.get_classical_potential() == "Stillinger-Weber":
                read_mixrule = True
            elif self.towhee.get_classical_potential() == "Embedded Atom Method":
                read_mixrule = True
                read_interpolatestyle = True
                read_rcut = True
            elif self.towhee.get_classical_potential() == "Tabulated Pair":
                read_mixrule = True
                read_interpolatestyle = True
            else:
                print "Invalid classical_potential!"

            if read_mixrule:
                value = self.cboClassicalMixrule.GetValue()
                if self.CheckValue(value, "classical_mixrule", False):
                    self.towhee.set_classical_mixrule(value)
                else:
                    self.cboClassicalMixrule.SetValue("Explicit")
                    return

                value = self.cboCmixRescalingStyle.GetValue()
                if self.CheckValue(value, "cmix rescaling style", False):
                    self.towhee.set_cmix_rescaling_style(value)
                else:
                    self.cboCmixRescalingStyle.SetValue("none")
                    return

                if self.towhee.get_cmix_rescaling_style() == "grossfield 2003":
                    value = self.txtCmixLambda.GetValue()
                    if self.CheckValue(value, "cmix lambda", False):
                        self.towhee.set_cmix_lambda(value)
                    else:
                        self.txtCmixLambda.SetValue("????")
                        return

                    value = self.txtCmixNpair.GetValue()
                    if self.CheckValue(value, "cmix npair", True):
                        self.towhee.set_cmix_npair(int(value))
                    else:
                        self.txtCmixNpair.SetValue("????")
                        return

                    self.towhee.clear_cmix_pair_list()
                    for npair in range(self.towhee.get_cmix_npair()):
                        value = self.txtCmixPairList[npair].GetValue()
                        if self.CheckValue(value, "cmix pair list", False):
                            self.towhee.append_cmix_pair_list(value)
                        else:
                            self.txtCmixPairList[npair].SetValue("????")
                            return

            if read_interpolatestyle:
                if self.CheckValue(value, "interpolatestyle"):
                    self.towhee.set_interpolatestyle(value)
                else:
                    self.txtInterpolatestyle.SetValue("????")
                    return

            if read_lshift:
                if self.rbLshift.GetSelection():
                    self.towhee.set_lshift_false()
                else:
                    self.towhee.set_lshift_true()

            if read_ltailc:
                if self.rbLtailc.GetSelection():
                    self.towhee.set_ltailc_false()
                else:
                    self.towhee.set_ltailc_true()

            if read_rmin:
                value = self.txtRmin.GetValue()
                if self.CheckValue(value, "rmin"):
                    self.towhee.set_rmin(value)
                else:
                    self.txtRmin.SetValue("????")
                    return

            if read_rcut:
                value = self.txtRcut.GetValue()
                if self.CheckValue(value, "rcut"):
                    self.towhee.set_rcut(value)
                else:
                    self.txtRcut.SetValue("????")
                    return

            if read_rcutin:
                value = self.txtRcutin.GetValue()
                if self.CheckValue(value, "rcutin"):
                    self.towhee.set_rcutin(value)
                else:
                    self.txtRcutin.SetValue("????")
                    return

            if read_rpd:
                value = self.txtRadialPressureDelta.GetValue()
                if self.CheckValue(value, "radial pressure delta"):
                    self.towhee.set_radial_pressure_delta(value)
                else:
                    self.txtRadialPressureDelta.SetValue("????")
                    return

            self.towhee.set_coulombstyle(self.cboCoulombstyle.GetValue())

            if self.towhee.get_coulombstyle() == "ewald_fixed_kmax":
                value = self.txtKalp.GetValue()
                if self.CheckValue(value, "kalp"):
                    self.towhee.set_kalp(value)
                else:
                    self.txtKalp.SetValue("????")
                    return

                value = self.txtKmax.GetValue()
                if self.CheckValue(value, "kmax", True):
                    self.towhee.set_kmax(int(value))
                else:
                    self.txtKmax.SetValue("????")
                    return

                value = self.txtDielectric.GetValue()
                if self.CheckValue(value, "dielectric"):
                    self.towhee.set_dielect(value)
                else:
                    self.txtDielectric.SetValue("????")
                    return
            elif self.towhee.get_coulombstyle() == "ewald_fixed_cutoff":
                value = self.txtEwald_prec.GetValue()
                if self.CheckValue(value, "ewald_prec"):
                    self.towhee.set_ewald_prec(value)
                else:
                    self.txtEwald_prec.SetValue("????")
                    return

                value = self.txtRcelect.GetValue()
                if self.CheckValue(value, "rcelect"):
                    self.towhee.set_rcelect(value)
                else:
                    self.txtRcelect.SetValue("????")
                    return

                value = self.txtDielectric.GetValue()
                if self.CheckValue(value, "dielectric"):
                    self.towhee.set_dielect(value)
                else:
                    self.txtDielectric.SetValue("????")
                    return
            elif self.towhee.get_coulombstyle() == "minimum image":
                value = self.txtDielectric.GetValue()
                if self.CheckValue(value, "dielectric"):
                    self.towhee.set_dielect(value)
                else:
                    self.txtDielectric.SetValue("????")
                    return
            elif self.towhee.get_coulombstyle() != "none":
                print "Invalid!"
                return

            value = self.txtNfield.GetValue()
            if self.CheckValue(value, "nfield", True):
                self.towhee.set_nfield(int(value))
            else:
                self.txtNfield.SetValue("????")
                return
            #
            # External Field Tab
            #
            hrdindex = 0
            hafindex = 0
            ljindex = 0
            umbindex = 0
            steeleindex = 0
            self.towhee.clear_externalfields()
            for i in range(self.towhee.get_nfield()):
                value = self.cboFieldType[i].GetValue()
                if self.CheckValue(value, "fieldtype", False):
                    ef = self.towhee.create_externalfield(value)
                else:
                    self.cboFieldType[i].SetValue("Hard Wall")
                    return

                if ef.get_fieldtype() == "Hard Wall":
                    value = self.txtHrdbox[hrdindex].GetValue()
                    if self.CheckValue(value, "hrdbox", True):
                        ef.set_box(int(value))
                    else:
                        self.txtHrdbox[hrdindex].SetValue("????")
                        return

                    value = self.txtHrdxyz[hrdindex].GetValue()
                    if self.CheckValue(value, "hrdxyz"):
                        ef.set_xyz(value)
                    else:
                        self.txtHrdxyz[hrdindex].SetValue("????")
                        return

                    value = self.txtHrdcen[hrdindex].GetValue()
                    if self.CheckValue(value, "hrdcen"):
                        ef.set_cen(value)
                    else:
                        self.txtHrdcen[hrdindex].SetValue("????")
                        return

                    value = self.txtHrdrad[hrdindex].GetValue()
                    if self.CheckValue(value, "hrdrad"):
                        ef.set_rad(value)
                    else:
                        self.txtHrdrad[hrdindex].SetValue("????")
                        return

                    value = self.cboHrdEnergyType[hrdindex].GetValue()
                    if self.CheckValue(value, "hrd_energy_type", False):
                        ef.set_energy_type(value)
                    else:
                        self.cboHrdEnergyType[hrdindex].SetValue("????")
                        return

                    if ef.get_energy_type() == "finite":
                        value = self.txtHrdWallEnergy[hrdindex].GetValue()
                        if self.CheckValue(value, "hrd_wall_energy"):
                            ef.set_wall_energy(value)
                        else:
                            self.txtHrdWallEnergy[hrdindex].SetValue("????")
                            return

                    hrdindex+=1
                    self.towhee.append_externalfields(ef)
                elif ef.get_fieldtype() == "Harmonic Attractor":
                    value = self.txtHafbox[hrdindex].GetValue()
                    if self.CheckValue(value, "hafbox", True):
                        ef.set_box(int(value))
                    else:
                        self.txtHafbox[hafindex].SetValue("????")
                        return

                    value = self.txtHafk[hafindex].GetValue()
                    if self.CheckValue(value, "hafk"):
                        ef.set_k(value)
                    else:
                        self.txtHafk[hafindex].SetValue("????")
                        return

                    value = self.txtHafnentries[hafindex].GetValue()
                    if self.CheckValue(value, "hafnentries", True):
                        ef.set_nentries(int(value))
                    else:
                        self.txtHafnentries[hrdindex].SetValue("????")
                        return

                    value = self.cboHafrefpos[hafindex].GetValue()
                    if self.CheckValue(value, "hafrefpos", False):
                        ef.set_refpos(value)
                    else:
                        self.cboHafrefpos[hafindex].SetValue("????")
                        return

                    if ef.get_refpos() == "Global":
                        value = self.txtHafglobx[hafindex].GetValue()
                        if self.CheckValue(value, "hafglobx"):
                            ef.set_globx(value)
                        else:
                            self.txtHafglobx[hafindex].SetValue("????")
                            return

                        value = self.txtHafgloby[hafindex].GetValue()
                        if self.CheckValue(value, "hafgloby"):
                            ef.set_globy(value)
                        else:
                            self.txtHafgloby[hafindex].SetValue("????")
                            return

                        value = self.txtHafglobz[hafindex].GetValue()
                        if self.CheckValue(value, "hafglobz"):
                            ef.set_globz(value)
                        else:
                            self.txtHafglobz[hafindex].SetValue("????")
                            return

                    value = self.cboHafkey[hafindex].GetValue()
                    if self.CheckValue(value, "hafkey"):
                        ef.set_key(value)
                    else:
                        self.cboHafkey[hafindex].SetValue("????")
                        return

                    for z in range(ef.get_nentries()):
                        value = self.txtHafmolec[hafindex][z].GetValue()
                        if self.CheckValue(value, "hafmolec", True):
                            ef.append_molec(int(value))
                        else:
                            self.txtHafmolec[hafindex][z].SetValue("????")
                            return

                        if ef.get_key() == "Element":
                            value = self.txtHafelement[hafindex][z].GetValue()
                            if self.CheckValue(value, "hafelement"):
                                ef.append_element(value)
                                ef.append_name("")   # !!! I don't like doing this
                            else:
                                self.txtHafelement[hafindex][z].SetValue("????")
                                return
                        else:
                            value = self.txtHafname[hafindex][z].GetValue()
                            if self.CheckValue(value, "hafname"):
                                ef.append_name(value)
                                ef.append_element("")   # !!! I don't like doing this
                            else:
                                self.txtHafname[hafindex][z].SetValue("????")
                                return
                    hafindex+=1
                    self.towhee.append_externalfields(ef)
                elif ef.get_fieldtype() == "LJ 9-3 Wall":
                    value = self.txtLjfbox[ljindex].GetValue()
                    if self.CheckValue(value, "ljfbox", True):
                        ef.set_box(int(value))
                    else:
                        self.txtLjfbox[ljindex].SetValue("????")
                        return

                    value = self.txtLjfxyz[ljindex].GetValue()
                    if self.CheckValue(value, "ljfxyz"):
                        ef.set_xyz(value)
                    else:
                        self.txtLjfxyz[ljindex].SetValue("????")
                        return

                    value = self.txtLjfcen[ljindex].GetValue()
                    if self.CheckValue(value, "ljfcen"):
                        ef.set_cen(value)
                    else:
                        self.txtLjfcen[ljindex].SetValue("????")
                        return

                    value = self.txtLjfdir[ljindex].GetValue()
                    if self.CheckValue(value, "ljfdir", True):
                        ef.set_dir(int(value))
                    else:
                        self.txtLjfdir[ljindex].SetValue("????")
                        return

                    value = self.txtLjfcut[ljindex].GetValue()
                    if self.CheckValue(value, "ljfcut"):
                        ef.set_cut(value)
                    else:
                        self.txtLjfcut[ljindex].SetValue("????")
                        return

                    if self.rbLjfshift[ljindex].GetSelection():
                        ef.set_shift_false()
                    else:
                        ef.set_shift_true()

                    value = self.txtLjfrho[ljindex].GetValue()
                    if self.CheckValue(value, "ljfrho"):
                        ef.set_rho(value)
                    else:
                        self.txtLjfrho[ljindex].SetValue("????")
                        return

                    value = self.txtLjfntypes[ljindex].GetValue()
                    if self.CheckValue(value, "ljfntypes", True):
                        ef.set_ntypes(int(value))
                    else:
                        ef.set_ntypes(1)
                        self.txtLjfntypes[ljindex].SetValue("????")
                        return

                    for j in range(ef.get_ntypes()):
                        value = self.txtLjfname[ljindex][j].GetValue()
                        if self.CheckValue(value, "ljfname"):
                            ef.append_name(value)
                        else:
                            self.txtLjfname[ljindex][j].SetValue("????")
                            return

                        value = self.txtLjfsig[ljindex][j].GetValue()
                        if self.CheckValue(value, "ljfsig"):
                            ef.append_sig(value)
                        else:
                            self.txtLjfsig[ljindex][j].SetValue("????")
                            return

                        value = self.txtLjfeps[ljindex][j].GetValue()
                        if self.CheckValue(value, "ljfeps"):
                            ef.append_eps(value)
                        else:
                            self.txtLjfeps[ljindex][j].SetValue("????")
                            return
                    ljindex+=1
                    self.towhee.append_externalfields(ef)
                elif ef.get_fieldtype() == "Hooper Umbrella":
                    value = self.txtUmbbox[umbindex].GetValue()
                    if self.CheckValue(value, "umbbox", True):
                        ef.set_box(int(value))
                    else:
                        self.txtUmbbox[umbindex].SetValue("????")
                        return

                    value = self.txtUmbxyz[umbindex].GetValue()
                    if self.CheckValue(value, "umbxyz"):
                        ef.set_xyz(value)
                    else:
                        self.txtUmbxyz[umbindex].SetValue("????")
                        return

                    value = self.txtUmbcenter[umbindex].GetValue()
                    if self.CheckValue(value, "umbcenter"):
                        ef.set_center(value)
                    else:
                        self.txtUmbcenter[umbindex].SetValue("????")
                        return

                    value = self.txtUmba[umbindex].GetValue()
                    if self.CheckValue(value, "umba"):
                        ef.set_a(value)
                    else:
                        self.txtUmba[umbindex].SetValue("????")
                        return
                    umbindex+=1
                    self.towhee.append_externalfields(ef)
                elif ef.get_fieldtype() == "Steele Wall":
                    value = self.txtSteelebox[steeleindex].GetValue()
                    if self.CheckValue(value, "steelebox", True):
                        ef.set_box(int(value))
                    else:
                        self.txtSteelebox[steeleindex].SetValue("????")
                        return

                    value = self.txtSteelexyz[steeleindex].GetValue()
                    if self.CheckValue(value, "steele xyz"):
                        ef.set_xyz(value)
                    else:
                        self.txtSteelexyz[steeleindex].SetValue("????")
                        return

                    value = self.txtSteelesurface[steeleindex].GetValue()
                    if self.CheckValue(value, "steele surface"):
                        ef.set_surface(value)
                    else:
                        self.txtSteelesurface[steeleindex].SetValue("????")
                        return

                    value = self.txtSteeledir[steeleindex].GetValue()
                    if self.CheckValue(value, "steele dir", True):
                        ef.set_dir(int(value))
                    else:
                        self.txtSteeledir[steeleindex].SetValue("????")
                        return

                    value = self.txtSteelecutoff[steeleindex].GetValue()
                    if self.CheckValue(value, "steele cutoff"):
                        ef.set_cutoff(value)
                    else:
                        self.txtSteelecutoff[steeleindex].SetValue("????")
                        return

                    if self.rbSteeleshift[steeleindex].GetSelection():

                        ef.set_shift_false()
                    else:
                        ef.set_shift_true()

                    value = self.txtSteeledelta[steeleindex].GetValue()
                    if self.CheckValue(value, "steele delta"):
                        ef.set_delta(value)
                    else:
                        self.txtSteeledelta[steeleindex].SetValue("????")
                        return

                    value = self.txtSteelerho_s[steeleindex].GetValue()
                    if self.CheckValue(value, "steele rho_s"):
                        ef.set_rho_s(value)
                    else:
                        self.txtSteelerho_s[steeleindex].SetValue("????")
                        return

                    value = self.txtSteelentype[steeleindex].GetValue()
                    if self.CheckValue(value, "steele ntype", True):
                        ef.set_ntype(int(value))
                    else:
                        ef.set_ntype(1)
                        self.txtLjfntypes[steeleindex].SetValue("????")
                        return

                    for j in range(ef.get_ntype()):
                        value = self.txtSteelename[steeleindex][j].GetValue()
                        if self.CheckValue(value, "steele name"):
                            ef.append_name(value)
                        else:
                            self.txtSteelename[steeleindex][j].SetValue("????")
                            return

                        value = self.txtSteelesigma_sf[steeleindex][j].GetValue()
                        if self.CheckValue(value, "steele sigma_sf"):
                            ef.append_sigma_sf(value)
                        else:
                            self.txtSteelesigma_sf[steeleindex][j].SetValue("????")
                            return

                        value = self.txtSteeleepsilon_sf[steeleindex][j].GetValue()
                        if self.CheckValue(value, "steele epsilon_sf"):
                            ef.append_epsilon_sf(value)
                        else:
                            self.txtSteeleepsilon_sf[steeleindex][j].SetValue("????")
                            return
                    steeleindex+=1
                    self.towhee.append_externalfields(ef)
        #
        # Initialiaztion Tab
        #
        if self.rbLinit.GetSelection():
            self.towhee.set_linit_false()
        else:
            self.towhee.set_linit_true()

        self.towhee.set_initboxtype(self.cboInitboxtype.GetValue())

        if self.towhee.get_initboxtype() != "unit cell":
            self.towhee.clear_initstyle()
            for i in range(self.towhee.get_numboxes()):
                T = []
                for j in range(self.towhee.get_nmolty()):
                    value = self.cboInitstyle[i][j].GetValue()
                    if self.CheckValue(value, "initstyle"):
                        T.append(value)
                    else:
                        self.cboInitstyle[i][j].SetValue("????")
                        return
                self.towhee.append_initstyle(T)

            self.towhee.clear_initlattice()
            for i in range(self.towhee.get_numboxes()):
                T = []
                for j in range(self.towhee.get_nmolty()):
                    value = self.cboInitlattice[i][j].GetValue()
                    if self.CheckValue(value, "initlattice"):
                        T.append(value)
                    else:
                        self.cboInitlattice[i][j].SetValue("????")
                        return
                self.towhee.append_initlattice(T)
            #
            # Have to go through the initstyles to throw out any helix variables that don't belong
            # And then if we had detected a helix variable error before, recheck all the helix variables
            # because I could have thrown out the one with the error.  I know, I could make them go back and check,
            # but I am feeling kind
            #
            helixes = []
            for i in range(self.towhee.get_nmolty()):
                helix = False
                for j in range(self.towhee.get_numboxes()):
                    initstyle = self.cboInitstyle[j][i].GetValue()
                    if initstyle == "helix":
                        helix = True
                if helix == True:
                    helixes.append(i)
            if len(helixes) == 0: # Easy case
                self.towhee.clear_helix()
            else:
                # Make sure there are no new helixes that weren't set yet
                extra = False
                for i in helixes:
                    not_there = True
                    for h in self.towhee.get_helix():
                        if i == h.get_nmolty():
                            not_there = False
                    if not_there:
                        extra = True
                if extra:
                    d = wx.MessageDialog(self,
                        "Error:  I've detected unset helix variables",
                        "Helix Value Error",
                        wx.ICON_ERROR)
                    d.ShowModal()
                    d.Destroy()
                    return
                # Delete the ones that don't belong any more
                index = []
                all_helixes = self.towhee.get_helix()
                keepGoing = True
                while(keepGoing):
                    for i in range(len(all_helixes)):
                        if all_helixes[i].get_nmolty() not in helixes:
                            del all_helixes[i]
                            break
                        else:
                            keepGoing = False
                self.towhee.set_helix(all_helixes)
                # If there was a failure before, we could have just removed it... so recheck
                still_failure = False
                for helix in self.towhee.get_helix():
                    still_failure = self.CheckValue(str(helix.get_moltyp()), "helix_moltyp", True)
                    if still_failure == False: return
                    still_failure = self.CheckValue(helix.get_radius(), "helix_radius")
                    if still_failure == False: return
                    still_failure = self.CheckValue(helix.get_angle(), "helix_angle")
                    if still_failure == False: return
                    still_failure = self.CheckValue(helix.get_keytype(), "helix_keytype")
                    if still_failure == False: return
                    still_failure = self.CheckValue(helix.get_keyname(), "helix_keyname")
                    if still_failure == False: return
                    still_failure = self.CheckValue(helix.get_conlen(), "helix_conlen")
                    if still_failure == False: return
                    still_failure = self.CheckValue(helix.get_phase(), "helix_phase")
                    if still_failure == False: return
                self.helix_failure = False

            self.towhee.clear_initmol()
            for i in range(self.towhee.get_numboxes()):
                T = []
                for j in range(self.towhee.get_nmolty()):
                    value = self.txtInitmol[i][j].GetValue()
                    if self.CheckValue(value, "initmol", True):
                        T.append(int(value))
                    else:
                        self.txtInitmol[i][j].SetValue("????")
                        return
                self.towhee.append_initmol(T)

        if self.towhee.get_initboxtype() == "dimensions":
            self.towhee.clear_hmatrix()
            for i in range(self.towhee.get_numboxes()):
                hm = self.towhee.create_hmatrix()
                T = []
                value = self.txtHmatrix[9*i].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i].SetValue("????")
                    return

                value = self.txtHmatrix[9*i+1].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+1].SetValue("????")
                    return

                value = self.txtHmatrix[9*i+2].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+2].SetValue("????")
                    return
                hm.set_row1(T)

                T = []
                value = self.txtHmatrix[9*i+3].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+3].SetValue("????")
                    return

                value = self.txtHmatrix[9*i+4].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+4].SetValue("????")
                    return

                value = self.txtHmatrix[9*i+5].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+5].SetValue("????")
                    return
                hm.set_row2(T)

                T = []
                value = self.txtHmatrix[9*i+6].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+6].SetValue("????")
                    return

                value = self.txtHmatrix[9*i+7].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+7].SetValue("????")
                    return

                value = self.txtHmatrix[9*i+8].GetValue()
                if self.CheckValue(value, "hmatrix"):
                    T.append(value)
                else:
                    self.txtHmatrix[9*i+8].SetValue("????")
                    return
                hm.set_row3(T)

                self.towhee.append_hmatrix(hm)
        elif self.towhee.get_initboxtype() == "number density":
            self.towhee.clear_box_number_density()
            for i in range(self.towhee.get_numboxes()):
                value = self.txtBoxNumberDensity[i].GetValue()
                if self.CheckValue(value, "box number density"):
                    self.towhee.append_box_number_density(value)
                else:
                    self.txtBoxNumberDensity[i].SetValue("????")
                    return

        self.towhee.clear_inix()
        self.towhee.clear_iniy()
        self.towhee.clear_iniz()
        for i in range(self.towhee.get_numboxes()):
            value = self.txtInixyz[3*i].GetValue()
            if self.CheckValue(value, "inix", True):
                self.towhee.append_inix(int(value))
            else:
                self.txtInixyz[3*i].SetValue("????")
                return

            value = self.txtInixyz[3*i+1].GetValue()
            if self.CheckValue(value, "iniy", True):
                self.towhee.append_iniy(int(value))
            else:
                self.txtInixyz[3*i+1].SetValue("????")
                return

            value = self.txtInixyz[3*i+2].GetValue()
            if self.CheckValue(value, "iniz", True):
                self.towhee.append_iniz(int(value))
            else:
                self.txtInixyz[3*i+2].SetValue("????")
                return
        #
        # Monte Carlo Moves Tab... I don't have to get the details of each
        # move because they are saved whenever they are change.  I just have
        # to get the probabilities because they could change.  Then I have to
        # double check to make sure there are no errors
        #
        if (self.towhee.get_ensemble() == "nvt" and self.towhee.get_numboxes() > 1)\
        or self.towhee.get_ensemble() == "npt":
            #
            # Isotropic Volume Move
            #
            mcm = self.towhee.get_ivm()
            value = self.txtPmvol.GetValue()
            if self.CheckValue(value, "pmvol"):
                mcm.set_move_probability(value)
                self.towhee.set_ivm(mcm)
            else:
                mcm.set_move_probability("????")
                self.txtPmvol.SetValue("????")
                self.ivm_failure = True
                self.towhee.set_ivm(mcm)
                return

            if self.ivm_failure:
                d = wx.MessageDialog(self,
                    "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                    "Isotropic Volume Move",
                    "Isotropic Volume Move Error",
                    wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                return
            #
            # Anisotropic Volume Move
            #
            mcm = self.towhee.get_avm()
            value = self.txtPmcell.GetValue()
            if self.CheckValue(value, "pmcell"):
                mcm.set_move_probability(value)
                self.towhee.set_avm(mcm)
            else:
                mcm.set_move_probability("????")
                self.txtPmcell.SetValue("????")
                self.avm_failure = True
                self.towhee.set_avm(mcm)
                return

            if self.avm_failure:
                d = wx.MessageDialog(self,
                    "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                    "Anisotropic Volume Move",
                    "Anisotropic Volume Move Error",
                    wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                return

        if self.towhee.get_ensemble() == "uvt":
            #
            # Configurational-bias Grand-Canonical Insertion/Deletion Move
            #
            mcm = self.towhee.get_cbgcidm()
            value = self.txtPmuvtcbswap.GetValue()
            if self.CheckValue(value, "pmuvtcbswap"):
                mcm.set_move_probability(value)
                self.towhee.set_cbgcidm(mcm)
            else:
                mcm.set_move_probability("????")
                self.txtPmuvtcbswap.SetValue("????")
                self.gcid_failure = True
                self.towhee.set_cbgcidm(mcm)
                return

            if self.gcid_failure:
                d = wx.MessageDialog(self,
                    "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                    "Configurational-bias Grand-Canonical Insertion/Deletion Move",
                    "Configurational-bias Grand-Canonical Insertion/Deletion Move Error",
                    wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                return

        if self.towhee.get_numboxes() > 1:
            #
            # Rotational-bias 2 box molecule Transfer Move
            #
            mcm = self.towhee.get_rb2bmtm()
            value = self.txtPm2boxrbswap.GetValue()
            if self.CheckValue(value, "pm2boxrbswap"):
                mcm.set_move_probability(value)
                self.towhee.set_rb2bmtm(mcm)
            else:
                mcm.set_move_probability("????")
                self.txtPm2boxrbswap.SetValue("????")
                self.cb2bmtm_failure = True
                self.towhee.set_rb2bmtm(mcm)
                return

            if self.rb2bmtm_failure:
                d = wx.MessageDialog(self,
                    "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                    "Rotational-bias 2 box molecule Transfer Move",
                    "Rotational-bias 2 box molecule Transfer Move Error",
                    wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                return
            #
            # Configurational-bias 2 box molecule Transfer Move
            #
            mcm = self.towhee.get_cb2bmtm()
            value = self.txtPm2boxcbswap.GetValue()
            if self.CheckValue(value, "pm2boxcbswap"):
                mcm.set_move_probability(value)
                self.towhee.set_cb2bmtm(mcm)
            else:
                mcm.set_move_probability("????")
                self.txtPm2boxcbswap.SetValue("????")
                self.rb2bmtm_failure = True
                self.towhee.set_cb2bmtm(mcm)
                return

            if self.cb2bmtm_failure:
                d = wx.MessageDialog(self,
                    "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                    "Configurational-bias 2 box molecule Transfer Move",
                    "Configurational-bias 2 box molecule Transfer Move Error",
                    wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                return
        #
        # Configurational-bias single box molecule Reinsertion Move
        #
        mcm = self.towhee.get_cbsbmrm()
        value = self.txtPm1boxcbswap.GetValue()
        if self.CheckValue(value, "pm1boxcbswap"):
            mcm.set_move_probability(value)
            self.towhee.set_cbsbmrm(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPm1boxcbswap.SetValue("????")
            self.cbsbmrm_failure = True
            self.towhee.set_cbsbmrm(mcm)
            return

        if self.cbsbmrm_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Configurational-bias single box molecule Reinsertion Move",
                "Configurational-bias single box molecule Reinsertion Move Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #
        # Aggregation Volume Bias Move Type 1
        #
        mcm = self.towhee.get_avbmt1()
        value = self.txtPmavb1.GetValue()
        if self.CheckValue(value, "pmavb1"):
            mcm.set_move_probability(value)
            self.towhee.set_avbmt1(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmavb1.SetValue("????")
            self.avbmt1_failure = True
            self.towhee.set_avbmt1(mcm)
            return
        
        if self.avbmt1_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Aggregation Volume Bias Move Type 1",
                "Aggregation Volume Bias Move Type 1 Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #
        # Aggregation Volume Bias Move Type 2
        #
        mcm = self.towhee.get_avbmt2()
        value = self.txtPmavb2.GetValue()
        if self.CheckValue(value, "pmavb2"):
            mcm.set_move_probability(value)
            self.towhee.set_avbmt2(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmavb2.SetValue("????")
            self.avbmt2_failure = True
            self.towhee.set_avbmt2(mcm)
            return

        if self.avbmt2_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Aggregation Volume Bias Move Type 2",
                "Aggregation Volume Bias Move Type 2 Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #
        # Aggregation Volume Bias Move Type 3
        #
        mcm = self.towhee.get_avbmt3()
        value = self.txtPmavb3.GetValue()
        if self.CheckValue(value, "pmavb3"):
            mcm.set_move_probability(value)
            self.towhee.set_avbmt3(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmavb3.SetValue("????")
            self.avbmt3_failure = True
            self.towhee.set_avbmt3(mcm)
            return

        if self.avbmt3_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Aggregation Volume Bias Move Type 3",
                "Aggregation Volume Bias Move Type 3 Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #
        # Configurational-Bias Partial Molecule Regrowth
        #
        mcm = self.towhee.get_cbpmr()
        value = self.txtPmcb.GetValue()
        if self.CheckValue(self, "pmcb"):
            mcm.set_move_probability(value)
            self.towhee.set_cbpmr(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmcb.SetValue("????")
            self.cbpmr_failure = True
            self.towhee.set_cbpmr(mcm)
            return

        if self.cbpmr_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Configurational-Bias Partial Molecule Regrowth",
                "Configurational-Bias Partial Molecule Regrowth Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #            
        # Configurational-Bias Protein backbone Regrowth
        #
        mcm = self.towhee.get_cbpbr()
        value = self.txtPmback.GetValue()
        if self.CheckValue(value, "pmback"):
            mcm.set_move_probability(value)
            self.towhee.set_cbpbr(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmback.SetValue("????")
            self.cbpbr_failure = True
            self.towhee.set_cbpbr(mcm)
            return

        if self.cbpbr_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Configurational-Bias Protein Backbone Regrowth",
                "Configurational-Bias Protein Backbone Regrowth Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        # 
        # Torsional Pivot Move
        #
        mcm = self.towhee.get_tpm()
        value = self.txtPmpivot.GetValue()
        if self.CheckValue(value, "pmpivot"):
            mcm.set_move_probability(value)
            self.towhee.set_tpm(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmpivot.SetValue("????")
            self.tpm_failure = True
            self.towhee.set_tpm(mcm)
            return

        if self.tpm_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Torsional Pivot Move",
                "Torsional Pivot Move Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #         
        # Concerted Rotation Move on a non-peptide backbone
        #
        mcm = self.towhee.get_crnmoanpb()
        value = self.txtPmconrot.GetValue()
        if self.CheckValue(value, "pmconrot"):
            mcm.set_move_probability(value)
            self.towhee.set_crnmoanpb(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmconrot.SetValue("????")
            self.crmnpb_failure = True
            self.towhee.set_crnmoanpb(mcm)
            return

        if self.crmnpb_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Concerted Rotation Move on a non-peptide backbone",
                "Concerted Rotation Move on a non-peptide backbone Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #         
        # Concerted Rotation Move over a 3 peptides backbone sequence
        #
        mcm = self.towhee.get_crnmoa3pbs()
        value = self.txtPmcrback.GetValue()
        if self.CheckValue(value, "pmcrback"):
            mcm.set_move_probability(value)
            self.towhee.set_crnmoa3pbs(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmcrback.SetValue("????")
            self.crm3pbs_failure = True
            self.towhee.set_crnmoa3pbs(mcm)
            return

        if self.crm3pbs_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Concerted Rotation Move over a 3 peptides backbone sequence",
                "Concerted Rotation Move over a 3 peptides backbone sequence Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #         
        # Plane Shift Move
        #
        mcm = self.towhee.get_psm()
        value = self.txtPmplane.GetValue()
        if self.CheckValue(value, "pmplane"):
            mcm.set_move_probability(value)
            self.towhee.set_psm(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmplane.SetValue("????")
            self.psm_failure = True
            self.towhee.set_psm(mcm)
            return

        if self.psm_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Plane Shift Move",
                "Plane Shift Move Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        # 
        # Row Shift Move
        #
        mcm = self.towhee.get_rsm()
        value = self.txtPmrow.GetValue()
        if self.CheckValue(value, "pmrow"):
            mcm.set_move_probability(value)
            self.towhee.set_rsm(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmrow.SetValue("????")
            self.rsm_failure = True
            self.towhee.set_psm(mcm)
            return

        if self.rsm_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Row Shift Move",
                "Row Shift Move Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        # 
        # Intramolecular Single Atom Translation Move
        #
        mcm = self.towhee.get_isatm()
        value = self.txtPmtraat.GetValue()
        if self.CheckValue(value, "pmtraat"):
            mcm.set_move_probability(value)
            self.towhee.set_isatm(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmtraat.SetValue("????")
            self.isatm_failure = True
            self.towhee.set_isatm(mcm)
            return

        if self.isatm_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Intramolecular Single Atom Translation Move",
                "Intramolecular Single Atom Translation Move Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        # 
        # Center-of-Mass Molecule Translation Move
        #
        mcm = self.towhee.get_cofmmtm()
        value = self.txtPmtracm.GetValue()
        if self.CheckValue(value, "pmtracm"):
            mcm.set_move_probability(value)
            self.towhee.set_cofmmtm(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmtraat.SetValue("????")
            self.cmmtm_failure = True
            self.towhee.set_cofmmtm(mcm)
            return

        if self.cmmtm_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Center-of-Mass Molecule Translation Move",
                "Center-of-Mass Molecule Translation Move Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #
        # Rotation about the Center-of-Mass Move
        #
        mcm = self.towhee.get_ratcomm()
        value = self.txtPmrotate.GetValue()
        if self.CheckValue(value, "pmrotate"):
            mcm.set_move_probability(value)
            self.towhee.set_ratcomm(mcm)
        else:
            mcm.set_move_probability("????")
            self.txtPmrotate.SetValue("????")
            self.rcmm_failure = True
            self.towhee.set_ratcomm(mcm)
            return
        
        if self.rcmm_failure:
            d = wx.MessageDialog(self,
                "Error:  I've detected unset variable in the Monte Carlo Move:\n"
                "Rotation about the Center-of-Mass Move",
                "Rotation about the Center-of-Mass Move Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return
        #
        # CBMC Tab
        #
        value = self.cboTor.GetValue()
        if self.CheckValue(value, "tor_cbstyle", True):
            self.towhee.set_tor_cbstyle(int(value))
        else:
           self.cboTor.SetValue("0")
           return

        if self.towhee.get_tor_cbstyle() == 1:
            value = self.txtSdevtor.GetValue()
            if self.CheckValue(value, "sdevtor"):
                self.towhee.set_sdevtor(value)
            else:
               self.txtSdevtor.SetValue("????")
               return

        value = self.cboBend.GetValue()
        if self.CheckValue(value, "bend_cbstyle", True):
            self.towhee.set_bend_cbstyle(int(value))
        else:
           self.cboBend.SetValue("0")
           return

        if self.towhee.get_bend_cbstyle() == 1:
            value = self.txtSdevbena.GetValue()
            if self.CheckValue(value, "sdevbena"):
                self.towhee.set_sdevbena(value)
            else:
               self.txtSdevbena.SetValue("????")
               return

            value = self.txtSdevbenb.GetValue()
            if self.CheckValue(value, "sdevbenb"):
                self.towhee.set_sdevbenb(value)
            else:
               self.txtSdevbenb.SetValue("????")
               return

        value = self.cboVib.GetValue()
        if self.CheckValue(value, "vib_cbstyle", True):
            self.towhee.set_vib_cbstyle(int(value))
        else:
           self.cboVib.SetValue("0")
           return

        if self.towhee.get_vib_cbstyle() == 0:
            v1 = self.txtVibrang1.GetValue()
            v2 = self.txtVibrang2.GetValue()
            
            if self.CheckValue(v1, "vibrang") == False:
               self.txtVibrang1.SetValue("????")
               return

            if self.CheckValue(v2, "vibrang") == False:
               self.txtVibrang2.SetValue("????")
               return
            vibrang = [v1, v2]
            self.towhee.set_vibrang(vibrang)
        elif self.towhee.get_vib_cbstyle() == 1:
            value = self.txtSdevvib.GetValue()
            if self.CheckValue(value, "sdevvib"):
                self.towhee.set_sdevvib(value)
            else:
               self.txtSdevvib.SetValue("????")
               return

        value = self.txtCdform.GetValue()
        if self.CheckValue(value, "cdform", True):
            self.towhee.set_cdform(int(value))
        else:
           self.txtCdform.SetValue("????")
           return

        self.towhee.clear_nch_nb_one()
        self.towhee.clear_nch_nb()
        self.towhee.clear_nch_tor_out()
        self.towhee.clear_nch_tor_in()
        self.towhee.clear_nch_tor_in_con()
        self.towhee.clear_nch_bend_a()
        self.towhee.clear_nch_bend_b()
        self.towhee.clear_nch_vib()
        for i in range(self.towhee.get_nmolty()):
            value = self.txtNch_nb_one[i].GetValue()
            if self.CheckValue(value, "nch_nb_one", True):
                self.towhee.append_nch_nb_one(int(value))
            else:
               self.txtNch_nb_one[i].SetValue("????")
               return

            value = self.txtNch_nb[i].GetValue()
            if self.CheckValue(value, "nch_nb", True):
                self.towhee.append_nch_nb(int(value))
            else:
               self.txtNch_nb[i].SetValue("????")
               return

            value = self.txtNch_tor_out[i].GetValue()
            if self.CheckValue(value, "nch_tor_out", True):
                self.towhee.append_nch_tor_out(int(value))
            else:
               self.txtNch_tor_out[i].SetValue("????")
               return

            value = self.txtNch_tor_in[i].GetValue()
            if self.CheckValue(value, "nch_tor_in", True):
                self.towhee.append_nch_tor_in(int(value))
            else:
               self.txtNch_tor_in[i].SetValue("????")
               return

            value = self.txtNch_tor_in_con[i].GetValue()
            if self.CheckValue(value, "nch_tor_in_con", True):
                self.towhee.append_nch_tor_in_con(int(value))
            else:
               self.txtNch_tor_in_con[i].SetValue("????")
               return

            value = self.txtNch_bend_a[i].GetValue()
            if self.CheckValue(value, "nch_bend_a", True):
                self.towhee.append_nch_bend_a(int(value))
            else:
               self.txtNch_bend_a[i].SetValue("????")
               return

            value = self.txtNch_bend_b[i].GetValue()
            if self.CheckValue(value, "nch_bend_b", True):
                self.towhee.append_nch_bend_b(int(value))
            else:
               self.txtNch_bend_b[i].SetValue("????")
               return

            value = self.txtNch_vib[i].GetValue()
            if self.CheckValue(value, "nch_vib", True):
                self.towhee.append_nch_vib(int(value))
            else:
               self.txtNch_vib[i].SetValue("????")
               return
        #
        # Inputs Tab
        #
        # Sanity check... should *never* see this
        # Famous last words...
        #
        all_in = self.towhee.get_inputs()
        if len(all_in) != self.towhee.get_nmolty():
            d = wx.MessageDialog(self,
                "Something happened that should never happen.  Please contact developer.",
                "Critical Error",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return

        for i in range(self.towhee.get_nmolty()):
            inp = self.towhee.get_single_input(i)
            current_inpstyle = int(self.cboInpstyle[i].GetValue())
            #
            # If inpstyle has changed, let them know
            #
            if inp.get_inpstyle() != current_inpstyle:
                d = wx.MessageDialog(self,
                    "Inpstyle has changed for molecule " + str(i+1) + ".  Please enter new data.",
                    "Error",
                    wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                return
            #
            # If nunit has changed, let them know
            #
            if inp.get_inpstyle() != 4:
                value = self.txtNunit[i].GetValue()
                if self.CheckValue(value, "nunit", True):
                    current_nunit = int(value)
                else:
                    self.txtNunit[i].SetValue("????")
                    return

                value = self.txtNmaxcbmc[i].GetValue()
                if self.CheckValue(value, "nmaxcbmc", True):
                    current_nmaxcbmc = int(value)
                    inp.set_nmaxcbmc(current_nmaxcbmc)
                else:
                    self.txtNmaxcbmc[i].SetValue("????")
                    return

                if inp.get_nunit() != current_nunit:
                    d = wx.MessageDialog(self,
                        "Nunit has changed for molecule " + str(i+1) + ".  Please enter new data.",
                        "Error",
                        wx.ICON_ERROR)
                    d.ShowModal()
                    d.Destroy()
                    return
            #
            # Have to check if there was an input error that wasn't taken care off
            # Fortunately, instead of rechecking every thing, just check the
            # input_error array.  This handles if they didn't enter any data
            # when they increase nmolty because that input_error is set to True
            #
            if self.input_error[i]:
                d = wx.MessageDialog(self,
                    "There is an error in the input data for molecule " + str(i+1) + ".  Please fix the data.",
                    "Error",
                    wx.ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                return

        self.parent.material.towhee_options = copy.deepcopy(self.towhee)
        self.Close(True)
        return

    def CancelAndExit(self, *args):
        self.parent.material.towhee_options = copy.deepcopy(self.old_towhee)
        self.Close(True)
        return

    def CheckValue(self, value, variable, int=False):
        #
        # Check only if it is suppose to be an int
        #
        if int and value.isdigit() == False:
            d = wx.MessageDialog(self,
                "Error:  " + variable + " is suppose to be an integer",
                "Invalid Value",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return False

        if value == "" or value == "????":
            d = wx.MessageDialog(self,
                "Error:  You forgot to set " + variable,
                "Value not set",
                wx.ICON_ERROR)
            d.ShowModal()
            d.Destroy()
            return False
        else:
            return True

# end of class TowheeEditor

#
# Class for the Helix Info Dialog Box
#
class HelixDlgBox(wx.Dialog):
    def __init__(self, parent, ID, title, helixes, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        kwds["size"] = (400,400)
        kwds["title"] = "Enter information about Helix"
        wx.Dialog.__init__(self, parent, ID, **kwds)

        self.swHelixHolder = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        #
        # Work around for bug in wxPython 2.5.2.8
        #
        self.swHelixHolder.SetBackgroundColour(self.swHelixHolder.GetBackgroundColour())
        
        self.helixes = helixes

        self.lblMoltyp = []
        self.txtMoltyp = []
        self.lblRadius = []
        self.txtRadius = []
        self.lblAngle = []
        self.txtAngle = []
        self.lblKeytype = []
        self.cboKeytype = []
        self.lblKeyname = []
        self.txtKeyname = []
        self.lblConlen = []
        self.txtConlen = []
        self.lblPhase = []
        self.txtPhase = []
        for helix in self.helixes:
            self.lblKeyname.append(wx.StaticText(self.swHelixHolder, -1, "helix_keyname"))
            hsize = self.lblKeyname[0].GetSize()
            self.txtKeyname.append(wx.TextCtrl(self.swHelixHolder, -1, helix.get_keyname()))
            self.lblMoltyp.append(wx.StaticText(self.swHelixHolder, -1, "helix_moltyp", style=wx.ALIGN_RIGHT, size=hsize))
            self.txtMoltyp.append(wx.TextCtrl(self.swHelixHolder, -1, str(helix.get_moltyp())))
            self.lblRadius.append(wx.StaticText(self.swHelixHolder, -1, "helix_radius", style=wx.ALIGN_RIGHT, size=hsize))
            self.txtRadius.append(wx.TextCtrl(self.swHelixHolder, -1, helix.get_radius()))
            self.lblAngle.append(wx.StaticText(self.swHelixHolder, -1, "helix_angle", style=wx.ALIGN_RIGHT, size=hsize))
            self.txtAngle.append(wx.TextCtrl(self.swHelixHolder, -1, helix.get_angle()))
            self.lblKeytype.append(wx.StaticText(self.swHelixHolder, -1, "helix_keytype", style=wx.ALIGN_RIGHT, size=hsize))
            self.cboKeytype.append(wx.ComboBox(self.swHelixHolder, -1, choices=["element", "nbname", "pdbname"],\
                style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(100,-1)))
            self.cboKeytype[-1].SetValue(helix.get_keytype())
            self.lblConlen.append(wx.StaticText(self.swHelixHolder, -1, "helix_conlen", style=wx.ALIGN_RIGHT, size=hsize))
            self.txtConlen.append(wx.TextCtrl(self.swHelixHolder, -1, helix.get_conlen()))
            self.lblPhase.append(wx.StaticText(self.swHelixHolder, -1, "helix_phase", style=wx.ALIGN_RIGHT, size=hsize))
            self.txtPhase.append(wx.TextCtrl(self.swHelixHolder, -1, helix.get_phase()))

        self.btnOK = wx.Button(self.swHelixHolder, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self.swHelixHolder, wx.ID_CANCEL, "Cancel")

        self.btnOK.SetDefault()
        self.swHelixHolder.SetScrollRate(50,50)
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrHelixDialog = wx.BoxSizer(wx.VERTICAL)
        szrHelixHolder = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrHelix = []
        szrMoltyp = []
        szrRadius = []
        szrAngle = []
        szrKeytype = []
        szrKeyname = []
        szrConlen = []
        szrPhase = []
        for i in self.helixes:
            szrHelix.append(wx.StaticBoxSizer(wx.StaticBox(self.swHelixHolder, -1,\
                "Mol Type " + str(i.get_nmolty()+1)), wx.VERTICAL))
            szrMoltyp.append(wx.BoxSizer(wx.HORIZONTAL))
            szrRadius.append(wx.BoxSizer(wx.HORIZONTAL))
            szrAngle.append(wx.BoxSizer(wx.HORIZONTAL))
            szrKeytype.append(wx.BoxSizer(wx.HORIZONTAL))
            szrKeyname.append(wx.BoxSizer(wx.HORIZONTAL))
            szrConlen.append(wx.BoxSizer(wx.HORIZONTAL))
            szrPhase.append(wx.BoxSizer(wx.HORIZONTAL))

        for i in range(len(self.helixes)):
            szrMoltyp[i].Add(self.lblMoltyp[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            szrMoltyp[i].Add(self.txtMoltyp[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            
            szrRadius[i].Add(self.lblRadius[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            szrRadius[i].Add(self.txtRadius[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            
            szrAngle[i].Add(self.lblAngle[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            szrAngle[i].Add(self.txtAngle[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            
            szrKeytype[i].Add(self.lblKeytype[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            szrKeytype[i].Add(self.cboKeytype[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            
            szrKeyname[i].Add(self.lblKeyname[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            szrKeyname[i].Add(self.txtKeyname[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            
            szrConlen[i].Add(self.lblConlen[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            szrConlen[i].Add(self.txtConlen[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            
            szrPhase[i].Add(self.lblPhase[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            szrPhase[i].Add(self.txtPhase[i], 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
            
            szrHelix[i].Add(szrMoltyp[i], 0, wx.ALL, 5)
            szrHelix[i].Add(szrRadius[i], 0, wx.ALL, 5)
            szrHelix[i].Add(szrAngle[i], 0, wx.ALL, 5)
            szrHelix[i].Add(szrKeytype[i], 0, wx.ALL, 5)
            szrHelix[i].Add(szrKeyname[i], 0, wx.ALL, 5)
            szrHelix[i].Add(szrConlen[i], 0, wx.ALL, 5)
            szrHelix[i].Add(szrPhase[i], 0, wx.ALL, 5)

            szrHelixDialog.Add(szrHelix[i], 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10)

        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrHelixDialog.Add(szrButtons, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.swHelixHolder.SetAutoLayout(1)
        self.swHelixHolder.SetSizer(szrHelixDialog)
        szrHelixDialog.FitInside(self.swHelixHolder)
        szrHelixDialog.SetVirtualSizeHints(self.swHelixHolder)
        
        szrHelixHolder.Add(self.swHelixHolder, 1, wx.EXPAND|wx.ALL, 5)

        self.SetAutoLayout(1)
        self.SetSizer(szrHelixHolder)
        self.Layout()
        return
# end of class Helix


#
# All the classes for the Dialog boxes that pop up for each Monte Carlo Move
#
class IVM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmvlpr = wx.StaticText(self, -1, "pmvlpr")
        dlgsize = self.lblPmvlpr.GetSize()
        self.txtPmvlpr = []
        for i in mcm.get_pmvlpr():
            self.txtPmvlpr.append(wx.TextCtrl(self, -1, i))

        self.lblRmvol = wx.StaticText(self, -1, "rmvol", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtRmvol = wx.TextCtrl(self, -1, mcm.get_rmvol())

        self.lblTavol = wx.StaticText(self, -1, "tavol", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtTavol = wx.TextCtrl(self, -1, mcm.get_tavol())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Isotropic Volume Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()

    def __do_layout(self):
        szrIVMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrTavol = wx.BoxSizer(wx.HORIZONTAL)
        szrRmvol = wx.BoxSizer(wx.HORIZONTAL)
        szrPmvlpr = wx.BoxSizer(wx.HORIZONTAL)

        szrPmvlpr.Add(self.lblPmvlpr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmvlpr:
            szrPmvlpr.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            
        szrRmvol.Add(self.lblRmvol, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrRmvol.Add(self.txtRmvol, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrTavol.Add(self.lblTavol, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrTavol.Add(self.txtTavol, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrIVMDialog.Add(szrPmvlpr, 1, wx.ALL|wx.EXPAND, 5)
        szrIVMDialog.Add(szrRmvol, 1, wx.ALL|wx.EXPAND, 5)
        szrIVMDialog.Add(szrTavol, 1, wx.ALL|wx.EXPAND, 5)
        szrIVMDialog.Add(szrButtons, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        self.SetAutoLayout(1)
        self.SetSizer(szrIVMDialog)
        szrIVMDialog.Fit(self)
        szrIVMDialog.SetSizeHints(self)
        self.Layout()
# end of class IVM

class AVM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmcellpr = wx.StaticText(self, -1, "pmcellpr")
        dlgsize = self.lblPmcellpr.GetSize()
        self.txtPmcellpr = []
        for i in mcm.get_pmcellpr():
            self.txtPmcellpr.append(wx.TextCtrl(self, -1, i))

        self.txtPmcellpt = []
        if mcm.get_ensemble() == "nvt":
            self.lblPmcellpt = wx.StaticText(self, -1, "pmcellpt", style=wx.ALIGN_RIGHT, size=dlgsize)
            current_pmcellpt_length = len(mcm.get_pmcellpt())
            for i in mcm.get_pmcellpt():
                self.txtPmcellpt.append(wx.TextCtrl(self, -1, i))

        self.lblRmcell = wx.StaticText(self, -1, "rmcell", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtRmcell = wx.TextCtrl(self, -1, mcm.get_rmcell())
        self.lblTacell = wx.StaticText(self, -1, "tacell", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtTacell = wx.TextCtrl(self, -1, mcm.get_tacell())
        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Anisotropic Volume Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrAVMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrTacell = wx.BoxSizer(wx.HORIZONTAL)
        szrRmcell = wx.BoxSizer(wx.HORIZONTAL)
        szrPmcellpr = wx.BoxSizer(wx.HORIZONTAL)

        szrPmcellpr.Add(self.lblPmcellpr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmcellpr:
            szrPmcellpr.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        if self.txtPmcellpt:
            szrPmcellpt = wx.BoxSizer(wx.HORIZONTAL)
            szrPmcellpt.Add(self.lblPmcellpt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            for i in self.txtPmcellpt:
                szrPmcellpt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            
        szrRmcell.Add(self.lblRmcell, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrRmcell.Add(self.txtRmcell, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrTacell.Add(self.lblTacell, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrTacell.Add(self.txtTacell, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrAVMDialog.Add(szrPmcellpr, 1, wx.ALL|wx.EXPAND, 5)
        if self.txtPmcellpt:
            szrAVMDialog.Add(szrPmcellpt, 1, wx.ALL|wx.EXPAND, 5)
        szrAVMDialog.Add(szrRmcell, 1, wx.ALL|wx.EXPAND, 5)
        szrAVMDialog.Add(szrTacell, 1, wx.ALL|wx.EXPAND, 5)
        szrAVMDialog.Add(szrButtons, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetAutoLayout(1)
        self.SetSizer(szrAVMDialog)
        szrAVMDialog.Fit(self)
        szrAVMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class AVM

class RB2BMTM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPm2rbswmt = wx.StaticText(self, -1, "pm2rbswmt")
        dlgsize = self.lblPm2rbswmt.GetSize()
        self.txtPm2rbswmt = []
        for i in mcm.get_pm2rbswmt():
            self.txtPm2rbswmt.append(wx.TextCtrl(self, -1, i))

        self.lblPm2rbswpr = wx.StaticText(self, -1, "pm2rbswpr", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPm2rbswpr = []
        for i in mcm.get_pm2rbswpr():
            self.txtPm2rbswpr.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Rotational-bias 2 Box Molecule Transfer Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrRB2BMTMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPm2rbswmt = wx.BoxSizer(wx.HORIZONTAL)
        szrPm2rbswpr = wx.BoxSizer(wx.HORIZONTAL)

        szrPm2rbswmt.Add(self.lblPm2rbswmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPm2rbswmt:
            szrPm2rbswmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrPm2rbswpr.Add(self.lblPm2rbswpr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPm2rbswpr:
            szrPm2rbswpr.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrRB2BMTMDialog.Add(szrPm2rbswmt, 1, wx.ALL|wx.EXPAND, 5)
        szrRB2BMTMDialog.Add(szrPm2rbswpr, 1, wx.ALL|wx.EXPAND, 5)
        szrRB2BMTMDialog.Add(szrButtons, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetAutoLayout(1)
        self.SetSizer(szrRB2BMTMDialog)
        szrRB2BMTMDialog.Fit(self)
        szrRB2BMTMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class RM2BMTM

class CB2BMTM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPm2cbswmt = wx.StaticText(self, -1, "pm2cbswmt")
        dlgsize = self.lblPm2cbswmt.GetSize()
        self.txtPm2cbswmt = []
        for i in mcm.get_pm2cbswmt():
            self.txtPm2cbswmt.append(wx.TextCtrl(self, -1, i))

        self.lblPm2cbswpr = wx.StaticText(self, -1, "pm2cbswpr", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPm2cbswpr = []
        for i in mcm.get_pm2cbswpr():
            self.txtPm2cbswpr.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Configurational-bias 2 Box Molecule Transfer Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrCB2BMTMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPm2cbswmt = wx.BoxSizer(wx.HORIZONTAL)
        szrPm2cbswpr = wx.BoxSizer(wx.HORIZONTAL)

        szrPm2cbswmt.Add(self.lblPm2cbswmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPm2cbswmt:
            szrPm2cbswmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrPm2cbswpr.Add(self.lblPm2cbswpr, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPm2cbswpr:
            szrPm2cbswpr.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrCB2BMTMDialog.Add(szrPm2cbswmt, 1, wx.ALL|wx.EXPAND, 5)
        szrCB2BMTMDialog.Add(szrPm2cbswpr, 1, wx.ALL|wx.EXPAND, 5)
        szrCB2BMTMDialog.Add(szrButtons, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetAutoLayout(1)
        self.SetSizer(szrCB2BMTMDialog)
        szrCB2BMTMDialog.Fit(self)
        szrCB2BMTMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class CM2BMTM

class CBSBMRM(wx.Dialog):
    def __init__(self, parent, ID, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID,\
        "Configurational-bias 2 Box Molecule Transfer Move",\
        **kwds)

        self.lblPm1cbswmt = wx.StaticText(self, -1, "pm1cbswmt")
        self.txtPm1cbswmt = []
        for i in mcm.get_pm1cbswmt():
            self.txtPm1cbswmt.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrCBSBMRMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPm1cbswmt = wx.BoxSizer(wx.HORIZONTAL)

        szrPm1cbswmt.Add(self.lblPm1cbswmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPm1cbswmt:
            szrPm1cbswmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrCBSBMRMDialog.Add(szrPm1cbswmt, 1, wx.ALL|wx.EXPAND, 5)
        szrCBSBMRMDialog.Add(szrButtons, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetAutoLayout(1)
        self.SetSizer(szrCBSBMRMDialog)
        szrCBSBMRMDialog.Fit(self)
        szrCBSBMRMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class CM2BMTM

class GCID(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmuvtcbmt = wx.StaticText(self, -1, "pmuvtcbmt")
        self.txtPmuvtcbmt = []
        for i in mcm.get_pmuvtcbmt():
            self.txtPmuvtcbmt.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Configurational Bias Grand Canonical Insertion/Deletion Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrGCIDDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmuvtcbmt = wx.BoxSizer(wx.HORIZONTAL)

        szrPmuvtcbmt.Add(self.lblPmuvtcbmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmuvtcbmt:
            szrPmuvtcbmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrGCIDDialog.Add(szrPmuvtcbmt, 1, wx.ALL|wx.EXPAND, 5)
        szrGCIDDialog.Add(szrButtons, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrGCIDDialog)
        szrGCIDDialog.Fit(self)
        szrGCIDDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class GCID

class AVBMT1(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmavb1mt = wx.StaticText(self, -1, "pmavb1mt")
        dlgsize = self.lblPmavb1mt.GetSize()
        self.txtPmavb1mt = []
        for i in mcm.get_pmavb1mt():
            self.txtPmavb1mt.append(wx.TextCtrl(self, -1, i))

        self.lblPmavb1in = wx.StaticText(self, -1, "pmavb1in", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPmavb1in = wx.TextCtrl(self, -1, mcm.get_pmavb1in())

        self.lblPmavb1ct = wx.StaticText(self, -1, "pmavb1ct", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPmavb1ct = []
        for i in mcm.get_pmavb1ct():
            for k in i:
                self.txtPmavb1ct.append(wx.TextCtrl(self, -1, k))

        self.lblAvb1rad = wx.StaticText(self, -1, "avb1rad", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtAvb1rad = wx.TextCtrl(self, -1, mcm.get_avb1rad())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Aggregation Volume Bias Move Type 1")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrAVBMT1Dialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb1in = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb1mt = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb1ct = wx.BoxSizer(wx.HORIZONTAL)
        szrAvb1rad = wx.BoxSizer(wx.HORIZONTAL)
        grdPmavb1ct = wx.GridSizer(len(self.txtPmavb1mt), len(self.txtPmavb1mt), 0, 0)

        szrPmavb1in.Add(self.lblPmavb1in, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrPmavb1in.Add(self.txtPmavb1in, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrPmavb1mt.Add(self.lblPmavb1mt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmavb1mt:
            szrPmavb1mt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrPmavb1ct.Add(self.lblPmavb1ct, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmavb1ct:
            grdPmavb1ct.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrPmavb1ct.Add(grdPmavb1ct, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)

        szrAvb1rad.Add(self.lblAvb1rad, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrAvb1rad.Add(self.txtAvb1rad, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrAVBMT1Dialog.Add(szrPmavb1in, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT1Dialog.Add(szrPmavb1mt, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT1Dialog.Add(szrPmavb1ct, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT1Dialog.Add(szrAvb1rad, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT1Dialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrAVBMT1Dialog)
        szrAVBMT1Dialog.Fit(self)
        szrAVBMT1Dialog.SetSizeHints(self)
        self.Layout()
        return
# end of class AVBMT1


class AVBMT2(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmavb2mt = wx.StaticText(self, -1, "pmavb2mt")
        dlgsize = self.lblPmavb2mt.GetSize()
        self.txtPmavb2mt = []
        for i in mcm.get_pmavb2mt():
            self.txtPmavb2mt.append(wx.TextCtrl(self, -1, i))

        self.lblPmavb2in = wx.StaticText(self, -1, "pmavb2in", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPmavb2in = wx.TextCtrl(self, -1, mcm.get_pmavb2in())

        self.lblPmavb2ct = wx.StaticText(self, -1, "pmavb2ct", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPmavb2ct = []
        for i in mcm.get_pmavb2ct():
            for k in i:
                self.txtPmavb2ct.append(wx.TextCtrl(self, -1, k))

        self.lblAvb2rad = wx.StaticText(self, -1, "avb2rad", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtAvb2rad = wx.TextCtrl(self, -1, mcm.get_avb2rad())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Aggregation Volume Bias Move Type 2")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrAVBMT2Dialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb2in = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb2mt = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb2ct = wx.BoxSizer(wx.HORIZONTAL)
        szrAvb2rad = wx.BoxSizer(wx.HORIZONTAL)
        grdPmavb2ct = wx.GridSizer(len(self.txtPmavb2mt), len(self.txtPmavb2mt), 0, 0)

        szrPmavb2in.Add(self.lblPmavb2in, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrPmavb2in.Add(self.txtPmavb2in, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrPmavb2mt.Add(self.lblPmavb2mt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmavb2mt:
            szrPmavb2mt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrPmavb2ct.Add(self.lblPmavb2ct, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmavb2ct:
            grdPmavb2ct.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrPmavb2ct.Add(grdPmavb2ct, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)

        szrAvb2rad.Add(self.lblAvb2rad, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrAvb2rad.Add(self.txtAvb2rad, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrAVBMT2Dialog.Add(szrPmavb2in, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT2Dialog.Add(szrPmavb2mt, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT2Dialog.Add(szrPmavb2ct, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT2Dialog.Add(szrAvb2rad, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT2Dialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrAVBMT2Dialog)
        szrAVBMT2Dialog.Fit(self)
        szrAVBMT2Dialog.SetSizeHints(self)
        self.Layout()
        return
# end of class AVBMT2


class AVBMT3(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmavb3mt = wx.StaticText(self, -1, "pmavb3mt")
        dlgsize = self.lblPmavb3mt.GetSize()
        self.txtPmavb3mt = []
        for i in mcm.get_pmavb3mt():
            self.txtPmavb3mt.append(wx.TextCtrl(self, -1, i))

        self.lblPmavb3ct = wx.StaticText(self, -1, "pmavb3ct", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPmavb3ct = []
        for i in mcm.get_pmavb3ct():
            for k in i:
                self.txtPmavb3ct.append(wx.TextCtrl(self, -1, k))

        self.lblAvb3rad = wx.StaticText(self, -1, "avb3rad", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtAvb3rad = wx.TextCtrl(self, -1, mcm.get_avb3rad())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Aggregation Volume Bias Move Type 3")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrAVBMT3Dialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb3in = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb3mt = wx.BoxSizer(wx.HORIZONTAL)
        szrPmavb3ct = wx.BoxSizer(wx.HORIZONTAL)
        szrAvb3rad = wx.BoxSizer(wx.HORIZONTAL)
        grdPmavb3ct = wx.GridSizer(len(self.txtPmavb3mt), len(self.txtPmavb3mt), 0, 0)

        szrPmavb3mt.Add(self.lblPmavb3mt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmavb3mt:
            szrPmavb3mt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrPmavb3ct.Add(self.lblPmavb3ct, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmavb3ct:
            grdPmavb3ct.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrPmavb3ct.Add(grdPmavb3ct, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        szrAvb3rad.Add(self.lblAvb3rad, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrAvb3rad.Add(self.txtAvb3rad, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrAVBMT3Dialog.Add(szrPmavb3mt, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT3Dialog.Add(szrPmavb3ct, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT3Dialog.Add(szrAvb3rad, 0, wx.ALL|wx.EXPAND, 5)
        szrAVBMT3Dialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetAutoLayout(1)
        self.SetSizer(szrAVBMT3Dialog)
        szrAVBMT3Dialog.Fit(self)
        szrAVBMT3Dialog.SetSizeHints(self)
        self.Layout()
        return
# end of class AVBMT3


class CBPMR(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmcbmt = wx.StaticText(self, -1, "pmcbmt")
        dlgsize = self.lblPmcbmt.GetSize()
        self.txtPmcbmt = []
        for i in mcm.get_pmcbmt():
            self.txtPmcbmt.append(wx.TextCtrl(self, -1, i))

        self.lblPmall = wx.StaticText(self, -1, "pmall", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPmall = []
        for i in mcm.get_pmall():
            self.txtPmall.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Configurational-Bias Partial Molecule Regrowth")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrCBPMRDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmcbmt = wx.BoxSizer(wx.HORIZONTAL)
        szrPmall = wx.BoxSizer(wx.HORIZONTAL)

        szrPmcbmt.Add(self.lblPmcbmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmcbmt:
            szrPmcbmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrPmall.Add(self.lblPmall, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmall:
            szrPmall.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrCBPMRDialog.Add(szrPmcbmt, 0, wx.ALL|wx.EXPAND, 5)
        szrCBPMRDialog.Add(szrPmall, 0, wx.ALL|wx.EXPAND, 5)
        szrCBPMRDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrCBPMRDialog)
        szrCBPMRDialog.Fit(self)
        szrCBPMRDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class CBPMR

class CBPBR(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmbkmt = wx.StaticText(self, -1, "pmbkmt")
        self.txtPmbkmt = []
        for i in mcm.get_pmbkmt():
            self.txtPmbkmt.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Configurational-Bias Protein Backbone Regrowth")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrCBPBRDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmbkmt = wx.BoxSizer(wx.HORIZONTAL)

        szrPmbkmt.Add(self.lblPmbkmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmbkmt:
            szrPmbkmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrCBPBRDialog.Add(szrPmbkmt, 0, wx.ALL|wx.EXPAND, 5)
        szrCBPBRDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrCBPBRDialog)
        szrCBPBRDialog.Fit(self)
        szrCBPBRDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class CBPMR


class TPM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmpivmt = wx.StaticText(self, -1, "pmpivmt")
        self.txtPmpivmt = []
        for i in mcm.get_pmpivmt():
            self.txtPmpivmt.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Torsional Pivot Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrTPMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmpivmt = wx.BoxSizer(wx.HORIZONTAL)

        szrPmpivmt.Add(self.lblPmpivmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmpivmt:
            szrPmpivmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrTPMDialog.Add(szrPmpivmt, 0, wx.ALL|wx.EXPAND, 5)
        szrTPMDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrTPMDialog)
        szrTPMDialog.Fit(self)
        szrTPMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class TPM


class CRMNPB(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmcrmt = wx.StaticText(self, -1, "pmcrmt")
        self.txtPmcrmt = []
        for i in mcm.get_pmcrmt():
            self.txtPmcrmt.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Concerted Rotation Move on a Non-Peptide Backbone")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrCRMNPBDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmcrmt = wx.BoxSizer(wx.HORIZONTAL)

        szrPmcrmt.Add(self.lblPmcrmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmcrmt:
            szrPmcrmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrCRMNPBDialog.Add(szrPmcrmt, 0, wx.ALL|wx.EXPAND, 5)
        szrCRMNPBDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrCRMNPBDialog)
        szrCRMNPBDialog.Fit(self)
        szrCRMNPBDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class CRMNPB


class CRM3PBS(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmcrbmt = wx.StaticText(self, -1, "pmcrbmt")
        self.txtPmcrbmt = []
        for i in mcm.get_pmcrbmt():
            self.txtPmcrbmt.append(wx.TextCtrl(self, -1, i))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Concerted Rotation Move over a 3 Peptides Backbone Sequence")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrCRM3PBSDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmcrbmt = wx.BoxSizer(wx.HORIZONTAL)

        szrPmcrbmt.Add(self.lblPmcrbmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmcrbmt:
            szrPmcrbmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
 
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrCRM3PBSDialog.Add(szrPmcrbmt, 0, wx.ALL|wx.EXPAND, 5)
        szrCRM3PBSDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrCRM3PBSDialog)
        szrCRM3PBSDialog.Fit(self)
        szrCRM3PBSDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class CRM3PBS


class PSM(wx.Dialog):
    def __init__(self, parent, ID, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, "Plane Shift Move", **kwds)

        self.lblPmplanebox = wx.StaticText(self, -1, "pmplanebox")
        dlgsize = self.lblPmplanebox.GetSize()
        self.txtPmplanebox = []
        for i in mcm.get_pmplanebox():
            self.txtPmplanebox.append(wx.TextCtrl(self, -1, i))

        self.lblPlanewidth = wx.StaticText(self, -1, "planewidth", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtPlanewidth = wx.TextCtrl(self, -1, mcm.get_planewidth())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrPSMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmplanebox = wx.BoxSizer(wx.HORIZONTAL)
        szrPlanewidth = wx.BoxSizer(wx.HORIZONTAL)

        szrPmplanebox.Add(self.lblPmplanebox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmplanebox:
            szrPmplanebox.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrPlanewidth.Add(self.lblPlanewidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrPlanewidth.Add(self.txtPlanewidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
  
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrPSMDialog.Add(szrPmplanebox, 0, wx.ALL|wx.EXPAND, 5)
        szrPSMDialog.Add(szrPlanewidth, 0, wx.ALL|wx.EXPAND, 5)
        szrPSMDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrPSMDialog)
        szrPSMDialog.Fit(self)
        szrPSMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class PSM


class RSM(wx.Dialog):
    def __init__(self, parent, ID, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, "Row Shift Move", **kwds)

        self.lblPmrowbox = wx.StaticText(self, -1, "pmrowbox")
        dlgsize = self.lblPmrowbox.GetSize()
        self.txtPmrowbox = []
        for i in mcm.get_pmrowbox():
            self.txtPmrowbox.append(wx.TextCtrl(self, -1, i))

        self.lblRowwidth = wx.StaticText(self, -1, "rowwidth", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtRowwidth = wx.TextCtrl(self, -1, mcm.get_rowwidth())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrRSMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmrowbox = wx.BoxSizer(wx.HORIZONTAL)
        szrRowwidth = wx.BoxSizer(wx.HORIZONTAL)

        szrPmrowbox.Add(self.lblPmrowbox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmrowbox:
            szrPmrowbox.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrRowwidth.Add(self.lblRowwidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrRowwidth.Add(self.txtRowwidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
  
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrRSMDialog.Add(szrPmrowbox, 0, wx.ALL|wx.EXPAND, 5)
        szrRSMDialog.Add(szrRowwidth, 0, wx.ALL|wx.EXPAND, 5)
        szrRSMDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrRSMDialog)
        szrRSMDialog.Fit(self)
        szrRSMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class RSM


class ISATM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmtamt = wx.StaticText(self, -1, "pmtamt")
        dlgsize = self.lblPmtamt.GetSize()
        self.txtPmtamt = []
        for i in mcm.get_pmtamt():
            self.txtPmtamt.append(wx.TextCtrl(self, -1, i))

        self.lblRmtraa = wx.StaticText(self, -1, "rmtraa", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtRmtraa = wx.TextCtrl(self, -1, mcm.get_rmtraa())
        self.lblTatraa = wx.StaticText(self, -1, "tatraa", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtTatraa = wx.TextCtrl(self, -1, mcm.get_tatraa())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Intramolecular Single Atom Translation Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrISATMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmtamt = wx.BoxSizer(wx.HORIZONTAL)
        szrRmtraa = wx.BoxSizer(wx.HORIZONTAL)
        szrTatraa = wx.BoxSizer(wx.HORIZONTAL)

        szrPmtamt.Add(self.lblPmtamt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmtamt:
            szrPmtamt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrRmtraa.Add(self.lblRmtraa, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrRmtraa.Add(self.txtRmtraa, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrTatraa.Add(self.lblTatraa, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrTatraa.Add(self.txtTatraa, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrISATMDialog.Add(szrPmtamt, 0, wx.ALL|wx.EXPAND, 5)
        szrISATMDialog.Add(szrRmtraa, 0, wx.ALL|wx.EXPAND, 5)
        szrISATMDialog.Add(szrTatraa, 0, wx.ALL|wx.EXPAND, 5)
        szrISATMDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrISATMDialog)
        szrISATMDialog.Fit(self)
        szrISATMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class ISATM


class CMMTM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmtcmt = wx.StaticText(self, -1, "pmtcmt")
        dlgsize = self.lblPmtcmt.GetSize()
        self.txtPmtcmt = []
        for i in mcm.get_pmtcmt():
            self.txtPmtcmt.append(wx.TextCtrl(self, -1, i))

        self.lblRmtrac = wx.StaticText(self, -1, "rmtrac", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtRmtrac = wx.TextCtrl(self, -1, mcm.get_rmtrac())
        self.lblTatrac = wx.StaticText(self, -1, "tatrac", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtTatrac = wx.TextCtrl(self, -1, mcm.get_tatrac())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Center-of-Mass Molecule Translation Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrCMMTMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmtcmt = wx.BoxSizer(wx.HORIZONTAL)
        szrRmtrac = wx.BoxSizer(wx.HORIZONTAL)
        szrTatrac = wx.BoxSizer(wx.HORIZONTAL)

        szrPmtcmt.Add(self.lblPmtcmt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmtcmt:
            szrPmtcmt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrRmtrac.Add(self.lblRmtrac, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrRmtrac.Add(self.txtRmtrac, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrTatrac.Add(self.lblTatrac, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrTatrac.Add(self.txtTatrac, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrCMMTMDialog.Add(szrPmtcmt, 0, wx.ALL|wx.EXPAND, 5)
        szrCMMTMDialog.Add(szrRmtrac, 0, wx.ALL|wx.EXPAND, 5)
        szrCMMTMDialog.Add(szrTatrac, 0, wx.ALL|wx.EXPAND, 5)
        szrCMMTMDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrCMMTMDialog)
        szrCMMTMDialog.Fit(self)
        szrCMMTMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class CMMTM

class RCMM(wx.Dialog):
    def __init__(self, parent, ID, title, mcm, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblPmromt = wx.StaticText(self, -1, "pmromt")
        dlgsize = self.lblPmromt.GetSize()
        self.txtPmromt = []
        for i in mcm.get_pmromt():
            self.txtPmromt.append(wx.TextCtrl(self, -1, i))

        self.lblRmrot = wx.StaticText(self, -1, "rmrot", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtRmrot = wx.TextCtrl(self, -1, mcm.get_rmrot())
        self.lblTarot = wx.StaticText(self, -1, "tarot", style=wx.ALIGN_RIGHT, size=dlgsize)
        self.txtTarot = wx.TextCtrl(self, -1, mcm.get_tarot())

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Rotation about the Center-of-Mass Move")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrRCMMDialog = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrPmromt = wx.BoxSizer(wx.HORIZONTAL)
        szrRmrot = wx.BoxSizer(wx.HORIZONTAL)
        szrTarot = wx.BoxSizer(wx.HORIZONTAL)

        szrPmromt.Add(self.lblPmromt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        for i in self.txtPmromt:
            szrPmromt.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrRmrot.Add(self.lblRmrot, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrRmrot.Add(self.txtRmrot, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrTarot.Add(self.lblTarot, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrTarot.Add(self.txtTarot, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        szrRCMMDialog.Add(szrPmromt, 0, wx.ALL|wx.EXPAND, 5)
        szrRCMMDialog.Add(szrRmrot, 0, wx.ALL|wx.EXPAND, 5)
        szrRCMMDialog.Add(szrTarot, 0, wx.ALL|wx.EXPAND, 5)
        szrRCMMDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetAutoLayout(1)
        self.SetSizer(szrRCMMDialog)
        szrRCMMDialog.Fit(self)
        szrRCMMDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class RCMM
#
# All the classes for the each input style
#
class Nanotube(wx.Dialog):
    def __init__(self, parent, ID, title, input, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.lblNanotube_bondlength = wx.StaticText(self, -1, "nanotube_bondlength", style=wx.ALIGN_RIGHT)
        nlength = self.lblNanotube_bondlength.GetSize()
        self.txtNanotube_bondlength = wx.TextCtrl(self, -1, input.get_bondlength())
        self.lblForcefield = wx.StaticText(self, -1, "forcefield", style=wx.ALIGN_RIGHT, size=nlength)
        self.txtForcefield = wx.TextCtrl(self, -1, input.get_forcefield())
        self.lblAtomname = wx.StaticText(self, -1, "atomname", style=wx.ALIGN_RIGHT, size=nlength)
        self.txtAtomname = wx.TextCtrl(self, -1, input.get_atomname())
        self.lblQqatom = wx.StaticText(self, -1, "qqatom", style=wx.ALIGN_RIGHT, size=nlength)
        self.txtQqatom = wx.TextCtrl(self, -1, input.get_qqatom())
        self.lblNanotube_n = wx.StaticText(self, -1, "nanotube_n", style=wx.ALIGN_RIGHT, size=nlength)
        self.txtNanotube_n = wx.TextCtrl(self, -1, str(input.get_n()))
        self.lblNanotube_m = wx.StaticText(self, -1, "nanotube_m", style=wx.ALIGN_RIGHT, size=nlength)
        self.txtNanotube_m = wx.TextCtrl(self, -1, str(input.get_m()))
        self.lblNanotube_ncells = wx.StaticText(self, -1, "nanotube_ncells", style=wx.ALIGN_RIGHT, size=nlength)
        self.txtNanotube_ncells = wx.TextCtrl(self, -1, str(input.get_ncells()))

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Input Style 4")
        self.btnOK.SetDefault()
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrNanotubeDialog = wx.BoxSizer(wx.VERTICAL)
        szrForcefield = wx.BoxSizer(wx.HORIZONTAL)
        szrAtomname = wx.BoxSizer(wx.HORIZONTAL)
        szrQqatom = wx.BoxSizer(wx.HORIZONTAL)
        szrNanotube_n = wx.BoxSizer(wx.HORIZONTAL)
        szrNanotube_m = wx.BoxSizer(wx.HORIZONTAL)
        szrNanotube_ncells = wx.BoxSizer(wx.HORIZONTAL)
        szrNanotube_bondlength = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)

        szrForcefield.Add(self.lblForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrForcefield.Add(self.txtForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrAtomname.Add(self.lblAtomname, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrAtomname.Add(self.txtAtomname, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrQqatom.Add(self.lblQqatom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrQqatom.Add(self.txtQqatom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_n.Add(self.lblNanotube_n, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_n.Add(self.txtNanotube_n, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_m.Add(self.lblNanotube_m, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_m.Add(self.txtNanotube_m, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_ncells.Add(self.lblNanotube_ncells, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_ncells.Add(self.txtNanotube_ncells, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_bondlength.Add(self.lblNanotube_bondlength, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotube_bondlength.Add(self.txtNanotube_bondlength, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNanotubeDialog.Add(szrForcefield, 0, wx.ALL|wx.EXPAND, 2)
        szrNanotubeDialog.Add(szrAtomname, 0, wx.ALL|wx.EXPAND, 2)
        szrNanotubeDialog.Add(szrQqatom, 0, wx.ALL|wx.EXPAND, 2)
        szrNanotubeDialog.Add(szrNanotube_n, 0, wx.ALL|wx.EXPAND, 2)
        szrNanotubeDialog.Add(szrNanotube_m, 0, wx.ALL|wx.EXPAND, 2)
        szrNanotubeDialog.Add(szrNanotube_ncells, 0, wx.ALL|wx.EXPAND, 2)
        szrNanotubeDialog.Add(szrNanotube_bondlength, 0, wx.ALL|wx.EXPAND, 2)
        szrNanotubeDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.SetAutoLayout(1)
        self.SetSizer(szrNanotubeDialog)
        szrNanotubeDialog.Fit(self)
        szrNanotubeDialog.SetSizeHints(self)
        self.Layout()
        return
# end of class Nanotube


class NucleicAcid(wx.Dialog):
    def __init__(self, parent, ID, title, input, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        kwds["size"] = (320,400)
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.swNucleicAcid = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        #
        # Work around for bug in wxPython 2.5.2.8
        #
        self.swNucleicAcid.SetBackgroundColour(self.swNucleicAcid.GetBackgroundColour())

        self.lblMonomername = wx.StaticText(self.swNucleicAcid, -1, "monomername", style=wx.ALIGN_RIGHT)
        nasize = self.lblMonomername.GetSize()
        self.lblTerminus = wx.StaticText(self.swNucleicAcid, -1, "terminus", style=wx.ALIGN_RIGHT, size=nasize)
        self.txtTerminus = wx.TextCtrl(self.swNucleicAcid, -1, str(input.get_terminus()), size=(50,-1))
        self.lblForcefield = wx.StaticText(self.swNucleicAcid, -1, "forcefield", style=wx.ALIGN_RIGHT, size=nasize)
        self.txtForcefield = wx.TextCtrl(self.swNucleicAcid, -1, str(input.get_forcefield()), size=(250,-1))
        self.txtMonomername = []
        for i in input.get_monomername():
            self.txtMonomername.append(wx.TextCtrl(self.swNucleicAcid, -1, i, size=(50,-1)))
        for i in range(len(input.get_monomername()), input.get_nunit()):
            self.txtMonomername.append(wx.TextCtrl(self.swNucleicAcid, -1, "", size=(50,-1)))

        self.btnOK = wx.Button(self.swNucleicAcid, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self.swNucleicAcid, wx.ID_CANCEL, "Cancel")

        self.SetTitle("Input Style 3")
        self.btnOK.SetDefault()
        self.swNucleicAcid.SetScrollRate(50, 50)
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        szrNucleicAcidDialog = wx.BoxSizer(wx.VERTICAL)
        szrForcefield = wx.BoxSizer(wx.HORIZONTAL)
        szrTerminus = wx.BoxSizer(wx.HORIZONTAL)
        szrMonomername = wx.BoxSizer(wx.HORIZONTAL)
        szrMonomernameList = wx.BoxSizer(wx.VERTICAL)
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)

        szrTerminus.Add(self.lblTerminus, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrTerminus.Add(self.txtTerminus, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrForcefield.Add(self.lblForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrForcefield.Add(self.txtForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrMonomername.Add(self.lblMonomername, 0, wx.ALL|wx.ALIGN_TOP, 2)
        for i in self.txtMonomername:
            szrMonomernameList.Add(i, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrMonomername.Add(szrMonomernameList, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
        szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        szrNucleicAcidDialog.Add(szrTerminus, 0, wx.ALL|wx.EXPAND, 2)
        szrNucleicAcidDialog.Add(szrForcefield, 0, wx.ALL|wx.EXPAND, 2)
        szrNucleicAcidDialog.Add(szrMonomername, 0, wx.ALL|wx.EXPAND, 2)
        szrNucleicAcidDialog.Add(szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 2)

        self.swNucleicAcid.SetAutoLayout(1)
        self.swNucleicAcid.SetSizer(szrNucleicAcidDialog)
        szrNucleicAcidDialog.FitInside(self.swNucleicAcid)
        szrNucleicAcidDialog.SetVirtualSizeHints(self.swNucleicAcid)
        return
# end of class NucleicAcid


class ConnectivityMap(wx.Dialog):
    def __init__(self, parent, ID, title, input, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        kwds["size"] = (400,600)
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.nunit = input.get_nunit()
        self.vibs = input.get_vibrations()
        self.imptors = input.get_improper_torsions()

        self.swCMHolder = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        #
        # Work around for bug in wxPython 2.5.2.8
        #
        self.swCMHolder.SetBackgroundColour(self.swCMHolder.GetBackgroundColour())

        self.lblCharge_assignment = wx.StaticText(self.swCMHolder, -1, "charge_assignment", style=wx.ALIGN_RIGHT, size=(150,-1))
        cmsize = self.lblCharge_assignment.GetSize()
        self.cboCharge_assignment = self.cboEnsemble = wx.ComboBox(self.swCMHolder, -1,\
            choices=["bond increment", "manual", "none"],\
            style=wx.CB_DROPDOWN|wx.CB_READONLY, size=(150,-1))
        self.cboCharge_assignment.SetValue(input.get_charge_assignment())
        wx.EVT_COMBOBOX(self, self.cboCharge_assignment.GetId(), self.ChargeAssignmentChanged)
        
        self.lblForcefield = wx.StaticText(self.swCMHolder, -1, "forcefield", style=wx.ALIGN_RIGHT, size=cmsize)
        self.txtForcefield = wx.TextCtrl(self.swCMHolder, -1, input.get_forcefield(), size=(150,-1))

        self.lblUnit = []
        self.txtUnit = []
        self.lblType = []
        self.txtType = []
        self.lblQqatom = []
        self.txtQqatom = []
        self.lblInvib = []
        self.txtInvib = []
        self.txtIjvib = []
        self.InvibIDs = []
        self.lblInimprop = []
        self.txtInimprop = []
        self.txtIjimprop2 = []
        self.txtIjimprop3 = []
        self.txtIjimprop4 = []
        self.txtItimprop = []
        self.InimpropIDs = []
        for i in input.get_unit():
            self.lblUnit.append(wx.StaticText(self.swCMHolder, -1, "Unit", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtUnit.append(wx.TextCtrl(self.swCMHolder, -1, str(i), size=(50,-1)))
        for i in range(len(input.get_unit()), input.get_nunit()):
            self.lblUnit.append(wx.StaticText(self.swCMHolder, -1, "Unit", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtUnit.append(wx.TextCtrl(self.swCMHolder, -1, str(i), size=(50,-1)))

        for i in input.get_type():
            self.lblType.append(wx.StaticText(self.swCMHolder, -1, "Type", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtType.append(wx.TextCtrl(self.swCMHolder, -1, i, size=(75,-1)))
        for i in range(len(input.get_type()), input.get_nunit()):
            self.lblType.append(wx.StaticText(self.swCMHolder, -1, "Type", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtType.append(wx.TextCtrl(self.swCMHolder, -1, "", size=(75,-1)))

        for i in input.get_qqatom():
            self.lblQqatom.append(wx.StaticText(self.swCMHolder, -1, "qqatom", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtQqatom.append(wx.TextCtrl(self.swCMHolder, -1, i, size=(75,-1)))
        for i in range(len(input.get_qqatom()), input.get_nunit()):
            self.lblQqatom.append(wx.StaticText(self.swCMHolder, -1, "qqatom", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtQqatom.append(wx.TextCtrl(self.swCMHolder, -1, "", size=(75,-1)))
        #
        # Vibrations
        #
        for vib in input.get_vibrations():
            self.lblInvib.append(wx.StaticText(self.swCMHolder, -1, "invib", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtInvib.append(wx.TextCtrl(self.swCMHolder, -1, str(vib.get_number_vibrations()), size=(75,-1)))
            self.InvibIDs.append(self.txtInvib[-1].GetId())
            wx.EVT_TEXT(self, self.txtInvib[-1].GetId(), self.InvibChanged)
            tempIjvib = []
            for vibes in vib.get_vibrations():
                tempIjvib.append(wx.TextCtrl(self.swCMHolder, -1, str(vibes)))
            self.txtIjvib.append(tempIjvib)
        for i in range(len(input.get_vibrations()), input.get_nunit()):
            new_vib = input.create_vibrations()
            self.vibs.append(new_vib)
            self.lblInvib.append(wx.StaticText(self.swCMHolder, -1, "invib", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtInvib.append(wx.TextCtrl(self.swCMHolder, -1, "0", size=(75,-1)))
            self.InvibIDs.append(self.txtInvib[-1].GetId())
            wx.EVT_TEXT(self, self.txtInvib[-1].GetId(), self.InvibChanged)
            tempIjvib = []
            self.txtIjvib.append(tempIjvib)
        #
        # Improper Torsions
        #
        for imptor in input.get_improper_torsions():
            self.lblInimprop.append(wx.StaticText(self.swCMHolder, -1, "inimprop", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtInimprop.append(wx.TextCtrl(self.swCMHolder, -1, str(imptor.get_number_improper_torsions()), size=(75,-1)))
            self.InimpropIDs.append(self.txtInimprop[-1].GetId())
            wx.EVT_TEXT(self, self.txtInimprop[-1].GetId(), self.InimpropChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            for imps in imptor.get_improper_torsions():
                tempImp2.append(wx.TextCtrl(self.swCMHolder, -1, str(imps[0]), size=(75,-1)))
                tempImp3.append(wx.TextCtrl(self.swCMHolder, -1, str(imps[1]), size=(75,-1)))
                tempImp4.append(wx.TextCtrl(self.swCMHolder, -1, str(imps[2]), size=(75,-1)))
                tempItim.append(wx.TextCtrl(self.swCMHolder, -1, str(imps[3]), size=(75,-1)))
            self.txtIjimprop2.append(tempImp2)
            self.txtIjimprop3.append(tempImp3)
            self.txtIjimprop4.append(tempImp4)
            self.txtItimprop.append(tempItim)
        for i in range(len(input.get_improper_torsions()), input.get_nunit()):
            new_it = input.create_improper_torsions()
            self.imptors.append(new_it)
            self.lblInimprop.append(wx.StaticText(self.swCMHolder, -1, "inimprop", style=wx.ALIGN_RIGHT, size=cmsize))
            self.txtInimprop.append(wx.TextCtrl(self.swCMHolder, -1, "0", size=(75,-1)))
            self.InimpropIDs.append(self.txtInimprop[i].GetId())
            wx.EVT_TEXT(self, self.txtInimprop[i].GetId(), self.InimpropChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            self.txtIjimprop2.append(tempImp2)
            self.txtIjimprop3.append(tempImp3)
            self.txtIjimprop4.append(tempImp4)
            self.txtItimprop.append(tempItim)

        self.btnOK = wx.Button(self.swCMHolder, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self.swCMHolder, wx.ID_CANCEL, "Cancel")
        
        self.SetTitle("Input Style 2")
        self.btnOK.SetDefault()
        self.swCMHolder.SetScrollRate(50,50)
        self.__do_layout()
        self.Center()
        return

    def __do_layout(self):
        self.szrCMDialog = wx.BoxSizer(wx.VERTICAL)
        self.szrForcefield = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCharge_assignment = wx.BoxSizer(wx.HORIZONTAL)
        self.szrCMAtoms = []
        self.szrUnit = []
        self.szrType = []
        self.szrQqatom = []
        self.szrVibrations = []
        self.szrInvib = []
        self.szrIjvib = []
        self.szrImpTors = []
        self.szrInimprop = []
        self.szrIjimprop = []
        for i in range(self.nunit):
            self.szrCMAtoms.append(wx.StaticBoxSizer(wx.StaticBox(self.swCMHolder, -1, "Atom " + str(i+1)), wx.VERTICAL))
            self.szrUnit.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrType.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrQqatom.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrVibrations.append(wx.StaticBoxSizer(wx.StaticBox(self.swCMHolder, -1, "Vibrations"), wx.VERTICAL))
            self.szrInvib.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrIjvib.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrImpTors.append(wx.StaticBoxSizer(wx.StaticBox(self.swCMHolder, -1, "Improper Torsions"), wx.VERTICAL))
            self.szrInimprop.append(wx.BoxSizer(wx.HORIZONTAL))
            tempIjimprop = []
            for j in range(self.imptors[i].get_number_improper_torsions()):
                tempIjimprop.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrIjimprop.append(tempIjimprop)
        self.szrButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.szrForcefield.Add(self.lblForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrForcefield.Add(self.txtForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrCharge_assignment.Add(self.lblCharge_assignment, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrCharge_assignment.Add(self.cboCharge_assignment, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrCMDialog.Add(self.szrForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrCMDialog.Add(self.szrCharge_assignment, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

        for i in range(self.nunit):
            self.szrUnit[i].Add(self.lblUnit[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrUnit[i].Add(self.txtUnit[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrType[i].Add(self.lblType[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrType[i].Add(self.txtType[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrQqatom[i].Add(self.lblQqatom[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrQqatom[i].Add(self.txtQqatom[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

            self.szrCMAtoms[i].Add(self.szrUnit[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrCMAtoms[i].Add(self.szrType[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrCMAtoms[i].Add(self.szrQqatom[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            
            self.szrInvib[i].Add(self.lblInvib[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrInvib[i].Add(self.txtInvib[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            for j in self.txtIjvib[i]:
                self.szrIjvib[i].Add(j, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrVibrations[i].Add(self.szrInvib[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrVibrations[i].Add(self.szrIjvib[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrCMAtoms[i].Add(self.szrVibrations[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)

            self.szrInimprop[i].Add(self.lblInimprop[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrInimprop[i].Add(self.txtInimprop[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrImpTors[i].Add(self.szrInimprop[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            for j in range(self.imptors[i].get_number_improper_torsions()):
                self.szrIjimprop[i][j].Add(self.txtIjimprop2[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjimprop[i][j].Add(self.txtIjimprop3[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjimprop[i][j].Add(self.txtIjimprop4[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjimprop[i][j].Add(self.txtItimprop[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrImpTors[i].Add(self.szrIjimprop[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrCMAtoms[i].Add(self.szrImpTors[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrCMDialog.Add(self.szrCMAtoms[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

        charge = self.cboCharge_assignment.GetValue()
        if charge != "manual":
            for i in range(len(self.szrCMAtoms)):
                self.szrCMAtoms[i].Hide(self.szrQqatom[i])

        self.szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrCMDialog.Add(self.szrButtons, 1, wx.ALL|wx.ALIGN_LEFT, 5)

        self.swCMHolder.SetAutoLayout(1)
        self.swCMHolder.SetSizer(self.szrCMDialog)
        self.szrCMDialog.FitInside(self.swCMHolder)
        self.szrCMDialog.SetVirtualSizeHints(self.swCMHolder)
        return

    def ChargeAssignmentChanged(self, evt):
        charge = self.cboCharge_assignment.GetStringSelection()
        if charge == "manual":
            for i in range(len(self.szrCMAtoms)):
                self.szrCMAtoms[i].Show(self.szrQqatom[i])
                self.szrCMAtoms[i].Layout()
        else:
            for i in range(len(self.szrCMAtoms)):
                self.szrCMAtoms[i].Hide(self.szrQqatom[i])
                self.szrCMAtoms[i].Layout()
        self.szrCMDialog.Layout() 
        return

    def InvibChanged(self, evt):
        index = self.InvibIDs.index(evt.GetId())
        l = self.txtInvib[index].GetValue()
        if l.isdigit():
            l = int(l)
            old_value = self.vibs[index].get_number_vibrations()
            if l > old_value:
                for i in range(old_value, l):
                    self.txtIjvib[index].append(wx.TextCtrl(self.swCMHolder, -1, "0", size=(75,-1)))
                    self.szrIjvib[index].Add(self.txtIjvib[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            elif l < old_value:
                for i in range(l, old_value):
                    self.szrIjvib[index].Remove(self.txtIjvib[index][-1])
                    self.txtIjvib[index][-1].Destroy()
                    self.txtIjvib[index].pop()

            self.vibs[index].set_number_vibrations(l)
            self.szrIjvib[index].Layout()
            self.szrVibrations[index].Layout()
            self.szrCMAtoms[index].Layout()
            self.szrCMDialog.FitInside(self.swCMHolder)
            self.Refresh()
        return

    def InimpropChanged(self, evt):
        index = self.InimpropIDs.index(evt.GetId())
        l = self.txtInimprop[index].GetValue()
        if l.isdigit():
            l = int(l)
            old_value = self.imptors[index].get_number_improper_torsions()
            if l > old_value:
                for i in range(old_value, l):
                    self.txtIjimprop2[index].append(wx.TextCtrl(self.swCMHolder, -1, "0", size=(75,-1)))
                    self.txtIjimprop3[index].append(wx.TextCtrl(self.swCMHolder, -1, "0", size=(75,-1)))
                    self.txtIjimprop4[index].append(wx.TextCtrl(self.swCMHolder, -1, "0", size=(75,-1)))
                    self.txtItimprop[index].append(wx.TextCtrl(self.swCMHolder, -1, "0", size=(75,-1)))
                    self.szrIjimprop[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrIjimprop[index][-1].Add(self.txtIjimprop2[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjimprop[index][-1].Add(self.txtIjimprop3[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjimprop[index][-1].Add(self.txtIjimprop4[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjimprop[index][-1].Add(self.txtItimprop[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrImpTors[index].Add(self.szrIjimprop[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            elif l < old_value:
                for i in range(l, old_value):
                    self.szrImpTors[index].Remove(self.szrIjimprop[index][-1])
                    self.txtIjimprop2[index][-1].Destroy()
                    self.txtIjimprop3[index][-1].Destroy()
                    self.txtIjimprop4[index][-1].Destroy()
                    self.txtItimprop[index][-1].Destroy()
                    self.txtIjimprop2[index].pop()
                    self.txtIjimprop3[index].pop()
                    self.txtIjimprop4[index].pop()
                    self.txtItimprop[index].pop()
                    self.szrIjimprop[index].pop()

            self.imptors[index].set_number_improper_torsions(l)
            self.szrImpTors[index].Layout()
            self.szrCMAtoms[index].Layout()
            self.szrCMDialog.FitInside(self.swCMHolder)
            self.Refresh()
        return
# end of class ConnectivityMap


class PolypeptideBuilder(wx.Dialog):
    def __init__(self, parent, ID, title, input, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        kwds["size"] = (480,400)
        wx.Dialog.__init__(self, parent, ID, title, **kwds)

        self.nunit = input.get_nunit()
        pepname = self.ResolveLengthDifferences(input.get_pepname(), input.get_nunit(), "")
        stereochem = self.ResolveLengthDifferences(input.get_stereochem(), input.get_nunit(), "")
        bondpartner = self.ResolveLengthDifferences(input.get_bondpartner(), input.get_nunit(), "0")
        terminus = self.ResolveLengthDifferences(input.get_terminus(), input.get_nunit(), "")
 
        self.swPBHolder = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        #
        # Work around for bug in wxPython 2.5.2.8
        #
        self.swPBHolder.SetBackgroundColour(self.swPBHolder.GetBackgroundColour())

        self.lblBondpartner = wx.StaticText(self.swPBHolder, -1, "bondpartner")
        listsize = self.lblBondpartner.GetSize()
        self.lblForcefield = wx.StaticText(self.swPBHolder, -1, "forcefield", style=wx.ALIGN_RIGHT, size=listsize)
        self.txtForcefield = wx.TextCtrl(self.swPBHolder, -1, input.get_forcefield(), size=(300,-1))
        self.lblProtgeom = wx.StaticText(self.swPBHolder, -1, "protgeom", style=wx.ALIGN_RIGHT, size=listsize)
        self.cboProtgeom = wx.ComboBox(self.swPBHolder, -1, choices=["linear", "cyclic"], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        if input.get_protgeom() == "cyclic":
            self.cboProtgeom.SetSelection(1)
            self.protgeom = "cyclic"
        else:
            self.cboProtgeom.SetSelection(0)
            self.protgeom = "linear"
        self.lblPepname = wx.StaticText(self.swPBHolder, -1, "pepname", style=wx.ALIGN_CENTER, size=listsize)
        self.lblStereochem = wx.StaticText(self.swPBHolder, -1, "stereochem", style=wx.ALIGN_CENTER, size=listsize)
        self.lblTerminus = wx.StaticText(self.swPBHolder, -1, "terminus", style=wx.ALIGN_CENTER, size=listsize)
        self.txtPepname =  []
        self.txtStereochem = []
        self.txtBondpartner =[]
        self.txtTerminus = []
        for i in range(input.get_nunit()):
            self.txtPepname.append(wx.TextCtrl(self.swPBHolder, -1, pepname[i], size=(listsize[0], -1)))
            self.txtStereochem.append(wx.TextCtrl(self.swPBHolder, -1, stereochem[i], size=(listsize[0], -1)))
            self.txtBondpartner.append(wx.TextCtrl(self.swPBHolder, -1, str(bondpartner[i]), size=(listsize[0], -1)))
            self.txtTerminus.append(wx.TextCtrl(self.swPBHolder, -1, terminus[i], size=(listsize[0], -1)))

        self.btnOK = wx.Button(self.swPBHolder, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self.swPBHolder, wx.ID_CANCEL, "Cancel")

        wx.EVT_COMBOBOX(self, self.cboProtgeom.GetId(), self.ProtgeomChanged)

        self.SetTitle("Input Style 1")
        self.btnOK.SetDefault()
        self.swPBHolder.SetScrollRate(0,50)
        self.__do_layout()
        self.UpdateDisplay()
        self.Center()
        return

    def __do_layout(self):
        self.szrPBDialog = wx.BoxSizer(wx.VERTICAL)
        self.szrForcefield = wx.BoxSizer(wx.HORIZONTAL)
        self.szrProtgeom = wx.BoxSizer(wx.HORIZONTAL)
        self.szrAminoAcids = wx.BoxSizer(wx.VERTICAL)
        self.szrAminoLabels = wx.BoxSizer(wx.HORIZONTAL)
        self.szrAminoValues = []
        for i in range(self.nunit):
            self.szrAminoValues.append(wx.BoxSizer(wx.HORIZONTAL))
        self.szrButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.szrForcefield.Add(self.lblForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrForcefield.Add(self.txtForcefield, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.szrProtgeom.Add(self.lblProtgeom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrProtgeom.Add(self.cboProtgeom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.szrAminoLabels.Add(self.lblPepname, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrAminoLabels.Add(self.lblStereochem, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrAminoLabels.Add(self.lblBondpartner, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrAminoLabels.Add(self.lblTerminus, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.szrAminoAcids.Add(self.szrAminoLabels, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
        for i in range(self.nunit):
            self.szrAminoValues[i].Add(self.txtPepname[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            self.szrAminoValues[i].Add(self.txtStereochem[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            self.szrAminoValues[i].Add(self.txtBondpartner[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            self.szrAminoValues[i].Add(self.txtTerminus[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
            self.szrAminoAcids.Add(self.szrAminoValues[i], 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.szrPBDialog.Add(self.szrForcefield, 0, wx.ALL|wx.EXPAND, 5)
        self.szrPBDialog.Add(self.szrProtgeom, 0, wx.ALL|wx.EXPAND, 5)
        self.szrPBDialog.Add(self.szrAminoAcids, 0, wx.ALL|wx.EXPAND, 5)
        self.szrPBDialog.Add(self.szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.swPBHolder.SetAutoLayout(1)
        self.swPBHolder.SetSizer(self.szrPBDialog)
        self.szrPBDialog.Fit(self.swPBHolder)
        self.szrPBDialog.SetVirtualSizeHints(self.swPBHolder)
        return

    def ProtgeomChanged(self, *args):
        l = self.cboProtgeom.GetStringSelection()
        self.protgeom = l
        self.UpdateDisplay()
        return

    def UpdateDisplay(self):
        if self.protgeom == "linear":
            self.lblTerminus.Show()
            for i in self.txtTerminus:
                i.Show()
        else:    
            self.lblTerminus.Hide()
            for i in self.txtTerminus:
                i.Hide()
        self.szrAminoLabels.Layout()
        for i in range(self.nunit):
            self.szrAminoValues[i].Layout()
        self.szrAminoAcids.Layout()
        self.szrPBDialog.Layout()
        return

    def ResolveLengthDifferences(self, array, length, value):
        l = len(array)
        if length > l:
            for i in range(l, length):
                array.append(value)
        elif length < l:
            for i in range(length, l):
                array.pop()
        return array
# end of class PolypeptideBuilder


class ExplicitDeclaration(wx.Dialog):
    def __init__(self, parent, ID, title, input, **kwds):
        kwds["style"] = wx.DIALOG_MODAL|wx.CAPTION|wx.SYSTEM_MENU
        kwds["size"] = (375,600)
        kwds["title"] = "Input Style 0"
        wx.Dialog.__init__(self, parent, ID, **kwds)
        self.nunit = input.get_nunit()
        self.vibs = input.get_vibrations()
        self.bends = input.get_bendings()
        self.tors = input.get_torsions()
        self.angles =  input.get_angles()
        self.imptors = input.get_improper_torsions()

        self.swEDHolder = wx.ScrolledWindow(self, -1, style=wx.TAB_TRAVERSAL)
        #
        # Work around for bug in wxPython 2.5.2.8
        #
        self.swEDHolder.SetBackgroundColour(self.swEDHolder.GetBackgroundColour())
        
        self.rbLPDB = wx.RadioBox(self.swEDHolder, -1, "lpdb", choices=["True", "False"], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        if input.get_lpdb():
            self.rbLPDB.SetSelection(0)
        else:
            self.rbLPDB.SetSelection(1)

        self.lblAminoshort = []
        self.txtAminoshort = []
        for i in input.get_aminoshort():
            self.lblAminoshort.append(wx.StaticText(self.swEDHolder, -1, "aminoshort", style=wx.ALIGN_RIGHT))
            self.txtAminoshort.append(wx.TextCtrl(self.swEDHolder, -1, i, size=(75,-1)))
        for i in range(len(input.get_aminoshort()), input.get_nunit()):
            self.lblAminoshort.append(wx.StaticText(self.swEDHolder, -1, "aminoshort", style=wx.ALIGN_RIGHT))
            self.txtAminoshort.append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
        edsize = self.lblAminoshort[0].GetSize()

        self.lblUnit = []
        self.txtUnit = []
        for i in range(input.get_nunit()):
            self.lblUnit.append(wx.StaticText(self.swEDHolder, -1, "Unit", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtUnit.append(wx.TextCtrl(self.swEDHolder, -1, str(i+1), size=(50,-1)))

        self.lblType = []
        self.txtType = []
        for i in input.get_type():
            self.lblType.append(wx.StaticText(self.swEDHolder, -1, "Type", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtType.append(wx.TextCtrl(self.swEDHolder, -1, str(i), size=(50,-1)))
        for i in range(len(input.get_type()), input.get_nunit()):
            self.lblType.append(wx.StaticText(self.swEDHolder, -1, "Type", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtType.append(wx.TextCtrl(self.swEDHolder, -1, "", size=(50,-1)))

        self.lblQqatom = []
        self.txtQqatom = []
        for i in input.get_qqatom():
            self.lblQqatom.append(wx.StaticText(self.swEDHolder, -1, "qqatom", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtQqatom.append(wx.TextCtrl(self.swEDHolder, -1, i, size=(75,-1)))
        for i in range(len(input.get_qqatom()), input.get_nunit()):
            self.lblQqatom.append(wx.StaticText(self.swEDHolder, -1, "qqatom", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtQqatom.append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))

        self.lblPdbname = []
        self.txtPdbname = []
        for i in input.get_pdbname():
            self.lblPdbname.append(wx.StaticText(self.swEDHolder, -1, "pdbname", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtPdbname.append(wx.TextCtrl(self.swEDHolder, -1, i, size=(50,-1)))
        for i in range(len(input.get_pdbname()), input.get_nunit()):
            self.lblPdbname.append(wx.StaticText(self.swEDHolder, -1, "pdbname", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtPdbname.append(wx.TextCtrl(self.swEDHolder, -1, "", size=(50,-1)))

        self.lblAminonum = []
        self.txtAminonum = []
        for i in input.get_aminonum():
            self.lblAminonum.append(wx.StaticText(self.swEDHolder, -1, "aminonum", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtAminonum.append(wx.TextCtrl(self.swEDHolder, -1, str(i), size=(50,-1)))
        for i in range(len(input.get_aminonum()), input.get_nunit()):
            self.lblAminonum.append(wx.StaticText(self.swEDHolder, -1, "aminonum", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtAminonum.append(wx.TextCtrl(self.swEDHolder, -1, "", size=(50,-1)))
        #
        # Vibrations
        #
        self.lblInvib = []
        self.txtInvib = []
        self.txtIjvib = []
        self.txtItvib = []
        self.InvibIDs = []
        for v in input.get_vibrations():
            self.lblInvib.append(wx.StaticText(self.swEDHolder, -1, "invib", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInvib.append(wx.TextCtrl(self.swEDHolder, -1, str(v.get_number_vibrations()), size=(75,-1)))
            self.InvibIDs.append(self.txtInvib[-1].GetId())
            wx.EVT_TEXT(self, self.txtInvib[-1].GetId(), self.InvibChanged)
            tempIjvib = []
            tempItvib = []
            for vibes in v.get_vibrations():
                tempIjvib.append(wx.TextCtrl(self.swEDHolder, -1, str(vibes[0]), size=(75,-1)))
                tempItvib.append(wx.TextCtrl(self.swEDHolder, -1, str(vibes[1]), size=(75,-1)))
            self.txtIjvib.append(tempIjvib)
            self.txtItvib.append(tempItvib)
        for i in range(len(input.get_vibrations()), input.get_nunit()):
            new_vib = input.create_vibrations()
            self.vibs.append(new_vib)
            self.lblInvib.append(wx.StaticText(self.swEDHolder, -1, "invib", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInvib.append(wx.TextCtrl(self.swEDHolder, -1, "0", size=(75,-1)))
            self.InvibIDs.append(self.txtInvib[-1].GetId())
            wx.EVT_TEXT(self, self.txtInvib[-1].GetId(), self.InvibChanged)
            tempIjvib = []
            tempItvib = []
            self.txtIjvib.append(tempIjvib)
            self.txtItvib.append(tempItvib)
        #
        # Bending
        #
        self.lblInben = []
        self.txtInben = []
        self.txtIjben2 = []
        self.txtIjben3 = []
        self.txtItben = []
        self.InbenIDs = []
        for b in input.get_bendings():
            self.lblInben.append(wx.StaticText(self.swEDHolder, -1, "inben", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInben.append(wx.TextCtrl(self.swEDHolder, -1, str(b.get_number_bendings()), size=(75,-1)))
            self.InbenIDs.append(self.txtInben[-1].GetId())
            wx.EVT_TEXT(self, self.txtInben[-1].GetId(), self.InbenChanged)
            tempIjben2 = []
            tempIjben3 = []
            tempItben = []
            for bends in b.get_bendings():
                tempIjben2.append(wx.TextCtrl(self.swEDHolder, -1, str(bends[0]), size=(75,-1)))
                tempIjben3.append(wx.TextCtrl(self.swEDHolder, -1, str(bends[1]), size=(75,-1)))
                tempItben.append(wx.TextCtrl(self.swEDHolder, -1, str(bends[2]), size=(75,-1)))
            self.txtIjben2.append(tempIjben2)
            self.txtIjben3.append(tempIjben3)
            self.txtItben.append(tempItben)
        for i in range(len(input.get_bendings()), input.get_nunit()):
            new_bend = input.create_bendings()
            self.bends.append(new_bend)
            self.lblInben.append(wx.StaticText(self.swEDHolder, -1, "inben", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInben.append(wx.TextCtrl(self.swEDHolder, -1, "0", size=(75,-1)))
            self.InbenIDs.append(self.txtInben[-1].GetId())
            wx.EVT_TEXT(self, self.txtInben[-1].GetId(), self.InbenChanged)
            tempIjben2 = []
            tempIjben3 = []
            tempItben = []
            self.txtIjben2.append(tempIjben2)
            self.txtIjben3.append(tempIjben3)
            self.txtItben.append(tempItben)
        #
        # Torsions
        #
        self.lblIntor = []
        self.txtIntor = []
        self.txtIjtor2 = []
        self.txtIjtor3 = []
        self.txtIjtor4 = []
        self.txtIttor = []
        self.IntorIDs = []
        for t in input.get_torsions():
            self.lblIntor.append(wx.StaticText(self.swEDHolder, -1, "intor", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtIntor.append(wx.TextCtrl(self.swEDHolder, -1, str(t.get_number_torsions()), size=(75,-1)))
            self.IntorIDs.append(self.txtIntor[-1].GetId())
            wx.EVT_TEXT(self, self.txtIntor[-1].GetId(), self.IntorChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            for tors in t.get_torsions():
                tempImp2.append(wx.TextCtrl(self.swEDHolder, -1, str(tors[0]), size=(75,-1)))
                tempImp3.append(wx.TextCtrl(self.swEDHolder, -1, str(tors[1]), size=(75,-1)))
                tempImp4.append(wx.TextCtrl(self.swEDHolder, -1, str(tors[2]), size=(75,-1)))
                tempItim.append(wx.TextCtrl(self.swEDHolder, -1, str(tors[3]), size=(75,-1)))
            self.txtIjtor2.append(tempImp2)
            self.txtIjtor3.append(tempImp3)
            self.txtIjtor4.append(tempImp4)
            self.txtIttor.append(tempItim)
        for i in range(len(input.get_torsions()), input.get_nunit()):
            new_tor = input.create_torsions()
            self.tors.append(new_tor)
            self.lblIntor.append(wx.StaticText(self.swEDHolder, -1, "intor", style=wx.ALIGN_RIGHT, size=(80,-1)))
            self.txtIntor.append(wx.TextCtrl(self.swEDHolder, -1, "0", size=(75,-1)))
            self.IntorIDs.append(self.txtIntor[-1].GetId())
            wx.EVT_TEXT(self, self.txtIntor[-1].GetId(), self.IntorChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            self.txtIjtor2.append(tempImp2)
            self.txtIjtor3.append(tempImp3)
            self.txtIjtor4.append(tempImp4)
            self.txtIttor.append(tempItim)
        #
        # Angle-Angle
        #
        self.lblInaa = []
        self.txtInaa = []
        self.txtIjaa0 = []
        self.txtIjaa1 = []
        self.txtIjaa2 = []
        self.txtItaa = []
        self.InaaIDs = []
        for a in input.get_angles():
            self.lblInaa.append(wx.StaticText(self.swEDHolder, -1, "inaa", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInaa.append(wx.TextCtrl(self.swEDHolder, -1, str(a.get_number_angles()), size=(75,-1)))
            self.InaaIDs.append(self.txtInaa[-1].GetId())
            wx.EVT_TEXT(self, self.txtInaa[-1].GetId(), self.InaaChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            for angles in a.get_angles():
                tempImp2.append(wx.TextCtrl(self.swEDHolder, -1, str(angles[0]), size=(75,-1)))
                tempImp3.append(wx.TextCtrl(self.swEDHolder, -1, str(angles[1]), size=(75,-1)))
                tempImp4.append(wx.TextCtrl(self.swEDHolder, -1, str(angles[2]), size=(75,-1)))
                tempItim.append(wx.TextCtrl(self.swEDHolder, -1, str(angles[3]), size=(75,-1)))
            self.txtIjaa0.append(tempImp2)
            self.txtIjaa1.append(tempImp3)
            self.txtIjaa2.append(tempImp4)
            self.txtItaa.append(tempItim)
        for i in range(len(input.get_angles()), input.get_nunit()):
            new_ang = input.create_angles()
            self.angles.append(new_ang)
            self.lblInaa.append(wx.StaticText(self.swEDHolder, -1, "inaa", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInaa.append(wx.TextCtrl(self.swEDHolder, -1, "0", size=(75,-1)))
            self.InaaIDs.append(self.txtInaa[-1].GetId())
            wx.EVT_TEXT(self, self.txtInaa[-1].GetId(), self.InaaChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            self.txtIjaa0.append(tempImp2)
            self.txtIjaa1.append(tempImp3)
            self.txtIjaa2.append(tempImp4)
            self.txtItaa.append(tempItim)
        #
        # Improper Torsions
        #
        self.lblInimprop = []
        self.txtInimprop = []
        self.txtIjimprop2 = []
        self.txtIjimprop3 = []
        self.txtIjimprop4 = []
        self.txtItimprop = []
        self.InimpropIDs = []
        for it in input.get_improper_torsions():
            self.lblInimprop.append(wx.StaticText(self.swEDHolder, -1, "inimprop", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInimprop.append(wx.TextCtrl(self.swEDHolder, -1, str(it.get_number_improper_torsions()), size=(75,-1)))
            self.InimpropIDs.append(self.txtInimprop[-1].GetId())
            wx.EVT_TEXT(self, self.txtInimprop[-1].GetId(), self.InimpropChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            for imps in it.get_improper_torsions():
                tempImp2.append(wx.TextCtrl(self.swEDHolder, -1, str(imps[0]), size=(75,-1)))
                tempImp3.append(wx.TextCtrl(self.swEDHolder, -1, str(imps[1]), size=(75,-1)))
                tempImp4.append(wx.TextCtrl(self.swEDHolder, -1, str(imps[2]), size=(75,-1)))
                tempItim.append(wx.TextCtrl(self.swEDHolder, -1, str(imps[3]), size=(75,-1)))
            self.txtIjimprop2.append(tempImp2)
            self.txtIjimprop3.append(tempImp3)
            self.txtIjimprop4.append(tempImp4)
            self.txtItimprop.append(tempItim)
        for i in range(len(input.get_improper_torsions()), input.get_nunit()):
            new_it = input.create_improper_torsions()
            self.imptors.append(new_it)
            self.lblInimprop.append(wx.StaticText(self.swEDHolder, -1, "inimprop", style=wx.ALIGN_RIGHT, size=edsize))
            self.txtInimprop.append(wx.TextCtrl(self.swEDHolder, -1, "0", size=(75,-1)))
            self.InimpropIDs.append(self.txtInimprop[-1].GetId())
            wx.EVT_TEXT(self, self.txtInimprop[-1].GetId(), self.InimpropChanged)
            tempImp2 = []
            tempImp3 = []
            tempImp4 = []
            tempItim = []
            self.txtIjimprop2.append(tempImp2)
            self.txtIjimprop3.append(tempImp3)
            self.txtIjimprop4.append(tempImp4)
            self.txtItimprop.append(tempItim)

        self.btnOK = wx.Button(self.swEDHolder, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self.swEDHolder, wx.ID_CANCEL, "Cancel")
        
        wx.EVT_RADIOBOX(self, self.rbLPDB.GetId(), self.LPDBChanged)

        self.btnOK.SetDefault()
        self.swEDHolder.SetScrollRate(0,50)
        self.__do_layout()
        self.LPDBChanged()
        self.Center()
        return

    def __do_layout(self):
        self.szrEDDialog = wx.BoxSizer(wx.VERTICAL)
        self.szrEDAtoms = []
        self.szrUnit = []
        self.szrType = []
        self.szrQqatom = []
        self.szrPdbname = []
        self.szrAminonum = []
        self.szrAminoshort = []
        self.szrVibrations = []
        self.szrInvib = []
        self.szrIjvib = []
        self.szrBendings = []
        self.szrInben = []
        self.szrIjben = []
        self.szrTorsions = []
        self.szrIntor = []
        self.szrIjtor = []
        self.szrAngleAngles = []
        self.szrInaa = []
        self.szrIjaa = []
        self.szrImproperTorsions = []
        self.szrInimprop = []
        self.szrIjimprop = []
        for i in range(self.nunit):
            self.szrEDAtoms.append(wx.StaticBoxSizer(wx.StaticBox(self.swEDHolder, -1, "Atom " + str(i+1)), wx.VERTICAL))
            self.szrUnit.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrType.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrQqatom.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrPdbname.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrAminonum.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrAminoshort.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrVibrations.append(wx.StaticBoxSizer(wx.StaticBox(self.swEDHolder, -1, "Vibrations"), wx.VERTICAL))
            self.szrInvib.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrBendings.append(wx.StaticBoxSizer(wx.StaticBox(self.swEDHolder, -1, "Bendings"), wx.VERTICAL))
            self.szrInben.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrTorsions.append(wx.StaticBoxSizer(wx.StaticBox(self.swEDHolder, -1, "Torsions"), wx.VERTICAL))
            self.szrIntor.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrAngleAngles.append(wx.StaticBoxSizer(wx.StaticBox(self.swEDHolder, -1, "Angle Angles"), wx.VERTICAL))
            self.szrInaa.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrImproperTorsions.append(wx.StaticBoxSizer(wx.StaticBox(self.swEDHolder, -1, "Improper Torsions"), wx.VERTICAL))
            self.szrInimprop.append(wx.BoxSizer(wx.HORIZONTAL))
            tempIjvib = []
            for j in range(self.vibs[i].get_number_vibrations()):
                tempIjvib.append(wx.BoxSizer(wx.HORIZONTAL))
            tempIjben = []
            for j in range(self.bends[i].get_number_bendings()):
                tempIjben.append(wx.BoxSizer(wx.HORIZONTAL))
            tempIjtor = []
            for j in range(self.tors[i].get_number_torsions()):
                tempIjtor.append(wx.BoxSizer(wx.HORIZONTAL))
            tempIjaa = []
            for j in range(self.angles[i].get_number_angles()):
                tempIjaa.append(wx.BoxSizer(wx.HORIZONTAL))
            tempIjimprop = []
            for j in range(self.imptors[i].get_number_improper_torsions()):
                tempIjimprop.append(wx.BoxSizer(wx.HORIZONTAL))
            self.szrIjvib.append(tempIjvib)
            self.szrIjben.append(tempIjben)
            self.szrIjtor.append(tempIjtor)
            self.szrIjaa.append(tempIjaa)
            self.szrIjimprop.append(tempIjimprop)
        self.szrButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.szrEDDialog.Add(self.rbLPDB, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        for i in range(self.nunit):
            self.szrUnit[i].Add(self.lblUnit[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrUnit[i].Add(self.txtUnit[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrType[i].Add(self.lblType[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrType[i].Add(self.txtType[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrQqatom[i].Add(self.lblQqatom[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrQqatom[i].Add(self.txtQqatom[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

            self.szrEDAtoms[i].Add(self.szrUnit[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrEDAtoms[i].Add(self.szrType[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrEDAtoms[i].Add(self.szrQqatom[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

            self.szrPdbname[i].Add(self.lblPdbname[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrPdbname[i].Add(self.txtPdbname[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrAminonum[i].Add(self.lblAminonum[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrAminonum[i].Add(self.txtAminonum[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrAminoshort[i].Add(self.lblAminoshort[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrAminoshort[i].Add(self.txtAminoshort[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

            self.szrEDAtoms[i].Add(self.szrPdbname[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrEDAtoms[i].Add(self.szrAminonum[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrEDAtoms[i].Add(self.szrAminoshort[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            # Vibrations
            self.szrInvib[i].Add(self.lblInvib[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrInvib[i].Add(self.txtInvib[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrVibrations[i].Add(self.szrInvib[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            for j in range(self.vibs[i].get_number_vibrations()):
                self.szrIjvib[i][j].Add(self.txtIjvib[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjvib[i][j].Add(self.txtItvib[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrVibrations[i].Add(self.szrIjvib[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrEDAtoms[i].Add(self.szrVibrations[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            # Bendingss
            self.szrInben[i].Add(self.lblInben[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrInben[i].Add(self.txtInben[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrBendings[i].Add(self.szrInben[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            for j in range(self.bends[i].get_number_bendings()):
                self.szrIjben[i][j].Add(self.txtIjben2[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjben[i][j].Add(self.txtIjben3[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjben[i][j].Add(self.txtItben[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrBendings[i].Add(self.szrIjben[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrEDAtoms[i].Add(self.szrBendings[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            # Torsions
            self.szrIntor[i].Add(self.lblIntor[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrIntor[i].Add(self.txtIntor[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrTorsions[i].Add(self.szrIntor[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            for j in range(self.tors[i].get_number_torsions()):
                self.szrIjtor[i][j].Add(self.txtIjtor2[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjtor[i][j].Add(self.txtIjtor3[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjtor[i][j].Add(self.txtIjtor4[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjtor[i][j].Add(self.txtIttor[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrTorsions[i].Add(self.szrIjtor[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrEDAtoms[i].Add(self.szrTorsions[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            # Angle-Angles
            self.szrInaa[i].Add(self.lblInaa[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrInaa[i].Add(self.txtInaa[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrAngleAngles[i].Add(self.szrInaa[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            for j in range(self.angles[i].get_number_angles()):
                self.szrIjaa[i][j].Add(self.txtIjaa0[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjaa[i][j].Add(self.txtIjaa1[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjaa[i][j].Add(self.txtIjaa2[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjaa[i][j].Add(self.txtItaa[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrAngleAngles[i].Add(self.szrIjaa[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrEDAtoms[i].Add(self.szrAngleAngles[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            # Improper Torsions
            self.szrInimprop[i].Add(self.lblInimprop[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrInimprop[i].Add(self.txtInimprop[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrImproperTorsions[i].Add(self.szrInimprop[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            for j in range(self.imptors[i].get_number_improper_torsions()):
                self.szrIjimprop[i][j].Add(self.txtIjimprop2[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjimprop[i][j].Add(self.txtIjimprop3[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjimprop[i][j].Add(self.txtIjimprop4[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrIjimprop[i][j].Add(self.txtItimprop[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                self.szrImproperTorsions[i].Add(self.szrIjimprop[i][j], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            self.szrEDAtoms[i].Add(self.szrImproperTorsions[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            self.szrEDDialog.Add(self.szrEDAtoms[i], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            
        self.szrButtons.Add(self.btnOK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrButtons.Add(self.btnCancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.szrEDDialog.Add(self.szrButtons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 2)

        self.swEDHolder.SetAutoLayout(1)
        self.swEDHolder.SetSizer(self.szrEDDialog)
        self.szrEDDialog.SetVirtualSizeHints(self.swEDHolder)
        self.szrEDDialog.FitInside(self.swEDHolder)
        self.Layout()
        return

    def InvibChanged(self, evt):
        index = self.InvibIDs.index(evt.GetId())
        l = self.txtInvib[index].GetValue()
        if l.isdigit():
            l = int(l)
            old_value = self.vibs[index].get_number_vibrations()
            if l > old_value:
                for i in range(old_value, l):
                    self.txtIjvib[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtItvib[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.szrIjvib[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrIjvib[index][-1].Add(self.txtIjvib[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjvib[index][-1].Add(self.txtItvib[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrVibrations[index].Add(self.szrIjvib[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            elif l < old_value:
                for i in range(l, old_value):
                    self.szrVibrations[index].Remove(self.szrIjvib[index][-1])
                    self.txtIjvib[index][-1].Destroy()
                    self.txtItvib[index][-1].Destroy()
                    self.txtIjvib[index].pop()
                    self.txtItvib[index].pop()
                    self.szrIjvib[index].pop()

            self.vibs[index].set_number_vibrations(l)
            self.szrVibrations[index].Layout()
            self.szrEDAtoms[index].Layout()
            self.szrEDDialog.FitInside(self.swEDHolder)
            self.Refresh()
        return

    def InbenChanged(self, evt):
        index = self.InbenIDs.index(evt.GetId())
        l = self.txtInben[index].GetValue()
        if l.isdigit():
            l = int(l)
            old_value = self.bends[index].get_number_bendings()
            if l > old_value:
                for i in range(old_value, l):
                    self.txtIjben2[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIjben3[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtItben[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.szrIjben[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrIjben[index][-1].Add(self.txtIjben2[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjben[index][-1].Add(self.txtIjben3[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjben[index][-1].Add(self.txtItben[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrBendings[index].Add(self.szrIjben[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            elif l < old_value:
                for i in range(l, old_value):
                    self.szrBendings[index].Remove(self.szrIjben[index][-1])
                    self.txtIjben2[index][-1].Destroy()
                    self.txtIjben3[index][-1].Destroy()
                    self.txtItben[index][-1].Destroy()
                    self.txtIjben2[index].pop()
                    self.txtIjben3[index].pop()
                    self.txtItben[index].pop()
                    self.szrIjben[index].pop()

            self.bends[index].set_number_bendings(l)
            self.szrBendings[index].Layout()
            self.szrEDAtoms[index].Layout()
            self.szrEDDialog.FitInside(self.swEDHolder)
            self.Refresh()
        return

    def IntorChanged(self, evt):
        index = self.IntorIDs.index(evt.GetId())
        l = self.txtIntor[index].GetValue()
        if l.isdigit():
            l = int(l)
            old_value = self.tors[index].get_number_torsions()
            if l > old_value:
                for i in range(old_value, l):
                    self.txtIjtor2[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIjtor3[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIjtor4[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIttor[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.szrIjtor[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrIjtor[index][-1].Add(self.txtIjtor2[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjtor[index][-1].Add(self.txtIjtor3[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjtor[index][-1].Add(self.txtIjtor4[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjtor[index][-1].Add(self.txtIttor[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrTorsions[index].Add(self.szrIjtor[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            elif l < old_value:
                for i in range(l, old_value):
                    self.szrTorsions[index].Remove(self.szrIjtor[index][-1])
                    self.txtIjtor2[index][-1].Destroy()
                    self.txtIjtor3[index][-1].Destroy()
                    self.txtIjtor4[index][-1].Destroy()
                    self.txtIttor[index][-1].Destroy()
                    self.txtIjtor2[index].pop()
                    self.txtIjtor3[index].pop()
                    self.txtIjtor4[index].pop()
                    self.txtIttor[index].pop()
                    self.szrIjtor[index].pop()

            self.tors[index].set_number_torsions(l)
            self.szrTorsions[index].Layout()
            self.szrEDAtoms[index].Layout()
            self.szrEDDialog.FitInside(self.swEDHolder)
            self.Refresh()
        return

    def InaaChanged(self, evt):
        index = self.InaaIDs.index(evt.GetId())
        l = self.txtInaa[index].GetValue()
        if l.isdigit():
            l = int(l)
            old_value = self.angles[index].get_number_angles()
            if l > old_value:
                for i in range(old_value, l):
                    self.txtIjaa0[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIjaa1[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIjaa2[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtItaa[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.szrIjaa[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrIjaa[index][-1].Add(self.txtIjaa0[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjaa[index][-1].Add(self.txtIjaa1[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjaa[index][-1].Add(self.txtIjaa2[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjaa[index][-1].Add(self.txtItaa[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrAngleAngles[index].Add(self.szrIjaa[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            elif l < old_value:
                for i in range(l, old_value):
                    self.szrAngleAngles[index].Remove(self.szrIjaa[index][-1])
                    self.txtIjaa0[index][-1].Destroy()
                    self.txtIjaa1[index][-1].Destroy()
                    self.txtIjaa2[index][-1].Destroy()
                    self.txtItaa[index][-1].Destroy()
                    self.txtIjaa0[index].pop()
                    self.txtIjaa1[index].pop()
                    self.txtIjaa2[index].pop()
                    self.txtItaa[index].pop()
                    self.szrIjaa[index].pop()

            self.angles[index].set_number_angles(l)
            self.szrAngleAngles[index].Layout()
            self.szrEDAtoms[index].Layout()
            self.szrEDDialog.FitInside(self.swEDHolder)
            self.Refresh()
        return

    def InimpropChanged(self, evt):
        index = self.InimpropIDs.index(evt.GetId())
        l = self.txtInimprop[index].GetValue()
        if l.isdigit():
            l = int(l)
            old_value = self.imptors[index].get_number_improper_torsions()
            if l > old_value:
                for i in range(old_value, l):
                    self.txtIjimprop2[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIjimprop3[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtIjimprop4[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.txtItimprop[index].append(wx.TextCtrl(self.swEDHolder, -1, "", size=(75,-1)))
                    self.szrIjimprop[index].append(wx.BoxSizer(wx.HORIZONTAL))
                    self.szrIjimprop[index][-1].Add(self.txtIjimprop2[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjimprop[index][-1].Add(self.txtIjimprop3[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjimprop[index][-1].Add(self.txtIjimprop4[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrIjimprop[index][-1].Add(self.txtItimprop[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
                    self.szrImproperTorsions[index].Add(self.szrIjimprop[index][-1], 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0)
            elif l < old_value:
                for i in range(l, old_value):
                    self.szrImproperTorsions[index].Remove(self.szrIjimprop[index][-1])
                    self.txtIjimprop2[index][-1].Destroy()
                    self.txtIjimprop3[index][-1].Destroy()
                    self.txtIjimprop4[index][-1].Destroy()
                    self.txtItimprop[index][-1].Destroy()
                    self.txtIjimprop2[index].pop()
                    self.txtIjimprop3[index].pop()
                    self.txtIjimprop4[index].pop()
                    self.txtItimprop[index].pop()
                    self.szrIjimprop[index].pop()

            self.imptors[index].set_number_improper_torsions(l)
            self.szrImproperTorsions[index].Layout()
            self.szrEDAtoms[index].Layout()
            self.szrEDDialog.FitInside(self.swEDHolder)
            self.Refresh()
        return

    def LPDBChanged(self, *args):
        l = self.rbLPDB.GetSelection()
        if l == 1:
            for i in range(self.nunit):
                self.szrEDAtoms[i].Hide(self.szrPdbname[i])
                self.szrEDAtoms[i].Hide(self.szrAminonum[i])
                self.szrEDAtoms[i].Hide(self.szrAminoshort[i])
        else:
            for i in range(self.nunit):
                self.szrEDAtoms[i].Show(self.szrPdbname[i])
                self.szrEDAtoms[i].Show(self.szrAminonum[i])
                self.szrEDAtoms[i].Show(self.szrAminoshort[i])

        for i in self.szrEDAtoms:
            i.Layout()

        self.szrEDDialog.FitInside(self.swEDHolder)
        self.szrEDDialog.Layout()
        return
# end of class ExplicitDeclaration
