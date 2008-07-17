// test the following methods:
//   - enable_cell_editing

$(document).ready(function() {

    var div = $('#table');

    make_test_table_1( div );

    thetable.find( "td:contains('Honore')" ).enable_cell_editing( );

    $(".red").css( 'color', 'red' );
  });
