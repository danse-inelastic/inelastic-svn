// test the following methods:
//   - table_addrow
//   - sort_table_by_col
// test features
//   - remember and toggle sorting direction


$(document).ready(function() {

    var thetable = $('#thetable');

    make_test_table_1( thetable );

    
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
    var booktitle = thead.find( 'td:contains("Title")' );
    booktitle.attr( 'direction', 0 );

    booktitle.click( function () {
	$this = $(this);
	direction = $this.attr( 'direction' );
	direction = direction == 0? 1:0;

	thetable.sort_table_by_col( 1, direction );

	$this.attr('direction', direction);
      } );

    $('.red').css( 'color', 'red' );
  });
