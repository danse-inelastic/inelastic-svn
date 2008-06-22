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
  $.fn.sort_table_by_col = function( column_name, direction ) {

    colno = get_colno( this, column_name );

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
    var input = this.children( 'input' );
    input.focus();
    var cell  = this;
    input.blur( function() {
	cell.restore_cell_from_editing();
      } );
  };

  
  // restore a cell from editable to normal
  $.fn.restore_cell_from_editing = function () {
    restore_cell_from_editing_by_class( this );
  }
  

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
    row = new_row_raw( arguments );
    $(thead).append( row );
  };

  // add a row to table body
  $.fn.table_addrow = function () {
    
    var tbody = get_tablebody( this );

    // explicitly formatted cells
    var arg0 = arguments[0];
    if (arg0.klass != undefined ) {
      row = new_row_raw( arguments );
      tbody.append( row );
    }
    // implicitly formatted cells
    else {
      var template = row_template_from_headrow( this );
      var row = new_row_from_template( template, arguments );
      tbody.append( row );
    }
    return this;
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

  // **** need more compare handlers here
  

  // --------------------------------
  // handlers to make a cell editable
  // --------------------------------
  //  text
  $.fn.enable_cell_editing.handle_text = function( cell ) {
    var text = cell.text();
    var width = cell.width();
    var html = '<input type="text" value ="' + text + '" />'; 
    cell.html( html );
    cell.children('input').width( width-1 );
  };


  // --------------------------------------------------------------
  // handlers to restore a cell from editable state to normal state
  // --------------------------------------------------------------
  //  text
  $.fn.restore_cell_from_editing.handle_text = function( cell ) {
    var value = cell.find( "input" ).attr( 'value' );
    cell.text( value );
  };


  // -------------------------
  // handlers to format a cell
  // -------------------------
  //  boolean
  $.fn.format_table_cells_by_class.format_boolean_cell = function( cell ) {
    var value = cell.text();
    var checked = Number(value)==0? '':'checked="checked"';
    var html = '<input type="checkbox" ' + checked + ' />';
    return cell.html( html ); 
  };
  
  //  money
  $.fn.format_table_cells_by_class.format_money_cell = function( cell ) {
    if (cell.text().substring(0,1) != '$') cell = cell.prepend( '$' );
    return cell.css("color", "green");
  };

  //  updown
  $.fn.format_table_cells_by_class.format_upanddown_cell = function( cell ) {
    if (Number(cell.text()) > 0) 
      return cell.css("color", "green").prepend( '^' );
    else
      return cell.css("color", "red").prepend( 'v' );
  };

  //  shipping_time
  $.fn.format_table_cells_by_class.format_shipping_time_cell = function( cell ) {
    var text = cell.text();
    if (text == 'na' || text == 'NA') return cell;
    var hours = Number(text);
    if (hours > 24 && hours % 24 == 0) return cell.text( hours/24 + " days" );
    if (hours == 1) return cell.text( "1 Hour" );
    return cell.text( hours+" Hours" );
  };

  //  single choice
  $.fn.format_table_cells_by_class.format_single_choice_cell = function( cell ) {
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

  
  // format each cell in a table according to the cell's class
  function format_cells_by_class( table ) {
    var tbody = get_tablebody( table );

    tbody.find( '.boolean' ).each( function(i){ 
        $.fn.format_table_cells_by_class.format_boolean_cell($(this));
      } );

    tbody.find( '.money' ).each( function(i){
        $.fn.format_table_cells_by_class.format_money_cell($(this));
      } );

    tbody.find( '.upanddown' ).each( function(i){
        $.fn.format_table_cells_by_class.format_upanddown_cell($(this));
      } );

    tbody.find( '.shipping_time' ).each( function(i){
        $.fn.format_table_cells_by_class.format_shipping_time_cell($(this));
      } );

    tbody.find( '.single_choice' ).each( function(i){
        $.fn.format_table_cells_by_class.format_single_choice_cell($(this));
      } );

  }


  // enable editing for a cell according to the cell's class
  function enable_cell_editing_by_class( cell ) {
    var klass = cell.attr('class');
    eval( "var handler = $.fn.enable_cell_editing.handle_" + klass + ";" );
    handler( cell );
  }


  // restore cell from editing status according to the cell's class
  function restore_cell_from_editing_by_class( cell ) {
    var klass = cell.attr('class');
    eval( "var handler = $.fn.restore_cell_from_editing.handle_" + klass + ";" );
    handler( cell );
  }


  // create a new row with given cells
  function new_row_raw(cells) {
    
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
      std.attr( 'name', cell.name );
      // may add more props here

      $(tr).append(td);

    }
    
    return $(tr);
  }

  function new_row_from_template(template, values) {

    if (template.length != values.length) {
      // how do I throw an error?
      return;
    }

    var cells = [];

    for (var i = 0; i < template.length; i++) {
      var value = values[i];
      var col = $(template[i]);
      cells.push( { content: value, klass: col.attr('class'), name: col.text() } );
    }
    
    return new_row_raw( cells );
  }

  
  function row_template_from_headrow( table ) {
    var theads = table.children( 'thead' );
    var lastthead = theads[ theads.length - 1 ];
    var rows = $(lastthead).children( 'tr' );
    var lastrow = rows[ rows.length - 1 ];
    return $(lastrow).children();
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

  // find out col number given column name
  function get_colno( table, colname ) {
    var thead = get_tablehead( table );
    var rows = $(thead).children( 'tr' );
    var lastrow = rows[ rows.length - 1 ];
    var cells = $(lastrow).children( 'td' );
    for (var i = 0; i<cells.length; i++ ) {
      var cell = cells[i];
      if ( $(cell).text() == colname ) {
	return i;
      } 
    }
    return "not found";    
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
      eval( "var handler = $.fn.sort_table_by_col.handle_" + klass1 + ";" );
      
      return handler( cell1text, cell2text );
    }
    rows.sort( compare );
    if (direction!=0) rows.reverse();
    return rows;
  }

 }) (jQuery);
