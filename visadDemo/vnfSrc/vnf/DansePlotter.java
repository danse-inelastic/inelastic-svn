/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
 */

package vnf;

// Import needed classes


import visad.ConstantMap;
import visad.DataReferenceImpl;
import visad.Display;
import visad.DisplayImpl;
import visad.DisplayRenderer;
import visad.FlatField;
import visad.FunctionType;
import visad.GraphicsModeControl;
import visad.Gridded1DSet;
import visad.Gridded2DSet;
import visad.Integer2DSet;
import visad.Linear1DSet;
import visad.RealTupleType;
import visad.RealType;
import visad.SI;
import visad.ScalarMap;
import visad.Set;
import visad.VisADException;
import visad.java2d.DisplayImplJ2D;
import visad.java2d.DisplayRendererJ2D;

import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.regex.Pattern;
import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;

import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

import net.sf.vfsjfilechooser.VFSJFileChooser;
import net.sf.vfsjfilechooser.VFSJFileChooser.RETURN_TYPE;
import net.sf.vfsjfilechooser.VFSJFileChooser.SELECTION_MODE;
import net.sf.vfsjfilechooser.accessories.DefaultAccessoriesPanel;
import net.sf.vfsjfilechooser.utils.VFSUtils;

import org.apache.commons.vfs.FileObject;
import org.apache.commons.vfs.FileSystemException;


/**
 * Danse Plotter
 */

//TODO: create an openFile method that takes the type of file as argument.  Instantiate file chooser inside of it and get rid of passing reference.
//TODO: break the menu bar out into a separate class

public class DansePlotter {

	// Declare variables for 1D Plotter
	private RealType x, y;
	private FunctionType func_domain_range;

	// Our Data values for x are represented by the set
	private Gridded1DSet x_set;

	// The Data class FlatField, which will hold time and height data
	// and the same for speed
	private FlatField data_ff;
	// The DataReference from the data to display
	private DataReferenceImpl data_ref;

	// The 2D display, and its the maps
	private DisplayImpl display;
	private ScalarMap xMap, yMap;



	// Declare additional variables for "image" plotter 
	private RealType z;
	private RealTupleType domain_tuple;
	private Set domain_set;
	// The 2D display, and its the maps
	private ScalarMap imageMap;

	//private JFileChooser fc;
	static JFrame jframe;

	public DansePlotter(String[] args) throws RemoteException,
	VisADException {
		// Create the quantities
		// Use RealType(String name, Unit u, Set set), set is null
		x = RealType.getRealType("x", null, null);
		y = RealType.getRealType("y", null, null);
		func_domain_range = new FunctionType(x, y);
		float[][] x_vals = new float[][]{{0}};
		//float[][] x_vals = new float[][]{{1.0f, 2.0f, 3.0f}};
		x_set = new Gridded1DSet(x, x_vals, x_vals[0].length);
		//float[][] y_vals = new float[][]{{1.0f, 1.0f, 1.0f}};
		float[][] y_vals = new float[][]{{0.0f}};
		// Create the FlatField
		data_ff = new FlatField(func_domain_range, x_set);
		// and put the y values above in it
		data_ff.setSamples(y_vals);
		// Create Display and its maps
		display = new DisplayImplJ2D("display1");

		// Get display's graphics mode control and draw scales
		GraphicsModeControl dispGMC = display.getGraphicsModeControl();
		dispGMC.setScaleEnable(true);
		dispGMC.setLineWidth(2.0f);
		// Create the ScalarMaps: 
		xMap = new ScalarMap(x, Display.XAxis);
		yMap = new ScalarMap(y, Display.YAxis);
		// Add maps to display
		display.addMap(xMap);
		display.addMap(yMap);
		// create reference and add it to display
		data_ref = new DataReferenceImpl("x_y_ref");
		data_ref.setData(data_ff);
		display.addReference(data_ref);

		final PlotterMenu menuBar = new PlotterMenu();
		
		// Create application window, put display into it

		jframe = new JFrame("Danse Plotter");
		jframe.setJMenuBar(menuBar);
		jframe.getContentPane().add(display.getComponent());

		// Set window size and make it visible
		jframe.setSize(700, 700);
		jframe.setVisible(true);
		
	}


	public static void main(String[] args) throws RemoteException,
	VisADException {
		new DansePlotter(args);
	}

} // end of Visad Tutorial Program 2_08
