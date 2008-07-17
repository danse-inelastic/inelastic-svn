$(document).ready(function() {

    var div = $('#table');
    make_test_table_1( div );

    thetable = div.find( 'table' );

    thetable.find( 'tbody' ).find( "td[datatype=text]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    thetable.find( 'tbody' ).find( "td[datatype=money]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    thetable.find( 'tbody' ).find( "td[datatype=single_choice]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    $(".red").css( 'color', 'red' );

  });
