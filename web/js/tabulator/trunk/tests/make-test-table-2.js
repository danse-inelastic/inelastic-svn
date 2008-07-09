// a table example

function headcell( s )
{
  return $( '<td>' + s + '</td>' );
}

function make_test_table_2( thetable ) {
  
  var shipping_choices =  {
  0: 'na',
  1: "1 Hour",
  2: "12 Hours",
  3: "24 Hours",
  4: "2 days",
  5: "1 week"
  };

  thead = $(thetable.children( 'thead' )[0]);
  headrow = $(thead.children( 'tr' )[0]);
  
  headrow.append( headcell( 'Sales' ) );
  headrow.append( headcell( 'Book' ) );
  headrow.append( headcell( 'Author' ) );
  headrow.append( headcell( 'Price' ) );
  headrow.append( headcell( 'In Store' ) );
  headrow.append( headcell( 'Shipping' ) ); 
  headrow.append( headcell( 'Bestseller' ) );


  thetable.table_setcolumndescriptors
    ( { name: 'Sales', datatype: 'upanddown'},
      { name: 'Book', datatype: 'text'},
      { name: 'Author', datatype: 'text'},
      { name: 'Price', datatype: 'money'},
      { name: 'In Store', datatype: 'boolean'},
      { name: 'Shipping', datatype: 'single_choice', choices: shipping_choices},
      { name: 'Bestseller', datatype: 'single_choice_in_one_column'}
      ) ;

  var N = 30;
  var BestSeller = Math.floor( Math.random() * N );

  for (var i = 0; i < N; i++ ) {
    
    var sales = Math.floor( Math.random() * 100 ) - Math.floor(100/2);
    var price = Math.floor( Math.random() * 3000 )/100.;
    var shipping = Math.floor( Math.random() * 6 );
    var title = randSentence( 3, 10 );
    var author = randSentence( 2, 8 );
    var instore = Math.floor( Math.random() * 2 );
    thetable.table_addrow_dataonly
      ( sales, title, author, price, instore, shipping, i==BestSeller );
    ;
  }

}


function randSentence(  maxnumberofwords, maxnumberofcharactersperword )
{
  var words = randWords(  maxnumberofwords, maxnumberofcharactersperword );

  var sentence = "";

  for ( var i=0; i<words.length; i++ ) {
    sentence += words[i];
    if (i<words.length-1) sentence += ' ';
  }
  
  return sentence;
}


function randWords( maxnumberofwords, maxnumberofcharactersperword )
{
  var nword = Math.floor( Math.random() * (maxnumberofwords-1) ) + 1;
  var words = [];

  for (var i=0; i<nword; i++) {
    words.push( randWord( maxnumberofcharactersperword ) );
  }
  
  return words;
}


function randWord( maxlength ) {
  var characters = "0123456789"
    + "ABCDEFGHIJKLMNOPQRSTUVWXTZ"
    + "abcdefghiklmnopqrstuvwxyz";
  
  var length = Math.floor( Math.random() * (maxlength-1) ) + 1;

  var word="";

  for (var j=0;j<length;j++) {
    var rand = Math.floor(Math.random() * characters.length);
    word += characters.substring(rand,rand+1);
  }

  return word;
}
