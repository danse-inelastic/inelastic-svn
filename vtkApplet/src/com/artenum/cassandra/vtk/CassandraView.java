/**
 * Copyright (c) Artenum SARL 2004-2005
 * @author Sebastien Jourdain
 *
 * All rights reserved. This software can
 * not be used or copy or diffused without
 * an explicit license of Artenum SARL, Paris-France
 */
package com.artenum.cassandra.vtk;

import vtk.vtkCamera;
import vtk.vtkCanvas;
import vtk.vtkGenericRenderWindowInteractor;
import vtk.vtkInteractorStyleTrackballCamera;
import vtk.vtkJPEGWriter;
import vtk.vtkPNGWriter;
import vtk.vtkPointPicker;
import vtk.vtkTIFFWriter;
import vtk.vtkWindowToImageFilter;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import java.util.ArrayList;
import java.util.Iterator;

import javax.swing.SwingUtilities;

/**
 * @author seb
 */
public class CassandraView extends vtkCanvas implements KeyListener {
    private static final long serialVersionUID = 1L;
    private double zoomFactor = 0.1;
    private boolean deepValidation = true;
    private vtkPointPicker pointPicker;
    private ArrayList pickingObservers;

    public CassandraView() {
        super();
        pointPicker = new vtkPointPicker();
        pointPicker.SetTolerance(0.005);
        vtkInteractorStyleTrackballCamera style = new vtkInteractorStyleTrackballCamera();
        getInteractor().SetInteractorStyle(style);
        getInteractor().SetPicker(pointPicker);
        pickingObservers = new ArrayList();
        // link observer to picker
        pointPicker.AddObserver("EndPickEvent", this, "pick");
    }

    public void addPickingObserver(PickingObserver po) {
        pickingObservers.add(po);
    }

    public void removePickingObserver(PickingObserver po) {
        pickingObservers.remove(po);
    }

    public void removePickingObserver(int index) {
        pickingObservers.remove(index);
    }

    public void pick() {
        PickingObserver observer = null;
        if (pointPicker.GetPointId() > 0) {
            for (Iterator i = pickingObservers.iterator(); i.hasNext();) {
                observer = (PickingObserver) i.next();
                observer.pick(pointPicker);
            }
        }
    }

    public vtkPointPicker getPointPicker() {
        return pointPicker;
    }

    public void setZoomFactor(double zoomFactor) {
        this.zoomFactor = zoomFactor;
    }

    public Dimension getMinimumSize() {
        return new Dimension(0, 0);
    }

    public void setXYView() {
        this.setCameraPosition(0.0, 0.0, ren.GetActiveCamera().GetDistance(), 0.0);
        this.UpdateLight();
        resetCamera();
    }

    public void setYZView() {
        this.setCameraPosition(ren.GetActiveCamera().GetDistance(), 0.0, 0.0, 0.0);
        this.UpdateLight();
        resetCamera();
    }

    public void setXZView() {
        this.setCameraPosition(0.0, ren.GetActiveCamera().GetDistance(), 0.0, 0.0);
        this.UpdateLight();
        resetCamera();
    }

    protected void setCameraPosition(double xCam, double yCam, double zCam, double rollCam) {
        ren.GetActiveCamera().SetPosition(xCam, yCam, zCam);
        ren.GetActiveCamera().SetRoll(rollCam);
    }

    public void setBackground(Color c) {
        double r = ((float) c.getRed()) / 255;
        double g = ((float) c.getGreen()) / 255;
        double b = ((float) c.getBlue()) / 255;
        GetRenderer().SetBackground(r, g, b);
    }

    public void setAmbiantLight(Color c) {
        double r = ((float) c.getRed()) / 255;
        double g = ((float) c.getGreen()) / 255;
        double b = ((float) c.getBlue()) / 255;
        GetRenderer().SetAmbient(r, g, b);
    }

    public void resetCamera() {
        super.resetCamera();
    }

    public void zoom(double zoomFactor) {
        vtkCamera cam = GetRenderer().GetActiveCamera();
        if (cam.GetParallelProjection() == 1) {
            cam.SetParallelScale(cam.GetParallelScale() / zoomFactor);
        } else {
            cam.Dolly(zoomFactor);
            resetCameraClippingRange();
        }
    }

    public void rotate(double xx, double yy) {
        vtkCamera cam = GetRenderer().GetActiveCamera();
        cam.Azimuth(xx);
        cam.Elevation(yy);
        cam.OrthogonalizeViewUp();
        resetCameraClippingRange();
        if (this.LightFollowCamera == 1) {
            lgt.SetPosition(cam.GetPosition());
            lgt.SetFocalPoint(cam.GetFocalPoint());
        }
    }

    public synchronized void deepValidateView() {
        // Linux view validation error
        if (System.getProperty("os.name").toLowerCase().indexOf("win") == -1) {
            Render();
            invalidate();
            validate();
            repaint();
        } else {
            repaint();
        }

        Dimension d = getPreferredSize();
        if (!getSize().equals(d)) {
            setSize(1, 1);
            setSize(d);
            invalidate();
            validate();
            repaint();
        } else if (deepValidation) {
            deepValidation = false;
            setSize(1, 1);
            setSize(d);
            invalidate();
            validate();
            repaint();
        }
    }

    public void validateViewAndWait() {
        try {
            SwingUtilities.invokeAndWait(new Runnable() {
                    public void run() {
                        // Linux view validation error
                        if (System.getProperty("os.name").toLowerCase().indexOf("win") == -1) {
                            Render();
                            invalidate();
                            validate();
                            repaint();
                        } else {
                            repaint();
                        }
                    }
                });
        } catch (Exception e) {}
    }

    public void validateViewAndGo() {
        try {
            SwingUtilities.invokeLater(new Runnable() {
                    public void run() {
                        // Linux view validation error
                        if (System.getProperty("os.name").toLowerCase().indexOf("win") == -1) {
                            Render();
                            invalidate();
                            validate();
                            repaint();
                        } else {
                            repaint();
                        }
                    }
                });
        } catch (Exception e) {}
    }

    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_I) {
            zoom(1.0 + zoomFactor);
        } else if (e.getKeyCode() == KeyEvent.VK_O) {
            zoom(1.0 - zoomFactor);
        } else if (e.getKeyCode() == KeyEvent.VK_UP) {
            rotate(0, -1);
        } else if (e.getKeyCode() == KeyEvent.VK_DOWN) {
            rotate(0, 1);
        } else if (e.getKeyCode() == KeyEvent.VK_LEFT) {
            rotate(1, 0);
        } else if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
            rotate(-1, 0);
        } else {
            super.keyPressed(e);
        }
    }

    public void keyReleased(KeyEvent e) {
        super.keyReleased(e);
    }

    public void keyTyped(KeyEvent e) {
        super.keyTyped(e);
    }

    public synchronized void saveToPNG(String fileToSave) {
        Lock();

        vtkWindowToImageFilter w2if = new vtkWindowToImageFilter();
        w2if.SetInput(rw);

        w2if.SetMagnification(1);
        w2if.Update();

        vtkPNGWriter writer = new vtkPNGWriter();
        writer.SetInput(w2if.GetOutput());
        writer.SetFileName(fileToSave);
        writer.Write();

        UnLock();
    }

    public synchronized void saveToJPG(String fileToSave) {
        Lock();

        vtkWindowToImageFilter w2if = new vtkWindowToImageFilter();
        w2if.SetInput(rw);

        w2if.SetMagnification(1);
        w2if.Update();

        vtkJPEGWriter writer = new vtkJPEGWriter();
        writer.SetInput(w2if.GetOutput());
        writer.SetFileName(fileToSave);
        writer.Write();

        UnLock();
    }

    public synchronized void saveToTIFF(String fileToSave) {
        Lock();

        vtkWindowToImageFilter w2if = new vtkWindowToImageFilter();
        w2if.SetInput(rw);

        w2if.SetMagnification(1);
        w2if.Update();

        vtkTIFFWriter writer = new vtkTIFFWriter();
        writer.SetInput(w2if.GetOutput());
        writer.SetFileName(fileToSave);
        writer.Write();

        UnLock();
    }

    public vtkGenericRenderWindowInteractor getInteractor() {
        return getIren();
    }
}
