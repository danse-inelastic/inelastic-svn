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

package com.artenum.cassandra.launcher;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import java.util.Enumeration;
import java.util.Properties;

/**
 * <pre>
 * <b>Project ref           :</b> CASSANDRA project
 * <b>Copyright and license :</b> See relevant sections
 * <b>Status                :</b> under development
 * <b>Creation              :</b> 04/03/2005
 * <b>Modification          :</b>
 *
 * <b>Description  :</b> Artenum internal project
 *
 * </pre>
 * <table cellpadding="3" cellspacing="0" border="1" width="100%">
 * <tr BGCOLOR="#CCCCFF" CLASS="TableHeadingColor"><td><b>Version number</b></td><td><b>Author (name, e-mail)</b></td><td><b>Corrections/Modifications</b></td></tr>
 * <tr><td>0.1</td><td>Sebastien Jourdain, jourdain@artenum.com</td><td>Creation</td></tr>
 * </table>
 *
 * @author        Sebastien Jourdain
 * @version       0.1
 */
public class PropertyLoader {
    public static void loadProperties(String fileToLoad)
        throws IOException, FileNotFoundException {
        loadProperties(new File(fileToLoad));
    }

    public static void loadProperties(File fileToLoad)
        throws IOException, FileNotFoundException {
        FileInputStream fis = null;
        Properties props = new Properties();
        try {
            fis = new FileInputStream(fileToLoad);
            props.load(fis);
        } finally {
            if (fis != null) {
                fis.close();
            }
        }

        for (Enumeration e = props.keys(); e.hasMoreElements();) {
            String key = (String) e.nextElement();
            System.setProperty(key, props.getProperty(key));
        }
    }
}
