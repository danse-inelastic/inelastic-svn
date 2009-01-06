$(document).ready(function() {
    var button = $("#clickme");
    var textfield = $("#textfield");

    button.click
      (function () 
       {
	 $.getJSON
	   ("main.cgi", 
	    function(json) {textfield.text(json.text);}
	    );
       }
       );
  });
