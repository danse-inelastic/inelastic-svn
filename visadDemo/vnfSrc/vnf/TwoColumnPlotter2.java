/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
 */

package vnf;

// Import needed classes

import visad.*;
import visad.java2d.DisplayImplJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

/**
 * Somewhat different version of program P2_07 We reorganize the MathType of
 * example P2_07 ( time -> (height, speed) ) as ( time -> height ) and ( time ->
 * speed ) When then plot time (along x-axis) against height and speed, both
 * (along y-axis) The color of speed display is changed to match the line color
 * os speed
 */

public class TwoColumnPlotter2 {

	// Declare variables
	// The quantities to be displayed in x- and y-axes

	private RealType time, height;
	private RealType black;

	// The functions ( time -> height )
	// and ( time -> speed )

	private FunctionType func_t_h;

	// Our Data values for x are represented by the set

	private Set time_set;

	// The Data class FlatField, which will hold time and height data
	// and the same for speed

	private FlatField height_ff;

	// The DataReference from the data to display

	private DataReferenceImpl t_h_ref;

	// The 2D display, and its the maps

	private DisplayImpl display;
	private ScalarMap blackXMap, blackYMap;
	private ScalarMap blackMap;
	private ScalarMap timeMap, heightYMap;

	public TwoColumnPlotter2(String[] args) throws RemoteException,
			VisADException {

		// Create the quantities
		// x and y are measured in SI meters
		// Use RealType(String name, Unit u, Set set), set is null

		time = RealType.getRealType("time", SI.second, null);
		height = RealType.getRealType("height", SI.meter, null);

		// Create a FunctionType, that is the class which represents the
		// function y = f(x)
		// Use FunctionType(MathType domain, MathType range)

		func_t_h = new FunctionType(time, height);

		// Create the time_set, with 5 values, but this time using a
		// Linear1DSet(MathType type, double first, double last, int length)

		int LENGTH = 32;
		time_set = new Linear1DSet(time, -3.0, 3.0, LENGTH);

		// Generate some points with a for-loop for the line
		// Note that we have the parabola height = 45 - 5 * time^2
		// But first we create a float array for the values

		float[][] h_vals = new float[1][LENGTH];
		float[][] s_vals = new float[1][LENGTH];

		// ...then we use a method of Set to get the samples from time_set;
		// this call will get the time values
		// "true" means we get a copy from the samples

		float[][] t_vals = time_set.getSamples(true);

		// finally generate height and speed values
		// height is given by the parabola height = 45 - 5 * time^2
		// and speed by its first derivative speed = -10 * time

		for (int i = 0; i < LENGTH; i++) {

			// height values...
			h_vals[0][i] = 45.0f - 5.0f * (float) (t_vals[0][i] * t_vals[0][i]);

			// ...and speed values: the derivative of the above function
			s_vals[0][i] = -10.0f * (float) t_vals[0][i];
		}

		// Create the FlatFields
		// Use FlatField(FunctionType type, Set domain_set)

		height_ff = new FlatField(func_t_h, time_set);

		// and put the y values above in it

		height_ff.setSamples(h_vals);

		// Create Display and its maps

		// A 2D display

		display = new DisplayImplJ2D("display1");

		// Get the display renderer
		DisplayRenderer dRenderer = display.getDisplayRenderer();

		// Set the display background color
		dRenderer.setBackgroundColor(Color.white);

		// Create the quantities
		// Use RealType(String name, Unit unit, Set set);

		black = RealType.getRealType("BLACK", null, null);

		// Create the ScalarMaps: latitude to XAxis, longitude to YAxis and
		// rgbVal to ZAxis and to RGB
		// Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

		blackXMap = new ScalarMap(black, Display.XAxis);
		blackYMap = new ScalarMap(black, Display.YAxis);
		blackXMap.setScalarName("x");
		blackYMap.setScalarName("y");

		blackMap = new ScalarMap(black, Display.Red);

		// Add maps to display

		display.addMap(blackXMap);
		display.addMap(blackYMap);
		display.addMap(blackMap);

		// Set axes colors

		float[] b1 = colorToFloats(Color.black);
		blackXMap.setScaleColor(b1);
		float[] b2 = colorToFloats(Color.black);
		blackYMap.setScaleColor(b2);

		// Get display's graphics mode control and draw scales

		GraphicsModeControl dispGMC = (GraphicsModeControl) display
				.getGraphicsModeControl();
		dispGMC.setScaleEnable(true);
		dispGMC.setLineWidth(2.0f);

		// Create the ScalarMaps: quantity time is to be displayed along XAxis,
		// and height and speed along YAxis
		// Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

		timeMap = new ScalarMap(time, Display.XAxis);

		heightYMap = new ScalarMap(height, Display.YAxis);

		// Add maps to display

		display.addMap(timeMap);
		display.addMap(heightYMap);

		// Scale heightYMap
		// we simply choose the range from 0.0 to 50.0

		heightYMap.setRange(0.0, 50.0);
		
	    // Choose yellow as the color for the speed curve

	    float heightRed = 1.0f;
	    float heightGreen = 1.0f;
	    float heightBlue = 0.0f;


	    float[] heightColor = new float[]{heightRed, heightGreen, heightBlue};

	    // ...and color the axis with the same yellow

	    heightYMap.setScaleColor( heightColor );

		// Create a data reference and set the FlatField as our data

		t_h_ref = new DataReferenceImpl("t_h_ref");

		t_h_ref.setData(height_ff);
		
	    // Create Constantmaps for speed and add its reference to display

	    ConstantMap[] heightCMap = {  new ConstantMap( heightRed, Display.Red),
	        		        new ConstantMap( heightGreen, Display.Green),
	        		        new ConstantMap( heightBlue, Display.Blue),
	        		        new ConstantMap( 1.50f, Display.LineWidth)};

		// Add reference to display

		display.addReference(t_h_ref, heightCMap);

		final JMenuBar menuBar = new JMenuBar();
		

		// Create application window, put display into it

		JFrame jframe = new JFrame("VisAD Tutorial example 2_08");
		jframe.setJMenuBar(menuBar);
		jframe.getContentPane().add(display.getComponent());
		
		//Build the first menu.
		JMenu menu;
		menu = new JMenu("File");
		//menu.setMnemonic(KeyEvent.VK_A);
		//menu.getAccessibleContext().setAccessibleDescription("The only menu in this program that has menu items");
		menuBar.add(menu);

		final JMenuItem newItemMenuItem = new JMenuItem();
		newItemMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				openTwoColumn()
			}
		});
		newItemMenuItem.setText("Open");
		menu.add(newItemMenuItem);

		final JMenuItem newItemMenuItem_1 = new JMenuItem();
		newItemMenuItem_1.setText("Save");
		menu.add(newItemMenuItem_1);

		final JMenuItem newItemMenuItem_2 = new JMenuItem();
		newItemMenuItem_2.setText("Exit");
		menu.add(newItemMenuItem_2);


		// Set window size and make it visible

		jframe.setSize(300, 300);
		jframe.setVisible(true);

	}

	/*
	 * Utility method to transform a Java color in an array of rgb components
	 * between 0 and 1
	 */
	private float[] colorToFloats(Color c) {

		float[] rgb = new float[] { 0.5f, 0.5f, 0.5f }; // init with gray
		if (c != null) {
			rgb[0] = (float) c.getRed() / 255.0f;
			rgb[1] = (float) c.getGreen() / 255.0f;
			rgb[2] = (float) c.getBlue() / 255.0f;

		}

		return rgb;
	}
	
	private void openTwoColumn() {
		
		int returnVal = fc.showOpenDialog(FileChooserDemo.this);

        if (returnVal == JFileChooser.APPROVE_OPTION) {
            File file = fc.getSelectedFile();
            //This is where a real application would open the file.
            log.append("Opening: " + file.getName() + "." + newline);
        } else {
            log.append("Open command cancelled by user." + newline);
        }

		String base = "http://trueblue.caltech.edu/java";//System.getProperty("user.dir");
		String[] args = new String[10];
		String atomsContent = getURLContentAsString(base + File.separatorChar
				+ "atoms.html");
		String latticeContent = getURLContentAsString(base + File.separatorChar
				+ "lattice.html");
		//put atoms in args
		args[0] = atomsContent;
		//put lattice in args
		Pattern p = Pattern.compile("\n");
		String[] coordLines = p.split(latticeContent);
		p = Pattern.compile("\\s");
		String[] coords = p.split(coordLines[0]);
		args[1] = coords[0];
		args[2] = coords[1];
		args[3] = coords[2];
		coords = p.split(coordLines[1]);
		args[4] = coords[0];
		args[5] = coords[1];
		args[6] = coords[2];
		coords = p.split(coordLines[2]);
		args[7] = coords[0];
		args[8] = coords[1];
		args[9] = coords[2];
	}

	public static void main(String[] args) throws RemoteException,
			VisADException {
		new TwoColumnPlotter2(args);
	}

} // end of Visad Tutorial Program 2_08
