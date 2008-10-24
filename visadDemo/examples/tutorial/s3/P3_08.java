/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s3;

// Import needed classes

import visad.*;
import visad.util.*;
import visad.java2d.DisplayImplJ2D;
import java.rmi.RemoteException;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

  /**
  VisAD Tutorial example 3_08
  Slight variation of example 3_07
  Add an RGB map to isolines
  Introduce the GraphicsModeControlWidget
  We have the function temperature = f(latitude, longitude)
  represented by the MathType
  ( (latitude, longitude) -> elevation )
  Run program with "java P3_08"
 */



public class P3_08{

// Declare variables
  // The domain quantities longitude and latitude
  // and the dependent quantity temperature

  private RealType longitude, latitude;
  private RealType temperature;


  // Tuple to pack longitude and latitude together, as the domain

  private RealTupleType domain_tuple;


  // The function (domain_tuple -> temperature )
  // Remeber, range is only "temperature"

  private FunctionType func_domain_temp;


   // Our Data values for the domain are represented by the Set

  private Set domain_set;


  // The Data class FlatField

  private FlatField vals_ff;

  // The DataReference from data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;
  private ScalarMap latMap, lonMap;
  private ScalarMap tempIsoMap, tempRGBMap, isoTempRGBMap;

  // These objects are for drawing isocontours

  private RealType isoTemperature;
  private FunctionType func_domain_isoTemp;

  private FlatField iso_vals_ff;
  private DataReferenceImpl iso_data_ref;

  // A GraphicsModeControlWidget

  private GMCWidget gmcWidget;


  public P3_08(String []args)
    throws RemoteException, VisADException {

    // Create the quantities
    // Use RealType(String name);

    latitude = RealType.getRealType("latitude");
    longitude = RealType.getRealType("longitude");

    domain_tuple = new RealTupleType(latitude, longitude);

    temperature = RealType.getRealType("temperature", SI.kelvin, null);

    isoTemperature = RealType.getRealType("isoTemperature", SI.kelvin, null);

    // Create a FunctionType (domain_tuple -> temperature )
    // Use FunctionType(MathType domain, MathType range)

    func_domain_temp = new FunctionType( domain_tuple, temperature);

    // ... the same for isoTemperature

    func_domain_isoTemp = new FunctionType( domain_tuple, isoTemperature);

    // Create the domain Set
    // Use LinearDSet(MathType type, double first1, double last1, int lengthX,
    //				     double first2, double last2, int lengthY)

    int NCOLS = 50;
    int NROWS = NCOLS;

    domain_set = new Linear2DSet(domain_tuple, -Math.PI, Math.PI, NROWS,
    					       -Math.PI, Math.PI, NCOLS);



    // Get the Set samples to facilitate the calculations

    float[][] set_samples = domain_set.getSamples( true );


    // The actual temperature values are stored in this array
    // float[1][ number_of_samples ]

    float[][] flat_samples = new float[1][NCOLS * NROWS];

    // We fill our 'flat' array with the generated values
    // by looping over NCOLS and NROWS

    for(int c = 0; c < NCOLS; c++)

      for(int r = 0; r < NROWS; r++){

	// ...temperature
	flat_samples[0][ c * NROWS + r ] = (float)( (Math.sin( 0.50*(double) set_samples[0][ c * NROWS + r ])  ) * Math.cos( (double) set_samples[1][ c * NROWS + r ] ) ) ;


    }


    // Create the FlatFields
    // Use FlatField(FunctionType type, Set domain_set)

      // For the colored image

    vals_ff = new FlatField( func_domain_temp, domain_set);

    // ...and put the values above into it
    // Note the argument false, meaning that the array won't be copied

    vals_ff.setSamples( flat_samples , false );


      // ...and for the isocontours

    iso_vals_ff = new FlatField( func_domain_isoTemp, domain_set);


    // Get the values from the temperatur  FlatField
    // create flat_isoVals array for clarity's sake
    // "false" argument means "don't copy"

    float[][] flat_isoVals = vals_ff.getFloats(false);


    // ...and put the values above into it

    // Note the argument false, meaning that the array won't be copied again

    iso_vals_ff.setSamples( flat_isoVals , false );



    // Create Display and its maps

    // A 2D display

    display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control and draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl)  display.getGraphicsModeControl();
    dispGMC.setScaleEnable(true);

    // Create a GMCWidget with the GraphicsModeControl above

    gmcWidget = new GMCWidget( dispGMC );

    // Create the ScalarMaps: latitude to YAxis, longitude to XAxis and
    // temperature to RGB and
    // isoTemperature to IsoContour
    // Use ScalarMap(ScalarType scalar, DisplayRealType display_scalar)

    latMap = new ScalarMap( latitude,    Display.YAxis );
    lonMap = new ScalarMap( longitude, Display.XAxis );

    tempIsoMap = new ScalarMap( isoTemperature,  Display.IsoContour );
    tempRGBMap = new ScalarMap( temperature,  Display.RGB );

    // to color isolines according to temperature values
    // but don't use... see below
    isoTempRGBMap = new ScalarMap( isoTemperature, Display.RGB );

    // Add maps to display

    display.addMap( latMap );
    display.addMap( lonMap );

    display.addMap( tempIsoMap );
    display.addMap( tempRGBMap );

    // uncomment next line to color the isolines, don't forget to call
    // display.addReference( iso_data_ref, null ) below

     //display.addMap( isoTempRGBMap );

    // The ContourControl
    // Note that we get the control from the IsoContour map

    ContourControl isoControl = (ContourControl) tempIsoMap.getControl();

    // Define some parameters for contour lines

    float interval = 0.125f;  // interval between lines

    float lowValue = -01.0f;  // lowest value

    float highValue = 1.0f;   // highest value

    float base = -1.0f;       //  starting at this base value

    // ...and set the lines with the method

    isoControl.setContourInterval(interval, lowValue, highValue, base);
    //isoControl.enableLabels(true);

    // Create data references and set the FlatField as our data

    data_ref = new DataReferenceImpl("data_ref");
    iso_data_ref = new DataReferenceImpl("iso_data_ref");

    data_ref.setData( vals_ff );
    iso_data_ref.setData( iso_vals_ff );

    // Add references to display: first the colored image's reference

    display.addReference( data_ref );

      // the isolines are colored gray, according to ConstantMaps

    ConstantMap[] isolinesCMap = { new ConstantMap( 0.75f, Display.Red ),
                                  new ConstantMap( 0.75f, Display.Green ),
                                  new ConstantMap( 0.75f, Display.Blue ) };


      // ...then the isolines reference, with a the constant maps

    display.addReference( iso_data_ref, isolinesCMap );

    // Create application window and add display to window

    JFrame jframe = new JFrame("VisAD Tutorial example 3_08");
    jframe.getContentPane().setLayout(new FlowLayout( FlowLayout.CENTER ));
    jframe.getContentPane().add(display.getComponent());

    // ... and GMCWidget too

    jframe.getContentPane().add( gmcWidget );

    // Set window size and make it visible

    jframe.setSize(400, 350);
    jframe.setVisible(true);


  }


  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P3_08(args);
  }

} //end of Visad Tutorial Program 3_08
