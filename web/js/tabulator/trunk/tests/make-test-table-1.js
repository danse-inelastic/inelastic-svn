// a table example

function add_headcell( descriptor, headrow, descriptors )
{
  id = descriptor.id;
  text = descriptor.text;
  
  cell = $( '<td id="' + id + '">' + text + '</td>' );
  headrow.append( cell );
  descriptors[ id ] = descriptor;
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
  
  descriptors = {};
  add_headcell
    ( { id: 'sales_col', text: 'Sales', datatype: 'upanddown' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'title_col', text: 'Title', datatype: 'text' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'author_col', text: 'Author', datatype: 'text' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'price_col', text: 'Price', datatype: 'money' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'in_store_col', text: 'In Store', datatype: 'boolean' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'shipping_col', text: 'Shipping', datatype: 'single_choice', choices: shipping_choices }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'bestseller_col', text: 'Bestseller', datatype: 'single_choice_in_one_column' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'date_col', text: 'Date of Publication', datatype: 'date', valid_range: [ '01/01/1970', '01/01/2010' ] }, 
      headrow, descriptors );

  thetable.table_setcolumndescriptors( descriptors );

}

function make_test_table_1( thetable ) {
  
  make_table_head( thetable );

  thetable.table_addrow_dataonly
    (-1500, "abcdefghijk", 'Some author 1', 12.99, 1, 3, 0, "12/01/1991");
  thetable.table_addrow_dataonly
    (1000, "QWERCVBF", 'Some author 2', 0, 1, 3, 0, "01/01/1992");
  thetable.table_addrow_dataonly
    (-100, "Boris Godunov", 'Alexandr Pushkin', 7.15, 1, 1, 0, "10/30/1995");
  thetable.table_addrow_dataonly
    (-200, "The Rainmaker", 'John Grisham', 7.99, 0, 4, 0, "01/01/2005");
  thetable.table_addrow_dataonly
    (350, "The Green Mile", 'Stephen King', 11.10, 1, 3, 0, "12/01/2001");
  thetable.table_addrow_dataonly
    (700, "Misery", 'Stephen King', 7.70, 0, 0, 1, "10/15/2001");
  thetable.table_addrow_dataonly
    (-1200, "The Dark Half", 'Stephen King', 0, 0, 4, 0, "05/01/1998");
  thetable.table_addrow_dataonly
    (1500, "The Partner", 'John Grisham', 12.99, 1, 4, 0, "01/01/1999");
  thetable.table_addrow_dataonly
    (500, "It", 'Stephen King', 9.70, 0, 0, 0, "03/15/1980");
  thetable.table_addrow_dataonly
    (400, "Cousin Bette", 'Honore de Balzac', 0, 1, 1, 0, "04/01/2007");  

}
