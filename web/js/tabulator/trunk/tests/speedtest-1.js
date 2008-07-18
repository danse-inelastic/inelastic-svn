$(document).ready(function() {

    var div = $('#table');
    make_test_table( div );

    thetable = div.find( 'table' );

    // make some cols sortable
    var thead = thetable.find( 'thead' );
    
    thetable.sort_table_by_col( "price_col", 0 );
    var price = thead.find( 'td:contains("Price")' );
    price.attr( 'direction', 0 );

    price.click( function () {
	$this = $(this);
	direction = $this.attr( 'direction' );
	direction = direction == 0? 1:0;

	thetable.sort_table_by_col( "price_col", direction );

	$this.attr('direction', direction);
      } );


    thetable.sort_table_by_col( "title_col", 0 );
    var book = thead.find( 'td:contains("Book")' );
    book.attr( 'direction', 0 );

    book.click( function () {
	$this = $(this);
	direction = $this.attr( 'direction' );
	direction = direction == 0? 1:0;

	thetable.sort_table_by_col( "title_col", direction );

	$this.attr('direction', direction);
      } );
    /*
    
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
