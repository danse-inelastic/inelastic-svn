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
import visad.Linear1DSet;
import visad.RealType;
import visad.SI;
import visad.ScalarMap;
import visad.Set;
import visad.VisADException;
import visad.java2d.DisplayImplJ2D;

import java.rmi.RemoteException;
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
 * Somewhat different version of program P2_07 We reorganize the MathType of
 * example P2_07 ( time -> (height, speed) ) as ( time -> height ) and ( time ->
 * speed ) When then plot time (along x-axis) against height and speed, both
 * (along y-axis) The color of speed display is changed to match the line color
 * os speed
 */

public class TwoColumnPlotter2 {

	// Declare variables
	// The quantities to be displayed in x- and y-axes

	private RealType x, y;
	private RealType black;

	// The functions ( time -> height )
	// and ( time -> speed )

	private FunctionType func_x_y;

	// Our Data values for x are represented by the set

	private Gridded1DSet x_set;

	// The Data class FlatField, which will hold time and height data
	// and the same for speed

	private FlatField y_ff;

	// The DataReference from the data to display

	private DataReferenceImpl x_y_ref;

	// The 2D display, and its the maps

	private DisplayImpl display;
	private ScalarMap blackXMap, blackYMap;
	private ScalarMap blackMap;
	private ScalarMap xMap, yMap;

	//private JFileChooser fc;
	private static JFrame jframe;

	public TwoColumnPlotter2(String[] args) throws RemoteException,
	VisADException {

		// Create the quantities
		// x and y are measured in SI meters
		// Use RealType(String name, Unit u, Set set), set is null

		x = RealType.getRealType("x", null, null);
		y = RealType.getRealType("y", null, null);

		// Create a FunctionType, that is the class which represents the
		// function y = f(x)
		// Use FunctionType(MathType domain, MathType range)

		func_x_y = new FunctionType(x, y);

		// Create the time_set, with 5 values, but this time using a
		// Linear1DSet(MathType type, double first, double last, int length)

		float[][] x_vals = new float[][]{{0}};
		x_set = new Gridded1DSet(x, x_vals, x_vals.length);

		// Generate some points with a for-loop for the line
		// Note that we have the parabola height = 45 - 5 * time^2
		// But first we create a float array for the values

		//		float[][] y_vals = new float[1][LENGTH];

		// Create the FlatFields
		// Use FlatField(FunctionType type, Set domain_set)

		y_ff = new FlatField(func_x_y, x_set);

		//		// and put the y values above in it
		//
		//		y_ff.setSamples(y_vals);

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

		GraphicsModeControl dispGMC = display.getGraphicsModeControl();
		dispGMC.setScaleEnable(true);
		dispGMC.setLineWidth(2.0f);

		// Create the ScalarMaps: quantity time is to be displayed along XAxis,
		// and height and speed along YAxis
		// Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

		xMap = new ScalarMap(x, Display.XAxis);

		yMap = new ScalarMap(y, Display.YAxis);

		// Add maps to display

		display.addMap(xMap);
		display.addMap(yMap);

		// Scale heightYMap
		// we simply choose the range from 0.0 to 50.0

		yMap.setRange(0.0, 50.0);

		// Choose yellow as the color for the speed curve

		float yRed = 0.0f;
		float yGreen = 0.0f;
		float yBlue = 0.0f;


		float[] yColor = new float[]{yRed, yGreen, yBlue};

		// ...and color the axis with the same yellow

		yMap.setScaleColor( yColor );

		// Create a data reference and set the FlatField as our data

		x_y_ref = new DataReferenceImpl("x_y_ref");

		x_y_ref.setData(y_ff);

		//		// Create Constantmaps for speed and add its reference to display
		//
		//		ConstantMap[] heightCMap = {  new ConstantMap( yRed, Display.Red),
		//				new ConstantMap( yGreen, Display.Green),
		//				new ConstantMap( yBlue, Display.Blue),
		//				new ConstantMap( 1.50f, Display.LineWidth)};
		//
		//		// Add reference to display
		//
		//		display.addReference(x_y_ref, heightCMap);

		final JMenuBar menuBar = new JMenuBar();


		// Create application window, put display into it

		jframe = new JFrame("Danse Plotter");
		jframe.setJMenuBar(menuBar);
		jframe.getContentPane().add(display.getComponent());

		//Build the first menu.
		JMenu menu;
		menu = new JMenu("File");
		//menu.setMnemonic(KeyEvent.VK_A);
		//menu.getAccessibleContext().setAccessibleDescription("The only menu in this program that has menu items");
		menuBar.add(menu);

		// create a file chooser
		final VFSJFileChooser fileChooser = new VFSJFileChooser();
		final JMenuItem newItemMenuItem = new JMenuItem();
		newItemMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				// configure the file dialog
				fileChooser.setAccessory(new DefaultAccessoriesPanel(fileChooser));
				fileChooser.setFileHidingEnabled(false);
				fileChooser.setMultiSelectionEnabled(false);
				fileChooser.setFileSelectionMode(SELECTION_MODE.FILES_ONLY);

				// show the file dialog
				RETURN_TYPE answer = fileChooser.showOpenDialog(TwoColumnPlotter2.jframe);

				// check if a file was selected
				if (answer == RETURN_TYPE.APPROVE){
					final FileObject aFileObject = fileChooser.getSelectedFile();

					// retrieve an input stream and read in all of the file contents at once
					String fileContents;
					try {
						InputStream is = VFSUtils.getInputStream(aFileObject);
						fileContents = convertStreamToString(is);

						//process file contents

						//split by newlines
						Pattern newLinePattern = Pattern.compile("\n");
						String[] dataLines = newLinePattern.split(fileContents);
						int numDataPoints = dataLines.length;
						float[][] x_vals = new float[1][numDataPoints];
						float[][] y_vals = new float[1][numDataPoints];

						//split the lines by white space
						Pattern whitespacePattern = Pattern.compile("\\s"); 
						for (int i=0; i<numDataPoints; i++){ //(String dataLine : dataLines) {
							String[] data = whitespacePattern.split(dataLines[i]);
							x_vals[0][i] = Float.valueOf(data[0].trim()).floatValue();
							y_vals[0][i] = Float.valueOf(data[1].trim()).floatValue();
						}
						x_set = new Gridded1DSet(x, x_vals, x_vals[0].length);
						y_ff = new FlatField( func_x_y, x_set);
						// and put the y values above in it
						y_ff.setSamples( y_vals );

						//						  private static final String ID = TwoColumnPlotter2.class.getName();
						//
						//						  private static DefaultFamily form = new DefaultFamily(ID);

					} catch (FileSystemException e) {
						e.printStackTrace();
					}  catch (VisADException e) {
						e.printStackTrace();
					} catch (RemoteException e) {
						e.printStackTrace();
					}
					//replot
					//jframe.repaint();

					display.reDisplayAll();
					jframe.setVisible(true);
				    jframe.toFront();
					// remove authentication credentials from the file path
					//final String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
				}
			}
		});
		newItemMenuItem.setText("Open");
		menu.add(newItemMenuItem);

		final JMenuItem newItemMenuItem_1 = new JMenuItem();
		newItemMenuItem_1.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				// configure the file dialog
				fileChooser.setAccessory(new DefaultAccessoriesPanel(fileChooser));
				fileChooser.setFileHidingEnabled(false);
				fileChooser.setMultiSelectionEnabled(false);
				fileChooser.setFileSelectionMode(SELECTION_MODE.FILES_ONLY);
				// show the file dialog
				RETURN_TYPE answer = fileChooser.showOpenDialog(TwoColumnPlotter2.jframe);
				// check if a file was selected
				if (answer == RETURN_TYPE.APPROVE){
					final FileObject aFileObject = fileChooser.getSelectedFile();
					// retrieve an input stream and read in all of the file contents at once
					String fileContents;
					try {
						// get an output stream and buffer it
						OutputStream os = VFSUtils.getOutputStream(aFileObject);	
					} catch (FileSystemException e) {
						e.printStackTrace();
					}
					// remove authentication credentials from the file path
					//final String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
				}
			}
		});
		newItemMenuItem_1.setText("Save");
		menu.add(newItemMenuItem_1);

		final JMenuItem newItemMenuItem_2 = new JMenuItem();
		newItemMenuItem_2.setText("Exit");
		menu.add(newItemMenuItem_2);

		// Set window size and make it visible
		jframe.setSize(700, 700);
		jframe.setVisible(true);

	}

	/*
	 * Utility method to transform a Java color in an array of rgb components
	 * between 0 and 1
	 */
	private float[] colorToFloats(Color c) {
		float[] rgb = new float[] { 0.5f, 0.5f, 0.5f }; // init with gray
		if (c != null) {
			rgb[0] = c.getRed() / 255.0f;
			rgb[1] = c.getGreen() / 255.0f;
			rgb[2] = c.getBlue() / 255.0f;
		}
		return rgb;
	}

	public String convertStreamToString(InputStream is) {
		/*
		 * To convert the InputStream to String we use the BufferedReader.readLine()
		 * method. We iterate until the BufferedReader return null which means
		 * there's no more data to read. Each line will appended to a StringBuilder
		 * and returned as String.
		 */
		BufferedReader reader = new BufferedReader(new InputStreamReader(is));
		StringBuilder sb = new StringBuilder();
		String line = null;
		try {
			while ((line = reader.readLine()) != null) {
				sb.append(line + "\n");
			}
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				is.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		} 
		return sb.toString();
	}

	//	private void openTwoColumn() {
	//		String fileName;
	//		
	//		
	//		int returnVal = fc.showOpenDialog(jframe);
	//		//int returnVal = fc.showOpenDialog(display.getComponent());
	//
	//        if (returnVal == JFileChooser.APPROVE_OPTION) {
	//            fileName = fc.getSelectedFile().getAbsolutePath();
	//        }
	//
	//		String atomsContent = getURLContentAsString("file://"+fileName);
	//	}

	//	public void importCoordinates(String fileContents) {
	//		// this method expects coordinates to be in xyz format!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	//		Scanner in = new Scanner(fileContents);
	//		int numOfLines = in.nextInt();
	//		in.nextLine();
	//		in.nextLine();
	//		data.clear();
	//		data.ensureCapacity(numOfLines);
	//
	//		// add rows manually for speed
	//		for (int i = 0; i < numOfLines; i++) {
	//			String[] row = new String[COLUMN_NAMES.length];
	//			for (int j = 0; j < row.length; j++)
	//				row[j] = "";
	//			row[indices[0]] = in.next();
	//			row[indices[2]] = in.next();
	//			row[indices[3]] = in.next();
	//			row[indices[4]] = in.next();
	//			data.add(row);
	//		}
	//		in.close();
	//	}


	public static void main(String[] args) throws RemoteException,
	VisADException {
		new TwoColumnPlotter2(args);
	}

} // end of Visad Tutorial Program 2_08
