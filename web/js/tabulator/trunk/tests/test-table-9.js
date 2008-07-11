$(document).ready(function() {

    Date.firstDayOfWeek = 7;
    Date.format = 'mm/dd/yyyy';

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    thetable.find( 'tbody' ).find( "td[datatype=text]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    thetable.find( 'tbody' ).find( "td[datatype=money]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    thetable.find( 'tbody' ).find( "td[datatype=single_choice]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

    thetable.find( 'tbody' ).find( "td[datatype=date]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );

  });
