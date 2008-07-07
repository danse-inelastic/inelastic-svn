$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    thetable.format_table_cells_by_class();
    
    thetable.find( 'tbody' ).find( ".text" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    thetable.find( 'tbody' ).find( ".money" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    thetable.find( 'tbody' ).find( ".single_choice" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

  });
