$(document).ready(function() {

    var table1 = $('#table1');

    table1.table_addrow
      ( { content: 'name', klass: 'identifier'},
	{ content: 'salary', klass: 'money'} 
	) ;

    table1.table_addrow
      ( { content: 'williams', klass: 'identifier'},
	{ content: '50000.00', klass: 'money'} 
	) ;

    $(".money").css("background", "lightgreen");

  });
