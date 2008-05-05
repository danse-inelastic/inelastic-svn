package cod;

import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.HeadlessException;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;

import javafireball.controller.JavaFireball;
import javagulp.controller.JavaGULP;

import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;

import org.openscience.jmol.app.Jmol;

import cseo.jodaf.client.FilePackage;

public class Search extends JPanel {
	private static final long serialVersionUID = 7887252066467721114L;
	
	private JTextField txtText = new JTextField();
	private JTextField txtElements = new JTextField();
	private JTextField txtNot = new JTextField();
	private JTextField txtVolumeMin = new JTextField();
	private JTextField txtVolumeMax = new JTextField();
	private JTextField txtNumberMin = new JTextField();
	private JTextField txtNumberMax = new JTextField();
	private JTextField txtSpaceGroup = new JTextField();
	
	private JTextField txtaMin = new JTextField();
	private JTextField txtaMax = new JTextField();
	private JTextField txtbMin = new JTextField();
	private JTextField txtbMax = new JTextField();
	private JTextField txtcMin = new JTextField();
	private JTextField txtcMax = new JTextField();
	private JTextField txtalphaMin = new JTextField();
	private JTextField txtalphaMax = new JTextField();
	private JTextField txtbetaMin = new JTextField();
	private JTextField txtbetaMax = new JTextField();
	private JTextField txtgammaMin = new JTextField();
	private JTextField txtgammaMax = new JTextField();

	private JButton btnSave = null;
	private JButton btnSearch = null;
	private JButton	btnJmol = new JButton("Export to Jmol");
	private JButton	btnGULP = new JButton("Export to GULP");
	private JButton	btnFireball = new JButton("Export to Fireball");
	private JScrollPane scrollPane = null;
	private JTable tblResult = null;
	private JTextArea txtQuery = null;
	public String workingDirectory = System.getProperty("user.home");

	private JRadioButton radcod = new JRadioButton("cod");
	private JRadioButton radpcod = new JRadioButton("pcod");
	
	public Search(){
//		, PhysChemRequestBox physChemRequestBox) {
//		pChemBox = physChemRequestBox;
//		if(pChemBox!=null)
//		workingDirectory = pChemBox.getWorkingDirectory();

		setLayout(new GridBagLayout());
		
		ButtonGroup group = new ButtonGroup();
		group.add(radcod);
		group.add(radpcod);
		radcod.setSelected(true);
		
		final GridBagConstraints btnConstraints = new GridBagConstraints();
		JLabel lblDatabase = new JLabel("Choose Database");
		btnConstraints.gridwidth = 2;
		btnConstraints.gridx = 6;
		btnConstraints.gridy = 0;
		add(lblDatabase, btnConstraints);
		btnConstraints.gridwidth = 1;
		btnConstraints.gridy = 1;
		add(radcod, btnConstraints);
		btnConstraints.gridx = 7;
		add(radpcod, btnConstraints);
		btnConstraints.ipady = -7;
		btnConstraints.gridx = 6;
		btnConstraints.gridy = 2;
		add(getBtnSearch(), btnConstraints);
		btnConstraints.gridx = 7;
		add(getBtnSave(), btnConstraints);
		btnConstraints.gridwidth = 2;
		btnConstraints.gridx = 6;
		btnConstraints.gridy = 3;
		add(btnJmol, btnConstraints);
		btnConstraints.gridy = 4;
		add(btnGULP, btnConstraints);
		btnConstraints.gridy = 5;
		add(btnFireball, btnConstraints);
		
		btnJmol.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				try {
					if (tblResult.getSelectedRow() == -1) {
						JOptionPane.showMessageDialog(null, "Please select a structure to view.");
						return;
					}
					Jmol jmol = Jmol.getJmol(new JFrame(), 640, 480, "");
					String db = "cod";
					if (radpcod.isSelected())
						db = "pcod";
					final String fileName = "http://fireball.phys.wvu.edu/cod/" + db + "/" + fileNumbers[tblResult.getSelectedRow()] + ".cif";
					
					StringBuffer contents=Main.getFileContents(fileName);
					
					//parse it and generate atoms
					CifParser cp = new CifParser(contents.toString());
					cp.parseCoordinates("_atom_site_fract_x");
					cp.parseOperators();
					cp.removeDuplicates();
					
					ArrayList<String> spec;
					ArrayList<double[]> coor;
					if (cp.newSpecies.size() == 0)
						spec = cp.species;
					else
						spec = cp.newSpecies;
					if (cp.newCoordinates.size() == 0)
						coor = cp.coordinates;
					else
						coor = cp.newCoordinates;
					
					//generate xyz file
					StringBuffer sb = new StringBuffer();
					sb.append(spec.size() + "\n\n");
					for (int j=0; j < spec.size(); j++) {
						sb.append(spec.get(j));
						double[] d = coor.get(j);
						for (int k=0; k < d.length; k++) {
							sb.append("\t" + d[k]);
						}
						sb.append("\n");
					}
					
					//write to disk, open Jmol, and delete temporary file
					File temp = new File(System.getProperty("user.home") + "/" + System.nanoTime() + ".xyz");
					FileWriter fw = new FileWriter(temp);
					fw.write(sb.toString());
					fw.close();
					jmol.viewer.openFile(temp.getPath());
					temp.deleteOnExit();
				} catch (HeadlessException e1) {
					e1.printStackTrace();
				} catch (FileNotFoundException e1) {
					e1.printStackTrace();
				} catch (Exception e1) {
					e1.printStackTrace();
				}
			}
		});
		btnGULP.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				ArrayList<String[]> args = new ArrayList<String[]>();

				int[] indices = tblResult.getSelectedRows();
				if (indices.length == 0) {
					JOptionPane.showMessageDialog(null, "Please select one or more structures to export.");
					return;
				}
				String fileName = null;
				String db = "cod";
				if (radpcod.isSelected())
					db = "pcod";
				
				ArrayList<ArrayList<String>> species = new ArrayList<ArrayList<String>>();
				ArrayList<ArrayList<double[]>> coordinates = new ArrayList<ArrayList<double[]>>();
				ArrayList<String> names = new ArrayList<String>();
				
				for (int i=0; i < indices.length; i++) {
					try {
						//download file
						fileName = "http://fireball.phys.wvu.edu/cod/" + db + "/" + fileNumbers[indices[i]] + ".cif";
						StringBuffer contents=Main.getFileContents(fileName);
						names.add(fileNumbers[indices[i]]);
						//System.out.println(fileName);
						
						//parse it and generate atoms
						CifParser cp = new CifParser(contents.toString());
						cp.parseCoordinates("_atom_site_fract_x");
						cp.parseOperators();
						cp.removeDuplicates();
						
						//add parameters
						String[] params = new String[7];
						for (int j=1; j < params.length; j++)
							params[j] = "" + tblResult.getValueAt(indices[i], j-1);
						args.add(params);
						
						if (cp.newSpecies.size() == 0)
							species.add(cp.species);
						else
							species.add(cp.newSpecies);
						if (cp.newCoordinates.size() == 0)
							coordinates.add(cp.coordinates);
						else
							coordinates.add(cp.newCoordinates);
					} catch (FileNotFoundException e1) {
						JOptionPane.showMessageDialog(null, db + " does not contain a cif file for this entry (" + fileName+").  Please try another.");
						e1.printStackTrace();
					} catch (Exception e2) {
						JOptionPane.showMessageDialog(null, db + "Error encountered while processing " + fileName);
						e2.printStackTrace();
					}
				}
				//open GULP
				JavaGULP.main(species, coordinates, args, names);
			}
		});
		btnFireball.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				ArrayList<String[]> args = new ArrayList<String[]>();

				int[] indices = tblResult.getSelectedRows();
				if (indices.length == 0) {
					JOptionPane.showMessageDialog(null, "Please select one or more structures to export.");
					return;
				}
				String fileName = null;
				String db = "cod";
				if (radpcod.isSelected())
					db = "pcod";
				
				ArrayList<String> filenames = new ArrayList<String>();
				ArrayList<ArrayList<String>> species = new ArrayList<ArrayList<String>>();
				ArrayList<ArrayList<double[]>> coordinates = new ArrayList<ArrayList<double[]>>();
				
				for (int i=0; i < indices.length; i++) {
					try {
						filenames.add(fileNumbers[indices[i]]);
						
						//download file
						fileName = "http://fireball.phys.wvu.edu/cod/" + db + "/" + fileNumbers[indices[i]] + ".cif";
						StringBuffer contents=Main.getFileContents(fileName);
						//System.out.println(fileName);
						
						//parse it and generate atoms
						CifParser cp = new CifParser(contents.toString());
						cp.parseCoordinates("_atom_site_fract_x");
						cp.parseOperators();
						cp.removeDuplicates();
						
						//add parameters
						String[] params = new String[6];
						for (int j=0; j < params.length; j++)
							params[j] = "" + tblResult.getValueAt(indices[i], j);
						args.add(params);
						
						if (cp.newSpecies.size() == 0)
							species.add(cp.species);
						else
							species.add(cp.newSpecies);
						if (cp.newCoordinates.size() == 0)
							coordinates.add(cp.coordinates);
						else
							coordinates.add(cp.newCoordinates);
					} catch (FileNotFoundException e1) {
						JOptionPane.showMessageDialog(null, db + " does not contain a cif file for this entry (" + fileName+").  Please try another.");
						e1.printStackTrace();
					} catch (Exception e2) {
						JOptionPane.showMessageDialog(null, db + "Error encountered while processing " + fileName);
						e2.printStackTrace();
					}
				}
				//open Fireball
				JavaFireball.main(filenames, species, coordinates, args);
			}
		});

		
		scrollPane = new JScrollPane();
		final GridBagConstraints scrollConstraints = new GridBagConstraints();
		scrollConstraints.fill = GridBagConstraints.BOTH;
		scrollConstraints.gridx = 0;
		scrollConstraints.gridy = 6;
		scrollConstraints.gridwidth = 9;
		scrollConstraints.weightx = 1.0;
		scrollConstraints.weighty = 1.0;
		add(scrollPane, scrollConstraints);

		txtQuery = new JTextArea();
		txtQuery.setLineWrap(true);
		txtQuery.setText("SELECT * FROM data ORDER BY entry LIMIT 1000");
		final GridBagConstraints queryConstraints = new GridBagConstraints();
		queryConstraints.fill = GridBagConstraints.BOTH;
		queryConstraints.gridy = 0;
		queryConstraints.gridx = 8;
		queryConstraints.gridheight = 6;
		add(txtQuery, queryConstraints);

		getTable();

		final GridBagConstraints labelConstraints = new GridBagConstraints();
		labelConstraints.gridx = 3;
		labelConstraints.gridwidth = 1;

		JLabel lblA = new JLabel("a");
		JLabel lblB = new JLabel("b");
		JLabel lblC = new JLabel("c");
		JLabel lblAlpha = new JLabel("alpha");
		JLabel lblBeta = new JLabel("beta");
		JLabel lblGamma = new JLabel("gamma");
		JLabel lblText = new JLabel("Text");
		JLabel lblElements = new JLabel("Elements");
		JLabel lblNot = new JLabel("Not Elements");
		JLabel lblVolume = new JLabel("Cell Volume");
		JLabel lblNumber = new JLabel("# of Elements");
		labelConstraints.gridy = 0;
		add(lblA, labelConstraints);
		labelConstraints.gridy = 1;
		add(lblB, labelConstraints);
		labelConstraints.gridy = 2;
		add(lblC, labelConstraints);
		labelConstraints.gridy = 3;
		add(lblAlpha, labelConstraints);
		labelConstraints.gridy = 4;
		add(lblBeta, labelConstraints);
		labelConstraints.gridy = 5;
		add(lblGamma, labelConstraints);
		labelConstraints.gridx = 0;
		labelConstraints.gridy = 0;
		add(lblText, labelConstraints);
		labelConstraints.gridy = 1;
		add(lblElements, labelConstraints);
		labelConstraints.gridy = 2;
		add(lblNot, labelConstraints);
		labelConstraints.gridy = 3;
		add(lblVolume, labelConstraints);
		labelConstraints.gridy = 4;
		add(lblNumber, labelConstraints);

		final GridBagConstraints txt1Constraints = new GridBagConstraints();
		txt1Constraints.gridwidth = 1;
		txt1Constraints.fill = GridBagConstraints.HORIZONTAL;

		txtText.addKeyListener(generateQuery);
		txtElements.addKeyListener(generateQuery);
		txtNot.addKeyListener(generateQuery);
		txtVolumeMin.addKeyListener(generateQuery);
		txtVolumeMax.addKeyListener(generateQuery);
		txtNumberMin.addKeyListener(generateQuery);
		txtNumberMax.addKeyListener(generateQuery);
		txtSpaceGroup.addKeyListener(generateQuery);

		txt1Constraints.gridwidth = 1;
		JLabel lblSpaceGroup = new JLabel("Space Group");
		txt1Constraints.gridx = 0;
		txt1Constraints.gridy = 5;
		add(lblSpaceGroup, txt1Constraints);
		txt1Constraints.gridwidth = 2;
		txt1Constraints.gridx = 1;
		txt1Constraints.gridy = 0;
		txt1Constraints.ipadx = 50;
		add(txtText, txt1Constraints);
		txt1Constraints.gridy = 1;
		add(txtElements, txt1Constraints);
		txt1Constraints.gridy = 2;
		add(txtNot, txt1Constraints);
		txt1Constraints.gridwidth = 1;
		txt1Constraints.gridy = 3;
		add(txtVolumeMin, txt1Constraints);
		txt1Constraints.gridx = 2;
		add(txtVolumeMax, txt1Constraints);
		txt1Constraints.gridx = 1;
		txt1Constraints.gridy = 4;
		add(txtNumberMin, txt1Constraints);
		txt1Constraints.gridx = 2;
		txt1Constraints.gridy = 4;
		add(txtNumberMax, txt1Constraints);
		txt1Constraints.gridx = 1;
		txt1Constraints.gridy = 5;
		txt1Constraints.gridwidth = 2;
		add(txtSpaceGroup, txt1Constraints);
		
		final GridBagConstraints txt2Constraints = new GridBagConstraints();
		txt2Constraints.gridwidth = 1;
		txt2Constraints.ipadx = 50;

		txtaMin.addKeyListener(generateQuery);
		txtaMax.addKeyListener(generateQuery);
		txtbMin.addKeyListener(generateQuery);
		txtbMax.addKeyListener(generateQuery);
		txtcMin.addKeyListener(generateQuery);
		txtcMax.addKeyListener(generateQuery);
		txtalphaMin.addKeyListener(generateQuery);
		txtalphaMax.addKeyListener(generateQuery);
		txtbetaMin.addKeyListener(generateQuery);
		txtbetaMax.addKeyListener(generateQuery);
		txtgammaMin.addKeyListener(generateQuery);
		txtgammaMax.addKeyListener(generateQuery);

		txt2Constraints.gridx = 4;
		txt2Constraints.gridy = 0;
		add(txtaMin, txt2Constraints);
		txt2Constraints.gridy = 1;
		add(txtbMin, txt2Constraints);
		txt2Constraints.gridy = 2;
		add(txtcMin, txt2Constraints);
		txt2Constraints.gridy = 3;
		add(txtalphaMin, txt2Constraints);
		txt2Constraints.gridy = 4;
		add(txtbetaMin, txt2Constraints);
		txt2Constraints.gridy = 5;
		add(txtgammaMin, txt2Constraints);
		txt2Constraints.gridx = 5;
		txt2Constraints.gridy = 0;
		add(txtaMax, txt2Constraints);
		txt2Constraints.gridy = 1;
		add(txtbMax, txt2Constraints);
		txt2Constraints.gridy = 2;
		add(txtcMax, txt2Constraints);
		txt2Constraints.gridy = 3;
		add(txtalphaMax, txt2Constraints);
		txt2Constraints.gridy = 4;
		add(txtbetaMax, txt2Constraints);
		txt2Constraints.gridy = 5;
		add(txtgammaMax, txt2Constraints);

	}

	private JButton getBtnSearch() {
		if (btnSearch == null) {
			btnSearch = new JButton();
			btnSearch.setText("Search");
			btnSearch.addMouseListener(new MouseAdapter() {
				public void mouseClicked(MouseEvent e) {
					int numColumns = getTable();
					try {
						Class.forName("com.mysql.jdbc.Driver");
						String db = "cod";
						if (radpcod.isSelected())
							db = "pcod";
						String url = "jdbc:mysql://fireball.phys.wvu.edu:3306/" + db;
						Connection con = DriverManager.getConnection(url);
						Statement stmt = con.createStatement();
						ResultSet rs = stmt.executeQuery(txtQuery.getText());
						int row = 0;
						while (rs.next()) {
							fileNumbers[row] = "" + rs.getObject(2);
							for (int i = 1; i <= numColumns; i++)
								tblResult.setValueAt(rs.getObject(i+3), row, i-1);
							row++;
						}
						rs.close();
						stmt.close();
						con.close();
					} catch (Exception ex) {
						System.out.println(ex.getMessage());
						System.out.println(ex.toString());
						ex.printStackTrace();
					}
				}
			});
		}
		return btnSearch;
	}
	String[] fileNumbers;

	private int getTable() {
		String temp, query = txtQuery.getText();
		int length = 1, number = 1000;
		do {
			temp = query.substring(query.length() - length, query.length() - length + 1);
			length++;
		} while (temp.matches("\\d"));
		number = Integer.parseInt(query.substring(query.length() - length + 2));
		try {
			scrollPane.remove(tblResult);
		} catch (NullPointerException npe) {
		}
		String word = txtQuery.getText();
		int endIndex = word.indexOf("FROM") - 1;
		word = word.substring(7, endIndex);
		String[] words;
		if (word.equals("*"))
			words = new String[] {"a", "b", "c", "alpha", "beta", "gamma", "vol", "nel", "sg", "formula", "text"};
		else
			words = word.split(", ");
		fileNumbers = new String[number];
		tblResult = new JTable(number, words.length);
		tblResult.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
		for (int i=0; i < words.length; i++){
			tblResult.getColumnModel().getColumn(i).setHeaderValue(words[i]);
			if (words[i].equals("formula"))
				tblResult.getColumnModel().getColumn(i).setPreferredWidth(250);
			if (words[i].equals("text"))
				tblResult.getColumnModel().getColumn(i).setPreferredWidth(2500);
		}
		scrollPane.setViewportView(tblResult);
		return words.length;
	}

	ArrayList<String> separateWords(String s, char delimiter){
		ArrayList<String> words = new ArrayList<String>();
		int index = -1;
		boolean newWord = true;
		for (int i = 0; i < s.length(); i++) {
			if (s.charAt(i) == delimiter)
				newWord = true;
			else {
				if (newWord) {
					newWord = false;
					words.add("");
					index++;
				}
				words.set(index, words.get(index) + s.substring(i, i + 1));
			}
		}
		return words;
	}
	KeyAdapter generateQuery = new KeyAdapter(){
		@Override
		public void keyReleased(KeyEvent e){
			String query = "SELECT * FROM data WHERE";
			if (!txtText.getText().equals("")) {
				ArrayList<String> words = separateWords(txtText.getText(), ' ');
				for (String word: words){
					query += " AND (text LIKE '% " + word + " %')";
				}
			}
			if (!txtSpaceGroup.getText().equals("")) {
				ArrayList<String> words = separateWords(txtSpaceGroup.getText(), ' ');
				for (String word: words){
					query += " AND (sg LIKE '% " + word + " %')";
				}
			}
			if (!txtElements.getText().equals("")) {
				ArrayList<String> elements = separateWords(txtElements.getText(), ' ');
				for (String element: elements){
					query += " AND (formula LIKE '% " + element + " %')";
				}
			}
			if (!txtNot.getText().equals("")) {
				ArrayList<String> elements = separateWords(txtNot.getText(), ' ');
				for (String element: elements){
					query += " AND (formula NOT LIKE '% " + element + " %')";
				}
			}
			try {
				query += between(txtVolumeMin, txtVolumeMax, "vol");
				query += between(txtNumberMin, txtNumberMax, "nel");
				query += between(txtaMin, txtaMax, "a");
				query += between(txtbMin, txtbMax, "b");
				query += between(txtcMin, txtcMax, "c");
				query += between(txtalphaMin, txtalphaMax, "alpha");
				query += between(txtbetaMin, txtbetaMax, "beta");
				query += between(txtgammaMin, txtgammaMax, "gamma");
				query = query.replace("WHERE AND", "WHERE");
			} catch (NumberFormatException nfe) {
				JOptionPane.showMessageDialog(null, "Please enter numbers in the numeric fields.");
			}
			if (query.endsWith(" WHERE"))
				query = "SELECT * FROM data";
			query += " ORDER BY entry LIMIT 1000";
			txtQuery.setText(query);
		}
	};
	private String between(JTextField box1, JTextField box2, String field) {
		String line = "", one = box1.getText(), two = box2.getText();
		if (!one.equals("")) {
			Double.parseDouble(one);
			if (!two.equals("")) {
				Double.parseDouble(two);
				line += " AND (" + field + " BETWEEN " + one + " AND " + two + ")";
			} else {
				line += " AND (" + field + " >= " + one + ")";
			}
		} else if (!two.equals("")) {
			Double.parseDouble(two);
			line += " AND (" + field + " <= " + two + ")";
		}
		return line;
	}
	private JButton getBtnSave() {
		if (btnSave == null) {
			btnSave = new JButton();
			btnSave.setText("Save");
			btnSave.addMouseListener(new MouseAdapter() {
				public void mouseClicked(MouseEvent e) {
//					if (Main.reqboxLocal == null) {
						JFileChooser file = new JFileChooser();
						file.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
						file.setDialogTitle("Choose a directory in which to save.");
						if (JFileChooser.APPROVE_OPTION == file.showSaveDialog(null)) {
							int[] indices = tblResult.getSelectedRows();
							String db = "cod";
							if (radpcod.isSelected())
								db = "pcod";
							for (int i=0; i < indices.length; i++) {
								String fileName = "http://fireball.phys.wvu.edu/cod/" + db + "/" + fileNumbers[indices[i]] + ".cif";
								File f = new File(file.getSelectedFile().getPath() + "/" + fileNumbers[indices[i]] + ".cif");
								try {
									StringBuffer contents = Main.getFileContents(fileName);
									FileOutputStream fos = new FileOutputStream(f);
									fos.write(contents.toString().getBytes());
									fos.close();
								} catch (FileNotFoundException e1) {
									JOptionPane.showMessageDialog(null, "Cannot find " + fileName);
									e1.printStackTrace();
								} catch (IOException e1) {
									e1.printStackTrace();
								}
							}
							
						}
//					} else {
//						int[] indices = tblResult.getSelectedRows();
//						FilePackage[] fp = new FilePackage[indices.length];
//						String db = "cod";
//						if (radpcod.isSelected())
//							db = "pcod";
//						for (int i=0; i < indices.length; i++) {
//							fp[i] = new FilePackage(null, "*.cif");
//							StringBuffer contents = null;
//							String fileName = null;
//							try {
//								fileName = "http://fireball.phys.wvu.edu/cod/" + db + "/" + fileNumbers[indices[i]] + ".cif";
//								contents = Main.getFileContents(fileName);
//							} catch (FileNotFoundException fnfe) {
//								JOptionPane.showMessageDialog(null, db + " does not contain a cif file for this entry (" + fileName+").  Please try another.");
//								fnfe.printStackTrace();
//							}
//							fp[i].setByteArray(contents.toString().getBytes());
//						}
//						Main.reqboxLocal.fileSaveToDirectoryDialog(fp);
//					}
				}
			});
		}
		return btnSave;
	}
}