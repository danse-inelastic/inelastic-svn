// test the following methods:
//   - table_addrow
//   - sort_table_by_col
// test features
//   - remember and toggle sorting direction


$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    thetable.format_table_cells_by_class();

    
    var thead = thetable.find( 'thead' );
    
    thetable.sort_table_by_col( "Price", 0 );
    var price = thead.find( 'td:contains("Price")' );
    price.attr( 'direction', 0 );

    price.click( function () {
	$this = $(this);
	direction = $this.attr( 'direction' );
	direction = direction == 0? 1:0;

	thetable.sort_table_by_col( 'Price', direction );

	$this.attr('direction', direction);
      } );


    thetable.sort_table_by_col( "Book", 0 );
    var book = thead.find( 'td:contains("Book")' );
    book.attr( 'direction', 0 );

    book.click( function () {
	$this = $(this);
	direction = $this.attr( 'direction' );
	direction = direction == 0? 1:0;

	thetable.sort_table_by_col( 'Book', direction );

	$this.attr('direction', direction);
      } );
  });
