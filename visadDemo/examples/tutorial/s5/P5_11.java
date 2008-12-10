/*
VisAD Tutorial
Copyright (C) 2000 Ugo Taddei
*/

package tutorial.s5;

// Import needed classes

import visad.*;
import visad.util.*;
import visad.data.gif.*;
import visad.java2d.DisplayImplJ2D;
import visad.java3d.DisplayImplJ3D;
import java.rmi.RemoteException;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Calendar;
import java.util.GregorianCalendar;
import visad.ss.*;


/**
  VisAD Tutorial example 5_11
  Introduce the Mapping widget
  Animating a GIF/JPEG image
   ( time -> (( longitude, latitude )  -> ( redType, greenType, blueType ) ) )
  Run program with java P5_11
 *
 */


public class P5_11{

  // Declare variables
  // The RealTypes

  private RealType time, longitude, latitude;

  // Not needed anymore
  //private RealType redType, greenType, blueType;


  // The function
  // ( time -> ( ( longitude, latitude ) -> ( redType, greenType,blueType ) ) )
  private FunctionType func_t_latlon;


  // Our Data values for longitude, latitude are represented by the set

  private Set latlonSet;

  // Time values are given by the set by the set

  private Set timeSet;


  // A FieldImpl

  private FieldImpl timeField;


  // The DataReference from the data to display

  private DataReferenceImpl data_ref;

  // The 2D display, and its the maps

  private DisplayImpl display;


  // Scalar maps from Mapping dialog will go in here
  private ScalarMap[] sMaps;

  // No start up maps needed

  //private ScalarMap timeAnimMap, timeZMap;
  //private ScalarMap lonXMap, latYMap, altiZMap;
  //private ScalarMap redMap, greenMap, blueMap;

  private AnimationControl ac;

  // The mapping dialog
  private MappingDialog md;


  public P5_11 (String[] args)
    throws RemoteException, VisADException {

    if(args.length <= 1){
      System.out.println("run with \"java P5_11 image_1.gif image_2.gif ...\"");
      return;
    }

    // The following will hold the number of images
    int nImages = args.length;

    // Create GIFForm object
    GIFForm image = new GIFForm();

    // Get the image data
    DataImpl imageData = image.open(args[0]);

    // Print out the MathType
    System.out.println(imageData.getType().prettyString());


    // Get the image type. Oh, well, we know it's a FunctionType
    FunctionType functionType = (FunctionType) imageData.getType();

    //MathType imageType = imageData.getType();


    // Get the domain...

    RealTupleType domain = (RealTupleType) functionType.getDomain();


    // Define Time and its set

    time = RealType.getRealTypeByName("Time");

    // make set as big enaough to hold all nImages
    timeSet = new Integer1DSet(time, nImages);

    // Make Function ( time -> ( Image-MathType) )

    func_t_latlon = new FunctionType(time, functionType);

    // Make Field

    timeField = new FieldImpl( func_t_latlon, timeSet);

    // Set Field with data from the images

    // set the first on, because it's already open

    timeField.setSample(0, imageData);

    // ...then set the rest
    for(int i=1;i<nImages;i++){

      imageData = image.open(args[i]);
      timeField.setSample(i, imageData);

    }

    // Create Display and its maps

    // The display

    display = new DisplayImplJ3D("display1");
    //display = new DisplayImplJ2D("display1");

    // Get display's graphics mode control draw scales

    GraphicsModeControl dispGMC = (GraphicsModeControl) display.getGraphicsModeControl();

    dispGMC.setScaleEnable(true);


    // Get preferred maps

    sMaps = timeField.getType().guessMaps( true );

    // Use method to add all maps, see method below
    addAllMaps( display, sMaps);

    // Create a data reference and set the FieldImpl as our data

    data_ref = new DataReferenceImpl("image_ref");

    data_ref.setData( timeField );

    // Add reference to display

    display.addReference( data_ref );

    // Create teh frame, which will be the MappingDialog's parent

    JFrame jframe = new JFrame("VisAD Tutorial example 5_11");

    // Create the Mapping Dialog
    md = new MappingDialog(jframe, timeField, sMaps, true, true);


    // A JButton to call the MappingDialog
    JButton remapButton = new JButton("Remap");
    remapButton.addActionListener(new ActionListener() {

      public void actionPerformed(ActionEvent E){
        try{

          // Call the mapping dialog and get the chosen maps from it
          md.display();

          sMaps = md.getMaps();

          // Clear display
          display.removeReference( data_ref );
          display.clearMaps();

          // Add chosen maps
          addAllMaps( display, sMaps);

          // Add the data reference again
          display.addReference( data_ref );

        }
        catch(VisADException ve){ ve.printStackTrace();
        }
        catch(RemoteException re){ re.printStackTrace();
        }

      }
    });


    // Put display and button into it application window

    jframe.getContentPane().setLayout( new BorderLayout());
    jframe.getContentPane().add(display.getComponent(), BorderLayout.CENTER);
    jframe.getContentPane().add(remapButton, BorderLayout.SOUTH);

    // Set window size and make it visible

    jframe.setSize(300, 300);
    jframe.setVisible(true);


  }


  // Conveniece method to add maps to a display
  // It'll check for an Animation map

  private void addAllMaps( DisplayImpl d, ScalarMap[] sm){

    for(int i=0;i<sm.length;i++){

      try{
        d.addMap( sm[i] );

        if( sm[i].getDisplayScalar().equals(Display.Animation)){

          ac =(AnimationControl) sm[i].getControl();
          ac.setOn(true);
          ac.setStep(1000);
        }

      }
      catch(VisADException ve){
        System.out.println("Couldn't add map: "+sm[i].toString() );
        ve.printStackTrace();
      }
      catch(RemoteException re){
        System.out.println("Couldn't add map: "+sm[i].toString() );
        re.printStackTrace();
      }
     }
  }

  public static void main(String[] args)
    throws RemoteException, VisADException
  {
    new P5_11(args);
  }

} //end of Visad Tutorial Program 5_11
