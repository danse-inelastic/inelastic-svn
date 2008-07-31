/*
 * (c) Copyright: Artenum SARL, 101-103 Boulevard Mac Donald,
 *                75019, Paris, France 2005.
 *                http://www.artenum.com
 *
 * License:
 *
 *  This program is free software; you can redistribute it
 *  and/or modify it under the terms of the Q Public License;
 *  either version 1 of the License.
 *
 *  This program is distributed in the hope that it will be
 *  useful, but WITHOUT ANY WARRANTY; without even the implied
 *  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 *  PURPOSE. See the Q Public License for more details.
 *
 *  You should have received a copy of the Q Public License
 *  License along with this program;
 *  if not, write to:
 *    Artenum SARL, 101-103 Boulevard Mac Donald,
 *    75019, PARIS, FRANCE, e-mail: contact@artenum.com
 */
package com.artenum.cassandra.util;

import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;

import vtk.vtkIVExporter;
import vtk.vtkLookupTable;
import vtk.vtkMapper;
import vtk.vtkOBJExporter;
import vtk.vtkOOGLExporter;
import vtk.vtkRIBExporter;
import vtk.vtkRenderWindow;
import vtk.vtkVRMLExporter;

import java.awt.Color;
import java.awt.Component;
import java.awt.Dialog;
import java.awt.Frame;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import javax.swing.JPopupMenu;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Cassandra toolbox.
 *
 * </pre>
 * <table cellpadding="3" cellspacing="0" border="1" width="100%">
 * <tr BGCOLOR="#CCCCFF" CLASS="TableHeadingColor"><td><b>Version number</b></td><td><b>Author (name, e-mail)</b></td><td><b>Corrections/Modifications</b></td></tr>
 * <tr><td>0.1</td><td>Sebastien Jourdain, jourdain@artenum.com</td><td>Creation</td></tr>
 * </table>
 *
 * @author        Sebastien Jourdain
 * @version       0.1
 */
public class CassandraToolBox {
    public static Frame getParentFrame(Component c) {
        Component currentComponent = c;
        while ((currentComponent != null) && !(currentComponent instanceof Frame)) {
            if (currentComponent instanceof JPopupMenu) {
                currentComponent = ((JPopupMenu) currentComponent).getInvoker();
            } else {
                currentComponent = currentComponent.getParent();
            }
        }

        return (Frame) currentComponent;
    }

    public static Dialog getParentDialog(Component c) {
        Component currentComponent = c;
        while ((currentComponent != null) && !(currentComponent instanceof Dialog)) {
            if (currentComponent instanceof JPopupMenu) {
                currentComponent = ((JPopupMenu) currentComponent).getInvoker();
            } else {
                currentComponent = currentComponent.getParent();
            }
        }

        return (Dialog) currentComponent;
    }

    public static void updateMapper(PipeLineManager pipelineManager, vtkLookupTable lookupTable) {
        for (Iterator i = pipelineManager.getMapperList().getData().iterator(); i.hasNext();) {
            vtkMapper mapper = (vtkMapper) ((VtkObject) i.next()).getVtkObject();
            if (mapper.GetLookupTable().equals(lookupTable)) {
                mapper.SetScalarRange(lookupTable.GetTableRange());
            }
        }
    }

    public static void updateLookupTableRange(vtkLookupTable lookupTable, double min, double max) {
        double realMin = lookupTable.GetTableRange()[0];
        double realMax = lookupTable.GetTableRange()[1];
        if (realMin > min) {
            realMin = min;
        }

        if (realMax < max) {
            realMax = max;
        }

        lookupTable.SetRange(realMin, realMax);
        lookupTable.Build();
    }

    public static Color vtkColorConverter(double r, double g, double b) {
        return new Color((float) r, (float) g, (float) b);
    }

    public static double[] vtkColorConverter(Color c) {
        double[] rgb = new double[3];
        rgb[0] = ((float) c.getRed()) / 255;
        rgb[1] = ((float) c.getGreen()) / 255;
        rgb[2] = ((float) c.getBlue()) / 255;
        return rgb;
    }

    public static Color vtkColorConverter(double[] rvb) {
        return vtkColorConverter(rvb[0], rvb[1], rvb[2]);
    }

    public static ArrayList splitNumbers(String fileNameToSplit) {
        ArrayList result = new ArrayList();
        StringBuffer number = null;
        StringBuffer text = null;
        int numberID = 1;
        int stringID = 2;
        int currentID = -1;
        for (int i = 0; i < fileNameToSplit.length(); i++) {
            if ((fileNameToSplit.charAt(i) >= '0') && (fileNameToSplit.charAt(i) <= '9')) {
                if ((currentID == stringID) || (currentID == -1)) {
                    currentID = numberID;
                    number = new StringBuffer();
                    result.add(number);
                }

                number.append(fileNameToSplit.charAt(i));
            } else {
                if ((currentID == numberID) || (currentID == -1)) {
                    currentID = stringID;
                    text = new StringBuffer();
                    result.add(text);
                }

                text.append(fileNameToSplit.charAt(i));
            }
        }

        return result;
    }

    public static void sortFileList(File[] fileListToSort) {
        Arrays.sort(fileListToSort, new FileComparator());
    }

    public static void saveObject(Object obj, String fileName)
        throws Exception {
        FileOutputStream fos = new FileOutputStream(fileName);
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(obj);
        oos.close();
    }

    public static Object loadObject(String fileName) throws Exception {
        FileInputStream fis = new FileInputStream(fileName);
        ObjectInputStream ois = new ObjectInputStream(fis);
        return ois.readObject();
    }

    public static void export3DScene(String filename, vtkRenderWindow input)
        throws Exception {
        long start = System.currentTimeMillis();
        vtkIVExporter exporter1 = new vtkIVExporter();
        exporter1.SetInput(input);
        exporter1.SetFileName(filename + ".oiv");
        exporter1.Update();
        System.out.println("OpenInventor: " + (System.currentTimeMillis() - start));

        start = System.currentTimeMillis();
        vtkOOGLExporter exporter2 = new vtkOOGLExporter();
        exporter2.SetInput(input);
        exporter2.SetFileName(filename + ".geom");
        exporter2.Update();
        System.out.println("OOGL: " + (System.currentTimeMillis() - start));

        start = System.currentTimeMillis();
        vtkOBJExporter exporter3 = new vtkOBJExporter();
        exporter3.SetInput(input);
        exporter3.SetFilePrefix(filename);
        exporter3.Update();
        System.out.println("OBJ: " + (System.currentTimeMillis() - start));

        start = System.currentTimeMillis();
        vtkRIBExporter exporter4 = new vtkRIBExporter();
        exporter4.SetInput(input);
        exporter4.SetFilePrefix(filename);
        exporter4.Update();
        System.out.println("RIB: " + (System.currentTimeMillis() - start));

        start = System.currentTimeMillis();
        vtkVRMLExporter exporter = new vtkVRMLExporter();
        exporter.SetInput(input);
        exporter.SetFileName(filename + ".wrl");
        exporter.Update();
        System.out.println("VRML: " + (System.currentTimeMillis() - start));
    }

    public static void export3DScene(vtkRenderWindow input)
        throws Exception {
        long start = System.currentTimeMillis();
        byte[] buffer = new byte[1024 * 1024];
        int length = -1;
        start = System.currentTimeMillis();
        vtkVRMLExporter exporter = new vtkVRMLExporter();
        exporter.SetInput(input);
        exporter.SetFileName("tmp.wrl");
        exporter.Update();
        FileInputStream fis = new FileInputStream("scene.wrl");
        BufferedInputStream bis = new BufferedInputStream(fis);
        FileOutputStream fos = new FileOutputStream("scene.zip");
        BufferedOutputStream bos = new BufferedOutputStream(fos);
        ZipOutputStream zos = new ZipOutputStream(bos);
        ZipEntry entry = new ZipEntry("scene3D.wrl");
        zos.putNextEntry(entry);
        // write content
        while ((length = bis.read(buffer)) != -1) {
            zos.write(buffer, 0, length);
        }

        zos.closeEntry();
        zos.close();
        fis.close();
        System.out.println("VRML: " + (System.currentTimeMillis() - start));
    }
}
