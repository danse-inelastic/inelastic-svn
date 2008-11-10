// MiniDataServer.java

import java.awt.event.*;
import java.net.*;
import java.rmi.*;
import javax.swing.*;
import visad.*;
import visad.data.*;
import visad.java2d.DisplayImplJ2D;

/*
This example creates a RemoteServer and loads a data object into it.
Start it up by typing:
    java MiniDataServer ServerName DataName dataFile

where ServerName is the desired name for the RMI server, DataName is
the desired name for the data reference, and dataFile is the name of
the data file to load up and serve.  Be sure you start up rmiregistry
before running MiniDataServer.

Then, load up the SpreadSheet and try:
    rmi://ip.address/ServerName/DataName
(where ip.address is your machine's IP address) and you should see
the data in the SpreadSheet cell.
*/

public class MiniDataServer {

  public static void main(String[] args) throws Exception {
    if (args.length < 3) {
      System.err.println("Please specify three command line arguments:");
      System.err.println("  - Server name (e.g., MyServer)");
      System.err.println("  - Cell name (e.g., A1)");
      System.err.println("  - Data file (e.g., mydata.nc)");
      System.exit(-1);
    }
    String server = args[0];
    String cell = args[1];
    String file = args[2];

    // load data
    System.out.println("Loading " + file + "...");
    DefaultFamily loader = new DefaultFamily("loader");
    Data data = loader.open(file);

    // set up display
    System.out.println("Setting up display...");
    ScalarMap[] maps = data.getType().guessMaps(false);
    DisplayImplJ2D display = new DisplayImplJ2D("MiniDataServer");
    for (int i=0; i<maps.length; i++) display.addMap(maps[i]);
    DataReferenceImpl ref = new DataReferenceImpl(cell);
    ref.setData(data);
    display.addReference(ref);

    // start up remote server
    System.out.println("Starting remote server...");
    RemoteServerImpl rsi = null;
    try {
      rsi = new RemoteServerImpl();
      Naming.rebind("///" + server, rsi);
    }
    catch (java.rmi.ConnectException exc) {
      System.err.println("Please run rmiregistry first.");
      System.exit(-2);
    }
    catch (MalformedURLException exc) {
      System.err.println("Error binding server; try a different name.");
      System.exit(-3);
    }
    catch (RemoteException exc) {
      System.err.println("Error binding server:");
      exc.printStackTrace();
      System.exit(-4);
    }
    rsi.addDataReference(ref);

    // set up GUI
    System.out.println("Bringing up display...");
    JFrame frame = new JFrame("Mini data server");
    JPanel pane = new JPanel();
    pane.setLayout(new BoxLayout(pane, BoxLayout.X_AXIS));
    frame.setContentPane(pane);
    pane.add(display.getComponent());
    frame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) { System.exit(0); }
    });
    frame.pack();
    frame.show();
  }

}

