// test the following methods:
//   - table_addrow
//   - table_addheadrow

$(document).ready(function() {

    var table1 = $('#table1');

    table1.table_addheadrow
      ( { content: 'name'},
	{ content: 'salary'} 
	) ;

    table1.table_addcolumndescriptors
      ( { name: 'name', klass: 'identifier'},
	{ name: 'salary', klass: 'money'} 
	) ;

    table1.table_addrow_dataonly( 'williams', 50000.00 );

    $(".money").css("background", "lightgreen");

  });
