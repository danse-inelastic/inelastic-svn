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
    ( { content: 'Sales'},
      { content: 'Book'},
      { content: 'Author'},
      { content: 'Price'},
      { content: 'In Store'},
      { content: 'Shipping'},
      { content: 'Bestseller'}
      ) ;

  thetable.table_addcolumndescriptors
    ( { name: 'Sales', klass: 'upanddown'},
      { name: 'Book', klass: 'text'},
      { name: 'Author', klass: 'text'},
      { name: 'Price', klass: 'money'},
      { name: 'In Store', klass: 'boolean'},
      { name: 'Shipping', klass: 'single_choice', choices: shipping_choices},
      { name: 'Bestseller', klass: 'single_choice_in_one_column'}
      ) ;

  var N = 50;

  for (var i = 0; i < N; i++ ) {
    
    var sales = Math.floor( Math.random() * 100 ) - Math.floor(100/2);
    var price = Math.floor( Math.random() * 3000 )/100.;
    var shipping = Math.floor( Math.random() * 6 );
    
    thetable.table_addrow_dataonly( sales, 'a book', "an author", price, 1, shipping, 0 );
    ;
  }

}
