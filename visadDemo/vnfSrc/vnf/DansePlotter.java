/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
 */

package vnf;

// Import needed classes


import java.awt.Image;
import java.awt.Rectangle;
import java.awt.Toolkit;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;
import java.rmi.RemoteException;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

import thredds.ui.Resource;
import ucar.nc2.NetcdfFileCache;
import ucar.nc2.dataset.NetcdfDatasetCache;
import ucar.util.prefs.PreferencesExt;
import ucar.util.prefs.XMLStore;
import ucar.util.prefs.ui.Debug;
import visad.DisplayImpl;
import visad.VisADException;


/**
 * Danse Plotter
 */

//TODO: create an openFile method that takes the type of file as argument.  Instantiate file chooser inside of it and get rid of passing reference.

public class DansePlotter {
	static private final String FRAME_SIZE = "FrameSize";

	//private ucar.util.prefs.PreferencesExt mainPrefs;


	public DansePlotter(ucar.util.prefs.PreferencesExt prefs, JFrame parentFrame) 
	throws RemoteException,VisADException {
		
		float[][] x_vals = new float[][]{{0}};
		float[][] y_vals = new float[][]{{0.0f}};
		Line line = new Line(x_vals, y_vals);
		DisplayImpl display = line.getDisplay();
		
		final PlotterMenu menuBar = new PlotterMenu(parentFrame);
		parentFrame.setJMenuBar(menuBar);
		parentFrame.getContentPane().removeAll();
		parentFrame.getContentPane().add(display.getComponent());
		
	}
	
	  // Splash Window
	  private static class SplashScreen extends javax.swing.JWindow {
	    public SplashScreen() {
	      Image image = Resource.getImage("/resources/danseLogo.JPG");
	      ImageIcon icon = new ImageIcon(image);
	      JLabel lab = new JLabel(icon);
	      getContentPane().add(lab);
	      pack();

	      //show();
	      java.awt.Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
	      int width = image.getWidth(null);
	      int height = image.getHeight(null);
	      setLocation(screenSize.width / 2 - (width / 2), screenSize.height / 2 - (height / 2));
	      addMouseListener(new MouseAdapter() {
	        public void mousePressed(MouseEvent e) {
	          setVisible(false);
	        }
	      });
	      setVisible(true);
	    }
	  }
	  
	  static private void exit() {
		    //dansePlotter.save();
		    Rectangle bounds = frame.getBounds();
		    prefs.putBeanObject(FRAME_SIZE, bounds);
		    try {
		      store.save();
		    } catch (IOException ioe) {
		      ioe.printStackTrace();
		    }

		    done = true; // on some systems, still get a window close event
		    NetcdfFileCache.exit(); // kill the timer thread
		    NetcdfDatasetCache.exit(); // kill the timer thread
		    System.exit(0);
		  }
	  
	  // handle messages
	  private static DansePlotter dansePlotter;
	  private static JFrame frame;
	  private static PreferencesExt prefs;
	  private static XMLStore store;
	  private static boolean done = false;

	  private static String wantDataset = null;

	  private static void setDataset() {
//	    SwingUtilities.invokeLater(new Runnable() { // do it in the swing event thread

//	      public void run() {
//	        dansePlotter.makeComponent("THREDDS");
//	        dansePlotter.threddsUI.setDataset(wantDataset);
//	        dansePlotter.tabbedPane.setSelectedComponent(dansePlotter.threddsUI);
//	      }
//	    });
	  }
	  
	  


	public static void main(String[] args) throws RemoteException,
	VisADException {
		final SplashScreen splash = new SplashScreen();
		
	    // prefs storage
	    try {
	      String prefStore = ucar.util.prefs.XMLStore.makeStandardFilename(".unidata", "NetcdfUI22.xml");
	      store = ucar.util.prefs.XMLStore.createFromFile(prefStore, null);
	      prefs = store.getPreferences();
	      Debug.setStore(prefs.node("Debug"));
	    } catch (IOException e) {
	      System.out.println("XMLStore Creation failed " + e);
	    }

	    // initializations
	    //BAMutil.setResourcePath("/resources/nj22/ui/icons/");
	    // initCaches();

	    // for efficiency, persist aggregations. every hour, delete stuff older than 30 days
	    //Aggregation.setPersistenceCache(new DiskCache2("/.unidata/cachePersist", true, 60 * 24 * 30, 60));
	    //DqcFactory.setPersistenceCache(new DiskCache2("/.unidata/dqc", true, 60 * 24 * 365, 60));

	    // test
	    // java.util.logging.Logger.getLogger("ucar.nc2").setLevel( java.util.logging.Level.SEVERE);

	    // put UI in a JFrame
	    frame = new JFrame("Danse Plotter 0.1");
	    dansePlotter = new DansePlotter(prefs, frame);

	    //frame.setIconImage(BAMutil.getImage("netcdfUI"));

	    frame.addWindowListener(new WindowAdapter() {
	      public void windowActivated(WindowEvent e) {
	        splash.setVisible(false);
	        splash.dispose();
	      }

	      public void windowClosing(WindowEvent e) {
	        if (!done) exit();
	      }
	    });

	    Rectangle bounds = (Rectangle) prefs.getBean(FRAME_SIZE, new Rectangle(50, 50, 800, 450));
	    frame.setBounds(bounds);

	    frame.pack();
	    frame.setBounds(bounds);
	    frame.setVisible(true);

//	    // set Authentication for accessing passsword protected services like TDS PUT
//	    java.net.Authenticator.setDefault(new thredds.ui.UrlAuthenticatorDialog(frame));
//
//	    // use HTTPClient
//	    CredentialsProvider provider = new thredds.ui.UrlAuthenticatorDialog(frame);
//	    ucar.nc2.dataset.HttpClientManager.init(provider, "ToolsUI");
//	    ucar.nc2.dods.DODSNetcdfFile.setAllowSessions(false);
//
//	    // load protocol for ADDE URLs
//	    URLStreamHandlerFactory.install();
//	    URLStreamHandlerFactory.register("adde", new edu.wisc.ssec.mcidas.adde.AddeURLStreamHandler());
//
//	    // in case a dataset was on the command line
//	    if (wantDataset != null)
//	      setDataset();
//	  }

	}

} 
