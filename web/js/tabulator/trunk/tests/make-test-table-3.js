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

  thead = $(thetable.children( 'thead' )[0]);
  thead.append( $( '<tr></tr>' ) );
  headrow = $(thead.children( 'tr' )[0]);
  
  descriptors = {};
  add_headcell
    ( { id: 'columnA', text: 'A', datatype: 'money' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'columnB', text: 'B', datatype: 'money' }, 
      headrow, descriptors );
  add_headcell
    ( { id: 'columnC', text: 'C', datatype: 'money' }, 
      headrow, descriptors );

  thetable.table_setcolumndescriptors( descriptors );

}


function make_test_table_3( thetable ) {
  
  make_table_head( thetable );

  for (var i=0; i<10; i++) {
    var a = Math.floor( Math.random() * 3000 )/100.;
    var b = Math.floor( Math.random() * 3000 )/100.;
    var c = a+b;
    thetable.table_appendrow_dataonly (i, [a,b,c]);
  }
  
}
