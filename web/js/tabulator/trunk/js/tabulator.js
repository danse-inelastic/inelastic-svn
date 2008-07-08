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

// meta data are saved in cells to allow sorting, formatting.

(function($) {

  // ********************************************
  //  public methods added to jQuery
  // ********************************************
  

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
    enable_cell_editing_by_class( this );

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
    restore_cell_from_editing_by_class( this );
  }
  

  // add decorations to a cell
  $.fn.format_cell = function() {
    format_cell_by_class( this );
  };

  
  // add decorations to cells by cell classes
  $.fn.format_table_cells_by_class = function () {
    format_cells_by_class( this );
    return this;
  };
  

  // ---------------------
  // basic table creation
  // ---------------------

  // add a row to table head
  $.fn.table_addheadrow = function () {
    var thead = get_tablehead( this );
    nrows = thead.children( 'row' ).length;
    row = new_row_raw( nrows, arguments );
    $(thead).append( row );
  };


  // add column descriptors for a table
  // a column descriptor describe the properties of a column, such
  // as name, type, sorting direction? 
  $.fn.table_addcolumndescriptors = function () {
    $(this).data( 'column_descriptors', arguments );
  };


  // add a row to table body
  $.fn.table_addrow = function () {
    append_row_to_table( arguments, this );
    return this;
  };

  
  // add a row to table body. only the data are specified. meta data 
  // will be obtained from "column_descriptors"
  $.fn.table_addrow_dataonly = function() {
    var data = arguments;
    var tbl = this;

    var cells = [];
    
    var column_descriptors = tbl.data( 'column_descriptors' );

    for (var i=0; i<data.length; i++) {
      var descriptor = column_descriptors[i];
      var klass = descriptor.klass;
      var cell = { 'content': data[i], 'klass': klass };
      cells.push( cell );
    }
    
    append_row_to_table( cells, tbl );
  };


  // ********************************************
  // handlers
  // These handlers can be extended so that the
  // behaviors of this tabulator can be changed
  // ********************************************

  // -----------------------------
  // handlers to compare two cells
  // -----------------------------
  //  money
  $.fn.sort_table_by_col.handle_money = function( cell1text, cell2text ) {
    if (cell1text.substring(0,1) == '$') cell1text = cell1text.substring(1, cell1text.length+1);
    if (cell2text.substring(0,1) == '$') cell2text = cell2text.substring(1, cell2text.length+1);
    return Number( cell1text ) - Number( cell2text );
  };

  //  text
  $.fn.sort_table_by_col.handle_text = function( cell1text, cell2text ) {
    return cell1text.substring(0,1) < cell2text.substring(0,1)? -1: 1;
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


  // --------------------------------------------------------------
  // handlers to restore a cell from editable state to normal state
  // --------------------------------------------------------------
  //  text
  $.fn.restore_cell_from_editing.handle_text = function( cell ) {
    var value = cell.find( "input" ).attr( 'value' );
    cell.text( value );
  };

  //  money
  $.fn.restore_cell_from_editing.handle_money = function( cell ) {
    var value = cell.find( "input" ).attr( 'value' );
    cell.text( '$' + value );
  };

  //  single_choice
  $.fn.restore_cell_from_editing.handle_single_choice = function( cell ) {
    var select = cell.find( "select" );
    var value = select.attr('value');
    column_descriptor = get_column_descriptor( cell );
    choices = column_descriptor.choices;
    text = choices[ value ];
    cell.text( text );
  };


  // -------------------------
  // handlers to format a cell
  // -------------------------
  //  text
  $.fn.format_cell.handle_text = function( cell ) {
  };

  //  boolean
  $.fn.format_cell.handle_boolean = function( cell ) {
    var value = cell.text();
    var checked = Number(value)==0? '':'checked="checked"';
    var html = '<input type="checkbox" ' + checked + ' />';
    return cell.html( html ); 
  };
  
  //  money
  $.fn.format_cell.handle_money = function( cell ) {
    if (cell.text().substring(0,1) != '$') cell = cell.prepend( '$' );
    return cell.css("color", "green");
  };

  //  updown
  $.fn.format_cell.handle_upanddown = function( cell ) {
    if (Number(cell.text()) > 0) 
      return cell.css("color", "green").prepend( '^' );
    else
      return cell.css("color", "red").prepend( 'v' );
  };

  // single_choice
  $.fn.format_cell.handle_single_choice = function( cell ) {
    text = cell.text();
    column_descriptor = get_column_descriptor( cell );
    choices = column_descriptor.choices;
    text = choices[ text ];
    cell.text( text );
    return cell;
  };  

  //  single choice in one column
  $.fn.format_cell.handle_single_choice_in_one_column = function( cell ) {
    var value = cell.text();
    var html = '<input type="radio" ';
    var checked = Number(value)==0? '':'checked="checked"';
    html += checked;
    html += 'name="' + cell.attr('name') + '"';
    html += '/>';
    return cell.html( html ); 
  };

  

  // ********************************************
  // implementation details
  // ********************************************


  // append a row to the table
  function append_row_to_table( cells, table ) {
    var tbody = get_tablebody( table );

    nrows = tbody.children( 'row' ).length;
    row = new_row_raw( nrows, cells );
    tbody.append( row );
  }


  // find the parent table
  function find_parent_table( element ) {
    return $( element.parents( 'table' )[0] );
  }


  // get column descriptor of a cell
  function get_column_descriptor( cell ) {
    table = find_parent_table( cell );
    colno = cell.attr( 'colno' );
    return table.data('column_descriptors')[ colno ];
  }
  
  // format a cell according to its class
  function format_cell_by_class( cell ) {
    var klass = cell.attr('class');
    var handler = eval( "$.fn.format_cell.handle_" + klass );
    handler( cell );
  }


  // format each cell in a table according to the cell's class
  function format_cells_by_class( table ) {
    var tbody = get_tablebody( table );
    $(tbody).find( 'td' ).each( function(i) {
	$(this).format_cell();
      } );
  }


  // enable editing for a cell according to the cell's class
  function enable_cell_editing_by_class( cell ) {
    var klass = cell.attr('class');
    var handler = eval( "$.fn.enable_cell_editing.handle_" + klass );
    handler( cell );
  }


  // restore cell from editing status according to the cell's class
  function restore_cell_from_editing_by_class( cell ) {
    var klass = cell.attr('class');
    var handler = eval( "$.fn.restore_cell_from_editing.handle_" + klass );
    handler( cell );
  }


  // create a new row with given cells
  function new_row_raw(rowno, cells) {
    
    // new row
    var tr = document.createElement( 'tr' );

    // add all cells. each argument correspond to a cell
    for (i=0; i<cells.length; i++) {

      var cell = cells[i];

      var td = document.createElement( 'td' );
      td.innerHTML = cell.content;

      // class
      std = $(td);
      std.addClass( cell.klass );
      //std.attr( 'name', cell.name );
      std.attr( 'colno', i );
      std.attr( 'rowno', rowno );

      $(tr).append(td);

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
      var klass1 = cell1.attr('class');
      var cell1text = cell1.text();

      var cell2 = $(cells2[colno]);
      var klass2 = cell2.attr('class');
      var cell2text = cell2.text();
      
      // ****** shall we assert classes are matched? *******
      var handler = eval( "$.fn.sort_table_by_col.handle_" + klass1 );
      
      return handler( cell1text, cell2text );
    }
    rows.sort( compare );
    if (direction!=0) rows.reverse();
    return rows;
  }

 }) (jQuery);


// version
// $Id$

// End of file 
