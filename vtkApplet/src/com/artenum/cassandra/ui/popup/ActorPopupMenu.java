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
package com.artenum.cassandra.ui.popup;

import com.artenum.cassandra.action.menu.RenameVtkObject;
import com.artenum.cassandra.pipeline.CascadeRemoveManager;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;

import vtk.vtkActor;
import vtk.vtkActor2D;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.util.Hashtable;

import javax.swing.JCheckBoxMenuItem;
import javax.swing.JColorChooser;
import javax.swing.JLabel;
import javax.swing.JMenuItem;
import javax.swing.JPopupMenu;
import javax.swing.JSlider;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Actor popup menu.
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
public class ActorPopupMenu extends JPopupMenu implements ActionListener, ChangeListener, VtkObjectPopupMenu {
    // Actions
    public final static String ACTOR_SHOW = "actor.show";
    public final static String ACTOR_COLOR = "actor.color";
    public final static String ACTOR_REMOVE = "actor.remove";
    private PipeLineManager pipeLineManager;
    private CascadeRemoveManager cascadeRemoveManager;
    private VtkObject currentVtkObject;

    // UI components
    private JCheckBoxMenuItem viewActor;
    private JSlider actorOpacity;
    private JMenuItem actorColor;
    private RenameVtkObject actorRename;
    private JMenuItem actorRemove;

    public ActorPopupMenu(PipeLineManager pipeLineManager, CascadeRemoveManager cascadeRemoveManager) {
        this.pipeLineManager = pipeLineManager;
        this.cascadeRemoveManager = cascadeRemoveManager;
        // Init popup with its ui components
        viewActor = new JCheckBoxMenuItem("Visible");
        viewActor.setActionCommand(ACTOR_SHOW);
        viewActor.addActionListener(this);
        actorColor = new JMenuItem("Actor color");
        actorColor.setActionCommand(ACTOR_COLOR);
        actorColor.addActionListener(this);
        actorOpacity = new JSlider(0, 50, 50);
        actorOpacity.addChangeListener(this);
        Hashtable label = new Hashtable();
        label.put(new Integer(0), new JLabel("0%"));
        label.put(new Integer(50), new JLabel("100%"));
        label.put(new Integer(25), new JLabel("50%"));
        actorOpacity.setMinorTickSpacing(1);
        actorOpacity.setMajorTickSpacing(5);
        actorOpacity.setLabelTable(label);
        actorOpacity.setPaintLabels(true);
        actorOpacity.setPaintLabels(true);
        actorRename = new RenameVtkObject("Rename", "Rename actor", null);
        actorRemove = new JMenuItem("Remove");
        actorRemove.setActionCommand(ACTOR_REMOVE);
        actorRemove.addActionListener(this);
        //
        add(viewActor);
        add(actorOpacity);
        addSeparator();
        add(actorColor);
        add(actorRename);
        addSeparator();
        add(actorRemove);
    }

    public void setCurrentVtkOject(VtkObject currentVtkObject) {
        this.currentVtkObject = currentVtkObject;
        actorRename.setVtkObject(currentVtkObject);
        // init popup with current vtkObject
        actorColor.setEnabled(currentVtkObject.getVtkObject() instanceof vtkActor);
        if (currentVtkObject.getVtkObject() instanceof vtkActor) {
            actorOpacity.setValue((int) (((vtkActor) currentVtkObject.getVtkObject()).GetProperty().GetOpacity() * 50));
        }

        if (currentVtkObject.getVtkObject() instanceof vtkActor2D) {
            actorOpacity.setValue((int) (((vtkActor2D) currentVtkObject.getVtkObject()).GetProperty().GetOpacity() * 50));
        }

        if (currentVtkObject.getMetaData().get(VtkObject.ACTOR_VISIBLE) == null) {
            viewActor.setSelected(false);
        } else {
            viewActor.setSelected(((String) currentVtkObject.getMetaData().get(VtkObject.ACTOR_VISIBLE)).equals("true"));
        }
    }

    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        if (command.equals(ACTOR_SHOW)) {
            pipeLineManager.setActorVisible(currentVtkObject, viewActor.isSelected());
        } else if (command.equals(ACTOR_COLOR)) {
            Color c = JColorChooser.showDialog(this, "Actor color", Color.BLACK);
            if (c != null) {
                double r = ((float) c.getRed()) / 255;
                double g = ((float) c.getGreen()) / 255;
                double b = ((float) c.getBlue()) / 255;

                if (currentVtkObject.getVtkObject() instanceof vtkActor) {
                    ((vtkActor) currentVtkObject.getVtkObject()).GetProperty().SetColor(r, g, b);
                }

                ((vtkActor) currentVtkObject.getVtkObject()).ApplyProperties();
            }
        } else if (command.equals(ACTOR_REMOVE)) {
            cascadeRemoveManager.removeActor(currentVtkObject);
        }

        pipeLineManager.validateViewAndGo();
    }

    public void stateChanged(ChangeEvent e) {
        if (currentVtkObject.getVtkObject() instanceof vtkActor) {
            ((vtkActor) currentVtkObject.getVtkObject()).GetProperty().SetOpacity(((double) actorOpacity.getValue()) / 50);
        } else if (currentVtkObject.getVtkObject() instanceof vtkActor2D) {
            ((vtkActor2D) currentVtkObject.getVtkObject()).GetProperty().SetOpacity(((double) actorOpacity.getValue()) / 50);
        }

        pipeLineManager.validateViewAndGo();
    }

    public JMenuItem getActorColorMenuItem() {
        return actorColor;
    }

    public JSlider getActorOpacityMenuItem() {
        return actorOpacity;
    }

    public JMenuItem getActorRemoveMenuItem() {
        return actorRemove;
    }

    public JMenuItem getActorRenameMenuItem() {
        return actorRename;
    }

    public JCheckBoxMenuItem getActorVisibleMenuItem() {
        return viewActor;
    }
}
