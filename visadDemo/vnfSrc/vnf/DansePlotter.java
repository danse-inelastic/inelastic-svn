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
	private RealType black;
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
	private ScalarMap blackXMap, blackYMap;
	private ScalarMap blackMap;
	private ScalarMap xMap, yMap;



	// Declare additional variables for "image" plotter 
	private RealType z;
	private RealTupleType domain_tuple;
	private Set domain_set;
	// The 2D display, and its the maps
	private ScalarMap imageMap;

	//private JFileChooser fc;
	private static JFrame jframe;

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

		final JMenuBar menuBar = new JMenuBar();
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
				openTwoColumnAscii(fileChooser);
			}
		});
		newItemMenuItem.setText("Open Two Column Ascii");
		menu.add(newItemMenuItem);

		final JMenuItem newItemMenuItem_3 = new JMenuItem();
		newItemMenuItem_3.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				openTrajectory(fileChooser);
			}
		});
		newItemMenuItem_3.setText("Open Trajectory");
		menu.add(newItemMenuItem_3);
		
		final JMenuItem newItemMenuItem_3p5 = new JMenuItem();
		newItemMenuItem_3p5.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				openImage(fileChooser);
			}
		});
		newItemMenuItem_3p5.setText("Open Image");
		menu.add(newItemMenuItem_3p5);

		final JMenuItem newItemMenuItem_1 = new JMenuItem();
		newItemMenuItem_1.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				saveTwoColumnAscii(fileChooser);
			}
		});
		newItemMenuItem_1.setText("Save");
		menu.add(newItemMenuItem_1);

		final JMenuItem newItemMenuItem_2 = new JMenuItem();
		newItemMenuItem_2.setText("Exit");
		menu.add(newItemMenuItem_2);

		// Create application window, put display into it

		jframe = new JFrame("Danse Plotter");
		jframe.setJMenuBar(menuBar);
		jframe.getContentPane().add(display.getComponent());

		// Set window size and make it visible
		jframe.setSize(700, 700);
		jframe.setVisible(true);

	}
	
	private void openImage(VFSJFileChooser fileChooser) {
		// reads a set of values from a file in grid formation
		
		// configure the file dialog
		fileChooser.setAccessory(new DefaultAccessoriesPanel(fileChooser));
		fileChooser.setFileHidingEnabled(false);
		fileChooser.setMultiSelectionEnabled(false);
		fileChooser.setFileSelectionMode(SELECTION_MODE.FILES_ONLY);

		// show the file dialog
		RETURN_TYPE answer = fileChooser.showOpenDialog(DansePlotter.jframe);

		// check if a file was selected
		if (answer == RETURN_TYPE.APPROVE){
			final FileObject aFileObject = fileChooser.getSelectedFile();

			// retrieve an input stream and read in all of the file contents at once
			String fileContents;
			try {
				InputStream is = VFSUtils.getInputStream(aFileObject);
				//fileContents = convertStreamToString(is);
				
				//split the lines by white space
				Pattern whitespacePattern = Pattern.compile("\\s"); 
				BufferedReader reader = new BufferedReader(new InputStreamReader(is));
				String line = null;
				ArrayList<float[]> rawData = new ArrayList<float[]>();
				try {
					while ((line = reader.readLine()) != null) {
						String[] splitLine = whitespacePattern.split(line);
						float[] lineNumbers = new float[splitLine.length];
						for(int i=0; i< splitLine.length; i++){
							lineNumbers[i] = Float.valueOf(splitLine[i].trim()).floatValue();
						}
						rawData.add(lineNumbers);
					}
				} catch (IOException e) {
					e.printStackTrace();
				}
				int numXData = rawData.get(0).length;
				int numYData = rawData.size();
				float[][] zRaw = (float[][])rawData.toArray();
				
			    float[][] flat_samples = new float[1][numXData*numYData];

			    // ...and then we fill our 'flat' array with the original values
			    // Note that the pixel values indicate the order in which these values
			    // are stored in flat_samples
			    for(int c = 0; c < numXData; c++)
			      for(int r = 0; r < numYData; r++)
			    	  
			    	  flat_samples[0][ c * numYData + r ] = zRaw[r][c];
//				// Create the domain tuple
//				domain_tuple = new RealTupleType(x, y);				
//				z = RealType.getRealType("z");
//				func_domain_range = new FunctionType( domain_tuple, z);
//				//domain_set = new Gridded2DSet(domain_tuple, xy_vals, xy_vals[0].length);
//				domain_set = new Integer2DSet(domain_tuple, xy_vals[0].length, xy_vals[0].length);
//				// redo the flatfield to contain image data
//				// Use FlatField(FunctionType type, Set domain_set)
				data_ff = new FlatField( func_domain_range, domain_set);

				// ...and put the z values above into it
				// Note the argument false, meaning that the array won't be copied
				data_ff.setSamples(flat_samples);

				//TODO: not sure if these next lines necessary
				// Get display's graphics mode control and draw scales
				GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();
				dispGMC.setScaleEnable(true);
				
				// fix display to show new type of data
				display.removeReference(data_ref);
				imageMap = new ScalarMap( z, Display.RGB );
				//display.addMap(xMap);
				//display.addMap(yMap);
				display.addMap( imageMap );
				
				//set the new FlatField as our data
				//TODO check that this is the right way to update the display by comparing
				//with the first animation example
				data_ref.setData( data_ff );
				
				// Add reference to display
				display.addReference(data_ref);

			} catch (FileSystemException e) {
				e.printStackTrace();
			}  catch (VisADException e) {
				e.printStackTrace();
			} catch (RemoteException e) {
				e.printStackTrace();
			}
			//replot
			//jframe.repaint();
			// Get the display renderer
			//			DisplayRendererJ2D dRenderer = (DisplayRendererJ2D)display.getDisplayRenderer();
			//			// render again
			//			dRenderer.render_trigger();

			jframe.setVisible(true);
			jframe.toFront();
			// remove authentication credentials from the file path
			//final String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
		}
	}

	private void openTrajectory(VFSJFileChooser fileChooser) {
		// configure the file dialog
		fileChooser.setAccessory(new DefaultAccessoriesPanel(fileChooser));
		fileChooser.setFileHidingEnabled(false);
		fileChooser.setMultiSelectionEnabled(false);
		fileChooser.setFileSelectionMode(SELECTION_MODE.FILES_ONLY);

		// show the file dialog
		RETURN_TYPE answer = fileChooser.showOpenDialog(DansePlotter.jframe);

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
				float[][] xy_vals = new float[2][numDataPoints];
				float[][] z_vals = new float[1][numDataPoints];
				//split the lines by white space
				Pattern whitespacePattern = Pattern.compile("\\s"); 
				for (int i=0; i<numDataPoints; i++){ //(String dataLine : dataLines) {
					String[] data = whitespacePattern.split(dataLines[i]);
					// read the x val and put it on row 1
					xy_vals[1][i] = Float.valueOf(data[0].trim()).floatValue();
					// read the y val and put it on row 0
					xy_vals[0][i] = Float.valueOf(data[1].trim()).floatValue();
					z_vals[0][i] = Float.valueOf(data[2].trim()).floatValue();
				}

				// Create the domain tuple
				domain_tuple = new RealTupleType(x, y);				
				z = RealType.getRealType("z");
				func_domain_range = new FunctionType( domain_tuple, z);
				domain_set = new Gridded2DSet(domain_tuple, xy_vals, xy_vals[0].length);
				// redo the flatfield to contain image data
				// Use FlatField(FunctionType type, Set domain_set)
				data_ff = new FlatField( func_domain_range, domain_set);

				// ...and put the z values above into it
				// Note the argument false, meaning that the array won't be copied
				data_ff.setSamples( z_vals);

				//TODO: not sure if these next lines necessary
				// Get display's graphics mode control and draw scales
				GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();
				dispGMC.setScaleEnable(true);
				
				// fix display to show new type of data
				display.removeReference(data_ref);
				imageMap = new ScalarMap( z, Display.RGB );
				//display.addMap(xMap);
				//display.addMap(yMap);
				display.addMap( imageMap );
				
				//set the new FlatField as our data
				//TODO check that this is the right way to update the display by comparing
				//with the first animation example
				data_ref.setData( data_ff );
				
				// Add reference to display
				display.addReference(data_ref);

			} catch (FileSystemException e) {
				e.printStackTrace();
			}  catch (VisADException e) {
				e.printStackTrace();
			} catch (RemoteException e) {
				e.printStackTrace();
			}
			//replot
			//jframe.repaint();
			// Get the display renderer
			//			DisplayRendererJ2D dRenderer = (DisplayRendererJ2D)display.getDisplayRenderer();
			//			// render again
			//			dRenderer.render_trigger();

			jframe.setVisible(true);
			jframe.toFront();
			// remove authentication credentials from the file path
			//final String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
		}
	}

	private float[] colorToFloats(Color c) {
		float[] rgb = new float[] { 0.5f, 0.5f, 0.5f }; // init with gray
		if (c != null) {
			rgb[0] = c.getRed() / 255.0f;
			rgb[1] = c.getGreen() / 255.0f;
			rgb[2] = c.getBlue() / 255.0f;
		}
		return rgb;
	}

	private void openTwoColumnAscii(final VFSJFileChooser fileChooser) {
		// configure the file dialog
		fileChooser.setAccessory(new DefaultAccessoriesPanel(fileChooser));
		fileChooser.setFileHidingEnabled(false);
		fileChooser.setMultiSelectionEnabled(false);
		fileChooser.setFileSelectionMode(SELECTION_MODE.FILES_ONLY);

		// show the file dialog
		RETURN_TYPE answer = fileChooser.showOpenDialog(DansePlotter.jframe);

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
				data_ff = new FlatField( func_domain_range, x_set);
				// and put the y values above in it
				data_ff.setSamples( y_vals );
				//x_y_ref = new DataReferenceImpl("data_ref");
				// set the display with the new data
				display.removeReference(data_ref);
				data_ref.setData( data_ff );
				// Add reference to display
				display.addReference(data_ref);
				//	private static final String ID = TwoColumnPlotter2.class.getName();
				//
				//	private static DefaultFamily form = new DefaultFamily(ID);

			} catch (FileSystemException e) {
				e.printStackTrace();
			}  catch (VisADException e) {
				e.printStackTrace();
			} catch (RemoteException e) {
				e.printStackTrace();
			}
			//replot
			//jframe.repaint();
			// Get the display renderer
			//			DisplayRendererJ2D dRenderer = (DisplayRendererJ2D)display.getDisplayRenderer();
			//			// render again
			//			dRenderer.render_trigger();

			jframe.setVisible(true);
			jframe.toFront();
			// remove authentication credentials from the file path
			//final String safeName = VFSUtils.getFriendlyName(aFileObject.toString());
		}
	}

	/**
	 * @param fileChooser
	 */
	private void saveTwoColumnAscii(final VFSJFileChooser fileChooser) {
		// configure the file dialog
		fileChooser.setAccessory(new DefaultAccessoriesPanel(fileChooser));
		fileChooser.setFileHidingEnabled(false);
		fileChooser.setMultiSelectionEnabled(false);
		fileChooser.setFileSelectionMode(SELECTION_MODE.FILES_ONLY);
		// show the file dialog
		RETURN_TYPE answer = fileChooser.showOpenDialog(DansePlotter.jframe);
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
	
	public String getLine(InputStream is) {
		/*
		 * To get a line of data we use the BufferedReader.readLine()
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
		new DansePlotter(args);
	}

} // end of Visad Tutorial Program 2_08
