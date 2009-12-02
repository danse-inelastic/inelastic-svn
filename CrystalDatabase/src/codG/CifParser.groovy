/*
  Automatically Converted from Java Source 
  
  by java2groovy v0.0.1   Copyright Jeremy Rayner 2007
  
  !! NOT FIT FOR ANY PURPOSE !! 
  'java2groovy' cannot be used to convert one working program into another  */

package cod

import java.io.File
import java.io.FileWriter
import java.io.IOException
import java.util.ArrayList
import java.util.NoSuchElementException
import java.util.Scanner

import org.cheffo.jeplite.JEP

class CifParser 
    {private String contents
    private ArrayList<String> lines = new ArrayList<String>()
    private ArrayList<Integer> loops = new ArrayList<Integer>()
    ArrayList<String> species = new ArrayList<String>()
    ArrayList<double[]> coordinates = new ArrayList<double[]>()
    ArrayList<double[]> newCoordinates = new ArrayList<double[]>()
    ArrayList<String> newSpecies = new ArrayList<String>()
    private File f
    boolean modified = false

    CifParserCifParser(String contents) throws Exception{
        this.contents = contents
        Scanner temp = new Scanner(this.contents)
        while (temp.hasNext()) {
            String s = temp.nextLine().trim()
            if (!s.startsWith("#")) {
                if (s.startsWith("loop_")) 
                loops.add(lines.size())
                lines.add(s)
}
}







        temp.close()
}













    CifParserCifParser(File file) throws Exception{
        f = file
        this.contents = Main.getFileContents("file:" + file.getPath()).toString()
        Scanner temp = new Scanner(this.contents)
        while (temp.hasNext()) {
            String s = temp.nextLine().trim()
            if (!s.startsWith("#")) {
                if (s.startsWith("loop_")) 
                loops.add(lines.size())
                lines.add(s)
}
}







        temp.close()
}














    void SaveDialog() throws IOException{




        if (modified) {
            System.out.println(f.getPath())
}
}




















    StringBuffer debug = new StringBuffer()

    void parseOperators() throws Exception{
        ArrayList<Integer> indices = indicesOf("_symmetry_equiv_pos_as_xyz")
        if (indices.size() == 0) 
        return 
        if (indices.size() == 1) {
            int index = indices.get(0)
            String str = null
            JEP jep = new JEP()
            while (

























                lines.get(index + 1).trim().startsWith("'")
) {

                index++
                str = lines.get(index).trim()

                str = str.replace("'", """")
                String[] dims = str.split(",")
                if (dims.length != 3) 
                throw new Exception("not 3 operations")

                for (int j = 0 ; j < coordinates.size() ; j++){
                    double[] temp = coordinates.get(j)
                    double[] d = new double[3]

                    for (int i = 0 ; i < d.length ; i++){
                        String s = dims[i].trim()
                        s = s.replace("x", """" + temp[0])
                        s = s.replace("y", """" + temp[1])
                        s = s.replace("z", """" + temp[2])
                        s = replaceFractions(s)
                        jep.parseExpression(s)
                        d[i] = jep.getValue()
}








                    newCoordinates.add(d)
                    newSpecies.add(species.get(j))
}
}
}
}





































    void parseCoordinates(String str) throws Exception{

        ArrayList<Integer> indices = indicesOf(str)
        if (indices.size() == 0) 
        return 
        if (indices.size() > 1) 
        return 
        int index = indices.get(0)


        int loop = -1
        for (int i = 0 ; i < loops.size() ; i++){
            if (loops.get(i) < index) 
            loop = loops.get(i)
}




        int fields = 1
        while (lines.get(loop + fields).startsWith("_")) {
            fields++
}



        int diff = index - loop - 2
        for (int i = loop + fields ; i < lines.size() ; i++){
            String l = lines.get(i)
            if (l.startsWith("loop_") || l.equals("""") || l.startsWith("_")) {
                i = lines.size()
} else {





















                try {

                    lines.set(i, removeParens(lines.get(i)))
                    Scanner sc = new Scanner(lines.get(i))
                    debug.append(lines.get(i) + "\n")
                    String s = sc.next()
                    for (int j = 0 ; j < diff ; j++)
                    sc.next()

                    double[] d = new double[3]
                    d[0] = Double.parseDouble(sc.next())
                    d[1] = Double.parseDouble(sc.next())
                    d[2] = Double.parseDouble(sc.next())

                    species.add(s)
                    coordinates.add(d)
                    sc.close()
}
















                 catch (NoSuchElementException e) {
                    debug.append("Concatenating lines\n")
                    lines.set(i, lines.get(i) + " " + lines.remove(i + 1))
                    i--

                    e.printStackTrace()
}
}
}
}












































































    final private String[] elements = ["h"]











    private boolean startsWithElement(String s) {
        if (s.length() < 2 || s.startsWith("Uiso") || s.startsWith("Uani")
             || s.startsWith("iso") || s.startsWith("Uij")
             || s.startsWith("aniso") || s.startsWith("Ueq")
             || s.startsWith("Vani") || s.startsWith("Viso")
             || s.startsWith("calc") || s.startsWith("Bij")
             || s.startsWith("uani")
) 





        return false
        s = s.substring(0, 2).toLowerCase()
        for <FOR_EACH_CLAUSE>String q</FOR_EACH_CLAUSE>{
            if (s.startsWith(q)) 
            return true
}



        s = s.substring(0, 1)
        for <FOR_EACH_CLAUSE>String q</FOR_EACH_CLAUSE>{
            if (s.startsWith(q)) 
            return true
}



        return false
}




















    void getAllCoordinates() {}



    private String replaceFractions(String s) {
        if (s.contains("1/2")) {
            s = s.replace("1/2", "0.5")
            modified = true
}



        if (s.contains("1/4")) {
            s = s.replace("1/4", "0.25")
            modified = true
}



        if (s.contains("3/4")) {
            s = s.replace("3/4", "0.75")
            modified = true
}



        if (s.contains("1/3")) {
            s = s.replace("1/3", String.valueOf(1.0 / 3.0))
            modified = true
}



        if (s.contains("2/3")) {
            s = s.replace("2/3", String.valueOf(2.0 / 3.0))
            modified = true
}



        if (s.contains("3/2")) {
            s = s.replace("3/2", "1.5")
            modified = true
}



        return s
}



























    String removeParens(String s) {
        if (s.contains("(")) {
            s = s.replace("(", """")
            modified = true
}



        if (s.contains(")")) {
            s = s.replace(")", """")
            modified = true
}



        s = replaceFractions(s)
        return s
}












    private int indexOf(String search) {
        int index = -1
        for (int i = 0 ; i < lines.size() ; i++){
            if (lines.get(i).contains(search)) {
                index = i
                i = lines.size()
}
}





        return index
}










    private ArrayList<Integer> indicesOf(String search) {
        ArrayList<Integer> indices = new ArrayList<Integer>()
        for (int i = 0 ; i < lines.size() ; i++){
            if (lines.get(i).contains(search)) {
                indices.add(i)
}
}




        return indices
}









    private StringBuffer printFile() {
        StringBuffer sb = new StringBuffer()
        for <FOR_EACH_CLAUSE>String s</FOR_EACH_CLAUSE>{
            sb.append(s + "\n")
}


        return sb
}







    private void writeFile(String s) throws IOException{
        FileWriter fw = new FileWriter(f)


        fw.write(s)
        fw.close()
}







    void removeDuplicates() {

        if (newCoordinates.size() != 0) {

            for (int i = 0 ; i < newCoordinates.size() ; i++){
                double[] d = newCoordinates.get(i)
                for (int j = 0 ; j < d.length ; j++){
                    if (d[j] >= 1) 
                    d[j] = d[j] - 1.0
                    if (d[j] < 0) 
                    d[j] = d[j] + 1.0
}





                newCoordinates.set(i, d)
}











            for (int i = 0 ; i < newCoordinates.size() - 1 ; i++){
                for (int j = i + 1 ; j < newCoordinates.size() ; j++){
                    double[] d1 = newCoordinates.get(i)double[] d2 = newCoordinates.get(j)
                    if (distance(d1, d2) < 0.000001) {
                        newCoordinates.remove(j)
                        newSpecies.remove(j)
                        j--
}
}
}
}
}




























    private double distance(double[] d1, double[] d2) {
        double x = d1[0] - d2[0]
        double y = d1[1] - d2[1]
        double z = d1[2] - d2[2]
        return Math.sqrt(x*x + y*y + z*z)
}
}
