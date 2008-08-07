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
import com.artenum.cassandra.util.VtkObjectComboBoxModel;

import vtk.vtkLookupTable;
import vtk.vtkScalarBarActor;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Frame;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFormattedTextField;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JSpinner;
import javax.swing.JTextField;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Scalar bar Control dialog.
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
public class ScalarBarControlDialog extends JDialog implements ActionListener {
    private VtkObject scalarBar;
    private JComboBox lookupTableComboBox;
    private JRadioButton horizontal;
    private JRadioButton vertical;
    private JTextField title;
    private JFormattedTextField x;
    private JFormattedTextField y;
    private JFormattedTextField width;
    private JFormattedTextField height;
    private JSpinner nbColor;
    private VtkObjectComboBoxModel lookupTableModel;
    private PipeLineManager pipelineManager;

    //
    private JButton exit;
    private JButton update;

    public ScalarBarControlDialog(Frame parentFrame, final PipeLineManager pipelineManager) {
        super(parentFrame, "Scalar Bar control");
        this.pipelineManager = pipelineManager;
        lookupTableModel = new VtkObjectComboBoxModel(pipelineManager.getLookupTableList(), null);

        // Dialog box
        getContentPane().setLayout(new BoxLayout(getContentPane(), BoxLayout.PAGE_AXIS));

        // title
        JPanel line = new JPanel(new BorderLayout());
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Title"));
        title = new JTextField();
        line.add(title, BorderLayout.CENTER);
        getContentPane().add(line);

        // position
        line = new JPanel(new BorderLayout());
        JPanel colA = new JPanel(new GridLayout(4, 0));
        JPanel colB = new JPanel(new GridLayout(4, 0));
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Shape"));
        x = new JFormattedTextField("0");
        x.setValue(new Double(0));
        x.setColumns(20);
        y = new JFormattedTextField("0");
        y.setValue(new Double(0));
        width = new JFormattedTextField("0");
        width.setValue(new Double(0));
        height = new JFormattedTextField("0");
        height.setValue(new Double(0));
        colA.add(new JLabel("x : ", JLabel.RIGHT));
        colA.add(new JLabel("y : ", JLabel.RIGHT));
        colA.add(new JLabel("width : ", JLabel.RIGHT));
        colA.add(new JLabel("height : ", JLabel.RIGHT));
        colB.add(x);
        colB.add(y);
        colB.add(width);
        colB.add(height);
        line.add(colA, BorderLayout.WEST);
        line.add(colB, BorderLayout.CENTER);
        getContentPane().add(line);

        // Orientation
        horizontal = new JRadioButton("Horizontal");
        vertical = new JRadioButton("Vertical");
        ButtonGroup group = new ButtonGroup();
        horizontal.addActionListener(this);
        vertical.addActionListener(this);
        group.add(horizontal);
        group.add(vertical);
        line = new JPanel(new GridLayout(1, 2));
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Orientation"));
        line.add(horizontal);
        line.add(vertical);
        getContentPane().add(line);

        //lookuptable
        line = new JPanel(new BorderLayout());
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Lookup table"));
        lookupTableComboBox = new JComboBox(lookupTableModel);
        line.add(lookupTableComboBox, BorderLayout.CENTER);
        getContentPane().add(line);

        // nb color
        // Button
        update = new JButton("Update");
        update.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    updateScalarBar();
                    pipelineManager.validateViewAndGo();
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

    public void setScalarBar(VtkObject scalarBar) {
        this.scalarBar = scalarBar;
        // update ui
        width.setValue(new Double(getVtkScalarBar().GetWidth()));
        height.setValue(new Double(getVtkScalarBar().GetHeight()));
        double[] xy = getVtkScalarBar().GetPosition();
        x.setValue(new Double(xy[0]));
        y.setValue(new Double(xy[1]));
        title.setText(getVtkScalarBar().GetTitle());
        vertical.setSelected(getVtkScalarBar().GetOrientation() == 1);
        lookupTableModel.setSelectedEncapsulateItem(getVtkScalarBar().GetLookupTable());
    }

    public void updateScalarBar() {
        getVtkScalarBar().SetWidth(((Number) width.getValue()).doubleValue());
        getVtkScalarBar().SetHeight(((Number) height.getValue()).doubleValue());
        //getVtkScalarBar().SetMaximumNumberOfColors(((Integer) nbColor.getValue()).intValue());
        getVtkScalarBar().SetPosition(((Number) x.getValue()).doubleValue(), ((Number) y.getValue()).doubleValue());
        getVtkScalarBar().SetTitle(title.getText());
        if (horizontal.isSelected()) {
            getVtkScalarBar().SetOrientationToHorizontal();
        } else {
            getVtkScalarBar().SetOrientationToVertical();
        }

        getVtkScalarBar().SetLookupTable((vtkLookupTable) ((VtkObject) lookupTableModel.getSelectedItem()).getVtkObject());
        pipelineManager.notifyConnectivityChange(scalarBar);
    }

    public vtkScalarBarActor getVtkScalarBar() {
        return (vtkScalarBarActor) scalarBar.getVtkObject();
    }

    public void actionPerformed(ActionEvent arg0) {
        Number oldX = (Number) x.getValue();
        Number oldY = (Number) y.getValue();
        Number oldWidth = (Number) width.getValue();
        Number oldHeight = (Number) height.getValue();

        //
        x.setValue(oldY);
        y.setValue(oldX);
        height.setValue(oldWidth);
        width.setValue(oldHeight);
    }
}
