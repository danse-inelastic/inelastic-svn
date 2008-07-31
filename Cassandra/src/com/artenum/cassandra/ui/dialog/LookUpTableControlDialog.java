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
package com.artenum.cassandra.ui.dialog;

import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.util.CassandraToolBox;
import com.artenum.cassandra.util.VtkObjectComboBoxModel;

import vtk.vtkDataSet;
import vtk.vtkLookupTable;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Frame;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.text.NumberFormat;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFormattedTextField;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Lookup Table Control dialog.
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
public class LookUpTableControlDialog extends JDialog implements ActionListener, ListSelectionListener {
    private VtkObject lookupTable;
    private PipeLineManager pipelineManager;
    private VtkObjectComboBoxModel datasetModel;

    // UI components
    private JList multiDatasetForRange;
    private JFormattedTextField nbColor;
    private JFormattedTextField min;
    private JFormattedTextField max;
    private JFormattedTextField minHue;
    private JFormattedTextField maxHue;
    private JRadioButton rampLinear;
    private JRadioButton rampSCurve;
    private JRadioButton rampSQRT;
    private JRadioButton scaleLinear;
    private JRadioButton scaleLog10;

    //
    private JButton exit;
    private JButton update;

    public LookUpTableControlDialog(Frame parentFrame, PipeLineManager pipelineManager) {
        super(parentFrame, "Lookup Table control");
        this.pipelineManager = pipelineManager;
        datasetModel = new VtkObjectComboBoxModel(pipelineManager.getDataSetList(), null);
        // Dialog box
        getContentPane().setLayout(new BoxLayout(getContentPane(), BoxLayout.PAGE_AXIS));

        // Multi dataset
        JPanel line = new JPanel(new BorderLayout());
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Dataset scalar range"));
        multiDatasetForRange = new JList(datasetModel);
        multiDatasetForRange.addListSelectionListener(this);
        line.add(new JScrollPane(multiDatasetForRange), BorderLayout.CENTER);
        getContentPane().add(line);

        // range
        line = new JPanel(new BorderLayout());
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Range"));
        JPanel colA = new JPanel(new GridLayout(3, 0));
        JPanel colB = new JPanel(new GridLayout(3, 0));
        nbColor = new JFormattedTextField(NumberFormat.getIntegerInstance());
        nbColor.setColumns(20);
        min = new JFormattedTextField("0");
        min.setValue(new Double(0));
        max = new JFormattedTextField("0");
        max.setValue(new Double(1));
        colA.add(new JLabel("Number of color : ", JLabel.RIGHT));
        colA.add(new JLabel("Min : ", JLabel.RIGHT));
        colA.add(new JLabel("Max : ", JLabel.RIGHT));
        colB.add(nbColor);
        colB.add(min);
        colB.add(max);
        line.add(colA, BorderLayout.WEST);
        line.add(colB, BorderLayout.CENTER);
        getContentPane().add(line);

        // Hue range
        line = new JPanel(new BorderLayout());
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Huge range"));
        colA = new JPanel(new GridLayout(2, 0));
        colB = new JPanel(new GridLayout(2, 0));
        minHue = new JFormattedTextField("0");
        minHue.setValue(new Double(0));
        maxHue = new JFormattedTextField("0");
        maxHue.setValue(new Double(0));
        colA.add(new JLabel("Min : ", JLabel.RIGHT));
        colA.add(new JLabel("Max : ", JLabel.RIGHT));
        colB.add(minHue);
        colB.add(maxHue);
        line.add(colA, BorderLayout.WEST);
        line.add(colB, BorderLayout.CENTER);
        getContentPane().add(line);

        // ramp
        line = new JPanel(new GridLayout(0, 4));
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Ramp"));
        ButtonGroup group = new ButtonGroup();
        rampLinear = new JRadioButton("Linear");
        rampSCurve = new JRadioButton("Curve");
        rampSQRT = new JRadioButton("Square root");
        group.add(rampLinear);
        group.add(rampSCurve);
        group.add(rampSQRT);
        line.add(rampLinear);
        line.add(rampSCurve);
        line.add(rampSQRT);
        getContentPane().add(line);

        // Scale
        line = new JPanel(new GridLayout(0, 2));
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Scale"));
        ButtonGroup groupScale = new ButtonGroup();
        scaleLinear = new JRadioButton("Linear");
        scaleLog10 = new JRadioButton("log10");
        groupScale.add(scaleLinear);
        groupScale.add(scaleLog10);
        line.add(scaleLinear);
        line.add(scaleLog10);
        getContentPane().add(line);

        // Button
        update = new JButton("Update");
        update.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    updateLookupTable();
                }
            });
        exit = new JButton("Cancel");
        exit.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    dispose();
                }
            });
        line = new JPanel();
        line.setLayout(new BoxLayout(line, BoxLayout.LINE_AXIS));
        line.add(Box.createHorizontalGlue());
        line.add(update);
        line.add(exit);
        getContentPane().add(line);

        // Pack
        pack();
        setLocationRelativeTo(parentFrame);
    }

    public void setLookupTable(VtkObject lookupTable) {
        this.lookupTable = lookupTable;
        // update ui
        switch (getVtkLookUpTable().GetRamp()) {
        case 0:
            // linear
            rampLinear.setSelected(true);
            break;
        case 1:
            // curve
            rampSCurve.setSelected(true);
            break;
        case 2:
            // sqrt
            rampSQRT.setSelected(true);
            break;
        }

        switch (getVtkLookUpTable().GetScale()) {
        case 0:
            // Linear
            scaleLinear.setSelected(true);
            break;
        case 1:
            // Log10
            scaleLog10.setSelected(true);
            break;
        }

        double[] range = getVtkLookUpTable().GetTableRange();
        double[] hueRange = getVtkLookUpTable().GetHueRange();
        min.setValue(new Double(range[0]));
        max.setValue(new Double(range[1]));
        minHue.setValue(new Double(hueRange[0]));
        maxHue.setValue(new Double(hueRange[1]));
        nbColor.setValue(new Integer(getVtkLookUpTable().GetNumberOfColors()));
    }

    public void updateLookupTable() {
        if (rampLinear.isSelected()) {
            getVtkLookUpTable().SetRampToLinear();
        }

        if (rampSCurve.isSelected()) {
            getVtkLookUpTable().SetRampToSCurve();
        }

        if (rampSQRT.isSelected()) {
            getVtkLookUpTable().SetRampToSQRT();
        }

        if (scaleLinear.isSelected()) {
            getVtkLookUpTable().SetScaleToLinear();
        }

        if (scaleLog10.isSelected()) {
            getVtkLookUpTable().SetScaleToLog10();
        }

        getVtkLookUpTable().SetNumberOfColors(((Number) nbColor.getValue()).intValue());
        getVtkLookUpTable().SetRange(((Number) min.getValue()).doubleValue(), ((Number) max.getValue()).doubleValue());
        getVtkLookUpTable().SetHueRange(((Number) minHue.getValue()).doubleValue(), ((Number) maxHue.getValue()).doubleValue());

        // update mappers
        CassandraToolBox.updateMapper(pipelineManager, getVtkLookUpTable());

        getVtkLookUpTable().Build();
        pipelineManager.notifyConnectivityChange(lookupTable);
        pipelineManager.validateViewAndGo();
    }

    public vtkLookupTable getVtkLookUpTable() {
        return (vtkLookupTable) lookupTable.getVtkObject();
    }

    public void actionPerformed(ActionEvent e) {
        // update range data
        Object obj = multiDatasetForRange.getSelectedValue();
        if (obj != null) {
            double[] range = ((vtkDataSet) ((VtkObject) obj).getVtkObject()).GetScalarRange();
            min.setValue(new Double(range[0]));
            max.setValue(new Double(range[1]));
        }
    }

    public void valueChanged(ListSelectionEvent e) {
        double min = 0;
        double max = 0;
        double[] range;
        Object[] selectedObjects = multiDatasetForRange.getSelectedValues();
        for (int i = 0; i < selectedObjects.length; i++) {
            range = ((vtkDataSet) ((VtkObject) selectedObjects[i]).getVtkObject()).GetScalarRange();
            if (i == 0) {
                min = range[0];
                max = range[1];
            }

            if (min > range[0]) {
                min = range[0];
            }

            if (max < range[1]) {
                max = range[1];
            }
        }

        if (min != max) {
            this.min.setValue(new Double(min));
            this.max.setValue(new Double(max));
        }
    }
}
