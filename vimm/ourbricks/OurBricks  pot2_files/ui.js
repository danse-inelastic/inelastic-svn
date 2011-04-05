
function showVideo(){
    html = '<div id="show_video_div" style="color:black;border=0"><iframe src="/video.html" width="1040" height="620" frameBorder="0"></iframe></div>';
    var video_div = $(html).appendTo($('body'));
    $.fancybox({
	    'scrolling': 'no',
		'titleShow': false,
		'href': "#show_video_div",
		'onClosed': function() { video_div.remove(); }
	});
}

var g_showLoginActive = false;      /// yikes, guard against multiple logins thrown by fileuploader with multiple files
function showLogin(){
    if (g_showLoginActive) return;
    loginshown = true;
    g_showLoginActive = true;
    html = '<div id="signin_div" style="color:black"><iframe src="/signup" width="750" height="420" frameBorder="0"></iframe></div>';
    var signin_div = $(html).appendTo($('body'));
    g_showLoginSync = true;
    $.fancybox({
	    'scrolling': 'no',
		'titleShow': false,
		'href': "#signin_div",
    	'onClosed': function() { signin_div.remove(); g_showLoginActive=false}
//        'onClosed': function() { location.reload(true); }
	});
}
