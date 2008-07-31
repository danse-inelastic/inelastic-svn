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
package com.artenum.cassandra.action.menu;

import com.artenum.cassandra.pipeline.PipeLineManager;

import vtk.vtkActor;
import vtk.vtkCellArray;
import vtk.vtkDoubleArray;
import vtk.vtkFloatArray;
import vtk.vtkIntArray;
import vtk.vtkPoints;
import vtk.vtkPolyData;
import vtk.vtkPolyDataMapper;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JMenuItem;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> MenuItem for adding a square dataset with its pipeline.
 *                       Each corner have a potentiel 10, 20, 30, 40
 *
 * <b>Change log :</b>
 * </pre>
 * <table cellpadding="3" cellspacing="0" border="1" width="100%">
 * <tr BGCOLOR="#CCCCFF" CLASS="TableHeadingColor"><td><b>Version number</b></td><td><b>Author (name, e-mail)</b></td><td><b>Corrections/Modifications</b></td></tr>
 * <tr><td>0.1</td><td>Sebastien Jourdain, jourdain@artenum.com</td><td>Creation</td></tr>
 * </table>
 *
 * @author        Sebastien Jourdain
 * @version       0.1
 */
public class AddPlaque extends JMenuItem implements ActionListener {
    private PipeLineManager pipelineManager;

    public AddPlaque(String itemName, PipeLineManager pipelineManager) {
        super(itemName);
        addActionListener(this);
        //
        this.pipelineManager = pipelineManager;
    }

    public void actionPerformed(ActionEvent e) {
        vtkFloatArray pcoords = new vtkFloatArray();
        pcoords.SetNumberOfComponents(3);
        pcoords.SetNumberOfTuples(4);
        pcoords.SetTuple3(0, 0.0, 0.0, 0.0);
        pcoords.SetTuple3(1, 0.0, 1.0, 0.0);
        pcoords.SetTuple3(2, 1.0, 0.0, 0.0);
        pcoords.SetTuple3(3, 1.0, 1.0, 0.0);

        vtkPoints points = new vtkPoints();
        points.SetData(pcoords);

        vtkCellArray strips = new vtkCellArray();
        strips.InsertNextCell(4);
        strips.InsertCellPoint(0);
        strips.InsertCellPoint(1);
        strips.InsertCellPoint(2);
        strips.InsertCellPoint(3);

        vtkIntArray temperature = new vtkIntArray();
        temperature.SetName("Temperature");
        temperature.InsertNextValue(10);
        temperature.InsertNextValue(20);
        temperature.InsertNextValue(40);
        temperature.InsertNextValue(30);

        vtkDoubleArray vorticity = new vtkDoubleArray();
        vorticity.SetName("Vorticity");
        vorticity.InsertNextValue(2.7);
        vorticity.InsertNextValue(4.1);
        vorticity.InsertNextValue(5.3);
        vorticity.InsertNextValue(3.4);

        vtkPolyData polydata = new vtkPolyData();
        polydata.SetPoints(points);
        polydata.SetStrips(strips);
        polydata.GetPointData().SetScalars(temperature);
        polydata.GetPointData().AddArray(vorticity);

        vtkPolyDataMapper mapper = new vtkPolyDataMapper();
        mapper.SetInput(polydata);
        mapper.SetScalarRange(0, 40);

        vtkActor actor = new vtkActor();
        actor.SetMapper(mapper);

        pipelineManager.addDataSet(polydata, "Plaque");
        pipelineManager.addMapper(mapper, "Plaque");
        pipelineManager.setActorVisible(pipelineManager.addActor(actor, "Plaque"), true);

        pipelineManager.validateViewAndGo();
    }
}
