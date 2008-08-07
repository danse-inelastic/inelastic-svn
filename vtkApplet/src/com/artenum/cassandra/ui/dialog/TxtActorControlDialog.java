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

import vtk.vtkTextActor;

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
import javax.swing.JButton;
import javax.swing.JColorChooser;
import javax.swing.JDialog;
import javax.swing.JFormattedTextField;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Text Actor Control dialog.
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
public class TxtActorControlDialog extends JDialog {
    private PipeLineManager pipelineManager;
    private VtkObject currentVtkObject;

    //
    private JTextField txtContent;
    private JFormattedTextField posX;
    private JFormattedTextField posY;
    private JFormattedTextField fontSize;
    private JButton color;

    //
    private JButton exit;
    private JButton update;

    public TxtActorControlDialog(final Frame parentFrame, final PipeLineManager pipelineManager) {
        super(parentFrame, "Text control");
        this.pipelineManager = pipelineManager;

        // Dialog box
        getContentPane().setLayout(new BoxLayout(getContentPane(), BoxLayout.PAGE_AXIS));

        // Txt content
        JPanel line = new JPanel(new BorderLayout());
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Text content"));
        txtContent = new JTextField();
        line.add(txtContent, BorderLayout.CENTER);
        getContentPane().add(line);

        // Position
        line = new JPanel(new BorderLayout());
        line.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.BLACK, 1), "Range"));
        JPanel colA = new JPanel(new GridLayout(4, 0));
        JPanel colB = new JPanel(new GridLayout(4, 0));
        posX = new JFormattedTextField("0");
        posX.setValue(new Double(0));
        posX.setColumns(20);
        posY = new JFormattedTextField("0");
        posY.setValue(new Double(0));
        fontSize = new JFormattedTextField(NumberFormat.getIntegerInstance());
        color = new JButton();
        color.setBackground(Color.WHITE);
        colA.add(new JLabel("X : ", JLabel.RIGHT));
        colA.add(new JLabel("Y : ", JLabel.RIGHT));
        colA.add(new JLabel("Font size : ", JLabel.RIGHT));
        colA.add(new JLabel("Color : ", JLabel.RIGHT));
        colB.add(posX);
        colB.add(posY);
        colB.add(fontSize);
        colB.add(color);
        line.add(colA, BorderLayout.WEST);
        line.add(colB, BorderLayout.CENTER);
        getContentPane().add(line);

        // Button
        color.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    vtkTextActor vtkTxtActor = (vtkTextActor) currentVtkObject.getVtkObject();
                    Color result = JColorChooser.showDialog(parentFrame, "Text color",
                            CassandraToolBox.vtkColorConverter(vtkTxtActor.GetTextProperty().GetColor()));
                    if (result != null) {
                        color.setBackground(result);
                        vtkTxtActor.GetTextProperty().SetColor(CassandraToolBox.vtkColorConverter(result));
                    }

                    pipelineManager.validateViewAndGo();
                }
            });

        update = new JButton("Update");
        update.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    double x = ((Number) posX.getValue()).doubleValue();
                    double y = ((Number) posY.getValue()).doubleValue();
                    int size = ((Number) fontSize.getValue()).intValue();
                    vtkTextActor vtkTxtActor = (vtkTextActor) currentVtkObject.getVtkObject();
                    vtkTxtActor.SetPosition(x, y);
                    vtkTxtActor.SetInput(txtContent.getText());
                    vtkTxtActor.GetTextProperty().SetFontSize(size);
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

    public void setTxtActor(VtkObject currentTxtActor) {
        this.currentVtkObject = currentTxtActor;
        vtkTextActor vtkTxtActor = (vtkTextActor) currentVtkObject.getVtkObject();
        posX.setValue(new Double(vtkTxtActor.GetPosition()[0]));
        posY.setValue(new Double(vtkTxtActor.GetPosition()[1]));
        fontSize.setValue(new Integer(vtkTxtActor.GetTextProperty().GetFontSize()));
        txtContent.setText(vtkTxtActor.GetInput());
    }
}
