// test the following methods:
//   - table_addrow
//   - table_addheadrow

$(document).ready(function() {

    var table1 = $('#table1');

    table1.table_addheadrow
      ( { content: 'name', klass: 'identifier'},
	{ content: 'salary', klass: 'money'} 
	) ;

    table1.table_addrow( 'williams', 50000.00 );

    $(".money").css("background", "lightgreen");

  });
