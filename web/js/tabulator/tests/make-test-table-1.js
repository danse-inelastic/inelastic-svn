// a table example

function make_test_table_1( thetable ) {
  
  var shipping_choices =  {
  0: 'na',
  1: "1 Hour",
  2: "12 Hours",
  3: "24 Hours",
  4: "2 days",
  5: "1 week"
  };

  thetable.table_addheadrow
    ( { content: 'Sales', klass: 'upanddown'},
      { content: 'Book', klass: 'text'},
      { content: 'Author', klass: 'text'},
      { content: 'Price', klass: 'money'},
      { content: 'In Store', klass: 'boolean'},
      { content: 'Shipping', klass: 'single_choice', choices: shipping_choices},
      { content: 'Bestseller', klass: 'single_choice_in_one_column'}
      ) ;

  thetable.table_addrow(-1500, "abcdefghijk", 'Some author 1', 
			'$12.99', 1, 3, 0);
  thetable.table_addrow(1000, "QWERCVBF", 'Some author 2', 
			0, 1, 3, 0);
  thetable.table_addrow(-100, "Boris Godunov", 'Alexandr Pushkin', 
			7.15, 1, 1, 0);
  thetable.table_addrow(-200, "The Rainmaker", 'John Grisham', 
			7.99, 0, 4, 0);
  thetable.table_addrow(350, "The Green Mile", 'Stephen King', 
			11.10, 1, 3, 0);
  thetable.table_addrow(700, "Misery", 'Stephen King', 
			7.70, 0, 0, 1);
  thetable.table_addrow(-1200, "The Dark Half", 'Stephen King', 
			0, 0, 4, 0);
  thetable.table_addrow(1500, "The Partner", 'John Grisham', 
			12.99, 1, 4, 0);
  thetable.table_addrow(500, "It", 'Stephen King', 
			9.70, 0, 0, 0);
  thetable.table_addrow(400, "Cousin Bette", 'Honore de Balzac', 
			0, 1, 1, 0);  
}
