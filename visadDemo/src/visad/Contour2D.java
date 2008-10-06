//
// Contour2D.java
//

/*
 VisAD system for interactive analysis and visualization of numerical
 data.  Copyright (C) 1996 - 2008 Bill Hibbard, Curtis Rueden, Tom
 Rink, Dave Glowacki, Steve Emmerson, Tom Whittaker, Don Murray, and
 Tommy Jasmin.

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Library General Public
 License as published by the Free Software Foundation; either
 version 2 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Library General Public License for more details.

 You should have received a copy of the GNU Library General Public
 License along with this library; if not, write to the Free
 Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
 MA 02111-1307, USA
 */

package visad;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import visad.util.Trace;

/**
 * Contour2D is a class equipped with a 2-D contouring function.
 * <P>
 */
public class Contour2D {

  // Applet variables

  /**           */
  protected Contour2D con;

  /**           */
  protected int whichlabels = 0;

  /**           */
  protected boolean showgrid;

  /**           */
  protected int rows, cols, scale;

  /**           */
  protected int[] num1, num2, num3, num4;

  /**           */
  protected float[][] vx1, vy1, vx2, vy2, vx3, vy3, vx4, vy4;

  /**           */
  public static final int EASY = 0;

  /**           */
  public static final int HARD = 1;

  /**           */
  public static final int DIFFICULTY_THRESHOLD = 600000;

  /**           */
  public static final float DIMENSION_THRESHOLD = 5.0E5f;

  /**
   * Compute contour lines for a 2-D array. If the interval is negative, then
   * contour lines less than base will be drawn as dashed lines. The contour
   * lines will be computed for all V such that:
   * 
   * <pre>
   * lowlimit &lt;= V &lt;= highlimit
   * </pre>
   * 
   * and
   * 
   * <pre>
   * V = base + n*interval  for some integer n
   * </pre>
   * 
   * Note that the input array, g, should be in column-major (FORTRAN) order.
   * 
   * @param g
   *          the 2-D array to contour.
   * @param nr
   *          size of 2-D array in rows
   * @param nc
   *          size of 2-D array in columns.
   * @param interval
   *          contour interval
   * @param lowlimit
   *          the lower limit on values to contour.
   * @param highlimit
   *          the upper limit on values to contour.
   * @param base
   *          base value to start contouring at.
   * @param vx1
   *          array to put contour line vertices (x value)
   * @param vy1
   *          array to put contour line vertices (y value)
   * @param vz1
   * @param maxv1
   *          size of vx1, vy1 arrays
   * @param numv1
   *          pointer to int to return number of vertices in vx1,vy1
   * @param vx2
   *          array to put 'hidden' contour line vertices (x value)
   * @param vy2
   *          array to put 'hidden' contour line vertices (y value)
   * @param vz2
   * @param maxv2
   *          size of vx2, vy2 arrays
   * @param numv2
   *          pointer to int to return number of vertices in vx2,vy2
   * @param vx3
   *          array to put contour label vertices (x value)
   * @param vy3
   *          array to put contour label vertices (y value)
   * @param vz3
   * @param maxv3
   *          size of vx3, vy3 arrays
   * @param numv3
   *          pointer to int to return number of vertices in vx3,vy3
   * @param vx4
   *          array to put contour label vertices, inverted (x value)
   * @param vy4
   *          array to put contour label vertices, inverted (y value) <br>**
   *          see note for VxB and VyB in PlotDigits.java
   * @param vz4
   * @param maxv4
   *          size of vx4, vy4 arrays
   * @param numv4
   *          pointer to int to return number of vertices in vx4,vy4
   * @param auxValues
   *          colors corresponding to grid points
   * @param auxLevels1
   *          colors corresponding to interpolated points for basic lines
   * @param auxLevels2
   *          colors corresponding to interpolated points for fill lines
   * @param auxLevels3
   *          colors corresponding to interpolated points for expanding label
   *          lines
   * @param swap
   * @param fill
   *          true if filling contours
   * @param tri
   * @param tri_color
   * @param grd_normals
   * @param tri_normals
   * @param interval_colors
   * @param lbl_vv
   *          values for label line segments
   * @param lbl_cc
   *          label color triples
   * @param lbl_loc
   *          center points for label locations
   * @param scale_ratio
   * @param label_size
   * @param labelColor
   * @param spatial_set
   * 
   * @throws VisADException
   */
  public static void contour(float g[], int nr, int nc, float interval,
      float lowlimit, float highlimit, float base, float vx1[][],
      float vy1[][], float[][] vz1, int maxv1, int[] numv1, float vx2[][],
      float vy2[][], float[][] vz2, int maxv2, int[] numv2, float vx3[][],
      float vy3[][], float[][] vz3, int maxv3, int[] numv3, float vx4[][],
      float vy4[][], float[][] vz4, int maxv4, int[] numv4, byte[][] auxValues,
      byte[][] auxLevels1, byte[][] auxLevels2, byte[][] auxLevels3,
      boolean[] swap, boolean fill, float[][] tri, byte[][] tri_color,
      float[][][] grd_normals, float[][] tri_normals, byte[][] interval_colors,
      float[][][][] lbl_vv, byte[][][][] lbl_cc, float[][][] lbl_loc,
      double scale_ratio, double label_size, byte[] labelColor,
      Gridded3DSet spatial_set) throws VisADException {
    boolean[] dashes = { false };
    float[] intervals = intervalToLevels(interval, lowlimit, highlimit, base,
        dashes);
    boolean dash = dashes[0];

    contour(g, nr, nc, intervals, lowlimit, highlimit, base, dash, auxValues,
        swap, fill, grd_normals, interval_colors, scale_ratio, label_size,
        labelColor, spatial_set);
  }

  /**
   * Returns an array of contour values and an indication on whether to use
   * dashed lines below the base value.
   * 
   * @param interval
   *          The contouring interval. Must be non-zero. If the interval is
   *          negative, then contour lines less than the base will be drawn as
   *          dashed lines. Must not be NaN.
   * @param low
   *          The minimum contour value. The returned array will not contain a
   *          value below this. Must not be NaN.
   * @param high
   *          The maximum contour value. The returned array will not contain a
   *          value above this. Must not be NaN.
   * @param ba
   *          The base contour value. The returned values will be integer
   *          multiples of the interval away from this this value. Must not be
   *          NaN. dash Whether or not contour lines less than the base should
   *          be drawn as dashed lines. This is a computed and returned value.
   * @param dash
   * 
   * @return
   * @throws VisADException
   *           The contour interval is zero or too small.
   */
  public static float[] intervalToLevels(float interval, float low, float high,
      float ba, boolean[] dash) throws VisADException {
    float[] levs = null;

    if (interval == 0.0) {
      throw new VisADException("Contour interval cannot be zero");
    }

    dash[0] = false;
    if (interval < 0) {
      dash[0] = true;
      interval = -interval;
    }

    // compute list of contours
    // compute nlo and nhi, for low and high contour values in the box
    long nlo = Math.round((Math.ceil((low - ba) / Math.abs(interval))));
    long nhi = Math.round((Math.floor((high - ba) / Math.abs(interval))));

    // how many contour lines are needed.
    int numc = (int) (nhi - nlo) + 1;
    if (numc < 1)
      return levs;
    if (numc > 4000) {
      throw new VisADException("Contour interval " + interval
          + " too small for range " + low + "," + high);
    }

    try {
      levs = new float[numc];
    } catch (OutOfMemoryError e) {
      throw new VisADException("Contour interval too small");
    }

    for (int i = 0; i < numc; i++) {
      levs[i] = ba + (nlo + i) * interval;
    }

    return levs;
  }

  /**           */
  public static int vertexCnt = 0;

  /**           */
  public static boolean TRUEVALUE = true;

  public static ContourOutput contour(float g[], int nr, int nc,
      float[] values, float lowlimit, float highlimit, float base,
      boolean dash, byte[][] auxValues, boolean[] swap, boolean fill,
      float[][][] grd_normals, byte[][] interval_colors, double scale_ratio,
      double label_size, byte[] labelColor, Gridded3DSet spatial_set)
      throws VisADException {

    dash = fill ? false : dash;
    PlotDigits plot = new PlotDigits();
    int ir, ic;
    int nrm, ncm;
    int numc, il;
    int lr, lc, lc2, lrr, lr2, lcc;
    float xd, yd, xx, yy;
    float xdd, ydd;
    // float clow, chi;
    float gg;

    // these are just estimates
    // int est = 2 * Length; WLH 14 April 2000
    double dest = Math.sqrt((double) spatial_set.getLength());
    int est = (int) (dest * Math.sqrt(dest));
    if (est < 1000)
      est = 1000;
    int maxv2 = est;
    int maxv1 = 2 * 2 * maxv2;
    // maxv3 and maxv4 should be equal
    int maxv3 = est;
    int maxv4 = maxv3;
    int maxsize = maxv1 + maxv2;

    // setup colors arrays
    int color_length = (auxValues != null) ? auxValues.length : 0;
    byte[][] auxLevels1 = null;
    byte[][] auxLevels2 = null;
    byte[][] auxLevels3 = null;
    if (color_length > 0) {
      auxLevels1 = new byte[color_length][maxv1];
      auxLevels2 = new byte[color_length][maxv2];
      auxLevels3 = new byte[color_length][maxv3];
    }

    // setup display coordinate arrays
    float[] vx = new float[maxsize];
    float[] vy = new float[maxsize];
    float[] vx1 = new float[maxv1];
    float[] vy1 = new float[maxv1];
    float[] vz1 = new float[maxv1];
    float[] vx2 = new float[maxv2];
    float[] vy2 = new float[maxv2];
    float[] vz2 = new float[maxv2];
    float[] vx3 = new float[maxv3];
    float[] vy3 = new float[maxv3];
    float[] vz3 = new float[maxv3];
    float[] vx4 = new float[maxv4];
    float[] vy4 = new float[maxv4];
    float[] vz4 = new float[maxv4];

    float[][] tri = new float[2][];
    float[][] tri_normals = new float[1][];
    byte[][] tri_color = new byte[color_length][];

    int numv;

    // JDM:Find the max and min values of the data
    float maxValue = Float.NEGATIVE_INFINITY;
    float minValue = Float.POSITIVE_INFINITY;
    for (int i = 0; i < g.length; i++) {
      if (g[i] > maxValue)
        maxValue = g[i];
      if (g[i] < minValue)
        minValue = g[i];
    }

    /* DRM 1999-05-18, CTR 29 Jul 1999: values could be null */
    float[] myvals = null;
    boolean debug = false;
    if (values != null && (minValue < maxValue) /* grid was not all missing */) {
      myvals = (float[]) values.clone();

      // Sort the values. Get the original indidices
      int[] indices = QuickSort.sort(myvals);

      // JDM: Now, change the order of the colors to reflect the new sort order
      byte[][] tmpColors = new byte[interval_colors.length][interval_colors[0].length];
      for (int colorIdx = 0; colorIdx < interval_colors[0].length; colorIdx++) {
        for (int rgbIdx = 0; rgbIdx < interval_colors.length; rgbIdx++) {
          tmpColors[rgbIdx][indices[colorIdx]] = interval_colors[rgbIdx][colorIdx];
        }
      }
      interval_colors = tmpColors;

      // JDM: Clip the myvals array to only use values within the range of the
      // data
      int minIdx = 0;
      int maxIdx = myvals.length - 1;

      for (int i = 0; i < myvals.length; i++) {
        if (minValue <= myvals[i]) {
          break;
        }
        minIdx = i;
        // System.err.println(
        // "min:" + minValue + " " + myvals[i] + " " + minIdx);
      }
      for (int i = myvals.length - 1; i >= 0; i--) {
        if (maxValue >= myvals[i]) {
          break;
        }
        maxIdx = i;
      }
      // debug =true;
      int newSize = maxIdx - minIdx + 1;
      int newIdx = 0;
      if (debug) {
        System.err.println("min: " + minValue + " max:" + maxValue + " idx:"
            + minIdx + "-" + maxIdx + " new size:" + newSize);
        System.err.print("original values: ");
        for (int i = 0; i < myvals.length; i++) {
          System.err.print(myvals[i] + ",");
        }
        System.err.println("");
      }

      float[] tmpValues = new float[newSize];
      tmpColors = new byte[interval_colors.length][newSize];
      for (int i = minIdx; i <= maxIdx; i++) {
        for (int rgbIdx = 0; rgbIdx < interval_colors.length; rgbIdx++) {
          tmpColors[rgbIdx][newIdx] = interval_colors[rgbIdx][i];
        }
        tmpValues[newIdx] = myvals[i];
        newIdx++;
      }

      if (debug) {
        System.err.print("new values: ");
        for (int i = 0; i < tmpValues.length; i++) {
          System.err.print(tmpValues[i] + ",");
        }
        System.err.println("");
      }

      myvals = tmpValues;
      interval_colors = tmpColors;
    }

    int low;
    int hi;

    int t;

    byte[][] auxLevels = null;
    int naux = (auxValues != null) ? auxValues.length : 0;
    byte[] auxa = null;
    byte[] auxb = null;
    byte[] auxc = null;
    byte[] auxd = null;
    if (naux > 0) {
      if (auxLevels1 == null || auxLevels1.length != naux || auxLevels2 == null
          || auxLevels2.length != naux || auxLevels3 == null
          || auxLevels3.length != naux) {
        throw new SetException("Contour2D.contour: "
            + "auxLevels length doesn't match");
      }
      for (int i = 0; i < naux; i++) {
        if (auxValues[i].length != g.length) {
          throw new SetException("Contour2D.contour: "
              + "auxValues lengths don't match");
        }
      }
      auxa = new byte[naux];
      auxb = new byte[naux];
      auxc = new byte[naux];
      auxd = new byte[naux];
      auxLevels = new byte[naux][maxsize];
    } else {
      if (auxLevels1 != null || auxLevels2 != null || auxLevels3 != null) {
        throw new SetException("Contour2D.contour: "
            + "auxValues null but auxLevels not null");
      }
    }

    // initialize vertex counts
    int[] numv1 = new int[] { 0 };
    int[] numv2 = new int[] { 0 };
    int[] numv3 = new int[] { 0 };
    int[] numv4 = new int[] { 0 };

    if (values == null)
      return null; // WLH 24 Aug 99

    // JDM: if we have no values then return
    if (myvals == null || myvals.length == 0)
      return null;

    // flags for each level indicating dashed rendering
    boolean[] dashFlags = new boolean[myvals.length];

    int numLevels = myvals.length;
    float minLevelValue = myvals[0];
    float maxLevelValue = myvals[numLevels - 1];

    /*
     * DRM: 1999-05-19 - Not needed since dash is a boolean // check for bad
     * contour interval if (interval==0.0) { throw new
     * DisplayException("Contour2D.contour: interval cannot be 0"); } if (!dash)
     * { // draw negative contour lines as dashed lines interval = -interval;
     * idash = 1; } else { idash = 0; }
     */

    nrm = nr - 1;
    ncm = nc - 1;

    xdd = ((nr - 1) - 0.0f) / (nr - 1.0f); // = 1.0
    ydd = ((nc - 1) - 0.0f) / (nc - 1.0f); // = 1.0

    /**
     * -TDR xd = xdd - 0.0001f; yd = ydd - 0.0001f; gap too big *
     */
    xd = xdd - 0.00002f;
    yd = ydd - 0.00002f;

    /*
     * set up mark array mark= 0 if avail for label center, 2 if in label, and 1
     * if not available and not in label
     * 
     * lr and lc give label size in grid boxes lrr and lcc give unavailable
     * radius
     */
    if (swap[0]) {
      lr = 1 + (nr - 2) / 10;
      lc = 1 + (nc - 2) / 50;
    } else {
      lr = 1 + (nr - 2) / 50;
      lc = 1 + (nc - 2) / 10;
    }
    lc2 = lc / 2;
    lr2 = lr / 2;
    lrr = 1 + (nr - 2) / 8;
    lcc = 1 + (nc - 2) / 8;

    // allocate mark array
    char[] mark = new char[nr * nc];

    // initialize mark array to zeros
    for (int i = 0; i < nr * nc; i++)
      mark[i] = 0;

    // set top and bottom rows to 1
    float max_g = -Float.MAX_VALUE;
    float min_g = Float.MAX_VALUE;
    for (ic = 0; ic < nc; ic++) {
      for (ir = 0; ir < lr; ir++) {
        mark[(ic) * nr + (ir)] = 1;
        mark[(ic) * nr + (nr - ir - 2)] = 1;
        float val = g[(ic) * nr + (ir)];
        if (val > max_g)
          max_g = val;
        if (val < min_g)
          min_g = val;
      }
    }

    // set left and right columns to 1
    for (ir = 0; ir < nr; ir++) {
      for (ic = 0; ic < lc; ic++) {
        mark[(ic) * nr + (ir)] = 1;
        mark[(nc - ic - 2) * nr + (ir)] = 1;
      }
    }
    numv = 0;

    // - color fill arrays
    byte[][] color_bin = null;
    byte[][][] o_flags = null;
    short[][] n_lines = null;
    short[][] ctrLow = null;

    if (fill) {
      color_bin = interval_colors;
      o_flags = new byte[nrm][ncm][];
      n_lines = new short[nrm][ncm];
      ctrLow = new short[nrm][ncm];
    }

    // - estimate contour difficutly
    // Trace.startTrace();
    Trace.call1("Contour2d.calculating difficulty");
    float left_diff = 0;
    float rght_diff = 0;
    float up_diff = 0;
    float down_diff = 0;

    int cnt_local_min_max = 0;
    int skip = (int) ((Math.max(nr, nc) / 100 < 1) ? 1 : Math.max(nr, nc) / 100);
    int test_skip = 2;
    for (ir = test_skip; ir < nrm - test_skip; ir += skip) {
      for (ic = test_skip; ic < ncm - test_skip; ic += skip) {
        up_diff = g[ic * nr + (ir + test_skip)] - g[ic * nr + ir];
        down_diff = g[ic * nr + ir] - g[ic * nr + (ir - test_skip)];
        rght_diff = g[(ic + test_skip) * nr + ir] - g[ic * nr + ir];
        left_diff = g[ic * nr + ir] - g[(ic - test_skip) * nr + ir];

        if ((left_diff * rght_diff < 0) || (up_diff * down_diff < 0)) {
          cnt_local_min_max++;
        }
      }
    }

    int threshold = cnt_local_min_max * skip * skip * skip;
    int contourDifficulty = (threshold > Contour2D.DIFFICULTY_THRESHOLD) ? Contour2D.HARD
        : Contour2D.EASY;
    Trace.call2("Contour2d.calculating difficulty",
        (contourDifficulty == EASY) ? "EASY" : "HARD");

    ContourStripSet ctrSet = new ContourStripSet(nrm, myvals, swap,
        scale_ratio, label_size, nr, nc, spatial_set, contourDifficulty);

    visad.util.Trace.call1("Contour2d.loop", " nrm=" + nrm + " ncm=" + ncm
        + " naux=" + naux + " myvals.length=" + myvals.length);

    // compute contours
    for (ir = 0; ir < nrm; ir++) {
      int ir_plus1 = ir + 1;
      xx = xdd * ir + 0.0f; // = ir
      for (ic = 0; ic < ncm; ic++) {
        int ic_plus1 = ic + 1;
        int ic_times_nr = ic * nr;
        int ic_plus1_times_nr = ic_plus1 * nr;

        float ga, gb, gc, gd;
        float gAvg, gMin, gMax;
        float tmp1, tmp2;

        // WLH 21 April 2000
        // if (numv+8 >= maxsize || nump+4 >= 2*maxsize) {
        if (numv + 8 >= maxsize) {
          // allocate more space
          maxsize = 2 * maxsize;
          /*
           * WLH 21 April 2000 int[] tt = ipnt; ipnt = new int[2 maxsize];
           * System.arraycopy(tt, 0, ipnt, 0, nump);
           */
          float[] tx = vx;
          float[] ty = vy;
          vx = new float[maxsize];
          vy = new float[maxsize];
          System.arraycopy(tx, 0, vx, 0, numv);
          System.arraycopy(ty, 0, vy, 0, numv);
          tx = null;
          ty = null;
          if (naux > 0) {
            byte[][] ta = auxLevels;
            auxLevels = new byte[naux][maxsize];
            for (int i = 0; i < naux; i++) {
              System.arraycopy(ta[i], 0, auxLevels[i], 0, numv);
            }
            ta = null;
          }
        }

        // save index of first vertex in this grid box
        // JDM: ipnt[nump++] = numv;

        yy = ydd * ic + 0.0f; // = ic
        /*
         * ga = ( g[ (ic) nr + (ir) ] ); gb = ( g[ (ic) nr + (ir+1) ] ); gc = (
         * g[ (ic+1) nr + (ir) ] ); gd = ( g[ (ic+1) nr + (ir+1) ] ); boolean
         * miss = false; if (ga != ga || gb != gb || gc != gc || gd != gd) {
         * miss = true; System.out.println("ic, ir = " + ic + "  " + ir +
         * " gabcd = " + ga + " " + gb + " " + gc + " " + gd); }
         */

        /*
         * if (ga != ga || gb != gb || gc != gc || gd != gd) { if (!anymissing)
         * { anymissing = true; System.out.println("missing"); } } else { if
         * (!anynotmissing) { anynotmissing = true;
         * System.out.println("notmissing"); } }
         */
        // get 4 corner values, skip box if any are missing
        ga = g[ic_times_nr + ir];
        if (ga != ga)
          continue;
        gb = g[ic_times_nr + ir_plus1];
        if (gb != gb)
          continue;
        gc = g[ic_plus1_times_nr + ir];
        if (gc != gc)
          continue;
        gd = g[ic_plus1_times_nr + ir_plus1];
        if (gd != gd)
          continue;

        /*
         * DRM move outside the loop byte[] auxa = null; byte[] auxb = null;
         * byte[] auxc = null; byte[] auxd = null; if (naux > 0) { auxa = new
         * byte[naux]; auxb = new byte[naux]; auxc = new byte[naux]; auxd = new
         * byte[naux];
         */
        if (naux > 0) {
          for (int i = 0; i < naux; i++) {
            byte[] auxValues_i = auxValues[i];
            auxa[i] = auxValues_i[ic_times_nr + ir];
            auxb[i] = auxValues_i[ic_times_nr + ir_plus1];
            auxc[i] = auxValues_i[ic_plus1_times_nr + ir];
            auxd[i] = auxValues_i[ic_plus1_times_nr + ir_plus1];
          }
        }

        // find average, min, and max of 4 corner values
        gAvg = (ga + gb + gc + gd) / 4.0f;

        // gMin = MIN4(ga,gb,gc,gd);
        tmp1 = ((ga) < (gb) ? (ga) : (gb));
        tmp2 = ((gc) < (gd) ? (gc) : (gd));
        gMin = ((tmp1) < (tmp2) ? (tmp1) : (tmp2));

        // gMax = MAX4(ga,gb,gc,gd);
        tmp1 = ((ga) > (gb) ? (ga) : (gb));
        tmp2 = ((gc) > (gd) ? (gc) : (gd));
        gMax = ((tmp1) > (tmp2) ? (tmp1) : (tmp2));

        /*
         * remove for new signature, replace with code below // compute clow and
         * chi, low and high contour values in the box tmp1 = (gMin-base) /
         * interval; clow = base + interval (( (tmp1) >= 0 ? (int) ((tmp1) +
         * 0.5) : (int) ((tmp1)-0.5) )-1); while (clow<gMin) { clow += interval;
         * }
         * 
         * tmp1 = (gMax-base) / interval; chi = base + interval (( (tmp1) >= 0 ?
         * (int) ((tmp1) + 0.5) : (int) ((tmp1)-0.5) )+1); while (chi>gMax) {
         * chi -= interval; }
         * 
         * // how many contour lines in the box: tmp1 = (chi-clow) / interval;
         * numc = 1+( (tmp1) >= 0 ? (int) ((tmp1) + 0.5) : (int) ((tmp1)-0.5) );
         * 
         * // gg is current contour line value gg = clow;
         */

        low = 0;
        hi = numLevels - 1;
        if (gMax < minLevelValue || gMin > maxLevelValue) {
          // no contours
          numc = 1;
        } else {
          // some inside the box
          // JDM: Instead of iterating through the whole list just do a
          // binarySearch
          /*
           * for (int i = 0; i < myvals.length; i++) { if (i == 0 && myvals[i]
           * >= gn) { low = i; } else if (myvals[i] >= gn && myvals[i-1] < gn) {
           * low = i; } if (i == 0 && myvals[i] >= gx) { hi = i; } else if
           * (myvals[i] >= gx && myvals[i-1] < gx) { hi = i; } }
           */
          hi = java.util.Arrays.binarySearch(myvals, gMax);
          if (hi < 0)
            hi = (-hi) - 1;
          if (hi >= myvals.length)
            hi = myvals.length - 1;
          low = java.util.Arrays.binarySearch(myvals, gMin);
          if (low < 0)
            low = (-low) - 1;

          numc = hi - low + 1;
        }

        // gg = myvals[low];
        /*
         * if (!any && numc > 0) { System.out.println("gMin = " + gMin +
         * " gMax = " + gMax + " gAvg = " + gAvg); System.out.println("numc = "
         * + numc + " clow = " + myvals[low] + " chi = " + myvals[hi]); any =
         * true; }
         */
        if (fill) {
          o_flags[ir][ic] = new byte[2 * numc]; // - case flags
          n_lines[ir][ic] = 0; // - number of contour line segments
          ctrLow[ir][ic] = (short) hi;
        }

        for (il = 0; il < numc; il++) {
          if ((low + il) >= myvals.length) {
            System.err.println("bad range: myvals.length=" + myvals + " il="
                + il + " low=" + low + " high=" + hi);
          }
          gg = myvals[low + il];

          // WLH 21 April 2000
          // if (numv+8 >= maxsize || nump+4 >= 2*maxsize) {
          if (numv + 8 >= maxsize) {
            // allocate more space
            maxsize = 2 * maxsize;
            /*
             * WLH 21 April 2000 int[] tt = ipnt; ipnt = new int[2 maxsize];
             * System.arraycopy(tt, 0, ipnt, 0, nump);
             */
            float[] tx = vx;
            float[] ty = vy;
            vx = new float[maxsize];
            vy = new float[maxsize];
            System.arraycopy(tx, 0, vx, 0, numv);
            System.arraycopy(ty, 0, vy, 0, numv);
            tx = null;
            ty = null;
            if (naux > 0) {
              byte[][] ta = auxLevels;
              auxLevels = new byte[naux][maxsize];
              for (int i = 0; i < naux; i++) {
                System.arraycopy(ta[i], 0, auxLevels[i], 0, numv);
              }
              ta = null;
            }
          }

          // make sure gg is within contouring limits
          if (gg < gMin)
            continue;
          if (gg > gMax)
            break;
          if (gg < lowlimit)
            continue;
          if (gg > highlimit)
            break;

          // compute orientation of lines inside box
          int ii = 0;
          if (gg > ga)
            ii = 1;
          if (gg > gb)
            ii += 2;
          if (gg > gc)
            ii += 4;
          if (gg > gd)
            ii += 8;
          if (ii > 7)
            ii = 15 - ii;
          if (ii <= 0)
            continue;

          if (fill) {
            if ((low + il) < ctrLow[ir][ic])
              ctrLow[ir][ic] = (short) (low + il);
          }

          // DO LABEL HERE
          if ((mark[(ic) * nr + (ir)]) == 0) {
            int kc, kr, mc, mr, jc, jr;

            // Insert a label

            // BOX TO AVOID
            kc = ic - lc2 - lcc;
            kr = ir - lr2 - lrr;
            mc = kc + 2 * lcc + lc - 1;
            mr = kr + 2 * lrr + lr - 1;
            // OK here
            for (jc = kc; jc <= mc; jc++) {
              if (jc >= 0 && jc < nc) {
                for (jr = kr; jr <= mr; jr++) {
                  if (jr >= 0 && jr < nr) {
                    if ((mark[(jc) * nr + (jr)]) != 2) {
                      mark[(jc) * nr + (jr)] = 1;
                    }
                  }
                }
              }
            }

            // BOX TO HOLD LABEL
            kc = ic - lc2;
            kr = ir - lr2;
            mc = kc + lc - 1;
            mr = kr + lr - 1;
            for (jc = kc; jc <= mc; jc++) {
              if (jc >= 0 && jc < nc) {
                for (jr = kr; jr <= mr; jr++) {
                  if (jr >= 0 && jr < nr) {
                    mark[(jc) * nr + (jr)] = 2;
                  }
                }
              }
            }

            if (numv4[0] + 1000 >= maxv4) {
              // allocate more space
              maxv4 = 2 * (numv4[0] + 1000);
              float[][] tx = new float[][] { vx4 };
              float[][] ty = new float[][] { vy4 };
              vx4 = new float[maxv4];
              vy4 = new float[maxv4];
              System.arraycopy(tx[0], 0, vx4, 0, numv4[0]);
              System.arraycopy(ty[0], 0, vy4, 0, numv4[0]);
              tx = null;
              ty = null;
            }

            if (numv3[0] + 1000 >= maxv3) {
              // allocate more space
              maxv3 = 2 * (numv3[0] + 1000);
              float[][] tx = new float[][] { vx3 };
              float[][] ty = new float[][] { vy3 };
              vx3 = new float[maxv3];
              vy3 = new float[maxv3];
              System.arraycopy(tx[0], 0, vx3, 0, numv3[0]);
              System.arraycopy(ty[0], 0, vy3, 0, numv3[0]);
              tx = null;
              ty = null;
              if (naux > 0) {
                byte[][] ta = auxLevels3;
                for (int i = 0; i < naux; i++) {
                  // byte[] taa = auxLevels3[i];
                  auxLevels3[i] = new byte[maxv3];
                  System.arraycopy(ta[i], 0, auxLevels3[i], 0, numv3[0]);
                }
                ta = null;
              }
            }

            /*
             * plot.plotdigits( value, xk, yk, xm, ym, maxsize, swap);
             * System.arraycopy(plot.Vx, 0, vx3[0], numv3[0], plot.NumVerts);
             * System.arraycopy(plot.Vy, 0, vy3[0], numv3[0], plot.NumVerts); if
             * (naux > 0) { for (int i=0; i<naux; i++) { for (int j=numv3[0];
             * j<numv3[0]+plot.NumVerts; j++) { auxLevels3[i][j] = auxa[i]; } }
             * }
             */
            numv3[0] += plot.NumVerts;
            /*
             * System.arraycopy(plot.VxB, 0, vx4[0], numv4[0], plot.NumVerts);
             * System.arraycopy(plot.VyB, 0, vy4[0], numv4[0], plot.NumVerts);
             */
            numv4[0] += plot.NumVerts;
          }

          float gba, gca, gdb, gdc;
          switch (ii) {
          case 1:
            gba = gb - ga;
            gca = gc - ga;

            if (naux > 0) {
              float ratioba = (gg - ga) / gba;
              float ratioca = (gg - ga) / gca;
              for (int i = 0; i < naux; i++) {
                t = (int) ((1.0f - ratioba)
                    * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                        : ((float) auxa[i])) + ratioba
                    * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                        : ((float) auxb[i])));
                auxLevels[i][numv] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                t = (int) ((1.0f - ratioca)
                    * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                        : ((float) auxa[i])) + ratioca
                    * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                        : ((float) auxc[i])));
                auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv] = auxa[i] + (auxb[i]-auxa[i])
                 * ratioba; auxLevels[i][numv+1] = auxa[i] + (auxc[i]-auxa[i])
                 * ratioca;
                 */
              }
            }

            if (((gba) < 0 ? -(gba) : (gba)) < 0.0000001) {
              vx[numv] = xx;
            } else {
              vx[numv] = xx + xd * (gg - ga) / gba;
            }
            vy[numv] = yy;
            numv++;
            if (((gca) < 0 ? -(gca) : (gca)) < 0.0000001) {
              vy[numv] = yy;
            } else {
              vy[numv] = yy + yd * (gg - ga) / gca;
            }
            vx[numv] = xx;
            numv++;
            if (fill) {
              o_flags[ir][ic][n_lines[ir][ic]] = (byte) ii;
              n_lines[ir][ic]++;
            }
            if (vx[numv - 2] == vx[numv - 1] || vy[numv - 2] == vy[numv - 1]) {
              vx[numv - 2] += 0.00001f;
              vy[numv - 1] += 0.00001f;
            }
            break;

          case 2:
            gba = gb - ga;
            gdb = gd - gb;

            if (naux > 0) {
              float ratioba = (gg - ga) / gba;
              float ratiodb = (gg - gb) / gdb;
              for (int i = 0; i < naux; i++) {
                t = (int) ((1.0f - ratioba)
                    * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                        : ((float) auxa[i])) + ratioba
                    * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                        : ((float) auxb[i])));
                auxLevels[i][numv] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                t = (int) ((1.0f - ratiodb)
                    * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                        : ((float) auxb[i])) + ratiodb
                    * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                        : ((float) auxd[i])));
                auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv] = auxa[i] + (auxb[i]-auxa[i])
                 * ratioba; auxLevels[i][numv+1] = auxb[i] + (auxd[i]-auxb[i])
                 * ratiodb;
                 */
              }
            }

            if (((gba) < 0 ? -(gba) : (gba)) < 0.0000001)
              vx[numv] = xx;
            else
              vx[numv] = xx + xd * (gg - ga) / gba;
            vy[numv] = yy;
            numv++;
            if (((gdb) < 0 ? -(gdb) : (gdb)) < 0.0000001)
              vy[numv] = yy;
            else
              vy[numv] = yy + yd * (gg - gb) / gdb;
            vx[numv] = xx + xd;
            numv++;
            if (fill) {
              o_flags[ir][ic][n_lines[ir][ic]] = (byte) ii;
              n_lines[ir][ic]++;
            }
            if (vx[numv - 2] == vx[numv - 1] || vy[numv - 2] == vy[numv - 1]) {
              vx[numv - 2] -= 0.00001f;
              vy[numv - 1] += 0.00001f;
            }
            break;

          case 3:
            gca = gc - ga;
            gdb = gd - gb;

            if (naux > 0) {
              float ratioca = (gg - ga) / gca;
              float ratiodb = (gg - gb) / gdb;
              for (int i = 0; i < naux; i++) {
                t = (int) ((1.0f - ratioca)
                    * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                        : ((float) auxa[i])) + ratioca
                    * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                        : ((float) auxc[i])));
                auxLevels[i][numv] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                t = (int) ((1.0f - ratiodb)
                    * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                        : ((float) auxb[i])) + ratiodb
                    * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                        : ((float) auxd[i])));
                auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv] = auxa[i] + (auxc[i]-auxa[i])
                 * ratioca; auxLevels[i][numv+1] = auxb[i] + (auxd[i]-auxb[i])
                 * ratiodb;
                 */
              }
            }

            if (((gca) < 0 ? -(gca) : (gca)) < 0.0000001)
              vy[numv] = yy;
            else
              vy[numv] = yy + yd * (gg - ga) / gca;
            vx[numv] = xx;
            numv++;
            if (((gdb) < 0 ? -(gdb) : (gdb)) < 0.0000001)
              vy[numv] = yy;
            else
              vy[numv] = yy + yd * (gg - gb) / gdb;
            vx[numv] = xx + xd;
            numv++;
            if (fill) {
              o_flags[ir][ic][n_lines[ir][ic]] = (byte) ii;
              n_lines[ir][ic]++;
            }
            break;

          case 4:
            gca = gc - ga;
            gdc = gd - gc;

            if (naux > 0) {
              float ratioca = (gg - ga) / gca;
              float ratiodc = (gg - gc) / gdc;
              for (int i = 0; i < naux; i++) {
                t = (int) ((1.0f - ratioca)
                    * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                        : ((float) auxa[i])) + ratioca
                    * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                        : ((float) auxc[i])));
                auxLevels[i][numv] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                t = (int) ((1.0f - ratiodc)
                    * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                        : ((float) auxc[i])) + ratiodc
                    * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                        : ((float) auxd[i])));
                auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv] = auxa[i] + (auxc[i]-auxa[i])
                 * ratioca; auxLevels[i][numv+1] = auxc[i] + (auxd[i]-auxc[i])
                 * ratiodc;
                 */
              }
            }

            if (((gca) < 0 ? -(gca) : (gca)) < 0.0000001)
              vy[numv] = yy;
            else
              vy[numv] = yy + yd * (gg - ga) / gca;
            vx[numv] = xx;
            numv++;
            if (((gdc) < 0 ? -(gdc) : (gdc)) < 0.0000001)
              vx[numv] = xx;
            else
              vx[numv] = xx + xd * (gg - gc) / gdc;
            vy[numv] = yy + yd;
            numv++;
            if (fill) {
              o_flags[ir][ic][n_lines[ir][ic]] = (byte) ii;
              n_lines[ir][ic]++;
            }
            if (vx[numv - 2] == vx[numv - 1] || vy[numv - 2] == vy[numv - 1]) {
              vx[numv - 1] += 0.00001f;
              vy[numv - 2] -= 0.00001f;
            }
            break;

          case 5:
            gba = gb - ga;
            gdc = gd - gc;

            if (naux > 0) {
              float ratioba = (gg - ga) / gba;
              float ratiodc = (gg - gc) / gdc;
              for (int i = 0; i < naux; i++) {
                t = (int) ((1.0f - ratioba)
                    * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                        : ((float) auxa[i])) + ratioba
                    * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                        : ((float) auxb[i])));
                auxLevels[i][numv] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                t = (int) ((1.0f - ratiodc)
                    * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                        : ((float) auxc[i])) + ratiodc
                    * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                        : ((float) auxd[i])));
                auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv] = auxa[i] + (auxb[i]-auxa[i])
                 * ratioba; auxLevels[i][numv+1] = auxc[i] + (auxd[i]-auxc[i])
                 * ratiodc;
                 */
              }
            }

            if (((gba) < 0 ? -(gba) : (gba)) < 0.0000001)
              vx[numv] = xx;
            else
              vx[numv] = xx + xd * (gg - ga) / gba;
            vy[numv] = yy;
            numv++;
            if (((gdc) < 0 ? -(gdc) : (gdc)) < 0.0000001)
              vx[numv] = xx;
            else
              vx[numv] = xx + xd * (gg - gc) / gdc;
            vy[numv] = yy + yd;
            numv++;
            if (fill) {
              o_flags[ir][ic][n_lines[ir][ic]] = (byte) ii;
              n_lines[ir][ic]++;
            }
            break;

          case 6:
            gba = gb - ga;
            gdc = gd - gc;
            gca = gc - ga;
            gdb = gd - gb;

            if (naux > 0) {
              float ratioba = (gg - ga) / gba;
              float ratiodc = (gg - gc) / gdc;
              float ratioca = (gg - ga) / gca;
              float ratiodb = (gg - gb) / gdb;
              for (int i = 0; i < naux; i++) {
                t = (int) ((1.0f - ratioba)
                    * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                        : ((float) auxa[i])) + ratioba
                    * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                        : ((float) auxb[i])));
                auxLevels[i][numv] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv] = auxa[i] + (auxb[i]-auxa[i])
                 * ratioba;
                 */
                if ((gg > gAvg) ^ (ga < gb)) {
                  t = (int) ((1.0f - ratioca)
                      * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                          : ((float) auxa[i])) + ratioca
                      * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                          : ((float) auxc[i])));
                  auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0
                      : ((t > 255) ? -1 : ((t < 128) ? t : t - 256)));
                  t = (int) ((1.0f - ratiodb)
                      * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                          : ((float) auxb[i])) + ratiodb
                      * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                          : ((float) auxd[i])));
                  auxLevels[i][numv + 2] = (byte) ((t < 0) ? 0
                      : ((t > 255) ? -1 : ((t < 128) ? t : t - 256)));
                  /*
                   * MEM_WLH auxLevels[i][numv+1] = auxa[i] + (auxc[i]-auxa[i])
                   * ratioca; auxLevels[i][numv+2] = auxb[i] + (auxd[i]-auxb[i])
                   * ratiodb;
                   */
                } else {
                  t = (int) ((1.0f - ratiodb)
                      * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                          : ((float) auxb[i])) + ratiodb
                      * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                          : ((float) auxd[i])));
                  auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0
                      : ((t > 255) ? -1 : ((t < 128) ? t : t - 256)));
                  t = (int) ((1.0f - ratioca)
                      * ((auxa[i] < 0) ? ((float) auxa[i]) + 256.0f
                          : ((float) auxa[i])) + ratioca
                      * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                          : ((float) auxc[i])));
                  auxLevels[i][numv + 2] = (byte) ((t < 0) ? 0
                      : ((t > 255) ? -1 : ((t < 128) ? t : t - 256)));
                  /*
                   * MEM_WLH auxLevels[i][numv+1] = auxb[i] + (auxd[i]-auxb[i])
                   * ratiodb; auxLevels[i][numv+2] = auxa[i] + (auxc[i]-auxa[i])
                   * ratioca;
                   */
                }
                t = (int) ((1.0f - ratiodc)
                    * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                        : ((float) auxc[i])) + ratiodc
                    * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                        : ((float) auxd[i])));
                auxLevels[i][numv + 3] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv+3] = auxc[i] + (auxd[i]-auxc[i])
                 * ratiodc;
                 */
              }
            }

            if (((gba) < 0 ? -(gba) : (gba)) < 0.0000001)
              vx[numv] = xx;
            else
              vx[numv] = xx + xd * (gg - ga) / gba;
            vy[numv] = yy;
            numv++;
            // here's a brain teaser
            if ((gg > gAvg) ^ (ga < gb)) { // (XOR)
              if (((gca) < 0 ? -(gca) : (gca)) < 0.0000001)
                vy[numv] = yy;
              else
                vy[numv] = yy + yd * (gg - ga) / gca;
              vx[numv] = xx;
              numv++;
              if (fill) {
                o_flags[ir][ic][n_lines[ir][ic]] = (byte) 1 + (byte) 32;
                n_lines[ir][ic]++;
              }
              if (((gdb) < 0 ? -(gdb) : (gdb)) < 0.0000001)
                vy[numv] = yy;
              else
                vy[numv] = yy + yd * (gg - gb) / gdb;
              vx[numv] = xx + xd;
              if (fill) {
                o_flags[ir][ic][n_lines[ir][ic]] = (byte) 7 + (byte) 32;
                n_lines[ir][ic]++;
              }
              numv++;
            } else {
              if (((gdb) < 0 ? -(gdb) : (gdb)) < 0.0000001)
                vy[numv] = yy;
              else
                vy[numv] = yy + yd * (gg - gb) / gdb;
              vx[numv] = xx + xd;
              numv++;
              if (fill) {
                o_flags[ir][ic][n_lines[ir][ic]] = (byte) 2 + (byte) 32;
                n_lines[ir][ic]++;
              }
              if (((gca) < 0 ? -(gca) : (gca)) < 0.0000001)
                vy[numv] = yy;
              else
                vy[numv] = yy + yd * (gg - ga) / gca;
              vx[numv] = xx;
              numv++;
              if (fill) {
                o_flags[ir][ic][n_lines[ir][ic]] = (byte) 4 + (byte) 32;
                n_lines[ir][ic]++;
              }
            }
            if (((gdc) < 0 ? -(gdc) : (gdc)) < 0.0000001)
              vx[numv] = xx;
            else
              vx[numv] = xx + xd * (gg - gc) / gdc;
            vy[numv] = yy + yd;
            numv++;
            break;

          case 7:
            gdb = gd - gb;
            gdc = gd - gc;

            if (naux > 0) {
              float ratiodb = (gg - gb) / gdb;
              float ratiodc = (gg - gc) / gdc;
              for (int i = 0; i < naux; i++) {
                t = (int) ((1.0f - ratiodb)
                    * ((auxb[i] < 0) ? ((float) auxb[i]) + 256.0f
                        : ((float) auxb[i])) + ratiodb
                    * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                        : ((float) auxd[i])));
                auxLevels[i][numv] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                t = (int) ((1.0f - ratiodc)
                    * ((auxc[i] < 0) ? ((float) auxc[i]) + 256.0f
                        : ((float) auxc[i])) + ratiodc
                    * ((auxd[i] < 0) ? ((float) auxd[i]) + 256.0f
                        : ((float) auxd[i])));
                auxLevels[i][numv + 1] = (byte) ((t < 0) ? 0 : ((t > 255) ? -1
                    : ((t < 128) ? t : t - 256)));
                /*
                 * MEM_WLH auxLevels[i][numv] = auxb[i] + (auxb[i]-auxb[i])
                 * ratiodb; auxLevels[i][numv+1] = auxc[i] + (auxd[i]-auxc[i])
                 * ratiodc;
                 */
              }
            }

            if (((gdb) < 0 ? -(gdb) : (gdb)) < 0.0000001)
              vy[numv] = yy;
            else
              vy[numv] = yy + yd * (gg - gb) / gdb;
            vx[numv] = xx + xd;
            numv++;
            if (((gdc) < 0 ? -(gdc) : (gdc)) < 0.0000001)
              vx[numv] = xx;
            else
              vx[numv] = xx + xd * (gg - gc) / gdc;
            vy[numv] = yy + yd;
            numv++;
            if (fill) {
              o_flags[ir][ic][n_lines[ir][ic]] = (byte) ii;
              n_lines[ir][ic]++;
            }
            if (vx[numv - 2] == vx[numv - 1] || vy[numv - 2] == vy[numv - 1]) {
              vx[numv - 1] -= 0.00001f;
              vy[numv - 2] -= 0.00001f;
            }
            break;
          } // switch

          // If contour level is negative, make dashed line
          if (gg < base && dash) { /* DRM: 1999-05-19 */
            dashFlags[low + il] = true;
          }
          /*
           * if ((20.0 <= vy[numv-2] && vy[numv-2] < 22.0) || (20.0 <=
           * vy[numv-1] && vy[numv-1] < 22.0)) { System.out.println("vy = " +
           * vy[numv-1] + " " + vy[numv-2] + " ic, ir = " + ic + " " + ir); }
           */

          if (ii == 6) { // - add last two pairs
            ctrSet.add(vx, vy, numv - 4, numv - 3, low + il, ir, ic);
            ctrSet.add(vx, vy, numv - 2, numv - 1, low + il, ir, ic);
          } else {
            ctrSet.add(vx, vy, numv - 2, numv - 1, low + il, ir, ic);
          }

        } // for il -- NOTE: gg incremented in for statement
      } // for ic
    } // for ir

    // System.err.println ("ii:" + ii1 + " " +ii2 + " " +ii3 + " " +ii4 + " "
    // +ii5 + " " +ii6);
    visad.util.Trace.call2("Contour2d.loop");

    /** ------------------- Color Fill ------------------------- */
    if (fill) {
      fillGridBox(g, n_lines, vx, vy, xd, xdd, yd, ydd, nr, nrm, nc, ncm,
          ctrLow, tri, tri_color, o_flags, myvals, color_bin, grd_normals,
          tri_normals);
      // BMF 2006-10-04 do not return, ie. draw labels on filled contours
      // for now, just return because we don't need to do labels
      // return;
    }

    // ---TDR, build Contour Strips

    float[][][][] lbl_vv = new float[4][][][];
    byte[][][][] lbl_cc = new byte[4][][][];
    float[][][] lbl_loc = new float[3][][];
    float[][][] vvv = new float[2][][];
    byte[][][] new_colors = new byte[2][][];

    Trace.call1("Contour2d.getLineColorArrays");
    ctrSet.getLineColorArrays(vx, vy, auxLevels, labelColor, vvv, new_colors,
        lbl_vv, lbl_cc, lbl_loc, dashFlags, contourDifficulty);
    Trace.call2("Contour2d.getLineColorArrays");

    vx2 = vvv[1][0];
    vy2 = vvv[1][1];
    vz2 = vvv[1][2];
    numv1[0] = vvv[0][0].length;
    numv2[0] = vvv[1][0].length;

    int n_lbls = lbl_vv[0].length;
    if (n_lbls > 0) {
      vx3 = lbl_vv[0][0][0];
      vy3 = lbl_vv[0][0][1];
      vz3 = lbl_vv[0][0][2];
      vx4 = lbl_vv[1][0][0];
      vy4 = lbl_vv[1][0][1];
      vz4 = lbl_vv[1][0][2];
      numv3[0] = lbl_vv[0][0][0].length;
      numv4[0] = lbl_vv[1][0][0].length;
    }

    if (auxLevels != null) {
      int clr_dim = auxValues.length;
      auxLevels1[0] = new_colors[0][0];
      auxLevels1[1] = new_colors[0][1];
      auxLevels1[2] = new_colors[0][2];
      if (clr_dim == 4)
        auxLevels1[3] = new_colors[0][3];
      auxLevels2[0] = new_colors[1][0];
      auxLevels2[1] = new_colors[1][1];
      auxLevels2[2] = new_colors[1][2];
      if (clr_dim == 4)
        auxLevels2[3] = new_colors[1][3];
      if (n_lbls > 0) {
        auxLevels3[0] = lbl_cc[0][0][0];
        auxLevels3[1] = lbl_cc[0][0][1];
        auxLevels3[2] = lbl_cc[0][0][2];
        if (clr_dim == 4)
          auxLevels3[3] = lbl_cc[0][0][3];
      }
    }

    Trace.call1("Contour2d.final block");

    if (contourDifficulty == Contour2D.EASY) {
      vx1 = vvv[0][0];
      vy1 = vvv[0][1];
      vz1 = vvv[0][2];
    } else { // contourDifficulty == Contour2D.HARD
      int start = numv1[0];

      float[][] vx_tmp = new float[1][];
      float[][] vy_tmp = new float[1][];
      float[][] vz_tmp = new float[1][];
      float[] vx1_tmp = new float[numv];
      float[] vy1_tmp = new float[numv];
      float[] vz1_tmp = new float[numv];

      byte[][] aux_tmp = null;
      byte[][] aux1_tmp = null;
      int clr_dim = 3;
      if (auxLevels != null) {
        clr_dim = auxValues.length;
        aux_tmp = new byte[4][];
        aux1_tmp = new byte[4][];
        aux1_tmp[0] = new byte[numv];
        aux1_tmp[1] = new byte[numv];
        aux1_tmp[2] = new byte[numv];
        if (clr_dim == 4)
          aux1_tmp[3] = new byte[numv];
      }

      int cnt = 0;
      for (int kk = 0; kk < ctrSet.qSet.length; kk++) {
        ctrSet.qSet[kk].getArrays(vx, vy, auxLevels, vx_tmp, vy_tmp, vz_tmp,
            aux_tmp, spatial_set);
        int len = vx_tmp[0].length;
        System.arraycopy(vx_tmp[0], 0, vx1_tmp, cnt, len);
        System.arraycopy(vy_tmp[0], 0, vy1_tmp, cnt, len);
        System.arraycopy(vz_tmp[0], 0, vz1_tmp, cnt, len);
        if (auxLevels != null) {
          System.arraycopy(aux_tmp[0], 0, aux1_tmp[0], cnt, len);
          System.arraycopy(aux_tmp[1], 0, aux1_tmp[1], cnt, len);
          System.arraycopy(aux_tmp[2], 0, aux1_tmp[2], cnt, len);
          if (clr_dim == 4)
            System.arraycopy(aux_tmp[3], 0, aux1_tmp[3], cnt, len);
        }
        cnt += len;
      }

      vx1 = new float[numv1[0] + cnt];
      vy1 = new float[numv1[0] + cnt];
      vz1 = new float[numv1[0] + cnt];
      System.arraycopy(vvv[0][0], 0, vx1, 0, numv1[0]);
      System.arraycopy(vvv[0][1], 0, vy1, 0, numv1[0]);
      System.arraycopy(vvv[0][2], 0, vz1, 0, numv1[0]);
      System.arraycopy(vx1_tmp, 0, vx1, start, cnt);
      System.arraycopy(vy1_tmp, 0, vy1, start, cnt);
      System.arraycopy(vz1_tmp, 0, vz1, start, cnt);

      if (auxLevels != null) {
        auxLevels1[0] = new byte[numv1[0] + cnt];
        auxLevels1[1] = new byte[numv1[0] + cnt];
        auxLevels1[2] = new byte[numv1[0] + cnt];
        if (clr_dim == 4)
          auxLevels1[3] = new byte[numv1[0] + cnt];

        System.arraycopy(new_colors[0][0], 0, auxLevels1[0], 0, numv1[0]);
        System.arraycopy(new_colors[0][1], 0, auxLevels1[1], 0, numv1[0]);
        System.arraycopy(new_colors[0][2], 0, auxLevels1[2], 0, numv1[0]);
        if (clr_dim == 4)
          System.arraycopy(new_colors[0][3], 0, auxLevels1[3], 0, numv1[0]);

        System.arraycopy(aux1_tmp[0], 0, auxLevels1[0], start, cnt);
        System.arraycopy(aux1_tmp[1], 0, auxLevels1[1], start, cnt);
        System.arraycopy(aux1_tmp[2], 0, auxLevels1[2], start, cnt);
        if (clr_dim == 4)
          System.arraycopy(aux1_tmp[3], 0, auxLevels1[3], start, cnt);
      }

      numv1[0] += cnt;

      vx1_tmp = null;
      vy1_tmp = null;
      vz1_tmp = null;
    }
    Trace.call2("Contour2d.final block");

    ctrSet.setGridValues(vx, vy);
    ctrSet.setGridColors(auxLevels);

    return new ContourOutput(vx1, vy1, vz1, auxLevels1, // basic lines
        vx2, vy2, vz2, auxLevels2, // fill lines
        vx3, vy3, vz3, auxLevels3, // label lines
        vx4, vy4, vz4, // expanding lines
        tri, tri_color, tri_normals, lbl_loc, lbl_vv, lbl_cc, ctrSet);

  }

  /**
   * 
   * 
   * @param g
   * @param n_lines
   * @param vx
   * @param vy
   * @param xd
   * @param xdd
   * @param yd
   * @param ydd
   * @param nr
   * @param nrm
   * @param nc
   * @param ncm
   * @param ctrLow
   * @param tri
   * @param tri_color
   * @param o_flags
   * @param values
   * @param color_bin
   * @param grd_normals
   * @param tri_normals
   */
  private static void fillGridBox(float[] g, short[][] n_lines, float[] vx,
      float[] vy, float xd, float xdd, float yd, float ydd, int nr, int nrm,
      int nc, int ncm, short[][] ctrLow, float[][] tri, byte[][] tri_color,
      byte[][][] o_flags, float[] values, byte[][] color_bin,
      float[][][] grd_normals, float[][] tri_normals) {
    float xx, yy;
    int[] numv = new int[1];
    numv[0] = 0;

    int n_tri = 0;
    for (int ir = 0; ir < nrm; ir++) {
      for (int ic = 0; ic < ncm; ic++) {
        if (n_lines[ir][ic] == 0) {
          n_tri += 2;
        } else {
          n_tri += (4 + (n_lines[ir][ic] - 1) * 2);
        }
        boolean any = false;
        if (o_flags[ir][ic] != null) {
          for (int k = 0; k < o_flags[ir][ic].length; k++) {
            if (o_flags[ir][ic][k] > 32)
              any = true;
          }
          if (any)
            n_tri += 4;
        }
      }
    }
    tri[0] = new float[n_tri * 3];
    tri[1] = new float[n_tri * 3];
    for (int kk = 0; kk < color_bin.length; kk++) {
      tri_color[kk] = new byte[n_tri * 3];
    }
    tri_normals[0] = new float[3 * n_tri * 3];

    int[] t_idx = new int[1];
    t_idx[0] = 0;
    int[] n_idx = new int[1];
    n_idx[0] = 0;

    for (int ir = 0; ir < nrm; ir++) {
      xx = xdd * ir + 0.0f;
      for (int ic = 0; ic < ncm; ic++) {
        float ga, gb, gc, gd;
        yy = ydd * ic + 0.0f;

        // get 4 corner values, skip box if any are missing
        ga = (g[(ic) * nr + (ir)]);
        // test for missing
        if (ga != ga)
          continue;
        gb = (g[(ic) * nr + (ir + 1)]);
        // test for missing
        if (gb != gb)
          continue;
        gc = (g[(ic + 1) * nr + (ir)]);
        // test for missing
        if (gc != gc)
          continue;
        gd = (g[(ic + 1) * nr + (ir + 1)]);
        // test for missing
        if (gd != gd)
          continue;

        numv[0] += n_lines[ir][ic] * 2;

        fillGridBox(new float[] { ga, gb, gc, gd }, n_lines[ir][ic], vx, vy,
            xx, yy, xd, yd, ic, ir, ctrLow[ir][ic], tri, t_idx, tri_color,
            numv[0], o_flags[ir][ic], values, color_bin, grd_normals, n_idx,
            tri_normals);
      }
    }
  }

  /**
   * 
   * 
   * @param corners
   * @param numc
   * @param vx
   * @param vy
   * @param xx
   * @param yy
   * @param xd
   * @param yd
   * @param nc
   * @param nr
   * @param ctrLow
   * @param tri
   * @param t_idx
   * @param tri_color
   * @param numv
   * @param o_flags
   * @param values
   * @param color_bin
   * @param grd_normals
   * @param n_idx
   * @param tri_normals_a
   */
  private static void fillGridBox(float[] corners, int numc, float[] vx,
      float[] vy, float xx, float yy, float xd, float yd, int nc, int nr,
      short ctrLow, float[][] tri, int[] t_idx, byte[][] tri_color, int numv,
      byte[] o_flags, float[] values, byte[][] color_bin,
      float[][][] grd_normals, int[] n_idx, float[][] tri_normals_a) {

    float[] tri_normals = tri_normals_a[0];
    int[] cnt_tri = new int[1];
    cnt_tri[0] = 0;
    int il = 0;
    int color_length = color_bin.length;
    float[] vv1 = new float[2];
    float[] vv2 = new float[2];
    float[] vv1_last = new float[2];
    float[] vv2_last = new float[2];
    float[][] vv = new float[2][2];
    float[][] vv_last = new float[2][2];

    int dir = 1;
    int start = numv - 2;
    int o_start = numc - 1;
    int o_idx = 0;
    byte o_flag = o_flags[o_idx];
    int[] closed = { 0 };
    boolean up;
    boolean right;

    int v_idx = start + dir * il * 2;

    // -- color level at corners
    // ------------------------------
    byte[][] crnr_color = new byte[4][color_length];
    boolean[] crnr_out = new boolean[] { true, true, true, true };
    boolean all_out = true;
    for (int tt = 0; tt < corners.length; tt++) {
      int cc = 0;
      int kk = 0;
      for (kk = 0; kk < (values.length - 1); kk++) {
        if ((corners[tt] >= values[kk]) && (corners[tt] < values[kk + 1])) {
          cc = kk;
          all_out = false;
          crnr_out[tt] = false;
        }
      }
      for (int ii = 0; ii < color_length; ii++) {
        crnr_color[tt][ii] = color_bin[ii][cc];
      }
    }

    int tt = t_idx[0]; // - initialize triangle vertex counter

    dir = 1;
    start = numv - numc * 2;
    o_start = 0;
    v_idx = start + dir * il * 2;
    up = false;
    right = false;
    float[] x_avg = new float[2];
    float[] y_avg = new float[2];

    if (numc > 1) { // -- first/next ctr line midpoints
      int idx = v_idx;
      x_avg[0] = (vx[idx] + vx[idx + 1]) / 2;
      y_avg[0] = (vy[idx] + vy[idx + 1]) / 2;
      idx = v_idx + 2;
      x_avg[1] = (vx[idx] + vx[idx + 1]) / 2;
      y_avg[1] = (vy[idx] + vy[idx + 1]) / 2;
      if ((x_avg[1] - x_avg[0]) > 0)
        up = true;
      if ((y_avg[1] - y_avg[0]) > 0)
        right = true;
    } else if (numc == 1) { // - default values for logic below
      x_avg[0] = 0f;
      y_avg[0] = 0f;
      x_avg[1] = 1f;
      y_avg[1] = 1f;
    } else if (numc == 0) // - empty grid box (no contour lines)
    {
      if (all_out)
        return;

      tri_normals[n_idx[0]++] = grd_normals[nc][nr][0];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr][1];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr][2];
      for (int ii = 0; ii < color_length; ii++) {
        tri_color[ii][tt] = crnr_color[0][ii];
      }
      tri[0][tt] = xx;
      tri[1][tt++] = yy;

      tri_normals[n_idx[0]++] = grd_normals[nc][nr + 1][0];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr + 1][1];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr + 1][2];
      for (int ii = 0; ii < color_length; ii++) {
        tri_color[ii][tt] = crnr_color[0][ii];
      }
      tri[0][tt] = xx + xd;
      tri[1][tt++] = yy;

      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][0];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][1];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][2];
      for (int ii = 0; ii < color_length; ii++) {
        tri_color[ii][tt] = crnr_color[0][ii];
      }
      tri[0][tt] = xx + xd;
      tri[1][tt++] = yy + yd;

      t_idx[0] = tt;
      cnt_tri[0]++;

      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][0];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][1];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][2];
      for (int ii = 0; ii < color_length; ii++) {
        tri_color[ii][tt] = crnr_color[0][ii];
      }
      tri[0][tt] = xx + xd;
      tri[1][tt++] = yy + yd;

      tri_normals[n_idx[0]++] = grd_normals[nc][nr][0];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr][1];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr][2];
      for (int ii = 0; ii < color_length; ii++) {
        tri_color[ii][tt] = crnr_color[0][ii];
      }
      tri[0][tt] = xx;
      tri[1][tt++] = yy;

      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr][0];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr][1];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr][2];
      for (int ii = 0; ii < color_length; ii++) {
        tri_color[ii][tt] = crnr_color[0][ii];
      }
      tri[0][tt] = xx;
      tri[1][tt++] = yy + yd;
      t_idx[0] = tt;

      cnt_tri[0]++;
      return;
    } // -- end no contour lines

    // --If any case 6 (saddle point), handle with special logic
    for (int iii = 0; iii < o_flags.length; iii++) {
      if (o_flags[iii] > 32) {
        fillCaseSix(xx, yy, xd, yd, v_idx, dir, o_flags, ctrLow, vx, vy, nc,
            nr, crnr_color, crnr_out, tri, t_idx, color_bin, tri_color,
            color_length, grd_normals, n_idx, tri_normals, closed, cnt_tri);
        return;
      }
    }

    // -- start making triangles for color fill
    // ---------------------------------------------

    if (o_flag == 1 || o_flag == 4 || o_flag == 2 || o_flag == 7) {
      boolean opp = false;
      float dy = 0;
      float dx = 0;
      float dist_0 = 0;
      float dist_1 = 0;

      /**
       * compare midpoints distances for first/next contour lines
       * -------------------------------------------------
       */
      if (o_flag == 1) {
        dy = (y_avg[1] - (yy));
        dx = (x_avg[1] - (xx));
        dist_1 = dy * dy + dx * dx;
        dy = (y_avg[0] - (yy));
        dx = (x_avg[0] - (xx));
        dist_0 = dy * dy + dx * dx;
      }
      if (o_flag == 2) {
        dy = (y_avg[1] - (yy));
        dx = (x_avg[1] - (xx + xd));
        dist_1 = dy * dy + dx * dx;
        dy = (y_avg[0] - (yy));
        dx = (x_avg[0] - (xx + xd));
        dist_0 = dy * dy + dx * dx;
      }
      if (o_flag == 4) {
        dy = (y_avg[1] - (yy + yd));
        dx = (x_avg[1] - (xx));
        dist_1 = dy * dy + dx * dx;
        dy = (y_avg[0] - (yy + yd));
        dx = (x_avg[0] - (xx));
        dist_0 = dy * dy + dx * dx;
      }
      if (o_flag == 7) {
        dy = (y_avg[1] - (yy + yd));
        dx = (x_avg[1] - (xx + xd));
        dist_1 = dy * dy + dx * dx;
        dy = (y_avg[0] - (yy + yd));
        dx = (x_avg[0] - (xx + xd));
        dist_0 = dy * dy + dx * dx;
      }
      if (dist_1 < dist_0)
        opp = true;
      if (opp) {
        fillToOppCorner(xx, yy, xd, yd, v_idx, o_flag, cnt_tri, dir, vx, vy,
            nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals,
            n_idx, tri_normals, closed);
      } else {
        fillToNearCorner(xx, yy, xd, yd, v_idx, o_flag, cnt_tri, dir, vx, vy,
            nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals,
            n_idx, tri_normals, closed);
      }
    } else if (o_flags[o_idx] == 3) {
      int flag = 1;
      if (right)
        flag = -1;
      fillToSide(xx, yy, xd, yd, v_idx, o_flag, flag, cnt_tri, dir, vx, vy, nc,
          nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
          tri_normals, closed);
    } else if (o_flags[o_idx] == 5) {
      int flag = 1;
      if (!up)
        flag = -1;
      fillToSide(xx, yy, xd, yd, v_idx, o_flag, flag, cnt_tri, dir, vx, vy, nc,
          nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
          tri_normals, closed);
    }

    byte last_o = o_flags[o_idx];
    int cc_start = (dir > 0) ? (ctrLow - 1) : (ctrLow + (numc - 1));

    // - move to next contour line
    // --------------------------------
    il++;
    for (il = 1; il < numc; il++) {
      v_idx = start + dir * il * 2;
      o_idx = o_start + dir * il;
      int v_idx_last = v_idx - 2 * dir;
      int cc = cc_start + dir * il;

      if (o_flags[o_idx] != last_o) // - contour line case change
      {
        byte[] side_s = new byte[2];
        byte[] last_side_s = new byte[2];
        byte[] b_arg = new byte[2];
        boolean flip;

        getBoxSide(vx, vy, xx, xd, yy, yd, v_idx, dir, o_flags[o_idx], b_arg);
        side_s[0] = b_arg[0];
        side_s[1] = b_arg[1];
        getBoxSide(vx, vy, xx, xd, yy, yd, v_idx_last, dir, last_o, b_arg);
        last_side_s[0] = b_arg[0];
        last_side_s[1] = b_arg[1];

        if (side_s[0] == last_side_s[0]) {
          flip = false;
        } else if (side_s[0] == last_side_s[1]) {
          flip = true;
        } else if (side_s[1] == last_side_s[0]) {
          flip = true;
        } else if (side_s[1] == last_side_s[1]) {
          flip = false;
        } else {
          if (((side_s[0] + last_side_s[0]) & 1) == 1) {
            flip = false;
          } else {
            flip = true;
          }
        }

        if (!flip) {
          vv1[0] = vx[v_idx];
          vv1[1] = vy[v_idx];
          vv2[0] = vx[v_idx + dir];
          vv2[1] = vy[v_idx + dir];

          vv[0][0] = vx[v_idx];
          vv[1][0] = vy[v_idx];
          vv[0][1] = vx[v_idx + dir];
          vv[1][1] = vy[v_idx + dir];
        } else {
          vv1[0] = vx[v_idx + dir];
          vv1[1] = vy[v_idx + dir];
          vv2[0] = vx[v_idx];
          vv2[1] = vy[v_idx];

          vv[0][0] = vx[v_idx + dir];
          vv[1][0] = vy[v_idx + dir];
          vv[0][1] = vx[v_idx];
          vv[1][1] = vy[v_idx];
        }
        vv1_last[0] = vx[v_idx_last];
        vv1_last[1] = vy[v_idx_last];
        vv2_last[0] = vx[v_idx_last + dir];
        vv2_last[1] = vy[v_idx_last + dir];

        vv_last[0][0] = vx[v_idx_last];
        vv_last[1][0] = vy[v_idx_last];
        vv_last[0][1] = vx[v_idx_last + dir];
        vv_last[1][1] = vy[v_idx_last + dir];

        // --- fill between contour lines
        fillToLast(xx, yy, xd, yd, nc, nr, vv1, vv2, vv1_last, vv2_last, tri,
            cnt_tri, t_idx, tri_color, color_bin, cc, color_length,
            grd_normals, n_idx, tri_normals);

        byte[] b_arg2 = new byte[2];
        getBoxSide(vv[0], vv[1], xx, xd, yy, yd, 0, dir, o_flags[o_idx], b_arg);
        getBoxSide(vv_last[0], vv_last[1], xx, xd, yy, yd, 0, dir, last_o,
            b_arg2);

        for (int kk = 0; kk < 2; kk++) { // - close off corners
          float[] vvx = new float[2];
          float[] vvy = new float[2];
          byte side = 0;
          byte last_s = 0;

          side = b_arg[kk];
          last_s = b_arg2[kk];

          if (side != last_s) {
            if ((side == 0 && last_s == 3) || (side == 3 && last_s == 0)) { // -
                                                                            // case
                                                                            // 1
              fillToNearCorner(xx, yy, xd, yd, 0, (byte) 1, cnt_tri, 1,
                  new float[] { vv[0][kk], vv_last[0][kk] }, new float[] {
                      vv[1][kk], vv_last[1][kk] }, nc, nr, crnr_color,
                  crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
                  tri_normals, closed);
            }
            if ((side == 0 && last_s == 1) || (side == 1 && last_s == 0)) { // -
                                                                            // case
                                                                            // 2
              fillToNearCorner(xx, yy, xd, yd, 0, (byte) 2, cnt_tri, 1,
                  new float[] { vv[0][kk], vv_last[0][kk] }, new float[] {
                      vv[1][kk], vv_last[1][kk] }, nc, nr, crnr_color,
                  crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
                  tri_normals, closed);
            }
            if ((side == 2 && last_s == 3) || (side == 3 && last_s == 2)) { // -
                                                                            // case
                                                                            // 4
              fillToNearCorner(xx, yy, xd, yd, 0, (byte) 4, cnt_tri, 1,
                  new float[] { vv[0][kk], vv_last[0][kk] }, new float[] {
                      vv[1][kk], vv_last[1][kk] }, nc, nr, crnr_color,
                  crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
                  tri_normals, closed);
            }
            if ((side == 2 && last_s == 1) || (side == 1 && last_s == 2)) { // -
                                                                            // case
                                                                            // 7
              fillToNearCorner(xx, yy, xd, yd, 0, (byte) 7, cnt_tri, 1,
                  new float[] { vv[0][kk], vv_last[0][kk] }, new float[] {
                      vv[1][kk], vv_last[1][kk] }, nc, nr, crnr_color,
                  crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
                  tri_normals, closed);
            }
            if ((side == 2 && last_s == 0) || (side == 0 && last_s == 2)) { // -
                                                                            // case
                                                                            // 5
              if (side == 0) {
                vvx[0] = vv[0][kk];
                vvy[0] = vv[1][kk];
                vvx[1] = vv_last[0][kk];
                vvy[1] = vv_last[1][kk];
              } else {
                vvx[0] = vv_last[0][kk];
                vvy[0] = vv_last[1][kk];
                vvx[1] = vv[0][kk];
                vvy[1] = vv[1][kk];
              }
              int flag = -1;
              if (((closed[0] & 4) == 0) && ((closed[0] & 1) == 0))
                flag = 1;
              fillToSide(xx, yy, xd, yd, 0, (byte) 5, flag, cnt_tri, 1, vvx,
                  vvy, nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color,
                  grd_normals, n_idx, tri_normals, closed);
            }
            if ((side == 1 && last_s == 3) || (side == 3 && last_s == 1)) { // -
                                                                            // case
                                                                            // 3
              if (side == 3) {
                vvx[0] = vv[0][kk];
                vvy[0] = vv[1][kk];
                vvx[1] = vv_last[0][kk];
                vvy[1] = vv_last[1][kk];
              } else {
                vvx[0] = vv_last[0][kk];
                vvy[0] = vv_last[1][kk];
                vvx[1] = vv[0][kk];
                vvy[1] = vv[1][kk];
              }
              int flag = -1;
              if (((closed[0] & 4) == 0) && ((closed[0] & 8) == 0))
                flag = 1;
              fillToSide(xx, yy, xd, yd, 0, (byte) 3, flag, cnt_tri, 1, vvx,
                  vvy, nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color,
                  grd_normals, n_idx, tri_normals, closed);
            }
          }
        }
      } else {
        vv1[0] = vx[v_idx];
        vv1[1] = vy[v_idx];
        vv2[0] = vx[v_idx + dir];
        vv2[1] = vy[v_idx + dir];
        vv1_last[0] = vx[v_idx_last];
        vv1_last[1] = vy[v_idx_last];
        vv2_last[0] = vx[v_idx_last + dir];
        vv2_last[1] = vy[v_idx_last + dir];

        fillToLast(xx, yy, xd, yd, nc, nr, vv1, vv2, vv1_last, vv2_last, tri,
            cnt_tri, t_idx, tri_color, color_bin, cc, color_length,
            grd_normals, n_idx, tri_normals);
      }
      last_o = o_flags[o_idx];
    } // ---- contour loop

    /*- last or first/last contour line
    ------------------------------------*/
    int flag_set = 0;
    if ((last_o == 1) || (last_o == 2) || (last_o == 4) || (last_o == 7)) {
      if (last_o == 1)
        flag_set = (closed[0] & 1);
      if (last_o == 2)
        flag_set = (closed[0] & 2);
      if (last_o == 4)
        flag_set = (closed[0] & 4);
      if (last_o == 7)
        flag_set = (closed[0] & 8);

      if (flag_set > 0) {
        fillToOppCorner(xx, yy, xd, yd, v_idx, last_o, cnt_tri, dir, vx, vy,
            nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals,
            n_idx, tri_normals, closed);
      } else {
        fillToNearCorner(xx, yy, xd, yd, v_idx, last_o, cnt_tri, dir, vx, vy,
            nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals,
            n_idx, tri_normals, closed);
      }
    } else if (last_o == 3) {
      int flag = -1;
      if (closed[0] == 3)
        flag = 1;
      fillToSide(xx, yy, xd, yd, v_idx, last_o, flag, cnt_tri, dir, vx, vy, nc,
          nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
          tri_normals, closed);
    } else if (last_o == 5) {
      int flag = 1;
      if (closed[0] == 5)
        flag = -1;
      fillToSide(xx, yy, xd, yd, v_idx, last_o, flag, cnt_tri, dir, vx, vy, nc,
          nr, crnr_color, crnr_out, tri, t_idx, tri_color, grd_normals, n_idx,
          tri_normals, closed);
    }

  } // --- end fillGridBox

  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param xx
   * @param xd
   * @param yy
   * @param yd
   * @param v_idx
   * @param dir
   * @param o_flag
   * @param side
   */
  private static void getBoxSide(float[] vx, float[] vy, float xx, float xd,
      float yy, float yd, int v_idx, int dir, byte o_flag, byte[] side) {
    /*
     * if (vy[v_idx] == yy) side[0] = 0; // a-b if (vy[v_idx] == (yy + yd))
     * side[0] = 2; // c-d if (vx[v_idx] == xx) side[0] = 3; // a-c if
     * (vx[v_idx] == (xx + xd)) side[0] = 1; // b-d
     */

    for (int kk = 0; kk < 2; kk++) {
      int ii = v_idx + kk * dir;
      switch (o_flag) {
      case 1:
        side[kk] = 3;
        if (vy[ii] == yy)
          side[kk] = 0;
        break;
      case 2:
        side[kk] = 1;
        if (vy[ii] == yy)
          side[kk] = 0;
        break;
      case 4:
        side[kk] = 3;
        if (vy[ii] == (yy + yd))
          side[kk] = 2;
        break;
      case 7:
        side[kk] = 1;
        if (vy[ii] == (yy + yd))
          side[kk] = 2;
        break;
      case 3:
        side[kk] = 1;
        if (vx[ii] == xx)
          side[kk] = 3;
        break;
      case 5:
        side[kk] = 0;
        if (vy[ii] == (yy + yd))
          side[kk] = 2;
        break;
      }
    }
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param xx
   * @param yy
   * @param nc
   * @param nr
   * @param xd
   * @param yd
   * @param grd_normals
   * @param n_idx
   * @param tri_normals
   */
  private static void interpNormals(float vx, float vy, float xx, float yy,
      int nc, int nr, float xd, float yd, float[][][] grd_normals, int[] n_idx,
      float[] tri_normals) {
    int side = -1;
    float[] nn = new float[3];

    if (vy == yy)
      side = 0; // a-b
    if (vy == (yy + yd))
      side = 2; // c-d
    if (vx == xx)
      side = 3; // a-c
    if (vx == (xx + xd))
      side = 1; // b-d

    float dx = vx - xx;
    float dy = vy - yy;

    switch (side) {
    case 0:
      nn[0] = ((grd_normals[nc][nr + 1][0] - grd_normals[nc][nr][0]) / xd) * dx
          + grd_normals[nc][nr][0];
      nn[1] = ((grd_normals[nc][nr + 1][1] - grd_normals[nc][nr][1]) / xd) * dx
          + grd_normals[nc][nr][1];
      nn[2] = ((grd_normals[nc][nr + 1][2] - grd_normals[nc][nr][2]) / xd) * dx
          + grd_normals[nc][nr][2];
      break;
    case 3:
      nn[0] = ((grd_normals[nc + 1][nr][0] - grd_normals[nc][nr][0]) / yd) * dy
          + grd_normals[nc][nr][0];
      nn[1] = ((grd_normals[nc + 1][nr][1] - grd_normals[nc][nr][1]) / yd) * dy
          + grd_normals[nc][nr][1];
      nn[2] = ((grd_normals[nc + 1][nr][2] - grd_normals[nc][nr][2]) / yd) * dy
          + grd_normals[nc][nr][2];
      break;
    case 1:
      nn[0] = ((grd_normals[nc + 1][nr + 1][0] - grd_normals[nc][nr + 1][0]) / yd)
          * dy + grd_normals[nc][nr + 1][0];
      nn[1] = ((grd_normals[nc + 1][nr + 1][1] - grd_normals[nc][nr + 1][1]) / yd)
          * dy + grd_normals[nc][nr + 1][1];
      nn[2] = ((grd_normals[nc + 1][nr + 1][2] - grd_normals[nc][nr + 1][2]) / yd)
          * dy + grd_normals[nc][nr + 1][2];
      break;
    case 2:
      nn[0] = ((grd_normals[nc + 1][nr + 1][0] - grd_normals[nc + 1][nr][0]) / xd)
          * dx + grd_normals[nc + 1][nr][0];
      nn[1] = ((grd_normals[nc + 1][nr + 1][1] - grd_normals[nc + 1][nr][1]) / xd)
          * dx + grd_normals[nc + 1][nr][1];
      nn[2] = ((grd_normals[nc + 1][nr + 1][2] - grd_normals[nc + 1][nr][2]) / xd)
          * dx + grd_normals[nc + 1][nr][2];
      break;
    default:
      System.out.println("interpNormals, bad side: " + side);
    }
    // - re-normalize
    float mag = (float) Math
        .sqrt(nn[0] * nn[0] + nn[1] * nn[1] + nn[2] * nn[2]);
    nn[0] /= mag;
    nn[1] /= mag;
    nn[2] /= mag;
    tri_normals[n_idx[0]++] = nn[0];
    tri_normals[n_idx[0]++] = nn[1];
    tri_normals[n_idx[0]++] = nn[2];
  }

  /**
   * 
   * 
   * @param xx
   * @param yy
   * @param xd
   * @param yd
   * @param nc
   * @param nr
   * @param vv1
   * @param vv2
   * @param vv1_last
   * @param vv2_last
   * @param tri
   * @param cnt_tri
   * @param t_idx
   * @param tri_color
   * @param color_bin
   * @param cc
   * @param color_length
   * @param grd_normals
   * @param n_idx
   * @param tri_normals
   */
  private static void fillToLast(float xx, float yy, float xd, float yd,
      int nc, int nr, float[] vv1, float[] vv2, float[] vv1_last,
      float[] vv2_last, float[][] tri, int[] cnt_tri, int[] t_idx,
      byte[][] tri_color, byte[][] color_bin, int cc, int color_length,
      float[][][] grd_normals, int[] n_idx, float[] tri_normals) {
    int tt = t_idx[0];

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = color_bin[ii][cc];
    }
    tri[0][tt] = vv1[0];
    tri[1][tt] = vv1[1];
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = color_bin[ii][cc];
    }
    tri[0][tt] = vv2[0];
    tri[1][tt] = vv2[1];
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = color_bin[ii][cc];
    }
    tri[0][tt] = vv1_last[0];
    tri[1][tt] = vv1_last[1];
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;
    cnt_tri[0]++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = color_bin[ii][cc];
    }
    tri[0][tt] = vv1_last[0];
    tri[1][tt] = vv1_last[1];
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = color_bin[ii][cc];
    }
    tri[0][tt] = vv2_last[0];
    tri[1][tt] = vv2_last[1];
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = color_bin[ii][cc];
    }
    tri[0][tt] = vv2[0];
    tri[1][tt] = vv2[1];
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;
    t_idx[0] = tt;
    cnt_tri[0]++;
  }

  /**
   * 
   * 
   * @param xx
   * @param yy
   * @param xd
   * @param yd
   * @param v_idx
   * @param dir
   * @param o_flags
   * @param ctrLow
   * @param vx
   * @param vy
   * @param nc
   * @param nr
   * @param crnr_color
   * @param crnr_out
   * @param tri
   * @param t_idx
   * @param color_bin
   * @param tri_color
   * @param color_length
   * @param grd_normals
   * @param n_idx
   * @param tri_normals
   * @param closed
   * @param cnt_tri
   */
  private static void fillCaseSix(float xx, float yy, float xd, float yd,
      int v_idx, int dir, byte[] o_flags, short ctrLow, float[] vx, float[] vy,
      int nc, int nr, byte[][] crnr_color, boolean[] crnr_out, float[][] tri,
      int[] t_idx, byte[][] color_bin, byte[][] tri_color, int color_length,
      float[][][] grd_normals, int[] n_idx, float[] tri_normals, int[] closed,
      int[] cnt_tri) {

    int n1 = 0;
    int n2 = 0;
    int n4 = 0;
    int n7 = 0;

    for (int kk = 0; kk < o_flags.length; kk++) {
      if ((o_flags[kk] - 32) == 1 || o_flags[kk] == 1)
        n1++;
      if ((o_flags[kk] - 32) == 2 || o_flags[kk] == 2)
        n2++;
      if ((o_flags[kk] - 32) == 4 || o_flags[kk] == 4)
        n4++;
      if ((o_flags[kk] - 32) == 7 || o_flags[kk] == 7)
        n7++;
    }
    float[][] vv1 = new float[2][n1 * 2];
    float[][] vv2 = new float[2][n2 * 2];
    float[][] vv4 = new float[2][n4 * 2];
    float[][] vv7 = new float[2][n7 * 2];
    int[] clr_idx1 = new int[n1];
    int[] clr_idx2 = new int[n2];
    int[] clr_idx4 = new int[n4];
    int[] clr_idx7 = new int[n7];
    float[] vvv1 = new float[2];
    float[] vvv2 = new float[2];
    float[] vvv1_last = new float[2];
    float[] vvv2_last = new float[2];

    n1 = 0;
    n2 = 0;
    n4 = 0;
    n7 = 0;
    int ii = v_idx;
    int cc = ctrLow - 1;
    int cnt = 0;
    int[] cases = { 1, 2, 7, 4 }; // - corner cases, clockwise around box

    for (int kk = 0; kk < o_flags.length; kk++) {
      if (o_flags[kk] > 32)
        cnt++;

      if ((o_flags[kk] - 32) == 1 || o_flags[kk] == 1) {
        clr_idx1[n1] = cc;
        vv1[0][2 * n1] = vx[ii];
        vv1[1][2 * n1] = vy[ii];
        vv1[0][2 * n1 + 1] = vx[ii + 1];
        vv1[1][2 * n1 + 1] = vy[ii + 1];
        n1++;
      } else if ((o_flags[kk] - 32) == 2 || o_flags[kk] == 2) {
        clr_idx2[n2] = cc;
        vv2[0][2 * n2] = vx[ii];
        vv2[1][2 * n2] = vy[ii];
        vv2[0][2 * n2 + 1] = vx[ii + 1];
        vv2[1][2 * n2 + 1] = vy[ii + 1];
        n2++;
      } else if ((o_flags[kk] - 32) == 4 || o_flags[kk] == 4) {
        clr_idx4[n4] = cc;
        vv4[0][2 * n4] = vx[ii];
        vv4[1][2 * n4] = vy[ii];
        vv4[0][2 * n4 + 1] = vx[ii + 1];
        vv4[1][2 * n4 + 1] = vy[ii + 1];
        n4++;
      } else if ((o_flags[kk] - 32) == 7 || o_flags[kk] == 7) {
        clr_idx7[n7] = cc;
        vv7[0][2 * n7] = vx[ii];
        vv7[1][2 * n7] = vy[ii];
        vv7[0][2 * n7 + 1] = vx[ii + 1];
        vv7[1][2 * n7 + 1] = vy[ii + 1];
        n7++;
      }
      if (o_flags[kk] < 32) {
        cc += 1;
      } else if (cnt == 2) {
        cnt = 0;
        cc++;
      }
      ii += 2;
    }

    int[] clr_idx = null;
    float[] vvx = null;
    float[] vvy = null;
    float[] x_avg = new float[2];
    float[] y_avg = new float[2];
    float dist_0 = 0;
    float dist_1 = 0;
    float xxx = 0;
    float yyy = 0;
    float dx = 0;
    float dy = 0;
    int nn = 0;
    int pt = 0;
    int n_pt = 0;
    int s_idx = 0;
    int ns_idx = 0;
    byte[] tmp = null;
    byte[] cntr_color = null;
    int cntr_clr = Integer.MIN_VALUE;

    float[][] edge_points = new float[2][8];
    boolean[] edge_point_a_corner = { false, false, false, false, false, false,
        false, false };
    boolean[] edge_point_out = { false, false, false, false, false, false,
        false, false };
    boolean this_crnr_out = false;
    int n_crnr_out = 0;

    // - fill corners
    for (int kk = 0; kk < cases.length; kk++) {
      switch (cases[kk]) {
      case 1:
        nn = n1;
        clr_idx = clr_idx1;
        vvx = vv1[0];
        vvy = vv1[1];
        xxx = xx;
        yyy = yy;
        pt = 0;
        n_pt = 7;
        s_idx = 0;
        ns_idx = 1;
        tmp = crnr_color[0];
        this_crnr_out = crnr_out[0];
        break;
      case 2:
        nn = n2;
        clr_idx = clr_idx2;
        vvx = vv2[0];
        vvy = vv2[1];
        xxx = xx + xd;
        yyy = yy;
        pt = 1;
        n_pt = 2;
        s_idx = 0;
        ns_idx = 1;
        tmp = crnr_color[1];
        this_crnr_out = crnr_out[1];
        break;
      case 4:
        nn = n4;
        clr_idx = clr_idx4;
        vvx = vv4[0];
        vvy = vv4[1];
        xxx = xx;
        yyy = yy + yd;
        pt = 5;
        n_pt = 6;
        s_idx = 1;
        ns_idx = 0;
        tmp = crnr_color[2];
        this_crnr_out = crnr_out[2];
        break;
      case 7:
        nn = n7;
        clr_idx = clr_idx7;
        vvx = vv7[0];
        vvy = vv7[1];
        xxx = xx + xd;
        yyy = yy + yd;
        pt = 3;
        n_pt = 4;
        s_idx = 0;
        ns_idx = 1;
        tmp = crnr_color[3];
        this_crnr_out = crnr_out[3];
        break;
      }

      if (nn == 0) {
        edge_points[0][pt] = xxx;
        edge_points[1][pt] = yyy;
        edge_points[0][n_pt] = xxx;
        edge_points[1][n_pt] = yyy;
        cntr_color = tmp;
        edge_point_a_corner[pt] = true;
        edge_point_a_corner[n_pt] = true;
        edge_point_out[pt] = this_crnr_out;
        edge_point_out[n_pt] = this_crnr_out;
        if (this_crnr_out)
          n_crnr_out++;
      } else if (nn == 1) {
        fillToNearCorner(xx, yy, xd, yd, 0, (byte) cases[kk], cnt_tri, dir,
            vvx, vvy, nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color,
            grd_normals, n_idx, tri_normals, closed);

        edge_points[0][pt] = vvx[s_idx];
        edge_points[1][pt] = vvy[s_idx];
        edge_points[0][n_pt] = vvx[ns_idx];
        edge_points[1][n_pt] = vvy[ns_idx];
        if (clr_idx[0] > cntr_clr)
          cntr_clr = clr_idx[0];
      } else {
        int il = 0;
        int idx = 0;
        x_avg[0] = (vvx[idx] + vvx[idx + 1]) / 2;
        y_avg[0] = (vvy[idx] + vvy[idx + 1]) / 2;
        idx = idx + 2;
        x_avg[1] = (vvx[idx] + vvx[idx + 1]) / 2;
        y_avg[1] = (vvy[idx] + vvy[idx + 1]) / 2;

        dy = (y_avg[1] - (yyy));
        dx = (x_avg[1] - (xxx));
        dist_1 = dy * dy + dx * dx;
        dy = (y_avg[0] - (yyy));
        dx = (x_avg[0] - (xxx));
        dist_0 = dy * dy + dx * dx;

        boolean cornerFirst = false;
        if (dist_1 > dist_0)
          cornerFirst = true;

        if (cornerFirst) {
          fillToNearCorner(xx, yy, xd, yd, 0, (byte) cases[kk], cnt_tri, dir,
              vvx, vvy, nc, nr, crnr_color, crnr_out, tri, t_idx, tri_color,
              grd_normals, n_idx, tri_normals, closed);
        } else {
          edge_points[0][pt] = vvx[s_idx];
          edge_points[1][pt] = vvy[s_idx];
          edge_points[0][n_pt] = vvx[ns_idx];
          edge_points[1][n_pt] = vvy[ns_idx];
          if (clr_idx[0] > cntr_clr)
            cntr_clr = clr_idx[0];
        }
        for (il = 1; il < nn; il++) {
          idx = dir * il * 2;
          int idx_last = idx - 2 * dir;

          vvv1[0] = vvx[idx];
          vvv1[1] = vvy[idx];
          vvv2[0] = vvx[idx + dir];
          vvv2[1] = vvy[idx + dir];
          vvv1_last[0] = vvx[idx_last];
          vvv1_last[1] = vvy[idx_last];
          vvv2_last[0] = vvx[idx_last + dir];
          vvv2_last[1] = vvy[idx_last + dir];

          fillToLast(xx, yy, xd, yd, nc, nr, vvv1, vvv2, vvv1_last, vvv2_last,
              tri, cnt_tri, t_idx, tri_color, color_bin, clr_idx[il],
              color_length, grd_normals, n_idx, tri_normals);

          if (!cornerFirst && il == (nn - 1)) {
            fillToNearCorner(xx, yy, xd, yd, idx, (byte) cases[kk], cnt_tri,
                dir, vvx, vvy, nc, nr, crnr_color, crnr_out, tri, t_idx,
                tri_color, grd_normals, n_idx, tri_normals, closed);
          }
          if (cornerFirst && il == (nn - 1)) {
            edge_points[0][pt] = vvx[idx + s_idx];
            edge_points[1][pt] = vvy[idx + s_idx];
            edge_points[0][n_pt] = vvx[idx + ns_idx];
            edge_points[1][n_pt] = vvy[idx + ns_idx];
            if (clr_idx[il] > cntr_clr)
              cntr_clr = clr_idx[il];
          }
        }
      }
    }

    // - fill remainder with tris all sharing center point
    // ----------------------------------------------------
    if (n_crnr_out == 2) { // - don't fill center region
      return;
    }

    if (cntr_color == null) { // - All corners were closed off
      cntr_color = new byte[color_length];
      for (int c = 0; c < color_length; c++) {
        cntr_color[c] = color_bin[c][cntr_clr];
      }
    }
    int tt = t_idx[0];
    for (int kk = 0; kk < edge_points[0].length; kk++) {
      pt = kk;
      n_pt = kk + 1;
      if (kk == (edge_points[0].length - 1)) {
        pt = 0;
        n_pt = 7;
      }

      if (edge_point_a_corner[pt] || edge_point_a_corner[n_pt]) {
        if (edge_point_out[pt] || edge_point_out[n_pt])
          continue;
      }

      for (int c = 0; c < color_length; c++) {
        tri_color[c][tt] = cntr_color[c];
      }
      tri[0][tt] = edge_points[0][pt];
      tri[1][tt] = edge_points[1][pt];
      interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd,
          grd_normals, n_idx, tri_normals);
      tt++;

      for (int c = 0; c < color_length; c++) {
        tri_color[c][tt] = cntr_color[c];
      }
      tri[0][tt] = edge_points[0][n_pt];
      tri[1][tt] = edge_points[1][n_pt];
      interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd,
          grd_normals, n_idx, tri_normals);
      tt++;

      // - center point
      for (int c = 0; c < color_length; c++) {
        tri_color[c][tt] = cntr_color[c];
      }
      tri[0][tt] = xx + xd * 0.5f;
      tri[1][tt] = yy + yd * 0.5f;
      // - center normal, interpolate from corners
      float[] nrm = { 0f, 0f, 0f };
      for (int ic = 0; ic < 2; ic++) {
        for (int ir = 0; ir < 2; ir++) {
          nrm[0] += 0.25 * grd_normals[nc + ic][nr + ir][0];
          nrm[1] += 0.25 * grd_normals[nc + ic][nr + ir][1];
          nrm[2] += 0.25 * grd_normals[nc + ic][nr + ir][2];
        }
      }
      // - renormalize normal
      float mag = (float) Math.sqrt(nrm[0] * nrm[0] + nrm[1] * nrm[1] + nrm[2]
          * nrm[2]);
      nrm[0] /= mag;
      nrm[1] /= mag;
      nrm[2] /= mag;
      tri_normals[n_idx[0]++] = nrm[0];
      tri_normals[n_idx[0]++] = nrm[1];
      tri_normals[n_idx[0]++] = nrm[2];
      tt++;

      cnt_tri[0]++;
    }
    t_idx[0] = tt;

  }

  /**
   * 
   * 
   * @param xx
   * @param yy
   * @param xd
   * @param yd
   * @param v_idx
   * @param o_flag
   * @param cnt
   * @param dir
   * @param vx
   * @param vy
   * @param nc
   * @param nr
   * @param crnr_color
   * @param crnr_out
   * @param tri
   * @param t_idx
   * @param tri_color
   * @param grd_normals
   * @param n_idx
   * @param tri_normals
   * @param closed
   */
  private static void fillToNearCorner(float xx, float yy, float xd, float yd,
      int v_idx, byte o_flag, int[] cnt, int dir, float[] vx, float[] vy,
      int nc, int nr, byte[][] crnr_color, boolean[] crnr_out, float[][] tri,
      int[] t_idx, byte[][] tri_color, float[][][] grd_normals, int[] n_idx,
      float[] tri_normals, int[] closed) {
    float cx = 0;
    float cy = 0;
    int cc = 0;

    int color_length = crnr_color[0].length;
    int cnt_tri = cnt[0];
    int tt = t_idx[0];

    switch (o_flag) {
    case 1:
      cc = 0;
      closed[0] = closed[0] | 1;
      if (crnr_out[cc])
        return;
      cx = xx;
      cy = yy;
      tri_normals[n_idx[0]++] = grd_normals[nc][nr][0];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr][1];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr][2];
      break;
    case 4:
      cc = 2;
      closed[0] = closed[0] | 4;
      if (crnr_out[cc])
        return;
      cx = xx;
      cy = yy + yd;
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr][0];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr][1];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr][2];
      break;
    case 2:
      cc = 1;
      closed[0] = closed[0] | 2;
      if (crnr_out[cc])
        return;
      cx = xx + xd;
      cy = yy;
      tri_normals[n_idx[0]++] = grd_normals[nc][nr + 1][0];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr + 1][1];
      tri_normals[n_idx[0]++] = grd_normals[nc][nr + 1][2];
      break;
    case 7:
      cc = 3;
      closed[0] = closed[0] | 8;
      if (crnr_out[cc])
        return;
      cx = xx + xd;
      cy = yy + yd;
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][0];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][1];
      tri_normals[n_idx[0]++] = grd_normals[nc + 1][nr + 1][2];
      break;
    }

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx;
    tri[1][tt] = cy;
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = vx[v_idx];
    tri[1][tt] = vy[v_idx];
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = vx[v_idx + dir];
    tri[1][tt] = vy[v_idx + dir];
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    cnt_tri++;
    cnt[0] = cnt_tri;
    t_idx[0] = tt;
  }

  /**
   * 
   * 
   * @param xx
   * @param yy
   * @param xd
   * @param yd
   * @param v_idx
   * @param o_flag
   * @param cnt
   * @param dir
   * @param vx
   * @param vy
   * @param nc
   * @param nr
   * @param crnr_color
   * @param crnr_out
   * @param tri
   * @param t_idx
   * @param tri_color
   * @param grd_normals
   * @param n_idx
   * @param tri_normals
   * @param closed
   */
  private static void fillToOppCorner(float xx, float yy, float xd, float yd,
      int v_idx, byte o_flag, int[] cnt, int dir, float[] vx, float[] vy,
      int nc, int nr, byte[][] crnr_color, boolean[] crnr_out, float[][] tri,
      int[] t_idx, byte[][] tri_color, float[][][] grd_normals, int[] n_idx,
      float[] tri_normals, int[] closed) {

    float cx1 = 0;
    float cx2 = 0;
    float cx3 = 0;
    float cy1 = 0;
    float cy2 = 0;
    float cy3 = 0;
    int cc = 0;
    int[][] grd = new int[3][2];
    int color_length = crnr_color[0].length;

    switch (o_flag) {
    case 1:
      closed[0] = closed[0] | 14;
      if (crnr_out[1] || crnr_out[2] || crnr_out[3])
        return;
      cx1 = xx + xd;
      cy1 = yy;
      cx2 = xx + xd;
      cy2 = yy + yd;
      cx3 = xx;
      cy3 = yy + yd;
      cc = 3;
      grd[0][0] = 1;
      grd[0][1] = 0;
      grd[1][0] = 1;
      grd[1][1] = 1;
      grd[2][0] = 0;
      grd[2][1] = 1;
      break;
    case 2:
      closed[0] = closed[0] | 13;
      if (crnr_out[0] || crnr_out[2] || crnr_out[3])
        return;
      cx1 = xx;
      cy1 = yy;
      cx2 = xx;
      cy2 = yy + yd;
      cx3 = xx + xd;
      cy3 = yy + yd;
      cc = 2;
      grd[0][0] = 0;
      grd[0][1] = 0;
      grd[1][0] = 0;
      grd[1][1] = 1;
      grd[2][0] = 1;
      grd[2][1] = 1;
      break;
    case 4:
      closed[0] = closed[0] | 11;
      if (crnr_out[0] || crnr_out[1] || crnr_out[3])
        return;
      cx1 = xx;
      cy1 = yy;
      cx2 = xx + xd;
      cy2 = yy;
      cx3 = xx + xd;
      cy3 = yy + yd;
      cc = 1;
      grd[0][0] = 0;
      grd[0][1] = 0;
      grd[1][0] = 1;
      grd[1][1] = 0;
      grd[2][0] = 1;
      grd[2][1] = 1;
      break;
    case 7:
      closed[0] = closed[0] | 7;
      if (crnr_out[0] || crnr_out[1] || crnr_out[2])
        return;
      cx1 = xx + xd;
      cy1 = yy;
      cx2 = xx;
      cy2 = yy;
      cx3 = xx;
      cy3 = yy + yd;
      cc = 0;
      grd[0][0] = 1;
      grd[0][1] = 0;
      grd[1][0] = 0;
      grd[1][1] = 0;
      grd[2][0] = 0;
      grd[2][1] = 1;
      break;
    }

    int cnt_tri = cnt[0];
    int tt = t_idx[0];

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx1;
    tri[1][tt] = cy1;
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[0][1]][nr + grd[0][0]][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[0][1]][nr + grd[0][0]][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[0][1]][nr + grd[0][0]][2];
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx2;
    tri[1][tt] = cy2;
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][2];
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    if (dir > 0) {
      tri[0][tt] = vx[v_idx];
      tri[1][tt] = vy[v_idx];
    } else {
      tri[0][tt] = vx[v_idx + dir];
      tri[1][tt] = vy[v_idx + dir];
    }
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;
    cnt_tri++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx3;
    tri[1][tt] = cy3;
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[2][1]][nr + grd[2][0]][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[2][1]][nr + grd[2][0]][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[2][1]][nr + grd[2][0]][2];
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx2;
    tri[1][tt] = cy2;
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][2];
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    if (dir > 0) {
      tri[0][tt] = vx[v_idx + dir];
      tri[1][tt] = vy[v_idx + dir];
    } else {
      tri[0][tt] = vx[v_idx];
      tri[1][tt] = vy[v_idx];
    }
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;
    cnt_tri++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx2;
    tri[1][tt] = cy2;
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + grd[1][1]][nr + grd[1][0]][2];
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = vx[v_idx];
    tri[1][tt] = vy[v_idx];
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = vx[v_idx + dir];
    tri[1][tt] = vy[v_idx + dir];
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;
    cnt_tri++;

    cnt[0] = cnt_tri;
    t_idx[0] = tt;

  }

  /**
   * 
   * 
   * @param xx
   * @param yy
   * @param xd
   * @param yd
   * @param v_idx
   * @param o_flag
   * @param flag
   * @param cnt
   * @param dir
   * @param vx
   * @param vy
   * @param nc
   * @param nr
   * @param crnr_color
   * @param crnr_out
   * @param tri
   * @param t_idx
   * @param tri_color
   * @param grd_normals
   * @param n_idx
   * @param tri_normals
   * @param closed
   */
  private static void fillToSide(float xx, float yy, float xd, float yd,
      int v_idx, byte o_flag, int flag, int[] cnt, int dir, float[] vx,
      float[] vy, int nc, int nr, byte[][] crnr_color, boolean[] crnr_out,
      float[][] tri, int[] t_idx, byte[][] tri_color, float[][][] grd_normals,
      int[] n_idx, float[] tri_normals, int[] closed) {

    int cnt_tri = cnt[0];
    int tt = t_idx[0];
    float cx1 = 0;
    float cy1 = 0;
    float cx2 = 0;
    float cy2 = 0;
    int cc = 0;
    int[][] grd = new int[2][2];
    int color_length = crnr_color[0].length;

    switch (o_flag) {
    case 3:
      switch (flag) {
      case 1:
        closed[0] = closed[0] | 12;
        if (crnr_out[2] || crnr_out[3])
          return;
        cx1 = xx;
        cy1 = yy + yd;
        cx2 = xx + xd;
        cy2 = yy + yd;
        cc = 3;
        grd[0][0] = 0;
        grd[0][1] = 1;
        grd[1][0] = 1;
        grd[1][1] = 1;
        break;
      case -1:
        closed[0] = closed[0] | 3;
        if (crnr_out[0] || crnr_out[1])
          return;
        cx1 = xx;
        cy1 = yy;
        cx2 = xx + xd;
        cy2 = yy;
        cc = 0;
        grd[0][0] = 0;
        grd[0][1] = 0;
        grd[1][0] = 1;
        grd[1][1] = 0;
        break;
      }
      break;

    case 5:
      switch (flag) {
      case 1:
        closed[0] = closed[0] | 5;
        if (crnr_out[0] || crnr_out[2])
          return;
        cx1 = xx;
        cy1 = yy;
        cx2 = xx;
        cy2 = yy + yd;
        cc = 0;
        grd[0][0] = 0;
        grd[0][1] = 0;
        grd[1][0] = 0;
        grd[1][1] = 1;
        break;
      case -1:
        closed[0] = closed[0] | 10;
        if (crnr_out[1] || crnr_out[3])
          return;
        cx1 = xx + xd;
        cy1 = yy;
        cx2 = xx + xd;
        cy2 = yy + yd;
        grd[0][0] = 1;
        grd[0][1] = 0;
        grd[1][0] = 1;
        grd[1][1] = 1;
        cc = 3;
        break;
      }
      break;

    }

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx1;
    tri[1][tt] = cy1;
    int i = grd[0][0];
    int j = grd[0][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][2];
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = vx[v_idx];
    tri[1][tt] = vy[v_idx];
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = vx[v_idx + dir];
    tri[1][tt] = vy[v_idx + dir];
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;
    cnt_tri++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx1;
    tri[1][tt] = cy1;
    i = grd[0][0];
    j = grd[0][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][2];
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    if (dir > 0) {
      tri[0][tt] = vx[v_idx + dir];
      tri[1][tt] = vy[v_idx + dir];
    } else {
      tri[0][tt] = vx[v_idx];
      tri[1][tt] = vy[v_idx];
    }
    t_idx[0] = tt;
    interpNormals(tri[0][tt], tri[1][tt], xx, yy, nc, nr, xd, yd, grd_normals,
        n_idx, tri_normals);
    tt++;

    for (int ii = 0; ii < color_length; ii++) {
      tri_color[ii][tt] = crnr_color[cc][ii];
    }
    tri[0][tt] = cx2;
    tri[1][tt] = cy2;
    i = grd[1][0];
    j = grd[1][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][0];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][1];
    tri_normals[n_idx[0]++] = grd_normals[nc + j][nr + i][2];
    tt++;
    cnt_tri++;

    cnt[0] = cnt_tri;
    t_idx[0] = tt;

  }

  static final class ContourOutput {

    final float[] linesXCoords;
    final float[] linesYCoords;
    final float[] linesZCoords;
    final byte[][] linesColors;

    final float[] fillXCoords;
    final float[] fillYCoords;
    final float[] fillZCoords;
    final byte[][] fillColors;

    final float[] labelXCoords;
    final float[] labelYCoords;
    final float[] labelZCoords;
    final byte[][] labelColors;

    final float[] expLineXCoords;
    final float[] expLineYCoords;
    final float[] expLineZCoords;

    final float[][] triangleCoords;
    final byte[][] triangleColors;
    final float[][] triangleNormals;

    final float[][][] labelLocations;
    final float[][][][] labelVV;
    final byte[][][][] labelCC;

    private final ContourStripSet stripSet;

    ContourOutput(float[] linesX, float[] linesY, float[] linesZ,
        byte[][] linesClr, float[] fillX, float[] fillY, float[] fillZ,
        byte[][] fillClr, float[] lblX, float[] lblY, float[] lblZ,
        byte[][] lblClr, float[] expX, float[] expY, float[] expZ,
        float[][] tri, byte[][] triClr, float[][] triNorm, float[][][] lblLoc,
        float[][][][] lblVV, byte[][][][] lblCC, ContourStripSet set) {
      linesXCoords = linesX;
      linesYCoords = linesY;
      linesZCoords = linesZ;
      linesColors = linesClr;
      fillXCoords = fillX;
      fillYCoords = fillY;
      fillZCoords = fillZ;
      fillColors = fillClr;
      labelXCoords = lblX;
      labelYCoords = lblY;
      labelZCoords = lblZ;
      labelColors = lblClr;
      expLineXCoords = expX;
      expLineYCoords = expY;
      expLineZCoords = expZ;
      triangleCoords = tri;
      triangleColors = triClr;
      triangleNormals = triNorm;
      labelLocations = lblLoc;
      labelVV = lblVV;
      labelCC = lblCC;

      stripSet = set;
    }

    boolean isLineStyled(int lvl) {
      return stripSet.isLevelStyled(lvl);
    }
    
    boolean isLabeled(int lvl) {
      return stripSet.isLabeled(lvl);
    }

    List<float[][][]> getLineStripCoordinates(int lvl) {
      return stripSet.getLineStripCoordinates(lvl);
    }

    List<byte[][][]> getLineStripColors(int lvl) {
      return stripSet.getLineStripColors(lvl);
    }

    int getIntervalCount() {
      return stripSet.vecArray.length;
    }

    Vector<ContourStrip> getStrips(int lvl) {
      return stripSet.vecArray[lvl];
    }
    
    int[] getLabelIndexes(int lvlIdx) {
      return stripSet.labelIndexes[lvlIdx];
    }
    
    float[] getLevels() {
      return stripSet.levels;
    }
  }
} // end class

/**
 * Class ContourQuadSet
 * 
 */

class ContourQuadSet {

  /**           */
  int nx = 1;

  /**           */
  int ny = 1;

  /**           */
  int npx;

  /**           */
  int npy;

  /**           */
  int nc;

  /**           */
  int nr;

  /**           */
  int lev_idx;

  /**           */
  int numv = 0;

  /**           */
  ContourStripSet css = null;

  /**           */
  ContourQuad[][] qarray = null;

  /**           */
  int snumv = 0;

  /**           */
  public Map<CachedArrayDimension, CachedArray> subGridMap = new HashMap<CachedArrayDimension, CachedArray>();

  /**           */
  public Map<CachedArrayDimension, CachedArray> subGrid2Map = new HashMap<CachedArrayDimension, CachedArray>();

  /**           */
  public Map<CachedArrayDimension, CachedArray> markGridMap = new HashMap<CachedArrayDimension, CachedArray>();

  /**           */
  public Map<CachedArrayDimension, CachedArray> markGrid2Map = new HashMap<CachedArrayDimension, CachedArray>();

  /**
   * 
   * 
   * @param nr
   * @param nc
   * @param lev_idx
   * @param css
   */
  ContourQuadSet(int nr, int nc, int lev_idx, ContourStripSet css) {
    this.nc = nc;
    this.nr = nr;
    this.lev_idx = lev_idx;
    this.css = css;

    if (css.contourDifficulty == Contour2D.HARD && nr >= 20 && nc >= 20) {
      nx = 20;
      ny = 20;
    } else {
      nx = 1;
      ny = 1;
    }

    npy = (int) (nr / ny);
    npx = (int) (nc / nx);

    qarray = new ContourQuad[ny][nx];
    // JDM: Only make the ContourQuad objects when we need them
    /*
     * for (int j=0; j<ny; j++) { for (int i=0; i<nx; i++) { qarray[j][i] =
     * makeContourQuad(j,i); } }
     */
  }

  /**
   * 
   * 
   * @param j
   * @param i
   * 
   * @return
   */
  private ContourQuad makeContourQuad(int j, int i) {
    int lenx = npx;
    int leny = npy;
    if (j == ny - 1)
      leny = nr - (ny - 1) * npy;
    if (i == nx - 1)
      lenx = nc - (nx - 1) * npx;
    return new ContourQuad(this, j * npy, i * npx, leny, lenx);
  }

  /**
   * 
   * 
   * @param idx0
   * @param ir
   * @param ic
   */
  public void add(int idx0, int ir, int ic) {
    int ix = (int) (ic / npx);
    int iy = (int) (ir / npy);
    if (ix >= nx)
      ix = nx - 1;
    if (iy >= ny)
      iy = ny - 1;
    if (qarray[iy][ix] == null) {
      qarray[iy][ix] = makeContourQuad(iy, ix);
    }
    qarray[iy][ix].add(idx0, ir, ic);
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   */
  public void get(float[] vx, float[] vy) {
    numv = 0;
    snumv = 0;
    for (int j = 0; j < ny; j++) {
      for (int i = 0; i < nx; i++) {
        if (qarray[j][i] == null)
          continue;
        ContourStrip[] c_strps = qarray[j][i].getContourStrips(vx, vy);
        numv += qarray[j][i].numv;
        snumv += qarray[j][i].stripCnt;
        if (c_strps != null) {
          css.vecArray[lev_idx].add(c_strps[0]);
        }
      }
    }
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param auxLevels
   * @param vx1
   * @param vy1
   * @param vz1
   * @param colors
   * @param spatial_set
   * 
   * @throws VisADException
   */
  public void getArrays(float[] vx, float[] vy, byte[][] auxLevels,
      float[][] vx1, float[][] vy1, float[][] vz1, byte[][] colors,
      Gridded3DSet spatial_set) throws VisADException {

    float[][] arrays = new float[2][2 * numv];
    int clr_dim = 3;
    if (auxLevels != null) {
      clr_dim = auxLevels.length;
      colors[0] = new byte[2 * numv];
      colors[1] = new byte[2 * numv];
      colors[2] = new byte[2 * numv];
      colors[3] = new byte[2 * numv];
    }

    int cnt = 0;
    for (int j = 0; j < ny; j++) {
      for (int i = 0; i < nx; i++) {
        if (qarray[j][i] == null)
          continue;
        for (int k = 0; k < qarray[j][i].numv; k++) {
          int vidx = qarray[j][i].vert_indices[k];
          if (vidx >= 0) {
            arrays[0][cnt] = vx[vidx];
            arrays[1][cnt] = vy[vidx];
            if (auxLevels != null) {
              colors[0][cnt] = auxLevels[0][vidx];
              colors[1][cnt] = auxLevels[1][vidx];
              colors[2][cnt] = auxLevels[2][vidx];
              if (clr_dim == 4)
                colors[3][cnt] = auxLevels[3][vidx];
            }
            cnt++;
            arrays[0][cnt] = vx[vidx + 1];
            arrays[1][cnt] = vy[vidx + 1];
            if (auxLevels != null) {
              colors[0][cnt] = auxLevels[0][vidx + 1];
              colors[1][cnt] = auxLevels[1][vidx + 1];
              colors[2][cnt] = auxLevels[2][vidx + 1];
              if (clr_dim == 4)
                colors[3][cnt] = auxLevels[3][vidx];
            }
            cnt++;
          }
        }
      }
    }

    float[][] tmp = new float[2][cnt];
    System.arraycopy(arrays[0], 0, tmp[0], 0, cnt);
    System.arraycopy(arrays[1], 0, tmp[1], 0, cnt);

    float[][] tmp3D = spatial_set.gridToValue(tmp);
    vx1[0] = tmp3D[0];
    vy1[0] = tmp3D[1];
    vz1[0] = tmp3D[2];
    arrays = null;
    colors = null;
  }
}

/**
 * Class ContourQuad
 * 
 */

class ContourQuad {

  /**           */
  int[] vert_indices;

  /**           */
  int[] vert_indices_save = null;

  /**           */
  int[] grid_indices;

  /**           */
  int maxnumv;

  /**           */
  int numv;

  /**           */
  ContourQuadSet qs;

  /**           */
  int nc;

  /**           */
  int nr;

  /**           */
  int strty;

  /**           */
  int strtx;

  /**           */
  int leny;

  /**           */
  int lenx;

  /**           */
  int lev_idx;

  /**           */
  int[][] sub_grid = null;

  /**           */
  int[][] sub_grid_2 = null;

  /**           */
  int[][] mark_grid = null;

  /**           */
  int[][] mark_grid_2 = null;

  /**           */
  ContourStripSet css = null;

  /**           */
  int[] stripVert_indices;

  /**           */
  int stripCnt = 0;

  /**
   * 
   * 
   * @param qs
   * @param strty
   * @param strtx
   * @param leny
   * @param lenx
   */
  ContourQuad(ContourQuadSet qs, int strty, int strtx, int leny, int lenx) {
    maxnumv = 100;
    numv = 0;
    vert_indices = new int[maxnumv]; // - indices into vx,vy
    grid_indices = new int[maxnumv]; // - location on the grid
    this.qs = qs;
    this.nc = qs.nc;
    this.nr = qs.nr;
    this.strty = strty;
    this.strtx = strtx;
    this.leny = leny;
    this.lenx = lenx;
    css = qs.css;
    lev_idx = qs.lev_idx;
  }

  /**
   * 
   * 
   * @param idx0
   * @param gy
   * @param gx
   */
  public void add(int idx0, int gy, int gx) {
    if (numv < maxnumv - 2) {
      vert_indices[numv] = idx0;
      grid_indices[numv] = gy * nc + gx;
      numv++;
    } else {
      maxnumv += 50;
      int[] tmpA = vert_indices;
      int[] tmpB = grid_indices;
      vert_indices = new int[maxnumv];
      grid_indices = new int[maxnumv];
      System.arraycopy(tmpA, 0, vert_indices, 0, numv);
      System.arraycopy(tmpB, 0, grid_indices, 0, numv);
      tmpA = null;
      tmpB = null;
      vert_indices[numv] = idx0;
      grid_indices[numv] = gy * nc + gx;
      numv++;
    }
  }

  /**
   * 
   * 
   * @param leny
   * @param lenx
   * 
   * @return
   */
  public int[][][] getWorkArrays(int leny, int lenx) {
    Object key;

    java.util.Set<CachedArrayDimension> keySet = qs.subGridMap.keySet();

    key = null;
    for (CachedArrayDimension obj : keySet) {
      if (obj.equals(new CachedArrayDimension(leny, lenx))) {
        key = obj;
        break;
      }
    }

    int[][] subgrid = null;
    int[][] subgrid2 = null;
    int[][] markgrid = null;
    int[][] markgrid2 = null;

    if (key != null) {
      subgrid = ((CachedArray) qs.subGridMap.get(key)).getArray();
      subgrid2 = ((CachedArray) qs.subGrid2Map.get(key)).getArray();
      markgrid = ((CachedArray) qs.markGridMap.get(key)).getArray();
      markgrid2 = ((CachedArray) qs.markGrid2Map.get(key)).getArray();
    } else {
      subgrid = new int[leny][lenx];
      subgrid2 = new int[leny][lenx];
      markgrid = new int[leny][lenx];
      markgrid2 = new int[leny][lenx];
      CachedArrayDimension newKey = new CachedArrayDimension(leny, lenx);
      qs.subGridMap.put(newKey, new CachedArray(subgrid));
      qs.subGrid2Map.put(newKey, new CachedArray(subgrid2));
      qs.markGridMap.put(newKey, new CachedArray(markgrid));
      qs.markGrid2Map.put(newKey, new CachedArray(markgrid2));
    }
    return new int[][][] { subgrid, subgrid2, markgrid, markgrid2 };
  }

  /**
   * 
   */
  public void get() {
    int ix_i = -1;
    int iy_i = -1;
    int[][][] workarrays = getWorkArrays(leny, lenx);
    sub_grid = workarrays[0];
    sub_grid_2 = workarrays[1];
    mark_grid = workarrays[2];
    mark_grid_2 = workarrays[3];

    for (int j = 0; j < leny; j++) {
      for (int i = 0; i < lenx; i++) {
        sub_grid[j][i] = 0;
        sub_grid_2[j][i] = 0;
      }
    }

    if (vert_indices_save == null) {
      vert_indices_save = new int[vert_indices.length];
      System.arraycopy(vert_indices, 0, vert_indices_save, 0,
          vert_indices.length);
    } else {
      System.arraycopy(vert_indices_save, 0, vert_indices, 0,
          vert_indices.length);
    }

    for (int ii = 0; ii < numv; ii++) {
      int kk = grid_indices[ii];
      int iy = (int) kk / nc;
      int ix = kk - iy * nc;
      sub_grid[iy - strty][ix - strtx] = vert_indices[ii];
      mark_grid[iy - strty][ix - strtx] = ii;
      if (ix_i == ix && iy_i == iy) {
        sub_grid_2[iy - strty][ix - strtx] = vert_indices[ii];
        mark_grid_2[iy - strty][ix - strtx] = ii;
      }
      ix_i = ix;
      iy_i = iy;
    }
  }

  /**
   * 
   */
  public void reset() {
    for (int j = 0; j < leny; j++) {
      for (int i = 0; i < lenx; i++) {
        if (sub_grid[j][i] < 0) {
          sub_grid[j][i] *= -1;
        }
      }
    }
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   * 
   * @return
   */
  public ContourStrip[] getContourStrips(float[] vx, float[] vy) {

    get();
    stripVert_indices = new int[200];
    int n_segs = 0;
    int[][] udrl = { { 1, -1, 0, 0 }, { 0, 0, 1, -1 } }; // -up/down, right/left

    // - find starting point
    int[] start = getStartPoint();
    if (start == null) {
      return null;
    }
    int iy = start[0];
    int ix = start[1];

    int idx0 = sub_grid[iy][ix];
    int idx1 = idx0 + 1;

    ContourStrip c_strp = new ContourStrip(200, lev_idx, idx0, idx1,
        css.plot_s[lev_idx], css);

    int idxA = idx0;
    int idxB = idx0;
    int idxA_2;
    int idxB_2;

    int ix_t, iy_t;
    int ix_a = ix;
    int iy_a = iy;
    int ix_b = ix;
    int iy_b = iy;

    int cnt = 0;
    stripVert_indices[cnt++] = idx0;
    sub_grid[iy][ix] *= -1;

    int test_cnt = 0;
    while ((n_segs < 100) && (test_cnt < 300)) {
      test_cnt++;

      // - A
      for (int k = 0; k < 4; k++) {
        ix_t = ix_a + udrl[0][k];
        iy_t = iy_a + udrl[1][k];
        if ((iy_t >= 0 && iy_t < leny) && (ix_t >= 0 && ix_t < lenx)) {

          idxA = sub_grid[iy_t][ix_t];
          idxA_2 = sub_grid_2[iy_t][ix_t];

          if (idxA > 0) {
            if (c_strp.addPair(vx, vy, idxA, idxA + 1)) {
              sub_grid[iy_t][ix_t] *= -1;
              stripVert_indices[cnt++] = idxA;
              ix_a = ix_t;
              iy_a = iy_t;
              vert_indices[mark_grid[iy_t][ix_t]] = -1;
              n_segs++;
              break;
            }
          }
          if (idxA_2 > 0) {
            if (c_strp.addPair(vx, vy, idxA_2, idxA_2 + 1)) {
              sub_grid_2[iy_t][ix_t] *= -1;
              stripVert_indices[cnt++] = idxA_2;
              ix_a = ix_t;
              iy_a = iy_t;
              vert_indices[mark_grid_2[iy_t][ix_t]] = -1;
              n_segs++;
              break;
            }
          }
        }
      }

      // - B
      for (int k = 0; k < 4; k++) {
        ix_t = ix_b + udrl[0][k];
        iy_t = iy_b + udrl[1][k];
        if ((iy_t >= 0 && iy_t < leny) && (ix_t >= 0 && ix_t < lenx)) {

          idxB = sub_grid[iy_t][ix_t];
          idxB_2 = sub_grid_2[iy_t][ix_t];

          if (idxB > 0) {
            if (c_strp.addPair(vx, vy, idxB, idxB + 1)) {
              sub_grid[iy_t][ix_t] *= -1;
              stripVert_indices[cnt++] = idxB;
              ix_b = ix_t;
              iy_b = iy_t;
              vert_indices[mark_grid[iy_t][ix_t]] = -1;
              n_segs++;
              break;
            }
          }
          if (idxB_2 > 0) {
            if (c_strp.addPair(vx, vy, idxB_2, idxB_2 + 1)) {
              sub_grid_2[iy_t][ix_t] *= -1;
              stripVert_indices[cnt++] = idxB_2;
              ix_b = ix_t;
              iy_b = iy_t;
              vert_indices[mark_grid_2[iy_t][ix_t]] = -1;
              n_segs++;
              break;
            }
          }
        }
      }
    }
    stripCnt = cnt;

    sub_grid = null;
    sub_grid_2 = null;
    return new ContourStrip[] { c_strp };

  }

  /**
   * 
   * 
   * @return
   */
  public int[] getStartPoint() {
    int n_trys = 20;
    float nn = (float) lenx * leny;
    java.util.Random rnd = new java.util.Random();

    for (int tt = 0; tt < n_trys; tt++) {
      int kk = (int) (nn * rnd.nextFloat());
      int j = (int) kk / lenx;
      int i = kk - j * lenx;
      if (sub_grid[j][i] != 0) {
        return new int[] { j, i };
      }
    }
    return null;
  }
}

/**
 * Class CachedArray
 * 
 */

class CachedArray {

  /**           */
  int[][] array;

  /**
   * 
   * 
   * @param array
   */
  public CachedArray(int[][] array) {
    this.array = array;
  }

  /**
   * 
   * 
   * @return
   */
  int[][] getArray() {
    return array;
  }
}

/**
 * Class CachedArrayDimension
 * 
 */

class CachedArrayDimension {

  /**           */
  int lenx;

  /**           */
  int leny;

  /**
   * 
   * 
   * @param leny
   * @param lenx
   */
  CachedArrayDimension(int leny, int lenx) {
    this.leny = leny;
    this.lenx = lenx;
  }

  /**
   * 
   * 
   * @param obj
   * 
   * @return
   */
  public boolean equals(CachedArrayDimension obj) {
    return (lenx == obj.lenx && leny == obj.leny);
  }
}

/**
 * ContourStripSet is used internally by Contour2D
 */

class ContourStripSet {

  // value for dash algm.

  /**           */
  static final int DEFAULT_DASH_VALUE = 2;

  /**           */
  static final int DISABLE_DASH_VALUE = -1;

  /**           */
  int mxsize;

  /**           */
  float[] levels;

  int[][] labelIndexes;
  
  /**           */
  int n_levs;

  /**           */
  int nr;

  /**           */
  int nc;

  /**           */
  Gridded3DSet spatial_set;

  /** Contour strips by level. */
  Vector<ContourStrip>[] vecArray;

  /**           */
  Vector<ContourStrip> vec;

  /**           */
  PlotDigits[] plot_s;

  /**           */
  float[][] plot_min_max;

  /**           */
  boolean[] swap;

  /**           */
  ContourQuadSet[] qSet;

  /**           */
  int contourDifficulty = Contour2D.EASY;

  /** Grid X coordinates. */
  private float[] gridX;
  /** Grid Y coordinates. */
  private float[] gridY;
  /** Colors corresponding to grid values. */
  private byte[][] gridColors;

  /**
   * 
   * 
   * @param size
   * @param levels
   * @param swap
   * @param scale_ratio
   * @param label_size
   * @param nr
   * @param nc
   * @param spatial_set
   * @param contourDifficulty
   * 
   * @throws VisADException
   */
  ContourStripSet(int size, float[] levels, boolean[] swap, double scale_ratio,
      double label_size, int nr, int nc, Gridded3DSet spatial_set,
      int contourDifficulty) throws VisADException {

    this.mxsize = 40 * size;
    this.levels = levels;
    n_levs = levels.length;
    labelIndexes = new int[n_levs][];
    vecArray = new Vector[n_levs];
    plot_s = new PlotDigits[n_levs];
    plot_min_max = new float[n_levs][2];
    float fac = (float) ((0.15 * (1.0 / scale_ratio)) * label_size);
    this.nr = nr;
    this.nc = nc;
    this.swap = swap;
    this.spatial_set = spatial_set;
    this.contourDifficulty = contourDifficulty;

    for (int kk = 0; kk < n_levs; kk++) {
      vecArray[kk] = new Vector<ContourStrip>();
      PlotDigits plot = new PlotDigits();
      plot.Number = levels[kk];
      plot.plotdigits(levels[kk], 0f, 0f, fac * 1, fac * 1, 400, new boolean[] {
          false, false, false });

      float[][] tmp = new float[2][];
      tmp[0] = plot.Vx;
      tmp[1] = plot.Vy;
      plot.Vx = tmp[1];
      plot.Vy = tmp[0];
      tmp[0] = plot.VxB;
      tmp[1] = plot.VyB;
      plot.VxB = tmp[1];
      plot.VyB = tmp[0];

      float vx_min = Float.MAX_VALUE;
      float vy_min = Float.MAX_VALUE;
      float vx_max = -Float.MAX_VALUE;
      float vy_max = -Float.MAX_VALUE;
      float vxB_min = Float.MAX_VALUE;
      float vyB_min = Float.MAX_VALUE;
      float vxB_max = -Float.MAX_VALUE;
      float vyB_max = -Float.MAX_VALUE;
      for (int ii = 0; ii < plot.NumVerts; ii++) {
        if (plot.Vx[ii] < vx_min)
          vx_min = plot.Vx[ii];
        if (plot.Vy[ii] < vy_min)
          vy_min = plot.Vy[ii];
        if (plot.Vx[ii] > vx_max)
          vx_max = plot.Vx[ii];
        if (plot.Vy[ii] > vy_max)
          vy_max = plot.Vy[ii];
        if (plot.VxB[ii] < vxB_min)
          vxB_min = plot.VxB[ii];
        if (plot.VyB[ii] < vyB_min)
          vyB_min = plot.VyB[ii];
        if (plot.VxB[ii] > vxB_max)
          vxB_max = plot.VxB[ii];
        if (plot.VyB[ii] > vyB_max)
          vyB_max = plot.VyB[ii];
      }
      float t_x = (vx_max - vx_min) / 2 + vx_min;
      float t_y = (vy_max - vy_min) / 2 + vy_min;
      float t_xB = (vxB_max - vxB_min) / 2 + vxB_min;
      float t_yB = (vyB_max - vyB_min) / 2 + vyB_min;

      for (int ii = 0; ii < plot.NumVerts; ii++) {
        plot.Vx[ii] -= t_x;
        plot.Vy[ii] -= t_y;
        plot.VxB[ii] -= t_xB;
        plot.VyB[ii] -= t_yB;
      }
      plot_s[kk] = plot;
      if (swap[0] == false) {
        plot_min_max[kk][0] = vy_min;
        plot_min_max[kk][1] = vy_max;
      } else {
        plot_min_max[kk][0] = vx_min;
        plot_min_max[kk][1] = vx_max;
      }
      plot_min_max[kk][0] = vx_min;
      plot_min_max[kk][1] = vx_max;
    }

    qSet = new ContourQuadSet[n_levs];
    for (int kk = 0; kk < n_levs; kk++) {
      qSet[kk] = new ContourQuadSet(nr, nc, kk, this);
    }
  }

  /**
   * Set the grid coordinates used to contruct <code>ContourStrip</code>s
   * contained in this set.
   * 
   * @param gx
   * @param gy
   */
  void setGridValues(float[] gx, float[] gy) {
    gridX = gx;
    gridY = gy;
  }

  void setGridColors(byte[][] colors) {
    gridColors = colors;
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param idx0
   * @param idx1
   * @param lev_idx
   * @param ir
   * @param ic
   */
  void add(float[] vx, float[] vy, int idx0, int idx1, int lev_idx, int ir,
      int ic) {
    qSet[lev_idx].add(idx0, ir, ic);
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param idx0
   * @param idx1
   * @param level
   */
  void add(float[] vx, float[] vy, int idx0, int idx1, float level) {
    int lev_idx = 0;
    for (int kk = 0; kk < n_levs; kk++) {
      if (level == levels[kk])
        lev_idx = kk;
    }
    add(vx, vy, idx0, idx1, lev_idx);
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param idx0
   * @param idx1
   * @param lev_idx
   */
  void add(float[] vx, float[] vy, int idx0, int idx1, int lev_idx) {
    vec = vecArray[lev_idx];
    int n_strip = vec.size();

    if (n_strip == 0) {
      ContourStrip c_strp = new ContourStrip(mxsize, lev_idx, idx0, idx1,
          plot_s[lev_idx], this);
      vec.add(c_strp);
    } else {
      int[] found_array = new int[3];
      int found = 0;
      for (int kk = 0; kk < n_strip; kk++) {
        ContourStrip c_strp = vec.get(kk);
        if (c_strp.addPair(vx, vy, idx0, idx1)) {
          found_array[found] = kk;
          found++;
        }
      }
      if (found == 3) {
        ContourStrip c_strp = new ContourStrip(mxsize, lev_idx, idx0, idx1,
            plot_s[lev_idx], this);
        vec.add(c_strp);
      } else if (found == 2) {
        ContourStrip c_strpA = vec.get(found_array[0]);
        ContourStrip c_strpB = vec.get(found_array[1]);
        ContourStrip c_strp = c_strpA.merge(c_strpB);

        vec.add(c_strp);
        vec.remove(c_strpA);
        vec.remove(c_strpB);
      } else if (found == 0) {
        ContourStrip c_strp = new ContourStrip(mxsize, lev_idx, idx0, idx1,
            plot_s[lev_idx], this);
        vec.add(c_strp);
      }
    }
  }

  /**
   * 
   * @param vx
   *          Grid coordinate values.
   * @param vy
   *          Grid coordinate values.
   * @param colors
   *          Colors for grid coordinate values.
   * @param labelColor
   *          Color for labels if filling.
   * @param lev_idx
   *          Index of the level to process.
   * @param out_vv
   *          Output line display coords for basic lines.
   * @param out_bb
   *          Output colors for basic lines.
   * @param out_vvL
   *          Output line display coords for labels.
   * @param out_bbL
   *          Output colors for label lines.
   * @param out_loc
   *          Output location coords for labels.
   * @param dashed
   *          Flags indicating which levels to dash.
   */
  void getLineColorArrays(float[] vx, float[] vy, byte[][] colors,
      byte[] labelColor, int lev_idx, float[][][] out_vv, byte[][][] out_bb,
      float[][][][] out_vvL, byte[][][][] out_bbL, float[][][] out_loc,
      boolean[] dashed) {

    int n_strips = vecArray[lev_idx].size();

    float[][][][] la = new float[n_strips][2][][]; // line arrays
    byte[][][][] ca = new byte[n_strips][2][][]; // color arrays
    float[][][][][] laL = new float[n_strips][4][][][]; // line arrays for
                                                        // labels
    byte[][][][][] caL = new byte[n_strips][4][][][]; // color arrays for labels
    float[][][][] locL = new float[n_strips][3][][]; // location arrays for
                                                     // labels

    // populate output arrays by strip
    for (int kk = 0; kk < n_strips; kk++) {
      ContourStrip cs = vecArray[lev_idx].get(kk);
      cs.isDashed = dashed[lev_idx];
      cs.getLabeledLineColorArray(vx, vy, colors, labelColor, la[kk], ca[kk],
          laL[kk], caL[kk], locL[kk]);
    }

    // -- contour/contour label gap line arrays
    for (int tt = 0; tt < 2; tt++) {
      int len = 0;
      for (int mm = 0; mm < n_strips; mm++) {
        if (la[mm][tt] != null) {
          len += la[mm][tt][0].length;
        }
      }
      out_vv[tt] = new float[3][len];
      int cnt = 0;
      for (int mm = 0; mm < n_strips; mm++) {
        if (la[mm][tt] != null) {
          System.arraycopy(la[mm][tt][0], 0, out_vv[tt][0], cnt,
              la[mm][tt][0].length);
          System.arraycopy(la[mm][tt][1], 0, out_vv[tt][1], cnt,
              la[mm][tt][1].length);
          System.arraycopy(la[mm][tt][2], 0, out_vv[tt][2], cnt,
              la[mm][tt][1].length);
          cnt += la[mm][tt][0].length;
        }
      }

      int clr_dim = 0;
      if (colors != null) {
        clr_dim = colors.length;
        len = 0;
        for (int mm = 0; mm < n_strips; mm++) {
          if (ca[mm][tt] != null) {
            len += ca[mm][tt][0].length;
          }
        }
        out_bb[tt] = new byte[clr_dim][len];
        cnt = 0;
        for (int mm = 0; mm < n_strips; mm++) {
          if (ca[mm][tt] != null) {
            for (int cc = 0; cc < clr_dim; cc++) {
              System.arraycopy(ca[mm][tt][cc], 0, out_bb[tt][cc], cnt,
                  ca[mm][tt][cc].length);
            }
            cnt += ca[mm][tt][0].length;
          }
        }
      }
    }

    // -- label, vx3/vx4, line arrays
    int n_lbl = 0; // total number of labels for this level
    for (int mm = 0; mm < n_strips; mm++) {
      if (laL[mm][0] != null) {
        n_lbl += laL[mm][0].length;
      }
    }
    out_vvL[0] = new float[n_lbl][][];
    out_vvL[1] = new float[n_lbl][][];
    out_vvL[2] = new float[n_lbl][][];
    out_vvL[3] = new float[n_lbl][][];
    out_bbL[0] = new byte[n_lbl][][];
    out_bbL[1] = new byte[n_lbl][][];
    out_bbL[2] = new byte[n_lbl][][];
    out_bbL[3] = new byte[n_lbl][][];
    out_loc[0] = new float[n_lbl][];
    out_loc[1] = new float[n_lbl][];
    out_loc[2] = new float[n_lbl][];

    // fill label value and color arrays 
    for (int tt = 0; tt < 4; tt++) { // left, left loc, right, right loc
      n_lbl = 0;
      for (int kk = 0; kk < n_strips; kk++) {
        if (laL[kk][tt] != null) { // we have location for a label
          for (int mm = 0; mm < laL[kk][tt].length; mm++) {
            out_vvL[tt][n_lbl] = laL[kk][tt][mm];
            if (caL[kk][tt] != null) {
              out_bbL[tt][n_lbl] = caL[kk][tt][mm];
            }
            vecArray[lev_idx].get(kk).numLabels++;
            n_lbl++;
          }
        }
      }
    }
    
    // fill label location arrays
    for (int tt = 0; tt < 3; tt++) {
      n_lbl = 0;
      for (int kk = 0; kk < n_strips; kk++) {
        if (locL[kk][0] != null) {
          for (int mm = 0; mm < locL[kk][tt].length; mm++) {
            out_loc[tt][n_lbl] = locL[kk][tt][mm];
            n_lbl++;
          }
        }
      }
    }

  }

  /**
   * @param vx
   * @param vy
   * @param colors
   *          shared colors
   * @param labelColor
   *          RGB label color byte array
   * @param out_vv
   *          output vector verticie array {{ X }, { Y }}
   * @param out_bb
   * @param out_vvL
   * @param out_bbL
   * @param out_loc
   * @param dashFlags
   * @param contourDifficulty
   */
  void getLineColorArrays(float[] vx, float[] vy, byte[][] colors,
      byte[] labelColor, float[][][] out_vv, byte[][][] out_bb,
      float[][][][] out_vvL, byte[][][][] out_bbL, float[][][] out_loc,
      boolean[] dashFlags, int contourDifficulty) {

    if (contourDifficulty == Contour2D.EASY) {
      makeContourStrips(vx, vy);
    } else {
      for (int kk = 0; kk < qSet.length; kk++) {
        qSet[kk].get(vx, vy);
      }
    }

    float[][][][] tmp = new float[n_levs][2][][];
    byte[][][][] btmp = new byte[n_levs][2][][];
    float[][][][][] tmpL = new float[n_levs][4][][][];
    byte[][][][][] btmpL = new byte[n_levs][4][][][];
    float[][][][] tmpLoc = new float[n_levs][3][][];

    int n_lbl = 0;

    // set the line and color arrays for each level
    for (int kk = 0; kk < n_levs; kk++) {
      getLineColorArrays(vx, vy, colors, labelColor, kk, tmp[kk], btmp[kk],
          tmpL[kk], btmpL[kk], tmpLoc[kk], dashFlags);
      
      
      // note the indexes to the labels for this level
      labelIndexes[kk] = new int[tmpL[kk][0].length];
      for (int ii = 0; ii < tmpL[kk][0].length; ii++) {
        labelIndexes[kk][ii] = n_lbl + ii;
      }
      
      n_lbl += tmpL[kk][0].length;
    }

    for (int tt = 0; tt < 2; tt++) {
      int len = 0;
      for (int kk = 0; kk < n_levs; kk++) {
        len += tmp[kk][tt][0].length;
      }
      out_vv[tt] = new float[3][len];
      int cnt = 0;
      for (int lvl = 0; lvl < n_levs; lvl++) {
        System.arraycopy(tmp[lvl][tt][0], 0, out_vv[tt][0], cnt,
            tmp[lvl][tt][0].length);
        System.arraycopy(tmp[lvl][tt][1], 0, out_vv[tt][1], cnt,
            tmp[lvl][tt][0].length);
        System.arraycopy(tmp[lvl][tt][2], 0, out_vv[tt][2], cnt,
            tmp[lvl][tt][0].length);
        cnt += tmp[lvl][tt][0].length;
      }
      int clr_dim = 0;
      if (colors != null) {
        clr_dim = colors.length;
        len = 0;
        for (int lvl = 0; lvl < n_levs; lvl++) {
          len += btmp[lvl][tt][0].length;
        }
        out_bb[tt] = new byte[clr_dim][len];
        cnt = 0;
        for (int lvl = 0; lvl < n_levs; lvl++) {
          for (int cc = 0; cc < clr_dim; cc++) {
            System.arraycopy(btmp[lvl][tt][cc], 0, out_bb[tt][cc], cnt,
                btmp[lvl][tt][cc].length);
          }
          cnt += btmp[lvl][tt][0].length;
        }
      }
    }
    btmp = null;

    for (int tt = 0; tt < 4; tt++) { // left lines, left locs, 
                                     // right lines, right locs
      out_vvL[tt] = new float[n_lbl][][];
      int cnt = 0;
      for (int lvl = 0; lvl < n_levs; lvl++) {
        for (int ll = 0; ll < tmpL[lvl][tt].length; ll++) {
          out_vvL[tt][cnt] = tmpL[lvl][tt][ll];
          cnt++;
        }
      }
      out_bbL[tt] = new byte[n_lbl][][];
      cnt = 0;
      for (int lvl = 0; lvl < n_levs; lvl++) {
        for (int ll = 0; ll < tmpL[lvl][tt].length; ll++) {
          out_bbL[tt][cnt] = btmpL[lvl][tt][ll];
          cnt++;
        }
      }
    }
    tmpL = null;
    btmpL = null;

    for (int tt = 0; tt < 3; tt++) { // x, y, z
      out_loc[tt] = new float[n_lbl][];
      int cnt = 0;
      for (int lvl = 0; lvl < n_levs; lvl++) {
        if (tmpLoc[lvl][tt] != null) {
          for (int ll = 0; ll < tmpLoc[lvl][tt].length; ll++) {
            out_loc[tt][cnt] = tmpLoc[lvl][tt][ll];
            cnt++;
          }
        }
      }
    }
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   */
  void makeContourStrips(float[] vx, float[] vy) {
    for (int kk = 0; kk < n_levs; kk++) {
      int nx = qSet[kk].nx;
      int ny = qSet[kk].ny;
      for (int j = 0; j < ny; j++) {
        for (int i = 0; i < nx; i++) {
          if (qSet[kk].qarray[j][i] == null)
            continue;
          int[] vert_indices = qSet[kk].qarray[j][i].vert_indices;
          int len = qSet[kk].qarray[j][i].numv;
          for (int q = 0; q < len; q++) {
            int idx = vert_indices[q];
            add(vx, vy, idx, idx + 1, kk);
          }
        }
      }
    }
  }

  /**
   * Get grid coordinates representing the data at the level specified.
   * 
   * @param lvlIdx
   *          The level for which to generate an array.
   * @return An list of in line strip format, an emtpy list if none.
   * @see {@link VisADLineStripArray}
   */
  List<float[][][]> getLineStripCoordinates(int lvlIdx) {
    if (lvlIdx > vecArray.length - 1) {
      return new ArrayList<float[][][]>(0);
    }
    Vector<ContourStrip> strips = vecArray[lvlIdx];
    List<float[][][]> stripValues = new ArrayList<float[][][]>();
    for (ContourStrip strip : strips) {
      stripValues.add(strip.getLineStripArrays(gridX, gridY));
    }
    return stripValues;
  }

  /**
   * Get colors corresponding to the grid coordinates for a level.
   * 
   * @param lvlIdx
   *          The level for which to get colors.
   * @return A list of arrays for the strips that make up the level, an empty
   *         list if none.
   */
  List<byte[][][]> getLineStripColors(int lvlIdx) {
    if (lvlIdx > vecArray.length - 1) {
      return new ArrayList<byte[][][]>(0);
    }
    Vector<ContourStrip> strips = vecArray[lvlIdx];
    List<byte[][][]> stripColors = new ArrayList<byte[][][]>();
    for (ContourStrip strip : strips) {;
      stripColors.add(strip.getColorStripArrays(gridColors));
    }
    return stripColors;
  }

  /**
   * Are we using line style for a level.
   * 
   * @param lvl
   *          The index of the the level.
   * @return True if the first strip is using line style, false otherwise. There
   *         is an assumption that if the first level is styled they all are.
   */
  boolean isLevelStyled(int lvl) {
    if (vecArray.length > lvl + 1 && vecArray[lvl] != null) {
      if (vecArray[lvl].size() > 0) {
        return vecArray[lvl].get(0).isDashed;
      }
    }
    return false;
  }
  
  boolean isLabeled(int lvl) {
    return vecArray[lvl].get(0).isLabeled();
  }
}

/**
 * ContourStrip is used internally by Contour2D to track the indexes associated
 * with a strip. Indexes are in line strip format and not line array format.
 */
class ContourStrip {

  /** Minimum number of points for which to perform label algm */
  static final int LBL_ALGM_THRESHHOLD = 20;

  /**
   * Intpereted arrays smaller than this will be interpreted again essentially
   * resulting in a re-doubleing of the number of points.
   * 
   * @deprecated J3D line styles are now used for dashing, so interrpretation is
   *             no longer necessary.
   */
  static final int INTERP_THRESHHOLD = 4;

  /**
   * Array of indexes to values in the grid coordinate arrays that make up this
   * strip.
   */
  int[] idx_array;

  /** Starting index in the strip data array. */
  int low_idx;

  /** Ending index in the strip data array. */
  int hi_idx;

  /** Index to the level for this strip in the intervals array. */
  int lev_idx;

  private boolean isLabeled = false;
  /** First index which starts the break for the label. */
  private int start_break;
  /** Last index which ends the break for the label. */
  private int stop_break;
  /** Number of indexes that make up the break for the label. */
  private int n_skip;

  /** Number of labels on this strip. */
  int numLabels; 
  
  boolean isDashed = false;

  /**           */
  PlotDigits plot;

  /**           */
  ContourStripSet css;

  /**           */
  float lbl_half;

  /**
   * 
   * 
   * @param mxsize
   * @param lev_idx
   * @param idx0
   * @param idx1
   * @param plot
   * @param css
   */
  ContourStrip(int mxsize, int lev_idx, int idx0, int idx1, PlotDigits plot,
      ContourStripSet css) {
    idx_array = new int[mxsize];
    this.lev_idx = lev_idx;
    this.plot = plot;

    low_idx = mxsize / 2;
    hi_idx = low_idx + 1;
    idx_array[low_idx] = idx0;
    idx_array[hi_idx] = idx1;
    this.css = css;
    this.lbl_half = (css.plot_min_max[lev_idx][1] - css.plot_min_max[lev_idx][0]) / 2;
    this.lbl_half += this.lbl_half * 0.30;
  }

  /**
   * 
   * 
   * @param idx_array
   * @param lev_idx
   * @param plot
   * @param css
   */
  ContourStrip(int[] idx_array, int lev_idx, PlotDigits plot,
      ContourStripSet css) {
    this.lev_idx = lev_idx;
    int mxsize = idx_array.length + 400;
    this.idx_array = new int[mxsize];
    this.plot = plot;
    low_idx = mxsize / 2 - (idx_array.length) / 2;
    hi_idx = (low_idx + idx_array.length) - 1;
    System.arraycopy(idx_array, 0, this.idx_array, low_idx, idx_array.length);
    this.css = css;
    this.lbl_half = (css.plot_min_max[lev_idx][1] - css.plot_min_max[lev_idx][0]) / 2;
    this.lbl_half += this.lbl_half * 0.30;
  }
  
  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param idx0
   * @param idx1
   * 
   * @return
   */
  boolean addPair(float[] vx, float[] vy, int idx0, int idx1) {

    float vx0 = vx[idx0];
    float vy0 = vy[idx0];
    float vx1 = vx[idx1];
    float vy1 = vy[idx1];

    float vx_s = vx[idx_array[low_idx]];
    float vy_s = vy[idx_array[low_idx]];
    float dist = (vx0 - vx_s) * (vx0 - vx_s) + (vy0 - vy_s) * (vy0 - vy_s);

    if (dist <= 0.00001) {
      if (low_idx < 2) {
        int[] tmp = new int[idx_array.length + 200];
        System.arraycopy(idx_array, 0, tmp, 100, idx_array.length);
        idx_array = tmp;
        tmp = null;
        low_idx += 100;
        hi_idx += 100;
      }
      low_idx -= 1;
      idx_array[low_idx] = idx0;
      low_idx -= 1;
      idx_array[low_idx] = idx1;
      return true;
    }
    dist = (vx1 - vx_s) * (vx1 - vx_s) + (vy1 - vy_s) * (vy1 - vy_s);
    if (dist <= 0.00001) {
      if (low_idx < 2) {
        int[] tmp = new int[idx_array.length + 200];
        System.arraycopy(idx_array, 0, tmp, 100, idx_array.length);
        idx_array = tmp;
        tmp = null;
        low_idx += 100;
        hi_idx += 100;
      }
      low_idx -= 1;
      idx_array[low_idx] = idx1;
      low_idx -= 1;
      idx_array[low_idx] = idx0;
      return true;
    }

    vx_s = vx[idx_array[hi_idx]];
    vy_s = vy[idx_array[hi_idx]];
    dist = (vx0 - vx_s) * (vx0 - vx_s) + (vy0 - vy_s) * (vy0 - vy_s);
    if (dist <= 0.00001) {
      if (hi_idx > idx_array.length - 2) {
        int[] tmp = new int[idx_array.length + 200];
        System.arraycopy(idx_array, 0, tmp, 100, idx_array.length);
        idx_array = tmp;
        tmp = null;
        low_idx += 100;
        hi_idx += 100;
      }
      hi_idx += 1;
      idx_array[hi_idx] = idx0;
      hi_idx += 1;
      idx_array[hi_idx] = idx1;
      return true;
    }
    dist = (vx1 - vx_s) * (vx1 - vx_s) + (vy1 - vy_s) * (vy1 - vy_s);
    if (dist <= 0.00001) {
      if (hi_idx > idx_array.length - 2) {
        int[] tmp = new int[idx_array.length + 200];
        System.arraycopy(idx_array, 0, tmp, 100, idx_array.length);
        idx_array = tmp;
        tmp = null;
        low_idx += 100;
        hi_idx += 100;
      }
      hi_idx += 1;
      idx_array[hi_idx] = idx1;
      hi_idx += 1;
      idx_array[hi_idx] = idx0;
      return true;
    }
    return false;
  }

  /**
   * 
   * 
   * @param vx
   * @param vy
   * @param colors
   * @param labelColor
   * @param out_vv
   * @param out_colors
   * @param out_vvL
   * @param out_colorsL
   * @param lbl_loc
   */
  void getLabeledLineColorArray(float[] vx, float[] vy, byte[][] colors,
      byte[] labelColor, float[][][] out_vv, byte[][][] out_colors,
      float[][][][] out_vvL, byte[][][][] out_colorsL, float[][][] lbl_loc) {

    float[][] vv = getLineArray(vx, vy);
    byte[][] bb = getColorArray(colors);

    processLineArrays(vv, bb, labelColor, out_vv, out_colors, out_vvL,
        out_colorsL, lbl_loc);
  }

  /**
   * Get an array of points where the number of points is doubled if the number
   * of points is below a treshold.
   * 
   * @param vx
   * @param vy
   * @param colors
   * @param labelColor
   * @param out_vv
   * @param out_colors
   * @param out_vvL
   * @param out_colorsL
   * @param lbl_loc
   * @deprecated J3D line styles are now used, so interrpretation is no longer
   *             necessary.
   */
  void getInterpolatedLabeledColorArray(float[] vx, float[] vy,
      byte[][] colors, byte[] labelColor, float[][][] out_vv,
      byte[][][] out_colors, float[][][][] out_vvL, byte[][][][] out_colorsL,
      float[][][] lbl_loc) {

    byte[][] bb = getColorArray(colors);
    byte[][] interp_bb = interpolateColorArray(bb);

    float[][] vv = getLineArray(vx, vy);
    float[][] interp_vv = interpolateLineArray(vv);

    // BMF 2006-10-04
    // interpolate twice if below threshhold to
    // make sure there are visible labels
    int ptCnt = vv.length / 2;
    if (ptCnt < INTERP_THRESHHOLD) {
      interp_bb = interpolateColorArray(interp_bb);
      interp_vv = interpolateLineArray(interp_vv);
    }

    processLineArrays(interp_vv, interp_bb, labelColor, out_vv, out_colors,
        out_vvL, out_colorsL, lbl_loc);
  }

  /**
   * Common line array code
   * 
   * @param vv_grid
   *          grid coordinates..
   * @param bb
   *          grid color values.
   * @param labelColor
   *          RGB label color byte array
   * @param out_vv
   * @param out_colors
   * @param out_vvL
   * @param out_colorsL
   * @param lbl_loc
   */
  private void processLineArrays(float[][] vv_grid, byte[][] bb,
      byte[] labelColor, float[][][] out_vv, byte[][][] out_colors,
      float[][][][] out_vvL, byte[][][][] out_colorsL, float[][][] lbl_loc) {

    float[][] vv = null;

    try {
      vv = css.spatial_set.gridToValue(vv_grid);
    } catch (VisADException e) {
      System.out.println(e.getMessage());
    }

    int clr_dim = 0;
    if (bb != null)
      clr_dim = bb.length;
    int n_lbl = 1;

    out_vvL[0] = null;
    out_colorsL[0] = null;
    out_vvL[1] = null;
    out_colorsL[1] = null;
    lbl_loc[0] = null;

    out_vvL[2] = null;
    out_colorsL[2] = null;
    out_vvL[3] = null;
    out_colorsL[3] = null;
    lbl_loc[1] = null;
    lbl_loc[2] = null;

    out_vv[0] = vv;
    out_colors[0] = bb;
    out_vv[1] = null;
    out_colors[1] = null;

    int totalPts = vv[0].length / 2;

    if ((totalPts > LBL_ALGM_THRESHHOLD && ((lev_idx & 1) == 1))
        || css.n_levs == 1) {
      // if ((lev_idx & 1) == 1 || css.n_levs == 1) {
      isLabeled = true;
      int loc = (vv[0].length) / 2; // - start at half-way pt.
      int n_pairs_b = 1;
      int n_pairs_f = 1;
      boolean found = false;
      float ctr_dist;
      int pos = loc;

      // - compute distance between label location (loc) and points
      // - on each side, when greater than lbl_half - stop. This
      // - assumes that around the label the contour line is fairly
      // - linear, seems good approx almost all of time.

      while (!found) { // - go backwards, ie decreasing index val
        pos -= 2;
        if (pos < 0 || pos > (vv[0].length - 1))
          return;
        float dx = vv[0][pos] - vv[0][loc];
        float dy = vv[1][pos] - vv[1][loc];
        float dz = vv[2][pos] - vv[2][loc];
        ctr_dist = (float) Math.sqrt((double) (dx * dx + dy * dy + dz * dz));
        if (ctr_dist > (float) Math.abs((double) lbl_half)) {
          found = true;
        } else {
          n_pairs_b++;
        }
      }

      pos = loc;
      found = false;
      while (!found) { // - go fowards, ie increasing index val
        pos += 2;
        if (pos < 0 || pos > (vv[0].length - 1))
          return;
        float dx = vv[0][pos] - vv[0][loc];
        float dy = vv[1][pos] - vv[1][loc];
        float dz = vv[2][pos] - vv[2][loc];
        ctr_dist = (float) Math.sqrt((double) (dx * dx + dy * dy + dz * dz));
        if (ctr_dist > (float) Math.abs((double) lbl_half)) {
          found = true;
        } else {
          n_pairs_f++;
        }
      }

      // - total number of points skipped (removed)
      n_skip = (n_pairs_b + n_pairs_f) * 2;
      if ((loc & 1) == 1) { // - odd
        start_break = loc - (1 + (n_pairs_b - 1) * 2);
        stop_break = loc + (2 + (n_pairs_f - 1) * 2);
      } else { // -even
        start_break = loc - (2 + (n_pairs_b - 1) * 2);
        stop_break = loc + (1 + (n_pairs_f - 1) * 2);
      }

      // - get the label vertices from the PlotDigits object for
      // - the isopleth value of the ContourStrip. 'B' arrays are
      // - for the flipped orientation.
      float[] vx_tmp = new float[plot.NumVerts];
      float[] vy_tmp = new float[plot.NumVerts];
      System.arraycopy(plot.Vx, 0, vx_tmp, 0, plot.NumVerts);
      System.arraycopy(plot.Vy, 0, vy_tmp, 0, plot.NumVerts);
      float[] vxB_tmp = new float[plot.NumVerts];
      float[] vyB_tmp = new float[plot.NumVerts];
      System.arraycopy(plot.VxB, 0, vxB_tmp, 0, plot.NumVerts);
      System.arraycopy(plot.VyB, 0, vyB_tmp, 0, plot.NumVerts);

      byte[][] lbl_clr = null;
      if (bb != null) {
        lbl_clr = new byte[clr_dim][plot.NumVerts];
      }

      // - Align labels with contour lines if rotate = true
      // ------------------------------------------------------
      boolean rotate = true;
      float[][] lbl_dcoords = null;
      if (rotate) {
        // - get a unit vector perpendicular to display coordinate grid
        // - at this label location (loc)
        float[][] norm = null;
        Gridded3DSet cg3d = (Gridded3DSet) css.spatial_set;
        try {
          norm = cg3d.getNormals(new float[][] { { vv_grid[0][loc] },
              { vv_grid[1][loc] } });
        } catch (VisADException e) {
          System.out.println(e.getMessage());
        }

        if (norm[2][0] < 0) {
          norm[0][0] = -norm[0][0];
          norm[1][0] = -norm[1][0];
          norm[2][0] = -norm[2][0];
        }

        // - get a unit vector parallel to the contour line at the label
        // - position.
        float del_x;
        float del_y;
        float del_z;
        del_z = vv[2][stop_break] - vv[2][start_break];
        del_y = vv[1][stop_break] - vv[1][start_break];
        del_x = vv[0][stop_break] - vv[0][start_break];
        float mag = (float) Math.sqrt(del_y * del_y + del_x * del_x + del_z
            * del_z);
        float[] ctr_u = new float[] { del_x / mag, del_y / mag, del_z / mag };

        if (ctr_u[0] < 0) {
          ctr_u[0] = -ctr_u[0];
          ctr_u[1] = -ctr_u[1];
          ctr_u[2] = -ctr_u[2];
        }

        // - get a vector perpendicular to contour line, and in the local
        // - tangent plane. norm_x_ctr: cross-product of local norm and
        // - unit vector parallel to contour line at label location.
        float[] norm_x_ctr = new float[] {
            norm[1][0] * ctr_u[2] - norm[2][0] * ctr_u[1],
            -(norm[0][0] * ctr_u[2] - norm[2][0] * ctr_u[0]),
            norm[0][0] * ctr_u[1] - norm[1][0] * ctr_u[0] };

        mag = (float) Math.sqrt(norm_x_ctr[0] * norm_x_ctr[0] + norm_x_ctr[1]
            * norm_x_ctr[1] + norm_x_ctr[2] * norm_x_ctr[2]);

        // - normalize vector
        norm_x_ctr[0] = norm_x_ctr[0] / mag;
        norm_x_ctr[1] = norm_x_ctr[1] / mag;
        norm_x_ctr[2] = norm_x_ctr[2] / mag;

        if (Math.abs((double) norm[2][0]) <= 0.00001) {
          if (norm_x_ctr[2] < 0) {
            norm_x_ctr[0] = -norm_x_ctr[0];
            norm_x_ctr[1] = -norm_x_ctr[1];
            norm_x_ctr[2] = -norm_x_ctr[2];
          }
        } else {
          if (norm_x_ctr[1] < 0) {
            norm_x_ctr[0] = -norm_x_ctr[0];
            norm_x_ctr[1] = -norm_x_ctr[1];
            norm_x_ctr[2] = -norm_x_ctr[2];
          }
        }

        // - align labels with contour lines at label location,
        // - lbl_dcoords are the result of the rotation.
        lbl_dcoords = new float[3][plot.NumVerts];
        for (int kk = 0; kk < plot.NumVerts; kk++) {
          lbl_dcoords[0][kk] = vx_tmp[kk] * ctr_u[0] + vyB_tmp[kk]
              * norm_x_ctr[0];
          lbl_dcoords[1][kk] = vx_tmp[kk] * ctr_u[1] + vyB_tmp[kk]
              * norm_x_ctr[1];
          lbl_dcoords[2][kk] = vx_tmp[kk] * ctr_u[2] + vyB_tmp[kk]
              * norm_x_ctr[2];
        }
        // - translate rotated label to plot location (loc)
        for (int kk = 0; kk < plot.NumVerts; kk++) {
          lbl_dcoords[0][kk] += vv[0][loc];
          lbl_dcoords[1][kk] += vv[1][loc];
          lbl_dcoords[2][kk] += vv[2][loc];
        }

      }
      // -- end label alignment

      // -- translate to label plot location --------------
      for (int kk = 0; kk < plot.NumVerts; kk++) {
        vx_tmp[kk] += vv[0][loc];
        vy_tmp[kk] += vv[1][loc];
        vxB_tmp[kk] += vv[0][loc];
        vyB_tmp[kk] += vv[1][loc];
      }
      // -- assign color to contour labels --------------
      if (labelColor != null) {
        for (int kk = 0; kk < plot.NumVerts; kk++) {
          lbl_clr[0][kk] = labelColor[0];
          lbl_clr[1][kk] = labelColor[1];
          lbl_clr[2][kk] = labelColor[2];
          if (clr_dim == 4)
            lbl_clr[3][kk] = labelColor[3];
        }
      } else if (bb != null) {
        for (int kk = 0; kk < plot.NumVerts; kk++) {
          lbl_clr[0][kk] = bb[0][loc];
          lbl_clr[1][kk] = bb[1][loc];
          lbl_clr[2][kk] = bb[2][loc];
          if (clr_dim == 4)
            lbl_clr[3][kk] = bb[3][loc];
        }
      }

      // - this sections creates the contour gap for the label
      out_vvL[0] = new float[n_lbl][][];
      out_colorsL[0] = new byte[n_lbl][][];
      out_vvL[1] = new float[n_lbl][][];
      out_colorsL[1] = new byte[n_lbl][][];
      lbl_loc[0] = new float[n_lbl][7];
      lbl_loc[0][0][0] = vv[0][loc];
      lbl_loc[0][0][1] = vv[1][loc];
      lbl_loc[0][0][2] = vv[2][loc];
      out_vv[0] = new float[3][vv[0].length - n_skip];
      out_vv[1] = new float[3][n_skip];
      if (bb != null) {
        out_colors[0] = new byte[clr_dim][bb[0].length - n_skip];
        out_colors[1] = new byte[clr_dim][n_skip];
      }

      int s_pos = 0;
      int d_pos = 0;
      int cnt = start_break;

      System.arraycopy(vv[0], s_pos, out_vv[0][0], d_pos, cnt);
      System.arraycopy(vv[1], s_pos, out_vv[0][1], d_pos, cnt);
      System.arraycopy(vv[2], s_pos, out_vv[0][2], d_pos, cnt);
      if (bb != null) {
        for (int cc = 0; cc < clr_dim; cc++) {
          System.arraycopy(bb[cc], s_pos, out_colors[0][cc], d_pos, cnt);
        }
      }

      s_pos = start_break;
      d_pos = 0;
      cnt = n_skip;

      System.arraycopy(vv[0], s_pos, out_vv[1][0], d_pos, cnt);
      System.arraycopy(vv[1], s_pos, out_vv[1][1], d_pos, cnt);
      System.arraycopy(vv[2], s_pos, out_vv[1][2], d_pos, cnt);
      if (bb != null) {
        for (int cc = 0; cc < clr_dim; cc++) {
          System.arraycopy(bb[cc], s_pos, out_colors[1][cc], d_pos, cnt);
        }
      }

      s_pos = stop_break + 1;
      d_pos = start_break;
      cnt = vv[0].length - s_pos;

      System.arraycopy(vv[0], s_pos, out_vv[0][0], d_pos, cnt);
      System.arraycopy(vv[1], s_pos, out_vv[0][1], d_pos, cnt);
      System.arraycopy(vv[2], s_pos, out_vv[0][2], d_pos, cnt);
      if (bb != null) {
        for (int cc = 0; cc < clr_dim; cc++) {
          System.arraycopy(bb[cc], s_pos, out_colors[0][cc], d_pos, cnt);
        }
      }
      // --- end label gap code

      // --- expanding/contracting left-right segments

      out_vvL[2] = new float[n_lbl][3][2];
      out_vvL[3] = new float[n_lbl][3][2];
      lbl_loc[1] = new float[n_lbl][3];
      lbl_loc[2] = new float[n_lbl][3];
      if (bb != null) {
        out_colorsL[2] = new byte[n_lbl][clr_dim][2];
        out_colorsL[3] = new byte[n_lbl][clr_dim][2];
      }
      // - left
      s_pos = start_break;
      d_pos = 0;
      cnt = 2;
      lbl_loc[1][0][0] = vv[0][s_pos];
      lbl_loc[1][0][1] = vv[1][s_pos];
      lbl_loc[1][0][2] = vv[2][s_pos];

      // - unit left
      float dx = vv[0][loc] - vv[0][s_pos];
      float dy = vv[1][loc] - vv[1][s_pos];
      float dz = vv[2][loc] - vv[2][s_pos];
      float dd = (float) Math.sqrt((double) (dx * dx + dy * dy + dz * dz));
      dx = dx / dd;
      dy = dy / dd;
      dz = dz / dd;
      float mm = dd - (float) Math.abs((double) lbl_half);
      dx *= mm;
      dy *= mm;
      dz *= mm;
      out_vvL[2][0][0][0] = vv[0][s_pos];
      out_vvL[2][0][1][0] = vv[1][s_pos];
      out_vvL[2][0][2][0] = vv[2][s_pos];
      out_vvL[2][0][0][1] = vv[0][s_pos] + dx;
      out_vvL[2][0][1][1] = vv[1][s_pos] + dy;
      out_vvL[2][0][2][1] = vv[2][s_pos] + dz;
      lbl_loc[0][0][3] = lbl_half;
      lbl_loc[0][0][4] = dd;
      if (bb != null) {
        for (int cc = 0; cc < clr_dim; cc++) {
          System.arraycopy(bb[cc], s_pos, out_colorsL[2][0][cc], d_pos, cnt);
        }
      }

      // - right
      s_pos = stop_break - 1;
      d_pos = 0;
      cnt = 2;
      lbl_loc[2][0][0] = vv[0][stop_break];
      lbl_loc[2][0][1] = vv[1][stop_break];
      lbl_loc[2][0][2] = vv[2][stop_break];

      // - unit right
      dx = vv[0][loc] - vv[0][stop_break];
      dy = vv[1][loc] - vv[1][stop_break];
      dz = vv[2][loc] - vv[2][stop_break];
      dd = (float) Math.sqrt((double) (dx * dx + dy * dy + dz * dz));
      dx = dx / dd;
      dy = dy / dd;
      dz = dz / dd;
      mm = dd - (float) Math.abs((double) lbl_half);
      dx *= mm;
      dy *= mm;
      dz *= mm;
      out_vvL[3][0][0][0] = vv[0][stop_break];
      out_vvL[3][0][1][0] = vv[1][stop_break];
      out_vvL[3][0][2][0] = vv[2][stop_break];
      out_vvL[3][0][0][1] = vv[0][stop_break] + dx;
      out_vvL[3][0][1][1] = vv[1][stop_break] + dy;
      out_vvL[3][0][2][1] = vv[2][stop_break] + dz;
      lbl_loc[0][0][5] = lbl_half;
      lbl_loc[0][0][6] = dd;
      if (bb != null) {
        for (int cc = 0; cc < clr_dim; cc++) {
          System.arraycopy(bb[cc], s_pos, out_colorsL[3][0][cc], d_pos, cnt);
        }
      }
      // ----- end expanding/contracting line segments

      // --- label vertices
      out_vvL[0][0] = new float[3][];
      out_vvL[0][0][0] = lbl_dcoords[0];
      out_vvL[0][0][1] = vy_tmp;
      out_colorsL[0][0] = lbl_clr;
      out_vvL[1][0] = new float[3][];
      out_vvL[1][0][0] = vxB_tmp;
      out_vvL[1][0][1] = lbl_dcoords[1];
      out_colorsL[1][0] = lbl_clr;
      out_vvL[0][0][2] = lbl_dcoords[2];
      out_vvL[1][0][2] = lbl_dcoords[2];
    } else { // - no label
      out_vv[0] = vv;
      out_colors[0] = bb;
      out_vv[1] = null;
      out_colors[1] = null;
      return;
    }
  }

  /**
   * Get a line array using this instances cached indexes.
   * 
   * @param vx
   *          X values to apply cached indexes to.
   * @param vy
   *          Y values to apply cached indexes to.
   * @see {@link VisADLineArray}
   * @return
   */
  float[][] getLineArray(float[] vx, float[] vy) {
    if (vx == null || vy == null) {
      return null;
    }
    float[] vvx = new float[hi_idx - low_idx + 1];
    float[] vvy = new float[vvx.length];

    for (int kk = low_idx, ii = 0; kk <= hi_idx; kk++, ii++) {
      vvx[ii] = vx[idx_array[kk]];
      vvy[ii] = vy[idx_array[kk]];
    }
    return new float[][] { vvx, vvy };
  }

  /**
   * Get line strip arrays for this strip.
   * 
   * @param vx
   *          X grid coords to apply cached indexes to.
   * @param vy
   *          Y grid coords to apply cached indexes to.
   * @return If this strip is has a label the first dim will be 2 arrays, one
   *         for before the label and one for after. Otherwise the first
   *         dimension will be a single array for the entire strip.
   */
  float[][][] getLineStripArrays(float[] vx, float[] vy) {

    int count = hi_idx - low_idx + 1;

    int lenBefore = start_break / 2 + 1;
    int lenAfter = (count - stop_break + 1) / 2;

    // if we're labeling and there are enough points before
    // and after to make at least 1 line
    if (isLabeled && (lenBefore >= 2 && lenAfter >= 2)) {
      float[][] vvBefore = new float[2][lenBefore];

      // the first point in the array
      vvBefore[0][0] = vx[idx_array[low_idx]];
      vvBefore[1][0] = vy[idx_array[low_idx]];

      // every other point up to the start of the break
      int kk = low_idx + 1;
      for (int ii = 1; ii < vvBefore[0].length; kk += 2, ii++) {
        vvBefore[0][ii] = vx[idx_array[kk]];
        vvBefore[1][ii] = vy[idx_array[kk]];
      }

      // skip to stop_break
      kk += n_skip - 1;

      float[][] vvAfter = new float[2][lenAfter];
      vvAfter[0][0] = vx[idx_array[kk]];
      vvAfter[1][0] = vy[idx_array[kk]];

      // every other point to the end
      kk++;
      for (int ii = 1; ii < vvAfter[0].length; kk += 2, ii++) {
        vvAfter[0][ii] = vx[idx_array[kk]];
        vvAfter[1][ii] = vy[idx_array[kk]];
      }

      // return new float[][][]{vvAfter};
      return new float[][][] { vvBefore, vvAfter };
    }

    // no label
    float[][] vv = null;
    if (count == 2) { // can't have less than 2 verticies
      vv = new float[2][count];
    } else {
      vv = new float[2][count / 2 + 1];
    }

    vv[0][0] = vx[idx_array[low_idx]];
    vv[1][0] = vy[idx_array[low_idx]];

    for (int kk = low_idx + 1, ii = 1; kk <= hi_idx; kk += 2, ii++) {
      vv[0][ii] = vx[idx_array[kk]];
      vv[1][ii] = vy[idx_array[kk]];
    }

    return new float[][][] { vv };
  }

  /**
   * Get the array of colors corresponding to cached indexes.
   * 
   * @param colors
   *          Line array formatted colors where the first dimension is the color
   *          dimension and the second the color values.
   * @see {@link VisADLineArray}
   * @return Array of colors in line array format.
   */
  byte[][] getColorArray(byte[][] colors) {
    if (colors == null)
      return null;
    int clr_dim = colors.length;
    int clr_len = (hi_idx - low_idx) + 1;
    byte[][] new_colors = new byte[clr_dim][clr_len];

    int ii = 0;
    for (int kk = low_idx; kk <= hi_idx; kk++) {
      for (int cc = 0; cc < clr_dim; cc++) {
        new_colors[cc][ii] = colors[cc][idx_array[kk]];
      }
      ii++;
    }
    return new_colors;
  }

  /**
   * Get the array of colors corresponding to cached indexes.
   * 
   * @param colors
   *          Line array formatted colors where the first dimension is the color
   *          dimension and the second the color values.
   * @see {@link VisADStripLineArray}
   * @return Array of colors in line strip array format.
   */
  byte[][][] getColorStripArrays(byte[][] colors) {

    int clrDim = colors.length;
    int count = hi_idx - low_idx + 1;

    int lenBefore = start_break / 2 + 1;
    int lenAfter = (count - stop_break + 1) / 2;
    
    if (isLabeled && (lenBefore >= 2 && lenAfter >= 2)) {
      byte[][] colorsBefore = new byte[clrDim][start_break / 2 + 1];

      // first point
      for (int cc = 0; cc < clrDim; cc++) {
        colorsBefore[cc][0] = colors[cc][idx_array[low_idx]];
      }

      // every other redundant point
      int kk = low_idx + 1;
      for (int ii = 1; ii < colorsBefore[0].length; kk += 2, ii++) {
        for (int cc = 0; cc < clrDim; cc++) {
          colorsBefore[cc][ii] = colors[cc][idx_array[kk]];
        }
      }

      kk += n_skip - 1;

      byte[][] colorsAfter = new byte[clrDim][(count - stop_break + 1) / 2];
      for (int cc = 0; cc < clrDim; cc++) {
        colorsAfter[cc][0] = colors[cc][idx_array[kk]];
      }

      // every other redundant point
      kk++;
      for (int ii = 1; ii < colorsAfter[0].length; kk += 2, ii++) {
        for (int cc = 0; cc < clrDim; cc++) {
          colorsAfter[cc][ii] = colors[cc][idx_array[kk]];
        }
      }

      // return new byte[][][]{colorsAfter};
      return new byte[][][] { colorsBefore, colorsAfter };
    }

    // no label
    byte[][] bb = null;
    if (count == 2) {
      bb = new byte[clrDim][count];
    } else {
      bb = new byte[clrDim][count / 2 + 1];
    }

    for (int cc = 0; cc < clrDim; cc++) {
      bb[cc][0] = colors[cc][idx_array[low_idx]];
    }

    for (int ii = 1, kk = low_idx + 1; kk <= hi_idx; kk += 2, ii++) {
      for (int cc = 0; cc < clrDim; cc++) {
        bb[cc][ii] = colors[cc][idx_array[kk]];
      }
    }

    return new byte[][][] { bb };
  }
  
  boolean isLabeled() {
    return isLabeled;
  }

  /**
   * Make dashes out of line array.
   * 
   * @param vv
   * 
   * @return A line array adjusted for dashes.
   * @deprecated Dashing can be set via a <code>ContantMap</code> or by using
   *             {@link GraphicsModeControl#setLineStyle(int)}.
   */
  float[][] getDashedLineArray(float[][] vv) {

    int X = 0;
    int Y = 1;

    // length of new array, Always even for line array
    int len = vv[0].length;

    float[][] interp = new float[2][len];

    // System.err.println("    vv[0].length:"+vv[0].length+" len:"+len+" skip:"+
    // skip);

    // from Contour2D.contour(...)
    for (int i = 0; i < vv[0].length; i += 2) {
      float vxa, vya, vxb, vyb;
      vxa = vv[X][i + 1];
      vya = vv[Y][i + 1];
      vxb = vv[X][i];
      vyb = vv[Y][i];
      interp[X][i + 1] = (3.0f * vxa + vxb) * 0.25f;
      interp[Y][i + 1] = (3.0f * vya + vyb) * 0.25f;
      interp[X][i] = (vxa + 3.0f * vxb) * 0.25f;
      interp[Y][i] = (vya + 3.0f * vyb) * 0.25f;
    }

    return interp;

  }

  // alternate interpolation
  // /**
  // * Take a color array and remove <code>skip</code> sized segments to
  // * match a dashed line array. No-op for <code>skip</code> <= 1.
  // * @param vv Line array as returned by <code>getLineArray</code>.
  // * @param skip Number of points to make up a dash; ie. number to skip.
  // * @see #getDashedLineArray(float[][], int)
  // * @return A line array interpolated as a dashed line array.
  // */
  // byte[][] getDashedColorArray(byte[][] colors, int skip) {
  //    
  // if (colors == null) return null;
  //    
  // // length of new array, Always even for line array
  // int len = (colors[0].length)/skip;
  // if( len % 2 == 1 ) len += 1;
  //    
  // //System.err.println("colors[0].length:"+colors[0].length+" len:"+len+
  // " skip:"+skip);
  //    
  // byte[][] interp = new byte[colors.length][len];
  //    
  // for(int i=0, j=0; i+skip<colors[0].length; i+=2*skip, j+=2) {
  // for (int k=0; k<colors.length; k++) {
  // interp[k][j] = colors[k][i];
  // interp[k][j+1] = colors[k][i+skip];
  // }
  // }
  //    
  // Make all colors white, for DEBUG'ing
  // for (int j=0; j<interp[0].length; j++){
  // for (int i=0; i<interp.length; i++){
  // interp[i][j] = (byte)255;
  // }
  // }
  //    
  // return interp;
  // }

  /**
   * BMF 2006-09-29 Double the size of a line array by adding the computed
   * midmoint between existing values.
   * 
   * @param vv
   *          Line array as returned by getLineArray(float[], float[])
   * @return An interpolated line array
   * @deprecated J3D line styles are now used, so interrpretation is no longer
   *             necessary.
   */
  float[][] interpolateLineArray(float[][] vv) {

    int X = 0;
    int Y = 1;

    int len = vv[0].length * 2;
    float[][] interp = new float[2][len];

    for (int i = 0, j = 0; i < vv[0].length; i += 2, j += 4) {
      interp[X][j] = vv[X][i];
      interp[Y][j] = vv[Y][i];

      interp[X][j + 1] = vv[X][i] + 0.5f * (vv[X][i + 1] - vv[X][i]);
      interp[Y][j + 1] = vv[Y][i] + 0.5f * (vv[Y][i + 1] - vv[Y][i]);

      interp[X][j + 2] = interp[X][j + 1];
      interp[Y][j + 2] = interp[Y][j + 1];

      interp[X][j + 3] = vv[X][i + 1];
      interp[Y][j + 3] = vv[Y][i + 1];
    }

    return interp;

  }

  /**
   * BMF 2006-09-29 Doubles the size of the color array by adding averaged
   * colors between existing colors.
   * 
   * @param colors
   *          Color array as returned by <code>getColorArray()</code>.
   * @return Interpreted color array.
   * @deprecated J3D line styles are now used, so interrpretation is no longer
   *             necessary.
   */
  byte[][] interpolateColorArray(byte[][] colors) {

    if (colors == null)
      return null;

    byte[][] interp = new byte[colors.length][colors[0].length * 2];

    for (int i = 0, j = 0; i < colors[0].length; i += 2, j += 4) {
      for (int k = 0; k < colors.length; k++) {
        byte avg = (byte) ((colors[k][i] + colors[k][i + 1]) / 2);
        interp[k][j] = colors[k][i];
        interp[k][j + 1] = avg;
        interp[k][j + 2] = avg;
        interp[k][j + 3] = colors[k][i + 1];
      }
    }

    // set all colors to white for debuging
    // for (int j=0; j<interp[0].length; j++){
    // for (int i=0; i<interp.length; i++){
    // if(i==3) interp[i][j] = (byte)255;
    // else interp[i][j] = (byte)255;
    // }
    // }

    return interp;
  }

  /**
   * 
   * 
   * @param c_strp
   * 
   * @return
   */
  ContourStrip merge(ContourStrip c_strp) {
    if (this.lev_idx != c_strp.lev_idx) {
      System.out.println("Contour2D.ContourStrip.merge: !BIG ATTENTION!");
    }

    int new_length;
    int[] new_idx_array = null;
    int[] thisLo = new int[2];
    int[] thisHi = new int[2];
    int[] thatLo = new int[2];
    int[] thatHi = new int[2];

    thisLo[0] = idx_array[low_idx];
    thisLo[1] = idx_array[low_idx + 1];
    thisHi[0] = idx_array[hi_idx];
    thisHi[1] = idx_array[hi_idx - 1];
    thatLo[0] = c_strp.idx_array[c_strp.low_idx];
    thatLo[1] = c_strp.idx_array[c_strp.low_idx + 1];
    thatHi[0] = c_strp.idx_array[c_strp.hi_idx];
    thatHi[1] = c_strp.idx_array[c_strp.hi_idx - 1];

    if (((thisLo[0] == thatLo[0]) || (thisLo[0] == thatLo[1]))
        || ((thisLo[1] == thatLo[0]) || (thisLo[1] == thatLo[1]))) {
      new_length = (hi_idx - low_idx) + 1 + (c_strp.hi_idx - c_strp.low_idx)
          + 1;
      new_length -= 2;
      new_idx_array = new int[new_length];

      int ii = 0;
      for (int kk = hi_idx; kk >= low_idx; kk--) {
        new_idx_array[ii] = idx_array[kk];
        ii++;
      }
      for (int kk = c_strp.low_idx + 2; kk <= c_strp.hi_idx; kk++) {
        new_idx_array[ii] = c_strp.idx_array[kk];
        ii++;
      }
    } else if (((thisLo[0] == thatHi[0]) || (thisLo[0] == thatHi[1]))
        || ((thisLo[1] == thatHi[0]) || (thisLo[1] == thatHi[1]))) {
      new_length = (hi_idx - low_idx) + 1 + (c_strp.hi_idx - c_strp.low_idx)
          + 1;
      new_length -= 2;
      new_idx_array = new int[new_length];

      int ii = 0;
      for (int kk = hi_idx; kk >= low_idx; kk--) {
        new_idx_array[ii] = idx_array[kk];
        ii++;
      }
      for (int kk = c_strp.hi_idx - 2; kk >= c_strp.low_idx; kk--) {
        new_idx_array[ii] = c_strp.idx_array[kk];
        ii++;
      }
    } else if (((thisHi[0] == thatHi[0]) || (thisHi[0] == thatHi[1]))
        || ((thisHi[1] == thatHi[0]) || (thisHi[1] == thatHi[1]))) {
      new_length = (hi_idx - low_idx) + 1 + (c_strp.hi_idx - c_strp.low_idx)
          + 1;
      new_length -= 2;
      new_idx_array = new int[new_length];

      int ii = 0;
      for (int kk = low_idx; kk <= hi_idx; kk++) {
        new_idx_array[ii] = idx_array[kk];
        ii++;
      }
      for (int kk = c_strp.hi_idx - 2; kk >= c_strp.low_idx; kk--) {
        new_idx_array[ii] = c_strp.idx_array[kk];
        ii++;
      }
    } else if (((thisHi[0] == thatLo[0]) || (thisHi[0] == thatLo[1]))
        || ((thisHi[1] == thatLo[0]) || (thisHi[1] == thatLo[1]))) {
      new_length = (hi_idx - low_idx) + 1 + (c_strp.hi_idx - c_strp.low_idx)
          + 1;
      new_length -= 2;
      new_idx_array = new int[new_length];

      int ii = 0;
      for (int kk = low_idx; kk <= hi_idx; kk++) {
        new_idx_array[ii] = idx_array[kk];
        ii++;
      }
      for (int kk = c_strp.low_idx + 2; kk <= c_strp.hi_idx; kk++) {
        new_idx_array[ii] = c_strp.idx_array[kk];
        ii++;
      }
    } else {
      return null;
    }

    return new ContourStrip(new_idx_array, lev_idx, plot, css);
  }

  /**
   * 
   * 
   * @return
   */
  public String toString() {
    return "(" + idx_array[low_idx] + "," + idx_array[low_idx + 1] + "), ("
        + idx_array[hi_idx] + "," + idx_array[hi_idx - 1] + ")";
  }
}
