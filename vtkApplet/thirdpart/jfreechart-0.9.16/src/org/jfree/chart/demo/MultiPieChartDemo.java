/* ===========================================================
 * JFreeChart : a free chart library for the Java(tm) platform
 * ===========================================================
 *
 * (C) Copyright 2000-2004, by Object Refinery Limited and Contributors.
 *
 * Project Info:  http://www.jfree.org/jfreechart/index.html
 *
 * This library is free software; you can redistribute it and/or modify it under the terms
 * of the GNU Lesser General Public License as published by the Free Software Foundation;
 * either version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License along with this
 * library; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 * [Java is a trademark or registered trademark of Sun Microsystems, Inc. 
 * in the United States and other countries.]
 *
 * ----------------------
 * MultiPieChartDemo.java
 * ----------------------
 * (C) Copyright 2002-2004, by Object Refinery Limited and Contributors.
 *
 * Original Author:  David Gilbert (for Object Refinery Limited);
 * Contributor(s):   -;
 *
 * $Id: MultiPieChartDemo.java,v 1.10 2004/01/03 05:11:00 mungady Exp $
 *
 * Changes
 * -------
 * 21-Aug-2002 : Version 1 (DG);
 * 11-Oct-2002 : Fixed errors reported by Checkstyle (DG);
 *
 */

package org.jfree.chart.demo;

import java.awt.Color;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PiePlot;
import org.jfree.data.CategoryDataset;
import org.jfree.data.DatasetUtilities;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

/**
 * A simple demonstration application showing how to create a chart consisting of multiple
 * pie charts.
 *
 * @author David Gilbert
 */
public class MultiPieChartDemo extends ApplicationFrame {

    /**
     * Creates a new demo.
     *
     * @param title  the frame title.
     */
    public MultiPieChartDemo(String title) {

        super(title);

        // create a dataset...
        double[][] data = new double[][] {
            {3.0, 4.0, 3.0, 5.0},
            {5.0, 7.0, 6.0, 8.0},
            {5.0, 7.0, 3.0, 8.0},
            {1.0, 2.0, 3.0, 4.0},
            {2.0, 3.0, 2.0, 3.0}
        };

        CategoryDataset dataset = DatasetUtilities.createCategoryDataset(
            "Region ",
            "Sales/Q",
            data
        );

        // create the chart...
        JFreeChart chart = ChartFactory.createPieChart(
            "Multi Pie Chart",  // chart title
            dataset,            // data
            PiePlot.PER_ROW,
            true,               // include legend
            true,
            false
        );

        // NOW DO SOME OPTIONAL CUSTOMISATION OF THE CHART...

        chart.setBackgroundPaint(Color.yellow);
        PiePlot plot = (PiePlot) chart.getPlot();
        plot.setSectionLabelType(PiePlot.VALUE_AND_PERCENT_LABELS);

        // OPTIONAL CUSTOMISATION COMPLETED.

        // add the chart to a panel...
        ChartPanel chartPanel = new ChartPanel(chart, true, true, true, false, true);
        chartPanel.setPreferredSize(new java.awt.Dimension(600, 380));
        setContentPane(chartPanel);

    }

    // ****************************************************************************
    // * JFREECHART DEVELOPER GUIDE                                               *
    // * The JFreeChart Developer Guide, written by David Gilbert, is available   *
    // * to purchase from Object Refinery Limited:                                *
    // *                                                                          *
    // * http://www.object-refinery.com/jfreechart/guide.html                     *
    // *                                                                          *
    // * Sales are used to provide funding for the JFreeChart project - please    * 
    // * support us so that we can continue developing free software.             *                                             *
    // ****************************************************************************
    
    /**
     * Starting point for the demonstration application.
     *
     * @param args  ignored.
     */
    public static void main(String[] args) {

        MultiPieChartDemo demo = new MultiPieChartDemo("Multi Pie Chart Demo");
        demo.pack();
        RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);

    }

}
