// test the following methods:
//   - table_addrow
//   - format_table_cells_by_class


$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    thetable.format_table_cells_by_class();
    
  });
