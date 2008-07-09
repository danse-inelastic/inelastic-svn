// a table example

function headcell( s )
{
  return $( '<td>' + s + '</td>' );
}


function make_test_table_3( thetable ) {
  
  thead = $(thetable.children( 'thead' )[0]);
  thead.append( $( '<tr></tr>' ) );

  headrow = $(thead.children( 'tr' )[0]);
  
  headrow.append( headcell( 'A' ) );
  headrow.append( headcell( 'B' ) );
  headrow.append( headcell( 'C' ) );


  thetable.table_setcolumndescriptors
    ( { name: 'A', datatype: 'money'},
      { name: 'B', datatype: 'money'},
      { name: 'C', datatype: 'money'}
      ) ;

  for (var i=0; i<10; i++) {
    var a = Math.floor( Math.random() * 3000 )/100.;
    var b = Math.floor( Math.random() * 3000 )/100.;
    var c = a+b;
    thetable.table_addrow_dataonly (a,b,c);
  }
  
}
