$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_2( thetable );

    // format table
    thetable.format_table_cells_by_class();

    // make some cols sortable
    var thead = thetable.find( 'thead' );
    
    thetable.sort_table_by_col( 3, 0 );
    var price = thead.find( 'td:contains("Price")' );
    price.attr( 'direction', 0 );

    price.click( function () {
	$this = $(this);
	direction = $this.attr( 'direction' );
	direction = direction == 0? 1:0;

	thetable.sort_table_by_col( 3, direction );

	$this.attr('direction', direction);
      } );


    thetable.sort_table_by_col( 1, 0 );
    var book = thead.find( 'td:contains("Book")' );
    book.attr( 'direction', 0 );

    book.click( function () {
	$this = $(this);
	direction = $this.attr( 'direction' );
	direction = direction == 0? 1:0;

	thetable.sort_table_by_col( 1, direction );

	$this.attr('direction', direction);
      } );
    /*
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
    */
  });
