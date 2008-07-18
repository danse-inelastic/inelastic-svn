$(document).ready(function() {

    var div = $('#table');
    make_test_table( div );

    
    thetable = div.find( 'table' );
    
    var callback = function (cell) {
      
      colAid = 'columnA';
      colBid = 'columnB';
      colCid = 'columnC';
      
      b = cell.extract_data_from_cell();

      rowid = Number( cell.parent().attr('rowid') );
      tbody = cell.parents( 'tbody' )[0];

      acell = findcell( tbody, colAid, rowid );
	
      a = acell.extract_data_from_cell();

      c = a+b;

      ccell = findcell( tbody, colCid, rowid );
      ccell.establish_cell_from_data( c );

    };

    thetable.find( 'tbody' ).find( "td[datatype=money][colid=columnB]" ).dblclick( function () {
	$(this).enable_cell_editing(  callback  );
      } );

  });


function findcell( container, colid, rowid ) { 
  srow = "tr[rowid='" + rowid + "']";
  scol = "td[colid='" + colid + "']";
  return $(container).find( srow ).find(scol);
}
