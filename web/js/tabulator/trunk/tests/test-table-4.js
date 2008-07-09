// test the following methods:
//   - table_addrow
//   - sort_table_by_col


$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    thetable.sort_table_by_col( 3, 0 );

    $('#priceup').click( function () {
	thetable.sort_table_by_col( 3, 1 );
      } );
  });
