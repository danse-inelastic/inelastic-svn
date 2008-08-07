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

import com.artenum.cassandra.PreferenceListener;
import com.artenum.cassandra.pipeline.PipeLineManager;
import com.artenum.cassandra.pipeline.VtkObjectListModel;
import com.artenum.cassandra.pipeline.graph.VtkPipeLineGraphModel;
import com.artenum.cassandra.pipeline.graph.VtkPipeLinePanel;
import com.artenum.cassandra.plugin.PluginManager;

import com.artenum.jyconsole.JyConsole;

import java.awt.BorderLayout;

import java.io.File;

import java.util.Hashtable;

import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Global GUI of Cassandra.
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
public class CassandraGUI extends JPanel implements PreferenceListener {
    public static final String PREF_SCRIPT_DIR = "cassandra.pref.script.dir";
    private JSplitPane pipeLine_renderer;
    private JSplitPane console;
    private JyConsole consolePython;
    private Hashtable prefTable;

    //
    private VtkPipeLineGraphModel graphModel;

    public CassandraGUI(PipeLineManager pipeLineManager, PluginManager pluginManager) {
        super(new BorderLayout());
        consolePython = new JyConsole();
        //
        JTabbedPane tabPane = new JTabbedPane();
        tabPane.addTab("View",
            new JScrollPane(new ActorList(new String[] { "Actor", "Scalar bar", "Text" },
                    new VtkObjectListModel[] { pipeLineManager.getActorList(), pipeLineManager.getScalarBarList(), pipeLineManager.getTextActorList() },
                    pipeLineManager)));
        tabPane.addTab("Tree", new JScrollPane(new CassandraTree(pipeLineManager, pluginManager)));
        graphModel = new VtkPipeLineGraphModel(pipeLineManager, pluginManager);
        tabPane.addTab("Pipeline", new JScrollPane(new VtkPipeLinePanel(graphModel)));
        //
        pipeLine_renderer = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, tabPane, pipeLineManager.getCassandraView());
        pipeLine_renderer.setOneTouchExpandable(true);
        console = new JSplitPane(JSplitPane.VERTICAL_SPLIT, pipeLine_renderer, consolePython);
        console.setOneTouchExpandable(true);
        add(console, BorderLayout.CENTER);
        pipeLine_renderer.setDividerLocation(0.5);
    }

    public void showConsole() {
        console.setDividerLocation(0.5);
    }

    public void hideConsole() {
        console.setDividerLocation(50000);
    }

    public void showPipeLine() {
        pipeLine_renderer.setDividerLocation(0.5);
    }

    public void hidePipeLine() {
        pipeLine_renderer.setDividerLocation(0);
    }

    public void showRenderer() {
        pipeLine_renderer.setDividerLocation(0.5);
    }

    public void hideRenderer() {
        pipeLine_renderer.setDividerLocation(50000);
    }

    public JyConsole getPyConsole() {
        return consolePython;
    }

    public void preferenceChanged() {
        if ((prefTable != null) && (prefTable.get(PREF_SCRIPT_DIR) != null)) {
            consolePython.getPreferences().put(JyConsole.PREF_SCRIPT_DIR, ((File) prefTable.get(PREF_SCRIPT_DIR)).getAbsolutePath());
        }
    }

    public void setPreferences(Hashtable prefTable) {
        this.prefTable = prefTable;
    }

    public void update() {
        graphModel.contentsChanged(null);
    }
}
