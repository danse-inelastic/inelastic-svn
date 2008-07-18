// a table example

function make_table_head( thetable ) {

  thead = $(thetable.children( 'thead' )[0]);
  headrow = $(thead.children( 'tr' )[0]);
  
  descriptors = { 
    'columnA': {text: 'A', datatype: 'money' }, 
    'columnB': {text: 'B', datatype: 'money' }, 
    'columnC': {text: 'C', datatype: 'money' }
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


function make_form() {
  return $( '<form> </form>' );
}


function make_test_table( div ) {
  
  // make the table skeleton
  thetable = make_table_skeleton();

  form = make_form();
  form.append( thetable );

  // add table skeleton to div
  div.append( form );

  
  // table contents
  make_table_head( thetable );

  for (var i=0; i<10; i++) {
    var a = Math.floor( Math.random() * 3000 )/100.;
    var b = Math.floor( Math.random() * 3000 )/100.;
    var c = a+b;
    thetable.table_appendrow_dataonly (i, [a,b,c]);
  }
  
}
