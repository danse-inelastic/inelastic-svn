// AnchoredPoint.java

/*
This application demonstrates a fixed-length line with one manipulable
endpoint (the other endpoint is fixed at the display's center).
*/

import visad.*;
import visad.java3d.*;
import visad.util.Util;

import java.awt.event.*;
import java.rmi.RemoteException;

import javax.swing.*;

public class AnchoredPoint {

  private static final float LENGTH = 5;
  private static final float END_X = 2;
  private static final float END_Y = 3;

  public static void main(String[] args) throws Exception {
    // math types
    RealType x = RealType.getRealType("x");
    RealType y = RealType.getRealType("y");
    final RealTupleType xy = new RealTupleType(x, y);

    // mappings
    ScalarMap xmap = new ScalarMap(x, Display.XAxis);
    ScalarMap ymap = new ScalarMap(y, Display.YAxis);
    xmap.setRange(END_X - LENGTH, END_X + LENGTH);
    ymap.setRange(END_Y - LENGTH, END_Y + LENGTH);

    // display
    DisplayImpl display = new DisplayImplJ3D("display",
      new TwoDDisplayRendererJ3D());
    display.disableAction();
    display.addMap(xmap);
    display.addMap(ymap);
    GraphicsModeControl gmc = display.getGraphicsModeControl();
    gmc.setScaleEnable(true);
    gmc.setPointSize(5.0f);

    // data references
    final DataReferenceImpl line_ref = new DataReferenceImpl("line");
    final DataReferenceImpl pt_ref = new DataReferenceImpl("point");
    display.addReference(line_ref);
    display.addReferences(new DirectManipulationRendererJ3D(), pt_ref, null);

    // data objects
    doPoint(xy, 0, 0, pt_ref);
    doLine(xy, 0, 0, line_ref);

    // computational cell
    CellImpl cell = new CellImpl() {
      public void doAction() {
        // get point coordinates
        RealTuple tuple = (RealTuple) pt_ref.getData();
        if (tuple == null) return;
        double[] vals = tuple.getValues();
        float xval = (float) vals[0];
        float yval = (float) vals[1];

        // adjust point coordinates
        float xlen = END_X - xval;
        float ylen = END_Y - yval;
        float len = (float) Math.sqrt(xlen * xlen + ylen * ylen);
        if (!Util.isApproximatelyEqual(len, LENGTH)) {
          double lamda = LENGTH / len;
          xval = (float) (END_X + lamda * (xval - END_X));
          yval = (float) (END_Y + lamda * (yval - END_Y));
          try { doPoint(xy, xval, yval, pt_ref); }
          catch (Exception exc) { exc.printStackTrace(); }
          return; // point change will retrigger cell
        }

        // update line
        try { doLine(xy, xval, yval, line_ref); }
        catch (Exception exc) { exc.printStackTrace(); }
      }
    };
    cell.addReference(pt_ref);
    display.enableAction();

    // show display onscreen
    JFrame frame = new JFrame("Fixed-length line with one anchored point");
    frame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) { System.exit(0); }
    });
    JPanel p = new JPanel();
    p.setLayout(new BoxLayout(p, BoxLayout.X_AXIS));
    p.add(display.getComponent());
    frame.setContentPane(p);
    frame.setSize(400, 400);
    Util.centerWindow(frame);
    frame.show();
  }

  private static void doLine(RealTupleType rtt, float x, float y,
    DataReferenceImpl line_ref) throws VisADException, RemoteException
  {
    float[][] samples = { {x, END_X}, {y, END_Y} };
    Gridded2DSet set = new Gridded2DSet(rtt, samples, 2);
    line_ref.setData(set);
  }

  private static void doPoint(RealTupleType rtt, float x, float y,
    DataReferenceImpl pt_ref) throws VisADException, RemoteException
  {
    pt_ref.setData(new RealTuple(rtt, new double[] {x, y}));
  }

}
