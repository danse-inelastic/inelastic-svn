$(document).ready(function() {

    var thetable = $('#thetable');

    thetable.table_addheadrow
      ( { content: 'Sales', klass: 'upanddown'},
	{ content: 'Book', klass: 'text'},
	{ content: 'Author', klass: 'text'},
	{ content: 'Price', klass: 'money'},
	{ content: 'In Store', klass: 'boolean'},
	{ content: 'Shipping', klass: 'shipping_time'},
	{ content: 'Bestseller', klass: 'single_choice'}
	) ;

    thetable.table_addrow(-1500, "A Time to Kill", 'John Grisham', 
			  '$12.99', 1, 24, 0);
    thetable.table_addrow(1000, "Blood and Smoke", 'Stephen King', 
			  0, 1, 24, 0);
    thetable.table_addrow(-100, "Boris Godunov", 'Alexandr Pushkin', 
			  7.15, 1, 1, 0);
    thetable.table_addrow(-200, "The Rainmaker", 'John Grisham', 
			  7.99, 0, 48, 0);
    thetable.table_addrow(350, "The Green Mile", 'Stephen King', 
			  11.10, 1, 24, 0);
    thetable.table_addrow(700, "Misery", 'Stephen King', 
			  7.70, 0, 'na', 1);
    thetable.table_addrow(-1200, "The Dark Half", 'Stephen King', 
			  0, 0, 48, 0);
    thetable.table_addrow(1500, "The Partner", 'John Grisham', 
			  12.99, 1, 48, 0);
    thetable.table_addrow(500, "It", 'Stephen King', 
			  9.70, 0, 'na', 0);
    thetable.table_addrow(400, "Cousin Bette", 'Honore de Balzac', 
			  0, 1, 1, 0);

    thetable.format_table_cells_by_class();
    
    thetable.find( "td:contains('Honore')" ).enable_cell_editing( );
  });
