// IrregularRenderTest.java

import java.rmi.RemoteException;

import javax.swing.*;

import visad.*;
import visad.java3d.DisplayImplJ3D;

public class IrregularRenderTest {

  public static void main(String[] args)
    throws VisADException, RemoteException
  {
    // create types
    RealType x = RealType.getRealType("x");
    RealType y = RealType.getRealType("y");
    RealType z = RealType.getRealType("z");
    RealTupleType xyz = new RealTupleType(x, y, z);
    RealType value = RealType.getRealType("value");

    // generate some irregular (random) samples
    int count = 512;
    float[][] samples = new float[3][count];
    for (int i=0; i<count; i++) for (int j=0; j<3; j++) {
      samples[j][i] = (float) (1000 * Math.random());
    }
    Irregular3DSet iset = new Irregular3DSet(xyz,
      samples, null, null, null, null, false);

    // build field
    FunctionType ftype = new FunctionType(xyz, value);
    FlatField field = new FlatField(ftype, iset);
    float[][] values = new float[1][count];
    for (int i=0; i<count; i++) {
      values[0][i] = 1500 - (Math.abs(samples[0][i] - 500) +
        Math.abs(samples[1][i] - 500) + Math.abs(samples[2][i] - 500));
    }
    field.setSamples(values, false);

    // resample field to regular grid
    int size = 32;
    count = size * size * size;
    Linear3DSet set = new Linear3DSet(xyz,
      0, 1000, size, 0, 1000, size, 0, 1000, size);
    field = (FlatField)
      field.resample(set, Data.WEIGHTED_AVERAGE, Data.NO_ERRORS);

    // create display
    DisplayImpl display = new DisplayImplJ3D("display");
    display.getGraphicsModeControl().setPointSize(5.0f);
    display.addMap(new ScalarMap(x, Display.XAxis));
    display.addMap(new ScalarMap(y, Display.YAxis));
    display.addMap(new ScalarMap(z, Display.ZAxis));
    ScalarMap color = new ScalarMap(value, Display.RGBA);
    display.addMap(color);

    // assign alpha channel
    BaseColorControl cc = (BaseColorControl) color.getControl();
    cc.setTable(tweakAlpha(cc.getTable()));

    // add data to display
    DataReferenceImpl ref = new DataReferenceImpl("ref");
    ref.setData(field);
    display.addReference(ref);

    // show display onscreen
    JFrame frame = new JFrame("Irregular rendering test");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.getContentPane().add(display.getComponent());
    frame.setBounds(200, 200, 400, 400);
    frame.show();
  }

  private static float[][] tweakAlpha(float[][] table) {
    int pow = 2;
    int len = table[3].length;
    for (int i=0; i<len; i++) {
      table[3][i] = (float) Math.pow((double) i / len, pow);
    }
    return table;
  }

}
