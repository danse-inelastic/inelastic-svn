//
// FormulaEval.java
//

/*
This program evaluates a simple formula using VisAD's formula package.
To run it, type "java FormulaEval 3.8 4.5 x+2*y" at the command line, where
"3.8" is a possible value for x, "4.5" is a possible value for y, and "x+2*y"
is the desired formula to evaluate.
*/

import java.rmi.RemoteException;
import visad.*;
import visad.formula.*;

public class FormulaEval {

   public static void main(String[] argv)
     throws VisADException, RemoteException
   {
     // get arguments from command line
     if (argv.length < 3) {
       System.out.println("Please enter three arguments: " +
         "two numbers and a formula.");
       System.exit(1);
     }
     double d1 = 0;
     double d2 = 0;
     try {
       d1 = Double.parseDouble(argv[0]);
       d2 = Double.parseDouble(argv[1]);
     }
     catch (NumberFormatException exc) {
       System.out.println("First two arguments must be numbers.");
       System.exit(2);
     }
     String formula = argv[2];

     // create two VisAD Data objects that store floating point values
     Real x = new Real(d1);
     Real y = new Real(d2);

     // create formula manager
     FormulaManager fman = FormulaUtil.createStandardManager();

     // register Data objects with formula manager
     fman.setThing("x", x);
     fman.setThing("y", y);

     // assign formula to new variable
     fman.assignFormula("f", formula);

     // wait for formula to finish computing, just to be safe
     fman.waitForFormula("f");

     // get value of function from formula manager
     Real f = (Real) fman.getThing("f");

     // print out results
     System.out.println("x = " + x.getValue() + ", y = " + y.getValue());
     System.out.println("f(x,y) = " + formula + " = " + f.getValue());

     // kill threads
     try { Thread.sleep(500); }
     catch (InterruptedException exc) { }
     ActionImpl.stopThreadPool();
   }

}
