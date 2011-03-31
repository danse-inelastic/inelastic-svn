// test the following methods:
//   - table_addrow
//   - enable_cell_editing

$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    thetable.format_table_cells_by_class();
    
    thetable.find( "td:contains('Honore')" ).enable_cell_editing( );

  });
