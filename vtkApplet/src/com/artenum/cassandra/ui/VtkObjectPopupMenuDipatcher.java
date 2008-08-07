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
package com.artenum.cassandra.ui;

import com.artenum.cassandra.pipeline.CascadeRemoveManager;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObject;
import com.artenum.cassandra.plugin.PluginManager;
import com.artenum.cassandra.ui.popup.ActorPopupMenu;
import com.artenum.cassandra.ui.popup.DataSetPopupMenu;
import com.artenum.cassandra.ui.popup.LookupTablePopupMenu;
import com.artenum.cassandra.ui.popup.MapperPopupMenu;
import com.artenum.cassandra.ui.popup.ScalarBarPopupMenu;
import com.artenum.cassandra.ui.popup.TxtActorPopupMenu;
import com.artenum.cassandra.ui.popup.VtkObjectPopupMenu;

import java.awt.Component;

import javax.swing.JPopupMenu;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Popup menu ma,ager/dispatcher for VtkObject
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
public class VtkObjectPopupMenuDipatcher {
    private PipeLineManager pipeLineManager;
    private PluginManager pluginManager;
    private VtkObject vtkObject;
    private JPopupMenu currentMenu;

    // Menu
    private DataSetPopupMenu dataSetMenu;
    private LookupTablePopupMenu lookupTableMenu;
    private ActorPopupMenu actorMenu;
    private TxtActorPopupMenu txtActorMenu;
    private ScalarBarPopupMenu scalarBarMenu;
    private MapperPopupMenu mapperMenu;

    public VtkObjectPopupMenuDipatcher(PipeLineManager pipeLineManager, PluginManager pluginManager) {
        this.pipeLineManager = pipeLineManager;
        this.pluginManager = pluginManager;
        CascadeRemoveManager crm = new CascadeRemoveManager(pipeLineManager);

        // Init the popup menus
        dataSetMenu = new DataSetPopupMenu(pipeLineManager, crm);
        lookupTableMenu = new LookupTablePopupMenu(pipeLineManager, crm);
        actorMenu = new ActorPopupMenu(pipeLineManager, crm);
        txtActorMenu = new TxtActorPopupMenu(pipeLineManager, crm);
        scalarBarMenu = new ScalarBarPopupMenu(pipeLineManager, crm);
        mapperMenu = new MapperPopupMenu(pipeLineManager, crm);
    }

    private JPopupMenu getPopup() {
        JPopupMenu result = (JPopupMenu) vtkObject.getMetaData().get(VtkObject.POPUP_MENU);
        if (result != null) {
            return result;
        }

        switch (vtkObject.getType()) {
        case VtkObject.ACTOR:
            return actorMenu;
        case VtkObject.SCALAR_BAR:
            return scalarBarMenu;
        case VtkObject.TXT_ACTOR:
            return txtActorMenu;
        case VtkObject.MAPPER:
            return mapperMenu;
        case VtkObject.DATASET:
            return dataSetMenu;
        case VtkObject.LOOKUP_TABLE:
            return lookupTableMenu;
        }

        return null;
    }

    public void showPopupMenu(Component invoker, int x, int y, VtkObject vtkObject) {
        this.vtkObject = vtkObject;
        this.currentMenu = getPopup();
        if (currentMenu != null) {
            if (currentMenu instanceof VtkObjectPopupMenu) {
                ((VtkObjectPopupMenu) currentMenu).setCurrentVtkOject(vtkObject);
            }

            currentMenu.show(invoker, x, y);
        }
    }
}
