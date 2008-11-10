// SurfaceAnimation.java

import java.awt.event.*;
import java.rmi.RemoteException;
import javax.swing.JFrame;

import visad.*;
import visad.java3d.*;

/** Constructs a surface whose colors animate over time. */
public class SurfaceAnimation {

  public static void main(String[] args)
    throws VisADException, RemoteException
  {
    int numTimePoints = 10;
    int xLen = 32, yLen = 32;
    int len = xLen * yLen;

    // construct data types
    RealType tType = RealType.getRealType("time");
    RealType xType = RealType.getRealType("x");
    RealType yType = RealType.getRealType("y");
    RealType zType = RealType.getRealType("z");
    RealType vType = RealType.getRealType("value");
    RealTupleType xy = new RealTupleType(xType, yType);
    RealTupleType zv = new RealTupleType(zType, vType);
    FunctionType surfaceType = new FunctionType(xy, zv);
    FunctionType animType = new FunctionType(tType, surfaceType);
    Integer2DSet surfaceSet = new Integer2DSet(xy, xLen, yLen);
    Integer1DSet animSet = new Integer1DSet(tType, numTimePoints);

    // generate surface values
    float[] surface = new float[len];
    for (int y=0; y<yLen; y++) {
      for (int x=0; x<xLen; x++) {
        // a nice, rounded surface
        float xn = (float) xLen / 2 - x;
        float yn = (float) yLen / 2 - y;
        surface[y * xLen + x] = xn * xn + yn * yn;
      }
    }

    // generate color values
    FieldImpl data = new FieldImpl(animType, animSet);
    for (int t=0; t<numTimePoints; t++) {
      FlatField field = new FlatField(surfaceType, surfaceSet);
      float[] values = new float[len];
      // a linear progression of color values
      for (int i=0; i<len; i++) values[i] = len * t + i;
      float[][] samples = {surface, values};
      field.setSamples(samples, false);
      data.setSample(t, field);
    }

    // create display
    DisplayImpl display = new DisplayImplJ3D("display");
    DataReferenceImpl ref = new DataReferenceImpl("ref");
    ref.setData(data);
    display.addMap(new ScalarMap(tType, Display.Animation));
    display.addMap(new ScalarMap(xType, Display.XAxis));
    display.addMap(new ScalarMap(yType, Display.YAxis));
    display.addMap(new ScalarMap(zType, Display.ZAxis));
    display.addMap(new ScalarMap(vType, Display.RGB));
    display.addReference(ref);

    // start animation
    AnimationControl animControl = (AnimationControl)
      display.getControl(AnimationControl.class);
    animControl.setOn(true);

    // show display onscreen
    JFrame frame = new JFrame("Surface animation");
    frame.getContentPane().add(display.getComponent());
    frame.addWindowListener(new WindowAdapter() {
      public void windowClosing(WindowEvent e) { System.exit(0); }
    });
    frame.pack();
    frame.show();
  }

}
