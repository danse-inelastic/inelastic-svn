package vnf;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.regex.Pattern;

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

import visad.DataReferenceImpl;
import visad.Display;
import visad.DisplayImpl;
import visad.FlatField;
import visad.FunctionType;
import visad.GraphicsModeControl;
import visad.Gridded1DSet;
import visad.Gridded2DSet;
import visad.Integer2DSet;
import visad.RealTupleType;
import visad.RealType;
import visad.ScalarMap;
import visad.VisADException;
import visad.java2d.DisplayImplJ2D;

public class PlotterMenu extends JMenuBar {

	public PlotterMenu() {
		//Build the first menu.
		JMenu menu;
		menu = new JMenu("File");
		//menu.setMnemonic(KeyEvent.VK_A);
		//menu.getAccessibleContext().setAccessibleDescription("The only menu in this program that has menu items");
		this.add(menu);

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
		
		final JMenuItem newItemMenuItem_3p6 = new JMenuItem();
		newItemMenuItem_3p6.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				open3DSurface(fileChooser);
			}
		});
		newItemMenuItem_3p6.setText("Open 3DSurface");
		menu.add(newItemMenuItem_3p6);
		
		final JMenuItem newItemMenuItem_3p7 = new JMenuItem();
		newItemMenuItem_3p7.addActionListener(new ActionListener() {
			public void actionPerformed(final ActionEvent arg0) {
				open3DSurface(fileChooser);
			}
		});
		newItemMenuItem_3p7.setText("Open Netcdf file");
		menu.add(newItemMenuItem_3p7);

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
			//String fileContents;
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
				//float[][] zRaw = (float[][])rawData.toArray();
			    float[][] flat_samples = new float[1][numXData*numYData];
			    // ...and then we fill our 'flat' array with the original values
			    // Note that the pixel values indicate the order in which these values
			    // are stored in flat_samples
			    float[] row;
			    for(int r = 0; r < numYData; r++){
			    	row = rawData.get(r);
			    	for(int c = 0; c < numXData; c++)
			    		flat_samples[0][ c * numYData + r ] = row[c];
				}
			    Image image = new Image(flat_samples, numXData, numYData);
				DisplayImpl display = image.getDisplay();
				DansePlotter.jframe.getContentPane().removeAll();
				DansePlotter.jframe.getContentPane().add(display.getComponent());
			} catch (FileSystemException e) {
				e.printStackTrace();
			}  catch (VisADException e) {
				e.printStackTrace();
			} catch (RemoteException e) {
				e.printStackTrace();
			}
			DansePlotter.jframe.setVisible(true);
			DansePlotter.jframe.toFront();
		}
	}
	
	private void open3DSurface(VFSJFileChooser fileChooser) {
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
			//String fileContents;
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
				//float[][] zRaw = (float[][])rawData.toArray();
			    float[][] flat_samples = new float[1][numXData*numYData];
			    // ...and then we fill our 'flat' array with the original values
			    // Note that the pixel values indicate the order in which these values
			    // are stored in flat_samples
			    float[] row;
			    for(int r = 0; r < numYData; r++){
			    	row = rawData.get(r);
			    	for(int c = 0; c < numXData; c++)
			    		flat_samples[0][ c * numYData + r ] = row[c];
				}
			    ThreeDSurface threeDSurface = new ThreeDSurface(flat_samples, numXData, numYData);
				DisplayImpl display = threeDSurface.getDisplay();
				DansePlotter.jframe.getContentPane().removeAll();
				DansePlotter.jframe.getContentPane().add(display.getComponent());
			} catch (FileSystemException e) {
				e.printStackTrace();
			}  catch (VisADException e) {
				e.printStackTrace();
			} catch (RemoteException e) {
				e.printStackTrace();
			}
			DansePlotter.jframe.setVisible(true);
			DansePlotter.jframe.toFront();
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
				//float[][] z_vals = new float[1][numDataPoints];
				//split the lines by white space
				Pattern whitespacePattern = Pattern.compile("\\s"); 
				for (int i=0; i<numDataPoints; i++){ //(String dataLine : dataLines) {
					String[] data = whitespacePattern.split(dataLines[i]);
					// read the x val and put it on row 1
					xy_vals[1][i] = Float.valueOf(data[0].trim()).floatValue();
					// read the y val and put it on row 0
					xy_vals[0][i] = Float.valueOf(data[1].trim()).floatValue();
					//z_vals[0][i] = Float.valueOf(data[2].trim()).floatValue();
				}
				Trajectory trajectory = new Trajectory(xy_vals);
				DisplayImpl display = trajectory.getDisplay();

				DansePlotter.jframe.getContentPane().removeAll();
				DansePlotter.jframe.getContentPane().add(display.getComponent());
				
			} catch (FileSystemException e) {
				e.printStackTrace();
			}  catch (VisADException e) {
				e.printStackTrace();
			} catch (RemoteException e) {
				e.printStackTrace();
			}

			DansePlotter.jframe.setVisible(true);
			DansePlotter.jframe.toFront();
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
				Line line = new Line(x_vals, y_vals);
				DisplayImpl display = line.getDisplay();
				DansePlotter.jframe.getContentPane().removeAll();
				DansePlotter.jframe.getContentPane().add(display.getComponent());
			} catch (FileSystemException e) {
				e.printStackTrace();
			}  catch (VisADException e) {
				e.printStackTrace();
			} catch (RemoteException e) {
				e.printStackTrace();
			}
			
			DansePlotter.jframe.toFront();
			DansePlotter.jframe.setVisible(true);
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


}
