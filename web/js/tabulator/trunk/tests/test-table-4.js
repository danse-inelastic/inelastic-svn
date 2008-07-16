// test the following methods:
//   - sort_table_by_col


$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    thetable.sort_table_by_col( 'price_col', 1 );

    $('#priceup').click( function () {
	thetable.sort_table_by_col( 'price_col', 0 );
      } );
    
    $(".red").css( 'color', 'red' );
  });
