// -*- JavaScript -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                         (C) 2008 All Rights Reserved  
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


// tabulator


// some meta data are saved in cells to allow sorting, formatting.
// some other meta data are stored in table.
// column_descriptors is a piece of meta data that is saved in table.


(function($) {

  // ********************************************
  //  public methods added to jQuery
  // ********************************************

  // ---------------------
  // table meta data setup
  // ---------------------

  // set column descriptors for a table
  // a column descriptor describe the properties of a column, such
  // as name, type, sorting direction? 
  $.fn.table_setcolumndescriptors = function () {
    $(this).data( 'column_descriptors', arguments );
  };



  // ---------------------
  // table manipulations
  // ---------------------

  // sort a table by a column
  // this -> table
  $.fn.sort_table_by_col = function( colno, direction ) {

    // save rows before we remove them from the table
    var saverows = [];
    var body = get_tablebody( this );
    var rows = body.children();
    for (var i = 0; i<rows.length; i++) {
      row = rows[i];
      saverows.push( row );
    }
    body.empty();
    var newrows = sort_rows_by_col( saverows, colno, direction );
    
    for (var i=0; i<newrows.length; i++) {
      body.append( newrows[i] );
    }
  };
  

  // make a cell editable
  $.fn.enable_cell_editing = function () {
    enable_cell_editing_by_datatype( this );

    // when cell lost focus, we should quit editing mode

    //  "input" or "select"?
    var input = this.children( 'input' );
    if (input.length == 0) input = this.children( 'select' );

    //  focus on input now
    input.focus();
    
    //  blur --> quit editing
    var cell  = this;
    input.blur( function() {
	cell.restore_cell_from_editing();
      } );
  };

  
  // restore a cell from editable to normal
  $.fn.restore_cell_from_editing = function () {
    restore_cell_from_editing_by_datatype( this );
  }
  

  // extract data value from a cell
  $.fn.extract_data_from_cell = function () {
    cell = this;
    datatype = cell.attr( 'datatype' );
    var handler = eval( '$.fn.extract_data_from_cell.handle_' + datatype );
    return handler( cell );
  };


  // establish a cell given a new value
  $.fn.establish_cell_from_data = function( data ) {
    cell = this;
    datatype = cell.attr( 'datatype' );
    var handler = eval( '$.fn.establish_cell_from_data.handle_' + datatype );
    return handler( cell, data );
  };


  // get value from an editing widget for a cell
  $.fn.cell_value_from_editing_widget = function() {
    cell = this;
    datatype = cell.attr( 'datatype' );
    var handler = eval( '$.fn.cell_value_from_editing_widget.handle_' + datatype );
    return handler( cell );
  };


  // ---------------------
  // basic table creation
  // ---------------------

  // add a row to table body. only the data are specified. meta data 
  // will be obtained from "column_descriptors" that is attached to the table
  $.fn.table_addrow_dataonly = function() {
    var data = arguments;
    var tbl = this;

    var ncells = data.length;
    
    var column_descriptors = tbl.data( 'column_descriptors' );

    row = append_newrow_to_table( ncells, tbl );
    cells = row.children( 'td' );
    
    for (var i=0; i<data.length; i++) {
      var descriptor = column_descriptors[i];
      var datatype = descriptor.datatype;
      var value = data[i];
      cell = $(cells[i]);
      cell.attr( 'datatype', datatype );
      cell.establish_cell_from_data( value );
    }

  };


  // ********************************************
  // handlers
  // These handlers can be extended so that the
  // behaviors of this tabulator can be changed
  // ********************************************


  // --------------------------------------
  // handlers to extract data from a cell
  // --------------------------------------
  // text
  $.fn.extract_data_from_cell.handle_text = function( cell ) {
    return cell.text();
  };
  
  // money
  $.fn.extract_data_from_cell.handle_money = function( cell ) {
    text = cell.text();
    if (text.substring(0,1) == '$') text = text.substring(1, text.length);
    return Number( text );
  };
  
  // --------------------------------------
  // handlers to establish a cell from data
  // --------------------------------------
  //  text
  $.fn.establish_cell_from_data.handle_text = function( cell, value ) {
    return cell.text( value ); 
  };
  
  //  boolean
  $.fn.establish_cell_from_data.handle_boolean = function( cell, value ) {
    var checked = Number(value)==0? '':'checked="checked"';
    var html = '<input type="checkbox" ' + checked + ' />';
    return cell.html( html ); 
  };
  
  //  money
  $.fn.establish_cell_from_data.handle_money = function( cell, value ) {
    text = '$ ' + value;
    cell.text( text );
    return cell.css("color", "green");
  };

  //  updown
  $.fn.establish_cell_from_data.handle_upanddown = function( cell, value ) {
    cell.text( value );
    if (value > 0) 
      return cell.css("color", "green").prepend( '^' );
    else
      return cell.css("color", "red").prepend( 'v' );
  };

  // single_choice
  $.fn.establish_cell_from_data.handle_single_choice = function( cell, value ) {
    column_descriptor = get_column_descriptor( cell );
    choices = column_descriptor.choices;
    text = choices[ value ];
    cell.text( text );
    return cell;
  };  

  //  single choice in one column
  $.fn.establish_cell_from_data.handle_single_choice_in_one_column = function( cell, value ) {
    var html = '<input type="radio" ';
    var checked = Number(value)==0? '':'checked="checked"';
    html += checked;
    html += 'name="' + cell.attr('name') + '"';
    html += '/>';
    return cell.html( html ); 
  };

  

  // -----------------------------
  // handlers to compare two cells
  // -----------------------------
  //  money
  $.fn.sort_table_by_col.handle_money = function( value1, value2 ) {
    return value1 - value2;
  };

  //  text
  $.fn.sort_table_by_col.handle_text = function( value1, value2 ) {
    return value1.substring(0,1) < value2.substring(0,1)? -1: 1;
  };

  // **** need more compare handlers here
  

  // --------------------------------
  // handlers to make a cell editable
  // --------------------------------
  //  text
  $.fn.enable_cell_editing.handle_text = function( cell ) {
    var text = cell.text();
    var width = cell.width();
    var height = cell.height();
    var html = '<input type="text" value ="' + text + '" />'; 
    cell.html( html );
    var input = cell.children('input');
    input.width( width );
    input.height( height );
  };

  //  money
  $.fn.enable_cell_editing.handle_money = function( cell ) {
    var text = cell.text();
    if (text.substring(0,1) == '$') text = text.substring(1, text.length);

    var width = cell.width();
    var height = cell.height();
    var html = '<input type="text" value ="' + text + '" />'; 
    
    cell.html( html );
    var input = cell.children('input')
    input.width( width );
    input.height( height );
  };

  //  single_choice
  $.fn.enable_cell_editing.handle_single_choice = function( cell ) {
    var text = cell.text();
    var width = cell.width();
    var height = cell.height();
    var choices = cell.data( 'choices' );
    if (choices == undefined) {
      descriptor = get_column_descriptor( cell );
      choices = descriptor.choices;
    }
    
    var options = [];
    
    for (var index in choices) {
      var choice = choices[index];
      var  opt = {'value': index, 'text': choice}
      if (choice == text) opt.selected = 'selected';
      options.push( opt );
    }

    var dl = dropdownlist( options );

    cell.html( dl );

    select = cell.children('select');
    select.width( width );
    select.height( height-2 );
  };

  // dropdownlist( [ {'value': "volvo", 'text': "Volvo"}, ... ] )
  function dropdownlist( options ) {
    var select = document.createElement( 'select' );

    for (var i=0; i<options.length; i++) {
      var opt = document.createElement( 'option' );
      var opt_info = options[i];
      $(opt).attr('value', opt_info.value);
      $(opt).text(opt_info.text);
      if (opt_info.selected) $(opt).attr('selected', 'selected');
      $(select).append( opt );
    } 
    
    return select;
  }


  // ---------------------------------------------
  // handlers to extract value from editing widget
  // ---------------------------------------------
  //  text
  $.fn.cell_value_from_editing_widget.handle_text = function( cell ) {
    return cell.find( "input" ).attr( 'value' );
  };

  //  money
  $.fn.cell_value_from_editing_widget.handle_money = function( cell ) {
    return cell.find( "input" ).attr( 'value' );
  };

  //  single_choice
  $.fn.cell_value_from_editing_widget.handle_single_choice = function( cell ) {
    var select = cell.find( "select" );
    return select.attr('value');
  };


  // ********************************************
  // implementation details
  // ********************************************


  // append a row with empty cells to the table
  function append_newrow_to_table( ncells, table ) {
    var tbody = get_tablebody( table );

    nrows = tbody.children( 'tr' ).length;
    row = new_row( nrows, ncells );
    tbody.append( row );
    return row;
  }


  // find the parent table
  function find_parent_table( element ) {
    return $( element.parents( 'table' )[0] );
  }


  // get column descriptor of a cell
  function get_column_descriptor( cell ) {
    table = find_parent_table( cell );
    colno = Number(cell.attr( 'colno' ));
    descriptors = table.data('column_descriptors');
    return descriptors[ colno ];
  }
  

  // enable editing for a cell according to the cell's datatype
  function enable_cell_editing_by_datatype( cell ) {
    var datatype = cell.attr('datatype');
    var handler = eval( "$.fn.enable_cell_editing.handle_" + datatype );
    handler( cell );
  }


  // restore cell from editing status according to the cell's datatype
  function restore_cell_from_editing_by_datatype( cell ) {
    value = cell.cell_value_from_editing_widget();
    cell.establish_cell_from_data( value );
  }


  // create a new row with empty cells
  function new_row(rowno, n) {
    
    // new row
    var tr = document.createElement( 'tr' );

    for (i=0; i<n; i++) {

      cell = $( document.createElement( 'td' ) );
      cell.attr( 'rowno', rowno );
      cell.attr( 'colno', i );

      $(tr).append(cell);

    }
    
    return $(tr);
  }

  
  function get_tablehead( table ) {
    var theads = table.children( 'thead' );
    var lastthead = theads[ theads.length - 1 ];
    return $(lastthead);
  }

  function get_tablebody( table ) {
    var tbodys = table.children( 'tbody' );
    var lasttbody = tbodys[ tbodys.length - 1 ];
    return $(lasttbody);
  }

  // sort given rows by a column. The column number is given.
  function sort_rows_by_col( rows, colno, direction ) {
    function compare (row1, row2) {
      var cells1 = $(row1).children('td');
      var cells2 = $(row2).children('td');

      var cell1 = $(cells1[colno]);
      var datatype1 = cell1.attr('datatype');
      var value1 = cell1.extract_data_from_cell();

      var cell2 = $(cells2[colno]);
      var datatype2 = cell2.attr('datatype');
      var value2 = cell2.extract_data_from_cell();
      
      // ****** shall we assert datatypes are matched? *******
      var handler = eval( "$.fn.sort_table_by_col.handle_" + datatype1 );
      
      return handler( value1, value2 );
    }
    rows.sort( compare );
    if (direction!=0) rows.reverse();
    return rows;
  }

 }) (jQuery);


// version
// $Id$

// End of file 
