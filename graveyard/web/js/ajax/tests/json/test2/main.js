$(document).ready(function() {
    var button = $("#clickme");
    button.click
      (function () 
       {
	 var textfield = $("#textfield");
	 var data = {"text": textfield.text()};

	 $.getJSON
	   ("main.cgi", 
	    data,
	    function(json) {textfield.text(json.text);}
	    );
       }
       );
  });
