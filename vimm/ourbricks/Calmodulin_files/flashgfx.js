/*  Kata Javascript Graphics - O3D Interface
 *  o3dgfx.js
 *
 *  Copyright (c) 2010, Daniel Reiter Horn
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are
 *  met:
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *  * Neither the name of Sirikata nor the names of its contributors may
 *    be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 * PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
 * OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

function callFlash(){
//    var flsh = document["flash_canvas"];
    var flsh = document.getElementById("flash_canvas");
    flsh.callFlash();
}



var FlashGraphics=function(callbackFunction,parentElement) {
    this.flashCallback=null;
    this.callback=callbackFunction;
    this.parentElement=parentElement;
    this.msgQueue=[];
    FlashGraphics.loaded =Kata.bind(this.loaded,this);
    var flashvars = {};
    var params = {wmode:"opaque",allowscriptaccess:"always"};
    var attributes = {name:"flash_canvas",id:"flash_canvas"};

//    swfobject.embedSWF(Kata_codeRoot + "externals/flashgfx/FlashGraphics.swf","container", "900", "600", "0","", flashvars, params, attributes);
    /// FIXME: hack, putting FlashGraphics.swf on S3 for now
    var root = Kata_codeRoot + "externals/flashgfx/";
    if (root.indexOf("ourbricks.com") > -1) {
        root = "";
    }
    swfobject.embedSWF(root + "FlashGraphics.swf", "container", "900", "600", "0","", flashvars, params, attributes);

    var thus = this;
    document.addEventListener('mousedown',
                            function (e){thus._mouseDown(e);},
                            true);
    document.addEventListener('mouseup',
                            function(e){thus._mouseUp(e);},
                            true);
    document.addEventListener('mousemove',
                            function(e){thus._mouseMove(e);},
                            true);
    document.addEventListener('keydown',
                            function (e){thus._keyDown(e);},
                            true);
    document.addEventListener('keyup',
                            function(e){thus._keyUp(e);},
                            true);
    document.addEventListener('mousewheel',                           /// Chrome
                            function(e){thus._scrollWheel(e);},
                            true);
    document.addEventListener('DOMMouseScroll',                       /// FF
                            function(e){thus._scrollWheel(e);},
                            true);
    if (false) document.body.addEventListener('contextmenu', //the right context menu is important for debugging, disable its disablement
    function(e){
        if (e.preventDefault) 
            e.preventDefault();
        else 
            e.returnValue = false;
        return false;
    }, true);
    
};

Kata.require([
    'katajs/oh/GraphicsSimulation.js',
    ['katajs/gfx/WebGLCompat.js',
     '../flashgfx/swfobject.js']
], function(){
    
    FlashGraphics.prototype.addObjectUpdate = function(vwObj) {
        this.mObjectUpdates[vwObj.mID] = vwObj;
    };
    
    FlashGraphics.prototype.removeObjectUpdate = function(vwObj) {
        delete this.mObjectUpdates[vwObj.mID];
    };
    
    FlashGraphics.prototype.loaded=function() {
        var flsh = this.parentElement;//
        flsh=document.getElementById("flash_canvas");       
        this.flashCallback=flsh;
        if (flsh.setYfovNearFar) {
            flsh.setYfovNearFar(Kata.GraphicsSimulation.YFOV_DEGREES,
                               Kata.GraphicsSimulation.CAMERA_NEAR,
                               Kata.GraphicsSimulation.CAMERA_FAR);
        }
        if (flsh.callFlash) {
            for (var i=0;i<this.msgQueue.length;++i) {            
                this.send(this.msgQueue[i]);
            }
            delete this.msgQueue;
        }else {
            Kata.warn("Flash loaded but did not register a function to call");
        }
    };
    buggCam=0;
    FlashGraphics.prototype.send=function(obj) {
        if (this.flashCallback) {
            var flsh=this.flashCallback;
            var f=function(obj) {
                //Kata.log(JSON.stringify(obj));
                if (obj.msg!="Custom") {
                    if (obj.msg == "Camera") buggCam=obj.id;
                    if (obj.msg == "Move") {
//                        obj.pos[0] = -obj.pos[0];
//                        obj.vel[0] = -obj.vel[0];
//                        obj.orient[1] = -obj.orient[1];
//                        console.log("DEBUG to flash, iscam:", buggCam == obj.id, "pos:", obj.pos, "orient:", obj.orient, "vel:", obj.vel, "rv:", obj.rotvel, "axis:", obj.rotaxis);
                    }
                    flsh.callFlash(obj);         
                }
            };
            f(obj);
            FlashGraphics.prototype.send=f;
        }else {
            this.msgQueue.push(obj);
        }
    };

    FlashGraphics.loaded=function() {
        Kata.warn("Flash graphics plugin loaded, but no Flash system in place to intercept callback");
    };
    FlashGraphics.inputCallback=function(){
        Kata.warn("Input received, but no input callback registered");
    };
     
    FlashGraphics.prototype.setInputCallback=function(cb) {
        FlashGraphics.inputCallback = cb;//flash needs to call global variables
        this._inputCb = cb;
    };
    
    FlashGraphics.prototype._extractMouseEventInfo = function(e){
        var ev = {};
        ev.type = e.type;
        ev.shiftKey = e.shiftKey;
        ev.altKey = e.altKey;
        ev.ctrlKey = e.ctrlKey;
        ev.which = e.button;
        ev.x = e.clientX;
        ev.y = e.clientY;
        ev.screenX = e.screenX;
        ev.screenY = e.screenY;
        ev.clientX = e.clientX;
        ev.clientY = e.clientY;
        var el = null;
        if (typeof(e.srcElement) != "undefined") {
            el = e.srcElement;
            ev.width = e.srcElement.clientWidth;
            ev.height = e.srcElement.clientHeight;
        }
        else if (typeof(e.target != "undefined")) {
            el = e.target;
            ev.width = e.target.width;
            ev.height = e.target.height;
        }
        else {
            ev.width = 0;
            ev.height = 0;
        }
        while (el != null) {
            ev.x -= el.offsetLeft || 0;
            ev.y -= el.offsetTop || 0;
            el = el.offsetParent;
        }
        return ev;
    };
    

    FlashGraphics.prototype._mouseDown = function(e){
        this._buttonState |= Math.pow(2, e.button);
        var ev = this._extractMouseEventInfo(e);
        var msg = {
            msg: "mousedown",
            event: ev
        };
        if (ev.which==2) {
            document.body.style.cursor="crosshair";
        }
        this._inputCb(msg);
    };
    
    FlashGraphics.prototype._mouseUp = function(e){
        this._buttonState &= 7 - Math.pow(2, e.button);
        var ev = this._extractMouseEventInfo(e);
        var msg = {
            msg: "mouseup",
            event: ev
        };
        if (ev.which == 2) {
            document.body.style.cursor = "default";
        }
        this._inputCb(msg);
    };
    
    /*
     * for now, we only send mouse moves if left button depressed
     * otherwise we flood with messages.  Note right button is controlled by OS so we ignore
     */
    FlashGraphics.prototype._mouseMove = function(e){
        if (this._buttonState) {
            var ev = this._extractMouseEventInfo(e);
            var msg = {
                msg: "mousemove",
                event: ev
            };
            this._inputCb(msg);
        }
    };

    FlashGraphics.prototype._keyDown = function(e){
        if (Kata.suppressCanvasKeyInput) return;
        var ev = {};
        ev.type = e.type;
        ev.keyCode = e.keyCode;
        ev.shiftKey = e.shiftKey;
        ev.altKey = e.altKey;
        ev.ctrlKey = e.ctrlKey;
        var msg = {
            msg: "keydown",
            event: ev
        };
        this._inputCb(msg);
    };

    FlashGraphics.prototype._keyUp = function(e) {
        var ev = {};
        ev.type = e.type;
        ev.keyCode = e.keyCode;
        ev.shiftKey = e.shiftKey;
        ev.altKey = e.altKey;
        ev.ctrlKey = e.ctrlKey;
        var msg = {
            msg: "keyup",
            event: ev
        };
        this._inputCb(msg);
    };

    FlashGraphics.prototype._scrollWheel = function(e){
        var ev = {};
        ev.type = e.type;
        ev.shiftKey = e.shiftKey;
        ev.altKey = e.altKey;
        ev.ctrlKey = e.ctrlKey;
        if (e.wheelDelta != null) {         /// Chrome
            ev.dy = e.wheelDelta;
        }
        else {                              /// Firefox
            ev.dy = e.detail * -40;         /// -3 for Firefox == 120 for Chrome
        }
        var msg = {
            msg: "wheel",
            event: ev
        };
        this._inputCb(msg);
    };
    
    Kata.GraphicsSimulation.registerDriver("flash", FlashGraphics);
}/*, "../externals/flashgfx/flashgfx.js"*/);

