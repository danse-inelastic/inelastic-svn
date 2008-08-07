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
package com.artenum.cassandra.plugin;

import java.awt.Color;
import java.awt.Component;

import java.util.ArrayList;
import java.util.Collection;

import javax.swing.AbstractListModel;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.ListCellRenderer;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> The PluginManager keeps track of the plugin instances.
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
public class PluginManager extends AbstractListModel implements ListCellRenderer {
    private ArrayList pluginList;
    private JLabel renderer;
    private Color selectedColor;
    private Color defaultColor;

    public PluginManager() {
        pluginList = new ArrayList();
        renderer = new JLabel();
        renderer.setOpaque(true);
        selectedColor = new Color(100, 100, 200);
        defaultColor = Color.white;
    }

    public int getSize() {
        return pluginList.size();
    }

    public Object getElementAt(int index) {
        return pluginList.get(index);
    }

    public void addPlugin(CassandraPlugin plugin) {
        pluginList.add(plugin);
        fireIntervalAdded(this, getSize() - 1, getSize() - 1);
    }

    public void removePlugin(CassandraPlugin plugin) {
        int index = pluginList.indexOf(plugin);
        if (index != -1) {
            pluginList.remove(index);
        }

        fireIntervalRemoved(this, index, index);
    }

    public CassandraPlugin getPlugin(int index) {
        return ((CassandraPlugin) pluginList.get(index));
    }

    public CassandraPlugin getLastPlugin() {
        return getPlugin(getSize() - 1);
    }

    public Collection getData() {
        return pluginList;
    }

    public Component getListCellRendererComponent(JList list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
        renderer.setBackground(isSelected ? selectedColor : defaultColor);
        renderer.setText(value.toString() + " (" + index + ")");
        return renderer;
    }
}
