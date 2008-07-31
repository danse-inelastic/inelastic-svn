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
import vtk.vtkArrowSource;
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
 * <b>Description  :</b> MenuItem for adding an arrow dataset with its pipeline.
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
public class AddArrow extends JMenuItem implements ActionListener {
    private PipeLineManager pipelineManager;

    public AddArrow(String itemName, PipeLineManager pipelineManager) {
        super(itemName);
        addActionListener(this);
        //
        this.pipelineManager = pipelineManager;
    }

    public void actionPerformed(ActionEvent e) {
        vtkArrowSource arrow = new vtkArrowSource();
        arrow.SetTipLength(1);
        arrow.SetTipRadius(30);
        arrow.SetTipResolution(20);
        arrow.SetShaftRadius(15);
        arrow.SetShaftResolution(30);
        arrow.SetProgress(100);
        arrow.SetProgressText("Hello");
        vtkPolyDataMapper mapper = new vtkPolyDataMapper();
        mapper.SetInput(arrow.GetOutput());
        vtkActor coneActor = new vtkActor();
        coneActor.SetMapper(mapper);

        pipelineManager.addDataSet(arrow.GetOutput(), "Arrow");
        pipelineManager.addMapper(mapper, "Arrow");
        pipelineManager.setActorVisible(pipelineManager.addActor(coneActor, "Arrow"), true);

        pipelineManager.validateViewAndGo();
    }
}
