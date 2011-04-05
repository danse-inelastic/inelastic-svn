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
g_moveGroundPlaneIgnoreOnce = 0;
function moveGroundPlane(scale){
    if (typeof(extra) != "undefined" && g_moveGroundPlaneIgnoreOnce++) {
        extra.groundHeight = scale;
        setGroundPlaneHeight(scale,extra.groundMesh?extra.groundMesh:extra.groundMesh="collada/models/invground.dae");
    }
}

function queryOn(el){
    if (document.getElementById(el).innerHTML != "Off") {
        return true;
    }
    else return false;
}
function toggleOnOff(el){
    var v;

console.log("INNER "+el);
    console.log(" "+    document.getElementById(el).innerHTML);
    if (document.getElementById(el).innerHTML != "Off") {
        document.getElementById(el).innerHTML = "Off";
        v = false;
    }
    else {
        document.getElementById(el).innerHTML = "On";
        v = true;
    }
    return v;
}
function toggleSunbeams(el,skyboxel){
    var v=toggleOnOff(el);
    var skybox=queryOn(skyboxel);
    setSkybox(skybox,v);
}
function toggleSkybox(el,sunbeamel){
    var v=toggleOnOff(el);
    var sunbeams=queryOn(sunbeamel);
    setSkybox(v,sunbeams);
}
function toggleShadows(el){
    var v=toggleOnOff(el);
    setShadows(v);
}
function toggleMouseRotation(){
    var v = toggleOnOff("toggle_rotation_button")
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
        msg: "CaptureCanvas",
        still:true
    });
    setTimeout(function(){
                   g_graphics.mGFX.send({
                                            msg: "CaptureCanvas"
                                        });                   
               }, 500); // it's all in the timing
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
    if (queryOn("toggle_sunbeam_button")){
        extra.sunbeams=true;
    }else {
        extra.sunbeams=false;
    }
    if (queryOn("toggle_skybox_button")){
        extra.skybox=["skydome.png"];
    }else {
        extra.skybox=[];
    }
    if (queryOn("toggle_shadows_button")){
        extra.shadows=true;
    }else {
        extra.shadows=false;
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
                    Kata.log("Error loading Document: status "+ req.status);
                }
                else {
                    console.log("publish status:", req.status, "text:", req.responseText);
                    if (req.responseText.indexOf("ERROR") >= 0) {
                        Kata.log("previewer error "+req.responseText);
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
    //console.log("Received "+JSON.stringify(m));
    if (m.msg == "Custom" && m.data.type=="CreatedLoadObject") {
        g_watchObj = m.data.id;
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

