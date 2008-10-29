//
// CursorSSCell.java
//

/*
Below is a simple extension of visad.ss.FancySSCell that prints range values
to the console window whenever the cursor is being displayed.  It shouldn't
be hard to modify this code to display the range values in a JLabel or other
such GUI component.

You should be able to follow this pattern to extend FancySSCell in any way
you desire, producing any number of different custom spreadsheet cell
behaviors.
*/

import java.awt.Frame;
import java.rmi.RemoteException;
import java.util.Vector;
import visad.*;
import visad.formula.FormulaManager;
import visad.ss.*;

public class CursorSSCell extends FancySSCell {

  public CursorSSCell(String name, FormulaManager fman, RemoteServer rs,
    boolean slave, String save, Frame parent)
    throws VisADException, RemoteException
  {
    super(name, fman, rs, slave, save, parent);

    addDisplayListener(new DisplayListener() {
      public void displayChanged(DisplayEvent e) {
        // get cursor value
        double[] scale_offset = new double[2];
        double[] dum_1 = new double[2];
        double[] dum_2 = new double[2];
        DisplayRenderer renderer = VDisplay.getDisplayRenderer();
        double[] cur = renderer.getCursor();
        Vector cursorStringVector = renderer.getCursorStringVector();
        if (cursorStringVector == null || cursorStringVector.size() == 0 ||
          cur == null || cur.length == 0 || cur[0] != cur[0])
        {
          return;
        }

        // locate x and y mappings
        ScalarMap[] maps = getMaps();
        ScalarMap map_x = null, map_y = null;
        for (int i=0; i<maps.length && (map_x==null || map_y==null); i++) {
          if (maps[i].getDisplayScalar().equals(Display.XAxis)) {
            map_x = maps[i];
          }
          else if (maps[i].getDisplayScalar().equals(Display.YAxis)) {
            map_y = maps[i];
          }
        }
        if (map_x == null || map_y == null) return;

        // get scale
        map_x.getScale(scale_offset, dum_1, dum_2);
        double value_x = (cur[0] - scale_offset[1]) / scale_offset[0];
        map_y.getScale(scale_offset, dum_1, dum_2);
        double value_y = (cur[1] - scale_offset[1]) / scale_offset[0];
        RealTuple tuple = null;
        try {
          tuple = new RealTuple(new Real[] {
            new Real((RealType) map_x.getScalar(), value_x),
            new Real((RealType) map_y.getScalar(), value_y)});
        }
        catch (VisADException exc) { exc.printStackTrace(); }
        catch (RemoteException exc) { exc.printStackTrace(); }

        // check each data object in the cell
        Data[] data = getData();
        for (int i=0; i<data.length; i++) {
          if (data[i] instanceof FlatField) {
            // get range values
            FlatField ff = (FlatField) data[i];
            double[] range_values = null;
            try {
              Data d = ff.evaluate(tuple);
              if (d instanceof Real) {
                Real r = (Real) d;
                range_values = new double[1];
                range_values[0] = r.getValue();
              }
              else if (d instanceof RealTuple) {
                RealTuple rt = (RealTuple) d;
                int dim = rt.getDimension();
                range_values = new double[dim];
                for (int j=0; j<dim; j++) {
                  Real r = (Real) rt.getComponent(j);
                  range_values[j] = r.getValue();
                }
              }
            }
            catch (VisADException exc) { exc.printStackTrace(); }
            catch (RemoteException exc) { exc.printStackTrace(); }

            // display range values somehow; e.g.:
            System.out.print("data #" + i + ": " +
              "(" + value_x + ", " + value_y + "): ");
            if (range_values == null) System.out.println("null");
            else {
              if (range_values.length == 1) {
                System.out.println(range_values[0]);
              }
              else {
                System.out.print("(" + range_values[0]);
                for (int j=1; j<range_values.length; j++) {
                  System.out.print(", " + range_values[j]);
                }
                System.out.println(")");
              }
            }
          }
        }
      }
    });
  }

  public static void main(String[] args) {
    SpreadSheet.setSSCellClass(CursorSSCell.class);
    SpreadSheet.main(args);
  }

}
