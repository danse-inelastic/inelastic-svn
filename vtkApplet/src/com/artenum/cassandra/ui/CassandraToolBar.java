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

import com.artenum.cassandra.action.CassandraActionListener;

import javax.swing.JButton;
import javax.swing.JToolBar;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> The Cassandra toolbar
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
public class CassandraToolBar extends JToolBar {
    private JButton print;
    private JButton xy;
    private JButton xz;
    private JButton yz;
    private JButton resetCamera;
    private CassandraActionListener listener;

    public CassandraToolBar(CassandraActionListener listener) {
        this.listener = listener;

        //
        print = new JButton("Save image");
        print.setActionCommand(CassandraActionListener.SAVE_VTK_VIEW);
        print.addActionListener(listener);
        xy = new JButton("XY");
        xy.setActionCommand(CassandraActionListener.SET_VIEW_XY);
        xy.addActionListener(listener);
        xz = new JButton("XZ");
        xz.setActionCommand(CassandraActionListener.SET_VIEW_XZ);
        xz.addActionListener(listener);
        yz = new JButton("YZ");
        yz.setActionCommand(CassandraActionListener.SET_VIEW_YZ);
        yz.addActionListener(listener);
        resetCamera = new JButton("Reset view");
        resetCamera.setActionCommand(CassandraActionListener.RESET_VIEW);
        resetCamera.addActionListener(listener);

        //
        add(print);
        add(xy);
        add(xz);
        add(yz);
        add(resetCamera);
    }
}
