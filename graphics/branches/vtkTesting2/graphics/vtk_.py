from graphics.common import *
import vtk, os

from graphics.numpytools import ravel, zeros, array, allclose, Float

#import vtk.util.colors


import wx
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
import wxPython.wx

import Tkinter
#from vtk.tk.vtkTkRenderWidget import vtkTkRenderWidget
from vtk.tk import vtkTkRenderWidget

class VtkBackend(BaseClass):
    """Backend using VTK"""

    def __init__(self, parent=None):
        BaseClass.__init__(self)
        self.parent = parent
        self.init()
        

    def init(self):
        self._master = None
        self.figure(self._attrs['curfig'])

        # convert tables for formatstrings
        self._colors = {
            '':  (0,0,1), # No color-->Blue
            'k': (0,0,0), # Black
            'r': (1,0,0), # Red 
            'g': (0,1,0), # Green
            'b': (0,0,1), # Blue
            'm': (1,0,1), # Magenta
            'c': (0,1,1), # Cyan
            'w': (1,1,1), # White
            'y': (1,1,0), # Yellow
            }

        self._arrow_types = { # tuple: (type,rotation)
            '':  (9,0),  # arrow
            '.': (0,0),  # no marker
            'o': (7,0),  # circle
            '+': (3,0),  # plus
            'x': (3,45), # x-mark
            '*': (3,0),  # star --> plus
            's': (6,0),  # square
            'd': (8,0),  # diamond
            'v': (5,180),# triangle (down) 
            '^': (5,0),  # triangle (up)
            '<': (5,90), # triangle (left) 
            '>': (5,270),# triangle (right)
            'p': (6,0),  # pentagram --> square
            'h': (6,0),  # hexagram --> square
            }

        self._colorbar_locations = {
            'North': ((.2, .75), (.6,.09)),
            'South': ((.2, .2), (.6, .09)),
            'East': ((.75, .09), (.1, .9)),
            'West': ((.2, .09), (.1, .9)),
            'NorthOutside': ((.2, .86), (.6,.09)),
            'SouthOutside': ((.2, .06), (.6, .09)),
            'EastOutside': ((.86, .09), (.1, .9)),
            'WestOutside': ((.01, .09), (.1, .9))
            }

        self._image_writers = {
            'tif': vtk.vtkTIFFWriter(),
            'bmp': vtk.vtkBMPWriter(),
            'pnm': vtk.vtkPNMWriter(),
            'ps': vtk.vtkPostScriptWriter(),
            'eps': vtk.vtkPostScriptWriter(),
            'png': vtk.vtkPNGWriter(),
            'jpg': vtk.vtkJPEGWriter(),
            }
        
        try:
            v = vtk.vtkMesaRenderer()
            _graphics_fact = vtk.vtkGraphicsFactory()
            _graphics_fact.SetUseMesaClasses(1)
            _image_fact = vtk.vtkImagingFactory()
            _image_fact.SetUseMesaClasses(1)
            del _graphics_fact
            del _image_fact
            del v
        except Exception, msg:
            print "No mesa", msg

    def _create_Tk_gui(self):
        fig = self.gcf()
        if self._master is None:
            self._master = Tkinter.Tk()
            self._master.withdraw()
        fig._root = Tkinter.Toplevel(self._master)
        fig._root.title("EasyViz Data Visualizer - Figure %d" % \
                        self._attrs['curfig'])
        # if the window is closed, we should delete the current figure and
        # create a new one.
        def _close_fig(event=None):
            self.clf()
            fig._root.withdraw()
        fig._root.protocol("WM_DELETE_WINDOW", _close_fig)
        fig._root.minsize(200, 200)
        fig._root.bind("<KeyPress-q>", _close_fig)
        fig._root.withdraw()
        master_f = Tkinter.Frame(fig._root, relief='sunken', bd=2)
        master_f.pack(side='top', fill='both', expand=1)
        renwin_frame = Tkinter.Frame(master_f)
        renwin_frame.pack(side='left', fill='both', expand=1)
        frame = Tkinter.Frame(renwin_frame)
        frame.pack(side='top', fill='both', expand=1)
        try:
            width, height = fig.get('size')
        except TypeError:
            width, height = (640, 480)
        tkw = vtkTkRenderWidget.vtkTkRenderWidget(frame, width=width, height=height)
        tkw.pack(expand='true', fill='both')
        renwin = tkw.GetRenderWindow()
        #renwin.SetSize(width, height)
        renwin.SetSize(width+1, height+1)
        #renwin.LineSmoothingOn()
        #tkw.UpdateRenderer(0.0, 0.0)
        #renwin.Render()
        return renwin
    
    def _create_wx_gui(self): # eventually change this so it invokes the main graphics panel
        # instead of this substitute
        # Make a frame to show it
        app = wx.PySimpleApp()
        frame = wx.Frame(None, wx.ID_ANY, "Graphics", size=(1110, 590))
        wxRW = wxVTKRenderWindow(frame, -1)
#        ren = vtk.vtkRenderer()
#        widget.GetRenderWindow().AddRenderer(ren) 

        # Layout the window
        pan=wx.Panel(frame,-1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wxRW, 1, wx.LEFT|wx.TOP|wx.GROW)
        pan.SetSizer(sizer) 

        frame.Show()
        app.MainLoop()

        return widget.GetRenderWindow()

    def _set_view_old(self):
        axis_cam = self._axis.get('camera')
        if not hasattr(self._axis, '_vtk_camera'):
            # initialize camera:
            pass
        else:
            # alter camera:
            pass
        camera = vtk.vtkCamera()
        self._axis._renderer.SetActiveCamera(camera)
        if axis_cam.get('camproj') == 'perspective':
            camera.ParallelProjectionOff()
        else:
            camera.ParallelProjectionOn()
        fp = axis_cam.get('camtarget')
        camera.SetFocalPoint(fp)
        camera.SetViewUp(axis_cam.get('camup'))
        if axis_cam.get('cammode') == 'auto':
            if axis_cam.get('view') == 3:
                camera.SetPosition(fp[0],fp[1]-1,fp[2])
                camera.Azimuth(-37.5)
                camera.Elevation(30)
            else:
                camera.SetPosition(fp[0], fp[1], 1)
        else:
            camera.SetPosition(axis_cam.get('campos'))
        #camera.ComputeViewPlaneNormal()
        #camera.OrthogonalizeViewUp()
        if axis_cam.get('camva') is not None:
            camera.SetViewAngle(axis_cam.get('camva'))
        azimuth = axis_cam.get('azimuth')
        if azimuth is not None:
            if axis_cam.get('view') == 3:
                azimuth += 37.5 # compensate for above
            camera.Azimuth(azimuth)
        elevation = axis_cam.get('elevation')
        if elevation is not None:
            if axis_cam.get('view') == 3:
                elevation -= 30 # compensate for above
            camera.Elevation(elevation)
        # make all actors fit inside the current scene:
        self._axis._renderer.ResetCamera()
        camera.Zoom(axis_cam.get('camzoom'))
        self._axis._vtk_camera = camera

    def _initialize_camera(self):
        ax_cam = self._axis.get('camera')
        camera = vtk.vtkCamera()
        fp = ax_cam.get('camtarget')
        camera.SetFocalPoint(fp)
        camera.SetViewUp(ax_cam.get('camup'))
        if ax_cam.get('cammode') == 'auto':
            if ax_cam.get('view') == 3:
                camera.SetPosition(fp[0],fp[1]-1,fp[2])
                camera.Azimuth(-37.5)
                camera.Elevation(30)
            else:
                camera.SetPosition(fp[0], fp[1], 1)
        else:
            camera.SetPosition(ax_cam.get('campos'))
        azimuth = ax_cam.get('azimuth')
        if azimuth is not None:
            if ax_cam.get('view') == 3:
                azimuth += 37.5 # compensate for above
            camera.Azimuth(azimuth)
        elevation = ax_cam.get('elevation')
        if elevation is not None:
            if ax_cam.get('view') == 3:
                elevation -= 30 # compensate for above
            camera.Elevation(elevation)

        return camera

    def _update_camera(self):
        ax_cam = self._axis.get('camera')
        camera = self._axis._vtk_camera
        return camera

    def _set_view(self):
        ax_cam = self._axis.get('camera')
        if not hasattr(self._axis, '_vtk_camera'):
            camera = self._initialize_camera()
        else:
            #camera = self._update_camera()
            camera = self._initialize_camera()

        if ax_cam.get('camroll') is not None:
            camera.Roll(ax_cam.get('camroll'))

        if ax_cam.get('camva') is not None:
            camera.SetViewAngle(ax_cam.get('camva'))
 
        if ax_cam.get('camproj') == 'perspective':
            camera.ParallelProjectionOff()
        else:
            camera.ParallelProjectionOn()
            
        self._axis._renderer.SetActiveCamera(camera)
        self._axis._vtk_camera = camera

        # make sure all actors are inside the current view:
        ren = self._axis._renderer
        ren.ResetCamera()
        if self._axis.get('camera').get('view') == 2:
            ren.GetActiveCamera().Zoom(1.5)
        camera.Zoom(ax_cam.get('camzoom'))
       
        # set the camera in the vtkCubeAxesActor2D object:
        self._axis._vtk_axes.SetCamera(camera)

    def _create_labeled_axes(self):
        ax = self._axis
        if not hasattr(ax, '_vtk_axes'):
            ax._vtk_axes = vtk.vtkCubeAxesActor2D()
        if ax.get('visible'):
            tprop = vtk.vtkTextProperty()
            tprop.SetColor(ax.get('fgcolor'))
            tprop.SetFontSize(ax.get('fontsize'))
            tprop.SetShadow(0)
            tprop.SetBold(0)
            mode = ax.get('mode')
            if mode in ['auto', 'tight']:
                dar = ax.get('daspect')
                bounds = b = list(ax._vtk_apd.GetOutput().GetBounds())
                if mode == 'auto':
                    incr = 0.1
                    dx = float(b[1] - b[0])
                    dy = float(b[3] - b[2])
                    dz = float(b[5] - b[4])
                    #b[0] -= dx*incr;  b[1] += dx*incr
                    #b[2] -= dy*incr;  b[3] += dy*incr
                    #b[4] -= dz*incr;  b[5] += dz*incr
                unscaled_bounds = ub = bounds[:]
                ub[0] *= dar[0];  ub[1] *= dar[0]
                ub[2] *= dar[1];  ub[3] *= dar[1]
                ub[4] *= dar[2];  ub[5] *= dar[2]
            elif mode == 'fill':
                print "axis mode 'fill' not implemented in VtkBackend"
            elif mode == 'manual':
                bounds = ax._vtk_scaled_bounds
                unscaled_bounds = ax._vtk_bounds
            #cube_axes = vtk.vtkCubeAxesActor2D()
            ax._vtk_axes.SetBounds(bounds)
            ax._vtk_axes.SetRanges(unscaled_bounds)
            ax._vtk_axes.UseRangesOn()
            #ax._vtk_axes.SetCamera(ax._vtk_camera)
            ax._vtk_axes.SetLabelFormat("%6.3g")
            ax._vtk_axes.SetFlyModeToOuterEdges()
            #ax._vtk_axes.SetFontFactor(ax.get('fontsize')/10.)
            ax._vtk_axes.ScalingOff()
            ax._vtk_axes.SetAxisTitleTextProperty(tprop)
            ax._vtk_axes.SetAxisLabelTextProperty(tprop)
            ax._vtk_axes.GetProperty().SetColor(ax.get('fgcolor'))
            ax._vtk_axes.SetCornerOffset(0)
            ax._vtk_axes.SetNumberOfLabels(5)
            ax._vtk_axes.SetXLabel(ax.get('xlabel'))
            ax._vtk_axes.SetYLabel(ax.get('ylabel'))
            ax._vtk_axes.SetZLabel(ax.get('zlabel'))
            if ax.get('camera').get('view') == 2:
                ax._vtk_axes.YAxisVisibilityOff()
            else:
                ax._vtk_axes.YAxisVisibilityOn()
            ax._renderer.AddActor(ax._vtk_axes)
            ax._vtk_box_bounds = bounds

    def _set_box_state(self):
        ax = self._axis
        if not hasattr(ax, '_vtk_box'):
            ax._vtk_box = vtk.vtkActor()
        # remove old box (if present):
        if ax._renderer.GetActors().IsItemPresent(ax._vtk_box):
            ax._renderer.RemoveActor(ax._vtk_box)
        if ax.get('box'):
            box = vtk.vtkCubeSource()
            #box.SetBounds(ax._vtk_scaled_bounds)
            box.SetBounds(ax._vtk_box_bounds)
            box.Update()
            outline = vtk.vtkOutlineFilter()
            outline.SetInput(box.GetOutput())
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(outline.GetOutput())
            ax._vtk_box.SetMapper(mapper)
            ax._vtk_box.GetProperty().SetColor(ax.get('fgcolor'))
            ax._renderer.AddActor(ax._vtk_box)

    def _set_colormap(self):
        colormap = self._axis.get('colormap')
        if not isinstance(colormap, vtk.vtkLookupTable):
            colormap = self.jet() # use default colormap
        self._axis._vtk_colormap = colormap

    def _set_colorbar(self):
        ax = self._axis
        cbar = ax.get('colorbar')

        if not hasattr(ax, '_vtk_colorbar'):
            ax._vtk_colorbar = vtk.vtkScalarBarActor()
        if ax._renderer.GetActors().IsItemPresent(ax._vtk_colorbar):
            ax._renderer.RemoveActor2D(ax._vtk_colorbar)
        if cbar.get('visible'):
            cblocation = cbar.get('cblocation')
            cbloc = self._colorbar_locations[cblocation]
            ax._vtk_colorbar.SetLookupTable(ax._vtk_colormap)
            if 'North' in cblocation or 'South' in cblocation:
                ax._vtk_colorbar.SetOrientationToHorizontal()
            else:
                ax._vtk_colorbar.SetOrientationToVertical()
            ax._vtk_colorbar.SetTitle(cbar.get('cbtitle'))
            ax._vtk_colorbar.SetPosition(*cbloc[0])
            ax._vtk_colorbar.SetPosition2(*cbloc[1])
            tprop = vtk.vtkTextProperty()
            tprop.SetColor(ax.get('fgcolor'))
            tprop.SetFontSize(ax.get('fontsize'))
            tprop.ShadowOff()
            ax._vtk_colorbar.SetTitleTextProperty(tprop)
            ax._vtk_colorbar.SetLabelTextProperty(tprop)
            ax._renderer.AddActor(ax._vtk_colorbar)

    def _set_shading(self, item, source, actor):
        shading = self._axis.get('shading')
        if shading == 'interp':
            actor.GetProperty().SetInterpolationToGouraud()
        elif shading == 'flat':
            actor.GetProperty().SetInterpolationToFlat()
        else: # use default shading ('faceted')
            actor.GetProperty().SetInterpolationToFlat()
            edges = vtk.vtkExtractEdges()
            edges.SetInput(source.GetOutput())
            edges.Update()
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(edges.GetOutput())
            mapper.ScalarVisibilityOff()
            mapper.SetResolveCoincidentTopologyToPolygonOffset()
            mesh = vtk.vtkActor()
            mesh.SetMapper(mapper)
            color = item.get('linecolor')
            if color == '' or color is None:
                color = (0,0,0) # use black as default
            elif not isinstance(color, (tuple,list)):
                try: color = self._colors[color]
                except: color = (0,0,0) # use black as default
            mesh.GetProperty().SetColor(color)
            self._axis._renderer.AddActor(mesh)

    def _set_title(self):
        tprop = vtk.vtkTextProperty()
        tprop.BoldOff()
        tprop.SetFontSize(self._axis.get('fontsize'))
        tprop.SetColor(self._axis.get('fgcolor'))
        tprop.SetFontFamilyToArial()
        tprop.SetVerticalJustificationToTop()
        tprop.SetJustificationToCentered()
	mapper = vtk.vtkTextMapper()
        mapper.SetInput(self._axis.get('title'))
        mapper.SetTextProperty(tprop)
	actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        actor.GetPositionCoordinate().SetCoordinateSystemToView()
        actor.GetPositionCoordinate().SetValue(0.0, 0.95)
        self._axis._renderer.AddActor(actor)

    def _set_caxis(self):
        if self._axis.get('caxismode') == 'auto':
            caxis = None
        else:
            caxis = self._axis.get('caxis')
        self._axis._vtk_caxis = caxis
        
    def _data_inside_bounds(self, data):
        fb = self._axis._vtk_scaled_bounds
        bounds = data.GetBounds()
        for i in range(0, len(fb), 2):
            if bounds[i] < fb[i] and not allclose(bounds[i],fb[i]):
                return False
        for i in range(1, len(fb), 2):
            if bounds[i] > fb[i] and not allclose(bounds[i],fb[i]):
                return False
        return True

    def _cut_data(self, indata):
        if self._data_inside_bounds(indata.GetOutput()):
            return indata
        box = vtk.vtkBox()
        box.SetBounds(self._axis._vtk_scaled_bounds)
        clipper = vtk.vtkClipPolyData()
        clipper.SetInput(indata.GetOutput())
        clipper.SetClipFunction(box)
        #clipper.GenerateClipScalarsOn()
        #clipper.GenerateClippedOutputOn()
        clipper.SetValue(0.0)
        clipper.InsideOutOn()
        clipper.Update()
        return clipper

    def _add_slices(self, item, sgrid, contours=False):
        cvector = item.get('cvector')
        center = sgrid.GetCenter()
        dar = self._axis.get('daspect')
        sx, sy, sz = item.get('slices')
        if len(shape(sx)) == 2 and shape(sx) == shape(sy) == shape(sz):
            s = Surface(sx,sy,sz)
            sgrid2 = self._get_2d_structured_grid(s)
            plane = vtk.vtkStructuredGridGeometryFilter()
            plane.SetInput(sgrid2)
            plane.Update()
            data = self._cut_data(plane)
            implds = vtk.vtkImplicitDataSet()
            implds.SetDataSet(data.GetOutput())
            implds.Modified()
            cut = vtk.vtkCutter()
            cut.SetInput(sgrid)
            cut.SetCutFunction(implds)
            cut.GenerateValues(10, -2,2)
            cut.GenerateCutScalarsOn()
            cut.Update()
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(cut.GetOutput())
            mapper.SetLookupTable(self._axis._vtk_colormap)
            caxis = self._axis.get('caxis')
            if None in caxis:
                caxis = data.GetOutput().GetScalarRange()
            mapper.SetScalarRange(caxis)
            mapper.Update()
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            self._set_shading(item, data, actor)
            self._set_actor_properties(item, actor)
            self._axis._renderer.AddActor(actor)
            self._axis._vtk_apd.AddInput(cut.GetOutput())
            self._axis._vtk_apd.AddInput(data.GetOutput())
        else:
            origins = []
            normals = []
            sx = ravel(sx)/dar[0]
            sy = ravel(sy)/dar[1]
            sz = ravel(sz)/dar[2]
            for i in range(len(sx)):
                normals.append([1,0,0])
                origins.append([sx[i]/dar[0], center[1], center[2]])
            for i in range(len(sy)):
                normals.append([0,1,0])
                origins.append([center[0], sy[i]/dar[1], center[2]])
            for i in range(len(sz)):
                normals.append([0,0,1])
                origins.append([center[0], center[1], sz[i]/dar[2]])
            for i in range(len(normals)):
                plane = vtk.vtkPlane()
                plane.SetOrigin(origins[i])
                plane.SetNormal(normals[i])
                cut = vtk.vtkCutter()
                cut.SetInput(sgrid)
                cut.SetCutFunction(plane)
                cut.Update()
                data = self._cut_data(cut)
                mapper = vtk.vtkPolyDataMapper()
                if contours:
                    iso = vtk.vtkContourFilter()
                    iso.SetInput(data.GetOutput())
                    if cvector is not None:
                        for i in range(len(cvector)):
                            iso.SetValue(i, cvector[i])
                    else:
                        zmin, zmax = data.GetOutput().GetScalarRange()
                        iso.GenerateValues(item.get('clevels'), zmin, zmax)
                    iso.Update()
                    mapper.SetInput(iso.GetOutput())
                else:
                    mapper.SetInput(data.GetOutput())
                mapper.SetLookupTable(self._axis._vtk_colormap)
                caxis = self._axis.get('caxis')
                if None in caxis:
                    caxis = sgrid.GetScalarRange()
                mapper.SetScalarRange(caxis)
                mapper.Update()
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                if not contours:
                    self._set_shading(item, data, actor)
                self._set_actor_properties(item, actor)
                self._axis._renderer.AddActor(actor)
                self._axis._vtk_apd.AddInput(cut.GetOutput())

    def _add_isosurface(self, item, sgrid):
        iso = vtk.vtkContourFilter()
        iso.SetInput(sgrid)
        iso.SetValue(0, item.get('isovalue'))
        iso.Update()
        data = self._cut_data(iso)
        normals = vtk.vtkPolyDataNormals()
        normals.SetInput(data.GetOutput())
        normals.SetFeatureAngle(45)
        normals.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(normals.GetOutput())
        mapper.SetLookupTable(self._axis._vtk_colormap)
        caxis = self._axis.get('caxis')
        if None in caxis:
            caxis = sgrid.GetScalarRange()
        mapper.SetScalarRange(caxis)
        mapper.Update()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self._set_shading(item, data, actor)
        self._set_actor_properties(item, actor)
        self._axis._renderer.AddActor(actor)
        self._axis._vtk_apd.AddInput(normals.GetOutput())

    def _get_2d_structured_grid(self, item, vectors=False,
                                heights=True, bottom=False):
        dar = self._axis.get('daspect')
        x = asarray(item.get('xdata'))/dar[0]
        y = asarray(item.get('ydata'))/dar[1]
        sgrid = vtk.vtkStructuredGrid()
        sgrid.SetDimensions(item.get('dims'))
        no_points = item.get('numberofpoints')
        points = vtk.vtkPoints()
        points.SetNumberOfPoints(no_points)
        if vectors:
            x = ravel(x)
            y = ravel(y)
            u = asarray(item.get('udata'))
            v = ravel(item.get('vdata'))
            w = ravel(item.get('wdata'))
            z = ravel(item.get('zdata'))
            if item.get('function') == 'quiver3':
                z = z/dar[2]
            if len(shape(u)) == 2:
                nx, ny = shape(u)
                if len(x) == nx:
                    x = ravel(x[:,NewAxis]*ones((1,ny)))
                if len(y) == ny:
                    y = ravel(y[NewAxis,:]*ones((nx,1)))
            u = ravel(u)
            vectors = vtk.vtkFloatArray()
            vectors.SetNumberOfTuples(no_points)
            vectors.SetNumberOfComponents(3)
            vectors.SetNumberOfValues(3*no_points)
            assert shape(x)==shape(y)==shape(z)==shape(u)==shape(v)==shape(w),\
                   "matrix dimensions must agree"
            for i in range(no_points):
                points.SetPoint(i, x[i], y[i], z[i])
                vectors.SetTuple3(i, u[i], v[i], w[i])
            points.Modified()
            sgrid.SetPoints(points)
            sgrid.GetPointData().SetVectors(vectors)
        else:
            values = asarray(item.get('zdata'))
            if heights:
                z = values/dar[2]
            elif bottom:
                z = zeros(values.shape, dtype=values.dtype) + \
                    self._axis._vtk_scaled_bounds[4]
            else:
                z = zeros(values.shape, dtype=values.dtype)
            try:
                cdata = asarray(item.get('cdata'))
            except KeyError:
                pass
            else:
                if cdata is not None and cdata.shape == values.shape:
                    values = cdata
            scalars = vtk.vtkFloatArray()
            scalars.SetNumberOfTuples(no_points)
            scalars.SetNumberOfComponents(1)
            nx, ny = shape(values)
            if shape(x) == (nx,) and shape(y) == (ny,):
                x = x[:,NewAxis]
                y = y[NewAxis,:]
            if shape(x) == (nx,1) and shape(y) == (1,ny):
                x = x*ones((1,ny))
                y = y*ones((nx,1))
            assert shape(x) == shape(y) == shape(z), \
                   "array dimensions must agree"
            ind = 0
            for j in range(ny):
                for i in range(nx):
                    points.SetPoint(ind, x[i,j], y[i,j], z[i,j])
                    scalars.SetValue(ind, values[i,j])
                    ind += 1
            points.Modified()
            sgrid.SetPoints(points)
            sgrid.GetPointData().SetScalars(scalars)

        sgrid.Update()
        return sgrid

    def _get_3d_structured_grid(self, item, vectors=False):
        dar = self._axis.get('daspect')
        x = asarray(item.get('xdata'))/dar[0]
        y = asarray(item.get('ydata'))/dar[1]
        z = asarray(item.get('zdata'))/dar[2]
        sgrid = vtk.vtkStructuredGrid()
        sgrid.SetDimensions(item.get('dims'))
        no_points = item.get('numberofpoints')
        points = vtk.vtkPoints()
        points.SetNumberOfPoints(no_points)
        if vectors:
            u = asarray(item.get('udata'))
            v = asarray(item.get('vdata'))
            w = asarray(item.get('wdata'))
            nx, ny, nz = shape(u)
            if shape(x) == (nx,) and shape(y) == (ny,):
                x = x[:,NewAxis,NewAxis]
                y = y[NewAxis,:,NewAxis]
            if shape(x) == (nx,1,1) and shape(y) == (1,ny,1):
                x = x*ones((1,ny,nz))
                y = y*ones((nx,1,nz))
            if shape(z) == (1,1,nz):
                z = z*ones((nx,ny,1))
            assert shape(x) == shape(y) == shape(z) == \
                   shape(u) == shape(v) == shape(w), \
                   "array dimensions must agree"
                
            vectors = vtk.vtkFloatArray()
            vectors.SetNumberOfTuples(no_points)
            vectors.SetNumberOfComponents(3)
            vectors.SetNumberOfValues(3*no_points)

            ind = 0
            for k in range(nz):
                for j in range(ny):
                    for i in range(nx):
                        points.SetPoint(ind, x[i,j,k], y[i,j,k], z[i,j,k])
                        vectors.SetTuple3(ind, u[i,j,k], v[i,j,k], w[i,j,k])
                        ind += 1
            points.Modified()
            sgrid.SetPoints(points)
            sgrid.GetPointData().SetVectors(vectors)
        else:
            scalars = vtk.vtkFloatArray()
            scalars.SetNumberOfTuples(no_points)
            scalars.SetNumberOfComponents(1)
            
            v = asarray(item.get('vdata'))
            # TODO: what about pseudocolor data?
            #cdata = ravel(item.get('cdata'))
            #if cdata is not None:
            #    v = cdata
            nx, ny, nz = shape(v)
            if shape(x) == (nx,) and shape(y) == (ny,) and shape(z) == (nz,):
                x = x[:,NewAxis,NewAxis]
                y = y[NewAxis,:,NewAxis]
                z = z[NewAxis,NewAxis,:]
            if shape(x) == (nx,1,1) and \
                   shape(y) == (1,ny,1) and shape(z) == (1,1,nz):
                x = x*ones((1,ny,nz))
                y = y*ones((nx,1,nz))
                z = z*ones((nx,ny,1))
            ind = 0
            for k in range(nz):
                for j in range(ny):
                    for i in range(nx):
                        points.SetPoint(ind, x[i,j,k], y[i,j,k], z[i,j,k])
                        scalars.SetValue(ind, v[i,j,k])
                        ind += 1
            points.Modified()
            sgrid.SetPoints(points)
            sgrid.GetPointData().SetScalars(scalars)
            
        sgrid.Update()
        return sgrid

    def _add_surface(self, item, sgrid):
        plane = vtk.vtkStructuredGridGeometryFilter()
        plane.SetInput(sgrid)
        plane.Update()
        data = self._cut_data(plane)
        normals = vtk.vtkPolyDataNormals()
        normals.SetInput(data.GetOutput())
        normals.SetFeatureAngle(45)
        normals.Update()
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInput(normals.GetOutput())
        mapper.SetLookupTable(self._axis._vtk_colormap)
        caxis = self._axis.get('caxis')
        if None in caxis:
            caxis = data.GetOutput().GetScalarRange()
        mapper.SetScalarRange(caxis)
        mapper.Update()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        if item.get('wireframe'):
            actor.GetProperty().SetRepresentationToWireframe()
        else:
            self._set_shading(item, data, actor)
        self._set_actor_properties(item, actor)
        self._add_legend(item, normals.GetOutput())
        self._axis._renderer.AddActor(actor)
        self._axis._vtk_apd.AddInput(normals.GetOutput())
        
    def _add_contours(self, item, sgrid):
        plane = vtk.vtkStructuredGridGeometryFilter()
        plane.SetInput(sgrid)
        plane.Update()
        data = self._cut_data(plane)
        filled = item.get('filled')
        if filled:
            iso = vtk.vtkBandedPolyDataContourFilter()
            iso.SetScalarModeToValue()
            iso.GenerateContourEdgesOn()
        else:
            iso = vtk.vtkContourFilter()
        iso.SetInput(data.GetOutput())
        clevels = item.get('clevels')
        cvector = item.get('cvector')
        if cvector is not None:
            for i in range(clevels):
                iso.SetValue(i, cvector[i])
        else:
            zmin, zmax = data.GetOutput().GetScalarRange()
            iso.SetNumberOfContours(clevels)
            iso.GenerateValues(clevels, zmin, zmax)
        iso.Update()
        isoMapper = vtk.vtkPolyDataMapper()
        isoMapper.SetInput(iso.GetOutput())
        isoMapper.SetLookupTable(self._axis._vtk_colormap)
        caxis = self._axis.get('caxis')
        if None in caxis:
            caxis = data.GetOutput().GetScalarRange()
        isoMapper.SetScalarRange(caxis)
        if item.get('linecolor'): # linecolor is defined:
            isoMapper.ScalarVisibilityOff()
        isoMapper.Update()
        isoActor = vtk.vtkActor()
        isoActor.SetMapper(isoMapper)
        self._set_actor_properties(item, isoActor)
        self._add_legend(item, iso.GetOutput())
        self._axis._renderer.AddActor(isoActor)
        self._axis._vtk_apd.AddInput(data.GetOutput())

        if filled: # create contour edges:
            edgeMapper = vtk.vtkPolyDataMapper()
            edgeMapper.SetInput(iso.GetContourEdgesOutput())
            edgeMapper.SetResolveCoincidentTopologyToPolygonOffset()
            edgeActor = vtk.vtkActor()
            edgeActor.SetMapper(edgeMapper)
            edgeActor.GetProperty().SetColor(0, 0, 0)
            self._axis._renderer.AddActor(edgeActor)

        if item.get('clabels'):
            # subsample the points and label them:
            mask = vtk.vtkMaskPoints()
            mask.SetInput(iso.GetOutput())
            mask.SetOnRatio(data.GetOutput().GetNumberOfPoints()/50)
            mask.SetMaximumNumberOfPoints(50)
            mask.RandomModeOn()

            # Create labels for points - only show visible points
            visPts = vtk.vtkSelectVisiblePoints()
            visPts.SetInput(mask.GetOutput())
            visPts.SetRenderer(self._axis._renderer)
            ldm = vtk.vtkLabeledDataMapper()
            ldm.SetInput(mask.GetOutput())
            ldm.SetLabelFormat("%.1g")
            ldm.SetLabelModeToLabelScalars()
            tprop = ldm.GetLabelTextProperty()
            tprop.SetFontFamilyToArial()
            tprop.SetFontSize(10)
            tprop.SetColor(0,0,0)
            tprop.ShadowOff()
            tprop.BoldOff()
            contourLabels = vtk.vtkActor2D()
            contourLabels.SetMapper(ldm)
            self._axis._renderer.AddActor(contourLabels)

    def _add_velocity_vectors(self, item, sgrid):
        marker, rotation = self._arrow_types[item.get('linemarker')]
        arrow = vtk.vtkGlyphSource2D()
        arrow.SetGlyphType(marker)
        arrow.SetFilled(item.get('filledarrows'))
        arrow.SetRotationAngle(rotation)
        if arrow.GetGlyphType() != 9: # not an arrow
            arrow.DashOn()
            arrow.SetCenter(.75,0,0)
        else:
            arrow.SetCenter(.5,0,0)        
        arrow.SetColor(self._colors[item.get('linecolor')])

        plane = vtk.vtkStructuredGridGeometryFilter()
        plane.SetInput(sgrid)
        plane.Update()
        data = self._cut_data(plane)
        glyph = vtk.vtkGlyph3D()
        glyph.SetInput(data.GetOutput()) 
        glyph.SetSource(arrow.GetOutput())
        glyph.SetColorModeToColorByVector()
        glyph.SetRange(data.GetOutput().GetScalarRange())
        glyph.ScalingOn()
        glyph.SetScaleModeToScaleByVector()
        glyph.OrientOn()
        glyph.SetVectorModeToUseVector()
        glyph.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(glyph.GetOutput())
        #vr = data.GetOutput().GetPointData().GetVectors().GetRange()
        #mapper.SetScalarRange(vr)
        mapper.ScalarVisibilityOff()
        mapper.Update()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self._set_actor_properties(item, actor)
        self._add_legend(item, arrow.GetOutput())
        self._axis._renderer.AddActor(actor)
        self._axis._vtk_apd.AddInput(glyph.GetOutput())

    def _add_streams(self, item, sgrid):
        length = sgrid.GetLength()
        max_velocity = sgrid.GetPointData().GetVectors().GetMaxNorm()
        max_time = 35.0*length/max_velocity
        
        n = item.get('numberofstreams')
        sx = ravel(item.get('startx'))
        sy = ravel(item.get('starty'))
        sz = ravel(item.get('startz'))
        dar = self._axis.get('daspect')
        for i in range(n):
            integ = vtk.vtkRungeKutta2() # or 4?
            stream = vtk.vtkStreamLine()
            stream.SetInput(sgrid)
            stream.SetStepLength(item.get('stepsize'))
            #stream.SetIntegrationStepLength(item.get('stepsize'))
            #stream.SetIntegrationDirectionToIntegrateBothDirections()
            stream.SetIntegrationDirectionToForward()
            #stream.SetMaximumPropagationTime(max_time)
            #stream.SetMaximumPropagationTime(200)
            stream.SpeedScalarsOn()
            #stream.VorticityOn()
            stream.SetStartPosition(sx[i]/dar[0], sy[i]/dar[1], sz[i]/dar[2])
            stream.SetIntegrator(integ)
            stream.Update()
            data = self._cut_data(stream)
            if item.get('ribbons'):
                streamribbon = vtk.vtkRibbonFilter()
                streamribbon.SetInput(data.GetOutput())
                streamribbon.VaryWidthOn()
                streamribbon.SetWidthFactor(item.get('ribbonwidth'))
                streamribbon.Update()
                output = streamribbon.GetOutput()
            elif item.get('tubes'):
                streamtube = vtk.vtkTubeFilter()
                streamtube.SetInput(data.GetOutput())
                streamtube.SetRadius(0.02)
                streamtube.SetNumberOfSides(item.get('n'))
                streamtube.SetVaryRadiusToVaryRadiusByVector()
                streamtube.Update()
                output = streamtube.GetOutput()
            else:
                output = data.GetOutput()
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(output)
            mapper.SetLookupTable(self._axis._vtk_colormap)
            caxis = self._axis.get('caxis')
            if None in caxis:
                caxis = output.GetBounds()[4:]
                #caxis = sgrid.GetScalarRange()
            mapper.SetScalarRange(caxis)
            mapper.Update()
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            #self._set_shading(item, stream, actor)
            self._set_actor_properties(item, actor)
            self._add_legend(item, output)
            self._axis._renderer.AddActor(actor)
            self._axis._vtk_apd.AddInput(output)
            
    def _add_line(self, item):
        dar = self._axis.get('daspect')
        n = item.get('numberofpoints')
        polydata = vtk.vtkPolyData()
        polydata.SetLines(vtk.vtkCellArray()) 
        points = vtk.vtkPoints()
        #points.SetNumberOfPoints(n)
        x = ravel(item.get('xdata'))/dar[0]
        y = ravel(item.get('ydata'))/dar[1]
        z = item.get('zdata')
        if z is not None:
            z = ravel(z)/dar[2]
        else:
            z = zeros(n, x.dtype)
        ids = vtk.vtkIdList()
        for i in range(1,n):
            points.InsertNextPoint(x[i-1], y[i-1], z[i-1])
            ids.InsertNextId(i-1)
            ids.InsertNextId(i)
            polydata.InsertNextCell(3, ids)
        points.InsertNextPoint(x[n-1], y[n-1], z[n-1]) # last point
        polydata.SetPoints(points)
        polydata.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(polydata)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self._set_actor_properties(item, actor)
        self._add_legend(item, polydata)
        self._axis._renderer.AddActor(actor)
        self._axis._vtk_apd.AddInput(polydata)

    def _set_actor_properties(self, item, actor):
        # set line properties:
        color = item.get('linecolor')
        if not isinstance(color, (tuple,list)):
            try: color = self._colors[color]
            except: color = (0,0,1) # use blue as default
        actor.GetProperty().SetColor(color)
        if item.get('linetype') == '--':
            actor.GetProperty().SetLineStipplePattern(65280)
        elif item.get('linetype') == ':':
            actor.GetProperty().SetLineStipplePattern(0x1111)
            actor.GetProperty().SetLineStippleRepeatFactor(1)
        actor.GetProperty().SetPointSize(item.get('pointsize'))
        linewidth = item.get('linewidth')
        if linewidth:
            actor.GetProperty().SetLineWidth(linewidth)
        
        # set material properties:
        ax = self._axis
        mat = item.get('material')
        if mat.get('opacity') is not None:
            actor.GetProperty().SetOpacity(mat.get('opacity'))
        if mat.get('ambient') is not None:
            actor.GetProperty().SetAmbient(mat.get('ambient'))
        if ax.get('ambientcolor') is not None:
            actor.GetProperty().SetAmbientColor(ax.get('ambientcolor'))
        if mat.get('diffuse') is not None:
            actor.GetProperty().SetDiffuse(mat.get('diffuse'))
        if ax.get('diffusecolor') is not None:
            actor.GetProperty().SetDiffuseColor(ax.get('diffusecolor'))
        if mat.get('specular') is not None:
            actor.GetProperty().SetSpecular(mat.get('specular'))
        if mat.get('specularpower') is not None:
            actor.GetProperty().SetSpecularPower(mat.get('specularpower'))

    def _set_grid(self):
        if not self._axis.get('visible') or not self._axis.get('grid'):
            return
        b = self._axis._vtk_box_bounds #self._axis._vtk_scaled_bounds
        if self._axis.get('camera').get('view') == 3:
            origins = [[b[0],b[2],b[4]], [b[0],b[3],b[4]], [b[1],b[2],b[4]]]
            points1 = [[b[1],b[2],b[4]], [b[0],b[3],b[5]], [b[1],b[2],b[5]]]
            points2 = [[b[0],b[3],b[4]], [b[1],b[3],b[4]], [b[1],b[3],b[4]]]
        else:
            origins = [[b[0],b[2],0]]
            points1 = [[b[0],b[3],0]]
            points2 = [[b[1],b[2],0]]
        for i in range(len(origins)):
            plane = vtk.vtkPlaneSource()
            plane.SetResolution(4, 4)
            plane.SetOrigin(origins[i])
            plane.SetPoint1(points1[i])
            plane.SetPoint2(points2[i])
            plane.Update()
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(plane.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(0,0,0)
            actor.GetProperty().SetRepresentationToWireframe()
            actor.GetProperty().SetLineStipplePattern(0x1111)
            actor.GetProperty().SetLineStippleRepeatFactor(1)
            self._axis._renderer.AddActor(actor)

    def _create_vtk_data(self):
        for item in self._axis.get('plotitems'):
            func = item.get('function')
            if isinstance(item, Line):
                self._add_line(item)
            elif isinstance(item, Surface):
                if func == 'pcolor':
                    sgrid = self._get_2d_structured_grid(item, heights=False)
                else:
                    sgrid = self._get_2d_structured_grid(item)
                self._add_surface(item, sgrid)
                citem = item.get('contours')
                if isinstance(citem, Contours):
                    csgrid = self._get_2d_structured_grid(citem, heights=False,
                                                          bottom=True)
                    self._add_contours(citem, csgrid)
            elif isinstance(item, Contours):
                if item.get('clocation') == 'surface':
                    sgrid = self._get_2d_structured_grid(item)
                else:
                    sgrid = self._get_2d_structured_grid(item, heights=False)
                self._add_contours(item, sgrid)
            elif isinstance(item, VelocityVectors):
                if len(item.get('udata').shape) == 3:
                    sgrid = self._get_3d_structured_grid(item, vectors=True)
                else:
                    sgrid = self._get_2d_structured_grid(item, vectors=True)
                self._add_velocity_vectors(item, sgrid)
            elif isinstance(item, Streams):
                if len(item.get('udata').shape) == 3: 
                    sgrid = self._get_3d_structured_grid(item, vectors=True)
                else:
                    sgrid = self._get_2d_structured_grid(item, vectors=True)
                self._add_streams(item, sgrid)
            elif isinstance(item, Volume):
                sgrid = self._get_3d_structured_grid(item)
                contours = func == 'contourslice'
                if func in ['slice_', 'contourslice']:
                    self._add_slices(item, sgrid, contours=contours)
                elif func == 'isosurface':
                    self._add_isosurface(item, sgrid)
            else:
                raise NotImplementedError, '%s not yet implemented' % item

            self._axis._vtk_apd.Update()

    def _add_legend(self, item, polydata):
        legend = item.get('legend')
        if legend:
            ax = self._axis
            n = ax._vtk_nolegends
            ax._vtk_nolegends += 1
            ax._vtk_legendbox.SetNumberOfEntries(ax._vtk_nolegends)
            ax._vtk_legendbox.SetEntrySymbol(n, polydata)
            ax._vtk_legendbox.SetEntryString(n, legend)
            color = self._colors[item.get('linecolor')]
            ax._vtk_legendbox.SetEntryColor(n, color)#ax.get('fgcolor'))

    def _set_legends(self):
        ax = self._axis
        n = ax._vtk_nolegends
        if n > 0:
            ax._vtk_legendbox.SetNumberOfEntries(n)
            #ax._vtk_legendbox.ScalarVisibilityOff()
            #ax._vtk_legendbox.BorderOff()
            ax._vtk_legendbox.GetPositionCoordinate().SetValue(0.8, 0.2, 0)
            ax._vtk_legendbox.GetPosition2Coordinate().SetValue(.2, n*.1, 0)
            ax._vtk_legendbox.GetProperty().SetColor(ax.get('fgcolor'))
            ax._renderer.AddActor(ax._vtk_legendbox)

    def _set_lights(self):
        if not hasattr(self._axis, '_vtk_lights'):
            self._axis._vtk_lights = []
        else: # remove all lights (if any)
            for l in self._axis._vtk_lights:
                self._axis._renderer.RemoveLight(l)
            self._axis._vtk_lights = []
        for l in self._axis.get('lights'):
            light = vtk.vtkLight()
            light.SetColor(l.get('lightcolor'))
            light.SetFocalPoint(l.get('lighttarget'))
            light.SetPosition(l.get('lightpos'))
            self._axis._renderer.AddLight(light)
            self._axis._vtk_lights.append(light)

    def _setup_axis(self):
        ax = self._axis
        xmin, xmax = ax.get('xmin'), ax.get('xmax')
        if None in [xmin, xmax]:
            xmin, xmax = ax.get('xlim')
        ymin, ymax = ax.get('ymin'), ax.get('ymax')
        if None in [ymin, ymax]:
            ymin, ymax = ax.get('ylim')
        zmin, zmax = ax.get('zmin'), ax.get('zmax')
        if None in [zmin, zmax]:
            zmin, zmax = ax.get('zlim')
        bnds = [xmin, xmax, ymin, ymax, zmin, zmax]
        ax._vtk_bounds = bnds[:]
        # scale axis:
        dar = ax.get('daspect')
        bnds[0] = bnds[0]/dar[0];  bnds[1] = bnds[1]/dar[0]
        bnds[2] = bnds[2]/dar[1];  bnds[3] = bnds[3]/dar[1]
        bnds[4] = bnds[4]/dar[2];  bnds[5] = bnds[5]/dar[2]
        ax._vtk_scaled_bounds = bnds[:]

##         fig = self.gcf()
##         # clean up:
##         if hasattr(ax, '_renderer'):
##             self._g.RemoveRenderer(ax._renderer)
##             if ax._renderer in fig._renderers:
##                 fig._renderers.remove(ax._renderer)
##             del ax._renderer
        
##         ax._renderer = vtk.vtkRenderer()
##         self._g.AddRenderer(ax._renderer)
##         # add this new renderer to the current figures list of renderers
##         # so we can remove it later (e.g. when using clf()):
##         fig._renderers.append(ax._renderer)

        if not hasattr(ax, '_renderer'):
            ax._renderer = vtk.vtkRenderer()
            self._g.AddRenderer(ax._renderer)
            # add this new renderer to the current figures list of renderers
            # so we can remove it later (e.g. when using clf()):
            self.gcf()._renderers.append(ax._renderer)
            
        if hasattr(ax, '_vtk_legendbox'):
            ax._renderer.RemoveActor(ax._vtk_legendbox)
        ax._vtk_legendbox = vtk.vtkLegendBoxActor()
        ax._vtk_nolegends = 0
        ax._vtk_legendbox.SetNumberOfEntries(0)

        #ax._renderer.TwoSidedLightingOff()
        ax._renderer.SetBackground(ax.get('bgcolor'))
        viewport = ax.get('viewport')
        if not viewport:
            viewport = (0,0,1,1)
        ax._renderer.SetViewport(viewport)
        ax._renderer.RemoveAllProps() # clear current scene
        #axshape = self.gcf().get('axshape')
        #ax._renderer.SetPixelAspect(axshape[1], axshape[0])

        if not hasattr(ax, '_vtk_apd'):
            ax._vtk_apd = vtk.vtkAppendPolyData()
        else:
            ax._vtk_apd.RemoveAllInputs()

    def _replot(self):
        self._axis = self.gca() # shortcut for fast access
        
        fig = self.gcf()
        if fig.get('axshape') != fig._axshape:
            # remove all current renderers:
            for ren in fig._renderers:
                self._g.RemoveRenderer(ren)
            fig._renderers = []
            fig._axshape = fig.get('axshape')
            
        #if self._master is not None:
        #    fig._root.withdraw()

        if len(self._axis.get('plotitems')) > 0:
            self._setup_axis()
            self._set_lights()
            self._set_colormap()
            self._set_caxis()
            self._create_vtk_data()
            self._create_labeled_axes()
            self._set_view()
            self._set_box_state()
            self._set_colorbar()
            self._set_title()
            self._set_legends()
            self._set_grid()

            # render scene:
            self._axis._renderer.Render()

        if self.get('show') and hasattr(fig, '_root'):
            fig._root.deiconify() # raise window
            fig._root.update()
            
        # render complete scene:
        self._g.Render()
            
    def figure(self, *args, **kwargs):
        """Extension of BaseClass.figure"""
        BaseClass.figure(self, *args, **kwargs) 
        fig = self.gcf()
        try:
            fig._g
        except:# get the parent's render window if it exists
            if self.parent==None:
                try:
                    fig._g = self._create_Tk_gui()
                except Tkinter.TclError:
                    # can't create gui; only offscreen rendering
                    fig._g = vtk.vtkRenderWindow()
                    try: width, height = fig.get('size')
                    except TypeError: width, height = (640, 480)
                    fig._g.SetSize(width, height)
                    fig._g.OffScreenRenderingOn()
            else:
                try:
                    fig._g = self.parent.renwin
                except :
                    #otherwise create your own
                    print 'error creating Vtk panel'
            fig._renderers = []
            fig._axshape = fig.get('axshape')
        self._g = fig._g # link for faster accessvtkRenderWindow
        #self._g.SetAAFrames(5)

    def clf(self):
        """Clear current figure."""
        fig = self.gcf()
        for ren in fig._renderers:
            self._g.RemoveRenderer(ren)
        fig._renderers = []
        if self._master is not None:
            fig._root.withdraw() # hide window
        del fig._g
        BaseClass.clf(self)

    def closefig(self, num):
        """Close figure window with number 'num'."""
        if num in self._figs:
            curfig = self._attrs['curfig']
            self.figure(num) # set figure with 'num' as current figure
            self.clf()
            del self._figs[num]
            self.figure(curfig) # put back the current figure
        else:
            print 'no such figure with number', num

    def closefigs(self):
        """Close all figure windows."""
        keys = self._figs.keys()
        for key in keys:
            closefig(key)
        BaseClass.closefigs(self)
        self.figure(self._attrs['curfig'])

    def hardcopy(self, filename=None, **kwargs):
        color = self.get('color')

        if filename is None:
            print "no filename given, can't save figure"
            return

        quality = 100 # 0 = low quality, 100 = high quality (only for JPEG)
        if 'quality' in kwargs:
            quality = int(kwargs['quality'])
        
        if not self.get('show'): # Don't display to screen
            self._g.OffScreenRenderingOn()

        self._replot()
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self._g)
        # use extension of the file name to determine which writer to use:
        ext = os.path.splitext(filename)[1][1:] 
        if ext in self._image_writers.keys():
            writer = self._image_writers[ext]
        else:
            print "File extension '%s' not supported. " \
                  "Using PostScript output." % ext
            writer = vtk.vtkPostScriptWriter()
        if hasattr(writer, 'SetQuality'): # jpeg
            writer.SetQuality(quality)
        writer.SetFileName(filename)
        writer.SetInput(w2if.GetOutput())
        writer.Write()
        self._g.OffScreenRenderingOff()

    def brighten(self, *args):
        """Brighten or darken color map."""
        nargs = len(args)
        if nargs == 2: # brighten(map,beta)
            if not isinstance(args[0], vtk.vtkLookupTable):
                raise ValueError, "brighten: map must be %s, not %s" % \
                      (type(vtk.vtkLookupTable), type(args[0]))
            lut, beta = args
        elif nargs == 1: # brighten(beta)
            if not hasattr(self._axis, '_vtk_colormap'):
                print "brighten: no colormap set."
                return
            lut = self._axis._vtk_colormap
            beta = args[0]
        if not isinstance(beta, (float,int)) or (beta <= -1 or beta >= 1):
            raise ValueError, "brighten: beta must be between -1 and 1"
        # all is OK, change colormap:
        hue = lut.GetHueRange()
        val = lut.GetValueRange()
 
    # colormaps
    def hsv(self, m=256):
        lut = vtk.vtkLookupTable()
        lut.SetHueRange(0.0, 1.0)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(1.0, 1.0)
        lut.SetNumberOfColors(m)
        lut.Build()
        return lut

    def gray(self, m=256):
        lut = vtk.vtkLookupTable()
        lut.SetHueRange(0.0, 0.0)
        lut.SetSaturationRange(0.0, 0.0)
        lut.SetValueRange(0.0, 1.0)
        lut.SetNumberOfColors(m)
        lut.Build()
        return lut

    def hot(self, m=256):
        lut = vtk.vtkLookupTable()
        inc = 0.01175
        lut.SetNumberOfColors(256)
        i = 0
        r = 0.0; g = 0.0; b = 0.0
        while r <= 1.:
            lut.SetTableValue(i, r, g, b, 1)
            r += inc;  i += 1
        r = 1.
        while g <= 1.:
            lut.SetTableValue(i, r, g, b, 1)
            g += inc;  i += 1
        g = 1.
        while b <= 1:
            if i == 256: break
            lut.SetTableValue(i, r, g, b, 1)
            b += inc;  i += 1
        lut.Build()
        return lut

    def flag(self, m=64):
        """Alternating red, white, blue, and black color map.

        - flag(m)
          'm' must be a multiple of 4
        """
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfColors(m)
        # the last parameter alpha is set to 1 by default
        # in method declaration
        for i in range(0,m,4):
            lut.SetTableValue(i,1,0,0,1)   # red
            lut.SetTableValue(1+i,1,1,1,1) # white
            lut.SetTableValue(2+i,0,0,1,1) # blue
            lut.SetTableValue(3+i,0,0,0,1) # black
        lut.Build()
        return lut

    def jet(self, m=256):
        # blue, cyan, green, yellow, red, black
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfColors(m)
        lut.SetHueRange(0.667,0.0)
        lut.Build()
        return lut

    def blue_to_yellow(self, m=200):
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfColors(m)
        for i in range(m):
            frac = i / float(m / 2.0 - 1.0)
            if (frac <= 1):
                r = frac
                g = r
                b = 1
            else:
                r = 1
                g = r
                b = 2 - frac
            # SetTableValue(indx, red, green, blue, alpha)
            lut.SetTableValue(i, r, g, b, 1)
        lut.Build()
        return lut

    def spring(self, m=256):
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfColors(m)
        lut.SetHueRange(0.0, 0.17)
        lut.SetSaturationRange(0.5, 1.0) 
        lut.SetValueRange(1.0, 1.0)
        lut.Build()
        return lut

    def summer(self, m=256):
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfColors(m)
        lut.SetHueRange(0.47, 0.17)
        lut.SetSaturationRange(1.0, 0.6) 
        lut.SetValueRange(0.5, 1.0)
        lut.Build()
        return lut

    def winter(self, m=256):
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfColors(m)
        lut.SetHueRange(0.8, 0.42)
        lut.SetSaturationRange(1.0, 1.0) 
        lut.SetValueRange(0.6, 1.0)
        lut.Build()
        return lut
        
    def autumn(self, m=256):
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfColors(m)
        lut.SetHueRange(0.0, 0.15)
        lut.SetSaturationRange(1.0, 1.0) 
        lut.SetValueRange(1.0, 1.0)
        lut.Build()
        return lut



def get_backend():
    return plt._g

