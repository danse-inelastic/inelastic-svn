// test the following methods:
//   - table_addrow
//   - table_addheadrow

$(document).ready(function() {

    var table1 = $('#table1');

    thead = $(table1.children( 'thead' )[0]);
    headrow = $(thead.children( 'tr' )[0]);

    headrow.append('<td>name</td>');
    headrow.append('<td>salary</td>');

    table1.table_setcolumndescriptors
      ( { name: 'name', datatype: 'text'},
	{ name: 'salary', datatype: 'money'} 
	) ;

    table1.table_addrow_dataonly( 'williams', 50000.00 );

    $("td[datatype=money]").css("background", "#AAFFFF");

  });
