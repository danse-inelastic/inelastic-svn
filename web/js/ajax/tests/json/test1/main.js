$(document).ready(function() {
    var button = $("#clickme");
    
    button.click( function () {
	$.getJSON("main.cgi", function(json){
	    alert("JSON Data: " + json.hello);
	  })
	  });
  });
