/*
 * (c) Copyright: Artenum SARL, 101-103 Boulevard Mac Donald,
 *                75019, Paris, France 2005.
 *                http://www.artenum.com
 *
 * License:
 *
 *  This program is free software; you can redistribute it
 *  and/or modify it under the terms of the Q Public License;
 *  either version 1 of the License.
 *
 *  This program is distributed in the hope that it will be
 *  useful, but WITHOUT ANY WARRANTY; without even the implied
 *  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 *  PURPOSE. See the Q Public License for more details.
 *
 *  You should have received a copy of the Q Public License
 *  License along with this program;
 *  if not, write to:
 *    Artenum SARL, 101-103 Boulevard Mac Donald,
 *    75019, PARIS, FRANCE, e-mail: contact@artenum.com
 */
package com.artenum.cassandra.util;

import java.io.File;

import java.util.ArrayList;
import java.util.Comparator;

/**
 * @author Sebastien
 */
public class FileComparator implements Comparator {
    public int compare(Object o1, Object o2) {
        ArrayList f1 = CassandraToolBox.splitNumbers(((File) o1).getName());
        ArrayList f2 = CassandraToolBox.splitNumbers(((File) o2).getName());
        StringBuffer s1 = null;
        StringBuffer s2 = null;
        int n1;
        int n2;
        for (int i = 0; i < f1.size(); i++) {
            s1 = (StringBuffer) f1.get(i);
            s2 = (StringBuffer) f2.get(i);
            if ((s1.charAt(0) <= '9') && (s1.charAt(0) >= '0')) {
                // Compare number
                n1 = Integer.parseInt(s1.toString());
                n2 = Integer.parseInt(s2.toString());
                if (n2 != n1) {
                    return (n1 - n2);
                }
            } else {
                // Compare text
                if (s1.toString().compareTo(s2.toString()) != 0) {
                    return s1.toString().compareTo(s2.toString());
                }
            }
        }

        return 0;
    }
}
