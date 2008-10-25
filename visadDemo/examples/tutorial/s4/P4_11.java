/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s4;

// Import needed classes

import visad.*;
import visad.util.*;
import visad.java3d.DisplayImplJ3D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

  /**
  VisAD Tutorial example 4_11
  Use a Linear3DSet
  Use RGBA Map and LabeledColorWidget with RGBA map
  We have the function rgbVal = h(RED, GREEN, BLUE)

  represented by the MathType
  ( (RED, GREEN, BLUE) -> rgbVal )
  Run program with "java P4_11"
 */



public class P4_11{

// Declare variables
  // The domain quantities longitude and latitude
  // and the dependent quantity rgbVal

  private RealType red, green, blue;
  private RealType rgbVal;

  // Tuple to pack longitude and latitude together

  private RealTupleType domain_tuple;


  // The function (domain_tuple -> rgbVal )

  private FunctionType func_domain_rgbVal;


   // Our Data values for the domain are represented by the Set

  private Set domain_set;


  // The Data class FlatField

  private FlatField vals_ff;

  // The DataReference from data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap redXMap, greenYMap, blueZMap;
  private ScalarMap redMap, greenMap, blueMap;
  private ScalarMap rgbaMap;
  private ScalarMap greenRangeMap;

  // Our color-alpha table

  private float[][] myColorTable;

 // The LabeledColorWidget
  private LabeledColorWidget labelCW;

 // The Range widget
  private SelectRangeWidget selRangeWid;

  public P4_11(String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name, Unit unit, Set set);

    red = RealType.getRealType("RED", null, null);
    green = RealType.getRealType("GREEN", null, null);
    blue = RealType.getRealType("BLUE", null, null);

    domain_tuple = new RealTupleType(red, green, blue);

    // The independent variable

    rgbVal = RealType.getRealType("RGB_VALUE", null, null);

    // Create a FunctionType (domain_tuple -> range_tuple )
    // Use FunctionType(MathType domain, MathType range)

    func_domain_rgbVal = new FunctionType( domain_tuple, rgbVal);

    // Create the domain Set
    // Integer3DSet(MathType type, int lengthX, int lengthY, int lengthZ)

    int NCOLS = 32;
    int NROWS = 32;
    int NLEVS = 16;

    domain_set = new Linear3DSet(domain_tuple,  -Math.PI, Math.PI, NROWS,
                                                -Math.PI, Math.PI, NCOLS,
                                                -Math.PI, 0.0,     NLEVS );

    // Our 'flat' array

    double[][] flat_samples = new double[1][NCOLS * NROWS * NLEVS];

    // Fill our 'flat' array with the rgbVal values
    // by looping over NCOLS and NROWS

    // but first get the Set samples to help with the calculations
    float[][] set_samples = domain_set.getSamples( true );

    // Note the use of an index variable, indicating the order of the samples


    int index = 0;

    for(int l = 0; l < NLEVS; l++)

      for(int c = 0; c < NCOLS; c++)

        for(int r = 0; r < NROWS; r++){

	      // set value for RealType rgbVal
	      flat_samples[0][ index ] =   (float) (Math.sin( 0.850 * (double)
	                                                  set_samples[0][ index ]) ) +

                                      (float) Math.exp( - 1.0/(Math.pow((double)
	                                     set_samples[1][ index ]*0.5/Math.PI, 2.0 ) -1.0 )) +

                                       (float) (Math.cos( 0.650 * (double)
	                                                  set_samples[2][ index ]) ) ;


	      // increment index
	      index++;

      }

    // Create a FlatField
    // Use FlatField(FunctionType type, Set domain_set)

    vals_ff = new FlatField( func_domain_rgbVal, domain_set);

    // ...and put the rgbVal values above into it

    // Note the argument false, meaning that the array won't be copied

    vals_ff.setSamples( flat_samples , false );

    // Create Display and its maps

    // This is new: a 3D display

    display = new DisplayImplJ3D("display1");

    // Get display's graphics mode control and draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl)  display.getGraphicsModeControl();
    dispGMC.setScaleEnable(true);
    dispGMC.setProjectionPolicy(DisplayImplJ3D.PARALLEL_PROJECTION);

    // Create the ScalarMaps: latitude to XAxis, longitude to YAxis and
    // rgbVal to ZAxis and to RGB
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    redXMap = new ScalarMap( red,    Display.XAxis );
    greenYMap = new ScalarMap( green, Display.YAxis );
    blueZMap = new ScalarMap( blue, Display.ZAxis );

    rgbaMap= new ScalarMap( rgbVal,  Display.RGBA );
    greenRangeMap = new ScalarMap( green, Display.SelectRange );


    // Add maps to display

    display.addMap( redXMap );
    display.addMap( greenYMap );
    display.addMap( blueZMap );

    display.addMap( greenRangeMap );
    display.addMap( rgbaMap);

    // Create a color-alpha table
    // Note: table has red, green, blue and alpha components
    // and is 9 units long, i.e float[4][9]


    int tableLength = 15;

    myColorTable = new float[4][tableLength];

    for(int i=0;i<tableLength;i++){

      myColorTable[0][i]= (float) i / ((float)tableLength-1.0f); // red component
      myColorTable[2][i]= (float) 1.0f - (float)i / ((float)tableLength-1.0f); // blue component

      if(i<(tableLength)/2){ // lower half of table

        myColorTable[1][i]= 2.0f *(float) i / (tableLength-1); // green component
        myColorTable[3][i]= 0.8f * myColorTable[0][i];

      }
      else{ // upper half of table

        myColorTable[1][i]=  2.0f - 2.0f *(float)i / ((float)tableLength-1); // green component
        myColorTable[3][i]= 0.8f * myColorTable[2][i];// alpha component

      }
    }

      // make lower edge "sharp"; alpha values only
      myColorTable[3][0]= (float) 1.0f; // alpha component
      myColorTable[3][1]= (float) 1.0f; // alpha component

      // make upper edge semi-transparent; alpha values only
      myColorTable[3][13]= (float) 0.5f; // alpha component
      myColorTable[3][14]= (float) 0.5f; // alpha component


    // Create a LabeledColorWidget with an
    // RGBA ScalarMap and an initial RGBA table

    labelCW = new LabeledColorWidget( rgbaMap, myColorTable );

    // ...and a SelectRangeWidget
    selRangeWid = new SelectRangeWidget( greenRangeMap );

    // Create a data reference and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");

    data_ref.setData( vals_ff );

    // Add reference to display

    display.addReference( data_ref );

    blueZMap.setRange(-Math.PI, Math.PI );



    // Create application window and add display to window

    JFrame jframe = new JFrame("VisAD Tutorial example 4_11");
    jframe.getContentPane().setLayout(new FlowLayout());
    jframe.getContentPane().add(display.getComponent());

    // Add widgets to the frame

    jframe.getContentPane().add(labelCW);
    jframe.getContentPane().add(selRangeWid);


    // Set window size and make it visible

    jframe.setSize(550, 340);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P4_11(args);
  }

} //end of Visad Tutorial Program 4_10
