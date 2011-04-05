var editToggleRotation;
var editToggleSkybox;
var editToggleSunbemas;
var editToggleShadows;
var createEditBox;
var showEditBox;
var showEmbed;
var embedSelectText;
var editSave;
var downloadArchive;
(function() {
    var sliderRez=1024;
    var powerBase=1.02;
    var powerScale=500;
    var g_groundPlaneHeight=-1.0e31;
    var g_scale=1.0;
    var groundPlaneMesh="collada/models/invground.dae";
    var useSunbeams=false;
    var useSkybox=false;
    var skybox=["skydome.png"];
    var extra;
    function normalizePosToZeroOne(value){
        return Math.log(value+1.0)/Math.log(powerBase)/powerScale;
    }
    function normalizeAnyToZeroOne(value){
        if (value>0)
            return normalizePosToZeroOne(value)*.5+.5;
        return .5-normalizePosToZeroOne(-value)*.5;
    }
    
    
    function reconstitutePosFromZeroOne(value){
        return Math.pow(powerBase,value*powerScale)-1.0;
        //if (value==1) value=1-1./sliderRez;
        //if (value==0) value=1./sliderRez;
        //return -Math.log(1-(1/(1-value)));
    }
    function reconstituteAnyFromZeroOne(value){
        if (value>.5)
            return reconstitutePosFromZeroOne((value-.5)*2);
        if (value==.5)
            return .5;
        return -reconstitutePosFromZeroOne(1.0-value*2);
    }
    function queryToggleValue(element_id){
        var ele = document.getElementById(element_id);
        if (!ele) {
            return false;
        }
        var curValue = ele.getElementsByTagName("div")[0];
        if (curValue.innerHTML.indexOf("On") == -1) {
            return false;
        }
        return true;
    }
    function getNewToggleValue(element_id,value) {
        var ele=document.getElementById(element_id);
        if (!ele) {
            return false;
        }
        var curValue=ele.getElementsByTagName("div")[0];
        if (value===undefined){
            if (curValue.innerHTML.indexOf("On")==-1){
                curValue.innerHTML="On";
                value=true;
            }else {
                curValue.innerHTML="Off";
                value=false;
            }
        }else {
            if (value) {
                curValue.innerHTML="On";
            }else {
                curValue.innerHTML="Off";
            }
        }
        return value;
    }
    editToggleRotation=function(value){
        var value=getNewToggleValue('edit_box_rotation',value);
        sendMessageToScript(new Kata.ScriptProtocol.ToScript.GUIMessage({
		    msg: "mouserot",
			event: {
			value: value
			    }
                   }));
	
    }
    editToggleSkybox=function(value){
        var value=getNewToggleValue('edit_box_skybox',value);
	useSkybox=value;
	sendMessageToScript(new Kata.ScriptProtocol.ToScript.GUIMessage({
		    msg:"skybox",
			event:{value:useSkybox?skybox:[],
			    sunbeams:useSunbeams}}));
    }
    editToggleSunbeams=function(value){
        var value=getNewToggleValue('edit_box_sunbeams',value);
	useSunbeams=value;
	sendMessageToScript(new Kata.ScriptProtocol.ToScript.GUIMessage({
		    msg:"skybox",
			event:{value:useSkybox?skybox:[],
			    sunbeams:useSunbeams}}));
    }
    
    editToggleShadows=function(value){
        var value=getNewToggleValue('edit_box_shadows',value);
	sendMessageToScript(new Kata.ScriptProtocol.ToScript.GUIMessage({
		    msg:"shadows",
			event:{value:value}}));
    }
    function getCurrentScale() {
	var retval=$("#edit_box_scale").slider("value")/sliderRez;
	if (retval==0)
	    retval=1./sliderRez;	
	return reconstitutePosFromZeroOne(retval);
    }
    function scaleUpdate(event,ui) {
        var value=getCurrentScale();
	g_scale=value;
	sendMessageToScript(new Kata.ScriptProtocol.ToScript.GUIMessage({
		    msg: "rescale",
			event: {
			value: value
			    }
                    }));
    }
    function sendMessageToScript(msg){
        document.getElementById('frame').contentWindow.postMessage(JSON.stringify(msg),'*');
    }
    function getGroundHeight(){
	return reconstituteAnyFromZeroOne($("#edit_box_ground_plane").slider("value")/sliderRez);
    }
    function groundUpdate(event,ui) {
        var value=getGroundHeight();
	g_groundPlaneHeight=value;
        sendMessageToScript(new Kata.ScriptProtocol.ToScript.GUIMessage({
                    msg: "groundHeight",
                        event: {
                        value: value,
                            mesh:groundPlaneMesh
                            }
        }));
    }
    parseCookie = function(c) {
	var cookie = null;
	var i = document.cookie.indexOf(c + "=");
	if (i >= 0) {
	    var cookie = document.cookie.substr(i + c.length+1);
	    var j = cookie.indexOf(";");
	    if (j >= 0) 
		cookie = cookie.substr(0, j);
	}
	return cookie
    }

    function publishNowFinish(msg) {
	//var i = Kata_codeRoot.indexOf("//") + 2
	//i += Kata_codeRoot.substr(i).indexOf("/") + 1
	var url = "/publish.py"//Kata_homeRoot.substr(0, i) + "publish.py";
	
	extra.url = msg.loadUrl;
	extra.mouse_rot=queryToggleValue('edit_box_rotation');
	extra.sunbeams=queryToggleValue('edit_box_sunbeams');
	if (queryToggleValue('edit_box_skybox'))
	    extra.skybox=skybox;
	else
	    extra.skybox=[];
	extra.scale=[g_scale,g_scale,g_scale];
	extra.shadows=queryToggleValue('edit_box_shadows');
	extra.groundMesh=groundPlaneMesh;
	extra.groundHeight=g_groundPlaneHeight;
	if (extra.groundHeight<-1000) {
	    delete extra.groundHeight;
	    delete extra.groundMesh;
	}
	extra.preview = 'false';
	extra.pos = msg.objPos;
	extra.orient = msg.objOrient;
	if (!extra.camera) {
	    extra.camera = {};
	}
	extra.camera.pos = msg.camPos;
	extra.camera.orient = msg.camOrient;
	
	extra.vertical_flip = 0;    
	if (navigator.userAgent.indexOf("Firefox/4.0b7") > -1) extra.vertical_flip = 1;
	if (navigator.userAgent.indexOf("Firefox/4.0b8") > -1) extra.vertical_flip = 1;
	if (navigator.userAgent.indexOf("Firefox/4.0b9") > -1) extra.vertical_flip = 1;
	if (navigator.userAgent.indexOf("Firefox/4.0b10") > -1) extra.vertical_flip = 1;
	
	extra.cookie = parseCookie("cookie_id");
	//extra.editpass = g_allowPreview;
	
	var data = JSON.stringify(extra);
	//console.log("publish cgi url:", url, "data:", data);
	
	var html = '<center><br>Saving scene...<br>';
	showVisibility(document.getElementById('save_pending'));
	var req = new XMLHttpRequest();
	if (req) {
	    req.onreadystatechange = function(){
		if (req.readyState == 4) {
		    if (req.status != 200) { //sorry, file:/// is dead; getting status 0 on allow-access fail [was:] && (req.status != 0)) {
			    Kata.error("Error loading Document: status "+ req.status+" for url "+url);
		    }
		    else {
			hideVisibility(document.getElementById('save_pending'));		
			if (req.responseText.indexOf("ERROR") >= 0) {
			    showVisibility(document.getElementById('save_failed'));		
			    setTimeout(function(){hideVisibility(document.getElementById('save_failed'))},30000);
			}else {
			    showVisibility(document.getElementById('save_complete'));		
			    setTimeout(function(){hideVisibility(document.getElementById('save_complete'))},2500);
			}
		    }
		}
	    }
	    req.open("POST", url, true);
	    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	    req.send(data + "\n" + msg.img);
	}
    }
    function handleMessage(msg) {
        if (msg.data[0]!='{') {//autogenerated messages
            return;
        }else {

        }
        try {
            var view_json = JSON.parse(msg.data);
	        if (view_json.type=="canvasCapture") {
	            publishNowFinish(view_json);
	        }else {
	            processViewJson(view_json);
	        }            
        } catch (x) {
            console.log("ILLEGAL "+msg.data);
            console.log(x);
        }
    }
    function processViewJson(view_json) {
	extra=view_json;
	if (view_json.groundMesh) {
	    groundPlaneMesh=view_json.groundMesh;
	}
	g_scale=view_json.scale?(view_json.scale.length?view_json.scale[0]:view_json.scale):1.0;
        var scalePos=normalizePosToZeroOne(g_scale);
	if (view_json.groundHeight!==undefined) 
	    g_groundPlaneHeight=view_json.groundHeight;
        var heightPos=view_json.groundHeight===undefined?0.0:normalizeAnyToZeroOne(view_json.groundHeight);
        $("#edit_box_scale").slider("option", "value", scalePos*sliderRez);
        $("#edit_box_ground_plane").slider("option","value",heightPos*sliderRez);
        if (view_json.mouse_rot||view_json.mouse_rot===undefined) {
            editToggleRotation(true);
        }else {
            editToggleRotation(false);        
        }
        if (view_json.skybox && view_json.skybox.length) {
	    skybox=view_json.skybox;
            editToggleSkybox(true);
        }else {
            editToggleSkybox(false);        
        }
        if (view_json.sunbeams) {
            editToggleSunbeams(true);
        }else {
            editToggleSunbeams(false);        
        }
        if (view_json.shadows) {
            editToggleShadows(true);
        }else {
            editToggleShadows(false);        
        }
    }
    
    if (window.addEventListener) {
        // For standards-compliant web browsers
        window.addEventListener("message", handleMessage, false);
    } else {
        window.attachEvent("onmessage", handleMessage);
    }
    createEditBox= (function () {
            var created=false;
            return function() {
                if (! created){
                    var scalePos=normalizePosToZeroOne(g_scale);
                    var heightPos=(g_groundPlaneHeight===undefined?0.0:normalizeAnyToZeroOne(g_groundPlaneHeight));
                    $("#edit_box_scale").slider({"max":sliderRez,slide:scaleUpdate,"value":scalePos*sliderRez});
                    $("#edit_box_ground_plane").slider({"max":sliderRez,slide:groundUpdate,"value":heightPos});
                    $("#edit_box").draggable().resizable({"minWidth":104,"minHeight":270});
                }
                created=true;
            };
        })();


    showEditBox=function() {
        toggleVisibility(document.getElementById("edit_box"))
    };
    showEmbed=function() {
	toggleVisibility(document.getElementById("embed_box"))
	setTimeout(embedSelectText,300);
    }
    embedSelectText=function() {
	var temp = document.getElementById("embed_form")
	temp.focus();
	temp.select();
	
    }
    editSave=function() {
	showVisibility(document.getElementById('save_pending'));	
	hideVisibility(document.getElementById('save_complete'));
	hideVisibility(document.getElementById('save_failed'));
	var msg=new Kata.ScriptProtocol.FromScript.GraphicsMessage("","","");
	msg.msg="CaptureCanvas"
        sendMessageToScript(msg);
    }
    downloadArchive = function(object_unique_hash){
	toggleVisibility(document.getElementById('download_box'));
        msg = {};
        msg.url = object_unique_hash;
        var data = JSON.stringify(msg);
        var url = "/download.py";
        var html;        
        var req = new XMLHttpRequest();
        if (req) {
            req.onreadystatechange = function(){
                if (req.readyState == 4) {
                    error = "";
                    if (req.status != 200 && req.status != 0) {
                        //console.log("Error loading Document: status ", req.status);
                        error = "Server error";
                    }
                    else {
                        //console.log("download:", req.responseText);
                        if (req.responseText.indexOf("ERROR") == 0) {
                            //console.log("unable to find download archive: " + req.responseText);
                            error = "Error: missing zip file";
                        }
                        else {
                            //alert (req.responseText.substr(req.responseText.indexOf("SUCCESS:")+8))
                            if (req.responseText.indexOf("ERROR") >= 0) {
                                //console.log("unable to find download archive: " + req.responseText);
                                error = "Error: zip file not found";
                            }
                        }
                    }
                    //console.log("link return " + req.responseText);
                    if (!error) {
                        var link = req.responseText.substr(req.responseText.indexOf("SUCCESS:") + 8);
                        html = '<center>Right-click this link, and select "download" or "save link as":<br><a style="color:#caf" href="' + link + '">' + link + "</a><br>";
                    }
                    else {
                        html = "<br/>" + error + "<br/>";
                    }
                    document.getElementById("download_box").getElementsByTagName("div")[0].innerHTML = html;
                }
            }
            req.open("POST", url, true);
            req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
            req.send(data);
        }
    }

})();
