// RiversColor.java

/*
This application demonstrates using UnionSets and FieldImpls
to create a collection of colored line segments.
*/

import visad.*;
import visad.java2d.*;

import java.awt.BorderLayout;
import java.awt.event.*;
import java.rmi.RemoteException;

import javax.swing.*;

/** RiversColor is based on visad/examples/Rivers.java. */
public class RiversColor {

  public static void main(String args[])
    throws VisADException, RemoteException
  {
    RealTupleType earth =
      new RealTupleType(RealType.Latitude, RealType.Longitude);

    // construct straight south flowing river1
    float[][] points1 = {{3.0f, 2.0f, 1.0f, 0.0f},
                         {0.0f, 0.0f, 0.0f, 0.0f}};
    Gridded2DSet river1 = new Gridded2DSet(earth, points1, 4);

    // construct east feeder river2
    float[][] points2 = {{3.0f, 2.0f, 1.0f},
                         {2.0f, 1.0f, 0.0f}};
    Gridded2DSet river2 = new Gridded2DSet(earth, points2, 3);

    // construct west feeder river3
    float[][] points3 = {{4.0f, 3.0f, 2.0f},
                         {-2.0f, -1.0f, 0.0f}};
    Gridded2DSet river3 = new Gridded2DSet(earth, points3, 3);

    // construct river system set
    Gridded2DSet[] riverSystem = {river1, river2, river3};
    UnionSet riversSet = new UnionSet(earth, riverSystem);

    // construct river field for coloring rivers
    RealType red = RealType.getRealType("red");
    RealType green = RealType.getRealType("green");
    RealType blue = RealType.getRealType("blue");
    RealTupleType rgb = new RealTupleType(red, green, blue);
    FunctionType ftype = new FunctionType(earth, rgb);
    FlatField riversField = new FlatField(ftype, riversSet);
    float[][] samples = new float[][] { // 4+3+3=10 sample points total
      {1, 1, 1, 1, 1, 1, 1, 0, 0, 0}, // red
      {1, 1, 1, 1, 0, 0, 0, 1, 1, 1}, // green
      {0, 0, 0, 0, 1, 1, 1, 1, 1, 1}  // blue
    };
    riversField.setSamples(samples, false);

    // create a DataReference for river system
    final DataReference riversRef = new DataReferenceImpl("rivers");
    riversRef.setData(riversField);

    // create a Display using Java2D
    DisplayImpl display = new DisplayImplJ2D("image display");

    // map earth coordinates to display coordinates
    display.addMap(new ScalarMap(RealType.Longitude, Display.XAxis));
    display.addMap(new ScalarMap(RealType.Latitude, Display.YAxis));

    // map color components to color space
    ScalarMap redMap = new ScalarMap(red, Display.Red);
    ScalarMap greenMap = new ScalarMap(green, Display.Green);
    ScalarMap blueMap = new ScalarMap(blue, Display.Blue);
    redMap.setRange(0, 1);
    greenMap.setRange(0, 1);
    blueMap.setRange(0, 1);
    display.addMap(redMap);
    display.addMap(greenMap);
    display.addMap(blueMap);

    // link the Display to riversRef
    display.addReference(riversRef);
    riversRef.setData(riversField);

    // create JFrame (i.e., a window) for display and slider
    JFrame frame = new JFrame("RiversColor VisAD Application");
    frame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) { System.exit(0); }
    });

    // create JPanel in JFrame
    JPanel panel = new JPanel();
    panel.setLayout(new BorderLayout());
    frame.setContentPane(panel);

    // add display to JPanel
    panel.add(display.getComponent());

    // set size of JFrame and make it visible
    frame.setSize(500, 500);
    frame.setVisible(true);
  }

}
