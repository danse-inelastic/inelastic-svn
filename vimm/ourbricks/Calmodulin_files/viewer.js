/**
 * @author dbm
 */

function sha256(s){ 
    var chrsz   = 8;
    var hexcase = 0;
 
    function safe_add (x, y) {
        var lsw = (x & 0xFFFF) + (y & 0xFFFF);
        var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
        return (msw << 16) | (lsw & 0xFFFF);
    }
 
    function S (X, n) { return ( X >>> n ) | (X << (32 - n)); }
    function R (X, n) { return ( X >>> n ); }
    function Ch(x, y, z) { return ((x & y) ^ ((~x) & z)); }
    function Maj(x, y, z) { return ((x & y) ^ (x & z) ^ (y & z)); }
    function Sigma0256(x) { return (S(x, 2) ^ S(x, 13) ^ S(x, 22)); }
    function Sigma1256(x) { return (S(x, 6) ^ S(x, 11) ^ S(x, 25)); }
    function Gamma0256(x) { return (S(x, 7) ^ S(x, 18) ^ R(x, 3)); }
    function Gamma1256(x) { return (S(x, 17) ^ S(x, 19) ^ R(x, 10)); }
 
    function core_sha256 (m, l) {
        var K = new Array(0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786, 0xFC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA, 0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x6CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070, 0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2);
        var HASH = new Array(0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19);
        var W = new Array(64);
        var a, b, c, d, e, f, g, h, i, j;
        var T1, T2;
 
        m[l >> 5] |= 0x80 << (24 - l % 32);
        m[((l + 64 >> 9) << 4) + 15] = l;
 
        for ( var i = 0; i<m.length; i+=16 ) {
            a = HASH[0];
            b = HASH[1];
            c = HASH[2];
            d = HASH[3];
            e = HASH[4];
            f = HASH[5];
            g = HASH[6];
            h = HASH[7];
            for ( var j = 0; j<64; j++) {
                if (j < 16) W[j] = m[j + i];
                else W[j] = safe_add(safe_add(safe_add(Gamma1256(W[j - 2]), W[j - 7]), Gamma0256(W[j - 15])), W[j - 16]);
                T1 = safe_add(safe_add(safe_add(safe_add(h, Sigma1256(e)), Ch(e, f, g)), K[j]), W[j]);
                T2 = safe_add(Sigma0256(a), Maj(a, b, c));
                h = g;
                g = f;
                f = e;
                e = safe_add(d, T1);
                d = c;
                c = b;
                b = a;
                a = safe_add(T1, T2);
            }
            HASH[0] = safe_add(a, HASH[0]);
            HASH[1] = safe_add(b, HASH[1]);
            HASH[2] = safe_add(c, HASH[2]);
            HASH[3] = safe_add(d, HASH[3]);
            HASH[4] = safe_add(e, HASH[4]);
            HASH[5] = safe_add(f, HASH[5]);
            HASH[6] = safe_add(g, HASH[6]);
            HASH[7] = safe_add(h, HASH[7]);
        }
        return HASH;
    }
 
    function str2binb (str) {
        var bin = Array();
        var mask = (1 << chrsz) - 1;
        for(var i = 0; i < str.length * chrsz; i += chrsz) {
            bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (24 - i%32);
        }
        return bin;
    }
 
    function binb2hex (binarray) {
        var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
        var str = "";
        for(var i = 0; i < binarray.length * 4; i++) {
            str += hex_tab.charAt((binarray[i>>2] >> ((3 - i%4)*8+4)) & 0xF) +
            hex_tab.charAt((binarray[i>>2] >> ((3 - i%4)*8  )) & 0xF);
        }
        return str;
    }
 
    return binb2hex(core_sha256(str2binb(s), s.length * chrsz));
}

var divDialog_html = '\
    <div style="position:relative;border-style:solid;border-color:BORDERCOL;background-color:BGDCOL ;color:TEXTCOL;padding:5px">\
    DIALOGTEXT\
    <button onclick="divDialogOK();" style="position:absolute;right:4px;top:4px">CLOSE</button>\
    <!--CANCELBUTTON-->\
    </center></div>\
    ';

var divDialog = function(text, ok, oktext, cancel, canceltext, textcolor, bgdcolor, bordercolor) {
    if (!bgdcolor) {bgdcolor = "#822"}
    if (!bordercolor) {bordercolor = "red"}
    if (!textcolor) {textcolor = "white"}
    if (!oktext) {oktext = "X"}
    if (!canceltext) {canceltext = "CANCEL"}
    var html = divDialog_html.replace("BORDERCOL", bordercolor);
    html = html.replace("TEXTCOL", textcolor);
    html = html.replace("BGDCOL", bgdcolor);    
    html = html.replace("DIALOGTEXT", text);    
    html = html.replace("CLOSE", oktext);
    if (cancel) {
        html = html.replace("<!--CANCELBUTTON-->", '<button onclick="divDialogCANCEL();">CANCELTEXT</button>');
        html = html.replace("CANCELTEXT", canceltext);
    }
    divDialogOK = ok;
    divDialogCANCEL = cancel;
    document.getElementById("div_dialog_div").innerHTML = html;
}

var divDialogDone = function() {
    document.getElementById("div_dialog_div").innerHTML = "";
}

g_webGLFound = true;    
function globalNoWebGLError(){
    document.getElementById("load_screen").innerHTML = "";
    g_webGLFound = false;
    var text = '\
        <div id="nogl" style="font-size:FONTSIZE">\
            <center>\
            <p><br\>\
                To view models in realtime 3D you need to download a webGL-enabled browser. These are links to versions of Chrome and Firefox that support webGL:\
                <br/><br/>\
                <a href="http://www.google.com/chrome/eula.html?extra=devchannel" target="_blank"><img style="border:none" src="chrome_logo.png" title="Install Chrome Dev Channel" alt="Chrome Developer Channel" /></a>\
                &nbsp &nbsp &nbsp\
                <a href="http://www.mozilla.com/firefox/beta/" target="_blank"><img style="border:none" src="ffbeta_logo.png" title="Install Firefox 4 Beta" alt="Firefox Beta" /></a>\
            </p>\
            <p>\
                If you have the latest beta browser and are still seeing this message, type <b>ABOUT</b>\
                into your address bar, search for "webgl" and enable it.<br/>\
                Not all machines can support webGL.\
            </p>\
            </center>\
        </div>'
    //text, ok, oktext, cancel, canceltext, textcolor, bgdcolor, bordercolor
    if (navigator.userAgent.indexOf("Chrome") != -1) {
        text = text.replace("ABOUT", "about:flags")
        text = text.replace("FONTSIZE", "large")
    }
    else {
        text = text.replace("ABOUT", "about:config")
        text = text.replace("FONTSIZE", "normal")
    }
    divDialog(text, function(){
        divDialogDone();
    }, null, null, null, "white", "#744", "gray");
}

g_needScreenshot = true;
g_loadDone = false;
function GlobalLoadDone(){
    if (!g_webGLFound) return;
    g_loadDone = true;
    document.getElementById("load_screen").innerHTML = "";
    if (g_allowPreview) {
        setTimeout(function(){
            var t = new Date().getTime() - g_load_start;
            console.log("LOAD TIME millisec:", t);
        //            document.getElementById("load_time").innerHTML = "load: " + t;        /// that's just ugly
        }, 1);
        if (g_needScreenshot) {
            setTimeout(publishNow, 10000); // it's all in the timing
        }
    }
    else {
        document.getElementById("load_time").innerHTML = "";
    }
    if (extra.errors && g_allowPreview) {
        var s = "<br><center>Errors: " + extra.errors;
        while (s.indexOf("|") > -1) {
            s = s.replace("|", '<br>')
        }
        s += "<br>"
        divDialog(s, function(){
            divDialogDone();
        });
    }
}

var cleanhref = document.location.href;
var i = cleanhref.indexOf("?");
if (i > -1) {
    cleanhref = cleanhref.substr(0, i);
}
i = cleanhref.indexOf(".html");
if (i == cleanhref.length - 5) {
    i = cleanhref.lastIndexOf("/");
    cleanhref = cleanhref.substr(0, i + 1);
}
console.log("clean href:", cleanhref);

var queryArgs = {};
var allowDups = {"dupargument": true};
function addQueryArgs(searchString, first) {
    queryArgList = []
    if (searchString.charAt(0)==first) {
        queryArgList = searchString.substr(1).split("&");
    }
    for (var i = 0; i < queryArgList.length; i++) {
        var query = queryArgList[i];
        var keyval = query.split("=");
        var key = keyval[0];
        var val = unescape(keyval[1]);
        if (allowDups[key] && key in queryArgs) {
            if (!(queryArgs[key] instanceof Array)) {
                queryArgs[key] = [queryArgs[key], val]
            } else {
                queryArgs[key].push(val);
            }
        } else {
            queryArgs[key] = val;
        }
    }
}
addQueryArgs(document.location.search, "?");
addQueryArgs(document.location.hash, "#");

console.log("Arguments: ", queryArgs);

//var bucket="vu.ourbricks.com";
if (queryArgs.bucket) {
    Kata_bucket = queryArgs.bucket;
}
else {
    var domain = document.URL;
    var i = domain.indexOf("//");
    if (i >= 0) {
        domain = domain.substr(i + 2);
    }
    i = domain.indexOf("/");
    if (i >= 0) {
        domain = domain.substr(0, i);
    }
    Kata_bucket = domain;
}
console.log("Kata_bucket=", Kata_bucket);

var load;
if (queryArgs["local"]=="true") {
    load = cleanhref + "server/bigbox_o3d";
    g_needScreenshot=false;
}
else {
    load = "http://" + Kata_bucket + "/test/server/bigbox_o3d";
}

if ("load" in queryArgs) {
    load = "" + queryArgs["load"];
    while (load.indexOf("|") > -1) {
        load = load.replace("|", "/");
    }
    load = cleanhref + load;
}
var uid=null;
if ("v" in queryArgs) {
    var vParam = queryArgs["v"];
    var j = vParam.indexOf(":");
    var user = vParam.substr(0, j);
    uid = vParam.substr(j + 1);
    if (uid.indexOf("/") == uid.length - 1) {
        uid = uid.substr(0, uid.length - 1);
    }
    var j = uid.indexOf(":");
    if (j > -1) {
        uid = uid.substr(0, j);
    }

    console.log("user, uid:", user, uid);
    load = "http://" + Kata_bucket + "/" + user + "/" + uid + "/processed";
    if (!user) {
        /// hack to view files uploaded to empty folder, which really means uploaded to root because of s3 bug:
        load = load.replace(Kata_bucket  + "//", Kata_bucket + "/")
    }
}
g_allowPreview = false;
if ("edit" in queryArgs) {
    var pw = queryArgs.edit;
    if (pw) {
        if (sha256(pw) == "a62157a13451da9b89e54350da4581ebfe19639c6be58da02663367bc1f0cc68") {
            console.log("edit mode enabled");
            g_allowPreview = pw;
        }
        else {
            console.log("edit mode not enabled; badd password:", sha256(pw));            
        }
    }
}
i = load.indexOf("?");
if (i > -1) {
    load = load.substr(0, i);
}
if (load[load.length - 1] == "/") {
    load = load.substr(0, load.length - 1);
}
console.log("LOAD:", load);
g_loadUrl = load;
g_lastCallbackTime = new Date().getTime();
g_FPSCounter = 0;
Kata.userRenderCallback = function(t){
	g_FPSCounter++;
	var now = t.getTime();
	if (now < g_lastCallbackTime + 1000) {
		return;
	}
	fps = 1000.0 * g_FPSCounter / (now - g_lastCallbackTime);
	document.getElementById("framerate").innerHTML = "fps: " + fps.toFixed(2);
	g_lastCallbackTime = now;
	g_FPSCounter = 0;
}
rescaleObject=function(v) {
    if (window.kata) {
        window.kata.getChannel().sendMessage(new Kata.ScriptProtocol.ToScript.GUIMessage({
            msg: "rescale",
            event: {
                value: v
            }
        }));
    }
};

g_driver = "GLGE";
if ("driver" in queryArgs) {
    g_driver = queryArgs["driver"]; // "o3d" or "GLGE"
    if (g_driver == "o3d") {
        document.write(
            "<script type='text/javascript' src='" +
                Kata_scriptRoot + "externals/o3djs/base.js"+"'></scr"+"ipt>" +
                "<script type='text/javascript' src='" +
                Kata_scriptRoot + "externals/o3d-webgl/base.js"+"'></scr"+"ipt>"+
                "<script type='text/javascript' src='" +
                Kata_scriptRoot + "katajs/gfx/o3dgfx.js"+"'></scr"+"ipt>");
    }
}

/// FIXME test: uid = "5923df36d93d4ad28949c148bde21826";

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

checkIfUser = function(cookie, error, cb){
    var i = Kata_homeRoot.indexOf("//") + 2
    i += Kata_homeRoot.substr(i).indexOf("/") + 1
    var url = Kata_homeRoot.substr(0, i) + "check-if-user";
    var obj = {}
    obj.cookie = cookie;
    obj.uid = uid;
    var data = JSON.stringify(obj);
    var req = new XMLHttpRequest();
    if (req) {
        req.onreadystatechange = function(){
            if (req.readyState == 4) {
                if (req.status != 200 && req.status != 0) {
                    error(req.status);
                }
                else {
                    cb(req.responseText);
                }
            }
        }
        req.open("POST", url, true);
        // req.withCredentials = true;
        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
        req.send(data);
    }
}

main = function(){
    var cookie = parseCookie("cookie_id");
    if (cookie && uid && document.getElementById("preview_extra_html")) {
        checkIfUser(cookie,
            function(status){
                alert("Error loading Document: status ", status);
                main1();
            },
            function(resptext){
                console.log("checkIfUser:", resptext);
                if (resptext.indexOf("SUCCESS") == 0) {
                    g_allowPreview = true;
                }
                main1();
            }
        );
    }
    else {
        main1();
    }
}

//var load_html_noGL = '<div style="position:absolute;top:50px"><img style="position:relative" src="LOADBASE/ourbricksImg.jpg"></img></div>'
var load_html_noGL = '\
<div style="position:absolute">\
    <img style="position:relative;width:WIDTHpx;height:HEIGHTpx;top:TOPpx;left:LEFTpx" src="LOADBASE/ourbricksImg.jpg"></img>\
</div>'


var load_html = '\
<div style="position:absolute">\
    <img style="position:relative;width:WIDTHpx;height:HEIGHTpx;top:TOPpx;left:LEFTpx" src="LOADBASE/ourbricksImg.jpg"></img>\
    <div align="center" style="position:relative; margin:auto; top:-350px; background-color: #678;\
                         opacity: 0.8;height: 250px;  width: 400px;\
                        -moz-border-radius:5px;-webkit-border-radius:5px;border: 1px">\
        <div align="center" style="position:relative; top: 52px">\
            <div id="load_screen_text">\
                <h1>LOADING...</h1>\
                <h2>WASD or arrow keys move camera</h2>\
                <h2>press HELP for more info</h2>\
            </div>\
        </div>\
    </div>\
</div>'

function enablePreview(){
    if (!g_allowPreview) return;
    var preview_html_text = '\
        <div style="position:absolute;left:010px;bottom:-22px;color:white">\
            resize:\
        </div>\
        <div style="position:absolute;left:430px;bottom:-25px;color:white">\
            allow mouse rotation:\
            <button id="toggle_rotation_button" onclick = "toggleAllowRotation()" >yes</button>\
        </div>\
        <div style="position:absolute;right:0px;bottom:-25px">\
            <button id="publish_button" onclick = "publishNow()" >save changes</button>\
        </div>;'
    
    var temp = extra.scale; /// bogus rescale call is made
    document.getElementById("preview_extra_html").innerHTML = preview_html_text;
    createRescaleSlider();
    extra.scale = temp;
    if (extra.errors) {
        var s = "Errors:" + extra.errors;
        while (s.indexOf("|") > -1) {
            s = s.replace("|", '<br>')
        }
        document.getElementById("extra_errors").innerHTML = s;
    }
    g_bottomPadding=23;
    resizeMainpane();
}

/*
 * function to take w, h, w2, h2, and return x, y, w, h that fills w2, h2 without changing aspect ratio
 * so it should be centered, with either vertical or horizontal letterboxing
 */
fixWidthHeight = function (w, h, w2, h2) {
    var a = w/h;
    var a2 = w2/h2;
    x = 0;
    y = 0;
    if (a > a2) {
        h = h * (w2 / w);
        w = w2;
        y = (h2 - h) / 2;
    }
    else {
        w = w * (h2 / h);
        h = h2;
        x = (w2 - w) / 2;
    }
    return [parseInt(x), parseInt(y), parseInt(w), parseInt(h)];
}

var g_graphics;
main1 = function() {
    var kata;
    var defaultSpace = "loop://localhost";
    function loadGFX(){
        var req = new XMLHttpRequest();
        if (req) {
            req.overrideMimeType("application/json")
            req.onreadystatechange = function(){
                extra = {};
                if (this.readyState == 4) {
                    if (this.status == 0 || this.status == 200) {
                        if (this.responseText) {
                            console.log("responseText:", this.responseText)
                            eval("extra=" + this.responseText);
                            console.log("extra:", extra)
                        }
                    }
                    else {
                        var html = '<div style="position:absolute;width:100%;%;top:150px;margin:auto;color:#ccc;font-size:large"><center>This OurBricks URL is either malformed, or the content has been removed</center></div>';
			            document.getElementById("load_screen").innerHTML ="";
                        var el = document.getElementById("object_description");
			            extra.description=html
                        if(el) el.innerHTML = html;
                    }                    

                    // pop up screenshot while loading (if it exists)
                    var loadbase = load;
                    var req2 = new XMLHttpRequest();
                    if (req2) {
                        req2.overrideMimeType("application/json")
                        req2.onreadystatechange = function(){
                            if (this.readyState == 4) {
                                if (this.status == 0 || this.status == 200) {
                                    //console.log("DEBUG html:", html);
                                    g_needScreenshot = false;
                                    if (!g_loadDone) {
                                        var html = load_html;
                                        if (!g_webGLFound) {
                                            html = load_html_noGL;
                                        }
                                        var el = document.getElementById("mainpane");
                                        var w = el.offsetWidth;
                                        var h = el.offsetHeight;
                                        var x = 0;
                                        var y = 0;
                                        if (extra.capwidth) {
                                            var temp = fixWidthHeight(extra.capwidth, extra.capheight, w, h)
                                            x = temp[0];
                                            y = temp[1];        /// oh for some Python sugar x, y, w, h = blah()
                                            w = temp[2];
                                            h = temp[3];
                                        }
                                        html = html.replace("LOADBASE", loadbase);
                                        html = html.replace("WIDTH", w);
                                        html = html.replace("HEIGHT", h);
                                        html = html.replace("LEFT", x);
                                        html = html.replace("TOP", y);
                                        document.getElementById("load_screen").innerHTML = html;
                                    }
                                }
                            }
                        }
                    };
                    req2.open("GET", loadbase + "/ourbricksImg.jpg", true);
                    req2.send("");

                    if (!g_allowPreview) {
                        var el = document.getElementById("edit_button")
                        if (el) el.innerHTML = "";                        
                    }
                    if (extra.userid) {
                        var html = '<div style="position:absolute;width:100%;%;top:30px;margin:auto;color:#ccc;font-size:medium"><a style="color: #ffffff" href="' + Kata_homeRoot + '?user=RELATED" target="_top">Other models by this person</a></div>';
                        var el = document.getElementById("related_links");
                        if (el) el.innerHTML = html.replace("RELATED", extra.userid);
                    }
                    if (extra.description) {
                        var html = '<div style="position:absolute;width:100%;%;top:2px;margin:auto;color:#ccc;font-size:medium">DESC</div>';
                        var el = document.getElementById("object_description");
                        if(el) el.innerHTML = html.replace("DESC",extra.description);
                    }
                    if (extra.title) {
                        document.getElementById("object_title").innerHTML = "<h2>" + extra.title + "</h2>";
                    }
                    if (extra.o3dscene) {
                        load += "/" + extra.o3dscene + ".dae";
                    }
                    
                    if (extra.license) {
                        license_language = extra.license;
                    }
                    if (extra.author) {
                        license_language = license_language + "<br/>" + "author: " + extra.author 
                    }
                    /// if in preview mode, set rotation button state
                    var mouse_rot = true;
                    if (extra.mouse_rot && extra.mouse_rot == "false") {
                        mouse_rot = false;
                        if (document.getElementById("toggle_rotation_button")) {
                            toggleAllowRotation();
                        }
                    }
                    console.log("mainscene load:", load);
                    var loadargs = {
                        mesh: load,
                        anim: extra.anim,
                        up_axis: extra.up_axis,
                        scale: extra.scale,
                        mouse_rot: mouse_rot,
                        center: extra.center,
                        bounds: extra.bounds,
                        driver: g_driver
                    };
                    if (extra.pos) {
                        loadargs.pos = extra.pos;
                    }
                    if (extra.orient) {
                        loadargs.orient = extra.orient;
                    }
                    window.kata = new Kata.MainThread("../../mainscript.js", "Example.BlessedScript", {
                        space: defaultSpace,
                        load: loadargs,
                        camera: extra.camera
                    });
                    g_graphics = new Kata.GraphicsSimulation(g_driver, window.kata.getChannel(), document.getElementById("container"));

                    /// in publish mode, suppress GLGE errors:
                    if (!g_allowPreview) {
                        GLGE.error = function(e){
                            console.log("GLGE ERROR:", e);
                        };
                    }
                    window.kata.getChannel().registerListener(function(channel, msg){
                        if (msg.msg == "Custom") {
//                            Kata.warn("moved to " + msg.data.campos);
                            if (msg.data.type == "Loaded") {
                                GlobalLoadDone();
                            }
                            else if (msg.data.type == "canvasCapture") {
                                publishNowFinish(msg.data.img);
                            }
                            else if (typeof(g_camPos) != "undefined") {
                                g_camPos = msg.data.campos.concat();
                            }
                        }
                        
                    });
                    // Simulated local space
                    loopspace = new Kata.LoopbackSpace(Kata.URL(defaultSpace));
                    if (typeof(previewContinue) != "undefined") {
                        previewContinue();
                    }
                }
            };
            console.log("load request:", load + "/view.json");
            req.open("GET", load + "/view.json?" + Math.random(), true);
            req.send("");
        }
    }
    if (g_driver == "GLGE") {
        g_GLGE_doc = new GLGE.Document();
        g_GLGE_doc.onLoad = loadGFX;
        g_GLGE_doc.load("glge_level.xml");
    }
    else {
        window.onload = loadGFX;
    }
    
    getHelp = function(){
        if (document.getElementById("help_screen").innerHTML.length < 50) {
            var el = document.getElementById("mainpane");
            var w = el.offsetWidth;
            var h = el.offsetHeight;
            var html = help_text.replace("TOP", h-310);
            var html = html.replace("LEFT", w-320);
            document.getElementById("help_screen").innerHTML = html
        }
        else {
            document.getElementById("help_screen").innerHTML = ""
        }
    }
    
    fullPage = function(){
        var url = document.URL.replace("/em.html", "/t.html")
        window.top.location=url;
    }
    
    showEmbed = function(){
        var url;
        if (uid) {
            url = "http://" + Kata_bucket + "/" + uid + "/processed/embed.html";
        }
        else {
            url = document.URL.replace("/t.html", "/embed.html");
            url = url.replace("/index.html", "/embed.html");
            url = url.replace("/em.html", "/embed.html");
        }
        var html = '<form onclick="embedSelectText()">\
        <textarea  id="embed_form" rows="3" cols = "80"><iframe src="URL" style="border:none" width="910" height="666"></iframe></textarea></form>'
        html = html.replace("URL", url);
        html = '<center>Copy this source code into your web page to embed this 3D scene:<br>' + html;
        divDialog(html, divDialogDone, null, null, null, "white", "#383", "gray");
        setTimeout(embedSelectText, 300);
    }
    
    embedSelectText = function(){
        var temp = document.getElementById("embed_form");
        temp.focus();
        temp.select();
    }
    
    showLicense = function(){
        if (document.getElementById("license_screen").innerHTML.length < 50) {
            document.getElementById("license_screen").innerHTML = license_text.replace("LICENSE", license_language)
        }
        else {
            document.getElementById("license_screen").innerHTML = ""
        }
    }
    
    downloadArchive = function(){
        msg = {};
        msg.url = queryArgs.v;
        var data = JSON.stringify(msg);
        var i = Kata_codeRoot.indexOf("//") + 2
        i += Kata_codeRoot.substr(i).indexOf("/") + 1
        var url = Kata_codeRoot.substr(0, i) + "cgi-bin/download.py";
        
        var req = new XMLHttpRequest();
        if (req) {
            req.onreadystatechange = function(){
                if (req.readyState == 4) {
                    if (req.status != 200 && req.status != 0) {
                        alert("Error loading Document: status ", req.status);
                    }
                    else {
                        console.log("download:", req.responseText);
                        if (req.responseText.indexOf("ERROR") == 0) {
                            alert(req.responseText);
                        }
                        else {
                            //alert (req.responseText.substr(req.responseText.indexOf("SUCCESS:")+8))
                            if (req.responseText.indexOf("ERROR") >= 0) {
                                alert(req.responseText);
                            }
                            else {
                                var link = req.responseText.substr(req.responseText.indexOf("SUCCESS:") + 8);
                                var html = '<center>Right-click this link, and select "download" or "save link as":<br><a style="color:#caf" href="' + link + '">' + link + "</a><br>";
                                divDialog(html, divDialogDone, null, null, null, "white", "#383", "gray");
                            }
                        }
                    }
                }
            }
            req.open("POST", url, true);
            req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
            req.send(data);
        }
    }

    var help_text = '\
<div style="position:absolute;left:LEFTpx;top:TOPpx;width:320px;color:white;background-color:black;opacity:0.85">\n\
<b>mouse & keyboard commands:</b><br>\n\
left click & drag to rotate object (if enabled)<br>\n\
..(try shift & control while rotating) <br>\n\
right click & drag to turn camera<br>\n\
W: move forward<br>\n\
A: move left<br>\n\
S: move backward<br>\n\
D: move right<br>\n\
page up: raise camera (R on Mac)<br>\n\
page down: lower camera (F on Mac)<br>\n\
space: reset scene<br>\n\
arrow keys also work<br>\n\
click HELP to clear this screen<br>\n\
</div>\n\
';
    var license_text = '\
<div align="center" style="position:relative; margin:auto; top: 75px; background-color: #678; \
opacity: 1.0;height: 350px;  width: 460px;  \
-moz-border-radius:5px;-webkit-border-radius:5px;border: 1px">\
<div style="position:relative; top: 50px">\
LICENSE<br>\
<br><button onclick="showLicense()">close</button>\
</div>\
</div>';

    var license_language = 'This work is licensed under a Creative Commons Attribution 3.0 Unported License.<br>\
More information about this license can be obtained \
<a href="http://creativecommons.org/licenses/by/3.0/">here</a>.<br>\
If you have trouble with this link, try <a href="http://beta.ourbricks.com/legalcode.html">here</a> instead.<br>\
<br><img src="cclogo.png"/>'

};
//main();
