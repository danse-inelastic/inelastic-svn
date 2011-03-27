/**
 * @author dbm
 */
g_scaleIgnoreOnce = 0;
function scaleAsset(scale){
    if (typeof(extra) != "undefined" && g_scaleIgnoreOnce++) {
        extra.scale = [scale, scale, scale]
        rescaleObject(parseFloat(scale));
    }
}

function toggleAllowRotation(){
    var v;
    if (document.getElementById("toggle_rotation_button").innerHTML == "yes") {
        document.getElementById("toggle_rotation_button").innerHTML = "no";
        v = false;
    }
    else {
        document.getElementById("toggle_rotation_button").innerHTML = "yes";
        v = true;
    }
    if (window.kata) {
        console.log("sending mouserot:", v)
        window.kata.getChannel().sendMessage(new Kata.ScriptProtocol.ToScript.GUIMessage({
            msg: "mouserot",
            event: {
                value: v
            }
        }));
    }
}

function publishNow(){
    /// this graphics msg results in a msg to mainscript, which sends a msg to our thread (in viewer.js) which calls publishNowFinish
    g_graphics.mGFX.send({
        msg: "CaptureCanvas"
    });
}
    
function publishNowFinish(img){
    var i = Kata_codeRoot.indexOf("//") + 2
    i += Kata_codeRoot.substr(i).indexOf("/") + 1
//    var url = Kata_codeRoot.substr(0, i) + "cgi-bin/publish.py";
    var url = Kata_homeRoot.substr(0, i) + "publish.py";
    
    extra.url = g_loadUrl;
    var inner = document.getElementById("toggle_rotation_button");
    if (inner && inner.innerHTML == "no") {
        extra.mouse_rot = 'false';
    }
    else {
        extra.mouse_rot = 'true';
    }
    extra.preview = 'false';
    extra.pos = g_objPos;
    extra.orient = g_objOrient;
    if (!extra.camera) {
        extra.camera = {};
    }
    extra.camera.pos = g_camPos;
    extra.camera.orient = g_camOrient;

    extra.vertical_flip = 0;    
    if (navigator.userAgent.indexOf("Firefox/4.0b7") > -1) extra.vertical_flip = 1;
    if (navigator.userAgent.indexOf("Firefox/4.0b8") > -1) extra.vertical_flip = 1;
    if (navigator.userAgent.indexOf("Firefox/4.0b9") > -1) extra.vertical_flip = 1;
    if (navigator.userAgent.indexOf("Firefox/4.0b10") > -1) extra.vertical_flip = 1;
     
    extra.cookie = parseCookie("cookie_id");
    extra.editpass = g_allowPreview;

    var data = JSON.stringify(extra);
    console.log("publish cgi url:", url, "data:", data);

    var html = '<center><br>Saving scene...<br>';
    if (!g_needScreenshot) {
        divDialog(html, divDialogDone, null, null, null, "white", "#136", "gray");
    }
    
    var req = new XMLHttpRequest();
    if (req) {
        req.onreadystatechange = function(){
            if (req.readyState == 4) {
                if (req.status != 200) { //sorry, file:/// is dead; getting status 0 on allow-access fail [was:] && (req.status != 0)) {
                    alert("Error loading Document: status ", req.status);
                }
                else {
                    console.log("publish status:", req.status, "text:", req.responseText);
                    if (req.responseText.indexOf("ERROR") >= 0) {
                        alert(req.responseText);
                        divDialogDone();
                    }
                    else if (!g_needScreenshot) {
                        var html = '<center><br>Scene saved<br>';
                        divDialog(html, divDialogDone, null, null, null, "white", "#163", "gray");
                        setTimeout(divDialogDone, 2000);
                    }
                    else {
                        g_needScreenshot = false;
                    }
                }
            }
        }
        req.open("POST", url, true);
        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
        req.send(data + "\n" + img);
    }
}

g_objPos=[0,0,0];
g_objOrient=[0,0,0,1];
g_camPos=[0,0,0];
g_camOrient=[0,0,0,1];
var g_watchObj, g_watchCam;

function previewListener(e, m){
    if (m.msg == "Camera") {
        g_watchCam = m.id;
    }
    if (m.msg == "Mesh") {
        g_watchObj = m.id;
    }
    if (m.id == g_watchObj) {
        if (m.pos) {
            for (var i = 0; i < 3; i++) {
                g_objPos[i] = m.pos[i];
            }
        }
        if (m.orient) {
            for (var i = 0; i < 4; i++) {
                g_objOrient[i] = m.orient[i];
            }
        }
    }
    if (m.id == g_watchCam) {
        if (m.pos) {
            for (var i = 0; i < 3; i++) {
                g_camPos[i] = m.pos[i];
            }
        }
        if (m.orient) {
            for (var i = 0; i < 4; i++) {
                g_camOrient[i] = m.orient[i];
            }
        }
    }
}


/// this happens after everything is loaded & set up:

function previewContinue(){
    window.kata.getChannel().registerListener(previewListener);
}

