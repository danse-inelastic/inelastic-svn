// test the following methods:
//   - table_appendrow

function make_table_skeleton( ) {
  
  table = $( '<table border="1"></table>' );
  
  thead = $( '<thead></thead' );
  table.append(thead);
  
  headrow = $( '<tr></tr>' );
  thead.append( headrow );

  tbody = $( '<tbody></tbody>' );
  table.append( tbody );
  
  return table;
}

$(document).ready(function() {

    div = $( '#table' );
    
    table1 = make_table_skeleton();
    div.append( table1 );
    
    headrow = $(table1.children( 'thead' ).children('tr')[0] ); 
    headrow.append('<td id="name">name</td>');
    headrow.append('<td id="salary">salary</td>');

    table1.table_setcolumndescriptors
      ( { name: { id: 'name', datatype: 'text'},
	  salary: { id: 'salary', datatype: 'money'} }
	) ;

    table1.table_appendrow_dataonly( 0, ['williams', 50000.00] );

    $("td[datatype=money]").css("background", "#AAFFFF");

  });
