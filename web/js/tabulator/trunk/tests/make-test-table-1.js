// a table example

function make_form() {
  return $( '<form> </form>' );
}


function make_table_skeleton( ) {
  
  table = $( '<table border="1"></table>' );
  
  thead = $( '<thead></thead' );
  table.append(thead);
  
  headrow = $( '<tr></tr>' );
  thead.append( headrow );

  tbody = $( '<tbody></tbody>' );
  table.append( tbody );
  
  return table;
}


function make_table_head( thetable ) {

  var shipping_choices =  {
  0: 'na',
  1: "1 Hour",
  2: "12 Hours",
  3: "24 Hours",
  4: "2 days",
  5: "1 week"
  };

  thead = $(thetable.children( 'thead' )[0]);
  headrow = $(thead.children( 'tr' )[0]);
  
  descriptors = {
    'sales_col': { text: 'Sales', datatype: 'upanddown' }, 
    'title_col': { text: 'Title', datatype: 'text' }, 
    'author_col': { text: 'Author', datatype: 'text' }, 
    'price_col': { text: 'Price', datatype: 'money' }, 
    'in_store_col': { text: 'In Store', datatype: 'boolean' },
    'shipping_col': { text: 'Shipping', datatype: 'single_choice', choices: shipping_choices },
    'bestseller_col': { text: 'Bestseller', datatype: 'single_choice_in_one_column' }, 
    'date_col': { text: 'Date of Publication', datatype: 'date', valid_range: [ '01/01/1970', '01/01/2010' ] }
  }

  establish_headrow_from_column_descriptors( headrow, descriptors );
  thetable.table_setcolumndescriptors( descriptors );

}


function add_headcell( id, text, headrow )
{
  cell = $( '<td id="' + id + '">' + text + '</td>' );
  headrow.append( cell );
}


function establish_headrow_from_column_descriptors( headrow, descriptors )
{
  for (var colid in descriptors) {
    descriptor = descriptors[ colid ];
    add_headcell( colid, descriptor.text, headrow );
  }
}



function make_test_table_1( div ) {
  
  // table skeleton
  thetable = make_table_skeleton();

  // add table to a form
  form = make_form();
  form.append( thetable );
  
  // add form to the division
  div.append( form );
  

  // contents of table
  // head
  make_table_head( thetable );
  // body rows
  thetable.table_appendrow_dataonly
    (0, [-1500, "abcdefghijk", 'Some author 1', 12.99, 1, 3, 0, "12/01/1991"]);
  thetable.table_appendrow_dataonly
    (1, [1000, "QWERCVBF", 'Some author 2', 0, 1, 3, 0, "01/01/1992"]);
  thetable.table_appendrow_dataonly
    (2, [-100, "Boris Godunov", 'Alexandr Pushkin', 7.15, 1, 1, 0, "10/30/1995"]);
  thetable.table_appendrow_dataonly
    (3, [-200, "The Rainmaker", 'John Grisham', 7.99, 0, 4, 0, "01/01/2005"]);
  thetable.table_appendrow_dataonly
    (4, [350, "The Green Mile", 'Stephen King', 11.10, 1, 3, 0, "12/01/2001"]);
  thetable.table_appendrow_dataonly
    (5, [700, "Misery", 'Stephen King', 7.70, 0, 0, 1, "10/15/2001"]);
  thetable.table_appendrow_dataonly
    (6, [-1200, "The Dark Half", 'Stephen King', 0, 0, 4, 0, "05/01/1998"]);
  thetable.table_appendrow_dataonly
    (7, [1500, "The Partner", 'John Grisham', 12.99, 1, 4, 0, "01/01/1999"]);
  thetable.table_appendrow_dataonly
    (8, [500, "It", 'Stephen King', 9.70, 0, 0, 0, "03/15/1980"]);
  thetable.table_appendrow_dataonly
    (9, [400, "Cousin Bette", 'Honore de Balzac', 0, 1, 1, 0, "04/01/2007"]);  
}

