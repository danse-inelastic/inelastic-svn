from vimm.vimmLib import simple_loader

import wx
import wx.grid
import os

class ZBuilder(wx.Frame):
    def __init__(self, parent, id,**kwds):
        # begin wxGlade: ZBuilder.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent,id,"ZBuilder", **kwds)

        self.parent = parent
        
        # Menu Bar
        self.ZBuilderMenubar = wx.MenuBar()
        self.SetMenuBar(self.ZBuilderMenubar)
        self.FileMenu = wx.Menu()
        ID_BUILD = wx.NewId()
        ID_IMPORT = wx.NewId()
        ID_EXPORT = wx.NewId()
        ID_CLOSE = wx.NewId()
        self.FileMenu.Append(ID_BUILD, "Build", "", wx.ITEM_NORMAL)
        self.FileMenu.Append(ID_IMPORT, "Import", "", wx.ITEM_NORMAL)
        self.FileMenu.Append(ID_EXPORT, "Export", "", wx.ITEM_NORMAL)
        self.FileMenu.Append(ID_CLOSE, "Close", "", wx.ITEM_NORMAL)
        self.ZBuilderMenubar.Append(self.FileMenu, "File")

        wx.EVT_MENU(self,ID_BUILD,self.build)
        wx.EVT_MENU(self,ID_IMPORT,self.zimport)
        wx.EVT_MENU(self,ID_EXPORT,self.zexport)
        wx.EVT_MENU(self,ID_CLOSE,self.close)
        
        # Menu Bar end
        self.grid = wx.grid.Grid(self, -1, size=(1, 1))

        self.__set_properties()
        self.__do_layout()
        
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ZBuilder.__set_properties
        self.SetTitle("ZBuilder")
        self.SetSize((400, 400))
        self.grid.CreateGrid(50, 7)
        self.grid.SetColLabelValue(0, "Atom")
        self.grid.SetColSize(0, 60)
        self.grid.SetColLabelValue(1, "I")
        self.grid.SetColSize(1, 30)
        self.grid.SetColLabelValue(2, "R")
        self.grid.SetColSize(2, 60)
        self.grid.SetColLabelValue(3, "J")
        self.grid.SetColSize(3, 30)
        self.grid.SetColLabelValue(4, "Angle")
        self.grid.SetColSize(4, 60)
        self.grid.SetColLabelValue(5, "K")
        self.grid.SetColSize(5, 30)
        self.grid.SetColLabelValue(6, "Torsion")
        self.grid.SetColSize(6, 60)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ZBuilder.__do_layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.grid, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
        # end wxGlade

    def close(self,*args): self.Close(True)
    def build(self,*args):
        nrows = self.grid.GetNumberRows()
        ncols = self.grid.GetNumberCols()

        vals = []
        for irow in range(nrows):
            row = []
            for icol in range(ncols):
                row.append(self.grid.GetCellValue(irow,icol))
            # Determine whether there are any nonblank values in row
            row = " ".join(row)
            words = row.split()
            if words:
                vals.append(words)

        if vals:
            geo = read_nwz(vals)
            material = simple_loader(geo)
            self.parent.material = material
            self.parent.render(1)
        return

    def zimport(self,*args): 
        fname = None
        d = wx.FileDialog(self,"Open","","","*",wx.OPEN)
        if d.ShowModal() == wx.ID_OK:
            fname = d.GetFilename()
            dir = d.GetDirectory()
            fullfilename = os.path.join(dir,fname)
        d.Destroy()
        if fname:
            zlines = getzlines(fname)
            zlist = getzlist(zlines)
            self.erase_all()
            nrows = len(zlist)
            self.insure_nrows(nrows) # Warning: broken; see below
            for irow in range(nrows):
                ncol = len(zlist[irow])
                for icol in range(ncol):
                    self.grid.SetCellValue(irow,icol,zlist[irow][icol])
            self.build()
        return

    def zexport(self,*args):
        nrows = self.grid.GetNumberRows()
        ncols = self.grid.GetNumberCols()
        vals = []
        for irow in range(nrows):
            row = []
            for icol in range(ncols):
                row.append(self.grid.GetCellValue(irow,icol))
            # Determine whether there are any nonblank values in row
            row = " ".join(row)
            words = row.split()
            if words:
                vals.append(words)
        if vals:
            for words in line:
                print words
        return        

    def erase_all(self):
        # Empty all cells
        nrows = self.grid.GetNumberRows()
        ncols = self.grid.GetNumberCols()
        for irow in range(nrows):
            for icol in range(ncols):
                self.grid.SetCellValue(irow,icol,'')
        return

    def insure_nrows(self,n):
        # Warning: This doesn't work. For some reason, it just
        #  inserts 1 row instead of diff rows
        nrows = self.grid.GetNumberRows()
        if n > nrows:
            diff = n-nrows
            self.grid.InsertRows(nrows-1,diff)
        return

# end of class ZBuilder


def getzlines(fname):
    # Grab the lines of a file delimited by "zmat" and "end"
    import re
    startpat = re.compile('^\s*zmat')
    endpat = re.compile('^\s*end')
    lines = []
    started = False
    for line in open(fname):
        if startpat.search(line):
            started = True
        elif started:
            if endpat.search(line):
                break
            lines.append(line)
    return lines

def getzlist(zlines):
    zlist = []
    for line in zlines:
        words = line.split()
        if words:
            zlist.append(words)
    return zlist

def read_nwz(zlist):
    from math import pi,sin,cos,sqrt
    deg2rad = pi/180.
    geo = []
    for words in zlist:
        sym = words[0]
        if len(words) == 0:
            continue
        elif len(words) == 1:
            # Atom at origin
            x=y=z=0
        elif len(words) == 3:
            # Atom along z-axis
            x=y=0
            iat = int(words[1])-1
            assert iat == 0
            r = float(words[2])
            z = r
        elif len(words) == 4:
            # This line contains a simple list of cartesian coordinates
            x,y,z = map(float,words[1:])
        elif len(words) == 5:
            # Atom in xy-plane
            y=0
            iat = int(words[1])-1
            r = float(words[2])
            jat = int(words[3])-1
            theta = float(words[4])*deg2rad
            x0,y0,z0 = geo[iat][1]
            x = x0+r*sin(theta)
            if iat == 0:
                z = z0 + r*cos(theta)
            else:
                z = z0 - r*cos(theta)
        else:
            # General case
            iat = int(words[1])-1
            r = float(words[2])
            jat = int(words[3])-1
            theta = float(words[4])*deg2rad
            kat = int(words[5])-1
            phi = float(words[6])*deg2rad
            xi,yi,zi = geo[iat][1]
            xj,yj,zj = geo[jat][1]
            xk,yk,zk = geo[kat][1]

            # Vector from iat -> jat
            xx = xj-xi
            yy = yj-yi
            zz = zj-zi
            rinv = 1/sqrt(xx*xx+yy*yy+zz*zz)
            xa = xx*rinv
            ya = yy*rinv
            za = zz*rinv

            # Vector from iat -> kat
            xb = xk-xi
            yb = yk-yi
            zb = zk-zi

            # Unit vector from iat -> kat
            xc = ya*zb - za*yb
            yc = za*xb - xa*zb
            zc = xa*yb - ya*xb
            rinv = 1/sqrt(xc*xc+yc*yc+zc*zc)
            xc *= rinv
            yc *= rinv
            zc *= rinv

            xb = yc*za - zc*ya
            yb = zc*xa - xc*za
            zb = xc*ya - yc*xa

            zz = r*cos(theta)
            xx = r*sin(theta)*cos(phi)
            yy = r*sin(theta)*sin(phi)

            x = xi + xa*zz + xb*xx + xc*yy
            y = yi + ya*zz + yb*xx + yc*yy
            z = zi + za*zz + zb*xx + zc*yy
            
        geo.append((sym,(x,y,z)))
    return geo

