// a table example

function make_test_table_2( thetable ) {
  
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

  var N = 50;

  for (var i = 0; i < N; i++ ) {
    
    var sales = Math.floor( Math.random() * (N+1) ) - Math.floor(N/2);
    var price = Math.floor( Math.random() * (N+1) ) / 100.;
    var shipping = Math.floor( Math.random() * 6 );
    
    thetable.table_addrow( sales, 'a book', "an author", price, 1, shipping, 0 );
    ;
  }

}
