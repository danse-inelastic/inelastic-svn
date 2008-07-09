$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_3( thetable );


    var callback = function (cell) {
      
      b = cell.extract_data_from_cell();

      rowno = Number( cell.attr('rowno') );
      tbody = cell.parents( 'tbody' )[0];

      acell = findcell( tbody, 0, rowno );
	
      a = acell.extract_data_from_cell();

      c = a+b;

      ccell = findcell( tbody, 2, rowno );
      ccell.establish_cell_from_data( c );

    };

    thetable.find( 'tbody' ).find( "td[datatype=money][colno=1]" ).dblclick( function () {
	$(this).enable_cell_editing(  callback  );
      } );

  });


function findcell( container, colno, rowno ) { 
  s = "td[colno='" + colno + "'][rowno='" + rowno + "']" ;
  return $(container).find( s );
}
