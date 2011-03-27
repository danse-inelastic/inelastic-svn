var a;
if(typeof Kata == "undefined") {
  Kata = {}
}Kata.closureIncluded = {"katajs/core/Core.js":true, "katajs/core/Core.js":true, "externals/protojs/protobuf.js":true, "externals/protojs/pbj.js":true, "externals/GLGE/glge_math.js":true, "externals/GLGE/glge.js":true, "externals/GLGE/glge_collada.js":true, "katajs/gfx/WebGLCompat.js":true, "katajs/gfx/glgegfx.js":true, "katajs/gfx/TextGraphics.js":true, "katajs/core/Math.uuid.js":true, "katajs/core/Location.js":true, "katajs/core/SimpleChannel.js":true, "katajs/core/Time.js":true, "katajs/core/URL.js":true, 
"katajs/core/MessageDispatcher.js":true, "katajs/core/Deque.js":true, "katajs/core/Quaternion.js":true, "katajs/core/SpaceID.js":true, "katajs/core/FilterChannel.js":true, "katajs/core/WebWorker.js":true, "katajs/core/ObjectID.js":true, "katajs/core/Channel.js":true, "katajs/core/PresenceID.js":true, "katajs/oh/SessionManager.js":true, "katajs/oh/ObjectHost.js":true, "katajs/oh/impl/ScriptProtocol.js":true, "katajs/oh/impl/BootstrapScript.js":true, "katajs/oh/Presence.js":true, "katajs/oh/MainThread.js":true, 
"katajs/oh/ObjectHostWorker.js":true, "katajs/oh/Script.js":true, "katajs/oh/GUISimulation.js":true, "katajs/oh/sst/SSTImpl.js":true, "katajs/oh/GraphicsScript.js":true, "katajs/oh/Simulation.js":true, "katajs/oh/odp/Endpoint.js":true, "katajs/oh/odp/Port.js":true, "katajs/oh/odp/Service.js":true, "katajs/oh/odp/PortID.js":true, "katajs/oh/RemotePresence.js":true, "katajs/oh/plugins/sirikata/impl/Loc.pbj.js":true, "katajs/oh/plugins/sirikata/impl/TimedMotionVector.pbj.js":true, "katajs/oh/plugins/sirikata/impl/TimeSync.pbj.js":true, 
"katajs/oh/plugins/sirikata/impl/Prox.pbj.js":true, "katajs/oh/plugins/sirikata/impl/Frame.pbj.js":true, "katajs/oh/plugins/sirikata/impl/Session.pbj.js":true, "katajs/oh/plugins/sirikata/impl/Empty.pbj.js":true, "katajs/oh/plugins/sirikata/impl/ObjectMessage.pbj.js":true, "katajs/oh/plugins/sirikata/impl/TimedMotionQuaternion.pbj.js":true, "katajs/oh/plugins/sirikata/impl/SSTHeader.pbj.js":true, "katajs/oh/plugins/sirikata/SirikataSpaceConnection.js":true, "katajs/oh/plugins/sirikata/Frame.js":true, 
"katajs/oh/plugins/sirikata/Sync.js":true, "katajs/oh/plugins/loop/LoopbackSpaceConnection.js":true, "katajs/oh/behavior/NamedObject.js":true, "katajs/oh/HostedObject.js":true, "katajs/oh/SpaceConnection.js":true, "katajs/oh/GraphicsSimulation.js":true, "katajs/network/TCPSST.js":true, "katajs/space/loop/Loc.js":true, "katajs/space/loop/Subscription.js":true, "katajs/space/loop/EveryoneProx.js":true, "katajs/space/loop/Space.js":true};network_debug = false;
if(typeof Kata == "undefined") {
  Kata = {}
}if(typeof console == "undefined") {
  console = {};
  debug_console = false
}else {
  debug_console = true
}if(typeof JSON == "undefined") {
  JSON = {}
}if(!Kata.scriptRoot) {
  Kata.scriptRoot = ""
}if(!Kata.queryString) {
  Kata.queryString = ""
}(function() {
  function e(v, B) {
    Kata._currentScript.push(v);
    try {
      B && B()
    }finally {
      Kata.getCurrentScript() != v && Kata.log("Error11: " + v + " != " + Kata.getCurrentScript(), Kata._currentScript);
      Kata._currentScript.pop();
      v && Kata.setIncluded(v)
    }
  }
  function j(v) {
    function B(E) {
      return function() {
        delete u[v[E]];
        Kata.include(v[E])
      }
    }
    for(var C = 0;C < v.length;C++) {
      for(;h[v[C]];) {
        v.splice(C, 1)
      }
    }for(C = 0;C < v.length - 1;C++) {
      q[v[C]] = q[v[C]] || [];
      q[v[C]].push(B(C + 1));
      u[v[C + 1]] = true
    }if(v.length) {
      u[v[0]] || Kata.include(v[0])
    }
  }
  var h = Kata.closureIncluded || {"katajs/core/Core.js":true}, o = {"katajs/core/Core.js":true}, q = {}, u = {};
  Kata._currentScript = [];
  Kata.getCurrentScript = function() {
    return Kata._currentScript[Kata._currentScript.length - 1]
  };
  Kata.require = function(v, B, C) {
    function E(N) {
      if(J[N]) {
        delete J[N];
        M--;
        if(M == 0) {
          C && delete u[C];
          e(C, B)
        }
      }
    }
    if(C && C in o) {
      Kata.warn("JS file " + C + " included twice.")
    }else {
      if(!u[C]) {
        var H, J = {}, M = 0;
        for(H = 0;H < v.length;H++) {
          if(v[H].push) {
            for(var K = 0;K < v[H].length;K++) {
              if(!o[v[H][K]] && !(v[H][K] in J)) {
                J[v[H][K]] = true;
                M++
              }
            }
          }else {
            if(!o[v[H]] && !(v[H] in J)) {
              J[v[H]] = true;
              M++
            }
          }
        }if(M) {
          if(C) {
            u[C] = true
          }for(H in J) {
            q[H] = q[H] || [];
            q[H].push(E)
          }for(H = 0;H < v.length;H++) {
            if(v[H].push) {
              j(v[H])
            }else {
              u[v[H]] || Kata.include(v[H])
            }
          }
        }else {
          B();
          Kata.setIncluded(C)
        }
      }
    }
  };
  Kata.defer = function(v) {
    v && Kata.require([], v, null)
  };
  Kata.setIncluded = function(v) {
    if(v) {
      if(!u[v]) {
        if(q[v]) {
          var B = q[v];
          delete q[v];
          for(var C = 0;C < B.length;C++) {
            B[C](v)
          }
        }o[v] = true
      }
    }
  };
  if(typeof importScripts != "undefined") {
    Kata.include = function(v) {
      if(!h[v]) {
        h[v] = true;
        e(v, function() {
          try {
            importScripts(Kata.scriptRoot + v + Kata.queryString)
          }catch(B) {
            Kata.log("Error in importScripts(" + Kata.scriptRoot + v + ")");
            throw B;
          }
        })
      }
    };
    Kata.evalInclude = Kata.include
  }else {
    if(typeof document != "undefined" && document.write) {
      for(var f = document.getElementsByTagName("script"), g = document.getElementsByTagName("head")[0], m = 0;m < f.length;m++) {
        var p = f[m].getAttribute("src");
        if(p) {
          var r = p.indexOf("katajs/core/Core.js");
          if(r != -1) {
            p = p.substr(0, r);
            if(p.length > 0 && p.slice(-1) != "/") {
              p += "/"
            }Kata.scriptRoot = p
          }
        }
      }window.pendingScripts = {};
      Kata.include = function(v) {
        if(!h[v]) {
          h[v] = true;
          var B;
          B = document.createElement("script");
          B.src = Kata.scriptRoot + v + Kata.queryString;
          B.type = "text/javascript";
          B.addEventListener("load", function() {
            Kata.getCurrentScript() && Kata.log("Error: " + v + " != " + Kata.getCurrentScript(), Kata._currentScript);
            Kata.setIncluded(v)
          }, true);
          g.appendChild(B)
        }
      };
      Kata.evalInclude = Kata.include
    }
  }Kata.extend = function(v, B) {
    for(var C in B) {
      v.prototype[C] = B[C]
    }v.prototype.constructor = v;
    v.prototype.SUPER = B
  };
  Kata.bind = function(v, B) {
    if(arguments.length == 2) {
      delete arguments;
      return function() {
        return v.apply(B, arguments)
      }
    }else {
      for(var C = new Array(arguments.length - 2), E = 2;E < arguments.length;++E) {
        C[E - 2] = arguments[E]
      }delete arguments;
      return function() {
        for(var H = arguments.length, J = new Array(H), M = 0;M < H;++M) {
          J[M] = arguments[M]
        }return v.apply(B, C.concat(J))
      }
    }
  };
  Kata.stringify = function(v, B) {
    B || (B = "");
    var C = B + "}";
    B += "    ";
    var E;
    if(typeof v != "object" || v === null) {
      return"" + v
    }E = "{\n";
    for(var H in v) {
      E += B + H + ": " + Kata.stringify(v[H], B) + ",\n"
    }E += C;
    return E
  };
  Kata.log = console.log && debug_console ? function() {
    console.log.apply(console, arguments)
  } : typeof document == "undefined" || typeof window == "undefined" ? (console.log = function() {
    for(var v = [], B = 0;B < arguments.length;B++) {
      v[B] = arguments[B];
      if(typeof v[B] == "object") {
        v[B] = Kata.stringify(v[B])
      }else {
        if(typeof v[B] != "string") {
          v[B] = "" + v[B]
        }
      }
    }self.postMessage({msg:s, debug:"log", contents:v})
  }) : debug_console ? (console.log = function() {
    window.status = "" + arguments[0];
    var v = document.createElement("p");
    v.style.border = "1px solid black";
    for(var B = v.style.margin = "0", C = 0;C < arguments.length;C++) {
      var E = arguments[C], H;
      if(typeof E != "object" || E.toString != Object.prototype.toString) {
        H = document.createElement("div");
        H.appendChild(document.createTextNode(E))
      }else {
        E = Kata.stringify(E);
        H = document.createElement("pre");
        H.appendChild(document.createTextNode(E))
      }H.style.margin = "0";
      H.style.padding = "5px";
      H.style.overflow = "auto";
      H.style.whiteSpace = "pre";
      H.style.border = "1px solid #ccc";
      H.style.marginLeft = B;
      B = "30px";
      v.appendChild(H)
    }document.body && document.body.appendChild(v)
  }) : (console.log = function() {
  });
  Kata.setStatus = function(v) {
    if(typeof window != "undefined") {
      window.status = v
    }
  };
  var s = "__magic_debug_msg_string";
  Kata.error = function(v) {
    if(typeof window == "undefined") {
      self.postMessage({msg:s, debug:"error", contents:v});
      throw v;
    }console.log(v);
    if(typeof console.error != "undefined") {
      Kata.setStatus(v);
      console.error && console.error(v);
      console.trace && console.trace()
    }
  };
  Kata.warn = function(v, B) {
    if(typeof B == "undefined" || !B) {
      B = ""
    }if(typeof window == "undefined") {
      self.postMessage({msg:s, debug:"warn", type:B, contents:v})
    }else {
      var C = null;
      if(B && v) {
        C = B + ": " + v
      }else {
        if(B) {
          C = B
        }else {
          if(v) {
            C = v
          }
        }
      }console.log(C);
      Kata.setStatus(C)
    }console.trace && console.trace()
  };
  Kata.notImplemented = function(v) {
    Kata.warn(v, "notImplemented")
  };
  var A = 1001;
  Kata.debugMessage = function(v, B) {
    if(B === undefined || B === null || B.msg != s) {
      return false
    }var C = 0;
    if(v) {
      if(!v.__debug_id) {
        v.__debug_id = A++
      }C = v.__debug_id
    }C = "<" + C + ">";
    switch(B.debug) {
      case "error":
        Kata.log(C + " " + B.contents);
        break;
      case "warn":
        Kata.log(C + B.type + ": " + B.contents);
        break;
      case "log":
        B.contents.splice(0, 0, C);
        Kata.log.apply(self, B.contents);
        break;
      default:
        Kata.error(C + " Unknown debug message type: " + B.debug);
        break
    }
    return true
  }
})();var PROTO = {};
PROTO.DefineProperty = function() {
  var e;
  if(typeof Object.defineProperty != "undefined") {
    e = function(q, u, f, g) {
      Object.defineProperty(q, u, {get:f, set:g, enumerable:true, configurable:false})
    }
  }else {
    if(Object.prototype.__defineGetter__ && Object.prototype.__defineSetter__) {
      e = function(q, u, f, g) {
        typeof f !== "undefined" && q.__defineGetter__(u, f);
        typeof g !== "undefined" && q.__defineSetter__(u, g)
      }
    }
  }if(e) {
    try {
      var j = function() {
      };
      e(j.prototype, "x", function() {
        return this.xval * 2
      }, function(q) {
        this.xval = q
      });
      var h = new j;
      h.x = 5;
      if(h.x != 10) {
        console.log("DefineProperty test gave the wrong result " + h.x);
        e = undefined
      }
    }catch(o) {
      typeof console != "undefined" && console.log && console.log("DefineProperty should be supported, but threw " + o, o);
      e = undefined
    }
  }return e
}();
PROTO.cloneType = function(e) {
  var j = {};
  for(var h in e) {
    j[h] = e[h]
  }return j
};
PROTO.wiretypes = {varint:0, fixed64:1, lengthdelim:2, fixed32:5};
PROTO.optional = "optional";
PROTO.repeated = "repeated";
PROTO.required = "required";
PROTO.I64 = function(e, j, h) {
  this.msw = e;
  this.lsw = j;
  if(typeof j === undefined) {
    console.error("Too few arguments passed to I64 constructor: perhaps you meant PROTO.I64.fromNumber()");
    throw"Too few arguments passed to I64 constructor: perhaps you meant PROTO.I64.fromNumber()";
  }if(h === true) {
    h = -1
  }h || (h = 1);
  this.sign = h
};
PROTO.I64.prototype = {toNumber:function() {
  return(this.msw * 4294967296 + this.lsw) * this.sign
}, toString:function() {
  function e(o) {
    for(var q = "", u = 0;u < o;++u) {
      q += "0"
    }return q
  }
  var j = this.msw.toString(16), h = this.lsw.toString(16);
  return(this.sign == -1 ? "-" : "") + "0x" + e(8 - j.length) + j + e(8 - h.length) + h
}, equals:function(e) {
  return this.sign == e.sign && this.msw == e.msw && this.lsw == e.lsw
}, hash:function() {
  return this.sign * this.msw + "_" + this.lsw
}, convertToUnsigned:function() {
  var e;
  e = this.lsw;
  var j;
  if(this.sign < 0) {
    j = 2147483647 - this.msw;
    j += 2147483647;
    j += 2;
    e = 2147483647 - this.lsw;
    e += 2147483647;
    e += 2
  }else {
    j = this.msw
  }return new PROTO.I64(j, e, 1)
}, convertFromUnsigned:function() {
  if(this.msw >= 2147483648) {
    return new PROTO.I64(this.msw - 2147483648, this.lsw, -1)
  }return new PROTO.I64(this.msw, this.lsw, 1)
}, convertToZigzag:function() {
  var e;
  e = this.sign < 0 ? this.lsw * 2 + 1 : this.lsw * 2;
  var j = this.msw * 2;
  if(e > 4294967295) {
    j += 1;
    e -= 4294967296
  }return new PROTO.I64(j, e, 1)
}, convertFromZigzag:function() {
  if(this.msw & 1) {
    return new PROTO.I64(this.msw >>> 1, 2147483648 + (this.lsw >>> 1), this.lsw & 1 ? -1 : 1)
  }return new PROTO.I64(this.msw >>> 1, this.lsw >>> 1, this.lsw & 1 ? -1 : 1)
}, serializeToLEBase256:function() {
  for(var e = new Array(8), j = this.lsw, h = 0;h < 4;h++) {
    e[h] = j & 255;
    j >>= 8
  }j = this.msw;
  for(h = 4;h < 8;h++) {
    e[h] = j & 255;
    j >>= 8
  }return e
}, serializeToLEVar128:function() {
  for(var e = new Array(1), j = this.lsw, h = 0;h < 4;h++) {
    e[h] = j & 127;
    j >>>= 7;
    if(j == 0 && this.msw == 0) {
      return e
    }e[h] += 128
  }e[4] = j & 15 | (this.msw & 7) << 4;
  j = this.msw >>> 3;
  if(j == 0) {
    return e
  }e[4] += 128;
  for(h = 5;h < 10;h++) {
    e[h] = j & 127;
    j >>>= 7;
    if(j == 0) {
      return e
    }e[h] += 128
  }return e
}, unsigned_add:function(e) {
  var j = this.lsw + e.lsw;
  e = this.msw + e.msw;
  var h = j % 4294967296;
  j -= h;
  e += j / 4294967296;
  return new PROTO.I64(e, h, this.sign)
}, sub:function(e) {
  if(e.sign != this.sign) {
    return this.unsigned_add(e)
  }if(e.msw > this.msw || e.msw == this.msw && e.lsw > this.lsw) {
    var j = e.sub(this);
    j.sign = -this.sign;
    return j
  }j = this.lsw - e.lsw;
  e = this.msw - e.msw;
  if(j < 0) {
    j += 4294967296;
    e -= 1
  }return new PROTO.I64(e, j, this.sign)
}, add:function(e) {
  if(e.sign < 0 && this.sign >= 0) {
    return this.sub(new PROTO.I64(e.msw, e.lsw, -e.sign))
  }if(e.sign >= 0 && this.sign < 0) {
    return e.sub(new PROTO.I64(this.msw, this.lsw, -this.sign))
  }return this.unsigned_add(e)
}};
PROTO.I64.fromNumber = function(e) {
  var j = e < 0 ? -1 : 1;
  e *= j;
  var h = e % 4294967296;
  return new PROTO.I64((e - h) / 4294967296, h, j)
};
PROTO.I64.from32pair = function(e, j, h) {
  return new PROTO.I64(e, j, h)
};
PROTO.I64.parseLEVar128 = function(e) {
  for(var j = 0, h = false, o = 1, q = 0;!h && q < 5;q++) {
    var u = e.readByte();
    if(u >= 128) {
      u -= 128
    }else {
      h = true
    }j += o * u;
    o *= 128
  }j = j % 4294967296;
  var f = 0;
  o = 8;
  for(q = 0;!h && q < 5;q++) {
    u = e.readByte();
    if(u >= 128) {
      u -= 128
    }else {
      h = true
    }f += o * u;
    o *= 128
  }return new PROTO.I64(f % 4294967296, j, 1)
};
PROTO.I64.parseLEBase256 = function(e) {
  for(var j = 0, h = 1, o = 0;o < 4;o++) {
    var q = e.readByte();
    j += h * q;
    h *= 256
  }j = j;
  var u = 0;
  h = 1;
  for(o = 0;o < 4;o++) {
    q = e.readByte();
    u += h * q;
    h *= 256
  }return new PROTO.I64(u, j, 1)
};
PROTO.I64.ONE = new PROTO.I64.fromNumber(1);
PROTO.I64.ZERO = new PROTO.I64.fromNumber(0);
PROTO.BinaryParser = function(e, j) {
  this.bigEndian = e;
  this.allowExceptions = j
};
a = PROTO.BinaryParser.prototype;
a.encodeFloat = function(e, j, h) {
  var o, q = Math.pow(2, h - 1) - 1, u = -q + 1, f = u - j, g = isNaN(o = parseFloat(e)) || o == -Infinity || o == +Infinity ? o : 0, m = 0, p = 2 * q + 1 + j + 3, r = new Array(p), s = (o = g !== 0 ? 0 : o) < 0;
  o = Math.abs(o);
  var A = Math.floor(o), v = o - A, B;
  for(e = p;e;r[--e] = 0);for(e = q + 2;A && e;r[--e] = A % 2, A = Math.floor(A / 2));for(e = q + 1;v > 0 && e;(r[++e] = ((v *= 2) >= 1) - 0) && --v);for(e = -1;++e < p && !r[e];);if(r[(o = j - 1 + (e = (m = q + 1 - e) >= u && m <= q ? e + 1 : q + 1 - (m = u - 1))) + 1]) {
    if(!(B = r[o])) {
      for(v = o + 2;!B && v < p;B = r[v++]);
    }for(v = o + 1;B && --v >= 0;(r[v] = !r[v] - 0) && (B = 0));
  }for(e = e - 2 < 0 ? -1 : e - 3;++e < p && !r[e];);(m = q + 1 - e) >= u && m <= q ? ++e : m < u && (m != q + 1 - p && m < f && this.warn("encodeFloat::float underflow"), e = q + 1 - (m = u - 1));
  (A || g !== 0) && (this.warn(A ? "encodeFloat::float overflow" : "encodeFloat::" + g), m = q + 1, e = q + 2, g == -Infinity ? (s = 1) : isNaN(g) && (r[e] = 1));
  o = Math.abs(m + q);
  v = h + 1;
  for(h = "";--v;h = o % 2 + h, o = o >>= 1);v = o = 0;
  e = (h = (s ? "1" : "0") + h + r.slice(e, e + j).join("")).length;
  for(j = [];e;o += (1 << v) * h.charAt(--e), v == 7 && (j[j.length] = o, o = 0), v = (v + 1) % 8);return this.bigEndian ? j.reverse() : j
};
a.encodeInt = function(e, j) {
  var h = Math.pow(2, j), o = [];
  (e >= h || e < -(h >> 1)) && this.warn("encodeInt::overflow") && (e = 0);
  for(e < 0 && (e += h);e;o[o.length] = e % 256, e = Math.floor(e / 256));for(j = -(-j >> 3) - o.length;j--;);return this.bigEndian ? o.reverse() : o
};
a.decodeFloat = function(e, j, h) {
  e = new this.Buffer(this.bigEndian, e);
  PROTO.BinaryParser.prototype.checkBuffer.call(e, j + h + 1);
  var o = Math.pow(2, h - 1) - 1, q = PROTO.BinaryParser.prototype.readBits.call(e, j + h, 1);
  h = PROTO.BinaryParser.prototype.readBits.call(e, j, h);
  var u = 0, f = 2, g = e.buffer.length + (-j >> 3) - 1, m, p, r;
  do {
    m = e.buffer[++g];
    p = j % 8 || 8;
    for(r = 1 << p;r >>= 1;m & r && (u += 1 / f), f *= 2);
  }while(j -= p);
  return h == (o << 1) + 1 ? u ? NaN : q ? -Infinity : +Infinity : (1 + q * -2) * (h || u ? !h ? Math.pow(2, -o + 1) * u : Math.pow(2, h - o) * (1 + u) : 0)
};
a.decodeInt = function(e, j, h) {
  e = (new this.Buffer(this.bigEndian, e)).readBits(0, j);
  j = Math.pow(2, j);
  return h && e >= j / 2 ? e - j : e
};
a.Buffer = function(e, j) {
  this.bigEndian = e || 0;
  this.buffer = [];
  PROTO.BinaryParser.prototype.setBuffer.call(this, j)
};
a.readBits = function(e, j) {
  function h(m, p) {
    for(++p;--p;m = ((m %= 2147483648) & 1073741824) == 1073741824 ? m * 2 : (m - 1073741824) * 2 + 2147483647 + 1);return m
  }
  if(e < 0 || j <= 0) {
    return 0
  }PROTO.BinaryParser.prototype.checkBuffer.call(this, e + j);
  var o, q = e % 8, u = this.buffer.length - (e >> 3) - 1, f = this.buffer.length + (-(e + j) >> 3), g = u - f;
  for(e = (this.buffer[u] >> q & (1 << (g ? 8 - q : j)) - 1) + (g && (o = (e + j) % 8) ? (this.buffer[f++] & (1 << o) - 1) << (g-- << 3) - q : 0);g;e += h(this.buffer[f++], (g-- << 3) - q));return e
};
a.setBuffer = function(e) {
  if(e) {
    for(var j, h = j = e.length, o = this.buffer = new Array(j);h;o[j - h] = e[--h]);this.bigEndian && o.reverse()
  }
};
a.hasNeededBits = function(e) {
  return this.buffer.length >= -(-e >> 3)
};
a.checkBuffer = function(e) {
  if(!PROTO.BinaryParser.prototype.hasNeededBits.call(this, e)) {
    throw new Error("checkBuffer::missing bytes");
  }
};
a.warn = function(e) {
  if(this.allowExceptions) {
    throw new Error(e);
  }return 1
};
a.toSmall = function(e) {
  return this.decodeInt(e, 8, true)
};
a.fromSmall = function(e) {
  return this.encodeInt(e, 8, true)
};
a.toByte = function(e) {
  return this.decodeInt(e, 8, false)
};
a.fromByte = function(e) {
  return this.encodeInt(e, 8, false)
};
a.toShort = function(e) {
  return this.decodeInt(e, 16, true)
};
a.fromShort = function(e) {
  return this.encodeInt(e, 16, true)
};
a.toWord = function(e) {
  return this.decodeInt(e, 16, false)
};
a.fromWord = function(e) {
  return this.encodeInt(e, 16, false)
};
a.toInt = function(e) {
  return this.decodeInt(e, 32, true)
};
a.fromInt = function(e) {
  return this.encodeInt(e, 32, true)
};
a.toDWord = function(e) {
  return this.decodeInt(e, 32, false)
};
a.fromDWord = function(e) {
  return this.encodeInt(e, 32, false)
};
a.toFloat = function(e) {
  return this.decodeFloat(e, 23, 8)
};
a.fromFloat = function(e) {
  return this.encodeFloat(e, 23, 8)
};
a.toDouble = function(e) {
  return this.decodeFloat(e, 52, 11)
};
a.fromDouble = function(e) {
  return this.encodeFloat(e, 52, 11)
};
PROTO.binaryParser = new PROTO.BinaryParser(false, false);
PROTO.encodeUTF8 = function(e) {
  for(var j = e.length, h = [], o, q, u, f, g = 0;g < j;g++) {
    o = e.charCodeAt(g);
    if((o & 65408) == 0) {
      h.push(o)
    }else {
      if((o & 64512) == 55296) {
        q = e.charCodeAt(g + 1);
        if((q & 64512) == 56320) {
          o = ((o & 1023) << 10 | q & 1023) + 65536;
          g++
        }else {
          console.log("Error decoding surrogate pair: " + o + "; " + q)
        }
      }q = o & 255;
      u = o & 65280;
      f = o & 16711680;
      if(o <= 2047) {
        h.push(192 | u >> 6 | q >> 6);
        h.push(128 | q & 63)
      }else {
        if(o <= 65535) {
          h.push(224 | u >> 12);
          h.push(128 | u >> 6 & 63 | q >> 6);
          h.push(128 | q & 63)
        }else {
          if(o <= 1114111) {
            h.push(240 | f >> 18);
            h.push(128 | f >> 12 & 63 | u >> 12);
            h.push(128 | u >> 6 & 63 | q >> 6);
            h.push(128 | q & 63)
          }else {
            console.log("Error encoding to utf8: " + o + " is greater than U+10ffff");
            h.push("?".charCodeAt(0))
          }
        }
      }
    }
  }return h
};
PROTO.decodeUTF8 = function(e) {
  for(var j = e.length, h = "", o, q, u, f, g = 0;g < j;g++) {
    o = e[g];
    if((o & 128) != 0) {
      if((o & 248) == 240) {
        q = e[g + 1];
        u = e[g + 2];
        f = e[g + 3];
        if((q & 192) == 128 && (u & 192) == 128 && (f & 192) == 128) {
          o = (o & 7) << 18 | (q & 63) << 12 | (u & 63) << 6 | f & 63;
          g += 3
        }else {
          console.log("Error decoding from utf8: " + o + "," + q + "," + u + "," + f);
          continue
        }
      }else {
        if((o & 240) == 224) {
          q = e[g + 1];
          u = e[g + 2];
          if((q & 192) == 128 && (u & 192) == 128) {
            o = (o & 15) << 12 | (q & 63) << 6 | u & 63;
            g += 2
          }else {
            console.log("Error decoding from utf8: " + o + "," + q + "," + u);
            continue
          }
        }else {
          if((o & 224) == 192) {
            q = e[g + 1];
            if((q & 192) == 128) {
              o = (o & 31) << 6 | q & 63;
              g += 1
            }else {
              console.log("Error decoding from utf8: " + o + "," + q);
              continue
            }
          }else {
            console.log("Error decoding from utf8: " + o + " encountered not in multi-byte sequence");
            continue
          }
        }
      }
    }if(o <= 65535) {
      h += String.fromCharCode(o)
    }else {
      if(o > 65535 && o <= 1114111) {
        o -= 65536;
        h += String.fromCharCode(55296 | o >> 10) + String.fromCharCode(56320 | o & 1023)
      }else {
        console.log("Error encoding surrogate pair: " + o + " is greater than U+10ffff")
      }
    }
  }return h
};
PROTO.Stream = function() {
  this.read_pos_ = this.write_pos_ = 0
};
PROTO.Stream.prototype = {read:function(e) {
  for(var j = [], h = 0;h < e;++h) {
    var o = this.readByte();
    if(o === null) {
      break
    }j.push(o)
  }return j
}, write:function(e) {
  for(var j = 0;j < e.length;j++) {
    this.writeByte(e[j])
  }
}, readByte:function() {
  return null
}, writeByte:function() {
  this.write_pos_ += 1
}, valid:function() {
  return false
}};
PROTO.ByteArrayStream = function(e) {
  this.array_ = e || [];
  this.read_pos_ = 0;
  this.write_pos_ = this.array_.length
};
PROTO.ByteArrayStream.prototype = new PROTO.Stream;
a = PROTO.ByteArrayStream.prototype;
a.read = function(e) {
  var j = this.array_.slice(this.read_pos_, this.read_pos_ + e);
  this.read_pos_ += e;
  return j
};
a.write = function(e) {
  Array.prototype.push.apply(this.array_, e);
  this.write_pos_ = this.array_.length
};
a.readByte = function() {
  return this.array_[this.read_pos_++]
};
a.writeByte = function(e) {
  this.array_.push(e);
  this.write_pos_ = this.array_.length
};
a.valid = function() {
  return this.read_pos_ < this.array_.length
};
a.getArray = function() {
  return this.array_
};
(function() {
  var e = [62, -1, 62, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, 63, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51], j = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", 
  "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"], h = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "_"];
  PROTO.Base64Stream = function(o) {
    this.alphabet = j;
    this.string_ = o || "";
    this.read_incomplete_value_ = this.read_pos_ = 0;
    this.read_needed_bits_ = 8;
    this.write_incomplete_value_ = this.write_extra_bits_ = 0;
    this.fixString()
  };
  PROTO.Base64Stream.prototype = new PROTO.Stream;
  PROTO.Base64Stream.prototype.setURLSafe = function() {
    this.alphabet = h
  };
  PROTO.Base64Stream.prototype.fixString = function() {
    var o = this.string_.length;
    if(this.string_[o - 1] == "=") {
      var q = 4, u = 2;
      if(this.string_[o - u] == "=") {
        q = 2;
        u = 3
      }this.write_extra_bits_ = q;
      this.write_incomplete_value_ = e[this.string_.charCodeAt(o - u) - 43];
      this.write_incomplete_value_ >>= 6 - q;
      this.string_ = this.string_.substring(0, o - u)
    }
  };
  PROTO.Base64Stream.prototype.readByte = function() {
    for(var o, q = this.read_needed_bits_;o === undefined || o == -1;) {
      if(this.read_pos_ >= this.string_.length) {
        if(this.valid()) {
          o = this.write_incomplete_value_ << 6 - q;
          this.read_pos_++;
          break
        }else {
          return null
        }
      }o = e[this.string_.charCodeAt(this.read_pos_++) - 43]
    }if(q == 8) {
      this.read_incomplete_value_ = o;
      this.read_needed_bits_ = 2;
      return this.readByte()
    }var u = this.read_incomplete_value_ << q;
    u |= o >> 6 - q;
    this.read_incomplete_value_ = o & (1 << 6 - q) - 1;
    this.read_needed_bits_ += 2;
    return u
  };
  PROTO.Base64Stream.prototype.writeByte = function(o) {
    this.write_extra_bits_ += 2;
    var q = this.write_extra_bits_;
    this.string_ += this.alphabet[o >> q | this.write_incomplete_value_ << 8 - q];
    this.write_incomplete_value_ = o & (1 << q) - 1;
    if(q == 6) {
      this.string_ += this.alphabet[this.write_incomplete_value_];
      this.write_incomplete_value_ = this.write_extra_bits_ = 0
    }if(this.string_.length % 77 == 76) {
      this.string_ += "\n"
    }
  };
  PROTO.Base64Stream.prototype.getString = function() {
    var o = this.string_, q = this.write_extra_bits_;
    if(q > 0) {
      o += this.alphabet[this.write_incomplete_value_ << 6 - q];
      if(q == 2) {
        o += "=="
      }else {
        if(q == 4) {
          o += "="
        }
      }
    }return o
  };
  PROTO.Base64Stream.prototype.valid = function() {
    return this.read_pos_ < this.string_.length || this.read_pos_ == this.string_.length && this.write_extra_bits_
  }
})();
PROTO.array = function() {
  function e(j, h) {
    this.datatype_ = j.type();
    this.length = 0;
    if(h instanceof Array) {
      for(j = 0;j < h.length;++j) {
        this.push(h[j])
      }
    }
  }
  e.IsInitialized = function(j) {
    return j.length > 0
  };
  e.prototype = {};
  e.prototype.push = function() {
    if(arguments.length === 0) {
      if(this.datatype_.composite) {
        var j = new this.datatype_;
        return this[this.length++] = j
      }else {
        throw"Called add(undefined) for a non-composite";
      }
    }else {
      for(var h = 0;h < arguments.length;h++) {
        j = this.datatype_.Convert(arguments[h]);
        if(this.datatype_.FromProto) {
          j = this.datatype_.FromProto(j)
        }this[this.length++] = j
      }
    }return arguments[0]
  };
  e.prototype.set = function(j, h) {
    h = this.datatype_.Convert(h);
    if(this.datatype_.FromProto) {
      h = this.datatype_.FromProto(h)
    }if(j < this.length && j >= 0) {
      this[j] = h
    }else {
      if(j == this.length) {
        this[this.length++] = h
      }else {
        throw"Called ProtoArray.set with index " + j + " higher than length " + this.length;
      }
    }return h
  };
  e.prototype.clear = function() {
    this.length = 0
  };
  return e
}();
PROTO.string = {Convert:function(e) {
  return"" + e
}, wiretype:PROTO.wiretypes.lengthdelim, SerializeToStream:function(e, j) {
  e = PROTO.encodeUTF8(e);
  return PROTO.bytes.SerializeToStream(e, j)
}, ParseFromStream:function(e) {
  e = PROTO.bytes.ParseFromStream(e);
  return PROTO.decodeUTF8(e)
}, toString:function(e) {
  return e
}};
PROTO.bytes = {Convert:function(e) {
  if(e instanceof Array) {
    return e
  }else {
    if(e instanceof PROTO.ByteArrayStream) {
      return e.getArray()
    }else {
      if(e.SerializeToStream) {
        var j = new PROTO.ByteArrayStream;
        e.SerializeToStream(j);
        return j.getArray()
      }else {
        throw"Not a Byte Array: " + e;
      }
    }
  }
}, wiretype:PROTO.wiretypes.lengthdelim, SerializeToStream:function(e, j) {
  PROTO.int32.SerializeToStream(e.length, j);
  j.write(e)
}, ParseFromStream:function(e) {
  var j = PROTO.int32.ParseFromStream(e);
  return e.read(j)
}, toString:function(e) {
  return"[" + e + "]"
}};
(function() {
  function e(F, L, O) {
    return{Convert:F, wiretype:0, SerializeToStream:L, ParseFromStream:O, toString:function(P) {
      return"" + P
    }}
  }
  function j(F) {
    if(F == NaN) {
      throw"not a number: " + F;
    }F = Math.round(F);
    if(F < 0) {
      throw"uint32/fixed32 does not allow negative: " + F;
    }if(F > 4294967295) {
      throw"uint32/fixed32 out of bounds: " + F;
    }return F
  }
  function h(F) {
    if(F == NaN) {
      throw"not a number: " + F;
    }F = Math.round(F);
    if(F > 2147483647 || F < -2147483648) {
      throw"sfixed32/[s]int32 out of bounds: " + F;
    }return F
  }
  function o(F, L) {
    if(F < 0) {
      F += 4294967296
    }for(var O = new Array(4), P = 0;P < 4;P++) {
      O[P] = F % 256;
      F >>>= 8
    }L.write(O)
  }
  function q(F) {
    for(var L = 0, O = 1, P = 0;P < 4;P++) {
      L += O * F.readByte();
      O *= 256
    }return L
  }
  function u(F) {
    F = q(F);
    if(F > 2147483647) {
      F -= 4294967296
    }return F
  }
  function f(F, L) {
    if(F < 0) {
      A(PROTO.I64.fromNumber(F), L)
    }else {
      for(var O = 0;O == 0 || F && O < 5;O++) {
        var P = F % 128;
        F >>>= 7;
        if(F) {
          P += 128
        }L.writeByte(P)
      }
    }
  }
  function g(F, L) {
    if(F < 0) {
      F = -F * 2 - 1
    }else {
      F *= 2
    }f(F, L)
  }
  function m(F) {
    for(var L = 0, O = false, P = 1, S = 0;!O && S < 5;S++) {
      var T = F.readByte();
      if(T === undefined) {
        console.log("read undefined byte from stream: n is " + L);
        break
      }if(T < 128) {
        O = true
      }L += P * (T & (S == 4 ? 15 : 127));
      P *= 128
    }return L
  }
  function p(F) {
    F = m(F);
    if(F > 2147483647) {
      F -= 2147483647;
      F -= 2147483647;
      F -= 2
    }return F
  }
  function r(F) {
    F = m(F);
    if(F & 1) {
      return(F + 1) / -2
    }return F / 2
  }
  function s(F) {
    if(F instanceof PROTO.I64) {
      return F
    }throw"64-bit integers must be PROTO.I64 objects!";
  }
  function A(F, L) {
    L.write(F.convertToUnsigned().serializeToLEVar128())
  }
  function v(F, L) {
    L.write(F.convertToZigzag().serializeToLEVar128())
  }
  function B(F, L) {
    L.write(F.serializeToLEVar128())
  }
  function C(F, L) {
    L.write(F.convertToUnsigned().serializeToLEBase256())
  }
  function E(F, L) {
    L.write(F.serializeToLEBase256())
  }
  function H(F) {
    return PROTO.I64.parseLEBase256(F).convertFromUnsigned()
  }
  function J(F) {
    return PROTO.I64.parseLEBase256(F)
  }
  function M(F) {
    return PROTO.I64.parseLEVar128(F).convertFromZigzag()
  }
  function K(F) {
    return PROTO.I64.parseLEVar128(F).convertFromUnsigned()
  }
  function N(F) {
    return PROTO.I64.parseLEVar128(F)
  }
  function Q(F) {
    var L = parseFloat(F);
    if(L == NaN) {
      throw"not a number: " + F;
    }return L
  }
  function R(F, L) {
    L.write(PROTO.binaryParser.fromFloat(F))
  }
  function D(F) {
    F = F.read(4);
    return PROTO.binaryParser.toFloat(F)
  }
  function G(F, L) {
    L.write(PROTO.binaryParser.fromDouble(F))
  }
  function I(F) {
    F = F.read(8);
    return PROTO.binaryParser.toDouble(F)
  }
  PROTO.sfixed32 = e(h, o, q);
  PROTO.fixed32 = e(j, o, u);
  PROTO.sfixed32.wiretype = PROTO.wiretypes.fixed32;
  PROTO.fixed32.wiretype = PROTO.wiretypes.fixed32;
  PROTO.int32 = e(h, f, p);
  PROTO.sint32 = e(h, g, r);
  PROTO.uint32 = e(j, f, m);
  PROTO.sfixed64 = e(s, C, H);
  PROTO.fixed64 = e(s, E, J);
  PROTO.sfixed64.wiretype = PROTO.wiretypes.fixed64;
  PROTO.fixed64.wiretype = PROTO.wiretypes.fixed64;
  PROTO.int64 = e(s, A, K);
  PROTO.sint64 = e(s, v, M);
  PROTO.uint64 = e(s, B, N);
  PROTO.bool = e(function(F) {
    return F ? true : false
  }, f, m);
  PROTO.Float = e(Q, R, D);
  PROTO.Double = e(Q, G, I);
  PROTO.Float.wiretype = PROTO.wiretypes.fixed32;
  PROTO.Double.wiretype = PROTO.wiretypes.fixed64
})();
PROTO.mergeProperties = function(e, j, h) {
  var o = {};
  for(var q in e) {
    o[e[q].id] = q
  }for(var u, f, g, m, p, r = {};j.valid();) {
    u = PROTO.int32.ParseFromStream(j);
    f = u % 8;
    u >>>= 3;
    g = (q = (p = o[u]) && e[p]) && q.type();
    m = undefined;
    switch(f) {
      case PROTO.wiretypes.varint:
        if(q && g.wiretype == PROTO.wiretypes.varint) {
          m = g.ParseFromStream(j)
        }else {
          PROTO.int64.ParseFromStream(j)
        }break;
      case PROTO.wiretypes.fixed64:
        if(q && g.wiretype == PROTO.wiretypes.fixed64) {
          m = g.ParseFromStream(j)
        }else {
          PROTO.fixed64.ParseFromStream(j)
        }break;
      case PROTO.wiretypes.lengthdelim:
        if(q) {
          if(g.wiretype != PROTO.wiretypes.lengthdelim) {
            var s;
            if(g.cardinality > 1) {
              if(r[p] === undefined) {
                r[p] = []
              }s = r[p]
            }u = PROTO.bytes.ParseFromStream(j);
            f = new PROTO.ByteArrayStream(u);
            for(var A = 0;A < u.length && f.valid();A++) {
              var v = g.ParseFromStream(f);
              if(g.cardinality > 1) {
                s.push(v);
                if(s.length == g.cardinality) {
                  if(q.multiplicity == PROTO.repeated) {
                    h[p].push(s)
                  }else {
                    h[p] = g.Convert(s)
                  }r[p] = [];
                  s = r[p]
                }
              }else {
                h[p].push(v)
              }
            }
          }else {
            m = g.ParseFromStream(j)
          }
        }else {
          PROTO.bytes.ParseFromStream(j)
        }break;
      case PROTO.wiretypes.fixed32:
        if(q && g.wiretype == PROTO.wiretypes.fixed32) {
          m = g.ParseFromStream(j)
        }else {
          PROTO.fixed32.ParseFromStream(j)
        }break;
      default:
        console.log("ERROR: Unknown type " + f + " for " + u);
        break
    }
    if(m !== undefined) {
      if(h[p] === undefined && g.cardinality > 1) {
        h[p] = {}
      }if(g.cardinality > 1) {
        if(r[p] === undefined) {
          r[p] = [];
          s = r[p]
        }s.push(m);
        if(s.length == g.cardinality) {
          if(q.multiplicity == PROTO.repeated) {
            h[p].push(s)
          }else {
            s = g.Convert(s);
            if(!PROTO.DefineProperty && g.FromProto) {
              s = g.FromProto(s)
            }h[p] = s
          }r[p] = undefined
        }
      }else {
        if(q.multiplicity === PROTO.repeated) {
          h[p].push(m)
        }else {
          m = g.Convert(m);
          if(!PROTO.DefineProperty && g.FromProto) {
            m = g.FromProto(m)
          }h[p] = m
        }
      }
    }
  }
};
PROTO.serializeTupleProperty = function(e, j, h) {
  var o = e.id, q = e.type().wiretype, u = o * 8 + q;
  if(q != PROTO.wiretypes.lengthdelim && e.options.packed) {
    q = [];
    u = new PROTO.ByteArrayStream(q);
    if(e.multiplicity == PROTO.repeated) {
      for(var f = 0;f < h.length;f++) {
        for(var g = e.type().Convert(h[f]), m = 0;m < e.type().cardinality;++m) {
          e.type().SerializeToStream(g[m], u)
        }
      }
    }else {
      g = e.type().Convert(h);
      for(m = 0;m < e.type().cardinality;++m) {
        e.type().SerializeToStream(g[m], u)
      }
    }u = o * 8 + PROTO.wiretypes.lengthdelim;
    PROTO.int32.SerializeToStream(u, j);
    PROTO.bytes.SerializeToStream(q, j)
  }else {
    if(e.multiplicity == PROTO.repeated) {
      for(f = 0;f < h.length;f++) {
        g = e.type().Convert(h[f]);
        for(m = 0;m < e.type().cardinality;++m) {
          PROTO.int32.SerializeToStream(u, j);
          e.type().SerializeToStream(g[m], j)
        }
      }
    }else {
      g = e.type().Convert(h);
      for(m = 0;m < e.type().cardinality;++m) {
        PROTO.int32.SerializeToStream(u, j);
        e.type().SerializeToStream(g[m], j)
      }
    }
  }
};
PROTO.serializeProperty = function(e, j, h) {
  var o = e.id;
  if(e.type()) {
    if(e.type().cardinality > 1) {
      PROTO.serializeTupleProperty(e, j, h)
    }else {
      var q = e.type().wiretype, u = o * 8 + q;
      if(e.multiplicity == PROTO.repeated) {
        if(q != PROTO.wiretypes.lengthdelim && e.options.packed) {
          q = [];
          u = new PROTO.ByteArrayStream(q);
          for(var f = 0;f < h.length;f++) {
            var g = e.type().Convert(h[f]);
            e.type().SerializeToStream(g, u)
          }u = o * 8 + PROTO.wiretypes.lengthdelim;
          PROTO.int32.SerializeToStream(u, j);
          PROTO.bytes.SerializeToStream(q, j)
        }else {
          for(f = 0;f < h.length;f++) {
            PROTO.int32.SerializeToStream(u, j);
            g = e.type().Convert(h[f]);
            e.type().SerializeToStream(g, j)
          }
        }
      }else {
        PROTO.int32.SerializeToStream(u, j);
        g = e.type().Convert(h);
        e.type().SerializeToStream(g, j)
      }
    }
  }
};
PROTO.Message = function(e, j) {
  var h = function() {
    this.properties_ = h.properties_;
    this.values_ = PROTO.DefineProperty ? {} : this;
    this.Clear();
    this.message_type_ = e
  };
  h.properties_ = {};
  for(var o in j) {
    if(j[o].isType) {
      h[o] = j[o]
    }else {
      h.properties_[o] = j[o]
    }
  }h.isType = true;
  h.composite = true;
  h.wiretype = PROTO.wiretypes.lengthdelim;
  h.IsInitialized = function(u) {
    return u && u.IsInitialized()
  };
  h.Convert = function(u) {
    if(!(u instanceof h)) {
      throw"Value not instanceof " + e + ": " + typeof u + " : " + u;
    }return u
  };
  h.SerializeToStream = function(u, f) {
    var g = [], m = new PROTO.ByteArrayStream(g);
    u.SerializeToStream(m);
    return PROTO.bytes.SerializeToStream(g, f)
  };
  h.ParseFromStream = function(u) {
    u = PROTO.bytes.ParseFromStream(u);
    u = new PROTO.ByteArrayStream(u);
    var f = new h;
    f.ParseFromStream(u);
    return f
  };
  h.prototype = {computeHasFields:function() {
    var u = {};
    for(var f in this.properties_) {
      if(this.HasField(f)) {
        u[f] = true
      }
    }return u
  }, Clear:function() {
    for(var u in this.properties_) {
      this.ClearField(u)
    }
  }, IsInitialized:function() {
    var u = false;
    for(var f in this.properties_) {
      u = true;
      if(this.values_[f] !== undefined) {
        var g = this.properties_[f];
        if(g.type()) {
          if(g.multiplicity == PROTO.repeated) {
            if(PROTO.array.IsInitialized(this.values_[f])) {
              return true
            }
          }else {
            if(!g.type().IsInitialized || g.type().IsInitialized(this.values_[f])) {
              return true
            }
          }
        }
      }
    }if(!u) {
      return true
    }return false
  }, ParseFromStream:function(u) {
    this.Clear();
    this.MergeFromStream(u)
  }, MergeFromStream:function(u) {
    PROTO.mergeProperties(this.properties_, u, this.values_)
  }, SerializeToStream:function(u) {
    var f = this.computeHasFields();
    for(var g in f) {
      PROTO.serializeProperty(this.properties_[g], u, this.values_[g])
    }
  }, SerializeToArray:function(u) {
    u = new PROTO.ByteArrayStream(u);
    this.SerializeToStream(u);
    return u.getArray()
  }, MergeFromArray:function(u) {
    this.MergeFromStream(new PROTO.ByteArrayStream(u))
  }, ParseFromArray:function(u) {
    this.Clear();
    this.MergeFromArray(u)
  }, ClearField:function(u) {
    var f = this.properties_[u];
    if(f.multiplicity == PROTO.repeated) {
      this.values_[u] = new PROTO.array(f)
    }else {
      f.type();
      delete this.values_[u]
    }
  }, ListFields:function() {
    var u = [], f = this.computeHasFields();
    for(var g in f) {
      u.push(g)
    }return u
  }, GetField:function(u) {
    var f = this.values_[u];
    u = this.properties_[u].type();
    if(f && u.FromProto) {
      return u.FromProto(f)
    }return f
  }, SetField:function(u, f) {
    if(f === undefined || f === null) {
      this.ClearField(u)
    }else {
      var g = this.properties_[u];
      if(g.multiplicity == PROTO.repeated) {
        this.ClearField(u);
        for(g = 0;g < f.length;g++) {
          this.values_[u].push(g)
        }
      }else {
        this.values_[u] = g.type().Convert(f)
      }
    }
  }, HasField:function(u) {
    if(this.values_[u] !== undefined) {
      var f = this.properties_[u];
      if(!f.type()) {
        return false
      }if(f.multiplicity == PROTO.repeated) {
        return PROTO.array.IsInitialized(this.values_[u])
      }else {
        if(!f.type().IsInitialized || f.type().IsInitialized(this.values_[u])) {
          return true
        }
      }
    }return false
  }, formatValue:function(u, f, g, m) {
    f = f + g;
    g = this.properties_[g].type();
    if(g.composite) {
      f += " " + m.toString(u + 1)
    }else {
      if(typeof m == "string") {
        u = m;
        u = u.replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r");
        f += ': "' + u + '"\n'
      }else {
        if(g.FromProto) {
          m = g.FromProto(m)
        }if(g.toString) {
          u = g.toString(m);
          f += ": " + u + "\n"
        }else {
          f += ": " + m + "\n"
        }
      }
    }return f
  }, toString:function(u) {
    var f = "", g = "";
    if(u) {
      g = "{\n";
      for(var m = 0;m < u * 2;m++) {
        f += " "
      }
    }else {
      u = 0
    }for(var p in this.properties_) {
      if(this.properties_[p].type()) {
        if(this.HasField(p)) {
          if(this.properties_[p].multiplicity == PROTO.repeated) {
            var r = this.values_[p];
            for(m = 0;m < r.length;m++) {
              g += this.formatValue(u, f, p, r[m])
            }
          }else {
            g += this.formatValue(u, f, p, this.values_[p])
          }
        }
      }
    }if(u) {
      g += "}\n"
    }return g
  }};
  if(PROTO.DefineProperty !== undefined) {
    for(var q in h.properties_) {
      (function(u) {
        PROTO.DefineProperty(h.prototype, u, function() {
          return this.GetField(u)
        }, function(f) {
          this.SetField(u, f)
        })
      })(q)
    }
  }return h
};
PROTO.Enum = function(e, j, h) {
  h || (h = 32);
  var o = {};
  h = {};
  h.isType = true;
  for(var q in j) {
    o[j[q]] = q;
    h[q] = j[q];
    h[j[q]] = q
  }h.values = j;
  h.reverseValues = o;
  h.Convert = function(u) {
    if(typeof u == "number") {
      return u
    }if(j[u] !== undefined) {
      return j[u]
    }throw"Not a valid " + e + " enumeration value: " + u;
  };
  h.toString = function(u) {
    if(o[u]) {
      return o[u]
    }return"" + u
  };
  h.ParseFromStream = function(u, f) {
    return PROTO.int32.ParseFromStream(u, f)
  };
  h.SerializeToStream = function(u, f) {
    return PROTO.int32.SerializeToStream(u, f)
  };
  h.wiretype = PROTO.wiretypes.varint;
  return h
};
PROTO.Flags = function(e, j, h) {
  return PROTO.Enum(j, h, e)
};
PROTO.Extend = function(e, j) {
  for(var h in j) {
    e.properties_[h] = j[h]
  }return e
};
if(typeof console == "undefined") {
  console = {}
}if(typeof console.log == "undefined") {
  console.log = function(e) {
    document && document.body && document.body.appendChild(document.createTextNode(e + "..."))
  }
};var PBJ = {};
function vectorGenerator(e, j, h) {
  h || (h = false);
  j = {Convert:function(o) {
    if(o instanceof Array && o.length == e) {
      return o
    }else {
      if(o instanceof Array && h && o.length == e + 1) {
        var q = o.slice(0, e);
        if(o[e] < 0) {
          q[0] += 3
        }return q
      }else {
        console.error("Vector_in_invalid_format: " + o + "; expect " + e + " elements.");
        return new Array(e)
      }
    }
  }, toString:function(o) {
    for(var q = "<" + o[0], u = 1;u < e + (h ? 1 : 0);u++) {
      q += ", " + o[u]
    }q += ">";
    return q
  }, wiretype:j.wiretype, SerializeToStream:j.SerializeToStream, ParseFromStream:j.ParseFromStream, cardinality:e};
  if(h) {
    if(e == 2) {
      j.FromProto = function(o) {
        var q = o[0];
        o = o[1];
        var u = q > 1.5 || o > 1.5 ? -1 : 1;
        if(q > 1.5) {
          q -= 3
        }if(o > 1.5) {
          o -= 3
        }return[q, o, u * Math.sqrt(1 - q * q - o * o)]
      }
    }else {
      if(e == 3) {
        j.FromProto = function(o) {
          var q = o[0], u = o[1];
          o = o[2];
          var f = q > 1.5 || u > 1.5 || o > 1.5 ? -1 : 1;
          if(q > 1.5) {
            q -= 3
          }if(u > 1.5) {
            u -= 3
          }if(o > 1.5) {
            o -= 3
          }return[q, u, o, f * Math.sqrt(1 - q * q - u * u - o * o)]
        }
      }
    }
  }return j
}
PBJ.uint8 = PROTO.uint32;
PBJ.uint16 = PROTO.uint32;
PBJ.int8 = PROTO.int32;
PBJ.int16 = PROTO.int32;
PBJ.sint8 = PROTO.sint32;
PBJ.sint16 = PROTO.sint32;
PBJ.vector2d = vectorGenerator(2, PROTO.Double);
PBJ.vector2f = vectorGenerator(2, PROTO.Float);
PBJ.vector3d = vectorGenerator(3, PROTO.Double);
PBJ.vector3f = vectorGenerator(3, PROTO.Float);
PBJ.vector4d = vectorGenerator(4, PROTO.Double);
PBJ.vector4f = vectorGenerator(4, PROTO.Float);
PBJ.normal = vectorGenerator(2, PROTO.Float, true);
PBJ.quaternion = vectorGenerator(3, PROTO.Float, true);
PBJ.duration = PROTO.cloneType(PROTO.sfixed64);
PBJ.duration.Convert = function(e) {
  return e instanceof PROTO.I64 ? e : PROTO.I64.fromNumber(e * 1E3)
};
PBJ.duration.FromProto = function(e) {
  return e.toNumber() / 1E3
};
PBJ.time = PROTO.cloneType(PROTO.fixed64);
PBJ.time.Convert = function(e) {
  if(e instanceof Date) {
    e = e.getTime() * 1E3
  }else {
    if(e instanceof PROTO.I64) {
      return e
    }
  }return PROTO.I64.fromNumber(e)
};
PBJ.time.toString = function(e) {
  var j;
  if(e instanceof PROTO.I64) {
    var h = e.toNumber();
    j = Math.floor(h / 1E3);
    var o = Math.floor(h / 1E6);
    e = e.sub(PROTO.I64.fromNumber(o * 1E6)).toNumber()
  }else {
    j = e;
    h = e * 1E3;
    o = Math.floor(j / 1E3);
    e = h - o * 1E6
  }if(e < 0) {
    e += 1E6
  }return"[" + (new Date(j)).toUTCString() + "]." + (1E6 + e).toString().substr(1)
};
PBJ.time.FromProto = function(e) {
  return e.toNumber() / 1E3
};
(function() {
  function e(f) {
    if(f >= h && f < h + 10) {
      return f - h
    }else {
      if(f >= o && f < o + 6) {
        return 10 + (f - o)
      }else {
        if(f >= q && f < q + 6) {
          return 10 + (f - q)
        }
      }
    }return 0
  }
  function j(f, g) {
    for(var m = new Array(g), p = f.length, r = 0, s = 0;r < p || s < g;r += 2, s++) {
      var A, v = f.charCodeAt(r);
      if(v == u) {
        r++;
        v = f.charCodeAt(r)
      }A = f.charCodeAt(r + 1);
      m[s] = e(v) * 16 + e(A)
    }return m
  }
  var h = "0".charCodeAt(0), o = "a".charCodeAt(0), q = "A".charCodeAt(0), u = "-".charCodeAt(0);
  PBJ.sha256 = PROTO.cloneType(PROTO.bytes);
  PBJ.sha256.Convert = function(f) {
    if(f instanceof Array) {
      return PROTO.bytes.Convert(f)
    }return j(f, 32)
  };
  PBJ.sha256.toString = function(f) {
    if(typeof f == "string") {
      return f
    }for(var g = "", m = 0;m < f.length && m < 32;m++) {
      g += (256 + f[m]).toString(16).substr(1)
    }for(;g.length < 64;) {
      g += "0"
    }return g
  };
  PBJ.sha256.FromProto = PBJ.sha256.toString;
  PBJ.uuid = PROTO.cloneType(PROTO.bytes);
  PBJ.uuid.Convert = function(f) {
    if(f instanceof Array) {
      return PROTO.bytes.Convert(f)
    }return j(f, 16)
  };
  PBJ.uuid.toString = function(f) {
    if(typeof f == "string") {
      return f
    }for(var g = "", m = 0;m < 16;m++) {
      if(m == 4 || m == 6 || m == 8 || m == 10) {
        g += "-"
      }g += m >= f.length ? "00" : (256 + f[m]).toString(16).substr(1)
    }return g
  };
  PBJ.uuid.FromProto = PBJ.uuid.toString
})();
PBJ.angle = PROTO.Float;
PBJ.boundingsphere3f = vectorGenerator(4, PROTO.Float);
PBJ.boundingsphere3d = vectorGenerator(4, PROTO.Double);
PBJ.boundingbox3f3f = vectorGenerator(6, PROTO.Float);
PBJ.boundingbox3d3f = vectorGenerator(6, PROTO.Double);if(typeof GLGE == "undefined") {
  GLGE = {}
}(function(e) {
  function j() {
    var h = e.Vec([1, 2, 3, 4]), o = e.Vec4(e.getVec4(h, 3), e.get1basedVec4(h, 3), e.getVec4(h, 1), e.getVec4(h, 0));
    h = e.identMatrix();
    o = e.mulMat4Vec4(h, o);
    if(e.getVec4(o, 0) != 4 || e.getVec4(o, 1) != 3 || e.getVec4(o, 2) != 2 || e.getVec4(o, 3) != 1) {
      throw"Unit Test 1 failed MatVecMul " + o;
    }o = e.Mat4([3, 4, 5, 0, 0.5, 0.75, 0, 0, 0.75, 0.5, 0, 0, 0.25, 0.25, 1, 1]);
    var q = e.Mat4([2, 1, 8, 2, 1, 4, 3, 2, 1, 0.5, 6.5, 2, 8, 3, 1, 0.25]), u = e.mulMat4(o, q), f = e.Mat4([15, 21.5, 68.5, 24, 1.75, 3.5, 6.25, 2.5, 2, 2.75, 7.5, 2.5, 9.75, 4.75, 10.25, 3.25]);
    for(q = 0;q < 4;++q) {
      for(var g = 0;g < 4;++g) {
        var m = e.getMat4(u, q, g) - e.getMat4(f, q, g);
        if(!(m < 1.0E-6 && m > -1.0E-6)) {
          throw"Unit Test 1 failed Multiplication " + e.getMat4(u, q, g) + " != " + e.getMat4(f, q, g);
        }
      }
    }q = e.inverseMat4(o);
    u = e.mulMat4(o, q);
    e.mulMat4(q, o);
    for(q = 0;q < 4;++q) {
      for(g = 0;g < 4;++g) {
        m = e.getMat4(u, q, g) - e.getMat4(h, q, g);
        if(!(m < 1.0E-4 && m > -1.0E-4)) {
          throw"Unit Test 1 failed Inverse " + e.getMat4(u, q, g) + " != " + e.getMat4(h, q, g);
        }
      }
    }
  }
  e.Vec = function(h) {
    return h.slice(0)
  };
  e.Vec3 = function(h, o, q) {
    return[h, o, q]
  };
  e.Vec4 = function(h, o, q, u) {
    return[h, o, q, u]
  };
  e.get1basedVec4 = function(h, o) {
    return h[o - 1]
  };
  e.get1basedVec3 = function(h, o) {
    return h[o - 1]
  };
  e.getVec4 = function(h, o) {
    return h[o]
  };
  e.getVec3 = function(h, o) {
    return h[o]
  };
  e.addVec4 = function(h, o) {
    return[h[0] + o[0], h[1] + o[1], h[2] + o[2], h[3] + o[3]]
  };
  e.addVec3 = function(h, o) {
    return[h[0] + o[0], h[1] + o[1], h[2] + o[2]]
  };
  e.subVec4 = function(h, o) {
    return[h[0] - o[0], h[1] - o[1], h[2] - o[2], h[3] - o[3]]
  };
  e.subVec3 = function(h, o) {
    return[h[0] - o[0], h[1] - o[1], h[2] - o[2]]
  };
  e.dotVec3 = function(h, o) {
    return h[0] * o[0] + h[1] * o[1] + h[2] * o[2]
  };
  e.dotVec4 = function(h, o) {
    return h[0] * o[0] + h[1] * o[1] + h[2] * o[2] + h[3] * o[3]
  };
  e.scaleVec4 = function(h, o) {
    return[h[0] * o, h[1] * o, h[2] * o, h[3] * o]
  };
  e.scaleVec3 = function(h, o) {
    return[h[0] * o, h[1] * o, h[2] * o]
  };
  e.crossVec3 = function(h, o) {
    return[h[1] * o[2] - h[2] * o[1], h[2] * o[0] - h[0] * o[2], h[0] * o[1] - h[1] * o[0]]
  };
  e.toUnitVec3 = function(h) {
    var o = h[0] * h[0] + h[1] * h[1] + h[2] * h[2], q = 1;
    if(o > 0) {
      q = Math.pow(o, 0.5)
    }return[h[0] / q, h[1] / q, h[2] / q]
  };
  e.toUnitVec4 = function(h) {
    var o = h[0] * h[0] + h[1] * h[1] + h[2] * h[2] + h[3] * h[3], q = 1;
    if(o > 0) {
      q = Math.pow(o, 0.5)
    }return[h[0] / q, h[1] / q, h[2] / q, h[3] / q]
  };
  e.lengthVec3 = function(h) {
    return Math.pow(h[0] * h[0] + h[1] * h[1] + h[2] * h[2], 0.5)
  };
  e.distanceVec3 = function(h, o) {
    return e.lengthVec3(e.subVec3(h, o))
  };
  e.lengthVec4 = function(h) {
    return Math.pow(h[0] * h[0] + h[1] * h[1] + h[2] * h[2] + h[3] * h[3], 0.5)
  };
  e.distanceVec4 = function(h, o) {
    return e.lengthVec4(e.subVec4(h, o))
  };
  e.angleVec3 = function(h, o) {
    h = e.toUnitVec3(h);
    o = e.toUnitVec3(o);
    d = e.dotVec3(h, o);
    if(d < -1) {
      d = -1
    }if(d > 1) {
      d = 1
    }return Math.acos(d)
  };
  e.angleVec4 = function(h, o) {
    h = e.toUnitVec4(h);
    o = e.toUnitVec4(o);
    d = e.dotVec4(h, o);
    if(d < -1) {
      d = -1
    }if(d > 1) {
      d = 1
    }return Math.acos(d)
  };
  GLGE_math_use_webgl_float = false;
  e.Mat3 = GLGE_math_use_webgl_float ? function(h) {
    if(h.length == 9) {
      return new Float32Array(h)
    }else {
      if(h.length == 16) {
        return new Float32Array([h[0], h[1], h[2], h[4], h[5], h[6], h[8], h[9], h[10]])
      }else {
        throw"invalid matrix length";
      }
    }
  } : function(h) {
    if(h.length == 9) {
      h = h.slice(0)
    }else {
      if(h.length == 16) {
        h = [h[0], h[1], h[2], h[4], h[5], h[6], h[8], h[9], h[10]]
      }else {
        throw"invalid matrix length";
      }
    }h.get = function(o) {
      return this[o]
    };
    return h
  };
  e.Mat = GLGE_math_use_webgl_float ? function(h) {
    return new Float32Array(h)
  } : function(h) {
    h = h.slice(0);
    h.get = function(o) {
      return this[o]
    };
    return h
  };
  e.Mat4 = function(h) {
    if(h.length == 9) {
      h = [h[0], h[1], h[2], 0, h[3], h[4], h[5], 0, h[6], h[7], h[8], 0, 0, 0, 0, 1]
    }else {
      if(h.length == 16) {
        h = h.slice(0)
      }else {
        throw"invalid matrix length";
      }
    }h.get = function(o) {
      return this[o]
    };
    return h
  };
  e.determinantMat4 = function(h) {
    return h[12] * h[9] * h[6] * h[3] - h[8] * h[13] * h[6] * h[3] - h[12] * h[5] * h[10] * h[3] + h[4] * h[13] * h[10] * h[3] + h[8] * h[5] * h[14] * h[3] - h[4] * h[9] * h[14] * h[3] - h[12] * h[9] * h[2] * h[7] + h[8] * h[13] * h[2] * h[7] + h[12] * h[1] * h[10] * h[7] - h[0] * h[13] * h[10] * h[7] - h[8] * h[1] * h[14] * h[7] + h[0] * h[9] * h[14] * h[7] + h[12] * h[5] * h[2] * h[11] - h[4] * h[13] * h[2] * h[11] - h[12] * h[1] * h[6] * h[11] + h[0] * h[13] * h[6] * h[11] + h[4] * h[1] * h[14] * 
    h[11] - h[0] * h[5] * h[14] * h[11] - h[8] * h[5] * h[2] * h[15] + h[4] * h[9] * h[2] * h[15] + h[8] * h[1] * h[6] * h[15] - h[0] * h[9] * h[6] * h[15] - h[4] * h[1] * h[10] * h[15] + h[0] * h[5] * h[10] * h[15]
  };
  e.inverseMat4 = function(h) {
    var o = h[0], q = h[1], u = h[2], f = h[3], g = h[4], m = h[5], p = h[6], r = h[7], s = h[8], A = h[9], v = h[10], B = h[11], C = h[12], E = h[13], H = h[14];
    h = h[15];
    var J = C * A * p * f - s * E * p * f - C * m * v * f + g * E * v * f + s * m * H * f - g * A * H * f - C * A * u * r + s * E * u * r + C * q * v * r - o * E * v * r - s * q * H * r + o * A * H * r + C * m * u * B - g * E * u * B - C * q * p * B + o * E * p * B + g * q * H * B - o * m * H * B - s * m * u * h + g * A * u * h + s * q * p * h - o * A * p * h - g * q * v * h + o * m * v * h;
    return[(A * H * r - E * v * r + E * p * B - m * H * B - A * p * h + m * v * h) / J, (E * v * f - A * H * f - E * u * B + q * H * B + A * u * h - q * v * h) / J, (m * H * f - E * p * f + E * u * r - q * H * r - m * u * h + q * p * h) / J, (A * p * f - m * v * f - A * u * r + q * v * r + m * u * B - q * p * B) / J, (C * v * r - s * H * r - C * p * B + g * H * B + s * p * h - g * v * h) / J, (s * H * f - C * v * f + C * u * B - o * H * B - s * u * h + o * v * h) / J, (C * p * f - g * H * f - C * 
    u * r + o * H * r + g * u * h - o * p * h) / J, (g * v * f - s * p * f + s * u * r - o * v * r - g * u * B + o * p * B) / J, (s * E * r - C * A * r + C * m * B - g * E * B - s * m * h + g * A * h) / J, (C * A * f - s * E * f - C * q * B + o * E * B + s * q * h - o * A * h) / J, (g * E * f - C * m * f + C * q * r - o * E * r - g * q * h + o * m * h) / J, (s * m * f - g * A * f - s * q * r + o * A * r + g * q * B - o * m * B) / J, (C * A * p - s * E * p - C * m * v + g * E * v + s * m * H - g * 
    A * H) / J, (s * E * u - C * A * u + C * q * v - o * E * v - s * q * H + o * A * H) / J, (C * m * u - g * E * u - C * q * p + o * E * p + g * q * H - o * m * H) / J, (g * A * u - s * m * u + s * q * p - o * A * p - g * q * v + o * m * v) / J]
  };
  e.mulMat4Vec3 = function(h, o) {
    return e.Vec3(h[0] * o[0] + h[1] * o[1] + h[2] * o[2] + h[3], h[4] * o[0] + h[5] * o[1] + h[6] * o[2] + h[7], h[8] * o[0] + h[9] * o[1] + h[10] * o[2] + h[11])
  };
  e.mulMat4Vec4 = function(h, o) {
    return e.Vec4(h[0] * o[0] + h[1] * o[1] + h[2] * o[2] + h[3] * o[3], h[4] * o[0] + h[5] * o[1] + h[6] * o[2] + h[7] * o[3], h[8] * o[0] + h[9] * o[1] + h[10] * o[2] + h[11] * o[3], h[12] * o[0] + h[13] * o[1] + h[14] * o[2] + h[15] * o[3])
  };
  e.scaleMat4 = function(h, o) {
    return e.Mat([h[0] * o, h[1] * o, h[2] * o, h[3] * o, h[4] * o, h[5] * o, h[6] * o, h[7] * o, h[8] * o, h[9] * o, h[10] * o, h[11] * o, h[12] * o, h[13] * o, h[14] * o, h[15] * o])
  };
  e.scaleInPlaceMat4 = function(h, o) {
    h.set(0, h[0] * o);
    h.set(1, h[1] * o);
    h.set(2, h[2] * o);
    h.set(3, h[3] * o);
    h.set(4, h[4] * o);
    h.set(5, h[5] * o);
    h.set(6, h[6] * o);
    h.set(7, h[7] * o);
    h.set(8, h[8] * o);
    h.set(9, h[9] * o);
    h.set(10, h[10] * o);
    h.set(11, h[11] * o);
    h.set(12, h[12] * o);
    h.set(13, h[13] * o);
    h.set(14, h[14] * o);
    h.set(15, h[15] * o);
    return h
  };
  e.addInPlaceMat4 = function(h, o) {
    h.set(0, h[0] + o[0]);
    h.set(1, h[1] + o[1]);
    h.set(2, h[2] + o[2]);
    h.set(3, h[3] + o[3]);
    h.set(4, h[4] + o[4]);
    h.set(5, h[5] + o[5]);
    h.set(6, h[6] + o[6]);
    h.set(7, h[7] + o[7]);
    h.set(8, h[8] + o[8]);
    h.set(9, h[9] + o[9]);
    h.set(10, h[10] + o[10]);
    h.set(11, h[11] + o[11]);
    h.set(12, h[12] + o[12]);
    h.set(13, h[13] + o[13]);
    h.set(14, h[14] + o[14]);
    h.set(15, h[15] + o[15]);
    return h
  };
  e.addMat4 = function(h, o) {
    return e.Mat([h[0] + o[0], h[1] + o[1], h[2] + o[2], h[3] + o[3], h[4] + o[4], h[5] + o[5], h[6] + o[6], h[7] + o[7], h[8] + o[8], h[9] + o[9], h[10] + o[10], h[11] + o[11], h[12] + o[12], h[13] + o[13], h[14] + o[14], h[15] + o[15]])
  };
  e.subInPlaceMat4 = function(h, o) {
    h.set(0, h[0] - o[0]);
    h.set(1, h[1] - o[1]);
    h.set(2, h[2] - o[2]);
    h.set(3, h[3] - o[3]);
    h.set(4, h[4] - o[4]);
    h.set(5, h[5] - o[5]);
    h.set(6, h[6] - o[6]);
    h.set(7, h[7] - o[7]);
    h.set(8, h[8] - o[8]);
    h.set(9, h[9] - o[9]);
    h.set(10, h[10] - o[10]);
    h.set(11, h[11] - o[11]);
    h.set(12, h[12] - o[12]);
    h.set(13, h[13] - o[13]);
    h.set(14, h[14] - o[14]);
    h.set(15, h[15] - o[15]);
    return h
  };
  e.subMat4 = function(h, o) {
    return e.Mat([h[0] - o[0], h[1] - o[1], h[2] - o[2], h[3] - o[3], h[4] - o[4], h[5] - o[5], h[6] - o[6], h[7] - o[7], h[8] - o[8], h[9] - o[9], h[10] - o[10], h[11] - o[11], h[12] - o[12], h[13] - o[13], h[14] - o[14], h[15] - o[15]])
  };
  e.mulMat4 = function(h, o) {
    var q = o[0], u = o[1], f = o[2], g = o[3], m = o[4], p = o[5], r = o[6], s = o[7], A = o[8], v = o[9], B = o[10], C = o[11], E = o[12], H = o[13], J = o[14];
    o = o[15];
    var M = h[0], K = h[1], N = h[2], Q = h[3], R = h[4], D = h[5], G = h[6], I = h[7], F = h[8], L = h[9], O = h[10], P = h[11], S = h[12], T = h[13], U = h[14];
    h = h[15];
    return[M * q + K * m + N * A + Q * E, M * u + K * p + N * v + Q * H, M * f + K * r + N * B + Q * J, M * g + K * s + N * C + Q * o, R * q + D * m + G * A + I * E, R * u + D * p + G * v + I * H, R * f + D * r + G * B + I * J, R * g + D * s + G * C + I * o, F * q + L * m + O * A + P * E, F * u + L * p + O * v + P * H, F * f + L * r + O * B + P * J, F * g + L * s + O * C + P * o, S * q + T * m + U * A + h * E, S * u + T * p + U * v + h * H, S * f + T * r + U * B + h * J, S * g + T * s + U * C + h * 
    o]
  };
  e.transposeInPlaceMat4 = function(h) {
    var o = h[1];
    h.set(1, h[4]);
    h.set(4, o);
    o = h[8];
    h.set(8, h[2]);
    h.set(2, o);
    o = h[3];
    h.set(3, h[12]);
    h.set(12, o);
    o = h[9];
    h.set(9, h[6]);
    h.set(6, o);
    o = h[13];
    h.set(13, h[7]);
    h.set(7, o);
    o = h[14];
    h.set(14, h[11]);
    h.set(11, o)
  };
  e.transposeMat4 = function(h) {
    return e.Mat4([h[0], h[4], h[8], h[12], h[1], h[5], h[9], h[13], h[2], h[6], h[10], h[14], h[3], h[7], h[11], h[15]])
  };
  e.mat4gl = function(h, o) {
    o[0] = h[0];
    o[1] = h[1];
    o[2] = h[2];
    o[3] = h[3];
    o[4] = h[4];
    o[5] = h[5];
    o[6] = h[6];
    o[7] = h[7];
    o[8] = h[8];
    o[9] = h[9];
    o[10] = h[10];
    o[11] = h[11];
    o[12] = h[12];
    o[13] = h[13];
    o[14] = h[14];
    o[15] = h[15]
  };
  e.set1basedMat4 = function(h, o, q, u) {
    h[(o - 1) * 4 + (q - 1)] = u;
    h.glData !== undefined && delete h.glData
  };
  e.setMat4 = function(h, o, q, u) {
    h[o * 4 + q] = u;
    h.glData !== undefined && delete h.glData
  };
  e.get1basedMat4 = function(h, o, q) {
    return h.get((o - 1) * 4 + (q - 1))
  };
  e.getMat4 = function(h, o, q) {
    return h[o * 4 + q]
  };
  e.glDataMat4 = function(h) {
    h.glArray = new Float32Array(h);
    return h.glArray
  };
  e.identMatrix = function() {
    return e.Mat([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
  };
  e.translateMatrix = function(h) {
    var o, q, u;
    if(arguments.length == 3) {
      o = arguments[0];
      q = arguments[1];
      u = arguments[2]
    }else {
      if(h.data) {
        o = h.data[0];
        q = h.data[1];
        u = h.data[2]
      }else {
        if(h instanceof Array) {
          o = h[0];
          q = h[1];
          u = h[2]
        }
      }
    }return e.Mat([1, 0, 0, o, 0, 1, 0, q, 0, 0, 1, u, 0, 0, 0, 1])
  };
  e.scaleMatrix = function(h) {
    var o, q, u;
    if(arguments.length == 3) {
      o = arguments[0];
      q = arguments[1];
      u = arguments[2]
    }else {
      if(h.data) {
        o = h.data[0];
        q = h.data[1];
        u = h.data[2]
      }else {
        if(h instanceof Array) {
          o = h[0];
          q = h[1];
          u = h[2]
        }
      }
    }return e.Mat([o, 0, 0, 0, 0, q, 0, 0, 0, 0, u, 0, 0, 0, 0, 1])
  };
  e.ROT_XYZ = 1;
  e.ROT_XZY = 2;
  e.ROT_YXZ = 3;
  e.ROT_YZX = 4;
  e.ROT_ZXY = 5;
  e.ROT_ZYX = 6;
  e.rotateMatrix = function(h, o) {
    var q, u, f;
    if(arguments.length > 2) {
      q = arguments[0];
      u = arguments[1];
      f = arguments[2];
      o = arguments[3]
    }else {
      if(h.data) {
        q = h.data[0];
        u = h.data[1];
        f = h.data[2]
      }else {
        if(h instanceof Array) {
          q = h[0];
          u = h[1];
          f = h[2]
        }
      }
    }if(!o) {
      o = e.ROT_XYZ
    }var g = Math.cos(q), m = Math.sin(q);
    q = Math.cos(u);
    var p = Math.sin(u);
    u = Math.cos(f);
    f = Math.sin(f);
    g = e.Mat([1, 0, 0, 0, 0, g, -m, 0, 0, m, g, 0, 0, 0, 0, 1]);
    q = e.Mat([q, 0, p, 0, 0, 1, 0, 0, -p, 0, q, 0, 0, 0, 0, 1]);
    u = e.Mat([u, -f, 0, 0, f, u, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);
    switch(o) {
      case e.ROT_XYZ:
        return e.mulMat4(g, e.mulMat4(q, u));
      case e.ROT_XZY:
        return e.mulMat4(g, e.mulMat4(u, q));
      case e.ROT_YXZ:
        return e.mulMat4(q, e.mulMat4(g, u));
      case e.ROT_YZX:
        return e.mulMat4(q, e.mulMat4(u, g));
      case e.ROT_ZXY:
        return e.mulMat4(u, e.mulMat4(g, q));
      case e.ROT_ZYX:
        return e.mulMat4(u, e.mulMat4(q, g))
    }
  };
  e.angleAxis = function(h, o) {
    var q, u, f, g, m, p, r, s;
    o = [o[0], o[1], o[2], 0];
    p = o[0];
    m = o[1];
    var A = o[2];
    o = Math.cos(h);
    var v = 1 - o;
    q = Math.sin(h);
    h = p * q;
    r = m * q;
    s = A * q;
    q = p * p;
    u = m * m;
    f = A * A;
    g = p * m;
    m = m * A;
    p = A * p;
    return e.Mat([v * q + o, v * g - s, v * p + r, 0, v * g + s, v * u + o, v * m - h, 0, v * p - r, v * m + h, v * f + o, 0, 0, 0, 0, 1])
  };
  e.quatRotation = function(h, o, q, u) {
    return e.Mat([1 - 2 * o * o - 2 * q * q, 2 * h * o - 2 * q * u, 2 * h * q + 2 * o * u, 0, 2 * h * o + 2 * q * u, 1 - 2 * h * h - 2 * q * q, 2 * o * q - 2 * h * u, 0, 2 * h * q - 2 * o * u, 2 * o * q + 2 * h * u, 1 - 2 * h * h - 2 * o * o, 0, 0, 0, 0, 1])
  };
  e.makeOrtho = function(h, o, q, u, f, g) {
    return e.Mat([2 / (o - h), 0, 0, -(o + h) / (o - h), 0, 2 / (u - q), 0, -(u + q) / (u - q), 0, 0, -2 / (g - f), -(g + f) / (g - f), 0, 0, 0, 1])
  };
  e.makeFrustum = function(h, o, q, u, f, g) {
    return e.Mat([2 * f / (o - h), 0, (o + h) / (o - h), 0, 0, 2 * f / (u - q), (u + q) / (u - q), 0, 0, 0, -(g + f) / (g - f), -2 * g * f / (g - f), 0, 0, -1, 0])
  };
  e.makePerspective = function(h, o, q, u) {
    h = q * Math.tan(h * 0.00872664625972);
    var f = -h;
    return e.makeFrustum(f * o, h * o, f, h, q, u)
  };
  e.matrix2Scale = function(h) {
    var o = h[0], q = h[1], u = h[2], f = h[4], g = h[5], m = h[6], p = h[8], r = h[9];
    h = h[10];
    o = Math.sqrt(o * o + q * q + u * u);
    f = Math.sqrt(f * f + g * g + m * m);
    p = Math.sqrt(p * p + r * r + h * h);
    return[o, f, p]
  };
  e.rotationMatrix2Quat = function(h) {
    var o = h[0] + h[5] + h[10] + 1, q, u, f;
    if(o > 0) {
      q = 0.5 / Math.sqrt(o);
      f = 0.25 / q;
      o = (h[9] - h[6]) * q;
      u = (h[2] - h[8]) * q;
      h = (h[4] - h[1]) * q
    }else {
      if(h[0] > h[5] && h[0] > h[10]) {
        q = Math.sqrt(1 + h[0] - h[5] - h[10]) * 2;
        f = (h[9] - h[6]) / q;
        o = 0.25 / q;
        u = (h[1] + h[4]) / q;
        h = (h[2] + h[8]) / q
      }else {
        if(h[5] > h[10]) {
          q = Math.sqrt(1 + h[5] - h[0] - h[10]) * 2;
          f = (h[2] - h[8]) / q;
          o = (h[1] + h[4]) / q;
          u = 0.25 / q;
          h = (h[6] + h[9]) / q
        }else {
          q = Math.sqrt(1 + h[10] - h[0] - h[5]) * 2;
          f = (h[4] - h[1]) / q;
          o = (h[2] + h[8]) / q;
          u = (h[6] + h[9]) / q;
          h = 0.25 / q
        }
      }
    }q = Math.sqrt(o * o + u * u + h * h + f * f);
    return[o / q, u / q, h / q, f / q]
  };
  e.rayToPlane = function(h, o) {
    o = e.toUnitVec3(o);
    return[o[0], o[1], o[2], e.dotVec3(h, o)]
  };
  e.rayIntersectPlane = function(h, o, q) {
    var u = [q[0], q[1], q[2]];
    q = q[3];
    var f = e.dotVec3(u, o);
    if(f <= 0) {
      return false
    }u = -(e.dotVec3(u, h) + q) / f;
    if(u <= 0) {
      return false
    }return e.addVec3(h, e.scaleVec3(o, u))
  };
  e.screenToDirection = function(h, o, q, u, f) {
    xcoord = -(2 * h / q - 1) / f[0];
    ycoord = (2 * o / u - 1) / f[5];
    zcoord = 1;
    return e.toUnitVec3([xcoord, ycoord, zcoord])
  };
  e.BoundingVolume = function(h, o, q, u, f, g) {
    this.limits = [h, o, q, u, f, g];
    this.calcProps()
  };
  e.BoundingVolume.prototype.getCornerPoints = function() {
    return this.points
  };
  e.BoundingVolume.prototype.getSphereRadius = function() {
    return this.radius
  };
  e.BoundingVolume.prototype.getCenter = function() {
    return this.center
  };
  e.BoundingVolume.prototype.isNull = function() {
    return this.limits[0] == 0 && this.limits[1] == 0 && this.limits[2] == 0 && this.limits[3] == 0 && this.limits[4] == 0 && this.limits[5] == 0
  };
  e.BoundingVolume.prototype.addBoundingVolume = function(h) {
    if(this.isNull()) {
      this.limits[0] = h.limits[0];
      this.limits[1] = h.limits[1];
      this.limits[2] = h.limits[2];
      this.limits[3] = h.limits[3];
      this.limits[4] = h.limits[4];
      this.limits[5] = h.limits[5]
    }else {
      if(!h.isNull()) {
        this.limits[0] = Math.min(h.limits[0], this.limits[0]);
        this.limits[2] = Math.min(h.limits[2], this.limits[2]);
        this.limits[4] = Math.min(h.limits[4], this.limits[4]);
        this.limits[1] = Math.max(h.limits[1], this.limits[1]);
        this.limits[3] = Math.max(h.limits[3], this.limits[3]);
        this.limits[5] = Math.max(h.limits[5], this.limits[5])
      }
    }this.calcProps()
  };
  e.BoundingVolume.prototype.calcProps = function() {
    var h = this.limits[0], o = this.limits[1], q = this.limits[2], u = this.limits[3], f = this.limits[4], g = this.limits[5];
    this.points = [[h, q, f], [o, q, f], [h, u, f], [o, u, f], [h, q, g], [o, q, g], [h, u, g], [o, u, g]];
    this.center = [(this.limits[1] - this.limits[0]) / 2 + this.limits[0], (this.limits[3] - this.limits[2]) / 2 + this.limits[2], (this.limits[5] - this.limits[4]) / 2 + this.limits[4]];
    h = this.limits[0] - this.center[0];
    o = this.limits[2] - this.center[1];
    q = this.limits[4] - this.center[2];
    this.radius = Math.sqrt(h * h + o * o + q * q)
  };
  e.BoundingVolume.prototype.clone = function() {
    return new e.BoundingVolume(this.limits[0], this.limits[1], this.limits[2], this.limits[3], this.limits[4], this.limits[5])
  };
  e.BoundingVolume.prototype.toString = function() {
    return this.limits.toString()
  };
  e.cameraViewProjectionToPlanes = function(h) {
    var o = e.inverseMat4(h), q = e.mulMat4Vec4, u = e.subVec3, f = e.crossVec3, g = e.toUnitVec3;
    h = e.dotVec3;
    var m = q(o, [-1, -1, -1, 1]), p = q(o, [1, -1, -1, 1]), r = q(o, [-1, -1, 1, 1]), s = q(o, [1, 1, -1, 1]), A = q(o, [1, 1, 1, 1]), v = q(o, [-1, 1, 1, 1]);
    m = [m[0] / m[3], m[1] / m[3], m[2] / m[3]];
    p = [p[0] / p[3], p[1] / p[3], p[2] / p[3]];
    r = [r[0] / r[3], r[1] / r[3], r[2] / r[3]];
    s = [s[0] / s[3], s[1] / s[3], s[2] / s[3]];
    A = [A[0] / A[3], A[1] / A[3], A[2] / A[3]];
    v = [v[0] / v[3], v[1] / v[3], v[2] / v[3]];
    o = g(f(u(s, p), u(m, p)));
    q = g(f(u(v, r), u(A, r)));
    var B = g(f(u(m, r), u(v, r))), C = g(f(u(A, s), u(s, p)));
    s = g(f(u(v, s), u(s, A)));
    u = g(f(u(m, p), u(r, m)));
    o.push(h(o, m));
    q.push(h(q, r));
    B.push(h(B, m));
    C.push(h(C, p));
    s.push(h(s, A));
    u.push(h(u, m));
    return[o, q, B, C, s, u]
  };
  e.sphereInFrustumPlanes = function(h, o) {
    var q = h[0], u = h[1], f = h[2];
    h = h[3];
    var g = o[0], m = o[1], p = o[2], r = o[3], s = o[4];
    o = o[5];
    return q * g[0] + u * g[1] + f * g[2] - g[3] - h > 0 || q * m[0] + u * m[1] + f * m[2] - m[3] - h > 0 || q * p[0] + u * p[1] + f * p[2] - p[3] - h > 0 || q * r[0] + u * r[1] + f * r[2] - r[3] - h > 0 || q * s[0] + u * s[1] + f * s[2] - s[3] - h > 0 || q * o[0] + u * o[1] + f * o[2] - o[3] - h > 0 ? false : true
  };
  e.pointsInFrustumPlanes = function(h, o) {
    var q = o[0], u = o[1], f = o[2], g = o[3], m = o[4];
    o = o[5];
    for(var p, r, s, A = 0;A < h.length;A++) {
      p = h[A][0];
      r = h[A][1];
      s = h[A][2];
      if(p * q[0] + r * q[1] + s * q[2] - q[3] > 0 && p * u[0] + r * u[1] + s * u[2] - u[3] > 0 && p * f[0] + r * f[1] + s * f[2] - g[3] > 0 && p * g[0] + r * g[1] + s * g[2] - m[3] > 0 && p * m[0] + r * m[1] + s * m[2] - m[3] > 0 && p * o[0] + r * o[1] + s * o[2] - o[3] > 0) {
        return false
      }
    }return true
  };
  j();
  e.Vec3 = e.Vec3;
  e.Vec4 = e.Vec4;
  e.get1basedVec4 = e.get1basedVec4;
  e.get1basedVec3 = e.get1basedVec3;
  e.getVec4 = e.getVec4;
  e.getVec3 = e.getVec3;
  e.addVec4 = e.addVec4;
  e.addVec3 = e.addVec3;
  e.subVec4 = e.subVec4;
  e.subVec3 = e.subVec3;
  e.dotVec3 = e.dotVec3;
  e.dotVec4 = e.dotVec4;
  e.scaleVec4 = e.scaleVec4;
  e.scaleVec3 = e.scaleVec3;
  e.crossVec3 = e.crossVec3;
  e.toUnitVec3 = e.toUnitVec3;
  e.toUnitVec4 = e.toUnitVec4;
  e.lengthVec3 = e.lengthVec3;
  e.distanceVec3 = e.distanceVec3;
  e.lengthVec4 = e.lengthVec4;
  e.distanceVec4 = e.distanceVec4;
  e.angleVec3 = e.angleVec3;
  e.angleVec4 = e.angleVec4;
  e.Mat3 = e.Mat3;
  e.Mat = e.Mat;
  e.Mat4 = e.Mat4;
  e.determinantMat4 = e.determinantMat4;
  e.inverseMat4 = e.inverseMat4;
  e.mulMat4Vec4 = e.mulMat4Vec4;
  e.scaleMat4 = e.scaleMat4;
  e.scaleInPlaceMat4 = e.scaleInPlaceMat4;
  e.addInPlaceMat4 = e.addInPlaceMat4;
  e.addMat4 = e.addMat4;
  e.subInPlaceMat4 = e.subInPlaceMat4;
  e.subMat4 = e.subMat4;
  e.mulMat4 = e.mulMat4;
  e.transposeInPlaceMat4 = e.transposeInPlaceMat4;
  e.transposeMat4 = e.transposeMat4;
  e.set1basedMat4 = e.set1basedMat4;
  e.setMat4 = e.setMat4;
  e.get1basedMat4 = e.get1basedMat4;
  e.getMat4 = e.getMat4;
  e.glDataMat4 = e.glDataMat4;
  e.identMatrix = e.identMatrix;
  e.translateMatrix = e.translateMatrix;
  e.scaleMatrix = e.scaleMatrix;
  e.ROT_XYZ = e.ROT_XYZ;
  e.ROT_XZY = e.ROT_XZY;
  e.ROT_YXZ = e.ROT_YXZ;
  e.ROT_YZX = e.ROT_YZX;
  e.ROT_ZXY = e.ROT_ZXY;
  e.ROT_ZYX = e.ROT_ZYX;
  e.rotateMatrix = e.rotateMatrix;
  e.angleAxis = e.angleAxis;
  e.quatRotation = e.quatRotation;
  e.makeOrtho = e.makeOrtho;
  e.makeFrustum = e.makeFrustum;
  e.makePerspective = e.makePerspective;
  e.matrix2Scale = e.matrix2Scale;
  e.rotationMatrix2Quat = e.rotationMatrix2Quat;
  e.mat4gl = e.mat4gl
})(GLGE);if(typeof GLGE == "undefined") {
  GLGE = {}
}(function(e) {
  function j() {
    if(e.Message) {
      e.Message = e.Message;
      e.Message.parseMessage = e.Message.parseMessage
    }if(e.Document) {
      e.Document = e.Document;
      e.Document.prototype.getElementById = e.Document.prototype.getElementById;
      e.Document.prototype.getElement = e.Document.prototype.getElement;
      e.Document.prototype.load = e.Document.prototype.load;
      e.Document.prototype.loadDocument = e.Document.prototype.loadDocument;
      e.Document.prototype.onLoad = e.Document.prototype.onLoad;
      e.Document.prototype.addLoadListener = e.Document.prototype.addLoadListener;
      e.Document.prototype.removeLoadListener = e.Document.prototype.removeLoadListener
    }if(e.Placeable) {
      e.Placeable = e.Placeable;
      e.Placeable.prototype.getRoot = e.Placeable.prototype.getRoot;
      e.Placeable.prototype.getRef = e.Placeable.prototype.getRef;
      e.Placeable.prototype.setId = e.Placeable.prototype.setId;
      e.Placeable.prototype.getId = e.Placeable.prototype.getId;
      e.Placeable.prototype.getLookat = e.Placeable.prototype.getLookat;
      e.Placeable.prototype.setLookat = e.Placeable.prototype.setLookat;
      e.Placeable.prototype.Lookat = e.Placeable.prototype.Lookat;
      e.Placeable.prototype.getRotOrder = e.Placeable.prototype.getRotOrder;
      e.Placeable.prototype.setRotOrder = e.Placeable.prototype.setRotOrder;
      e.Placeable.prototype.getRotMatrix = e.Placeable.prototype.getRotMatrix;
      e.Placeable.prototype.setRotMatrix = e.Placeable.prototype.setRotMatrix;
      e.Placeable.prototype.setLocX = e.Placeable.prototype.setLocX;
      e.Placeable.prototype.setLocY = e.Placeable.prototype.setLocY;
      e.Placeable.prototype.setLocZ = e.Placeable.prototype.setLocZ;
      e.Placeable.prototype.setLoc = e.Placeable.prototype.setLoc;
      e.Placeable.prototype.setDLocX = e.Placeable.prototype.setDLocX;
      e.Placeable.prototype.setDLocY = e.Placeable.prototype.setDLocY;
      e.Placeable.prototype.setDLocZ = e.Placeable.prototype.setDLocZ;
      e.Placeable.prototype.setDLoc = e.Placeable.prototype.setDLoc;
      e.Placeable.prototype.setQuatX = e.Placeable.prototype.setQuatX;
      e.Placeable.prototype.setQuatY = e.Placeable.prototype.setQuatY;
      e.Placeable.prototype.setQuatZ = e.Placeable.prototype.setQuatZ;
      e.Placeable.prototype.setQuatW = e.Placeable.prototype.setQuatW;
      e.Placeable.prototype.setQuat = e.Placeable.prototype.setQuat;
      e.Placeable.prototype.setRotX = e.Placeable.prototype.setRotX;
      e.Placeable.prototype.setRotY = e.Placeable.prototype.setRotY;
      e.Placeable.prototype.setRotZ = e.Placeable.prototype.setRotZ;
      e.Placeable.prototype.setRot = e.Placeable.prototype.setRot;
      e.Placeable.prototype.setDRotX = e.Placeable.prototype.setDRotX;
      e.Placeable.prototype.setDRotY = e.Placeable.prototype.setDRotY;
      e.Placeable.prototype.setDRotZ = e.Placeable.prototype.setDRotZ;
      e.Placeable.prototype.setDRot = e.Placeable.prototype.setDRot;
      e.Placeable.prototype.setScaleX = e.Placeable.prototype.setScaleX;
      e.Placeable.prototype.setScaleY = e.Placeable.prototype.setScaleY;
      e.Placeable.prototype.setScaleZ = e.Placeable.prototype.setScaleZ;
      e.Placeable.prototype.setScale = e.Placeable.prototype.setScale;
      e.Placeable.prototype.setDScaleX = e.Placeable.prototype.setDScaleX;
      e.Placeable.prototype.setDScaleY = e.Placeable.prototype.setDScaleY;
      e.Placeable.prototype.setDScaleZ = e.Placeable.prototype.setDScaleZ;
      e.Placeable.prototype.setDScale = e.Placeable.prototype.setDScale;
      e.Placeable.prototype.getLocX = e.Placeable.prototype.getLocX;
      e.Placeable.prototype.getLocY = e.Placeable.prototype.getLocY;
      e.Placeable.prototype.getLocZ = e.Placeable.prototype.getLocZ;
      e.Placeable.prototype.getDLocX = e.Placeable.prototype.getDLocX;
      e.Placeable.prototype.getDLocY = e.Placeable.prototype.getDLocY;
      e.Placeable.prototype.getDLocZ = e.Placeable.prototype.getDLocZ;
      e.Placeable.prototype.getQuatX = e.Placeable.prototype.getQuatX;
      e.Placeable.prototype.getQuatY = e.Placeable.prototype.getQuatY;
      e.Placeable.prototype.getQuatZ = e.Placeable.prototype.getQuatZ;
      e.Placeable.prototype.getQuatW = e.Placeable.prototype.getQuatW;
      e.Placeable.prototype.getRotX = e.Placeable.prototype.getRotX;
      e.Placeable.prototype.getRotY = e.Placeable.prototype.getRotY;
      e.Placeable.prototype.getRotZ = e.Placeable.prototype.getRotZ;
      e.Placeable.prototype.getDRotX = e.Placeable.prototype.getDRotX;
      e.Placeable.prototype.getDRotY = e.Placeable.prototype.getDRotY;
      e.Placeable.prototype.getDRotZ = e.Placeable.prototype.getDRotZ;
      e.Placeable.prototype.getScaleX = e.Placeable.prototype.getScaleX;
      e.Placeable.prototype.getScaleY = e.Placeable.prototype.getScaleY;
      e.Placeable.prototype.getScaleZ = e.Placeable.prototype.getScaleZ;
      e.Placeable.prototype.getDScaleX = e.Placeable.prototype.getDScaleX;
      e.Placeable.prototype.getDScaleY = e.Placeable.prototype.getDScaleY;
      e.Placeable.prototype.getDScaleZ = e.Placeable.prototype.getDScaleZ;
      e.Placeable.prototype.getPosition = e.Placeable.prototype.getPosition;
      e.Placeable.prototype.getRotation = e.Placeable.prototype.getRotation;
      e.Placeable.prototype.getScale = e.Placeable.prototype.getScale;
      e.Placeable.prototype.getModelMatrix = e.Placeable.prototype.getModelMatrix
    }if(e.Animatable) {
      e.Animatable = e.Animatable;
      e.Animatable.prototype.animationStart = e.Animatable.prototype.animationStart;
      e.Animatable.prototype.animate = e.Animatable.prototype.animate;
      e.Animatable.prototype.setAnimation = e.Animatable.prototype.setAnimation;
      e.Animatable.prototype.getAnimation = e.Animatable.prototype.getAnimation;
      e.Animatable.prototype.setFrameRate = e.Animatable.prototype.setFrameRate;
      e.Animatable.prototype.getFrameRate = e.Animatable.prototype.getFrameRate;
      e.Animatable.prototype.setLoop = e.Animatable.prototype.setLoop;
      e.Animatable.prototype.getLoop = e.Animatable.prototype.getLoop;
      e.Animatable.prototype.isLooping = e.Animatable.prototype.isLooping;
      e.Animatable.prototype.setPaused = e.Animatable.prototype.setPaused;
      e.Animatable.prototype.getPaused = e.Animatable.prototype.getPaused;
      e.Animatable.prototype.togglePaused = e.Animatable.prototype.togglePaused
    }if(e.BezTriple) {
      e.BezTriple = e.BezTriple;
      e.BezTriple.prototype.className = e.BezTriple.prototype.className;
      e.BezTriple.prototype.setX1 = e.BezTriple.prototype.setX1;
      e.BezTriple.prototype.setY1 = e.BezTriple.prototype.setY1;
      e.BezTriple.prototype.setX2 = e.BezTriple.prototype.setX2;
      e.BezTriple.prototype.setY2 = e.BezTriple.prototype.setY2;
      e.BezTriple.prototype.setX3 = e.BezTriple.prototype.setX3;
      e.BezTriple.prototype.setY4 = e.BezTriple.prototype.setY4
    }if(e.LinearPoint) {
      e.LinearPoint = e.LinearPoint;
      e.LinearPoint.prototype.className = e.LinearPoint.prototype.className;
      e.LinearPoint.prototype.setX = e.LinearPoint.prototype.setX;
      e.LinearPoint.prototype.setY = e.LinearPoint.prototype.setY
    }if(e.StepPoint) {
      e.StepPoint = e.StepPoint
    }if(e.AnimationCurve) {
      e.AnimationCurve = e.AnimationCurve;
      e.AnimationCurve.prototype.className = e.AnimationCurve.prototype.className;
      e.AnimationCurve.prototype.addPoint = e.AnimationCurve.prototype.addPoint;
      e.AnimationCurve.prototype.getValue = e.AnimationCurve.prototype.getValue
    }if(e.AnimationVector) {
      e.AnimationVector = e.AnimationVector;
      e.AnimationVector.prototype.addCurve = e.AnimationVector.prototype.addCurve;
      e.AnimationVector.prototype.removeCurve = e.AnimationVector.prototype.removeCurve;
      e.AnimationVector.prototype.setFrames = e.AnimationVector.prototype.setFrames;
      e.AnimationVector.prototype.getFrames = e.AnimationVector.prototype.getFrames
    }if(e.augment) {
      e.augment = e.augment
    }e.G_NODE = e.G_NODE;
    e.G_ROOT = e.G_ROOT;
    if(e.Group) {
      e.Group = e.Group;
      e.Group.prototype.children = e.Group.prototype.children;
      e.Group.prototype.className = e.Group.prototype.className;
      e.Group.prototype.type = e.Group.prototype.type;
      e.Group.prototype.getObjects = e.Group.prototype.getObjects;
      e.Group.prototype.getLights = e.Group.prototype.getLights;
      e.Group.prototype.addChild = e.Group.prototype.addChild;
      e.Group.prototype.addObject = e.Group.prototype.addObject;
      e.Group.prototype.addGroup = e.Group.prototype.addGroup;
      e.Group.prototype.addText = e.Group.prototype.addText;
      e.Group.prototype.addSkeleton = e.Group.prototype.addSkeleton;
      e.Group.prototype.addLight = e.Group.prototype.addLight;
      e.Group.prototype.addCamera = e.Group.prototype.addCamera;
      e.Group.prototype.removeChild = e.Group.prototype.removeChild;
      e.Group.prototype.getChildren = e.Group.prototype.getChildren
    }if(e.Text) {
      e.Text = e.Text;
      e.Text.prototype.className = e.Text.prototype.className;
      e.Text.prototype.getPickType = e.Text.prototype.getPickType;
      e.Text.prototype.setPickType = e.Text.prototype.setPickType;
      e.Text.prototype.getFont = e.Text.prototype.getFont;
      e.Text.prototype.setFont = e.Text.prototype.setFont;
      e.Text.prototype.getSize = e.Text.prototype.getSize;
      e.Text.prototype.setSize = e.Text.prototype.setSize;
      e.Text.prototype.getText = e.Text.prototype.getText;
      e.Text.prototype.setText = e.Text.prototype.setText;
      e.Text.prototype.setColor = e.Text.prototype.setColor;
      e.Text.prototype.setColorR = e.Text.prototype.setColorR;
      e.Text.prototype.setColorG = e.Text.prototype.setColorG;
      e.Text.prototype.setColorB = e.Text.prototype.setColorB;
      e.Text.prototype.getColor = e.Text.prototype.getColor;
      e.Text.prototype.setZtransparent = e.Text.prototype.setZtransparent;
      e.Text.prototype.isZtransparent = e.Text.prototype.isZtransparent
    }if(e.MultiMaterial) {
      e.MultiMaterial = e.MultiMaterial;
      e.MultiMaterial.prototype.className = e.MultiMaterial.prototype.className;
      e.MultiMaterial.prototype.setMesh = e.MultiMaterial.prototype.setMesh;
      e.MultiMaterial.prototype.getMesh = e.MultiMaterial.prototype.getMesh;
      e.MultiMaterial.prototype.setMaterial = e.MultiMaterial.prototype.setMaterial;
      e.MultiMaterial.prototype.getMaterial = e.MultiMaterial.prototype.getMaterial
    }if(e.Object instanceof Object) {
      e.Object = e.Object;
      e.Object.prototype.className = e.Object.prototype.className;
      e.Object.prototype.setZtransparent = e.Object.prototype.setZtransparent;
      e.Object.prototype.isZtransparent = e.Object.prototype.isZtransparent;
      e.Object.prototype.setSkeleton = e.Object.prototype.setSkeleton;
      e.Object.prototype.getSkeleton = e.Object.prototype.getSkeleton;
      e.Object.prototype.setMaterial = e.Object.prototype.setMaterial;
      e.Object.prototype.getMaterial = e.Object.prototype.getMaterial;
      e.Object.prototype.setMesh = e.Object.prototype.setMesh;
      e.Object.prototype.getMesh = e.Object.prototype.getMesh;
      e.Object.prototype.addMultiMaterial = e.Object.prototype.addMultiMaterial;
      e.Object.prototype.getMultiMaterials = e.Object.prototype.getMultiMaterials
    }if(e.Mesh) {
      e.Mesh = e.Mesh;
      e.Mesh.prototype.className = e.Mesh.prototype.className;
      e.Mesh.prototype.setJoints = e.Mesh.prototype.setJoints;
      e.Mesh.prototype.setInvBindMatrix = e.Mesh.prototype.setInvBindMatrix;
      e.Mesh.prototype.setVertexJoints = e.Mesh.prototype.setVertexJoints;
      e.Mesh.prototype.setVertexWeights = e.Mesh.prototype.setVertexWeights;
      e.Mesh.prototype.setUV = e.Mesh.prototype.setUV;
      e.Mesh.prototype.setUV2 = e.Mesh.prototype.setUV2;
      e.Mesh.prototype.setPositions = e.Mesh.prototype.setPositions;
      e.Mesh.prototype.setNormals = e.Mesh.prototype.setNormals;
      e.Mesh.prototype.setBuffer = e.Mesh.prototype.setBuffer;
      e.Mesh.prototype.setFaces = e.Mesh.prototype.setFaces;
      e.Mesh.prototype.addObject = e.Mesh.prototype.addObject;
      e.Mesh.prototype.removeObject = e.Mesh.prototype.removeObject
    }e.L_POINT = e.L_POINT;
    e.L_DIR = e.L_DIR;
    e.L_SPOT = e.L_SPOT;
    if(e.Light) {
      e.Light = e.Light;
      e.Light.prototype.className = e.Light.prototype.className;
      e.Light.prototype.getPMatrix = e.Light.prototype.getPMatrix;
      e.Light.prototype.setCastShadows = e.Light.prototype.setCastShadows;
      e.Light.prototype.getCastShadows = e.Light.prototype.getCastShadows;
      e.Light.prototype.setShadowBias = e.Light.prototype.setShadowBias;
      e.Light.prototype.getShadowBias = e.Light.prototype.getShadowBias;
      e.Light.prototype.setBufferWidth = e.Light.prototype.setBufferWidth;
      e.Light.prototype.getBufferHeight = e.Light.prototype.getBufferHeight;
      e.Light.prototype.setBufferHeight = e.Light.prototype.setBufferHeight;
      e.Light.prototype.getBufferWidth = e.Light.prototype.getBufferWidth;
      e.Light.prototype.setSpotCosCutOff = e.Light.prototype.setSpotCosCutOff;
      e.Light.prototype.getSpotCosCutOff = e.Light.prototype.getSpotCosCutOff;
      e.Light.prototype.setSpotExponent = e.Light.prototype.setSpotExponent;
      e.Light.prototype.getSpotExponent = e.Light.prototype.getSpotExponent;
      e.Light.prototype.getAttenuation = e.Light.prototype.getAttenuation;
      e.Light.prototype.setAttenuation = e.Light.prototype.setAttenuation;
      e.Light.prototype.setAttenuationConstant = e.Light.prototype.setAttenuationConstant;
      e.Light.prototype.setAttenuationLinear = e.Light.prototype.setAttenuationLinear;
      e.Light.prototype.setAttenuationQuadratic = e.Light.prototype.setAttenuationQuadratic;
      e.Light.prototype.setColor = e.Light.prototype.setColor;
      e.Light.prototype.setColorR = e.Light.prototype.setColorR;
      e.Light.prototype.setColorG = e.Light.prototype.setColorG;
      e.Light.prototype.setColorB = e.Light.prototype.setColorB;
      e.Light.prototype.getColor = e.Light.prototype.getColor;
      e.Light.prototype.getType = e.Light.prototype.getType;
      e.Light.prototype.setType = e.Light.prototype.setType
    }e.C_PERSPECTIVE = e.C_PERSPECTIVE;
    e.C_ORTHO = e.C_ORTHO;
    if(e.Camera) {
      e.Camera = e.Camera;
      e.Camera.prototype.className = e.Camera.prototype.className;
      e.Camera.prototype.getOrthoScale = e.Camera.prototype.getOrthoScale;
      e.Camera.prototype.setOrthoScale = e.Camera.prototype.setOrthoScale;
      e.Camera.prototype.getFar = e.Camera.prototype.getFar;
      e.Camera.prototype.setFar = e.Camera.prototype.setFar;
      e.Camera.prototype.getNear = e.Camera.prototype.getNear;
      e.Camera.prototype.setNear = e.Camera.prototype.setNear;
      e.Camera.prototype.getType = e.Camera.prototype.getType;
      e.Camera.prototype.setType = e.Camera.prototype.setType;
      e.Camera.prototype.getFovY = e.Camera.prototype.getFovY;
      e.Camera.prototype.setFovY = e.Camera.prototype.setFovY;
      e.Camera.prototype.getAspect = e.Camera.prototype.getAspect;
      e.Camera.prototype.setAspect = e.Camera.prototype.setAspect;
      e.Camera.prototype.getProjectionMatrix = e.Camera.prototype.getProjectionMatrix;
      e.Camera.prototype.setProjectionMatrix = e.Camera.prototype.setProjectionMatrix;
      e.Camera.prototype.getViewMatrix = e.Camera.prototype.getViewMatrix
    }e.FOG_NONE = e.FOG_NONE;
    e.FOG_LINEAR = e.FOG_LINEAR;
    e.FOG_QUADRATIC = e.FOG_QUADRATIC;
    if(e.Scene) {
      e.Scene = e.Scene;
      e.Scene.prototype.className = e.Scene.prototype.className;
      e.Scene.prototype.getFogType = e.Scene.prototype.getFogType;
      e.Scene.prototype.setFogType = e.Scene.prototype.setFogType;
      e.Scene.prototype.getFogFar = e.Scene.prototype.getFogFar;
      e.Scene.prototype.setFogFar = e.Scene.prototype.setFogFar;
      e.Scene.prototype.getFogNear = e.Scene.prototype.getFogNear;
      e.Scene.prototype.setFogNear = e.Scene.prototype.setFogNear;
      e.Scene.prototype.getFogColor = e.Scene.prototype.getFogColor;
      e.Scene.prototype.setFogColor = e.Scene.prototype.setFogColor;
      e.Scene.prototype.getBackgroundColor = e.Scene.prototype.getBackgroundColor;
      e.Scene.prototype.setBackgroundColor = e.Scene.prototype.setBackgroundColor;
      e.Scene.prototype.getAmbientColor = e.Scene.prototype.getAmbientColor;
      e.Scene.prototype.setAmbientColor = e.Scene.prototype.setAmbientColor;
      e.Scene.prototype.setAmbientColorR = e.Scene.prototype.setAmbientColorR;
      e.Scene.prototype.setAmbientColorG = e.Scene.prototype.setAmbientColorG;
      e.Scene.prototype.setAmbientColorB = e.Scene.prototype.setAmbientColorB;
      e.Scene.prototype.setCamera = e.Scene.prototype.setCamera;
      e.Scene.prototype.getCamera = e.Scene.prototype.getCamera;
      e.Scene.prototype.render = e.Scene.prototype.render;
      e.Scene.prototype.ray = e.Scene.prototype.ray;
      e.Scene.prototype.pick = e.Scene.prototype.pick
    }if(e.Renderer) {
      e.Renderer = e.Renderer;
      e.Renderer.prototype.getScene = e.Renderer.prototype.getScene;
      e.Renderer.prototype.setScene = e.Renderer.prototype.setScene;
      e.Renderer.prototype.render = e.Renderer.prototype.render
    }if(e.Texture) {
      e.Texture = e.Texture;
      e.Texture.prototype.className = e.Texture.prototype.className;
      e.Texture.prototype.getSrc = e.Texture.prototype.getSrc;
      e.Texture.prototype.setSrc = e.Texture.prototype.setSrc
    }if(e.MaterialLayer) {
      e.MaterialLayer = e.MaterialLayer;
      e.MaterialLayer.prototype.className = e.MaterialLayer.prototype.className;
      e.MaterialLayer.prototype.getMatrix = e.MaterialLayer.prototype.getMatrix;
      e.MaterialLayer.prototype.setTexture = e.MaterialLayer.prototype.setTexture;
      e.MaterialLayer.prototype.getTexture = e.MaterialLayer.prototype.getTexture;
      e.MaterialLayer.prototype.setMapto = e.MaterialLayer.prototype.setMapto;
      e.MaterialLayer.prototype.getMapto = e.MaterialLayer.prototype.getMapto;
      e.MaterialLayer.prototype.setMapinput = e.MaterialLayer.prototype.setMapinput;
      e.MaterialLayer.prototype.getMapinput = e.MaterialLayer.prototype.getMapinput;
      e.MaterialLayer.prototype.getOffset = e.MaterialLayer.prototype.getOffset;
      e.MaterialLayer.prototype.getRotation = e.MaterialLayer.prototype.getRotation;
      e.MaterialLayer.prototype.getScale = e.MaterialLayer.prototype.getScale;
      e.MaterialLayer.prototype.setOffsetX = e.MaterialLayer.prototype.setOffsetX;
      e.MaterialLayer.prototype.getOffsetX = e.MaterialLayer.prototype.getOffsetX;
      e.MaterialLayer.prototype.setOffsetY = e.MaterialLayer.prototype.setOffsetY;
      e.MaterialLayer.prototype.getOffsetY = e.MaterialLayer.prototype.getOffsetY;
      e.MaterialLayer.prototype.setOffsetZ = e.MaterialLayer.prototype.setOffsetZ;
      e.MaterialLayer.prototype.getOffsetZ = e.MaterialLayer.prototype.getOffsetZ;
      e.MaterialLayer.prototype.setDOffsetX = e.MaterialLayer.prototype.setDOffsetX;
      e.MaterialLayer.prototype.getDOffsetX = e.MaterialLayer.prototype.getDOffsetX;
      e.MaterialLayer.prototype.setDOffsetY = e.MaterialLayer.prototype.setDOffsetY;
      e.MaterialLayer.prototype.getDOffsetY = e.MaterialLayer.prototype.getDOffsetY;
      e.MaterialLayer.prototype.setDOffsetZ = e.MaterialLayer.prototype.setDOffsetZ;
      e.MaterialLayer.prototype.getDOffsetZ = e.MaterialLayer.prototype.getDOffsetZ;
      e.MaterialLayer.prototype.setScaleX = e.MaterialLayer.prototype.setScaleX;
      e.MaterialLayer.prototype.getScaleX = e.MaterialLayer.prototype.getScaleX;
      e.MaterialLayer.prototype.setScaleY = e.MaterialLayer.prototype.setScaleY;
      e.MaterialLayer.prototype.getScaleY = e.MaterialLayer.prototype.getScaleY;
      e.MaterialLayer.prototype.setScaleZ = e.MaterialLayer.prototype.setScaleZ;
      e.MaterialLayer.prototype.getScaleZ = e.MaterialLayer.prototype.getScaleZ;
      e.MaterialLayer.prototype.setDScaleX = e.MaterialLayer.prototype.setDScaleX;
      e.MaterialLayer.prototype.getDScaleX = e.MaterialLayer.prototype.getDScaleX;
      e.MaterialLayer.prototype.setDScaleY = e.MaterialLayer.prototype.setDScaleY;
      e.MaterialLayer.prototype.getDScaleY = e.MaterialLayer.prototype.getDScaleY;
      e.MaterialLayer.prototype.setDScaleZ = e.MaterialLayer.prototype.setDScaleZ;
      e.MaterialLayer.prototype.getDScaleZ = e.MaterialLayer.prototype.getDScaleZ;
      e.MaterialLayer.prototype.setRotX = e.MaterialLayer.prototype.setRotX;
      e.MaterialLayer.prototype.getRotX = e.MaterialLayer.prototype.getRotX;
      e.MaterialLayer.prototype.setRotY = e.MaterialLayer.prototype.setRotY;
      e.MaterialLayer.prototype.getRotY = e.MaterialLayer.prototype.getRotY;
      e.MaterialLayer.prototype.setRotZ = e.MaterialLayer.prototype.setRotZ;
      e.MaterialLayer.prototype.getRotZ = e.MaterialLayer.prototype.getRotZ;
      e.MaterialLayer.prototype.setDRotX = e.MaterialLayer.prototype.setDRotX;
      e.MaterialLayer.prototype.getDRotX = e.MaterialLayer.prototype.getDRotX;
      e.MaterialLayer.prototype.setDRotY = e.MaterialLayer.prototype.setDRotY;
      e.MaterialLayer.prototype.getDRotY = e.MaterialLayer.prototype.getDRotY;
      e.MaterialLayer.prototype.setDRotZ = e.MaterialLayer.prototype.setDRotZ;
      e.MaterialLayer.prototype.getDRotZ = e.MaterialLayer.prototype.getDRotZ;
      e.MaterialLayer.prototype.setBlendMode = e.MaterialLayer.prototype.setBlendMode;
      e.MaterialLayer.prototype.getBlendMode = e.MaterialLayer.prototype.getBlendMode
    }e.M_COLOR = e.M_COLOR;
    e.M_NOR = e.M_NOR;
    e.M_ALPHA = e.M_ALPHA;
    e.M_SPECCOLOR = e.M_SPECCOLOR;
    e.M_SPECULAR = e.M_SPECULAR;
    e.M_SHINE = e.M_SHINE;
    e.M_REFLECT = e.M_REFLECT;
    e.M_EMIT = e.M_EMIT;
    e.M_ALPHA = e.M_ALPHA;
    e.M_MSKR = e.M_MSKR;
    e.M_MSKG = e.M_MSKG;
    e.M_MSKB = e.M_MSKB;
    e.M_MSKA = e.M_MSKA;
    e.M_HEIGHT = e.M_HEIGHT;
    e.UV1 = e.UV1;
    e.UV2 = e.UV2;
    e.MAP_NORM = e.MAP_NORM;
    e.MAP_OBJ = e.MAP_OBJ;
    e.BL_MIX = e.BL_MIX;
    e.BL_MUL = e.BL_MUL;
    if(e.Material) {
      e.Material = e.Material;
      e.Material.prototype.className = e.Material.prototype.className;
      e.Material.prototype.setShadow = e.Material.prototype.setShadow;
      e.Material.prototype.getShadow = e.Material.prototype.getShadow;
      e.Material.prototype.setColor = e.Material.prototype.setColor;
      e.Material.prototype.setColorR = e.Material.prototype.setColorR;
      e.Material.prototype.setColorG = e.Material.prototype.setColorG;
      e.Material.prototype.setColorB = e.Material.prototype.setColorB;
      e.Material.prototype.getColor = e.Material.prototype.getColor;
      e.Material.prototype.setSpecularColor = e.Material.prototype.setSpecularColor;
      e.Material.prototype.getSpecularColor = e.Material.prototype.getSpecularColor;
      e.Material.prototype.setAlpha = e.Material.prototype.setAlpha;
      e.Material.prototype.getAlpha = e.Material.prototype.getAlpha;
      e.Material.prototype.setSpecular = e.Material.prototype.setSpecular;
      e.Material.prototype.getSpecular = e.Material.prototype.getSpecular;
      e.Material.prototype.setShininess = e.Material.prototype.setShininess;
      e.Material.prototype.getShininess = e.Material.prototype.getShininess;
      e.Material.prototype.setEmit = e.Material.prototype.setEmit;
      e.Material.prototype.getEmit = e.Material.prototype.getEmit;
      e.Material.prototype.setReflectivity = e.Material.prototype.setReflectivity;
      e.Material.prototype.getReflectivity = e.Material.prototype.getReflectivity;
      e.Material.prototype.addMaterialLayer = e.Material.prototype.addMaterialLayer;
      e.Material.prototype.getLayers = e.Material.prototype.getLayers;
      e.Material.prototype.addTexture = e.Material.prototype.addTexture
    }
  }
  var h = function(f) {
    return typeof f != "number" ? parseFloat(f) : f
  };
  e.augment = function(f, g) {
    for(proto in f.prototype) {
      g.prototype[proto] = f.prototype[proto]
    }
  };
  e.makeGlobal = function() {
    for(var f in e) {
      window[f] = e[f]
    }
  };
  e.New = function(f) {
    return e[f].prototype.className != "" ? new e[f] : false
  };
  e.TRUE = 1;
  e.FALSE = 0;
  e.DRAW_TRIS = 1;
  e.DRAW_LINES = 2;
  e.DRAW_LINELOOPS = 3;
  e.DRAW_LINESTRIPS = 4;
  e.DRAW_POINTS = 5;
  e.RENDER_DEFAULT = 0;
  e.RENDER_SHADOW = 1;
  e.RENDER_PICK = 2;
  e.RENDER_NORMAL = 3;
  e.RENDER_NULL = 4;
  e.TEXT_BOXPICK = 1;
  e.TEXT_TEXTPICK = 1;
  e.P_EULER = 1;
  e.P_QUAT = 2;
  e.P_MATRIX = 3;
  e.NONE = 0;
  e.XAXIS = 1;
  e.YAXIS = 2;
  e.ZAXIS = 3;
  e.POS_XAXIS = 1;
  e.NEG_XAXIS = 2;
  e.POS_YAXIS = 3;
  e.NEG_YAXIS = 4;
  e.POS_ZAXIS = 5;
  e.NEG_ZAXIS = 6;
  e.LINEAR_BLEND = function(f) {
    return f
  };
  e.QUAD_BLEND = function(f) {
    return f * f
  };
  e.SPECIAL_BLEND = function(f) {
    f *= 2 - f;
    return f * f
  };
  e.error = function(f) {
    console && console.log && console.log("GLGE error: " + f)
  };
  e.Assets = {};
  e.Assets.assets = {};
  e.Assets.createUUID = function() {
    var f = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"], g = ["8", "9", "A", "B"];
    uuid = "";
    for(var m = 0;m < 38;m++) {
      switch(m) {
        case 8:
          uuid += "-";
          break;
        case 13:
          uuid += "-";
          break;
        case 18:
          uuid += "-";
          break;
        case 14:
          uuid += "4";
          break;
        case 19:
          uuid += g[Math.round(Math.random() * 3)];
          break;
        default:
          uuid += f[Math.round(Math.random() * 15)];
          break
      }
    }return uuid
  };
  e.Assets.registerAsset = function(f, g) {
    g || (g = e.Assets.createUUID());
    f.uid = g;
    e.Assets.assets[g] = f
  };
  e.Assets.unregisterAsset = function(f) {
    delete e.Assets.assets[f]
  };
  e.Assets.get = function(f) {
    return(f = e.Assets.assets[f]) ? f : false
  };
  e.fastHash = function(f) {
    var g = 0, m = 0, p = 0, r = 0, s = 0, A = 0, v = 0, B = 0, C = 0, E = 0, H = 0, J = 0, M = 0, K = f.length;
    for(f += "000000";M < K;) {
      v = f.charCodeAt(M++);
      B = f.charCodeAt(M++);
      C = f.charCodeAt(M++);
      E = f.charCodeAt(M++);
      H = f.charCodeAt(M++);
      J = f.charCodeAt(M++);
      g = (s + v + B) % 255;
      m = (A + B + C) % 255;
      p = (g + C + E) % 255;
      r = (m + E + H) % 255;
      s = (p + H + J) % 255;
      A = (r + J + v) % 255
    }return[String.fromCharCode(g), String.fromCharCode(m), String.fromCharCode(p), String.fromCharCode(r), String.fromCharCode(s), String.fromCharCode(A)].join("")
  };
  e.getGLShader = function(f, g, m) {
    var p = e.fastHash(m);
    if(!f.shaderCache) {
      f.shaderCache = {}
    }if(!f.shaderCache[p]) {
      g = f.createShader(g);
      f.shaderSource(g, m);
      f.compileShader(g);
      if(!f.getShaderParameter(g, f.COMPILE_STATUS)) {
        try {
          e.error(f.getShaderInfoLog(g));
          return
        }catch(r) {
        }
      }f.shaderCache[p] = g
    }return f.shaderCache[p]
  };
  var o = 0;
  e.getGLProgram = function(f, g, m) {
    if(!f.programCache) {
      f.programCache = []
    }for(var p = f.programCache, r = 0;r < p.length;r++) {
      if(p[r].fShader == m && p[r].vShader == g) {
        return p[r].program
      }
    }var s = f.createProgram();
    s.progIdx = o++;
    f.attachShader(s, g);
    f.attachShader(s, m);
    f.linkProgram(s);
    p.push({vShader:g, fShader:m, program:s});
    if(!s.uniformDetails) {
      s.uniformDetails = {};
      g = f.getProgramParameter(s, f.ACTIVE_UNIFORMS);
      for(r = 0;r < g;++r) {
        m = f.getActiveUniform(s, r);
        s.uniformDetails[m.name] = {loc:e.getUniformLocation(f, s, m.name), info:m}
      }
    }return s
  };
  e.getUniformLocation = function(f, g, m) {
    if(!g.uniformCache) {
      g.uniformCache = {}
    }if(!g.uniformChecked) {
      g.uniformChecked = {}
    }if(!g.uniformChecked[m]) {
      g.uniformCache[m] = f.getUniformLocation(g, m);
      g.uniformChecked[m] = true
    }return g.uniformCache[m]
  };
  e.setUniform = function(f, g, m, p) {
    if(typeof p == "string") {
      p = +p
    }m != null && f["uniform" + g](m, p)
  };
  e.setUniform3 = function(f, g, m, p, r, s) {
    if(typeof p == "string") {
      p = +p
    }if(typeof r == "string") {
      r = +r
    }if(typeof s == "string") {
      s = +s
    }m != null && f["uniform" + g](m, p, r, s)
  };
  e.setUniform4 = function(f, g, m, p, r, s, A) {
    m != null && f["uniform" + g](m, p, r, s, A)
  };
  e.setUniformMatrix = function(f, g, m, p, r) {
    m != null && f["uniform" + g](m, p, r)
  };
  e.getAttribLocation = function(f, g, m) {
    if(!g.attribCache) {
      g.attribCache = {}
    }if(g.attribCache[m] == undefined) {
      g.attribCache[m] = f.getAttribLocation(g, m)
    }return g.attribCache[m]
  };
  e.QuickNotation = function() {
  };
  e.QuickNotation.prototype._ = function() {
    for(var f, g = 0;g < arguments.length;g++) {
      f = arguments[g];
      if(typeof f == "object") {
        if(f.className && this["add" + f.className]) {
          this["add" + f.className](f)
        }else {
          for(var m in f) {
            this["set" + m] && this["set" + m](f[m])
          }
        }
      }
    }return this
  };
  e.Message = {};
  e.Message.parseMessage = function(f) {
    switch(f.command) {
      case "create":
        var g = new e[f.type](f.uid);
        this.setAttributes(g, f.attributes);
        f.children && e.Message.addChildren(g, f.children);
        return g;
      case "update":
        g = e.Assets.get(f.uid);
        this.setAttributes(g, f.attributes);
        f.add && e.Message.addChildren(g, f.add);
        f.remove && e.Message.removeChildren(g, f.remove);
        return g
    }
    return null
  };
  e.Message.setAttributes = function(f, g) {
    if(g) {
      for(var m in g) {
        if(f["set" + m]) {
          if(g[m].command) {
            g[m] = e.Message.parseMessage(g[m])
          }f["set" + m](g[m])
        }
      }
    }return this
  };
  e.Message.addChildren = function(f, g) {
    g instanceof Array || (g = [g]);
    for(var m = 0;m < g.length;m++) {
      var p = g[m].command ? e.Message.parseMessage(g[m]) : e.Assets.get(g[m]);
      f["add" + p.className](p)
    }
  };
  e.Message.removeChildren = function(f, g) {
    g instanceof Array || (g = [g]);
    for(var m = 0;m < g.length;m++) {
      var p = e.Assets.get(g[m]);
      f["add" + p.className](p)
    }
  };
  e.Message.toLoad = [];
  e.Message.messageLoader = function(f, g, m) {
    e.Message.toLoad.push([f, g, m]);
    e.Message.toLoad.length == 1 && e.Message.loadMessages()
  };
  e.Message.loadMessages = function() {
    var f = e.Message.toLoad.pop(), g = new XMLHttpRequest;
    g.onreadystatechange = function() {
      if(this.readyState == 4) {
        this.status == 200 || this.status == 0 ? f[1](this.responseText) : e.error("Error loading Document: " + f[0] + " status " + this.status)
      }
    };
    g.open("GET", f[0], true);
    g.send("");
    e.Message.toLoad.length > 0 && e.Message.loadMessages()
  };
  e.colorParse = function(f) {
    var g, m, p, r, s = {aliceblue:"f0f8ff", antiquewhite:"faebd7", aqua:"00ffff", aquamarine:"7fffd4", azure:"f0ffff", beige:"f5f5dc", bisque:"ffe4c4", black:"000000", blanchedalmond:"ffebcd", blue:"0000ff", blueviolet:"8a2be2", brown:"a52a2a", burlywood:"deb887", cadetblue:"5f9ea0", chartreuse:"7fff00", chocolate:"d2691e", coral:"ff7f50", cornflowerblue:"6495ed", cornsilk:"fff8dc", crimson:"dc143c", cyan:"00ffff", darkblue:"00008b", darkcyan:"008b8b", darkgoldenrod:"b8860b", darkgray:"a9a9a9", 
    darkgreen:"006400", darkkhaki:"bdb76b", darkmagenta:"8b008b", darkolivegreen:"556b2f", darkorange:"ff8c00", darkorchid:"9932cc", darkred:"8b0000", darksalmon:"e9967a", darkseagreen:"8fbc8f", darkslateblue:"483d8b", darkslategray:"2f4f4f", darkturquoise:"00ced1", darkviolet:"9400d3", deeppink:"ff1493", deepskyblue:"00bfff", dimgray:"696969", dodgerblue:"1e90ff", feldspar:"d19275", firebrick:"b22222", floralwhite:"fffaf0", forestgreen:"228b22", fuchsia:"ff00ff", gainsboro:"dcdcdc", ghostwhite:"f8f8ff", 
    gold:"ffd700", goldenrod:"daa520", gray:"808080", green:"008000", greenyellow:"adff2f", honeydew:"f0fff0", hotpink:"ff69b4", indianred:"cd5c5c", indigo:"4b0082", ivory:"fffff0", khaki:"f0e68c", lavender:"e6e6fa", lavenderblush:"fff0f5", lawngreen:"7cfc00", lemonchiffon:"fffacd", lightblue:"add8e6", lightcoral:"f08080", lightcyan:"e0ffff", lightgoldenrodyellow:"fafad2", lightgrey:"d3d3d3", lightgreen:"90ee90", lightpink:"ffb6c1", lightsalmon:"ffa07a", lightseagreen:"20b2aa", lightskyblue:"87cefa", 
    lightslateblue:"8470ff", lightslategray:"778899", lightsteelblue:"b0c4de", lightyellow:"ffffe0", lime:"00ff00", limegreen:"32cd32", linen:"faf0e6", magenta:"ff00ff", maroon:"800000", mediumaquamarine:"66cdaa", mediumblue:"0000cd", mediumorchid:"ba55d3", mediumpurple:"9370d8", mediumseagreen:"3cb371", mediumslateblue:"7b68ee", mediumspringgreen:"00fa9a", mediumturquoise:"48d1cc", mediumvioletred:"c71585", midnightblue:"191970", mintcream:"f5fffa", mistyrose:"ffe4e1", moccasin:"ffe4b5", navajowhite:"ffdead", 
    navy:"000080", oldlace:"fdf5e6", olive:"808000", olivedrab:"6b8e23", orange:"ffa500", orangered:"ff4500", orchid:"da70d6", palegoldenrod:"eee8aa", palegreen:"98fb98", paleturquoise:"afeeee", palevioletred:"d87093", papayawhip:"ffefd5", peachpuff:"ffdab9", peru:"cd853f", pink:"ffc0cb", plum:"dda0dd", powderblue:"b0e0e6", purple:"800080", red:"ff0000", rosybrown:"bc8f8f", royalblue:"4169e1", saddlebrown:"8b4513", salmon:"fa8072", sandybrown:"f4a460", seagreen:"2e8b57", seashell:"fff5ee", sienna:"a0522d", 
    silver:"c0c0c0", skyblue:"87ceeb", slateblue:"6a5acd", slategray:"708090", snow:"fffafa", springgreen:"00ff7f", steelblue:"4682b4", tan:"d2b48c", teal:"008080", thistle:"d8bfd8", tomato:"ff6347", turquoise:"40e0d0", violet:"ee82ee", violetred:"d02090", wheat:"f5deb3", white:"ffffff", whitesmoke:"f5f5f5", yellow:"ffff00", yellowgreen:"9acd32"};
    if(s[f]) {
      f = "#" + s[f]
    }if(f.substr && f.substr(0, 1) == "#") {
      f = f.substr(1);
      if(f.length == 8) {
        g = parseInt("0x" + f.substr(0, 2)) / 255;
        m = parseInt("0x" + f.substr(2, 2)) / 255;
        p = parseInt("0x" + f.substr(4, 2)) / 255;
        r = parseInt("0x" + f.substr(6, 2)) / 255
      }else {
        if(f.length == 4) {
          g = parseInt("0x" + f.substr(0, 1)) / 15;
          m = parseInt("0x" + f.substr(1, 1)) / 15;
          p = parseInt("0x" + f.substr(2, 1)) / 15;
          r = parseInt("0x" + f.substr(3, 1)) / 15
        }else {
          if(f.length == 6) {
            g = parseInt("0x" + f.substr(0, 2)) / 255;
            m = parseInt("0x" + f.substr(2, 2)) / 255;
            p = parseInt("0x" + f.substr(4, 2)) / 255;
            r = 1
          }else {
            if(f.length == 3) {
              g = parseInt("0x" + f.substr(0, 1)) / 15;
              m = parseInt("0x" + f.substr(1, 1)) / 15;
              p = parseInt("0x" + f.substr(2, 1)) / 15;
              r = 1
            }
          }
        }
      }
    }else {
      if(f.substr && f.substr(0, 4) == "rgb(") {
        f = f.substr(4).split(",");
        g = parseInt(f[0]) / 255;
        m = parseInt(f[1]) / 255;
        p = parseInt(f[2]) / 255;
        r = 1
      }else {
        if(f.substr && f.substr(0, 5) == "rgba(") {
          f = f.substr(4).split(",");
          g = parseInt(f[0]) / 255;
          m = parseInt(f[1]) / 255;
          p = parseInt(f[2]) / 255;
          r = parseInt(f[3]) / 255
        }else {
          r = p = m = g = 0
        }
      }
    }return{r:g, g:m, b:p, a:r}
  };
  e.JSONLoader = function() {
  };
  e.JSONLoader.prototype.downloadPriority = 0;
  e.JSONLoader.prototype.setJSONSrc = function(f) {
    var g = this;
    e.Message.messageLoader(f, function(m) {
      g.setJSONString(m)
    }, this.downloadPriority)
  };
  e.JSONLoader.prototype.setJSONString = function(f) {
    f = JSON.parse(f);
    if(f.type == this.className) {
      f.uid = this.uid;
      f.command = "update";
      e.Message.parseMessage(f)
    }
  };
  e.JSONLoader.prototype.setDownloadPriority = function(f) {
    this.downloadPriority = f
  };
  e.JSONLoader.prototype.getDownloadPriority = function() {
    return this.downloadPriority
  };
  e.Events = function() {
  };
  e.Events.prototype.fireEvent = function(f, g) {
    if(this.events && this.events[f]) {
      f = this.events[f];
      for(var m = 0;m < f.length;m++) {
        f[m].call(this, g)
      }
    }
  };
  e.Events.prototype.addEventListener = function(f, g) {
    if(!this.events) {
      this.events = {}
    }this.events[f] || (this.events[f] = []);
    this.events[f].push(g)
  };
  e.Events.prototype.removeEventListener = function(f, g) {
    g = this.events[f].indexOf(g);
    g != -1 && this.events[f].splice(g, 1)
  };
  e.Document = function() {
    this.listeners = [];
    this.documents = []
  };
  e.Document.prototype.listeners = null;
  e.Document.prototype.documents = null;
  e.Document.prototype.rootURL = null;
  e.Document.prototype.loadCount = 0;
  e.Document.prototype.version = 0;
  e.Document.prototype.getElementById = function(f) {
    for(var g = this.getElementsByTagName("*"), m = 0;m < g.length;m++) {
      if(g[m].getAttribute("id") == f) {
        return g[m]
      }
    }return null
  };
  e.Document.prototype.getAbsolutePath = function(f, g) {
    if(f.substr(0, 7) == "http://" || f.substr(0, 7) == "file://" || f.substr(0, 8) == "https://") {
      return f
    }else {
      if(!g) {
        g = window.location.href
      }var m = g.split("/");
      g = m[2];
      for(var p = m[0], r = [], s = 3;s < m.length - 1;s++) {
        r.push(m[s])
      }if(f.substr(0, 1) == "/") {
        r = []
      }f = f.split("/");
      for(s = 0;s < f.length;s++) {
        if(f[s] == "..") {
          r.pop()
        }else {
          f[s] != "" && r.push(f[s])
        }
      }return p + "//" + g + "/" + r.join("/")
    }
  };
  e.Document.prototype.load = function(f) {
    this.documents = [];
    this.rootURL = f;
    this.loadDocument(f, null)
  };
  e.Document.prototype.loadDocument = function(f, g) {
    this.loadCount++;
    f = this.getAbsolutePath(f, g);
    if(g = new XMLHttpRequest) {
      g.docurl = f;
      g.docObj = this;
      g.overrideMimeType("text/xml");
      g.onreadystatechange = function() {
        if(this.readyState == 4) {
          if(this.status == 200 || this.status == 0) {
            this.responseXML.getElementById = this.docObj.getElementById;
            this.docObj.loaded(this.docurl, this.responseXML)
          }else {
            e.error("Error loading Document: " + this.docurl + " status " + this.status)
          }
        }
      };
      g.open("GET", f, true);
      g.send("")
    }
  };
  e.Document.prototype.loaded = function(f, g) {
    this.loadCount--;
    this.documents[f] = {xml:g};
    var m = g.getElementsByTagName("glge");
    if(m[0] && m[0].hasAttribute("version")) {
      this.version = parseFloat(m[0].getAttribute("version"))
    }g = g.getElementsByTagName("import");
    for(m = 0;m < g.length;m++) {
      if(!this.documents[this.getAbsolutePath(g[m].getAttribute("url"), f)]) {
        this.documents[this.getAbsolutePath(g[m].getAttribute("url"), f)] = {};
        this.loadDocument(g[m].getAttribute("url"), f)
      }
    }this.loadCount == 0 && this.finishedLoading()
  };
  e.Document.prototype.finishedLoading = function() {
    for(var f = 0;f < this.listeners.length;f++) {
      this.listeners[f](this.listeners.rootURL)
    }this.onLoad()
  };
  e.Document.prototype.onLoad = function() {
  };
  e.Document.prototype.classString = function(f) {
    if(!f) {
      return false
    }f = f.split("_");
    for(var g = "", m = 0;m < f.length;m++) {
      g = g + f[m][0].toUpperCase() + f[m].substr(1)
    }return g
  };
  e.Document.prototype.setProperties = function(f) {
    for(var g, m, p = 0;p < f.attributes.length;p++) {
      m = false;
      g = "set" + this.classString(f.attributes[p].nodeName);
      if(f.attributes[p].value[0] == "#") {
        m = this.getElement(f.attributes[p].value.substr(1), true)
      }m || (m = typeof e[f.attributes[p].value] != "undefined" ? e[f.attributes[p].value] : f.attributes[p].value);
      f.object[g] && f.object[g](m);
      if(f.attributes[p].nodeName == "uid") {
        e.Assets.unregisterAsset(f.object.uid);
        f.object.uid = f.attributes[p].value;
        e.Assets.registerAsset(f.object, f.attributes[p].value)
      }
    }
  };
  e.Document.prototype.addChildren = function(f) {
    for(var g, m = f.firstChild;m;) {
      g = "add" + this.classString(m.tagName);
      f.object[g] && f.object[g](this.getElement(m));
      m = m.nextSibling
    }
  };
  e.Document.prototype.getElement = function(f, g) {
    var m, p;
    if(typeof f == "string") {
      for(p in this.documents) {
        if(this.documents[p].xml) {
          if(m = this.documents[p].xml.getElementById(f)) {
            f = m;
            break
          }
        }
      }
    }if(typeof f == "string") {
      g || e.error("Element " + f + " not found in document");
      return false
    }else {
      return this["get" + this.classString(f.tagName)] ? this["get" + this.classString(f.tagName)](f) : this.getDefault(f)
    }
  };
  e.Document.prototype.getData = function(f) {
    if(!f.object) {
      f.object = this.parseArray(f);
      if(f.hasAttribute("type")) {
        switch(f.getAttribute("type")) {
          case "matrix":
            for(var g = 0;g < f.object.length;g++) {
              f.object[g] = e.Mat4(f.object[g].split(" "))
            }break;
          case "links":
            for(g = 0;g < f.object.length;g++) {
              f.object[g] = this.getElement(f.object[g].substr(1))
            }break
        }
      }
    }return f.object
  };
  e.Document.prototype.getDefault = function(f) {
    if(!f.object) {
      if(e[this.classString(f.tagName)]) {
        f.object = new (e[this.classString(f.tagName)]);
        this.setProperties(f);
        this.addChildren(f)
      }else {
        e.error("XML Parse Error: GLGE Object not found")
      }
    }return f.object
  };
  e.Document.prototype.getTexture = function(f) {
    if(!f.object) {
      var g = this.getAbsolutePath(this.rootURL, null);
      f.object = new (e[this.classString(f.tagName)]);
      f.object.setSrc(this.getAbsolutePath(f.getAttribute("src"), g));
      f.removeAttribute("src");
      this.setProperties(f)
    }return f.object
  };
  e.Document.prototype.getTextureVideo = e.Document.prototype.getTexture;
  e.Document.prototype.parseArray = function(f) {
    f = f.firstChild;
    for(var g = "", m = [], p, r;f;) {
      p = (g + f.nodeValue).split(",");
      f = f.nextSibling;
      p[0] == "" && p.unshift();
      if(f) {
        g = p.pop()
      }for(r = 0;r < p.length;r++) {
        m.push(p[r])
      }
    }return m
  };
  e.Document.prototype.getMesh = function(f) {
    if(this.version > 0) {
      return this.getDefault(f)
    }if(!f.object) {
      f.object = new e.Mesh;
      this.setProperties(f);
      for(var g = f.firstChild;g;) {
        switch(g.tagName) {
          case "positions":
            f.object.setPositions(this.parseArray(g));
            break;
          case "normals":
            f.object.setNormals(this.parseArray(g));
            break;
          case "uv1":
            f.object.setUV(this.parseArray(g));
            break;
          case "uv2":
            f.object.setUV2(this.parseArray(g));
            break;
          case "faces":
            f.object.setFaces(this.parseArray(g));
            break;
          case "joint_names":
            for(var m = this.parseArray(g), p = [], r = 0;r < m.length;r++) {
              m[r].substr(0, 1) == "#" ? p.push(this.getElement(m[r].substr(1))) : p.push(m[r])
            }f.object.setJoints(p);
            break;
          case "bind_matrix":
            m = this.parseArray(g);
            p = [];
            for(r = 0;r < m.length;r++) {
              p.push(e.Mat4(m[r].split(" ")))
            }f.object.setInvBindMatrix(p);
            break;
          case "joints":
            f.object.setVertexJoints(this.parseArray(g), g.getAttribute("count"));
            break;
          case "weights":
            f.object.setVertexWeights(this.parseArray(g), g.getAttribute("count"));
            break
        }
        g = g.nextSibling
      }
    }return f.object
  };
  e.Document.prototype.addLoadListener = function(f) {
    this.listeners.push(f)
  };
  e.Document.prototype.removeLoadListener = function(f) {
    for(var g = 0;g < this.listeners.length;g++) {
      this.listeners[g] === f && this.listeners.splice(g, 1)
    }
  };
  e.Document.prototype.parseScript = function(f) {
    this.rootURL = window.location.toString();
    var g = document.getElementById(f);
    if(!g) {
      return null
    }var m = "";
    for(g = g.firstChild;g;) {
      if(g.nodeType == 3) {
        m += g.textContent
      }g = g.nextSibling
    }m = (new DOMParser).parseFromString(m, "text/xml");
    m.getElementById = this.getElementById;
    this.documents["#" + f] = {xml:m};
    f = m.getElementsByTagName("import");
    for(m = 0;m < f.length;m++) {
      if(!this.documents[this.getAbsolutePath(f[m].getAttribute("url"), url)]) {
        this.documents[this.getAbsolutePath(f[m].getAttribute("url"), url)] = {};
        this.loadDocument(f[m].getAttribute("url"))
      }
    }this.loadCount == 0 && this.finishedLoading()
  };
  e.Placeable = function() {
  };
  e.Placeable.prototype.locX = 0;
  e.Placeable.prototype.locY = 0;
  e.Placeable.prototype.locZ = 0;
  e.Placeable.prototype.dLocX = 0;
  e.Placeable.prototype.dLocY = 0;
  e.Placeable.prototype.dLocZ = 0;
  e.Placeable.prototype.quatX = 0;
  e.Placeable.prototype.quatY = 0;
  e.Placeable.prototype.quatZ = 0;
  e.Placeable.prototype.quatW = 0;
  e.Placeable.prototype.rotX = 0;
  e.Placeable.prototype.rotY = 0;
  e.Placeable.prototype.rotZ = 0;
  e.Placeable.prototype.dRotX = 0;
  e.Placeable.prototype.dRotY = 0;
  e.Placeable.prototype.dRotZ = 0;
  e.Placeable.prototype.scaleX = 1;
  e.Placeable.prototype.scaleY = 1;
  e.Placeable.prototype.scaleZ = 1;
  e.Placeable.prototype.dScaleX = 0;
  e.Placeable.prototype.dScaleY = 0;
  e.Placeable.prototype.dScaleZ = 0;
  e.Placeable.prototype.matrix = null;
  e.Placeable.prototype.rotOrder = e.ROT_XYZ;
  e.Placeable.prototype.lookAt = null;
  e.Placeable.prototype.mode = e.P_EULER;
  e.Placeable.prototype.getRoot = function() {
    if(this.type == e.G_ROOT) {
      return this
    }else {
      if(this.parent) {
        var f = this.parent.getRoot();
        return f ? f : this
      }else {
        return this
      }
    }
  };
  e.Placeable.prototype.getRef = function() {
    return this.id ? this.id : this.parent ? this.parent.getRef() : null
  };
  e.Placeable.prototype.setId = function(f) {
    this.id = f;
    return this
  };
  e.Placeable.prototype.getId = function() {
    return this.id
  };
  e.Placeable.prototype.getLookat = function() {
    return this.lookAt
  };
  e.Placeable.prototype.setLookat = function(f) {
    this.lookAt = f;
    return this
  };
  e.Placeable.prototype.Lookat = function(f) {
    var g = this.getPosition();
    f = f.getPosition ? f.getPosition() : {x:f[0], y:f[1], z:f[2]};
    g = e.toUnitVec3([g.x - f.x, g.y - f.y, g.z - f.z]);
    f = e.toUnitVec3(e.crossVec3([0, 0, 1], g));
    var m = e.toUnitVec3(e.crossVec3(g, f));
    this.setRotMatrix(e.Mat4([f[0], m[0], g[0], 0, f[1], m[1], g[1], 0, f[2], m[2], g[2], 0, 0, 0, 0, 1]))
  };
  e.Placeable.prototype.getRotOrder = function() {
    return this.rotOrder
  };
  e.Placeable.prototype.setRotOrder = function(f) {
    this.rotOrder = f;
    this.rotmatrix = this.matrix = null;
    return this
  };
  e.Placeable.prototype.getRotMatrix = function() {
    if(!this.rotmatrix) {
      var f = this.getRotation();
      if(this.mode == e.P_EULER) {
        this.rotmatrix = e.rotateMatrix(f.x, f.y, f.z, this.rotOrder)
      }if(this.mode == e.P_QUAT) {
        this.rotmatrix = e.quatRotation(f.x, f.y, f.z, f.w)
      }
    }return this.rotmatrix
  };
  e.Placeable.prototype.setRotMatrix = function(f) {
    this.mode = e.P_MATRIX;
    this.rotmatrix = f;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setLocX = function(f) {
    this.locX = f;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setLocY = function(f) {
    this.locY = f;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setLocZ = function(f) {
    this.locZ = f;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setLoc = function(f, g, m) {
    this.locX = f;
    this.locY = g;
    this.locZ = m;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDLocX = function(f) {
    this.dLocX = f;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDLocY = function(f) {
    this.dLocY = f;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDLocZ = function(f) {
    this.dLocZ = f;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDLoc = function(f, g, m) {
    this.dLocX = f;
    this.dLocY = g;
    this.dLocZ = m;
    this.staticMatrix = this.translateMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setQuatX = function(f) {
    this.mode = e.P_QUAT;
    this.quatX = parseFloat(f);
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setQuatY = function(f) {
    this.mode = e.P_QUAT;
    this.quatY = parseFloat(f);
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setQuatZ = function(f) {
    this.mode = e.P_QUAT;
    this.quatZ = parseFloat(f);
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setQuatW = function(f) {
    this.mode = e.P_QUAT;
    this.quatW = parseFloat(f);
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setQuat = function(f, g, m, p) {
    this.mode = e.P_QUAT;
    this.quatX = f;
    this.quatY = g;
    this.quatZ = m;
    this.quatW = p;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setRotX = function(f) {
    this.mode = e.P_EULER;
    this.rotX = f;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setRotY = function(f) {
    this.mode = e.P_EULER;
    this.rotY = f;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setRotZ = function(f) {
    this.mode = e.P_EULER;
    this.rotZ = f;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setRot = function(f, g, m) {
    this.mode = e.P_EULER;
    this.rotX = f;
    this.rotY = g;
    this.rotZ = m;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDRotX = function(f) {
    this.mode = e.P_EULER;
    this.dRotX = f;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDRotY = function(f) {
    this.mode = e.P_EULER;
    this.dRotY = f;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDRotZ = function(f) {
    this.mode = e.P_EULER;
    this.dRotZ = f;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDRot = function(f, g, m) {
    this.mode = e.P_EULER;
    this.dRotX = f;
    this.dRotY = g;
    this.dRotZ = m;
    this.rotmatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setScaleX = function(f) {
    if(this.ScaleX == f) {
      return this
    }this.scaleX = f;
    this.scaleMatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setScaleY = function(f) {
    if(this.ScaleY == f) {
      return this
    }this.scaleY = f;
    this.scaleMatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setScaleZ = function(f) {
    if(this.ScaleZ == f) {
      return this
    }this.scaleZ = f;
    this.scaleMatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setScale = function(f, g, m) {
    if(!g) {
      m = g = f
    }this.scaleX = f;
    this.scaleY = g;
    this.scaleZ = m;
    this.scaleMatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDScaleX = function(f) {
    if(this.dScaleX == f) {
      return this
    }this.dScaleX = f;
    this.scaleMatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDScaleY = function(f) {
    if(this.dScaleY == f) {
      return this
    }this.dScaleY = f;
    this.scaleMatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDScaleZ = function(f) {
    if(this.dScaleZ == f) {
      return this
    }this.dScaleZ = f;
    this.scaleMatrix = this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.setDScale = function(f, g, m) {
    this.dScaleX = f;
    this.dScaleY = g;
    this.dScaleZ = m;
    this.scaleMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.getLocX = function() {
    return this.locX
  };
  e.Placeable.prototype.getLocY = function() {
    return this.locY
  };
  e.Placeable.prototype.getLocZ = function() {
    return this.locZ
  };
  e.Placeable.prototype.getDLocX = function() {
    return this.dLocX
  };
  e.Placeable.prototype.getDLocY = function() {
    return this.dLocY
  };
  e.Placeable.prototype.getDLocZ = function() {
    return this.dLocZ
  };
  e.Placeable.prototype.getQuatX = function() {
    return this.quatX
  };
  e.Placeable.prototype.getQuatY = function() {
    return this.quatY
  };
  e.Placeable.prototype.getQuatZ = function() {
    return this.quatZ
  };
  e.Placeable.prototype.getQuatW = function() {
    return this.quatW
  };
  e.Placeable.prototype.getRotX = function() {
    return this.rotX
  };
  e.Placeable.prototype.getRotY = function() {
    return this.rotY
  };
  e.Placeable.prototype.getRotZ = function() {
    return this.rotZ
  };
  e.Placeable.prototype.getDRotX = function() {
    return this.dRotX
  };
  e.Placeable.prototype.getDRotY = function() {
    return this.dRotY
  };
  e.Placeable.prototype.getDRotZ = function() {
    return this.dRotZ
  };
  e.Placeable.prototype.getScaleX = function() {
    return this.scaleX
  };
  e.Placeable.prototype.getScaleY = function() {
    return this.scaleY
  };
  e.Placeable.prototype.getScaleZ = function() {
    return this.scaleZ
  };
  e.Placeable.prototype.getDScaleX = function() {
    return this.dScaleX
  };
  e.Placeable.prototype.getDScaleY = function() {
    return this.dScaleY
  };
  e.Placeable.prototype.getDScaleZ = function() {
    return this.dScaleZ
  };
  e.Placeable.prototype.getPosition = function() {
    var f = {};
    f.x = parseFloat(this.locX) + parseFloat(this.dLocX);
    f.y = parseFloat(this.locY) + parseFloat(this.dLocY);
    f.z = parseFloat(this.locZ) + parseFloat(this.dLocZ);
    return f
  };
  e.Placeable.prototype.getRotation = function() {
    var f = {};
    if(this.mode == e.P_EULER) {
      f.x = parseFloat(this.rotX) + parseFloat(this.dRotX);
      f.y = parseFloat(this.rotY) + parseFloat(this.dRotY);
      f.z = parseFloat(this.rotZ) + parseFloat(this.dRotZ)
    }if(this.mode == e.P_QUAT) {
      f.x = parseFloat(this.quatX);
      f.y = parseFloat(this.quatY);
      f.z = parseFloat(this.quatZ);
      f.w = parseFloat(this.quatW)
    }return f
  };
  e.Placeable.prototype.getScale = function() {
    var f = {};
    f.x = parseFloat(this.scaleX) + parseFloat(this.dScaleX);
    f.y = parseFloat(this.scaleY) + parseFloat(this.dScaleY);
    f.z = parseFloat(this.scaleZ) + parseFloat(this.dScaleZ);
    return f
  };
  e.Placeable.prototype.getScaleMatrix = function() {
    if(!this.scaleMatrix) {
      this.scaleMatrix = e.scaleMatrix(parseFloat(this.scaleX) + parseFloat(this.dScaleX), parseFloat(this.scaleY) + parseFloat(this.dScaleY), parseFloat(this.scaleZ) + parseFloat(this.dScaleZ))
    }return this.scaleMatrix
  };
  e.Placeable.prototype.getTranslateMatrix = function() {
    if(!this.translateMatrix) {
      this.translateMatrix = e.translateMatrix(parseFloat(this.locX) + parseFloat(this.dLocX), parseFloat(this.locY) + parseFloat(this.dLocY), parseFloat(this.locZ) + parseFloat(this.dLocZ))
    }return this.translateMatrix
  };
  e.Placeable.prototype.getLocalMatrix = function() {
    this.getModelMatrix();
    return this.localMatrix
  };
  e.Placeable.prototype.setStaticMatrix = function(f) {
    this.staticMatrix = f;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.clearStaticMatrix = function() {
    this.staticMatrix = null;
    this.updateMatrix();
    return this
  };
  e.Placeable.prototype.updateMatrix = function() {
    this.matrix = null;
    if(this.children) {
      for(var f = 0;f < this.children.length;f++) {
        this.children[f].updateMatrix()
      }
    }
  };
  e.Placeable.prototype.getModelMatrix = function() {
    if(!this.matrix) {
      this.transinvmatrix = this.transmatrix = this.invmatrix = null;
      if(this.staticMatrix) {
        var f = this.staticMatrix;
        this.localMatrix = this.staticMatrix
      }else {
        f = this.getTranslateMatrix();
        var g = this.getScaleMatrix();
        this.localMatrix = f = e.mulMat4(f, e.mulMat4(this.getRotMatrix(), g))
      }if(this.parent) {
        f = e.mulMat4(this.parent.getModelMatrix(), f)
      }this.matrix = f
    }return this.matrix
  };
  e.Placeable.prototype.getInverseModelMatrix = function() {
    this.matrix || this.getModelMatrix();
    if(!this.invmatrix) {
      this.invmatrix = e.transposeMat4(this.matrix)
    }return this.invmatrix
  };
  e.Placeable.prototype.getTransposeModelMatrix = function() {
    this.matrix || this.getModelMatrix();
    if(!this.transmatrix) {
      this.transmatrix = e.transposeMat4(this.matrix)
    }return this.transmatrix
  };
  e.Placeable.prototype.getTransposeInverseModelMatrix = function() {
    this.matrix || this.getModelMatrix();
    if(!this.transinvmatrix) {
      this.invtransmatrix = e.transposeMat4(this.getInverseModelMatrix())
    }return this.transinvmatrix
  };
  e.Animatable = function() {
  };
  e.augment(e.Events, e.Animatable);
  e.Animatable.prototype.animationStart = null;
  e.Animatable.prototype.animation = null;
  e.Animatable.prototype.blendStart = 0;
  e.Animatable.prototype.blendTime = 0;
  e.Animatable.prototype.lastFrame = null;
  e.Animatable.prototype.frameRate = 30;
  e.Animatable.prototype.loop = e.TRUE;
  e.Animatable.prototype.paused = e.FALSE;
  e.Animatable.prototype.pausedTime = null;
  e.Animatable.prototype.blendFunction = e.LINEAR_BLEND;
  e.Animatable.prototype.blendTo = function(f, g, m) {
    if(!m) {
      m = e.LINEAR_BLEND
    }var p = new e.AnimationVector, r, s;
    for(prop in f) {
      r = new e.AnimationCurve;
      r.setChannel(prop);
      s = new e.LinearPoint;
      s.setX(1);
      s.setY(f[prop]);
      r.addPoint(s);
      p.addAnimationCurve(r)
    }this.setBlendFunction(m);
    this.setAnimation(p, g);
    return this
  };
  e.Animatable.prototype.setBlendFunction = function(f) {
    this.blendFunction = f;
    return this
  };
  e.Animatable.prototype.getBlendFunction = function() {
    return this.blendFunction
  };
  e.Animatable.prototype.setName = function(f) {
    this.name = f;
    return this
  };
  e.Animatable.prototype.getName = function() {
    return this.name
  };
  e.Animatable.prototype.getFrameNumber = function(f) {
    if(!this.startFrame) {
      this.startFrame = this.animation.startFrame
    }if(!this.animFrames) {
      this.animFrames = this.animation.frames
    }f || (f = parseInt((new Date).getTime()));
    if(this.animFrames > 1) {
      if(this.loop) {
        f = (parseFloat(f) - parseFloat(this.animationStart)) / 1E3 * this.frameRate % (this.animFrames - 1) + 1 + this.startFrame
      }else {
        f = (parseFloat(f) - parseFloat(this.animationStart)) / 1E3 * this.frameRate + 1 + this.startFrame;
        if(f >= this.animFrames) {
          f = this.animFrames
        }
      }
    }else {
      f = 1
    }return Math.round(f)
  };
  e.Animatable.prototype.setStartFrame = function(f, g, m) {
    this.loop = m;
    var p = parseInt((new Date).getTime());
    g || (g = 0);
    if(g > 0) {
      if(this.animation) {
        this.blendInitValues = this.getInitialValues(this.animation, p);
        this.blendTime = g
      }
    }this.animationStart = p;
    this.lastFrame = null;
    this.animFinished = false;
    this.startFrame = f;
    if(this.children) {
      for(p = 0;p < this.children.length;p++) {
        this.children[p].setStartFrame && this.children[p].setStartFrame(f, g, m)
      }
    }return this
  };
  e.Animatable.prototype.setFrames = function(f) {
    this.animFrames = f;
    if(this.children) {
      for(var g = 0;g < this.children.length;g++) {
        this.children[g].setFrames && this.children[g].setFrames(f)
      }
    }return this
  };
  e.Animatable.prototype.getInitialValues = function(f, g) {
    var m = {};
    if(this.animation) {
      this.lastFrame = null;
      this.animate(g, true)
    }for(var p in f.curves) {
      if(this["get" + p]) {
        m[p] = this["get" + p]()
      }
    }return m
  };
  e.Animatable.prototype.animate = function(f, g) {
    if(!this.paused && this.animation) {
      f || (f = parseInt((new Date).getTime()));
      var m = this.getFrameNumber(f);
      if(!this.animation.animationCache) {
        this.animation.animationCache = {}
      }if(m != this.lastFrame || this.blendTime != 0) {
        this.lastFrame = m;
        if(this.blendTime == 0) {
          if(!this.animation.animationCache[m] || g) {
            this.animation.animationCache[m] = [];
            if(this.animation.curves.LocX && this.animation.curves.LocY && this.animation.curves.LocZ && this.animation.curves.ScaleX && this.animation.curves.ScaleY && this.animation.curves.ScaleZ && this.animation.curves.QuatX && this.animation.curves.QuatY && this.animation.curves.QuatZ && this.animation.curves.QuatW) {
              for(property in this.animation.curves) {
                if(this["set" + property]) {
                  var p = this.animation.curves[property].getValue(parseFloat(m));
                  switch(property) {
                    case "QuatX":
                    ;
                    case "QuatY":
                    ;
                    case "QuatZ":
                    ;
                    case "QuatW":
                    ;
                    case "LocX":
                    ;
                    case "LocY":
                    ;
                    case "LocZ":
                    ;
                    case "ScaleX":
                    ;
                    case "ScaleY":
                    ;
                    case "ScaleZ":
                      break;
                    default:
                      this.animation.animationCache[m].push({property:property, value:p});
                      break
                  }
                  this["set" + property](p)
                }
              }this.animation.animationCache[m].push({property:"StaticMatrix", value:this.getLocalMatrix()})
            }else {
              for(property in this.animation.curves) {
                if(this["set" + property]) {
                  p = this.animation.curves[property].getValue(parseFloat(m));
                  switch(property) {
                    case "QuatX":
                    ;
                    case "QuatY":
                    ;
                    case "QuatZ":
                    ;
                    case "QuatW":
                    ;
                    case "RotX":
                    ;
                    case "RotY":
                    ;
                    case "RotZ":
                      var r = true;
                      break;
                    default:
                      this.animation.animationCache[m].push({property:property, value:p});
                      break
                  }
                  this["set" + property](p)
                }
              }if(r) {
                p = this.getRotMatrix();
                this.animation.animationCache[m].push({property:"RotMatrix", value:p})
              }
            }
          }else {
            p = this.animation.animationCache[m];
            for(r = 0;r < p.length;r++) {
              this["set" + p[r].property] && this["set" + p[r].property](p[r].value)
            }
          }
        }else {
          p = f - this.animationStart;
          if(p < this.blendTime) {
            r = p / this.blendTime;
            r = this.blendFunction(r);
            for(property in this.animation.curves) {
              if(this["set" + property]) {
                p = this.animation.curves[property].getValue(parseFloat(m));
                p = p * r + this.blendInitValues[property] * (1 - r);
                this["set" + property](p)
              }
            }
          }else {
            this.blendTime = 0
          }
        }
      }
    }if(this.children) {
      for(r = 0;r < this.children.length;r++) {
        this.children[r].animate && this.children[r].animate(f, g)
      }
    }if(this.animation && !this.animFinished && this.blendTime == 0 && this.animation.frames == m && !g) {
      this.animFinished = true;
      this.fireEvent("animFinished", {})
    }
  };
  e.Animatable.prototype.setAnimation = function(f, g, m) {
    if(m == null) {
      m = parseInt((new Date).getTime())
    }g || (g = 0);
    if(g > 0) {
      this.blendInitValues = this.getInitialValues(f, m);
      this.blendTime = g
    }this.startFrame = this.animFrames = null;
    this.animationStart = m;
    this.lastFrame = null;
    this.animation = f;
    this.animFinished = false;
    return this
  };
  e.Animatable.prototype.getAnimation = function() {
    return this.animation
  };
  e.Animatable.prototype.setFrameRate = function(f) {
    this.frameRate = f;
    return this
  };
  e.Animatable.prototype.getFrameRate = function() {
    return this.frameRate
  };
  e.Animatable.prototype.setLoop = function(f) {
    this.loop = f;
    return this
  };
  e.Animatable.prototype.getLoop = function() {
    return this.loop
  };
  e.Animatable.prototype.isLooping = e.Animatable.prototype.getLoop;
  e.Animatable.prototype.setPaused = function(f) {
    if(f) {
      this.pauseTime = parseInt((new Date).getTime())
    }else {
      this.animationStart += parseInt((new Date).getTime()) - this.pauseTime
    }this.paused = f;
    return this
  };
  e.Animatable.prototype.getPaused = function() {
    return this.paused
  };
  e.Animatable.prototype.togglePaused = function() {
    this.setPaused(!this.getPaused());
    return this.paused
  };
  j();
  e.BezTriple = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.QuickNotation, e.BezTriple);
  e.augment(e.JSONLoader, e.BezTriple);
  e.BezTriple.prototype.className = "BezTriple";
  e.BezTriple.prototype.setX1 = function(f) {
    this.x1 = parseFloat(f);
    return this
  };
  e.BezTriple.prototype.setY1 = function(f) {
    this.y1 = parseFloat(f);
    return this
  };
  e.BezTriple.prototype.setX2 = function(f) {
    this.x = parseFloat(f);
    return this
  };
  e.BezTriple.prototype.setY2 = function(f) {
    this.y = parseFloat(f);
    return this
  };
  e.BezTriple.prototype.setX3 = function(f) {
    this.x3 = parseFloat(f);
    return this
  };
  e.BezTriple.prototype.setY3 = function(f) {
    this.y3 = parseFloat(f);
    return this
  };
  e.LinearPoint = function() {
  };
  e.augment(e.QuickNotation, e.LinearPoint);
  e.augment(e.JSONLoader, e.LinearPoint);
  e.LinearPoint.prototype.className = "LinearPoint";
  e.LinearPoint.prototype.x = 0;
  e.LinearPoint.prototype.y = 0;
  e.LinearPoint.prototype.setX = function(f) {
    this.x = parseFloat(f);
    return this
  };
  e.LinearPoint.prototype.setY = function(f) {
    this.y = parseFloat(f);
    return this
  };
  e.StepPoint = function(f, g) {
    this.x = parseFloat(f);
    this.y = g
  };
  e.AnimationCurve = function(f) {
    e.Assets.registerAsset(this, f);
    this.keyFrames = [];
    this.solutions = {};
    this.caches = {}
  };
  e.augment(e.QuickNotation, e.AnimationCurve);
  e.augment(e.JSONLoader, e.AnimationCurve);
  e.AnimationCurve.prototype.className = "AnimationCurve";
  e.AnimationCurve.prototype.keyFrames = null;
  e.AnimationCurve.prototype.addPoint = function(f) {
    this.keyFrames.push(f);
    return this.keyFrames.length - 1
  };
  e.AnimationCurve.prototype.addStepPoint = e.AnimationCurve.prototype.addPoint;
  e.AnimationCurve.prototype.addLinearPoint = e.AnimationCurve.prototype.addPoint;
  e.AnimationCurve.prototype.addBezTriple = e.AnimationCurve.prototype.addPoint;
  e.AnimationCurve.prototype.coord = function(f, g) {
    return{x:f, y:g}
  };
  e.AnimationCurve.prototype.setChannel = function(f) {
    this.channel = f
  };
  e.AnimationCurve.prototype.getValue = function(f) {
    if(this.keyFrames.length == 0) {
      return 0
    }if(this.caches[f]) {
      return this.caches[f]
    }var g, m, p, r;
    if(f < this.keyFrames[0].x) {
      return this.keyFrames[0].y
    }for(var s = 0;s < this.keyFrames.length;s++) {
      if(this.keyFrames[s].x == f) {
        return this.keyFrames[s].y
      }if(this.keyFrames[s].x <= f && (g == undefined || this.keyFrames[s].x > this.keyFrames[g].x)) {
        p = g;
        g = s
      }else {
        if(this.keyFrames[s].x <= f && (p == undefined || this.keyFrames[s].x > this.keyFrames[p].x)) {
          p = s
        }
      }if(this.keyFrames[s].x > f && (m == undefined || this.keyFrames[s].x <= this.keyFrames[m].x)) {
        r = m;
        m = s
      }else {
        if(this.keyFrames[s].x > f && (r == undefined || this.keyFrames[s].x <= this.keyFrames[r].x)) {
          r = s
        }
      }
    }if(g == undefined) {
      g = m;
      m = r
    }if(m == undefined) {
      m = g;
      g = p
    }if(this.keyFrames[g] instanceof e.BezTriple && this.keyFrames[m] instanceof e.BezTriple) {
      p = this.coord(this.keyFrames[g].x, this.keyFrames[g].y);
      r = this.coord(this.keyFrames[g].x3, this.keyFrames[g].y3);
      g = this.coord(this.keyFrames[m].x1, this.keyFrames[m].y1);
      m = this.coord(this.keyFrames[m].x, this.keyFrames[m].y);
      return this.atX(f, p, r, g, m).y
    }if(this.keyFrames[g] instanceof e.LinearPoint && this.keyFrames[m] instanceof e.BezTriple) {
      p = this.coord(this.keyFrames[g].x, this.keyFrames[g].y);
      r = this.coord(this.keyFrames[m].x1, this.keyFrames[m].y1);
      g = this.coord(this.keyFrames[m].x1, this.keyFrames[m].y1);
      m = this.coord(this.keyFrames[m].x, this.keyFrames[m].y);
      return this.atX(f, p, r, g, m).y
    }if(this.keyFrames[g] instanceof e.BezTriple && this.keyFrames[m] instanceof e.LinearPoint) {
      p = this.coord(this.keyFrames[g].x, this.keyFrames[g].y);
      r = this.coord(this.keyFrames[g].x3, this.keyFrames[g].y3);
      g = this.coord(this.keyFrames[g].x3, this.keyFrames[g].y3);
      m = this.coord(this.keyFrames[m].x, this.keyFrames[m].y);
      return this.atX(f, p, r, g, m).y
    }if(this.keyFrames[g] instanceof e.LinearPoint && this.keyFrames[m] instanceof e.LinearPoint) {
      return(f - this.keyFrames[g].x) * (this.keyFrames[m].y - this.keyFrames[g].y) / (this.keyFrames[m].x - this.keyFrames[g].x) + this.keyFrames[g].y
    }if(this.keyFrames[g] instanceof e.StepPoint) {
      return this.keyFrames[g].y
    }if(!this.keyFrames.preStartKey) {
      this.keyFrames.preStartKey = this.keyFrames[0].y
    }this.caches[f] = this.keyFrames.preStartKey;
    return this.caches[f]
  };
  e.AnimationCurve.prototype.B1 = function(f) {
    return f * f * f
  };
  e.AnimationCurve.prototype.B2 = function(f) {
    return 3 * f * f * (1 - f)
  };
  e.AnimationCurve.prototype.B3 = function(f) {
    return 3 * f * (1 - f) * (1 - f)
  };
  e.AnimationCurve.prototype.B4 = function(f) {
    return(1 - f) * (1 - f) * (1 - f)
  };
  e.AnimationCurve.prototype.getBezier = function(f, g, m, p, r) {
    var s = {};
    s.x = g.x * this.B1(f) + m.x * this.B2(f) + p.x * this.B3(f) + r.x * this.B4(f);
    s.y = g.y * this.B1(f) + m.y * this.B2(f) + p.y * this.B3(f) + r.y * this.B4(f);
    return s
  };
  e.AnimationCurve.prototype.Quad3Solve = function(f, g, m, p) {
    ref = f + "-" + g + "--" + m + "-" + p;
    if(this.solutions[ref]) {
      return this.solutions[ref]
    }else {
      g /= f;
      m /= f;
      p /= f;
      f = (3 * m - g * g) / 9;
      m = -(27 * p) + g * (9 * m - 2 * g * g);
      m /= 54;
      g = g / 3;
      discrim = f * f * f + m * m;
      result = [];
      if(discrim > 0) {
        f = m + Math.sqrt(discrim);
        f = f < 0 ? -Math.pow(-f, 1 / 3) : Math.pow(f, 1 / 3);
        m = m - Math.sqrt(discrim);
        m = m < 0 ? -Math.pow(-m, 1 / 3) : Math.pow(m, 1 / 3);
        result[0] = -g + f + m;
        g += (f + m) / 2;
        result[1] = result[2] = -g
      }else {
        if(discrim == 0) {
          f = m < 0 ? -Math.pow(-m, 1 / 3) : Math.pow(m, 1 / 3);
          result[1] = -g + 2 * f;
          result[1] = result[2] = -(f + g)
        }else {
          f = -f;
          m = Math.acos(m / Math.sqrt(1));
          f = 2 * Math.sqrt(f);
          result[0] = -g + f * Math.cos(m / 3);
          result[1] = -g + f * Math.cos((m + 2 * Math.PI) / 3);
          result[2] = -g + f * Math.cos((m + 4 * Math.PI) / 3)
        }
      }f = false;
      if(result[0] >= 0 && result[0] <= 1) {
        f = result[0]
      }if(!f && result[1] >= 0 && result[1] <= 1) {
        f = result[1]
      }if(!f && result[2] >= 0 && result[2] <= 1) {
        f = result[2]
      }return this.solutions[ref] = f
    }
  };
  e.AnimationCurve.prototype.atX = function(f, g, m, p, r) {
    a = g.x - m.x * 3 + p.x * 3 - r.x;
    b = m.x * 3 - p.x * 6 + r.x * 3;
    c = p.x * 3 - r.x * 3;
    d = r.x - f;
    return this.getBezier(this.Quad3Solve(a, b, c, d), g, m, p, r)
  };
  e.AnimationVector = function(f) {
    e.Assets.registerAsset(this, f);
    this.curves = []
  };
  e.augment(e.QuickNotation, e.AnimationVector);
  e.augment(e.JSONLoader, e.AnimationVector);
  e.AnimationVector.prototype.curves = [];
  e.AnimationVector.prototype.frames = 250;
  e.AnimationVector.prototype.startFrame = 0;
  e.AnimationVector.prototype.addAnimationCurve = function(f) {
    this.curves[f.channel] = f;
    return this
  };
  e.AnimationVector.prototype.removeAnimationCurve = function(f) {
    delete this.curves[f]
  };
  e.AnimationVector.prototype.setFrames = function(f) {
    this.frames = f;
    return this
  };
  e.AnimationVector.prototype.getFrames = function() {
    return this.frames
  };
  e.AnimationVector.prototype.setStartFrame = function(f) {
    this.startFrame = f;
    return this
  };
  e.AnimationVector.prototype.getStartFrame = function() {
    return this.startFrame
  };
  e.G_NODE = 1;
  e.G_ROOT = 2;
  e.Group = function(f) {
    e.Assets.registerAsset(this, f);
    this.children = []
  };
  e.augment(e.Placeable, e.Group);
  e.augment(e.Animatable, e.Group);
  e.augment(e.QuickNotation, e.Group);
  e.augment(e.JSONLoader, e.Group);
  e.Group.prototype.children = null;
  e.Group.prototype.className = "Group";
  e.Group.prototype.type = e.G_NODE;
  e.Group.prototype.setAction = function(f, g, m) {
    f.start(g, m, this.getNames());
    return this
  };
  e.Group.prototype.getNames = function(f) {
    f || (f = {});
    var g = this.getName();
    if(g != "") {
      f[g] = this
    }for(g = 0;g < this.children.length;g++) {
      this.children[g].getNames && this.children[g].getNames(f)
    }return f
  };
  e.Group.prototype.getBoundingVolume = function(f, g) {
    f = f ? this.getLocalMatrix() : this.getModelMatrix();
    if(g) {
      f = e.mulMat4(g, f)
    }for(var m = null, p = 0;p < this.children.length;p++) {
      if(this.children[p].getBoundingVolume) {
        if(m) {
          m.addBoundingVolume(this.children[p].getBoundingVolume(true, f))
        }else {
          m = this.children[p].getBoundingVolume(true, f)
        }
      }
    }m || (m = new e.BoundingVolume(0, 0, 0, 0, 0, 0));
    if(!g) {
      this.boundingVolume = m.clone()
    }return m
  };
  e.Group.prototype.getObjects = function(f) {
    this.lookAt && this.Lookat(this.lookAt);
    this.animation && this.animate();
    f || (f = []);
    for(var g = 0;g < this.children.length;g++) {
      if(this.children[g].className == "Object" || this.children[g].className == "Text" || this.children[g].toRender) {
        this.children[g].renderFirst ? f.unshift(this.children[g]) : f.push(this.children[g])
      }else {
        this.children[g].getObjects && this.children[g].getObjects(f)
      }
    }return f
  };
  e.Group.prototype.getLights = function(f) {
    f || (f = []);
    for(var g = 0;g < this.children.length;g++) {
      if(this.children[g].className == "Light") {
        f.push(this.children[g])
      }else {
        this.children[g].getLights && this.children[g].getLights(f)
      }
    }return f
  };
  e.Group.prototype.addChild = function(f) {
    f.parent && f.parent.removeChild(f);
    f.matrix = null;
    f.parent = this;
    this.children.push(f);
    return this
  };
  e.Group.prototype.addObject = e.Group.prototype.addChild;
  e.Group.prototype.addObjectInstance = e.Group.prototype.addChild;
  e.Group.prototype.addGroup = e.Group.prototype.addChild;
  e.Group.prototype.addText = e.Group.prototype.addChild;
  e.Group.prototype.addSkeleton = e.Group.prototype.addChild;
  e.Group.prototype.addLight = e.Group.prototype.addChild;
  e.Group.prototype.addCamera = e.Group.prototype.addChild;
  e.Group.prototype.addWavefront = e.Group.prototype.addChild;
  e.Group.prototype.removeChild = function(f) {
    for(var g = 0;g < this.children.length;g++) {
      if(this.children[g] == f) {
        this.children.splice(g, 1);
        this.scene && this.scene["remove" + f.className] && this.scene["remove" + f.className](f);
        break
      }
    }
  };
  e.Group.prototype.getChildren = function() {
    return this.children
  };
  e.Group.prototype.GLInit = function(f) {
    this.gl = f;
    for(var g = 0;g < this.children.length;g++) {
      this.children[g].GLInit && this.children[g].GLInit(f)
    }
  };
  e.Group.prototype.getPickable = function() {
    return this.pickable
  };
  e.Group.prototype.setPickable = function(f) {
    for(var g = 0;g < this.children.length;g++) {
      this.children[g].setPickable && this.children[g].setPickable(f)
    }this.pickable = f;
    return this
  };
  e.ActionChannel = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.QuickNotation, e.ActionChannel);
  e.augment(e.JSONLoader, e.ActionChannel);
  e.ActionChannel.prototype.setTarget = function(f) {
    this.target = f
  };
  e.ActionChannel.prototype.setAnimation = function(f) {
    this.animation = f
  };
  e.ActionChannel.prototype.getTarget = function() {
    return this.target
  };
  e.ActionChannel.prototype.getAnimation = function() {
    return this.animation
  };
  e.Action = function(f) {
    e.Assets.registerAsset(this, f);
    this.channels = []
  };
  e.augment(e.QuickNotation, e.Action);
  e.augment(e.JSONLoader, e.Action);
  e.augment(e.Events, e.Action);
  e.Action.prototype.start = function(f, g, m) {
    g || (g = false);
    f || (f = 0);
    var p = this.channels, r = (new Date).getTime();
    this.animFinished = false;
    for(var s = 0;s < p.length;s++) {
      var A = p[s].getAnimation(), v = this, B = p[s].getTarget();
      if(typeof B == "string") {
        if(m && m[B]) {
          B = m[B]
        }
      }var C = {};
      C.finishEvent = function() {
        B.removeEventListener("animFinished", C.finishEvent);
        if(!v.animFinished && B.animation == A) {
          v.fireEvent("animFinished", {});
          v.animFinished = true
        }
      };
      B.addEventListener("animFinished", C.finishEvent);
      B.setAnimation(A, f, r);
      B.setLoop(g)
    }
  };
  e.Action.prototype.setStartFrame = function(f) {
    for(var g = 0;g < this.channels.length;g++) {
      this.channels[g].getAnimation().setStartFrame(f)
    }return this
  };
  e.Action.prototype.setFrames = function(f) {
    for(var g = 0;g < this.channels.length;g++) {
      this.channels[g].getAnimation().setFrames(f)
    }return this
  };
  e.Action.prototype.addActionChannel = function(f) {
    this.channels.push(f);
    return this
  };
  e.Action.prototype.removeActionChannel = function() {
    for(var f = 0;f < this.channels.length;f++) {
      if(this.channels[f] == channels) {
        this.channels.splice(f, 1);
        break
      }
    }
  };
  e.Text = function(f) {
    e.Assets.registerAsset(this, f);
    this.canvas = document.createElement("canvas");
    this.color = {r:1, g:1, b:1}
  };
  e.augment(e.Placeable, e.Text);
  e.augment(e.Animatable, e.Text);
  e.augment(e.QuickNotation, e.Text);
  e.augment(e.JSONLoader, e.Text);
  e.Text.prototype.className = "Text";
  e.Text.prototype.zTrans = true;
  e.Text.prototype.canvas = null;
  e.Text.prototype.aspect = 1;
  e.Text.prototype.color = null;
  e.Text.prototype.text = "";
  e.Text.prototype.font = "Times";
  e.Text.prototype.size = 100;
  e.Text.prototype.pickType = e.TEXT_TEXTPICK;
  e.Text.prototype.getPickType = function() {
    return this.pickType
  };
  e.Text.prototype.setPickType = function(f) {
    this.pickType = f;
    return this
  };
  e.Text.prototype.getFont = function() {
    return this.size
  };
  e.Text.prototype.setFont = function(f) {
    this.font = f;
    this.gl && this.updateCanvas(this.gl);
    return this
  };
  e.Text.prototype.getSize = function() {
    return this.size
  };
  e.Text.prototype.setSize = function(f) {
    this.size = f;
    this.gl && this.updateCanvas(this.gl);
    return this
  };
  e.Text.prototype.getText = function() {
    return this.text
  };
  e.Text.prototype.setText = function(f) {
    this.text = f;
    this.gl && this.updateCanvas(this.gl);
    return this
  };
  e.Text.prototype.setColor = function(f) {
    f = e.colorParse(f);
    this.color = {r:f.r, g:f.g, b:f.b};
    return this
  };
  e.Text.prototype.setColorR = function(f) {
    this.color.r = f;
    return this
  };
  e.Text.prototype.setColorG = function(f) {
    this.color.g = f;
    return this
  };
  e.Text.prototype.setColorB = function(f) {
    this.color.b = f;
    return this
  };
  e.Text.prototype.getColor = function() {
    return this.color
  };
  e.Text.prototype.setZtransparent = function(f) {
    this.zTrans = f;
    return this
  };
  e.Text.prototype.isZtransparent = function() {
    return this.zTrans
  };
  e.Text.prototype.GLGenerateShader = function(f) {
    this.GLShaderProgram && f.deleteProgram(this.GLShaderProgram);
    var g = "";
    g += "attribute vec3 position;\n";
    g += "attribute vec2 uvcoord;\n";
    g += "varying vec2 texcoord;\n";
    g += "uniform mat4 Matrix;\n";
    g += "uniform mat4 PMatrix;\n";
    g += "varying vec4 pos;\n";
    g += "void main(void){\n";
    g += "texcoord=uvcoord;\n";
    g += "pos = Matrix * vec4(position,1.0);\n";
    g += "gl_Position = PMatrix * pos;\n";
    g += "}\n";
    var m = "#ifdef GL_ES\nprecision highp float;\n#endif\n";
    m += "uniform sampler2D TEXTURE;\n";
    m += "varying vec2 texcoord;\n";
    m += "varying vec4 pos;\n";
    m += "uniform float far;\n";
    m += "uniform int picktype;\n";
    m += "uniform vec3 pickcolor;\n";
    m += "uniform vec3 color;\n";
    m += "void main(void){\n";
    m += "float alpha=texture2D(TEXTURE,texcoord).a;\n";
    m = m + "if(picktype==" + e.TEXT_BOXPICK + "){gl_FragColor = vec4(pickcolor,1.0);}";
    m = m + "else if(picktype==" + e.TEXT_TEXTPICK + "){gl_FragColor = vec4(pickcolor,alpha);}";
    m += "else{gl_FragColor = vec4(color.rgb*alpha,alpha);};\n";
    m += "}\n";
    this.GLFragmentShader = f.createShader(f.FRAGMENT_SHADER);
    this.GLVertexShader = f.createShader(f.VERTEX_SHADER);
    f.shaderSource(this.GLFragmentShader, m);
    f.compileShader(this.GLFragmentShader);
    if(f.getShaderParameter(this.GLFragmentShader, f.COMPILE_STATUS)) {
      f.shaderSource(this.GLVertexShader, g);
      f.compileShader(this.GLVertexShader);
      if(f.getShaderParameter(this.GLVertexShader, f.COMPILE_STATUS)) {
        this.GLShaderProgram = f.createProgram();
        f.attachShader(this.GLShaderProgram, this.GLVertexShader);
        f.attachShader(this.GLShaderProgram, this.GLFragmentShader);
        f.linkProgram(this.GLShaderProgram)
      }else {
        e.error(f.getShaderInfoLog(this.GLVertexShader))
      }
    }else {
      e.error(f.getShaderInfoLog(this.GLFragmentShader))
    }
  };
  e.Text.prototype.GLInit = function(f) {
    this.gl = f;
    this.createPlane(f);
    this.GLGenerateShader(f);
    this.glTexture = f.createTexture();
    this.updateCanvas(f)
  };
  e.Text.prototype.updateCanvas = function(f) {
    var g = this.canvas;
    g.width = 1;
    g.height = this.size * 1.2;
    var m = g.getContext("2d");
    m.font = this.size + "px " + this.font;
    g.width = m.measureText(this.text).width;
    g.height = this.size * 1.2;
    m = g.getContext("2d");
    m.textBaseline = "top";
    m.font = this.size + "px " + this.font;
    this.aspect = g.width / g.height;
    m.fillText(this.text, 0, 0);
    f.bindTexture(f.TEXTURE_2D, this.glTexture);
    try {
      f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, g)
    }catch(p) {
      f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, g, null)
    }f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MAG_FILTER, f.LINEAR);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MIN_FILTER, f.LINEAR);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_WRAP_S, f.CLAMP_TO_EDGE);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_WRAP_T, f.CLAMP_TO_EDGE);
    f.bindTexture(f.TEXTURE_2D, null)
  };
  e.Text.prototype.GLRender = function(f, g, m) {
    this.gl || this.GLInit(f);
    if(g == e.RENDER_DEFAULT || g == e.RENDER_PICK) {
      this.lookAt && this.Lookat(this.lookAt);
      if(f.program != this.GLShaderProgram) {
        f.useProgram(this.GLShaderProgram);
        f.program = this.GLShaderProgram
      }var p;
      for(p = 0;p < 8;p++) {
        f.disableVertexAttribArray(p)
      }p = e.getAttribLocation(f, this.GLShaderProgram, "position");
      f.bindBuffer(f.ARRAY_BUFFER, this.posBuffer);
      f.enableVertexAttribArray(p);
      f.vertexAttribPointer(p, this.posBuffer.itemSize, f.FLOAT, false, 0, 0);
      p = e.getAttribLocation(f, this.GLShaderProgram, "uvcoord");
      f.bindBuffer(f.ARRAY_BUFFER, this.uvBuffer);
      f.enableVertexAttribArray(p);
      f.vertexAttribPointer(p, this.uvBuffer.itemSize, f.FLOAT, false, 0, 0);
      f.activeTexture(f.TEXTURE0);
      f.bindTexture(f.TEXTURE_2D, this.glTexture);
      e.setUniform(f, "1i", e.getUniformLocation(f, this.GLShaderProgram, "TEXTURE"), 0);
      m || (m = 0);
      p = m >> 16 & 255;
      var r = m >> 8 & 255;
      m = m & 255;
      e.setUniform3(f, "3f", e.getUniformLocation(f, this.GLShaderProgram, "pickcolor"), m / 255, r / 255, p / 255);
      g == e.RENDER_PICK ? e.setUniform(f, "1i", e.getUniformLocation(f, this.GLShaderProgram, "picktype"), this.pickType) : e.setUniform(f, "1i", e.getUniformLocation(f, this.GLShaderProgram, "picktype"), 0);
      if(!this.GLShaderProgram.glarrays) {
        this.GLShaderProgram.glarrays = {}
      }g = this.size / 100;
      g = e.mulMat4(f.scene.camera.getViewMatrix(), e.mulMat4(this.getModelMatrix(), e.scaleMatrix(this.aspect * g, g, g)));
      m = e.getUniformLocation(f, this.GLShaderProgram, "Matrix");
      if(this.GLShaderProgram.glarrays.mMatrix) {
        e.mat4gl(g, this.GLShaderProgram.glarrays.mMatrix)
      }else {
        this.GLShaderProgram.glarrays.mMatrix = new Float32Array(g)
      }e.setUniformMatrix(f, "Matrix4fv", m, true, this.GLShaderProgram.glarrays.mMatrix);
      m = e.getUniformLocation(f, this.GLShaderProgram, "PMatrix");
      if(this.GLShaderProgram.glarrays.pMatrix) {
        e.mat4gl(f.scene.camera.getProjectionMatrix(), this.GLShaderProgram.glarrays.pMatrix)
      }else {
        this.GLShaderProgram.glarrays.pMatrix = new Float32Array(f.scene.camera.getProjectionMatrix())
      }e.setUniformMatrix(f, "Matrix4fv", m, true, this.GLShaderProgram.glarrays.pMatrix);
      g = e.getUniformLocation(f, this.GLShaderProgram, "far");
      e.setUniform(f, "1f", g, f.scene.camera.getFar());
      e.setUniform3(f, "3f", e.getUniformLocation(f, this.GLShaderProgram, "color"), this.color.r, this.color.g, this.color.b);
      f.bindBuffer(f.ELEMENT_ARRAY_BUFFER, this.GLfaces);
      f.drawElements(f.TRIANGLES, this.GLfaces.numItems, f.UNSIGNED_SHORT, 0);
      f.scene.lastMaterial = null
    }
  };
  e.Text.prototype.createPlane = function(f) {
    if(!this.posBuffer) {
      this.posBuffer = f.createBuffer()
    }f.bindBuffer(f.ARRAY_BUFFER, this.posBuffer);
    f.bufferData(f.ARRAY_BUFFER, new Float32Array([1, 1, 0, -1, 1, 0, -1, -1, 0, 1, -1, 0]), f.STATIC_DRAW);
    this.posBuffer.itemSize = 3;
    this.posBuffer.numItems = 4;
    if(!this.uvBuffer) {
      this.uvBuffer = f.createBuffer()
    }f.bindBuffer(f.ARRAY_BUFFER, this.uvBuffer);
    f.bufferData(f.ARRAY_BUFFER, new Float32Array([0, 0, 1, 0, 1, 1, 0, 1]), f.STATIC_DRAW);
    this.uvBuffer.itemSize = 2;
    this.uvBuffer.numItems = 4;
    if(!this.GLfaces) {
      this.GLfaces = f.createBuffer()
    }f.bindBuffer(f.ELEMENT_ARRAY_BUFFER, this.GLfaces);
    f.bufferData(f.ELEMENT_ARRAY_BUFFER, new Uint16Array([0, 1, 2, 2, 3, 0]), f.STATIC_DRAW);
    this.GLfaces.itemSize = 1;
    this.GLfaces.numItems = 6
  };
  e.ObjectLod = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.QuickNotation, e.ObjectLod);
  e.augment(e.JSONLoader, e.ObjectLod);
  e.ObjectLod.prototype.mesh = null;
  e.ObjectLod.prototype.className = "ObjectLod";
  e.ObjectLod.prototype.material = null;
  e.ObjectLod.prototype.program = null;
  e.ObjectLod.prototype.GLShaderProgramPick = null;
  e.ObjectLod.prototype.GLShaderProgramShadow = null;
  e.ObjectLod.prototype.GLShaderProgram = null;
  e.ObjectLod.prototype.pixelSize = 0;
  e.ObjectLod.prototype.setMesh = function(f) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }this.mesh && this.mesh.removeEventListener("shaderupdate", this.meshupdated);
    var g = this;
    this.meshupdated = function() {
      g.GLShaderProgram = null
    };
    f.addEventListener("shaderupdate", this.meshupdated);
    this.GLShaderProgram = null;
    this.mesh = f;
    return this
  };
  e.ObjectLod.prototype.getMesh = function() {
    return this.mesh
  };
  e.ObjectLod.prototype.setMaterial = function(f) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }this.material && this.material.removeEventListener("shaderupdate", this.materialupdated);
    var g = this;
    this.materialupdated = function() {
      g.GLShaderProgram = null
    };
    f.addEventListener("shaderupdate", this.materialupdated);
    this.GLShaderProgram = null;
    this.material = f;
    return this
  };
  e.ObjectLod.prototype.getMaterial = function() {
    return this.material
  };
  e.ObjectLod.prototype.getPixelSize = function() {
    return this.pixelSize
  };
  e.ObjectLod.prototype.setPixelSize = function(f) {
    this.pixelSize = parseFloat(f)
  };
  e.MultiMaterial = function(f) {
    e.Assets.registerAsset(this, f);
    this.lods = [new e.ObjectLod]
  };
  e.augment(e.QuickNotation, e.MultiMaterial);
  e.augment(e.JSONLoader, e.MultiMaterial);
  e.MultiMaterial.prototype.className = "MultiMaterial";
  e.MultiMaterial.prototype.setMesh = function(f) {
    this.lods[0].setMesh(f);
    return this
  };
  e.MultiMaterial.prototype.getMesh = function() {
    return this.lods[0].getMesh()
  };
  e.MultiMaterial.prototype.setMaterial = function(f) {
    this.lods[0].setMaterial(f);
    return this
  };
  e.MultiMaterial.prototype.getMaterial = function() {
    return this.lods[0].getMaterial()
  };
  e.MultiMaterial.prototype.getLOD = function(f) {
    var g = 0, m = this.lods[0];
    if(this.lods.length > 1) {
      for(var p = 1;p < this.lods.length;p++) {
        var r = this.lods[p].pixelSize;
        if(r > g && r < f && this.lods[p].mesh && this.lods[p].mesh.loaded) {
          g = r;
          m = this.lods[p]
        }
      }
    }return m
  };
  e.MultiMaterial.prototype.addObjectLod = function(f) {
    this.lods.push(f);
    return this
  };
  e.MultiMaterial.prototype.removeObjectLod = function(f) {
    (f = this.lods.indexOf(f)) && this.lods.splice(f, 1);
    return this
  };
  e.ObjectInstance = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.Placeable, e.ObjectInstance);
  e.augment(e.Animatable, e.ObjectInstance);
  e.augment(e.QuickNotation, e.ObjectInstance);
  e.augment(e.JSONLoader, e.ObjectInstance);
  e.ObjectInstance.prototype.parentObject = null;
  e.ObjectInstance.prototype.className = "ObjectInstance";
  e.ObjectInstance.prototype.setObject = function(f) {
    this.parentObject && this.parentObject.removeInstance(this);
    this.parentObject = f;
    f.addInstance(this);
    return this
  };
  e.ObjectInstance.prototype.getObject = function() {
    return this.parentObject
  };
  e.Object = function(f) {
    e.Assets.registerAsset(this, f);
    this.multimaterials = [];
    this.instances = [];
    this.renderCaches = []
  };
  e.augment(e.Placeable, e.Object);
  e.augment(e.Animatable, e.Object);
  e.augment(e.QuickNotation, e.Object);
  e.augment(e.JSONLoader, e.Object);
  e.Object.prototype.className = "Object";
  e.Object.prototype.mesh = null;
  e.Object.prototype.skeleton = null;
  e.Object.prototype.scene = null;
  e.Object.prototype.transformMatrix = e.identMatrix();
  e.Object.prototype.material = null;
  e.Object.prototype.gl = null;
  e.Object.prototype.multimaterials = null;
  e.Object.prototype.instances = null;
  e.Object.prototype.zTrans = false;
  e.Object.prototype.renderCaches = null;
  e.Object.prototype.id = "";
  e.Object.prototype.pickable = true;
  e.Object.prototype.drawType = e.DRAW_TRIS;
  e.Object.prototype.pointSize = 1;
  e.Object.prototype.cull = false;
  var q = [];
  q.push("#ifdef GL_ES\nprecision highp float;\n#endif\n");
  q.push("void main(void)\n");
  q.push("{\n");
  q.push("vec4 rgba=fract((gl_FragCoord.z/gl_FragCoord.w)/100.0 * vec4(16777216.0, 65536.0, 256.0, 1.0));\n");
  q.push("gl_FragColor=rgba-rgba.rrgb*vec4(0.0,0.00390625,0.00390625,0.00390625);\n");
  q.push("}\n");
  e.Object.prototype.shfragStr = q.join("");
  q = [];
  q.push("#ifdef GL_ES\nprecision highp float;\n#endif\n");
  q.push("varying vec3 n;\n");
  q.push("void main(void)\n");
  q.push("{\n");
  q.push("gl_FragColor=vec4(n,1.0);\n");
  q.push("}\n");
  e.Object.prototype.nfragStr = q.join("");
  q = [];
  q.push("#ifdef GL_ES\nprecision highp float;\n#endif\n");
  q.push("uniform float far;\n");
  q.push("uniform vec3 pickcolor;\n");
  q.push("varying vec3 n;\n");
  q.push("varying vec4 UVCoord;\n");
  q.push("void main(void)\n");
  q.push("{\n");
  q.push("float Xcoord = gl_FragCoord.x+0.5;\n");
  q.push("if(Xcoord>0.0) gl_FragColor = vec4(pickcolor,1.0);\n");
  q.push("if(Xcoord>1.0) gl_FragColor = vec4(n,1.0);\n");
  q.push("if(Xcoord>2.0){");
  q.push("vec3 rgb=fract((gl_FragCoord.z/gl_FragCoord.w) * vec3(65536.0, 256.0, 1.0));\n");
  q.push("gl_FragColor=vec4(rgb-rgb.rrg*vec3(0.0,0.00390625,0.00390625),1.0);\n");
  q.push("}");
  q.push("if(Xcoord>3.0){");
  q.push("vec3 rgb=fract(UVCoord.x * vec3(65536.0, 256.0, 1.0));\n");
  q.push("gl_FragColor=vec4(rgb-rgb.rrg*vec3(0.0,0.00390625,0.00390625),1.0);\n");
  q.push("}");
  q.push("if(Xcoord>4.0){");
  q.push("vec3 rgb=fract(UVCoord.y * vec3(65536.0, 256.0, 1.0));\n");
  q.push("gl_FragColor=vec4(rgb-rgb.rrg*vec3(0.0,0.00390625,0.00390625),1.0);\n");
  q.push("}");
  q.push("}\n");
  e.Object.prototype.pkfragStr = q.join("");
  e.Object.prototype.getPickable = function() {
    return this.pickable
  };
  e.Object.prototype.setPickable = function(f) {
    this.pickable = f;
    return this
  };
  e.Object.prototype.getCull = function() {
    return this.cull
  };
  e.Object.prototype.setCull = function(f) {
    this.cull = f;
    return this
  };
  e.Object.prototype.getDrawType = function() {
    return this.drawType
  };
  e.Object.prototype.setDrawType = function(f) {
    this.drawType = f;
    return this
  };
  e.Object.prototype.getPointSize = function() {
    return this.pointSize
  };
  e.Object.prototype.setPointSize = function(f) {
    this.pointSize = parseFloat(f);
    return this
  };
  e.Object.prototype.getSkeleton = function() {
    return this.skeleton
  };
  e.Object.prototype.setSkeleton = function(f) {
    this.skeleton = f;
    this.bones = null;
    return this
  };
  e.Object.prototype.getBoundingVolume = function(f, g) {
    f || (f = 0);
    if(!this.boundingVolume) {
      this.boundingVolume = []
    }if(!this.boundmatrix) {
      this.boundmatrix = []
    }var m;
    m = f ? this.getLocalMatrix() : this.getModelMatrix();
    if(g) {
      m = e.mulMat4(g, m)
    }var p = this.getModelMatrix();
    if(p != this.boundmatrix[f] || !this.boundingVolume[f]) {
      for(var r = this.multimaterials, s, A = 0;A < r.length;A++) {
        if(r[A].lods[0].mesh) {
          if(s) {
            s.addBoundingVolume(r[A].lods[0].mesh.getBoundingVolume(m))
          }else {
            s = r[A].lods[0].mesh.getBoundingVolume(m).clone()
          }
        }
      }s || (s = new e.BoundingVolume(0, 0, 0, 0, 0, 0));
      if(g) {
        return s
      }else {
        this.boundingVolume[f] = s
      }
    }this.boundmatrix[f] = p;
    return this.boundingVolume[f]
  };
  e.Object.prototype.setZtransparent = function(f) {
    this.zTrans = f;
    return this
  };
  e.Object.prototype.isZtransparent = function() {
    return this.zTrans
  };
  e.Object.prototype.addInstance = function(f) {
    this.instances.push(f);
    return this
  };
  e.Object.prototype.removeInstance = function(f) {
    for(var g = 0;g < this.instances;g++) {
      this.instance == f && this.instances.splice(g)
    }
  };
  e.Object.prototype.setMaterial = function(f, g) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }g || (g = 0);
    this.multimaterials[g] || (this.multimaterials[g] = new e.MultiMaterial);
    if(this.multimaterials[g].getMaterial() != f) {
      this.multimaterials[g].setMaterial(f);
      this.updateProgram()
    }return this
  };
  e.Object.prototype.getMaterial = function(f) {
    f || (f = 0);
    return this.multimaterials[f] ? this.multimaterials[f].getMaterial() : false
  };
  e.Object.prototype.setMesh = function(f, g) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }g || (g = 0);
    this.multimaterials[g] || this.multimaterials.push(new e.MultiMaterial);
    this.multimaterials[g].setMesh(f);
    this.boundingVolume = null;
    return this
  };
  e.Object.prototype.getMesh = function(f) {
    f || (f = 0);
    return this.multimaterials[f] ? this.multimaterials[f].getMesh() : false
  };
  e.Object.prototype.GLInit = function(f) {
    this.gl = f
  };
  e.Object.prototype.GLDestory = function() {
  };
  e.Object.prototype.updateProgram = function() {
    for(var f = 0;f < this.multimaterials.length;f++) {
      this.multimaterials[f].GLShaderProgram = null
    }
  };
  e.Object.prototype.addMultiMaterial = function(f) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }this.multimaterials.push(f);
    this.boundingVolume = null;
    return this
  };
  e.Object.prototype.getMultiMaterials = function() {
    return this.multimaterials
  };
  e.Object.prototype.GLGenerateShader = function(f) {
    var g = joints1 = joints2 = false, m = f.lights, p = [], r = false;
    this.mesh.normals || this.mesh.calcNormals();
    for(var s = 0;s < this.mesh.buffers.length;s++) {
      if(this.mesh.buffers[s].name == "tangent") {
        r = true
      }this.mesh.buffers[s].size > 1 ? p.push("attribute vec" + this.mesh.buffers[s].size + " " + this.mesh.buffers[s].name + ";\n") : p.push("attribute float " + this.mesh.buffers[s].name + ";\n");
      if(this.mesh.buffers[s].name == "UV") {
        g = true
      }if(this.mesh.buffers[s].name == "joints1") {
        joints1 = this.mesh.buffers[s]
      }if(this.mesh.buffers[s].name == "joints2") {
        joints2 = this.mesh.buffers[s]
      }
    }p.push("uniform mat4 worldView;\n");
    p.push("uniform mat4 projection;\n");
    p.push("uniform mat4 view;\n");
    p.push("uniform mat4 worldInverseTranspose;\n");
    p.push("uniform mat4 envMat;\n");
    for(s = 0;s < m.length;s++) {
      p.push("uniform vec3 lightpos" + s + ";\n");
      p.push("uniform vec3 lightdir" + s + ";\n");
      p.push("uniform mat4 lightmat" + s + ";\n");
      p.push("varying vec4 spotcoord" + s + ";\n")
    }p.push("varying vec3 eyevec;\n");
    for(s = 0;s < m.length;s++) {
      p.push("varying vec3 lightvec" + s + ";\n");
      p.push("varying vec3 tlightvec" + s + ";\n");
      p.push("varying float lightdist" + s + ";\n")
    }this.mesh.joints && this.mesh.joints.length > 0 && p.push("uniform vec4 jointMat[" + 3 * this.mesh.joints.length + "];\n");
    this.material && p.push(this.material.getVertexVarying(p));
    p.push("varying vec3 n;\n");
    p.push("varying vec3 b;\n");
    p.push("varying vec3 t;\n");
    p.push("varying vec4 UVCoord;\n");
    p.push("varying vec3 OBJCoord;\n");
    p.push("varying vec3 tang;\n");
    p.push("varying vec3 teyevec;\n");
    p.push("void main(void)\n");
    p.push("{\n");
    g && p.push("UVCoord=UV;\n");
    p.push("OBJCoord = position;\n");
    p.push("vec4 pos = vec4(0.0, 0.0, 0.0, 1.0);\n");
    p.push("vec4 norm = vec4(0.0, 0.0, 0.0, 1.0);\n");
    p.push("vec4 tang4 = vec4(0.0, 0.0, 0.0, 1.0);\n");
    if(joints1) {
      if(joints1.size == 1) {
        p.push("pos += vec4(dot(jointMat[int(3.0*joints1)],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints1+1.0)],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints1+2.0)],vec4(position,1.0)),1.0)*weights1;\n");
        p.push("norm += vec4(dot(jointMat[int(3.0*joints1)].xyz,normal),\n               dot(jointMat[int(3.0*joints1+1.0)].xyz,normal),\n               dot(jointMat[int(3.0*joints1+2.0)].xyz,normal),1.0)*weights1;\n");
        r && p.push("tang4 += vec4(dot(jointMat[int(3.0*joints1)].xyz,tangent),\n               dot(jointMat[int(3.0*joints1+1.0)].xyz,tangent),\n               dot(jointMat[int(3.0*joints1+2.0)].xyz,tangent),1.0)*weights1;\n")
      }else {
        for(s = 0;s < joints1.size;s++) {
          p.push("pos += vec4(dot(jointMat[int(3.0*joints1[" + s + "])],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints1[" + s + "]+1.0)],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints1[" + s + "]+2.0)],vec4(position,1.0)),1.0)*weights1[" + s + "];\n");
          p.push("norm += vec4(dot(jointMat[int(3.0*joints1[" + s + "])].xyz,normal),\n               dot(jointMat[int(3.0*joints1[" + s + "]+1.0)].xyz,normal),\n               dot(jointMat[int(3.0*joints1[" + s + "]+2.0)].xyz,normal),1.0)*weights1[" + s + "];\n");
          r && p.push("tang4 += vec4(dot(jointMat[int(3.0*joints1[" + s + "])].xyz,tangent),\n               dot(jointMat[int(3.0*joints1[" + s + "]+1.0)].xyz,tangent),\n               dot(jointMat[int(3.0*joints1[" + s + "]+2.0)].xyz,tangent),1.0)*weights1[" + s + "];\n")
        }
      }if(joints2) {
        if(joints2.size == 1) {
          p.push("pos += vec4(dot(jointMat[int(3.0*joints2)],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints2+1.0)],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints2+2.0)],vec4(position,1.0)),1.0)*weights2;\n");
          p.push("norm += vec4(dot(jointMat[int(3.0*joints2)].xyz,normal),\n               dot(jointMat[int(3.0*joints2+1.0)].xyz,normal),\n               dot(jointMat[int(3.0*joints2+2.0)].xyz,normal),1.0)*weights2;\n");
          r && p.push("tang4 += vec4(dot(jointMat[int(3.0*joints2)].xyz,tangent),\n               dot(jointMat[int(3.0*joints2+1.0)].xyz,tangent),\n               dot(jointMat[int(3.0*joints2+2.0)].xyz,tangent),1.0)*weights2;\n")
        }else {
          for(s = 0;s < joints2.size;s++) {
            p.push("pos += vec4(dot(jointMat[int(3.0*joints2[" + s + "])],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints2[" + s + "]+1.0)],vec4(position,1.0)),\n              dot(jointMat[int(3.0*joints2[" + s + "]+2.0)],vec4(position,1.0)),1.0)*weights2[" + s + "];\n");
            p.push("norm += vec4(dot(jointMat[int(3.0*joints2[" + s + "])].xyz,normal),\n               dot(jointMat[int(3.0*joints2[" + s + "]+1.0)].xyz,normal),\n               dot(jointMat[int(3.0*joints2[" + s + "]+2.0)].xyz,normal),1.0)*weights2[" + s + "];\n");
            r && p.push("tang4 += vec4(dot(jointMat[int(3.0*joints2[" + s + "])].xyz,tangent),\n               dot(jointMat[int(3.0*joints2[" + s + "]+1.0)].xyz,tangent),\n               dot(jointMat[int(3.0*joints2[" + s + "]+2.0)].xyz,tangent),1.0)*weights2[" + s + "];\n")
          }
        }
      }for(s = 0;s < m.length;s++) {
        p.push("spotcoord" + s + "=lightmat" + s + "*vec4(pos.xyz,1.0);\n")
      }p.push("pos = worldView * vec4(pos.xyz, 1.0);\n");
      p.push("norm = worldInverseTranspose * vec4(norm.xyz, 1.0);\n");
      r && p.push("tang = (worldInverseTranspose*vec4(tang4.xyz,1.0)).xyz;\n")
    }else {
      for(s = 0;s < m.length;s++) {
        p.push("spotcoord" + s + "=lightmat" + s + "*vec4(position,1.0);\n")
      }p.push("pos = worldView * vec4(position, 1.0);\n");
      p.push("norm = worldInverseTranspose * vec4(normal, 1.0);\n");
      r && p.push("tang = (worldInverseTranspose*vec4(tangent,1.0)).xyz;\n")
    }p.push("gl_Position = projection * pos;\n");
    p.push("gl_PointSize=" + this.pointSize.toFixed(5) + ";\n");
    p.push("eyevec = -pos.xyz;\n");
    p.push("t = normalize(tang);");
    p.push("n = normalize(norm.rgb);");
    p.push("b = normalize(cross(n,t));");
    if(r) {
      p.push("teyevec.x = dot(eyevec, t);");
      p.push("teyevec.y = dot(eyevec, b);");
      p.push("teyevec.z = dot(eyevec, n);")
    }else {
      p.push("teyevec = eyevec;")
    }for(s = 0;s < m.length;s++) {
      m[s].getType() == e.L_DIR ? p.push("vec3 tmplightvec" + s + " = -lightdir" + s + ";\n") : p.push("vec3 tmplightvec" + s + " = -(lightpos" + s + "-pos.xyz);\n");
      if(r) {
        p.push("tlightvec" + s + ".x = dot(tmplightvec" + s + ", t);");
        p.push("tlightvec" + s + ".y = dot(tmplightvec" + s + ", b);");
        p.push("tlightvec" + s + ".z = dot(tmplightvec" + s + ", n);")
      }else {
        p.push("tlightvec" + s + " = tmplightvec" + s + ";")
      }p.push("lightvec" + s + " = tmplightvec" + s + ";");
      p.push("lightdist" + s + " = length(lightpos" + s + ".xyz-pos.xyz);\n")
    }this.material && p.push(this.material.getLayerCoords(p));
    p.push("}\n");
    p = p.join("");
    if(this.material) {
      g = this.material.getFragmentShader(m)
    }else {
      g = [];
      g.push("void main(void)\n");
      g.push("{\n");
      g.push("gl_FragColor = vec4(1.0,1.0,1.0,1.0);\n");
      g.push("}\n");
      g = g.join("")
    }this.GLFragmentShaderNormal = e.getGLShader(f, f.FRAGMENT_SHADER, this.nfragStr);
    this.GLFragmentShaderShadow = e.getGLShader(f, f.FRAGMENT_SHADER, this.shfragStr);
    this.GLFragmentShaderPick = e.getGLShader(f, f.FRAGMENT_SHADER, this.pkfragStr);
    this.GLFragmentShader = e.getGLShader(f, f.FRAGMENT_SHADER, g);
    this.GLVertexShader = e.getGLShader(f, f.VERTEX_SHADER, p);
    this.GLShaderProgramPick = e.getGLProgram(f, this.GLVertexShader, this.GLFragmentShaderPick);
    this.GLShaderProgramShadow = e.getGLProgram(f, this.GLVertexShader, this.GLFragmentShaderShadow);
    this.GLShaderProgramNormal = e.getGLProgram(f, this.GLVertexShader, this.GLFragmentShaderNormal);
    this.GLShaderProgram = e.getGLProgram(f, this.GLVertexShader, this.GLFragmentShader)
  };
  e.Object.prototype.createShaders = function(f) {
    if(this.gl) {
      this.mesh = f.mesh;
      this.material = f.material;
      this.GLGenerateShader(this.gl);
      f.GLShaderProgramPick = this.GLShaderProgramPick;
      f.GLShaderProgramShadow = this.GLShaderProgramShadow;
      f.GLShaderProgram = this.GLShaderProgram
    }
  };
  e.Object.prototype.GLUniforms = function(f, g, m) {
    var p;
    switch(g) {
      case e.RENDER_DEFAULT:
        p = this.GLShaderProgram;
        break;
      case e.RENDER_SHADOW:
        p = this.GLShaderProgramShadow;
        break;
      case e.RENDER_NORMAL:
        p = this.GLShaderProgramNormal;
        break;
      case e.RENDER_PICK:
        p = this.GLShaderProgramPick;
        var r = m >> 16 & 255, s = m >> 8 & 255;
        m = m & 255;
        e.setUniform3(f, "3f", e.getUniformLocation(f, p, "pickcolor"), m / 255, s / 255, r / 255);
        break
    }
    if(!p.caches) {
      p.caches = {}
    }if(!p.glarrays) {
      p.glarrays = {}
    }m = p.caches;
    r = p.glarrays;
    s = f.scene;
    var A = s.camera;
    if(m.far != A.far) {
      e.setUniform(f, "1i", e.getUniformLocation(f, p, "far"), A.far);
      m.far = A.far
    }if(g == e.RENDER_DEFAULT) {
      if(m.ambientColor != s.ambientColor) {
        var v = s.ambientColor;
        e.setUniform3(f, "3f", e.getUniformLocation(f, p, "amb"), v.r, v.g, v.b);
        m.ambientColor = v
      }if(m.fogFar != s.fogFar) {
        e.setUniform(f, "1f", e.getUniformLocation(f, p, "fogfar"), s.fogFar);
        m.fogFar = s.fogFar
      }if(m.fogNear != s.fogNear) {
        e.setUniform(f, "1f", e.getUniformLocation(f, p, "fognear"), s.fogNear);
        m.fogNear = s.fogNear
      }if(m.fogType != s.fogType) {
        e.setUniform(f, "1i", e.getUniformLocation(f, p, "fogtype"), s.fogType);
        m.fogType = s.fogType
      }if(m.fogType != s.fogcolor) {
        e.setUniform3(f, "3f", e.getUniformLocation(f, p, "fogcolor"), s.fogColor.r, s.fogColor.g, s.fogColor.b);
        m.fogcolor = s.fogcolor
      }
    }v = A.getViewMatrix();
    s = this.getModelMatrix();
    if(!m.mvMatrix) {
      m.mvMatrix = {cameraMatrix:null, modelMatrix:null}
    }var B = m.mvMatrix;
    try {
      this.caches.mvMatrix = e.mulMat4(v, s);
      mvMatrix = this.caches.mvMatrix;
      if(this.mesh.joints) {
        mvMatrix = v
      }var C = e.getUniformLocation(f, p, "worldView");
      if(r.mvMatrix) {
        e.mat4gl(e.transposeMat4(mvMatrix), r.mvMatrixT)
      }else {
        r.mvMatrixT = new Float32Array(mvMatrix)
      }r.mvMatrix = mvMatrix;
      e.setUniformMatrix(f, "Matrix4fv", C, false, p.glarrays.mvMatrixT);
      var E = e.getUniformLocation(f, p, "envMat");
      if(E) {
        if(!this.caches.envMat) {
          var H = e.inverseMat4(mvMatrix);
          H[3] = 0;
          H[7] = 0;
          H[11] = 0;
          this.caches.envMat = H
        }H = this.caches.envMat;
        if(p.glarrays.envMat) {
          e.mat4gl(e.transposeMat4(H), r.envMatT)
        }else {
          r.envMatT = new Float32Array(e.transposeMat4(H))
        }r.envMat = H;
        e.setUniformMatrix(f, "Matrix4fv", E, false, r.envMatT)
      }if(!this.caches.normalMatrix) {
        var J = e.inverseMat4(mvMatrix);
        this.caches.normalMatrix = J
      }J = this.caches.normalMatrix;
      var M = e.getUniformLocation(f, p, "worldInverseTranspose");
      if(r.normalMatrix) {
        e.mat4gl(J, r.normalMatrix)
      }else {
        r.normalMatrix = new Float32Array(J)
      }e.setUniformMatrix(f, "Matrix4fv", M, false, r.normalMatrix);
      var K = e.getUniformLocation(f, p, "view");
      if(r.cameraMatrix) {
        e.mat4gl(e.transposeMat4(v), r.cameraMatrixT)
      }else {
        r.cameraMatrixT = new Float32Array(e.transposeMat4(v))
      }r.cameraMatrix = v;
      e.setUniformMatrix(f, "Matrix4fv", K, false, r.cameraMatrixT);
      B.camerMatrix = v;
      B.modelMatrix = s
    }catch(N) {
      e.error("Serious error in setting of camera cache" + N)
    }C = e.getUniformLocation(f, p, "projection");
    if(r.pMatrix) {
      e.mat4gl(e.transposeMat4(A.getProjectionMatrix()), r.pMatrixT)
    }else {
      r.pMatrixT = new Float32Array(e.transposeMat4(A.getProjectionMatrix()))
    }r.pMatrix = A.getProjectionMatrix();
    e.setUniformMatrix(f, "Matrix4fv", C, false, r.pMatrixT);
    if(g == e.RENDER_DEFAULT) {
      var Q = f.lights;
      if(!m.lights) {
        m.lights = []
      }if(!r.lights) {
        r.lights = []
      }if(!this.caches.lights) {
        this.caches.lights = []
      }J = m.lights;
      for(C = 0;C < Q.length;C++) {
        J[C] || (J[C] = {modelMatrix:null, cameraMatrix:null});
        if(J[C].modelMatrix != s || J[C].cameraMatrix != v) {
          this.caches.lights[C] || (this.caches.lights[C] = {});
          if(!this.caches.lights[C].pos) {
            this.caches.lights[C].pos = e.mulMat4Vec4(e.mulMat4(v, Q[C].getModelMatrix()), [0, 0, 0, 1])
          }E = this.caches.lights[C].pos;
          e.setUniform3(f, "3f", e.getUniformLocation(f, p, "lightpos" + C), E[0], E[1], E[2]);
          if(!this.caches.lights[C].lpos) {
            this.caches.lights[C].lpos = e.mulMat4Vec4(e.mulMat4(v, Q[C].getModelMatrix()), [0, 0, 1, 1])
          }H = this.caches.lights[C].lpos;
          e.setUniform3(f, "3f", e.getUniformLocation(f, p, "lightdir" + C), H[0] - E[0], H[1] - E[1], H[2] - E[2]);
          if(Q[C].s_cache) {
            try {
              var R = e.mulMat4(Q[C].s_cache.smatrix, s);
              if(r.lights[C]) {
                e.mat4gl(R, r.lights[C])
              }else {
                r.lights[C] = new Float32Array(R)
              }e.setUniformMatrix(f, "Matrix4fv", e.getUniformLocation(f, p, "lightmat" + C), true, r.lights[C]);
              J[C].modelMatrix = s;
              J[C].cameraMatrix = v
            }catch(D) {
            }
          }else {
            J[C].modelMatrix = s;
            J[C].cameraMatrix = v
          }
        }
      }
    }if(this.mesh.joints) {
      if(!m.joints) {
        m.joints = []
      }if(!r.joints) {
        r.joints = []
      }if(!r.jointsT) {
        r.jointsT = []
      }if(!r.jointsinv) {
        r.jointsinv = []
      }if(!r.jointsCombined || r.jointsCombined.length != this.mesh.joints.length * 12) {
        r.jointsCombined = new Float32Array(this.mesh.joints.length * 12)
      }R = m.joints;
      e.identMatrix();
      for(C = 0;C < this.mesh.joints.length;C++) {
        R[C] || (R[C] = {modelMatrix:null, invBind:null});
        if(typeof this.mesh.joints[C] == "string") {
          if(!this.bones) {
            this.bones = this.skeleton.getNames()
          }if(this.bones) {
            try {
              s = this.bones[this.mesh.joints[C]].getModelMatrix()
            }catch(G) {
              this.bones.errorMessagePrinted || e.error("skeleton/joints problem");
              this.bones.errorMessagePrinted = true
            }
          }
        }else {
          s = this.mesh.joints[C].getModelMatrix()
        }m = this.mesh.invBind[C];
        if(R[C].modelMatrix != s || R[C].invBind != m) {
          E = e.mulMat4(s, m);
          if(r.joints[C]) {
            e.mat4gl(e.transposeMat4(E), r.jointsT[C])
          }else {
            r.jointsT[C] = new Float32Array(e.transposeMat4(E))
          }r.joints[C] = E;
          if(r.jointsinv[C]) {
            e.mat4gl(e.inverseMat4(E), r.jointsinv[C])
          }else {
            r.jointsinv[C] = new Float32Array(e.inverseMat4(E))
          }E = r.jointsT[C];
          H = r.jointsCombined;
          H[C * 12] = E[0];
          H[C * 12 + 1] = E[4];
          H[C * 12 + 2] = E[8];
          H[C * 12 + 3] = E[12];
          H[C * 12 + 4] = E[1];
          H[C * 12 + 5] = E[5];
          H[C * 12 + 6] = E[9];
          H[C * 12 + 7] = E[13];
          H[C * 12 + 8] = E[2];
          H[C * 12 + 9] = E[6];
          H[C * 12 + 10] = E[10];
          H[C * 12 + 11] = E[14];
          R[C].modelMatrix = s;
          R[C].invBind = m
        }
      }try {
        f.uniform4fv(e.getUniformLocation(f, p, "jointMat"), r.jointsCombined)
      }catch(I) {
        e.error("Unsupported: fast matrix upload");
        for(C = 0;C < this.mesh.joints.length;C++) {
          E = r.jointsT[C];
          e.setUniform4(f, "4f", e.getUniformLocation(f, p, "jointMat[" + C * 3 + "]"), E[0], E[4], E[8], E[12]);
          e.setUniform4(f, "4f", e.getUniformLocation(f, p, "jointMat[" + (C * 3 + 1) + "]"), E[1], E[5], E[9], E[13]);
          e.setUniform4(f, "4f", e.getUniformLocation(f, p, "jointMat[" + (C * 3 + 2) + "]"), E[2], E[6], E[10], E[14])
        }
      }
    }this.material && g == e.RENDER_DEFAULT && f.scene.lastMaterial != this.material && this.material.textureUniforms(f, p, Q, this);
    f.scene.lastMaterial = this.material
  };
  e.Object.prototype.GLRender = function(f, g, m, p) {
    if(f) {
      this.gl || this.GLInit(f);
      this.lookAt && this.Lookat(this.lookAt);
      g == e.RENDER_DEFAULT && this.animation && this.animate();
      this.renderCaches[g] || (this.renderCaches[g] = {});
      var r = f.scene.camera.getViewMatrix(), s = this.getModelMatrix();
      if(this.renderCaches[g].camerMatrix != r || this.renderCaches[g].modelMatrix != s) {
        this.renderCaches[g] = {};
        this.renderCaches[g].camerMatrix = r;
        this.renderCaches[g].modelMatrix = s
      }this.caches = this.renderCaches[g];
      for(var A = 0;A < this.instances.length;A++) {
        var v = this.instances[A];
        if(!v.renderCaches) {
          v.renderCaches = []
        }v.renderCaches[g] || (v.renderCaches[g] = {});
        s = v.getModelMatrix();
        if(v.renderCaches[g].camerMatrix != r || v.renderCaches[g].modelMatrix != s) {
          v.renderCaches[g] = {};
          v.renderCaches[g].camerMatrix = r;
          v.renderCaches[g].modelMatrix = s
        }v.caches = {}
      }var B;
      if(p == undefined) {
        A = 0;
        p = this.multimaterials.length
      }else {
        A = p;
        p = p + 1
      }for(r = A;r < p;r++) {
        if(this.multimaterials[r].lods.length > 1 && !B) {
          B = f.scene.camera.getPosition();
          A = this.getPosition();
          B = e.lengthVec3([B.x - A.x, B.y - A.y, B.z - A.z]);
          B = e.mulMat4Vec4(f.scene.camera.getProjectionMatrix(), [this.getBoundingVolume().getSphereRadius(), 0, -B, 1]);
          B = B[0] / B[3] * f.scene.renderer.canvas.width
        }A = this.multimaterials[r].getLOD(B);
        if(A.mesh && A.mesh.loaded) {
          if(g == e.RENDER_NULL) {
            A.material && A.material.registerPasses(f, this);
            break
          }if(A.GLShaderProgram) {
            this.GLShaderProgramPick = A.GLShaderProgramPick;
            this.GLShaderProgramShadow = A.GLShaderProgramShadow;
            this.GLShaderProgram = A.GLShaderProgram
          }else {
            this.createShaders(A)
          }this.mesh = A.mesh;
          this.material = A.material;
          switch(this.drawType) {
            case e.DRAW_LINES:
              s = f.LINES;
              break;
            case e.DRAW_POINTS:
              s = f.POINTS;
              break;
            case e.DRAW_LINELOOPS:
              s = f.LINE_LOOP;
              break;
            case e.DRAW_LINESTRIPS:
              s = f.LINE_STRIP;
              break;
            default:
              s = f.TRIANGLES;
              break
          }
          switch(g) {
            case e.RENDER_DEFAULT:
              if(f.program != this.GLShaderProgram) {
                f.useProgram(this.GLShaderProgram);
                f.program = this.GLShaderProgram
              }this.mesh.GLAttributes(f, this.GLShaderProgram);
              break;
            case e.RENDER_SHADOW:
              if(f.program != this.GLShaderProgramShadow) {
                f.useProgram(this.GLShaderProgramShadow);
                f.program = this.GLShaderProgramShadow
              }this.mesh.GLAttributes(f, this.GLShaderProgramShadow);
              break;
            case e.RENDER_NORMAL:
              if(f.program != this.GLShaderProgramNormal) {
                f.useProgram(this.GLShaderProgramNormal);
                f.program = this.GLShaderProgramNormal
              }this.mesh.GLAttributes(f, this.GLShaderProgramNormal);
              break;
            case e.RENDER_PICK:
              if(f.program != this.GLShaderProgramPick) {
                f.useProgram(this.GLShaderProgramPick);
                f.program = this.GLShaderProgramPick
              }this.mesh.GLAttributes(f, this.GLShaderProgramPick);
              s = f.TRIANGLES;
              break
          }
          this.GLUniforms(f, g, m);
          switch(this.mesh.windingOrder) {
            case e.Mesh.WINDING_ORDER_UNKNOWN:
              f.disable(f.CULL_FACE);
              break;
            case e.Mesh.WINDING_ORDER_COUNTER:
              f.cullFace(f.FRONT);
            default:
              break
          }
          if(this.mesh.GLfaces) {
            f.bindBuffer(f.ELEMENT_ARRAY_BUFFER, this.mesh.GLfaces);
            f.drawElements(s, this.mesh.GLfaces.numItems, f.UNSIGNED_SHORT, 0)
          }else {
            f.drawArrays(s, 0, this.mesh.positions.length / 3)
          }switch(this.mesh.windingOrder) {
            case e.Mesh.WINDING_ORDER_UNKNOWN:
              f.scene.renderer.cullFaces && f.enable(f.CULL_FACE);
              break;
            case e.Mesh.WINDING_ORDER_COUNTER:
              f.cullFace(f.BACK);
            default:
              break
          }
          v = this.matrix;
          var C = this.caches;
          for(A = 0;A < this.instances.length;A++) {
            this.matrix = this.instances[A].getModelMatrix();
            this.skeleton && this.skeleton.setStaticMatrix(this.matrix);
            this.caches = this.instances[A].caches;
            this.GLUniforms(f, g, m);
            if(this.mesh.GLfaces) {
              f.bindBuffer(f.ELEMENT_ARRAY_BUFFER, this.mesh.GLfaces);
              f.drawElements(s, this.mesh.GLfaces.numItems, f.UNSIGNED_SHORT, 0)
            }else {
              f.drawArrays(s, 0, this.mesh.positions.length / 3)
            }
          }this.matrix = v;
          this.caches = C
        }
      }
    }
  };
  e.Mesh = function(f, g) {
    e.Assets.registerAsset(this, f);
    this.GLbuffers = [];
    this.buffers = [];
    this.UV = [];
    this.boneWeights = [];
    this.setBuffers = [];
    this.faces = {};
    this.windingOrder = g !== undefined ? g : e.Mesh.WINDING_ORDER_CLOCKWISE
  };
  e.Mesh.WINDING_ORDER_UNKNOWN = 2;
  e.Mesh.WINDING_ORDER_CLOCKWISE = 1;
  e.Mesh.WINDING_ORDER_COUNTER = 0;
  e.augment(e.QuickNotation, e.Mesh);
  e.augment(e.JSONLoader, e.Mesh);
  e.augment(e.Events, e.Mesh);
  e.Mesh.prototype.gl = null;
  e.Mesh.prototype.className = "Mesh";
  e.Mesh.prototype.GLbuffers = null;
  e.Mesh.prototype.buffers = null;
  e.Mesh.prototype.setBuffers = null;
  e.Mesh.prototype.GLfaces = null;
  e.Mesh.prototype.faces = null;
  e.Mesh.prototype.UV = null;
  e.Mesh.prototype.joints = null;
  e.Mesh.prototype.invBind = null;
  e.Mesh.prototype.loaded = false;
  e.Mesh.prototype.getBoundingVolume = function(f) {
    if(!this.boundingVolume) {
      for(var g, m, p, r, s, A, v = 0;v < this.buffers.length;v++) {
        if(this.buffers[v].name == "position") {
          var B = this.buffers[v].data;
          if(f) {
            if(B.length >= 3) {
              var C = e.mulMat4Vec3(f, B.slice(0, 3));
              g = m = C[0];
              p = r = C[1];
              s = A = C[2]
            }else {
              g = p = s = m = r = A = 0
            }for(var E = 3;E + 2 < B.length;E += 3) {
              C = e.mulMat4Vec3(f, B.slice(E, E + 3));
              g = Math.min(g, C[0]);
              m = Math.max(m, C[0]);
              p = Math.min(p, C[1]);
              r = Math.max(r, C[1]);
              s = Math.min(s, C[2]);
              A = Math.max(A, C[2])
            }
          }else {
            if(B.length >= 3) {
              g = m = B[0];
              p = r = B[1];
              s = A = B[2]
            }else {
              g = p = s = m = r = A = 0
            }for(E = 3;E + 3 < B.length;v = E + 3) {
              g = Math.min(g, B[v]);
              m = Math.max(m, B[v]);
              p = Math.min(p, B[v + 1]);
              r = Math.max(r, B[v + 1]);
              s = Math.min(s, B[v + 2]);
              A = Math.max(A, B[v + 2])
            }
          }
        }
      }this.boundingVolume = new e.BoundingVolume(g, m, p, r, s, A)
    }return this.boundingVolume
  };
  e.Mesh.prototype.setJoints = function(f) {
    this.joints = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Mesh.prototype.setInvBindMatrix = function(f) {
    this.invBind = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Mesh.prototype.setVertexJoints = function(f, g) {
    g || (g = f.length * 3 / this.positions.length);
    if(g < 5) {
      this.setBuffer("joints1", f, g)
    }else {
      for(var m = [], p = [], r = 0;r < f.length;r++) {
        r % g < 4 ? m.push(f[r]) : p.push(f[r])
      }this.setBuffer("joints1", m, 4);
      this.setBuffer("joints2", p, g - 4)
    }this.fireEvent("shaderupdate", {});
    return this
  };
  e.Mesh.prototype.setVertexWeights = function(f, g) {
    g || (g = f.length * 3 / this.positions.length);
    for(var m = 0;m < f.length;m += parseInt(g)) {
      for(var p = 0, r = 0;r < g;r++) {
        p += parseFloat(f[m + r])
      }for(r = 0;r < g;r++) {
        f[m + r] /= p
      }
    }if(g < 4) {
      this.setBuffer("weights1", f, g)
    }else {
      p = [];
      r = [];
      for(m = 0;m < f.length;m++) {
        m % g < 4 ? p.push(f[m]) : r.push(f[m])
      }this.setBuffer("weights1", p, 4);
      this.setBuffer("weights2", r, g - 4)
    }this.fireEvent("shaderupdate", {});
    return this
  };
  e.Mesh.prototype.clearBuffers = function() {
    this.GLFaces = null;
    delete this.GLFaces;
    for(i in this.buffers) {
      this.buffers[i] = null;
      delete this.buffers[i]
    }this.buffers = [];
    this.loaded = false
  };
  e.Mesh.prototype.setUV = function(f) {
    for(var g = 0, m = 0;m < f.length;m += 2) {
      this.UV[g] = f[m];
      this.UV[g + 1] = f[m + 1];
      this.UV[g + 2] || (this.UV[g + 2] = f[m]);
      this.UV[g + 3] || (this.UV[g + 3] = f[m + 1]);
      g += 4
    }this.setBuffer("UV", this.UV, 4);
    return this
  };
  e.Mesh.prototype.setUV2 = function(f) {
    for(var g = 0, m = 0;m < f.length;m += 2) {
      this.UV[g] || (this.UV[g] = f[m]);
      this.UV[g + 1] || (this.UV[g + 1] = f[m + 1]);
      this.UV[g + 2] = f[m];
      this.UV[g + 3] = f[m + 1];
      g += 4
    }this.setBuffer("UV", this.UV, 4);
    return this
  };
  e.Mesh.prototype.setPositions = function(f) {
    this.loaded = true;
    this.positions = f;
    this.setBuffer("position", f, 3);
    return this
  };
  e.Mesh.prototype.setNormals = function(f) {
    this.normals = f;
    this.setBuffer("normal", f, 3);
    return this
  };
  e.Mesh.prototype.setBuffer = function(f, g, m) {
    for(var p = 0;p < g.length;p++) {
      g[p] = parseFloat(g[p])
    }var r;
    for(p = 0;p < this.buffers.length;p++) {
      if(this.buffers[p].name == f) {
        r = p
      }
    }if(r) {
      this.buffers[r] = {name:f, data:g, size:m, GL:false}
    }else {
      this.buffers.push({name:f, data:g, size:m, GL:false})
    }return this
  };
  e.Mesh.prototype.setFaces = function(f) {
    this.faces = {data:f, GL:false};
    this.normals || this.calcNormals();
    for(f = 0;f < this.buffers.length;f++) {
      if(this.buffers[f].name == "position") {
        var g = this.buffers[f].data
      }if(this.buffers[f].name == "UV") {
        var m = this.buffers[f].data
      }if(this.buffers[f].name == "normal") {
        var p = this.buffers[f].data
      }
    }if(g && m) {
      var r = [], s = {};
      for(f = 0;f < this.faces.data.length;f += 3) {
        var A = [g[parseInt(this.faces.data[f]) * 3], g[parseInt(this.faces.data[f]) * 3 + 1], g[parseInt(this.faces.data[f]) * 3 + 2]], v = [g[parseInt(this.faces.data[f + 1]) * 3], g[parseInt(this.faces.data[f + 1]) * 3 + 1], g[parseInt(this.faces.data[f + 1]) * 3 + 2]], B = [g[parseInt(this.faces.data[f + 2]) * 3], g[parseInt(this.faces.data[f + 2]) * 3 + 1], g[parseInt(this.faces.data[f + 2]) * 3 + 2]], C = [p[parseInt(this.faces.data[f]) * 3], p[parseInt(this.faces.data[f]) * 3 + 1], p[parseInt(this.faces.data[f]) * 
        3 + 2]], E = [p[parseInt(this.faces.data[f + 1]) * 3], p[parseInt(this.faces.data[f + 1]) * 3 + 1], p[parseInt(this.faces.data[f + 1]) * 3 + 2]], H = [p[parseInt(this.faces.data[f + 2]) * 3], p[parseInt(this.faces.data[f + 2]) * 3 + 1], p[parseInt(this.faces.data[f + 2]) * 3 + 2]], J = [v[0] - A[0], v[1] - A[1], v[2] - A[2]], M = [B[0] - A[0], B[1] - A[1], B[2] - A[2]], K = [m[parseInt(this.faces.data[f + 1]) * 4] - m[parseInt(this.faces.data[f]) * 4], m[parseInt(this.faces.data[f + 1]) * 
        4 + 1] - m[parseInt(this.faces.data[f]) * 4 + 1]], N = [m[parseInt(this.faces.data[f + 2]) * 4] - m[parseInt(this.faces.data[f]) * 4], m[parseInt(this.faces.data[f + 2]) * 4 + 1] - m[parseInt(this.faces.data[f]) * 4 + 1]];
        J = e.toUnitVec3([J[0] * N[1] - M[0] * K[1], J[1] * N[1] - M[1] * K[1], J[2] * N[1] - M[2] * K[1]]);
        K = K[1] * N[0] - K[0] * N[1];
        if(K != 0) {
          J = e.toUnitVec3(e.scaleVec3(J, 1 / K))
        }if(s[[A[0], A[1], A[2], C[0], C[1], C[2]].join(",")]) {
          tang = s[[A[0], A[1], A[2], C[0], C[1], C[2]].join(",")];
          tang.vec = e.scaleVec3(e.addVec3(e.scaleVec3(tang.vec, tang.weight), J), 1 / tang.weight);
          tang.weight++
        }else {
          s[[A[0], A[1], A[2], C[0], C[1], C[2]].join(",")] = {vec:J, weight:1}
        }if(s[[v[0], v[1], v[2], E[0], E[1], E[2]].join(",")]) {
          tang = s[[v[0], v[1], v[2], E[0], E[1], E[2]].join(",")];
          tang.vec = e.scaleVec3(e.addVec3(e.scaleVec3(tang.vec, tang.weight), J), 1 / (tang.weight + 1));
          tang.weight++
        }else {
          s[[v[0], v[1], v[2], E[0], E[1], E[2]].join(",")] = {vec:J, weight:1}
        }if(s[[B[0], B[1], B[2], H[0], H[1], H[2]].join(",")]) {
          tang = s[[B[0], B[1], B[2], H[0], H[1], H[2]].join(",")];
          tang.vec = e.scaleVec3(e.addVec3(e.scaleVec3(tang.vec, tang.weight), J), 1 / (tang.weight + 1));
          tang.weight++
        }else {
          s[[B[0], B[1], B[2], H[0], H[1], H[2]].join(",")] = {vec:J, weight:1}
        }
      }for(f = 0;f < g.length / 3;f++) {
        A = [g[f * 3], g[f * 3 + 1], g[f * 3 + 2]];
        C = [p[f * 3], p[f * 3 + 1], p[f * 3 + 2]];
        if(t = s[[A[0], A[1], A[2], C[0], C[1], C[2]].join(",")].vec) {
          r[f * 3] = t[0];
          r[f * 3 + 1] = t[1];
          r[f * 3 + 2] = t[2]
        }
      }this.setBuffer("tangent", r, 3)
    }return this
  };
  e.Mesh.prototype.GLSetFaceBuffer = function(f) {
    if(!this.GLfaces) {
      this.GLfaces = f.createBuffer()
    }f.bindBuffer(f.ELEMENT_ARRAY_BUFFER, this.GLfaces);
    f.bufferData(f.ELEMENT_ARRAY_BUFFER, new Uint16Array(this.faces.data), f.STATIC_DRAW);
    this.GLfaces.itemSize = 1;
    this.GLfaces.numItems = this.faces.data.length
  };
  e.Mesh.prototype.GLSetBuffer = function(f, g, m, p) {
    this.GLbuffers[g] || (this.GLbuffers[g] = f.createBuffer());
    f.bindBuffer(f.ARRAY_BUFFER, this.GLbuffers[g]);
    f.bufferData(f.ARRAY_BUFFER, new Float32Array(m), f.STATIC_DRAW);
    this.GLbuffers[g].itemSize = p;
    this.GLbuffers[g].numItems = m.length / p
  };
  e.Mesh.prototype.calcNormals = function() {
    var f = [], g = this.positions, m = this.faces.data;
    if(!m) {
      m = [];
      for(var p = 0;p < g.length / 3;p++) {
        m[p] = p
      }
    }for(p = 0;p < m.length;p += 3) {
      var r = [g[m[p] * 3], g[m[p] * 3 + 1], g[m[p] * 3 + 2]], s = [g[m[p + 2] * 3], g[m[p + 2] * 3 + 1], g[m[p + 2] * 3 + 2]], A = e.subVec3([g[m[p + 1] * 3], g[m[p + 1] * 3 + 1], g[m[p + 1] * 3 + 2]], r);
      r = e.subVec3(s, r);
      A = e.toUnitVec3(e.crossVec3(A, r));
      if(f[m[p]] == undefined) {
        f[m[p]] = []
      }f[m[p]].push(A);
      if(f[m[p + 1]] == undefined) {
        f[m[p + 1]] = []
      }f[m[p + 1]].push(A);
      if(f[m[p + 2]] == undefined) {
        f[m[p + 2]] = []
      }f[m[p + 2]].push(A)
    }g = [];
    for(p = 0;p < f.length;p++) {
      r = A = m = 0;
      if(f[p] != undefined) {
        for(s = 0;s < f[p].length;s++) {
          m += f[p][s][0];
          A += f[p][s][1];
          r += f[p][s][2]
        }m /= f[p].length;
        A /= f[p].length;
        r /= f[p].length;
        g[p * 3] = m;
        g[p * 3 + 1] = A;
        g[p * 3 + 2] = r
      }
    }this.setNormals(g)
  };
  e.Mesh.prototype.GLAttributes = function(f, g) {
    this.gl = f;
    this.normals || this.calcNormals();
    for(var m = 0;m < 8;m++) {
      f.disableVertexAttribArray(m)
    }if(!this.faces.GL && this.faces.data && this.faces.data.length > 0) {
      this.GLSetFaceBuffer(f);
      this.faces.GL = true
    }for(m = 0;m < this.buffers.length;m++) {
      if(!this.buffers[m].GL) {
        this.GLSetBuffer(f, this.buffers[m].name, this.buffers[m].data, this.buffers[m].size);
        this.buffers[m].GL = true
      }attribslot = e.getAttribLocation(f, g, this.buffers[m].name);
      if(attribslot > -1) {
        f.bindBuffer(f.ARRAY_BUFFER, this.GLbuffers[this.buffers[m].name]);
        f.enableVertexAttribArray(attribslot);
        f.vertexAttribPointer(attribslot, this.GLbuffers[this.buffers[m].name].itemSize, f.FLOAT, false, 0, 0)
      }
    }
  };
  e.Light = function(f) {
    e.Assets.registerAsset(this, f);
    this.color = {r:1, g:1, b:1}
  };
  e.augment(e.Placeable, e.Light);
  e.augment(e.Animatable, e.Light);
  e.augment(e.QuickNotation, e.Light);
  e.augment(e.JSONLoader, e.Light);
  e.Light.prototype.className = "Light";
  e.L_POINT = 1;
  e.L_DIR = 2;
  e.L_SPOT = 3;
  e.Light.prototype.constantAttenuation = 1;
  e.Light.prototype.linearAttenuation = 0.002;
  e.Light.prototype.quadraticAttenuation = 8.0E-4;
  e.Light.prototype.spotCosCutOff = 0.95;
  e.Light.prototype.spotPMatrix = null;
  e.Light.prototype.spotExponent = 10;
  e.Light.prototype.color = null;
  e.Light.prototype.diffuse = true;
  e.Light.prototype.specular = true;
  e.Light.prototype.samples = 0;
  e.Light.prototype.softness = 0.01;
  e.Light.prototype.type = e.L_POINT;
  e.Light.prototype.frameBuffer = null;
  e.Light.prototype.renderBuffer = null;
  e.Light.prototype.texture = null;
  e.Light.prototype.bufferHeight = 256;
  e.Light.prototype.bufferWidth = 256;
  e.Light.prototype.shadowBias = 2;
  e.Light.prototype.castShadows = false;
  e.Light.prototype.getPMatrix = function() {
    if(!this.spotPMatrix) {
      var f;
      f = this.scene && this.scene.camera ? this.scene.camera.far : 1E3;
      this.spotPMatrix = e.makePerspective(Math.acos(this.spotCosCutOff) / 3.14159 * 360, 1, 0.1, f)
    }return this.spotPMatrix
  };
  e.Light.prototype.setCastShadows = function(f) {
    this.castShadows = f;
    return this
  };
  e.Light.prototype.getCastShadows = function() {
    return this.castShadows
  };
  e.Light.prototype.setShadowBias = function(f) {
    this.shadowBias = f;
    return this
  };
  e.Light.prototype.getShadowBias = function() {
    return this.shadowBias
  };
  e.Light.prototype.setShadowSamples = function(f) {
    this.samples = f;
    return this
  };
  e.Light.prototype.getShadowSamples = function() {
    return this.samples
  };
  e.Light.prototype.setShadowSoftness = function(f) {
    this.softness = f;
    return this
  };
  e.Light.prototype.getShadowSamples = function() {
    return this.softness
  };
  e.Light.prototype.setBufferWidth = function(f) {
    this.bufferWidth = f;
    return this
  };
  e.Light.prototype.getBufferHeight = function() {
    return this.bufferHeight
  };
  e.Light.prototype.setBufferHeight = function(f) {
    this.bufferHeight = f;
    return this
  };
  e.Light.prototype.getBufferWidth = function() {
    return this.bufferWidth
  };
  e.Light.prototype.setSpotCosCutOff = function(f) {
    this.spotPMatrix = null;
    this.spotCosCutOff = f;
    return this
  };
  e.Light.prototype.getSpotCosCutOff = function() {
    return this.spotCosCutOff
  };
  e.Light.prototype.setSpotExponent = function(f) {
    this.spotExponent = f;
    return this
  };
  e.Light.prototype.getSpotExponent = function() {
    return this.spotExponent
  };
  e.Light.prototype.getAttenuation = function() {
    var f = {};
    f.constant = this.constantAttenuation;
    f.linear = this.linearAttenuation;
    f.quadratic = this.quadraticAttenuation;
    return f
  };
  e.Light.prototype.setAttenuation = function(f, g, m) {
    this.constantAttenuation = f;
    this.linearAttenuation = g;
    this.quadraticAttenuation = m;
    return this
  };
  e.Light.prototype.setAttenuationConstant = function(f) {
    this.constantAttenuation = f;
    return this
  };
  e.Light.prototype.setAttenuationLinear = function(f) {
    this.linearAttenuation = f;
    return this
  };
  e.Light.prototype.setAttenuationQuadratic = function(f) {
    this.quadraticAttenuation = f;
    return this
  };
  e.Light.prototype.setColor = function(f) {
    f = e.colorParse(f);
    this.color = {r:f.r, g:f.g, b:f.b};
    return this
  };
  e.Light.prototype.setColorR = function(f) {
    this.color.r = f;
    return this
  };
  e.Light.prototype.setColorG = function(f) {
    this.color.g = f;
    return this
  };
  e.Light.prototype.setColorB = function(f) {
    this.color.b = f;
    return this
  };
  e.Light.prototype.getColor = function() {
    return this.color
  };
  e.Light.prototype.getType = function() {
    return this.type
  };
  e.Light.prototype.setType = function(f) {
    this.type = f;
    return this
  };
  e.Light.prototype.GLInit = function(f) {
    this.gl = f;
    this.type == e.L_SPOT && !this.texture && this.createSpotBuffer(f)
  };
  e.Light.prototype.createSpotBuffer = function(f) {
    this.frameBuffer = f.createFramebuffer();
    this.renderBuffer = f.createRenderbuffer();
    this.texture = f.createTexture();
    f.bindTexture(f.TEXTURE_2D, this.texture);
    try {
      f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, this.bufferWidth, this.bufferHeight, 0, f.RGBA, f.UNSIGNED_BYTE, null)
    }catch(g) {
      var m = new Uint8Array(this.bufferWidth * this.bufferHeight * 4);
      f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, h(this.bufferWidth), h(this.bufferHeight), 0, f.RGBA, f.UNSIGNED_BYTE, m)
    }f.bindFramebuffer(f.FRAMEBUFFER, this.frameBuffer);
    f.bindRenderbuffer(f.RENDERBUFFER, this.renderBuffer);
    f.renderbufferStorage(f.RENDERBUFFER, f.DEPTH_COMPONENT16, this.bufferWidth, this.bufferHeight);
    f.bindRenderbuffer(f.RENDERBUFFER, null);
    f.framebufferTexture2D(f.FRAMEBUFFER, f.COLOR_ATTACHMENT0, f.TEXTURE_2D, this.texture, 0);
    f.framebufferRenderbuffer(f.FRAMEBUFFER, f.DEPTH_ATTACHMENT, f.RENDERBUFFER, this.renderBuffer);
    f.bindFramebuffer(f.FRAMEBUFFER, null)
  };
  e.C_PERSPECTIVE = 1;
  e.C_ORTHO = 2;
  e.Camera = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.Placeable, e.Camera);
  e.augment(e.Animatable, e.Camera);
  e.augment(e.QuickNotation, e.Camera);
  e.augment(e.JSONLoader, e.Camera);
  e.Camera.prototype.className = "Camera";
  e.Camera.prototype.fovy = 35;
  e.Camera.prototype.aspect = 1;
  e.Camera.prototype.near = 0.1;
  e.Camera.prototype.far = 1E3;
  e.Camera.prototype.orthoscale = 5;
  e.Camera.prototype.type = e.C_PERSPECTIVE;
  e.Camera.prototype.pMatrix = null;
  e.Camera.prototype.getOrthoScale = function() {
    if(this.type == e.C_ORTHO) {
      return this.orthoscale
    }else {
      e.error("You may only get a scale for a orthographic camera");
      return 1
    }
  };
  e.Camera.prototype.setOrthoScale = function(f) {
    if(this.type == e.C_ORTHO) {
      this.orthoscale = f;
      this.pMatrix = null
    }else {
      e.error("You may only set a scale for a orthographic camera")
    }return this
  };
  e.Camera.prototype.getFar = function() {
    return this.far
  };
  e.Camera.prototype.setFar = function(f) {
    this.far = f;
    return this
  };
  e.Camera.prototype.getNear = function() {
    return this.near
  };
  e.Camera.prototype.setNear = function(f) {
    this.near = f;
    return this
  };
  e.Camera.prototype.getType = function() {
    return this.type
  };
  e.Camera.prototype.setType = function(f) {
    if(f == e.C_PERSPECTIVE || f == e.C_ORTHO) {
      this.type = f;
      this.pMatrix = null
    }else {
      e.error("unsuported camera type")
    }return this
  };
  e.Camera.prototype.getFovY = function() {
    if(this.type == e.C_PERSPECTIVE) {
      return this.fovy
    }else {
      e.error("You may only get a yfov for a perspective camera");
      return 1
    }
  };
  e.Camera.prototype.setFovY = function(f) {
    if(this.type == e.C_PERSPECTIVE) {
      this.fovy = f;
      this.pMatrix = this.ymax = null
    }else {
      e.error("You may only set a yfov for a perspective camera")
    }return this
  };
  e.Camera.prototype.getAspect = function() {
    if(this.type == e.C_PERSPECTIVE || this.type == e.C_ORTHO) {
      return this.aspect
    }else {
      e.error("You may only set a aspect for a perspective or orthographic camera");
      return 1
    }
  };
  e.Camera.prototype.setAspect = function(f) {
    if(this.type == e.C_PERSPECTIVE || this.type == e.C_ORTHO) {
      this.aspect = f;
      this.pMatrix = null
    }else {
      e.error("You may only set a aspect for a perspective or orthographic camera")
    }return this
  };
  e.Camera.prototype.getProjectionMatrix = function() {
    if(!this.pMatrix) {
      switch(this.type) {
        case e.C_PERSPECTIVE:
          this.pMatrix = e.makePerspective(this.fovy, this.aspect, this.near, this.far);
          break;
        case e.C_ORTHO:
          this.pMatrix = e.makeOrtho(-this.orthoscale * this.aspect, this.orthoscale * this.aspect, -this.orthoscale, this.orthoscale, this.near, this.far);
          break
      }
    }return this.pMatrix
  };
  e.Camera.prototype.setProjectionMatrix = function(f) {
    this.pMatrix = f;
    return this
  };
  e.Camera.prototype.updateMatrix = function() {
    var f = this.getPosition();
    f = e.translateMatrix(f.x, f.y, f.z);
    f = e.mulMat4(f, this.getRotMatrix());
    if(this.parent) {
      f = e.mulMat4(this.parent.getModelMatrix(), f)
    }this.matrix = e.inverseMat4(f)
  };
  e.Camera.prototype.getViewMatrix = function() {
    if(!this.matrix || !this.rotmatrix) {
      this.updateMatrix()
    }return this.matrix
  };
  e.Camera.prototype.getViewProjection = function() {
    var f = this.getProjectionMatrix(), g = this.getViewMatrix();
    if(f != this.vpProjectionMatrix || g != this.vpViewMatrix) {
      this.cameraViewProjection = e.mulMat4(f, g);
      this.vpProjectionMatrix = f;
      this.vpViewMatrix = g
    }return this.cameraViewProjection
  };
  e.FOG_NONE = 1;
  e.FOG_LINEAR = 2;
  e.FOG_QUADRATIC = 3;
  e.Scene = function(f) {
    e.Assets.registerAsset(this, f);
    this.children = [];
    this.camera = new e.Camera;
    this.backgroundColor = {r:1, g:1, b:1, a:1};
    this.ambientColor = {r:0, g:0, b:0};
    this.fogColor = {r:0.5, g:0.5, b:0.5};
    this.passes = []
  };
  e.augment(e.Group, e.Scene);
  e.augment(e.QuickNotation, e.Scene);
  e.augment(e.JSONLoader, e.Scene);
  e.Scene.prototype.camera = null;
  e.Scene.prototype.className = "Scene";
  e.Scene.prototype.renderer = null;
  e.Scene.prototype.backgroundColor = null;
  e.Scene.prototype.filter = null;
  e.Scene.prototype.fogColor = null;
  e.Scene.prototype.ambientColor = null;
  e.Scene.prototype.fogNear = 10;
  e.Scene.prototype.fogFar = 80;
  e.Scene.prototype.fogType = e.FOG_NONE;
  e.Scene.prototype.passes = null;
  e.Scene.prototype.culling = true;
  e.Scene.prototype.getFogType = function() {
    return this.fogType
  };
  e.Scene.prototype.setFogType = function(f) {
    this.fogType = f;
    return this
  };
  e.Scene.prototype.getFogFar = function() {
    return this.fogFar
  };
  e.Scene.prototype.setFogFar = function(f) {
    this.fogFar = f;
    return this
  };
  e.Scene.prototype.getFogNear = function() {
    return this.fogNear
  };
  e.Scene.prototype.setFogNear = function(f) {
    this.fogNear = f;
    return this
  };
  e.Scene.prototype.getFogColor = function() {
    return this.fogColor
  };
  e.Scene.prototype.setFogColor = function(f) {
    f = e.colorParse(f);
    this.fogColor = {r:f.r, g:f.g, b:f.b};
    return this
  };
  e.Scene.prototype.getBackgroundColor = function() {
    return this.backgroundColor
  };
  e.Scene.prototype.setBackgroundColor = function(f) {
    f = e.colorParse(f);
    this.backgroundColor = {r:f.r, g:f.g, b:f.b, a:f.a};
    return this
  };
  e.Scene.prototype.getAmbientColor = function() {
    return this.ambientColor
  };
  e.Scene.prototype.setAmbientColor = function(f) {
    f = e.colorParse(f);
    this.ambientColor = {r:f.r, g:f.g, b:f.b};
    this.renderer && this.renderer.gl.clearColor(this.backgroundColor.r, this.backgroundColor.g, this.backgroundColor.b, 1);
    return this
  };
  e.Scene.prototype.setAmbientColorR = function(f) {
    this.ambientColor.r = f;
    return this
  };
  e.Scene.prototype.setAmbientColorG = function(f) {
    this.ambientColor.g = f;
    return this
  };
  e.Scene.prototype.setAmbientColorB = function(f) {
    this.ambientColor.b = f;
    return this
  };
  e.Scene.prototype.setCamera = function(f) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }this.camera = f;
    return this
  };
  e.Scene.prototype.getCamera = function() {
    return this.camera
  };
  e.Scene.prototype.setCull = function(f) {
    this.culling = f;
    return this
  };
  e.Scene.prototype.getCull = function() {
    return this.culling
  };
  e.Scene.prototype.GLInit = function(f) {
    this.gl = f;
    f.lights = this.getLights();
    this.camera.setAspect(this.renderer.canvas.width / this.renderer.canvas.height);
    this.renderer.gl.clearColor(this.backgroundColor.r, this.backgroundColor.g, this.backgroundColor.b, 1);
    for(var g = 0;g < this.children;g++) {
      this.children[g].GLInit && children[g].GLInit(f)
    }
  };
  e.Scene.prototype.GLDestroy = function() {
  };
  e.Scene.sortFunc = function(f, g) {
    return f.zdepth - g.zdepth
  };
  e.Scene.prototype.zSort = function(f, g) {
    f = f.scene.camera.getViewMatrix();
    for(var m = 0;m < g.length;m++) {
      if(g[m].object.getBoundingVolume) {
        var p = g[m].object.getBoundingVolume().getCenter()
      }else {
        p = g[m].object.getModelMatrix();
        p = [p[3], p[7], p[11]]
      }g[m].zdepth = p[0] * f[8] + p[1] * f[9] + p[2] * f[10] + f[11]
    }g.sort(e.Scene.sortFunc);
    return g
  };
  e.Scene.prototype.setFilter2d = function(f) {
    this.filter = f;
    return this
  };
  e.Scene.prototype.getFilter2d = function() {
    return this.filter
  };
  e.Scene.prototype.getFrameBuffer = function(f) {
    if(this.filter) {
      return this.filter.getFrameBuffer(f)
    }return null
  };
  e.Scene.prototype.objectsInViewFrustum = function(f, g) {
    for(var m = [], p = e.cameraViewProjectionToPlanes(g), r = 0;r < f.length;r++) {
      g = f[r];
      if(g.getBoundingVolume && g.cull) {
        var s = g.getBoundingVolume(), A = s.getCenter(), v = s.getSphereRadius();
        if(e.sphereInFrustumPlanes([A[0], A[1], A[2], v], p)) {
          s = s.getCornerPoints();
          e.pointsInFrustumPlanes(s, p) && m.push(g)
        }
      }else {
        m.push(g)
      }
    }return m
  };
  e.Scene.prototype.unfoldRenderObject = function(f) {
    for(var g = [], m = 0;m < f.length;m++) {
      var p = f[m];
      if(p.getMultiMaterials) {
        for(var r = p.getMultiMaterials(), s = 0;s < r.length;s++) {
          var A = r[s].getMaterial();
          r[s].getMesh();
          if(!A.meshIdx) {
            A.matIdx = s
          }if(!A.meshIdx) {
            A.meshIdx = s
          }g.push({object:p, multiMaterial:s})
        }
      }else {
        g.push({object:p, multiMaterial:0})
      }
    }return g
  };
  e.Scene.prototype.stateSort = function(f, g) {
    if(!f.object.GLShaderProgram) {
      return 1
    }if(!g.object.GLShaderProgram) {
      return-1
    }var m = f.object.GLShaderProgram.progIdx, p = g.object.GLShaderProgram.progIdx;
    if(m > p) {
      return 1
    }else {
      if(m < p) {
        return-1
      }else {
        if(!f.object.multimaterials || !g.object.multimaterials) {
          return-1
        }m = f.object.multimaterials[f.multiMaterial].getMaterial().matIdx;
        p = g.object.multimaterials[g.multiMaterial].getMaterial().matIdx;
        if(m > p) {
          return 1
        }else {
          if(m < p) {
            return-1
          }else {
            m = f.object.multimaterials[f.multiMaterial].getMesh();
            f = f.object.multimaterials[f.multiMaterial].getMesh();
            if(!m) {
              return-1
            }if(!f) {
              return 1
            }m = m.meshIdx;
            p = f.meshIdx;
            return m > p ? 1 : m < p ? -1 : 0
          }
        }
      }
    }
  };
  e.Scene.prototype.render = function(f) {
    this.camera.lookAt && this.camera.Lookat(this.camera.lookAt);
    this.animate();
    var g = f.lights;
    f.scene = this;
    this.lastMaterial = null;
    f.disable(f.BLEND);
    this.framebuffer = this.getFrameBuffer(f);
    var m = this.getObjects(), p = this.camera.getViewProjection();
    if(this.culling) {
      p = this.camera.getViewProjection();
      m = this.objectsInViewFrustum(m, p)
    }m = this.unfoldRenderObject(m);
    m = m.sort(this.stateSort);
    for(var r = 0;r < g.length;r++) {
      if(g[r].castShadows) {
        g[r].gl || g[r].GLInit(f);
        f.bindFramebuffer(f.FRAMEBUFFER, g[r].frameBuffer);
        f.viewport(0, 0, h(g[r].bufferWidth), h(g[r].bufferHeight));
        f.clear(f.COLOR_BUFFER_BIT | f.DEPTH_BUFFER_BIT);
        p = this.camera.matrix;
        var s = this.camera.getProjectionMatrix();
        if(!g[r].s_cache) {
          g[r].s_cache = {}
        }if(g[r].s_cache.pmatrix != g[r].getPMatrix() || g[r].s_cache.mvmatrix != g[r].getModelMatrix()) {
          g[r].s_cache.pmatrix = g[r].getPMatrix();
          g[r].s_cache.mvmatrix = g[r].getModelMatrix();
          g[r].s_cache.imvmatrix = e.inverseMat4(g[r].getModelMatrix());
          g[r].s_cache.smatrix = e.mulMat4(g[r].getPMatrix(), g[r].s_cache.imvmatrix)
        }this.camera.setProjectionMatrix(g[r].s_cache.pmatrix);
        this.camera.matrix = g[r].s_cache.imvmatrix;
        for(var A = 0;A < m.length;A++) {
          m[A].object.GLRender(f, e.RENDER_SHADOW, A, m[A].multiMaterial)
        }f.flush();
        this.camera.matrix = p;
        this.camera.setProjectionMatrix(s);
        f.bindFramebuffer(f.FRAMEBUFFER, null)
      }
    }this.camera.animation && this.camera.animate();
    this.getPasses(f, m);
    p = this.camera.matrix;
    s = this.camera.getProjectionMatrix();
    for(this.allowPasses = false;this.passes.length > 0;) {
      g = this.passes.pop();
      f.bindFramebuffer(f.FRAMEBUFFER, g.frameBuffer);
      this.camera.matrix = g.cameraMatrix;
      this.camera.setProjectionMatrix(g.projectionMatrix);
      this.renderPass(f, m, 0, 0, g.width, g.height, e.RENDER_DEFAULT, g.self)
    }this.camera.matrix = p;
    this.camera.setProjectionMatrix(s);
    f.bindFramebuffer(f.FRAMEBUFFER, this.framebuffer);
    this.renderPass(f, m, this.renderer.getViewportOffsetX(), this.renderer.getViewportOffsetY(), this.renderer.getViewportWidth(), this.renderer.getViewportHeight());
    this.applyFilter(f, m, null);
    this.allowPasses = true
  };
  e.Scene.prototype.getPasses = function(f, g) {
    for(var m = 0;m < g.length;m++) {
      g[m].object.GLRender(f, e.RENDER_NULL, 0, g[m].multiMaterial)
    }
  };
  e.Scene.prototype.renderPass = function(f, g, m, p, r, s, A, v) {
    f.clearDepth(1);
    f.depthFunc(f.LEQUAL);
    f.viewport(m, p, r, s);
    f.clearColor(this.backgroundColor.r, this.backgroundColor.g, this.backgroundColor.b, this.backgroundColor.a);
    if(A) {
      f.clear(f.DEPTH_BUFFER_BIT | f.COLOR_BUFFER_BIT | f.STENCIL_BUFFER_BIT)
    }else {
      f.scissor(m, p, r, s);
      f.enable(f.SCISSOR_TEST);
      this.renderer.GLClear();
      f.disable(f.SCISSOR_TEST)
    }if(!A) {
      A = e.RENDER_DEFAULT
    }m = [];
    f.disable(f.BLEND);
    for(p = 0;p < g.length;p++) {
      if(!g[p].object.zTrans && g[p] != v) {
        g[p].object.GLRender(f, A, 0, g[p].multiMaterial)
      }else {
        g[p] != v && m.push(g[p])
      }
    }f.enable(f.BLEND);
    m = this.zSort(f, m);
    for(p = 0;p < m.length;p++) {
      g[p] != v && m[p].object.GLRender(f, A, 0, m[p].multiMaterial)
    }
  };
  e.Scene.prototype.applyFilter = function(f, g, m) {
    if(this.filter && this.filter.renderDepth) {
      f.clearDepth(1);
      f.depthFunc(f.LEQUAL);
      f.bindFramebuffer(f.FRAMEBUFFER, this.filter.getDepthBuffer(f));
      this.renderPass(f, g, 0, 0, this.filter.getDepthBufferWidth(), this.filter.getDepthBufferHeight(), e.RENDER_SHADOW)
    }if(this.filter && this.filter.renderNormal) {
      f.clearDepth(1);
      f.depthFunc(f.LEQUAL);
      f.bindFramebuffer(f.FRAMEBUFFER, this.filter.getNormalBuffer(f));
      this.renderPass(f, g, 0, 0, this.filter.getNormalBufferWidth(), this.filter.getNormalBufferHeight(), e.RENDER_NORMAL)
    }this.filter && this.filter.GLRender(f, m)
  };
  e.Scene.prototype.addRenderPass = function(f, g, m, p, r, s) {
    this.allowPasses && this.passes.push({frameBuffer:f, cameraMatrix:g, projectionMatrix:m, height:r, width:p, self:s});
    return this
  };
  e.Scene.prototype.ray = function(f, g) {
    var m = this.renderer.gl, p = this.camera.matrix, r = this.camera.pMatrix;
    this.camera.matrix = e.inverseMat4(e.Mat4([g[2], g[1], g[0], f[0], g[0], g[2], g[1], f[1], g[1], g[0], g[2], f[2], 0, 0, 0, 1]));
    if(!this.pickPMatrix) {
      this.pickPMatrix = e.makeOrtho(-1.0E-4, 1.0E-4, -1.0E-4, 1.0E-4, this.camera.near, this.camera.far)
    }this.camera.pMatrix = this.pickPMatrix;
    m.viewport(0, 0, 8, 1);
    m.clear(m.DEPTH_BUFFER_BIT);
    m.disable(m.BLEND);
    m.scene = this;
    for(var s = this.getObjects(), A = 0;A < s.length;A++) {
      s[A].pickable && s[A].GLRender(m, e.RENDER_PICK, A + 1)
    }m.flush();
    A = new Uint8Array(32);
    m.readPixels(0, 0, 8, 1, m.RGBA, m.UNSIGNED_BYTE, A);
    var v = [A[4] / 255, A[5] / 255, A[6] / 255], B = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) * 0.5;
    v = [v[0] / B - 1, v[1] / B - 1, v[2] / B - 1];
    s = s[A[0] + A[1] * 256 + A[2] * 65536 - 1];
    B = (A[10] / 255 + 0.00390625 * A[9] / 255 + 1.52587890625E-5 * A[8] / 255) * this.camera.far;
    var C = [];
    C[0] = A[14] / 255 + 0.00390625 * A[13] / 255 + 1.52587890625E-5 * A[12] / 255;
    C[1] = A[18] / 255 + 0.00390625 * A[17] / 255 + 1.52587890625E-5 * A[16] / 255;
    m.bindFramebuffer(m.FRAMEBUFFER, null);
    m.viewport(0, 0, this.renderer.canvas.width, this.renderer.canvas.height);
    this.camera.matrix = p;
    this.camera.pMatrix = r;
    if(s) {
      return{object:s, distance:B, coord:[f[0] - g[0] * B, f[1] - g[1] * B, f[2] - g[2] * B], normal:v, texture:C}
    }return null
  };
  e.Scene.prototype.pick = function(f, g) {
    f = this.makeRay(f, g);
    if(!f) {
      return null
    }return this.ray(f.origin, f.coord)
  };
  e.Scene.prototype.makeRay = function(f, g) {
    if(this.camera) {
      if(this.camera.matrix && this.camera.pMatrix) {
        var m = this.renderer.getViewportHeight(), p = this.renderer.getViewportWidth(), r = this.renderer.getViewportOffsetX(), s = this.renderer.getViewportHeight() - this.renderer.canvas.height + this.renderer.getViewportOffsetY();
        f = ((f - r) / p - 0.5) * 2;
        m = -((g + s) / m - 0.5) * 2;
        s = e.mulMat4(e.inverseMat4(this.camera.matrix), e.inverseMat4(this.camera.pMatrix));
        g = e.mulMat4Vec4(s, [f, m, -1, 1]);
        g = [g[0] / g[3], g[1] / g[3], g[2] / g[3]];
        m = e.mulMat4Vec4(s, [f, m, 1, 1]);
        m = [-(m[0] / m[3] - g[0]), -(m[1] / m[3] - g[1]), -(m[2] / m[3] - g[2])];
        m = e.toUnitVec3(m);
        return{origin:g, coord:m}
      }else {
        return null
      }
    }else {
      e.error("No camera set for picking");
      return null
    }
  };
  e.Renderer = function(f, g) {
    this.viewport = [];
    this.canvas = f;
    try {
      this.gl = f.getContext("experimental-webgl", {alpha:true, depth:true, stencil:true, antialias:true, premultipliedAlpha:true})
    }catch(m) {
    }if(!this.gl) {
      if(!g && typeof globalNoWebGLError == "undefined") {
        f = document.createElement("div");
        f.setAttribute("style", "position: absolute; top: 10px; left: 10px; font-family: sans-serif; font-size: 14px; padding: 10px;background-color: #fcffcb;color: #800; width: 200px; border:2px solid #f00");
        f.innerHTML = "Cannot detect webgl please download a compatible browser";
        document.getElementsByTagName("body")[0].appendChild(f)
      }else {
        g()
      }throw"cannot create webgl context";
    }try {
      this.gl.canvas = f
    }catch(p) {
    }if(!this.gl.getProgramParameter) {
      this.gl.getProgramParameter = this.gl.getProgrami
    }if(!this.gl.getShaderParameter) {
      this.gl.getShaderParameter = this.gl.getShaderi
    }this.gl.uniformMatrix4fvX = this.gl.uniformMatrix4fv;
    this.gl.uniformMatrix4fv = function(r, s, A) {
      s && e.mat4gl(e.transposeMat4(A), A);
      this.uniformMatrix4fvX(r, false, A)
    };
    this.gl.clearDepth(1);
    this.gl.clearStencil(0);
    this.gl.enable(this.gl.DEPTH_TEST);
    this.gl.depthFunc(this.gl.LEQUAL);
    this.gl.blendFuncSeparate(this.gl.SRC_ALPHA, this.gl.ONE_MINUS_SRC_ALPHA, this.gl.ZERO, this.gl.ONE)
  };
  e.augment(e.QuickNotation, e.Renderer);
  e.Renderer.prototype.gl = null;
  e.Renderer.prototype.scene = null;
  e.C_STENCIL = 1;
  e.C_DEPTH = 2;
  e.C_COLOR = 4;
  e.C_ALL = 7;
  e.Renderer.prototype.clearType = e.C_ALL;
  e.Renderer.prototype.setViewportWidth = function(f) {
    this.viewport[0] = f;
    return this
  };
  e.Renderer.prototype.setViewportHeight = function(f) {
    this.viewport[1] = f;
    return this
  };
  e.Renderer.prototype.setViewportOffsetX = function(f) {
    this.viewport[2] = f;
    return this
  };
  e.Renderer.prototype.setViewportOffsetY = function(f) {
    this.viewport[3] = f;
    return this
  };
  e.Renderer.prototype.clearViewport = function() {
    this.viewport = []
  };
  e.Renderer.prototype.getViewportWidth = function() {
    return this.viewport.length > 0 ? this.viewport[0] : this.canvas.width
  };
  e.Renderer.prototype.getViewportHeight = function() {
    return this.viewport.length > 0 ? this.viewport[1] : this.canvas.height
  };
  e.Renderer.prototype.getViewportOffsetX = function() {
    return this.viewport.length > 0 ? this.viewport[2] : 0
  };
  e.Renderer.prototype.getViewportOffsetY = function() {
    return this.viewport.length > 0 ? this.viewport[3] : 0
  };
  e.Renderer.prototype.setClearType = function(f) {
    this.clearType = f;
    return this
  };
  e.Renderer.prototype.getClearType = function() {
    return this.clearType
  };
  e.Renderer.prototype.GLClear = function() {
    var f = this.gl, g = this.clearType, m = 0;
    if(g & e.C_COLOR == e.C_COLOR) {
      m |= f.COLOR_BUFFER_BIT
    }if(g & e.C_DEPTH == e.C_DEPTH) {
      m |= f.DEPTH_BUFFER_BIT
    }if(g & e.C_STENCIL == e.C_STENCIL) {
      m |= f.STENCIL_BUFFER_BIT
    }f.clear(m)
  };
  e.Renderer.prototype.getScene = function() {
    return this.scene
  };
  e.Renderer.prototype.setScene = function(f) {
    f.renderer = this;
    this.scene = f;
    f.GLInit(this.gl);
    this.render();
    f.camera.matrix = null;
    return this
  };
  e.Renderer.prototype.render = function() {
    this.cullFaces && this.gl.enable(this.gl.CULL_FACE);
    if(this.scene) {
      this.scene.render(this.gl);
      if(!this.rendered) {
        this.scene.render(this.gl);
        this.rendered = true
      }
    }
  };
  e.Texture = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.QuickNotation, e.Texture);
  e.augment(e.JSONLoader, e.Texture);
  e.Texture.prototype.className = "Texture";
  e.Texture.prototype.image = null;
  e.Texture.prototype.glTexture = null;
  e.Texture.prototype.url = null;
  e.Texture.prototype.getSrc = function() {
    return this.url
  };
  e.Texture.prototype.setSrc = function(f) {
    this.url = f;
    this.state = 0;
    this.image = new Image;
    var g = this;
    this.image.onload = function() {
      g.state = 1
    };
    this.image.src = f;
    if(this.glTexture && this.gl) {
      this.gl.deleteTexture(this.glTexture);
      this.glTexture = null
    }return this
  };
  e.Texture.prototype.doTexture = function(f) {
    this.gl = f;
    if(!this.glTexture) {
      this.glTexture = f.createTexture()
    }if(this.state == 1) {
      f.bindTexture(f.TEXTURE_2D, this.glTexture);
      f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.image);
      f.generateMipmap(f.TEXTURE_2D);
      f.bindTexture(f.TEXTURE_2D, null);
      this.state = 2
    }f.bindTexture(f.TEXTURE_2D, this.glTexture);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MAG_FILTER, f.LINEAR);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MIN_FILTER, f.LINEAR_MIPMAP_LINEAR);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_WRAP_S, f.REPEAT);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_WRAP_T, f.REPEAT);
    return this.state == 2 ? true : false
  };
  e.TextureCanvas = function(f) {
    e.Assets.registerAsset(this, f);
    this.canvas = document.createElement("canvas")
  };
  e.augment(e.QuickNotation, e.TextureCanvas);
  e.augment(e.JSONLoader, e.TextureCanvas);
  e.TextureCanvas.prototype.className = "TextureCanvas";
  e.TextureCanvas.prototype.glTexture = null;
  e.TextureCanvas.prototype.autoUpdate = true;
  e.TextureCanvas.prototype.getAutoUpdate = function() {
    return this.autoUpdate
  };
  e.TextureCanvas.prototype.setAutoUpdate = function(f) {
    this.autoUpdate = f;
    return this
  };
  e.TextureCanvas.prototype.getCanvas = function() {
    return this.canvas
  };
  e.TextureCanvas.prototype.setCanvas = function(f) {
    this.canvas = f;
    return this
  };
  e.TextureCanvas.prototype.setHeight = function(f) {
    this.canvas.height = f;
    return this
  };
  e.TextureCanvas.prototype.setWidth = function(f) {
    this.canvas.width = f;
    return this
  };
  e.TextureCanvas.prototype.getHeight = function() {
    return this.canvas.height
  };
  e.TextureCanvas.prototype.getWidth = function() {
    return this.canvas.width
  };
  e.TextureCanvas.prototype.doTexture = function(f) {
    this.gl = f;
    if(this.glTexture) {
      f.bindTexture(f.TEXTURE_2D, this.glTexture);
      if(this.autoUpdate || this.doUpdate) {
        this.updateCanvas(f)
      }
    }else {
      this.glTexture = f.createTexture();
      f.bindTexture(f.TEXTURE_2D, this.glTexture);
      this.updateCanvas(f)
    }this.doUpdate = false;
    return true
  };
  e.TextureCanvas.prototype.update = function() {
    this.doUpdate = true
  };
  e.TextureCanvas.prototype.updateCanvas = function(f) {
    var g = this.canvas;
    f.bindTexture(f.TEXTURE_2D, this.glTexture);
    try {
      f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, g)
    }catch(m) {
      f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, g, null)
    }f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MAG_FILTER, f.LINEAR);
    f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MIN_FILTER, f.LINEAR);
    f.generateMipmap(f.TEXTURE_2D)
  };
  e.TextureVideo = function(f) {
    e.Assets.registerAsset(this, f);
    this.video = document.createElement("video");
    this.video.style.display = "none";
    this.video.setAttribute("loop", "loop");
    this.video.autoplay = true;
    this.video.addEventListener("ended", function() {
      this.play()
    }, true);
    document.getElementsByTagName("body")[0].appendChild(this.video);
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d")
  };
  e.augment(e.QuickNotation, e.TextureVideo);
  e.augment(e.JSONLoader, e.TextureVideo);
  e.TextureVideo.prototype.className = "TextureVideo";
  e.TextureVideo.prototype.glTexture = null;
  e.TextureVideo.prototype.getVideo = function() {
    return this.video
  };
  e.TextureVideo.prototype.setVideo = function(f) {
    this.video = f;
    return this
  };
  e.TextureVideo.prototype.setSrc = function(f) {
    this.video.src = f;
    return this
  };
  e.TextureVideo.prototype.getSrc = function() {
    return this.video.src
  };
  e.TextureVideo.prototype.doTexture = function(f) {
    this.gl = f;
    if(!this.glTexture) {
      this.glTexture = f.createTexture()
    }f.bindTexture(f.TEXTURE_2D, this.glTexture);
    this.updateTexture(f);
    return true
  };
  e.TextureVideo.prototype.updateTexture = function(f) {
    var g = this.video;
    f.bindTexture(f.TEXTURE_2D, this.glTexture);
    if(g.readyState > 0) {
      if(g.height <= 0) {
        g.style.display = "";
        g.height = g.offsetHeight;
        g.width = g.offsetWidth;
        g.style.display = "none"
      }this.canvas.height = g.height;
      this.canvas.width = g.width;
      this.ctx.drawImage(g, 0, 0);
      try {
        f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.canvas)
      }catch(m) {
        f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.canvas, null)
      }f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MAG_FILTER, f.LINEAR);
      f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MIN_FILTER, f.LINEAR);
      f.generateMipmap(f.TEXTURE_2D)
    }
  };
  e.TextureCamera = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.QuickNotation, e.TextureCamera);
  e.augment(e.JSONLoader, e.TextureCamera);
  e.TextureCamera.prototype.className = "Texture";
  e.TextureCamera.prototype.texture = null;
  e.TextureCamera.prototype.glTexture = null;
  e.TextureCamera.prototype.object = null;
  e.TextureCamera.prototype.camera = null;
  e.TextureCamera.prototype.bufferHeight = 0;
  e.TextureCamera.prototype.bufferWidth = 0;
  e.TextureCamera.prototype.mirrorAxis = e.NONE;
  e.TextureCamera.prototype.clipAxis = e.NONE;
  e.TextureCamera.prototype.setBufferWidth = function(f) {
    this.bufferWidth = f;
    this.update = true;
    return this
  };
  e.TextureCamera.prototype.getBufferWidth = function() {
    return this.bufferWidth
  };
  e.TextureCamera.prototype.setBufferHeight = function(f) {
    this.bufferHeight = f;
    this.update = true;
    return this
  };
  e.TextureCamera.prototype.getBufferHeight = function() {
    return this.bufferHeight
  };
  e.TextureCamera.prototype.setClipAxis = function(f) {
    this.clipAxis = f;
    return this
  };
  e.TextureCamera.prototype.getClipAxis = function() {
    return this.clipAxis
  };
  e.TextureCamera.prototype.setMirrorAxis = function(f) {
    this.mirrorAxis = f;
    return this
  };
  e.TextureCamera.prototype.getMirrorAxis = function() {
    return this.mirrorAxis
  };
  e.TextureCamera.prototype.setCamera = function(f) {
    this.camera = f;
    return this
  };
  e.TextureCamera.prototype.getCamera = function() {
    return this.camera
  };
  e.TextureCamera.prototype.doTexture = function(f, g) {
    if(this.camera) {
      this.gl = f;
      var m = g.getModelMatrix(), p = f.scene.camera.getProjectionMatrix(), r = this.camera.getViewMatrix(), s;
      if(this.mirrorAxis) {
        switch(this.mirrorAxis) {
          case e.XAXIS:
            s = e.mulMat4(e.mulMat4(e.mulMat4(r, m), e.scaleMatrix(-1, 1, 1)), e.inverseMat4(m));
            break;
          case e.YAXIS:
            s = e.mulMat4(e.mulMat4(e.mulMat4(r, m), e.scaleMatrix(1, -1, 1)), e.inverseMat4(m));
            break;
          case e.ZAXIS:
            s = e.mulMat4(e.mulMat4(e.mulMat4(r, m), e.scaleMatrix(1, 1, -1)), e.inverseMat4(m));
            break
        }
      }else {
        s = r
      }if(this.clipAxis) {
        var A;
        switch(this.clipAxis) {
          case e.NEG_XAXIS:
            A = e.toUnitVec3([-m[0], -m[4], -m[8]]);
            A = [A[0], A[1], A[2], -e.dotVec3([m[3], m[7], m[11]], A)];
            break;
          case e.POS_XAXIS:
            A = e.toUnitVec3([m[0], m[4], m[8]]);
            A = [A[0], A[1], A[2], -e.dotVec3([m[3], m[7], m[11]], A)];
            break;
          case e.NEG_YAXIS:
            A = e.toUnitVec3([-m[1], -m[5], -m[9]]);
            A = [A[0], A[1], A[2], -e.dotVec3([m[3], m[7], m[11]], A)];
            break;
          case e.POS_YAXIS:
            A = e.toUnitVec3([m[1], m[5], m[9]]);
            A = [A[0], A[1], A[2], -e.dotVec3([m[3], m[7], m[11]], A)];
            break;
          case e.NEG_ZAXIS:
            A = e.toUnitVec3([-m[2], -m[6], -m[10]]);
            A = [A[0], A[1], A[2], -e.dotVec3([m[3], m[7], m[11]], A) - 0.5];
            break;
          case e.POS_ZAXIS:
            A = e.toUnitVec3([m[2], m[6], m[10]]);
            A = [A[0], A[1], A[2], -e.dotVec3([m[3], m[7], m[11]], A) - 0.5];
            break
        }
        m = e.transposeMat4(e.inverseMat4(e.mulMat4(p, s)));
        A = e.mulMat4Vec4(m, A);
        A = e.scaleVec4(A, p[10]);
        A[3] -= 1;
        A[2] < 0 && e.scaleVec4(A, -1);
        p = e.mulMat4([1, 0, 0, 0, 0, 1, 0, 0, A[0], A[1], A[2], A[3], 0, 0, 0, 1], p)
      }m = !this.bufferHeight ? f.scene.renderer.canvas.height : this.bufferHeight;
      A = !this.bufferWidth ? f.scene.renderer.canvas.width : this.bufferWidth;
      if(!this.glTexture || this.update) {
        this.createFrameBuffer(f);
        f.scene.addRenderPass(this.frameBuffer, s, f.scene.camera.getProjectionMatrix(), A, m, g);
        f.bindTexture(f.TEXTURE_2D, this.glTexture);
        return this.update = false
      }else {
        f.bindTexture(f.TEXTURE_2D, this.glTexture);
        f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MAG_FILTER, f.LINEAR);
        f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MIN_FILTER, f.LINEAR);
        f.texParameteri(f.TEXTURE_2D, f.TEXTURE_WRAP_S, f.CLAMP_TO_EDGE);
        f.texParameteri(f.TEXTURE_2D, f.TEXTURE_WRAP_T, f.CLAMP_TO_EDGE);
        f.scene.addRenderPass(this.frameBuffer, s, p, A, m, g);
        return true
      }
    }else {
      return false
    }
  };
  e.TextureCamera.prototype.registerPasses = e.TextureCamera.prototype.doTexture;
  e.TextureCamera.prototype.createFrameBuffer = function(f) {
    var g = !this.bufferHeight ? f.scene.renderer.canvas.height : this.bufferHeight, m = !this.bufferWidth ? f.scene.renderer.canvas.width : this.bufferWidth;
    if(!this.frameBuffer) {
      this.frameBuffer = f.createFramebuffer()
    }if(!this.renderBuffer) {
      this.renderBuffer = f.createRenderbuffer()
    }if(!this.glTexture) {
      this.glTexture = f.createTexture()
    }f.bindTexture(f.TEXTURE_2D, this.glTexture);
    var p = new Uint8Array(m * g * 4);
    f.texImage2D(f.TEXTURE_2D, 0, f.RGBA, m, g, 0, f.RGBA, f.UNSIGNED_BYTE, p);
    f.bindFramebuffer(f.FRAMEBUFFER, this.frameBuffer);
    f.bindRenderbuffer(f.RENDERBUFFER, this.renderBuffer);
    f.renderbufferStorage(f.RENDERBUFFER, f.DEPTH_COMPONENT16, m, g);
    f.framebufferRenderbuffer(f.FRAMEBUFFER, f.DEPTH_ATTACHMENT, f.RENDERBUFFER, this.renderBuffer);
    f.framebufferTexture2D(f.FRAMEBUFFER, f.COLOR_ATTACHMENT0, f.TEXTURE_2D, this.glTexture, 0);
    f.bindRenderbuffer(f.RENDERBUFFER, null);
    f.bindFramebuffer(f.FRAMEBUFFER, null);
    f.bindTexture(f.TEXTURE_2D, null)
  };
  e.TextureCube = function(f) {
    e.Assets.registerAsset(this, f)
  };
  e.augment(e.QuickNotation, e.TextureCube);
  e.augment(e.JSONLoader, e.TextureCube);
  e.TextureCube.prototype.className = "TextureCube";
  e.TextureCube.prototype.posX = null;
  e.TextureCube.prototype.negX = null;
  e.TextureCube.prototype.posY = null;
  e.TextureCube.prototype.negY = null;
  e.TextureCube.prototype.posZ = null;
  e.TextureCube.prototype.negZ = null;
  e.TextureCube.prototype.texture = null;
  e.TextureCube.prototype.glTexture = null;
  e.TextureCube.prototype.loadState = 0;
  e.TextureCube.prototype.setSrc = function(f, g, m) {
    this.url = f;
    this.state = 0;
    this[g] = new Image;
    var p = this;
    this[g].onload = function() {
      p.loadState += m
    };
    this[g].src = f;
    if(this.glTexture && this.gl) {
      this.gl.deleteTexture(this.glTexture);
      this.glTexture = null
    }return this
  };
  e.TextureCube.prototype.setSrcPosX = function(f) {
    this.setSrc(f, "posX", 1);
    return this
  };
  e.TextureCube.prototype.setSrcNegX = function(f) {
    this.setSrc(f, "negX", 2);
    return this
  };
  e.TextureCube.prototype.setSrcPosY = function(f) {
    this.setSrc(f, "posY", 4);
    return this
  };
  e.TextureCube.prototype.setSrcNegY = function(f) {
    if(typeof f != "string") {
      this.negY = f;
      this.loadState += 8
    }else {
      this.setSrc(f, "negY", 8)
    }return this
  };
  e.TextureCube.prototype.setSrcPosZ = function(f) {
    this.setSrc(f, "posZ", 16);
    return this
  };
  e.TextureCube.prototype.setSrcNegZ = function(f) {
    this.setSrc(f, "negZ", 32);
    return this
  };
  e.TextureCube.prototype.doTexture = function(f) {
    this.gl = f;
    if(!this.glTexture) {
      this.glTexture = f.createTexture()
    }f.bindTexture(f.TEXTURE_CUBE_MAP, this.glTexture);
    if(this.loadState == 63 && this.state == 0) {
      f.texImage2D(f.TEXTURE_CUBE_MAP_POSITIVE_X, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.posX);
      f.texImage2D(f.TEXTURE_CUBE_MAP_NEGATIVE_X, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.negX);
      f.texImage2D(f.TEXTURE_CUBE_MAP_POSITIVE_Y, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.posY);
      f.texImage2D(f.TEXTURE_CUBE_MAP_NEGATIVE_Y, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.negY);
      f.texImage2D(f.TEXTURE_CUBE_MAP_POSITIVE_Z, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.posZ);
      f.texImage2D(f.TEXTURE_CUBE_MAP_NEGATIVE_Z, 0, f.RGBA, f.RGBA, f.UNSIGNED_BYTE, this.negZ);
      f.generateMipmap(f.TEXTURE_CUBE_MAP);
      f.bindTexture(f.TEXTURE_CUBE_MAP, null);
      this.state = 1
    }f.bindTexture(f.TEXTURE_CUBE_MAP, this.glTexture);
    return this.state == 1 ? true : false
  };
  e.MaterialLayer = function(f) {
    e.Assets.registerAsset(this, f);
    this.blendMode = e.BL_MIX
  };
  e.augment(e.Animatable, e.MaterialLayer);
  e.augment(e.QuickNotation, e.MaterialLayer);
  e.augment(e.JSONLoader, e.MaterialLayer);
  e.augment(e.Events, e.MaterialLayer);
  e.MaterialLayer.prototype.className = "MaterialLayer";
  e.MaterialLayer.prototype.texture = null;
  e.MaterialLayer.prototype.blendMode = null;
  e.MaterialLayer.prototype.mapto = e.M_COLOR;
  e.MaterialLayer.prototype.mapinput = e.UV1;
  e.MaterialLayer.prototype.scaleX = 1;
  e.MaterialLayer.prototype.offsetX = 0;
  e.MaterialLayer.prototype.rotX = 0;
  e.MaterialLayer.prototype.scaleY = 1;
  e.MaterialLayer.prototype.offsetY = 0;
  e.MaterialLayer.prototype.rotY = 0;
  e.MaterialLayer.prototype.scaleZ = 1;
  e.MaterialLayer.prototype.offsetZ = 0;
  e.MaterialLayer.prototype.rotZ = 0;
  e.MaterialLayer.prototype.dScaleX = 0;
  e.MaterialLayer.prototype.dOffsetX = 0;
  e.MaterialLayer.prototype.dRotX = 0;
  e.MaterialLayer.prototype.dScaleY = 0;
  e.MaterialLayer.prototype.dOffsetY = 0;
  e.MaterialLayer.prototype.dRotY = 0;
  e.MaterialLayer.prototype.dScaleZ = 0;
  e.MaterialLayer.prototype.dOffsetZ = 0;
  e.MaterialLayer.prototype.dRotZ = 0;
  e.MaterialLayer.prototype.alpha = 1;
  e.MaterialLayer.prototype.height = 0.05;
  e.MaterialLayer.prototype.matrix = null;
  e.MaterialLayer.prototype.getMatrix = function() {
    if(!this.matrix) {
      var f = this.getOffset(), g = this.getScale(), m = this.getRotation();
      this.matrix = e.mulMat4(e.mulMat4(e.translateMatrix(f.x, f.y, f.z), e.scaleMatrix(g.x, g.y, g.z)), e.rotateMatrix(m.x, m.y, m.z))
    }return this.matrix
  };
  e.MaterialLayer.prototype.setHeight = function(f) {
    this.height = f;
    return this
  };
  e.MaterialLayer.prototype.getHeight = function() {
    return this.height
  };
  e.MaterialLayer.prototype.setAlpha = function(f) {
    this.alpha = f;
    return this
  };
  e.MaterialLayer.prototype.getAlpha = function() {
    return this.alpha
  };
  e.MaterialLayer.prototype.setTexture = function(f) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }this.texture = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.MaterialLayer.prototype.getTexture = function() {
    return this.texture
  };
  e.MaterialLayer.prototype.setMapto = function(f) {
    this.mapto = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.MaterialLayer.prototype.getMapto = function() {
    return this.mapto
  };
  e.MaterialLayer.prototype.setMapinput = function(f) {
    this.mapinput = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.MaterialLayer.prototype.getMapinput = function() {
    return this.mapinput
  };
  e.MaterialLayer.prototype.getOffset = function() {
    var f = {};
    f.x = parseFloat(this.getOffsetX()) + parseFloat(this.getDOffsetX());
    f.y = parseFloat(this.getOffsetY()) + parseFloat(this.getDOffsetY());
    f.z = parseFloat(this.getOffsetZ()) + parseFloat(this.getDOffsetZ());
    return f
  };
  e.MaterialLayer.prototype.getRotation = function() {
    var f = {};
    f.x = parseFloat(this.getRotX()) + parseFloat(this.getDRotX());
    f.y = parseFloat(this.getRotY()) + parseFloat(this.getDRotY());
    f.z = parseFloat(this.getRotZ()) + parseFloat(this.getDRotZ());
    return f
  };
  e.MaterialLayer.prototype.getScale = function() {
    var f = {};
    f.x = parseFloat(this.getScaleX()) + parseFloat(this.getDScaleX());
    f.y = parseFloat(this.getScaleY()) + parseFloat(this.getDScaleY());
    f.z = parseFloat(this.getScaleZ()) + parseFloat(this.getDScaleZ());
    return f
  };
  e.MaterialLayer.prototype.setOffsetX = function(f) {
    this.matrix = null;
    this.offsetX = f;
    return this
  };
  e.MaterialLayer.prototype.getOffsetX = function() {
    return this.offsetX
  };
  e.MaterialLayer.prototype.setOffsetY = function(f) {
    this.matrix = null;
    this.offsetY = f;
    return this
  };
  e.MaterialLayer.prototype.getOffsetY = function() {
    return this.offsetY
  };
  e.MaterialLayer.prototype.setOffsetZ = function(f) {
    this.matrix = null;
    this.offsetZ = f;
    return this
  };
  e.MaterialLayer.prototype.getOffsetZ = function() {
    return this.offsetZ
  };
  e.MaterialLayer.prototype.setDOffsetX = function(f) {
    this.matrix = null;
    this.dOffsetX = f;
    return this
  };
  e.MaterialLayer.prototype.getDOffsetX = function() {
    return this.dOffsetX
  };
  e.MaterialLayer.prototype.setDOffsetY = function(f) {
    this.matrix = null;
    this.dOffsetY = f;
    return this
  };
  e.MaterialLayer.prototype.getDOffsetY = function() {
    return this.dOffsetY
  };
  e.MaterialLayer.prototype.setDOffsetZ = function(f) {
    this.matrix = null;
    this.dOffsetZ = f;
    return this
  };
  e.MaterialLayer.prototype.getDOffsetZ = function() {
    return this.dOffsetZ
  };
  e.MaterialLayer.prototype.setScaleX = function(f) {
    this.matrix = null;
    this.scaleX = f;
    return this
  };
  e.MaterialLayer.prototype.getScaleX = function() {
    return this.scaleX
  };
  e.MaterialLayer.prototype.setScaleY = function(f) {
    this.matrix = null;
    this.scaleY = f;
    return this
  };
  e.MaterialLayer.prototype.getScaleY = function() {
    return this.scaleY
  };
  e.MaterialLayer.prototype.setScaleZ = function(f) {
    this.matrix = null;
    this.scaleZ = f;
    return this
  };
  e.MaterialLayer.prototype.getScaleZ = function() {
    return this.scaleZ
  };
  e.MaterialLayer.prototype.setDScaleX = function(f) {
    this.matrix = null;
    this.dScaleX = f;
    return this
  };
  e.MaterialLayer.prototype.getDScaleX = function() {
    return this.dScaleX
  };
  e.MaterialLayer.prototype.setDScaleY = function(f) {
    this.matrix = null;
    this.dScaleY = f;
    return this
  };
  e.MaterialLayer.prototype.getDScaleY = function() {
    return this.dScaleY
  };
  e.MaterialLayer.prototype.setDScaleZ = function(f) {
    this.matrix = null;
    this.dScaleZ = f;
    return this
  };
  e.MaterialLayer.prototype.getDScaleZ = function() {
    return this.dScaleZ
  };
  e.MaterialLayer.prototype.setRotX = function(f) {
    this.matrix = null;
    this.rotX = f;
    return this
  };
  e.MaterialLayer.prototype.getRotX = function() {
    return this.rotX
  };
  e.MaterialLayer.prototype.setRotY = function(f) {
    this.matrix = null;
    this.rotY = f;
    return this
  };
  e.MaterialLayer.prototype.getRotY = function() {
    return this.rotY
  };
  e.MaterialLayer.prototype.setRotZ = function(f) {
    this.matrix = null;
    this.rotZ = f;
    return this
  };
  e.MaterialLayer.prototype.getRotZ = function() {
    return this.rotZ
  };
  e.MaterialLayer.prototype.setDRotX = function(f) {
    this.matrix = null;
    this.dRotX = f;
    return this
  };
  e.MaterialLayer.prototype.getDRotX = function() {
    return this.dRotX
  };
  e.MaterialLayer.prototype.setDRotY = function(f) {
    this.matrix = null;
    this.dRotY = f;
    return this
  };
  e.MaterialLayer.prototype.getDRotY = function() {
    return this.dRotY
  };
  e.MaterialLayer.prototype.setDRotZ = function(f) {
    this.matrix = null;
    this.dRotZ = f;
    return this
  };
  e.MaterialLayer.prototype.getDRotZ = function() {
    return this.dRotZ
  };
  e.MaterialLayer.prototype.setBlendMode = function(f) {
    this.blendMode = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.MaterialLayer.prototype.getBlendMode = function() {
    return this.blendMode
  };
  var u = 0;
  e.Material = function(f) {
    e.Assets.registerAsset(this, f);
    this.layers = [];
    this.layerlisteners = [];
    this.textures = [];
    this.lights = [];
    this.color = {r:1, g:1, b:1, a:1};
    this.specColor = {r:1, g:1, b:1};
    this.reflect = 0.8;
    this.shine = 10;
    this.specular = 1;
    this.emit = 0;
    this.alpha = 1;
    this.materialIdx = u++
  };
  e.augment(e.Animatable, e.Material);
  e.augment(e.QuickNotation, e.Material);
  e.augment(e.JSONLoader, e.Material);
  e.augment(e.Events, e.Material);
  e.M_COLOR = 1;
  e.M_NOR = 2;
  e.M_ALPHA = 4;
  e.M_SPECCOLOR = 8;
  e.M_SPECULAR = 16;
  e.M_SHINE = 32;
  e.M_REFLECT = 64;
  e.M_EMIT = 128;
  e.M_ALPHA = 256;
  e.M_MSKR = 512;
  e.M_MSKG = 1024;
  e.M_MSKB = 2048;
  e.M_MSKA = 4096;
  e.M_HEIGHT = 8192;
  e.M_AMBIENT = 16384;
  e.UV1 = 0;
  e.UV2 = 1;
  e.MAP_NORM = 3;
  e.MAP_OBJ = 4;
  e.MAP_REF = 5;
  e.MAP_ENV = 6;
  e.MAP_VIEW = 7;
  e.BL_MIX = 0;
  e.BL_MUL = 1;
  e.Material.prototype.layers = null;
  e.Material.prototype.className = "Material";
  e.Material.prototype.textures = null;
  e.Material.prototype.color = null;
  e.Material.prototype.specColor = null;
  e.Material.prototype.specular = null;
  e.Material.prototype.emit = null;
  e.Material.prototype.shine = null;
  e.Material.prototype.reflect = null;
  e.Material.prototype.lights = null;
  e.Material.prototype.alpha = null;
  e.Material.prototype.ambient = null;
  e.Material.prototype.shadow = true;
  e.Material.prototype.setShadow = function(f) {
    this.shadow = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getShadow = function() {
    return this.shadow
  };
  e.Material.prototype.setColor = function(f) {
    f.r || (f = e.colorParse(f));
    this.color = {r:f.r, g:f.g, b:f.b};
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.setColorR = function(f) {
    this.color.r = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.setColorG = function(f) {
    this.color.g = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.setColorB = function(f) {
    this.color.b = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getColor = function() {
    return this.color
  };
  e.Material.prototype.setSpecularColor = function(f) {
    f.r || (f = e.colorParse(f));
    this.specColor = {r:parseFloat(f.r), g:parseFloat(f.g), b:parseFloat(f.b)};
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getAmbient = function() {
    return this.ambient
  };
  e.Material.prototype.setAmbient = function(f) {
    f.r || (f = e.colorParse(f));
    this.ambient = {r:parseFloat(f.r), g:parseFloat(f.g), b:parseFloat(f.b)};
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getSpecularColor = function() {
    return this.specColor
  };
  e.Material.prototype.setAlpha = function(f) {
    this.alpha = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getAlpha = function() {
    return this.alpha
  };
  e.Material.prototype.setSpecular = function(f) {
    this.specular = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getSpecular = function() {
    return this.specular
  };
  e.Material.prototype.setShininess = function(f) {
    if(f <= 0.0625) {
      f = 0.0625
    }this.shine = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getShininess = function() {
    return this.shine
  };
  e.Material.prototype.setEmit = function(f) {
    this.emit = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getEmit = function() {
    return this.emit
  };
  e.Material.prototype.setReflectivity = function(f) {
    this.reflect = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getReflectivity = function() {
    return this.reflect
  };
  e.Material.prototype.setBinaryAlpha = function(f) {
    this.binaryAlpha = f;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.getBinaryAlpha = function() {
    return this.binaryAlpha
  };
  e.Material.prototype.addMaterialLayer = function(f) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }this.layers.push(f);
    var g = this, m = function() {
      g.fireEvent("shaderupdate", {})
    };
    this.layerlisteners.push(m);
    f.addEventListener("shaderupdate", m);
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.removeMaterialLayer = function(f) {
    var g = this.layers.indexOf(f);
    if(g >= 0) {
      this.layers.splice(g, 1);
      f.removeEventListener("shaderupdate", this.layerlisteners[g]);
      this.layerlisteners.splice(g, 1);
      this.fireEvent("shaderupdate", {})
    }return this
  };
  e.Material.prototype.getLayers = function() {
    return this.layers
  };
  e.Material.prototype.getLayerCoords = function() {
    var f = [];
    f.push("vec4 texturePos;\n");
    for(i = 0;i < this.layers.length;i++) {
      f.push("textureCoords" + i + "=vec3(0.0,0.0,0.0);\n");
      if(this.layers[i].mapinput == e.UV1 || this.layers[i].mapinput == e.UV2) {
        f.push("texturePos=vec4(vec2(UVCoord[" + this.layers[i].mapinput * 2 + "],(1.0-UVCoord[" + (this.layers[i].mapinput * 2 + 1) + "])),1.0,1.0);\n")
      }this.layers[i].mapinput == e.MAP_NORM && f.push("texturePos=vec4(normalize(n.xyz),1.0);\n");
      this.layers[i].mapinput == e.MAP_OBJ && f.push("texturePos=vec4(normalize(OBJCoord.xyz),1.0);\n");
      this.layers[i].mapinput == e.MAP_REF && f.push("texturePos=vec4(reflect(normalize(eyevec.xyz),normalize(n.xyz)),1.0);\n");
      this.layers[i].mapinput == e.MAP_ENV && f.push("texturePos=envMat * vec4(reflect(normalize(eyevec.xyz),normalize(n.xyz)),1.0);\n");
      f.push("textureCoords" + i + "=(layer" + i + "Matrix * texturePos).xyz;\n")
    }return f.join("")
  };
  e.Material.prototype.getVertexVarying = function() {
    var f = [];
    for(i = 0;i < this.layers.length;i++) {
      f.push("uniform mat4 layer" + i + "Matrix;\n");
      f.push("varying vec3 textureCoords" + i + ";\n")
    }return f.join("")
  };
  e.Material.prototype.registerPasses = function(f, g) {
    for(var m = 0;m < this.textures.length;m++) {
      this.textures[m].registerPasses && this.textures[m].registerPasses(f, g)
    }
  };
  e.Material.prototype.getFragmentShader = function(f) {
    for(var g = "#ifdef GL_ES\nprecision highp float;\n#endif\n", m = false, p = 0;p < f.length;p++) {
      if(f[p].type == e.L_POINT || f[p].type == e.L_SPOT || f[p].type == e.L_DIR) {
        g = g + "varying vec3 lightvec" + p + ";\n";
        g = g + "varying vec3 tlightvec" + p + ";\n";
        g = g + "varying vec3 lightpos" + p + ";\n";
        g = g + "varying vec3 tlightdir" + p + ";\n";
        g = g + "varying float lightdist" + p + ";\n";
        g = g + "varying vec2 spotCoords" + p + ";\n"
      }
    }g += "varying vec3 n;\n";
    g += "varying vec3 b;\n";
    g += "varying vec3 t;\n";
    g += "varying vec4 UVCoord;\n";
    g += "varying vec3 eyevec;\n";
    g += "varying vec3 OBJCoord;\n";
    g += "varying vec3 teyevec;\n";
    for(p = 0;p < this.textures.length;p++) {
      if(this.textures[p].className == "Texture") {
        g = g + "uniform sampler2D TEXTURE" + p + ";\n"
      }if(this.textures[p].className == "TextureCanvas") {
        g = g + "uniform sampler2D TEXTURE" + p + ";\n"
      }if(this.textures[p].className == "TextureVideo") {
        g = g + "uniform sampler2D TEXTURE" + p + ";\n"
      }if(this.textures[p].className == "TextureCube") {
        g = g + "uniform samplerCube TEXTURE" + p + ";\n"
      }
    }var r = 0, s = [], A;
    for(p = 0;p < f.length;p++) {
      g = g + "uniform vec3 lightcolor" + p + ";\n";
      g = g + "uniform vec3 lightAttenuation" + p + ";\n";
      g = g + "uniform float spotCosCutOff" + p + ";\n";
      g = g + "uniform float spotExp" + p + ";\n";
      g = g + "uniform vec3 lightdir" + p + ";\n";
      g = g + "uniform mat4 lightmat" + p + ";\n";
      g = g + "uniform float shadowbias" + p + ";\n";
      g = g + "uniform int shadowsamples" + p + ";\n";
      g = g + "uniform float shadowsoftness" + p + ";\n";
      g = g + "uniform bool castshadows" + p + ";\n";
      g = g + "varying vec4 spotcoord" + p + ";\n";
      if(f[p].getCastShadows() && this.shadow) {
        A = this.textures.length + r++;
        g = g + "uniform sampler2D TEXTURE" + A + ";\n";
        s[p] = A
      }
    }for(p = 0;p < this.layers.length;p++) {
      g = g + "varying vec3 textureCoords" + p + ";\n";
      g = g + "uniform float layeralpha" + p + ";\n";
      if((this.layers[p].mapto & e.M_HEIGHT) == e.M_HEIGHT) {
        g = g + "uniform float layerheight" + p + ";\n"
      }
    }g += "uniform vec4 baseColor;\n";
    g += "uniform vec3 specColor;\n";
    g += "uniform float shine;\n";
    g += "uniform float specular;\n";
    g += "uniform float reflective;\n";
    g += "uniform float emit;\n";
    g += "uniform float alpha;\n";
    g += "uniform vec3 amb;\n";
    g += "uniform float fognear;\n";
    g += "uniform float fogfar;\n";
    g += "uniform int fogtype;\n";
    g += "uniform vec3 fogcolor;\n";
    g += "uniform float far;\n";
    g += "uniform mat4 worldInverseTranspose;\n";
    g += "uniform mat4 projection;\n";
    g += "void main(void)\n";
    g += "{\n";
    g += "float att;\n";
    g += "int texture;\n";
    g += "float mask=1.0;\n";
    g += "float spec=specular;\n";
    g += "vec3 specC=specColor;\n";
    g += "vec4 view;\n";
    g += "vec3 textureCoords=vec3(0.0,0.0,0.0);\n";
    g += "float ref=reflective;\n";
    g += "float sh=shine;\n";
    g += "float em=emit;\n";
    g += "float al=alpha;\n";
    g += "vec3 amblight=amb;\n";
    g += "vec4 normalmap= vec4(n,0.0);\n";
    g += "vec4 color = baseColor;";
    g += "float pheight=0.0;\n";
    g += "vec3 textureHeight=vec3(0.0,0.0,0.0);\n";
    r = false;
    for(p = A = 0;p < this.layers.length;p++) {
      g = g + "textureCoords=textureCoords" + p + "+textureHeight;\n";
      g = g + "mask=layeralpha" + p + "*mask;\n";
      if(this.layers[p].mapinput == e.MAP_VIEW) {
        g += "view=projection * vec4(-eyevec,1.0);\n";
        g += "textureCoords=view.xyz/view.w*0.5+0.5;\n";
        g += "textureCoords=textureCoords+textureHeight;\n"
      }if(this.layers[p].getTexture().className == "Texture" || this.layers[p].getTexture().className == "TextureCanvas" || this.layers[p].getTexture().className == "TextureVideo") {
        var v = "xy", B = "2D"
      }else {
        v = "xyz";
        B = "Cube"
      }if((this.layers[p].mapto & e.M_COLOR) == e.M_COLOR) {
        A = p;
        g = this.layers[p].blendMode == e.BL_MUL ? g + "color = color*(1.0-mask) + color*texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ")*mask;\n" : g + "color = color*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ")*mask;\n"
      }if((this.layers[p].mapto & e.M_HEIGHT) == e.M_HEIGHT) {
        g = g + "pheight = texture2D(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").x;\n";
        g = g + "textureHeight =vec3((layerheight" + p + "* (pheight-0.5)  * normalize(teyevec).xy*vec2(1.0,-1.0)),0.0);\n"
      }if((this.layers[p].mapto & e.M_SPECCOLOR) == e.M_SPECCOLOR) {
        g = g + "specC = specC*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").rgb*mask;\n"
      }if((this.layers[p].mapto & e.M_MSKR) == e.M_MSKR) {
        g = g + "mask = texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").r;\n"
      }if((this.layers[p].mapto & e.M_MSKG) == e.M_MSKG) {
        g = g + "mask = texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").g;\n"
      }if((this.layers[p].mapto & e.M_MSKB) == e.M_MSKB) {
        g = g + "mask = texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").b;\n"
      }if((this.layers[p].mapto & e.M_MSKA) == e.M_MSKA) {
        g = g + "mask = texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").a;\n"
      }if((this.layers[p].mapto & e.M_SPECULAR) == e.M_SPECULAR) {
        g = g + "spec = spec*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").r*mask;\n"
      }if((this.layers[p].mapto & e.M_REFLECT) == e.M_REFLECT) {
        g = g + "ref = ref*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").g*mask;\n"
      }if((this.layers[p].mapto & e.M_SHINE) == e.M_SHINE) {
        g = g + "sh = sh*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").b*mask*255.0;\n"
      }if((this.layers[p].mapto & e.M_EMIT) == e.M_EMIT) {
        g = g + "em = em*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").r*mask;\n"
      }if((this.layers[p].mapto & e.M_NOR) == e.M_NOR) {
        g = g + "normalmap = normalmap*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ")*mask;\n";
        m = true
      }if((this.layers[p].mapto & e.M_ALPHA) == e.M_ALPHA) {
        r = true;
        g = g + "al = al*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").a*mask;\n"
      }if((this.layers[p].mapto & e.M_AMBIENT) == e.M_AMBIENT) {
        g = g + "amblight = amblight*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[p].texture.idx + ", textureCoords." + v + ").rgb*mask;\n"
      }
    }if(!r && this.layers.length) {
      if(this.layers[A].getTexture().className == "Texture" || this.layers[A].getTexture().className == "TextureCanvas" || this.layers[A].getTexture().className == "TextureVideo") {
        v = "xy";
        B = "2D"
      }else {
        v = "xyz";
        B = "Cube"
      }g = g + "al = al*(1.0-mask) + texture" + B + "(TEXTURE" + this.layers[A].texture.idx + ", textureCoords." + v + ").a*mask;\n"
    }g += "if(al<0.5) discard;\n";
    if(this.binaryAlpha) {
      g += "al=1.0;\n"
    }g += m ? "vec3 normal = normalize(normalmap.rgb)*2.0-1.0;\n" : "vec3 normal = normalize(n);\n";
    g += "vec3 lightvalue=amblight;\n";
    g += "vec3 specvalue=vec3(0.0,0.0,0.0);\n";
    g += "float dotN,spotEffect;";
    g += "vec3 lightvec=vec3(0.0,0.0,0.0);";
    g += "vec3 viewvec=vec3(0.0,0.0,0.0);";
    g += "float spotmul=0.0;";
    g += "float spotsampleX=0.0;";
    g += "float spotsampleY=0.0;";
    g += "float totalweight=0.0;";
    g += "int cnt=0;";
    g += "float specularSmoothStepValue=.125;\n";
    g += "vec2 spotoffset=vec2(0.0,0.0);";
    g += "float dp=0.0;";
    g += "if (normal.z<0.0) {normal.z=0.0;}\n";
    g += "normal/=length(normal);\n";
    for(p = 0;p < f.length;p++) {
      if(m) {
        g = g + "lightvec=tlightvec" + p + "*vec3(-1.0,-1.0,1.0);\n";
        g += "viewvec=teyevec*vec3(-1.0,-1.0,1.0);\n"
      }else {
        g = g + "lightvec=lightvec" + p + ";\n";
        g += "viewvec=eyevec;\n"
      }if(f[p].type == e.L_POINT) {
        g += "dotN=max(dot(normal,normalize(-lightvec)),0.0);\n";
        g = g + "att = 1.0 / (lightAttenuation" + p + "[0] + lightAttenuation" + p + "[1] * lightdist" + p + " + lightAttenuation" + p + "[2] * lightdist" + p + " * lightdist" + p + ");\n";
        if(f[p].diffuse) {
          g = g + "lightvalue += att * dotN * lightcolor" + p + ";\n"
        }if(f[p].specular) {
          g = g + "specvalue += smoothstep(-specularSmoothStepValue,specularSmoothStepValue,dotN)*att * specC * lightcolor" + p + " * spec  * pow(max(dot(reflect(normalize(lightvec), normal),normalize(viewvec)),0.0), 0.3*sh);\n"
        }
      }g += "spotEffect = 0.0;\n";
      if(f[p].type == e.L_SPOT) {
        g = g + "spotEffect = dot(normalize(lightdir" + p + "), normalize(-lightvec" + p + "));";
        g = g + "if (spotEffect > spotCosCutOff" + p + ") {\n";
        g = g + "spotEffect = pow(spotEffect, spotExp" + p + ");";
        if(f[p].getCastShadows() && this.shadow) {
          g = g + "if(castshadows" + p + "){\n";
          g = g + "vec4 dist=texture2D(TEXTURE" + s[p] + ", (((spotcoord" + p + ".xy)/spotcoord" + p + ".w)+1.0)/2.0);\n";
          g += "float depth = dot(dist, vec4(0.000000059604644775390625,0.0000152587890625,0.00390625,1.0))*100.0;\n";
          g += "spotmul=0.0;\n";
          g += "totalweight=0.0;\n";
          g = g + "if((depth+shadowbias" + p + "-length(lightvec" + p + "))<0.0) {spotmul=1.0; totalweight=1.0;}\n";
          g = g + "if(shadowsamples" + p + ">0){\n";
          g += "for(cnt=0; cnt<4; cnt++){;\n";
          g += "spotsampleX=-0.707106781;spotsampleY=-0.707106781;\n";
          g += "if(cnt==0 || cnt==3) spotsampleX=0.707106781;\n";
          g += "if(cnt==1 || cnt==3) spotsampleY=0.707106781;\n";
          g += "spotoffset=vec2(spotsampleX,spotsampleY)*0.5;\n";
          g = g + "dist=texture2D(TEXTURE" + s[p] + ", (((spotcoord" + p + ".xy)/spotcoord" + p + ".w)+1.0)/2.0+spotoffset*shadowsoftness" + p + ");\n";
          g += "depth = dot(dist, vec4(0.000000059604644775390625,0.0000152587890625,0.00390625,1.0))*100.0;\n";
          g = g + "if((depth+shadowbias" + p + "-length(lightvec" + p + "))<0.0){\n";
          g += "spotmul+=length(spotoffset);\n";
          g += "}\n";
          g += "totalweight+=length(spotoffset);\n";
          g += "};\n";
          g += "};\n";
          g += "if(totalweight!=spotmul){\n";
          g += "spotmul=0.0;\n";
          g += "totalweight=0.0;\n";
          g = g + "for(cnt=0; cnt<shadowsamples" + p + "*2; cnt++){;\n";
          g = g + "spotsampleX=(fract(sin(dot(spotcoord" + p + ".xy + vec2(float(cnt)),vec2(12.9898,78.233))) * 43758.5453)-0.5)*2.0;\n";
          g = g + "spotsampleY=(fract(sin(dot(spotcoord" + p + ".yz + vec2(float(cnt)),vec2(12.9898,78.233))) * 43758.5453)-0.5)*2.0;\n";
          g += "spotoffset=vec2(spotsampleX,spotsampleY);\n";
          g = g + "dist=texture2D(TEXTURE" + s[p] + ", (((spotcoord" + p + ".xy)/spotcoord" + p + ".w)+1.0)/2.0+spotoffset*shadowsoftness" + p + ");\n";
          g += "depth = dot(dist, vec4(0.000000059604644775390625,0.0000152587890625,0.00390625,1.0))*100.0;\n";
          g = g + "if((depth+shadowbias" + p + "-length(lightvec" + p + "))<0.0){\n";
          g += "spotmul+=length(spotoffset);\n";
          g += "}\n";
          g += "totalweight+=length(spotoffset);\n";
          g += "};\n";
          g += "}\n";
          g += "if(totalweight>0.0) spotEffect=spotEffect*pow(1.0-spotmul/totalweight,3.0);\n";
          g += "}"
        }g += "dotN=max(dot(normal,normalize(-lightvec)),0.0);\n";
        g = g + "att = spotEffect / (lightAttenuation" + p + "[0] + lightAttenuation" + p + "[1] * lightdist" + p + " + lightAttenuation" + p + "[2] * lightdist" + p + " * lightdist" + p + ");\n";
        if(f[p].diffuse) {
          g = g + "lightvalue += att * dotN * lightcolor" + p + ";\n"
        }g += "}\n";
        if(f[p].specular) {
          g = g + "specvalue += smoothstep(-specularSmoothStepValue,specularSmoothStepValue,dotN) * att * specC * lightcolor" + p + " * spec  * pow(max(dot(reflect(normalize(lightvec), normal),normalize(viewvec)),0.0), 0.3 * sh);\n"
        }
      }if(f[p].type == e.L_DIR) {
        g += "dotN=max(dot(normal,-normalize(lightvec)),0.0);\n";
        if(f[p].diffuse) {
          g = g + "lightvalue += dotN * lightcolor" + p + ";\n"
        }if(f[p].specular) {
          g = g + "specvalue += smoothstep(-specularSmoothStepValue,specularSmoothStepValue,dotN) * specC * lightcolor" + p + " * spec  * pow(max(dot(reflect(normalize(lightvec), normal),normalize(viewvec)),0.0), 0.3 * sh);\n"
        }
      }
    }g += "float fogfact=1.0;";
    g = g + "if(fogtype==" + e.FOG_QUADRATIC + ") fogfact=clamp(pow(max((fogfar - length(eyevec)) / (fogfar - fognear),0.0),2.0),0.0,1.0);\n";
    g = g + "if(fogtype==" + e.FOG_LINEAR + ") fogfact=clamp((fogfar - length(eyevec)) / (fogfar - fognear),0.0,1.0);\n";
    g += "lightvalue = (lightvalue)*ref;\n";
    g += "if(em>0.0){lightvalue=vec3(1.0,1.0,1.0);  fogfact=1.0;}\n";
    g += "if (al<.25) discard;\n";
    g += "gl_FragColor =vec4(specvalue.rgb+color.rgb*(em+1.0)*lightvalue.rgb,al)*fogfact+vec4(fogcolor,al)*(1.0-fogfact);\n";
    g += "}\n";
    return g
  };
  e.Material.prototype.textureUniforms = function(f, g, m, p) {
    this.animation && this.animate();
    var r = g.caches;
    if(r.baseColor != this.color) {
      if(this.ccache != this.color) {
        this.ccache = this.color;
        this.glColor = new Float32Array([this.color.r, this.color.g, this.color.b, this.color.a])
      }f.uniform4fv(e.getUniformLocation(f, g, "baseColor"), this.glColor);
      r.baseColor = this.color
    }if(r.specColor != this.specColor) {
      if(this.sccache != this.specColor) {
        this.sccache = this.specColor;
        this.glspecColor = new Float32Array([this.specColor.r, this.specColor.g, this.specColor.b])
      }f.uniform3fv(e.getUniformLocation(f, g, "specColor"), this.glspecColor);
      r.specColor = this.specColor
    }if(r.specular != this.specular) {
      e.setUniform(f, "1f", e.getUniformLocation(f, g, "specular"), this.specular);
      r.specular = this.specular
    }if(r.shine != this.shine) {
      e.setUniform(f, "1f", e.getUniformLocation(f, g, "shine"), this.shine);
      r.shine = this.shine
    }if(r.reflect != this.reflect) {
      e.setUniform(f, "1f", e.getUniformLocation(f, g, "reflective"), this.reflect);
      r.reflect = this.reflect
    }if(r.emit != this.emit) {
      e.setUniform(f, "1f", e.getUniformLocation(f, g, "emit"), this.emit);
      r.emit = this.emit
    }if(r.alpha != this.alpha) {
      e.setUniform(f, "1f", e.getUniformLocation(f, g, "alpha"), this.alpha);
      r.alpha = this.alpha
    }var s = 0, A = 0;
    if(!r.lightcolor) {
      r.lightcolor = [];
      r.lightAttenuation = [];
      r.spotCosCutOff = [];
      r.spotExponent = [];
      r.shadowbias = [];
      r.castshadows = [];
      r.shadowsamples = [];
      r.shadowsoftness = []
    }for(var v = 0;v < m.length;v++) {
      if(r.lightcolor[v] != m[v].color) {
        e.setUniform3(f, "3f", e.getUniformLocation(f, g, "lightcolor" + v), m[v].color.r, m[v].color.g, m[v].color.b);
        r.lightcolor[v] = m[v].color
      }if(r.lightAttenuation[v] != m[v].constantAttenuation) {
        e.setUniform3(f, "3f", e.getUniformLocation(f, g, "lightAttenuation" + v), m[v].constantAttenuation, m[v].linearAttenuation, m[v].quadraticAttenuation);
        r.lightAttenuation[v] = m[v].constantAttenuation
      }if(r.spotCosCutOff[v] != m[v].spotCosCutOff) {
        e.setUniform(f, "1f", e.getUniformLocation(f, g, "spotCosCutOff" + v), m[v].spotCosCutOff);
        r.spotCosCutOff[v] = m[v].spotCosCutOff
      }if(r.spotExponent[v] != m[v].spotExponent) {
        e.setUniform(f, "1f", e.getUniformLocation(f, g, "spotExp" + v), m[v].spotExponent);
        r.spotExponent[v] = m[v].spotExponent
      }if(r.shadowbias[v] != m[v].shadowBias) {
        e.setUniform(f, "1f", e.getUniformLocation(f, g, "shadowbias" + v), m[v].shadowBias);
        r.shadowbias[v] = m[v].shadowBias
      }if(r.castshadows[v] != m[v].castShadows) {
        e.setUniform(f, "1i", e.getUniformLocation(f, g, "castshadows" + v), m[v].castShadows);
        r.castshadows[v] = m[v].castShadows
      }if(r.shadowsamples[v] != m[v].samples) {
        e.setUniform(f, "1i", e.getUniformLocation(f, g, "shadowsamples" + v), m[v].samples);
        r.shadowsamples[v] = m[v].samples
      }if(r.shadowsoftness[v] != m[v].softness) {
        e.setUniform(f, "1f", e.getUniformLocation(f, g, "shadowsoftness" + v), m[v].softness);
        r.shadowsoftness[v] = m[v].softness
      }if(m[v].getCastShadows() && this.shadow && this.emit == 0) {
        A = this.textures.length + s++;
        f.activeTexture(f["TEXTURE" + A]);
        f.bindTexture(f.TEXTURE_2D, m[v].texture);
        f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MAG_FILTER, f.LINEAR);
        f.texParameteri(f.TEXTURE_2D, f.TEXTURE_MIN_FILTER, f.LINEAR);
        f.generateMipmap(f.TEXTURE_2D);
        e.setUniform(f, "1i", e.getUniformLocation(f, g, "TEXTURE" + A), A)
      }
    }if(!g.glarrays.layermat) {
      g.glarrays.layermat = []
    }for(v = 0;v < this.layers.length;v++) {
      this.layers[v].animation && this.layers[v].animate();
      this.layers[v].getScale();
      this.layers[v].getOffset();
      if(g.glarrays.layermat[v]) {
        e.mat4gl(this.layers[v].getMatrix(), g.glarrays.layermat[v])
      }else {
        g.glarrays.layermat[v] = new Float32Array(this.layers[v].getMatrix())
      }try {
        e.setUniformMatrix(f, "Matrix4fv", e.getUniformLocation(f, g, "layer" + v + "Matrix"), true, g.glarrays.layermat[v])
      }catch(B) {
      }e.setUniform(f, "1f", e.getUniformLocation(f, g, "layeralpha" + v), this.layers[v].getAlpha());
      e.setUniform(f, "1f", e.getUniformLocation(f, g, "layerheight" + v), this.layers[v].getHeight())
    }for(v = 0;v < this.textures.length;v++) {
      f.activeTexture(f["TEXTURE" + v]);
      this.textures[v].doTexture(f, p);
      e.setUniform(f, "1i", e.getUniformLocation(f, g, "TEXTURE" + v), v)
    }
  };
  e.Material.prototype.addTexture = function(f) {
    if(typeof f == "string") {
      f = e.Assets.get(f)
    }this.textures.push(f);
    f.idx = this.textures.length - 1;
    this.fireEvent("shaderupdate", {});
    return this
  };
  e.Material.prototype.addTextureCube = e.Material.prototype.addTexture;
  e.Material.prototype.addTextureCamera = e.Material.prototype.addTexture;
  e.Material.prototype.addTextureCanvas = e.Material.prototype.addTexture;
  e.Material.prototype.addTextureVideo = e.Material.prototype.addTexture;
  j()
})(GLGE);if(typeof GLGE == "undefined") {
  GLGE = {}
}(function(e) {
  function j(f, g) {
    var m = null;
    if(f.getAttribute("id") == g) {
      return f
    }for(var p = 0;p < f.childNodes.length;p++) {
      if(f.childNodes[p].nodeType == 1) {
        m = j(f.childNodes[p], g);
        if(m != null) {
          break
        }
      }
    }return m
  }
  e.ColladaDocuments = [];
  e.Collada = function() {
    this.children = [];
    this.actions = {};
    this.actionsIdx = this.boneIdx = 0
  };
  e.augment(e.Group, e.Collada);
  e.Collada.prototype.type = e.G_NODE;
  e.Collada.prototype.getAbsolutePath = function(f, g) {
    if(f.substr(0, 7) == "http://" || f.substr(0, 7) == "file://" || f.substr(0, 7) == "https://") {
      return f
    }else {
      if(!g) {
        g = window.location.href
      }var m = g.split("/");
      g = m[2];
      for(var p = m[0], r = [], s = 3;s < m.length - 1;s++) {
        r.push(m[s])
      }if(f.substr(0, 1) == "/") {
        r = []
      }f = f.split("/");
      for(s = 0;s < f.length;s++) {
        if(f[s] == "..") {
          r.pop()
        }else {
          f[s] != "" && r.push(f[s])
        }
      }return p + "//" + g + "/" + r.join("/")
    }
  };
  e.Collada.prototype.getElementById = function(f) {
    if(!this.idcache) {
      var g = this.getElementsByTagName("*"), m;
      this.idcache = {};
      for(var p = 0;p < g.length;p++) {
        m = g[p].getAttribute("id");
        if(m != "") {
          this.idcache[m] = g[p]
        }
      }
    }return this.idcache[f]
  };
  e.Collada.prototype.parseArray = function(f) {
    f = f.firstChild;
    for(var g = "", m = [], p, r;f;) {
      p = (g + f.nodeValue).replace(/\s+/g, " ").replace(/^\s+/g, "").split(" ");
      f = f.nextSibling;
      p[0] == "" && p.unshift();
      if(f) {
        g = p.pop()
      }for(r = 0;r < p.length;r++) {
        p[r] != "" && m.push(p[r])
      }
    }return m
  };
  e.Collada.prototype.isSketchupFile = function() {
    var f = this.xml.getElementsByTagName("asset");
    if(!f || f.length == 0) {
      return false
    }for(var g = 0;g < f.length;++g) {
      var m = f[g].getElementsByTagName("contributor");
      if(!m || m.length == 0) {
        return false
      }for(var p = 0;p < m.length;++p) {
        var r = m[p].getElementsByTagName("authoring_tool");
        if(!r || r.length == 0) {
          return false
        }for(var s = 0;s < r.length;++s) {
          if(r[s].firstChild.nodeValue.indexOf("Google") == 0) {
            return true
          }
        }
      }
    }return false
  };
  e.Collada.prototype.setDocument = function(f, g, m) {
    this.url = f;
    this.loadedCallback = m;
    if(f.indexOf("#") != -1) {
      this.rootId = f.substr(f.indexOf("#") + 1);
      f = f.substr(0, f.indexOf("#"))
    }if(g) {
      f = this.getAbsolutePath(f, g)
    }this.docURL = f;
    if(e.ColladaDocuments[f]) {
      this.xml = e.ColladaDocuments[f]
    }else {
      if(g = new XMLHttpRequest) {
        g.overrideMimeType("text/xml");
        var p = f, r = this;
        g.onreadystatechange = function() {
          if(this.readyState == 4) {
            if(this.status == 200 || this.status == 0) {
              this.responseXML.getElementById = r.getElementById;
              r.loaded(p, this.responseXML)
            }else {
              e.error("Error loading Document: " + p + " status " + this.status)
            }
          }
        };
        g.open("GET", f, true);
        g.send("")
      }
    }
  };
  e.Collada.prototype.getSource = function(f) {
    f = this.xml.getElementById(f);
    if(!f) {
      return[]
    }if(!f.jsArray || this.badAccessor) {
      var g;
      if(f.tagName == "vertices") {
        g = [];
        for(var m = f.getElementsByTagName("input"), p = 0;p < m.length;p++) {
          g[p] = this.getSource(m[p].getAttribute("source").substr(1));
          g[p].block = m[p].getAttribute("semantic")
        }
      }else {
        p = f.getElementsByTagName("technique_common")[0].getElementsByTagName("accessor")[0];
        g = this.xml.getElementById(p.getAttribute("source").substr(1));
        m = g.tagName;
        g = this.parseArray(g);
        stride = parseInt(p.getAttribute("stride"));
        (offset = parseInt(p.getAttribute("offset"))) || (offset = 0);
        stride || (stride = 1);
        count = parseInt(p.getAttribute("count"));
        var r = p.getElementsByTagName("param"), s = [];
        for(p = 0;p < r.length;p++) {
          r[p].hasAttribute("name") || this.exceptions.badAccessor || this.badAccessor ? s.push({type:r[p].getAttribute("type"), name:r[p].getAttribute("name")}) : s.push(false)
        }g = {array:g, stride:stride, offset:offset, count:count, pmask:s, type:m}
      }f.jsArray = g
    }return f.jsArray
  };
  var h = {};
  e.Collada.prototype.getMeshes = function(f, g) {
    h[this.url] || (h[this.url] = []);
    if(h[this.url][f]) {
      return h[this.url][f]
    }var m, p, r, s, A, v, B, C, E;
    m = this.xml.getElementById(f);
    if(!m) {
      e.error("Collada.getMeshes returning [], id: " + f);
      return[]
    }m = m.getElementsByTagName("mesh");
    if(!m) {
      e.error("Collada.getMeshes returning [], id: " + f);
      return[]
    }meshNode = null;
    if(m.length) {
      meshNode = m[0]
    }else {
      e.error("Collada.getMeshes returning [], id: " + f)
    }var H = [];
    if(!meshNode) {
      return H
    }A = meshNode.getElementsByTagName("polylist");
    for(m = 0;m < A.length;m++) {
      r = this.parseArray(A[m].getElementsByTagName("p")[0]);
      vcount = this.parseArray(A[m].getElementsByTagName("vcount")[0]);
      E = A[m].getElementsByTagName("input");
      var J = 0;
      for(p = 0;p < E.length;p++) {
        J = Math.max(J, E[p].getAttribute("offset"))
      }v = [];
      for(p = s = 0;p < vcount.length;p++) {
        for(E = 0;E < vcount[p] - 2;E++) {
          for(k = 0;k <= J;k++) {
            v.push(r[s + k])
          }for(k = 0;k <= J;k++) {
            v.push(r[s + (J + 1) * (E + 1) + k])
          }for(k = 0;k <= J;k++) {
            v.push(r[s + (J + 1) * (E + 2) + k])
          }
        }s += (J + 1) * vcount[p]
      }A[m].getElementsByTagName("p")[0].data = v
    }B = meshNode.getElementsByTagName("polygons");
    for(m = 0;m < B.length;m++) {
      var M = B[m].getElementsByTagName("p");
      v = [];
      for(var K = 0;K < M.length;K++) {
        r = this.parseArray(M[K]);
        E = B[m].getElementsByTagName("input");
        for(p = J = 0;p < E.length;p++) {
          J = Math.max(J, E[p].getAttribute("offset"))
        }for(E = s = 0;E < r.length / (J + 1) - 2;E++) {
          for(k = 0;k <= J;k++) {
            v.push(r[s + k])
          }for(k = 0;k <= J;k++) {
            v.push(r[s + (J + 1) * (E + 1) + k])
          }for(k = 0;k <= J;k++) {
            v.push(r[s + (J + 1) * (E + 2) + k])
          }
        }s += (J + 1) * (r.length / (J + 1))
      }if(M.length > 0) {
        B[m].getElementsByTagName("p")[0].data = v
      }
    }M = [];
    v = meshNode.getElementsByTagName("triangles");
    for(m = 0;m < A.length;m++) {
      M.push(A[m])
    }for(m = 0;m < B.length;m++) {
      B[m].getElementsByTagName("p").length > 0 && M.push(B[m])
    }for(m = 0;m < v.length;m++) {
      M.push(v[m])
    }for(m = 0;m < M.length;m++) {
      r = M[m].getElementsByTagName("input");
      A = [];
      v = [];
      s = [];
      B = {};
      for(p = 0;p < r.length;p++) {
        r[p].data = this.getSource(r[p].getAttribute("source").substr(1));
        C = r[p].getAttribute("semantic");
        if(C == "TEXCOORD") {
          (E = r[p].getAttribute("set")) || (E = 0);
          C += E
        }if(C == "VERTEX") {
          for(K = 0;K < r[p].data.length;K++) {
            B[r[p].data[K].block] = []
          }
        }r[p].block = C;
        r[p].offset = parseInt(r[p].getAttribute("offset"));
        B[C] = [];
        s.push(r[p])
      }r = M[m].getElementsByTagName("p")[0].data ? M[m].getElementsByTagName("p")[0].data : this.parseArray(M[m].getElementsByTagName("p")[0]);
      for(p = 0;p < s.length;p++) {
        if(s[p].block != "VERTEX") {
          s[p].data = [s[p].data];
          s[p].data[0].block = s[p].block
        }
      }for(p = J = 0;p < s.length;p++) {
        J = Math.max(s[p].offset + 1, J)
      }for(E = 0;E < r.length;E += J) {
        for(p = 0;p < s.length;p++) {
          for(K = 0;K < s[p].data.length;K++) {
            C = s[p].data[K].block;
            var N = s[p].data[K].stride;
            for(k = 0;k < s[p].data[K].stride;k++) {
              s[p].data[K].pmask[k] && B[C].push(s[p].data[K].array[r[E + s[p].offset] * s[p].data[K].stride + k + s[p].data[K].offset])
            }if(g && C == "POSITION") {
              for(k = 0;k < g.count;k++) {
                A.push(g.vertexJoints[r[E + s[p].offset] * g.count + k]);
                v.push(g.vertexWeight[r[E + s[p].offset] * g.count + k])
              }
            }if(C == "POSITION" && N == 1) {
              B[C].push(0);
              B[C].push(0)
            }C == "POSITION" && N == 2 && B[C].push(0);
            C == "TEXCOORD0" && N == 3 && B[C].pop();
            C == "TEXCOORD1" && N == 3 && B[C].pop()
          }
        }
      }r = [];
      E = e.Mesh.WINDING_ORDER_CLOCKWISE;
      if(B.NORMAL) {
        E = e.Mesh.WINDING_ORDER_CLOCKWISE;
        for(p = 0;p < B.POSITION.length;p += 9) {
          K = e.subVec3([B.POSITION[p], B.POSITION[p + 1], B.POSITION[p + 2]], [B.POSITION[p + 3], B.POSITION[p + 4], B.POSITION[p + 5]]);
          J = e.subVec3([B.POSITION[p + 6], B.POSITION[p + 7], B.POSITION[p + 8]], [B.POSITION[p], B.POSITION[p + 1], B.POSITION[p + 2]]);
          s = e.crossVec3(J, K);
          for(J = K = 0;J < 9;J += 3) {
            if(s[0] * B.NORMAL[p + J] + s[1] * B.NORMAL[p + J + 1] + s[2] * B.NORMAL[p + J + 2] < 0) {
              K -= 1
            }else {
              K += 1
            }
          }if(K < 0) {
            K = B.POSITION.length / 3;
            r.push(p / 3);
            r.push(p / 3 + 2);
            r.push(p / 3 + 1)
          }else {
            r.push(p / 3);
            r.push(p / 3 + 1);
            r.push(p / 3 + 2)
          }
        }
      }else {
        console.log("Autogenerating normals, do not know facings");
        B.NORMAL = [];
        for(p = 0;p < B.POSITION.length;p += 9) {
          K = e.subVec3([B.POSITION[p], B.POSITION[p + 1], B.POSITION[p + 2]], [B.POSITION[p + 3], B.POSITION[p + 4], B.POSITION[p + 5]]);
          J = e.subVec3([B.POSITION[p + 6], B.POSITION[p + 7], B.POSITION[p + 8]], [B.POSITION[p], B.POSITION[p + 1], B.POSITION[p + 2]]);
          s = e.toUnitVec3(e.crossVec3(e.toUnitVec3(J), e.toUnitVec3(K)));
          B.NORMAL.push(s[0]);
          B.NORMAL.push(s[1]);
          B.NORMAL.push(s[2]);
          B.NORMAL.push(s[0]);
          B.NORMAL.push(s[1]);
          B.NORMAL.push(s[2]);
          B.NORMAL.push(s[0]);
          B.NORMAL.push(s[1]);
          B.NORMAL.push(s[2])
        }K = B.POSITION.length / 3;
        for(p = 0;p < K;p++) {
          r.push(p)
        }
      }if(!this.isSketchupFile()) {
        E = e.Mesh.WINDING_ORDER_UNKNOWN
      }p = function(Q, R) {
        return Q > R ? R : Q
      };
      K = 21843;
      K *= 3;
      J = (r.length - r.length % K) / K + (r.length % K ? 1 : 0);
      s = [];
      for(C = 0;C < J;++C) {
        s.push(new e.Mesh(undefined, E));
        s[C].setPositions(B.POSITION.slice(K * C * 3, p(K * 3 * (C + 1), B.POSITION.length)));
        s[C].setNormals(B.NORMAL.slice(K * C * 3, p(K * (C + 1) * 3, B.POSITION.length)));
        B.TEXCOORD0 && s[C].setUV(B.TEXCOORD0.slice(K * C * 2, p(K * (C + 1) * 2, B.TEXCOORD0.length)));
        !B.TEXCOORD0 && B.TEXCOORD1 && s[C].setUV(B.TEXCOORD1.slice(K * C * 2, p(K * (C + 1) * 2, B.TEXCOORD1.length)));
        B.TEXCOORD1 && s[C].setUV2(B.TEXCOORD1.slice(K * C * 2, p(K * (C + 1) * 2, B.TEXCOORD1.length)))
      }if(g) {
        if(g.count > 8) {
          B = [];
          C = [];
          for(E = 0;E < v.length;E += g.count) {
            N = [];
            for(k = 0;k < g.count;k++) {
              N.push({weight:v[E + k], joint:A[E + k]})
            }N.sort(function(Q, R) {
              return parseFloat(R.weight) - parseFloat(Q.weight)
            });
            for(k = 0;k < 8;k++) {
              B.push(N[k].joint);
              C.push(N[k].weight)
            }
          }A = B;
          v = C;
          g.count = 8
        }for(C = 0;C < J;++C) {
          s[C].setJoints(g.joints);
          s[C].setInvBindMatrix(g.inverseBindMatrix);
          B = p(K * (C + 1) * g.count, A.length);
          E = K * C * g.count;
          s[C].setVertexJoints(A.slice(E, B), g.count);
          s[C].setVertexWeights(v.slice(E, B), g.count)
        }
      }for(C = 0;C < J;++C) {
        s[C].setFaces(r.slice(0, p(K * (C + 1), r.length) - K * C));
        s[C].matName = M[m].getAttribute("material");
        H.push(s[C])
      }
    }return h[this.url][f] = H
  };
  e.Collada.prototype.getFloat4 = function(f, g) {
    f = f.getElementsByTagName("newparam");
    for(var m = 0;m < f.length;m++) {
      if(f[m].getAttribute("sid") == g) {
        return f[m].getElementsByTagName("float4")[0].firstChild.nodeValue
      }
    }return null
  };
  e.Collada.prototype.getFloat = function(f, g) {
    f = f.getElementsByTagName("newparam");
    for(var m = 0;m < f.length;m++) {
      if(f[m].getAttribute("sid") == g) {
        return f[m].getElementsByTagName("float")[0].firstChild.nodeValue
      }
    }return null
  };
  e.Collada.prototype.getSampler = function(f, g) {
    f = f.getElementsByTagName("newparam");
    for(var m = 0;m < f.length;m++) {
      if(f[m].getAttribute("sid") == g) {
        return f[m].getElementsByTagName("sampler2D")[0].getElementsByTagName("source")[0].firstChild.nodeValue
      }
    }return null
  };
  e.Collada.prototype.getSurface = function(f, g) {
    f = f.getElementsByTagName("newparam");
    for(var m = 0;m < f.length;m++) {
      if(f[m].getAttribute("sid") == g) {
        return f[m].getElementsByTagName("surface")[0].getElementsByTagName("init_from")[0].firstChild.nodeValue
      }
    }return null
  };
  e.Collada.prototype.getImage = function(f) {
    if(f = this.xml.getElementById(f)) {
      return this.getAbsolutePath(f.getElementsByTagName("init_from")[0].firstChild.nodeValue, this.docURL)
    }
  };
  e.Collada.prototype.createMaterialLayer = function(f, g, m, p, r) {
    var s;
    (m = this.getSurface(m, this.getSampler(m, f.getAttribute("texture")))) || (m = f.getAttribute("texture"));
    s = this.getImage(m);
    m = new e.Texture;
    m.setSrc(s);
    g.addTexture(m);
    s = new e.MaterialLayer;
    s.setTexture(m);
    s.setMapto(p);
    if(f.hasAttribute("texcoord") && r[f.getAttribute("texcoord")]) {
      if(r[f.getAttribute("texcoord")] == 1) {
        s.setMapinput(e.UV2)
      }else {
        r[f.getAttribute("texcoord")] != 0 && e.error("GLGE only supports 2 texture sets\n");
        s.setMapinput(e.UV1)
      }
    }else {
      e.error("Collada material does not specify texture coordinates, but it may have them: defaulting to set 0\n");
      s.setMapinput(e.UV1)
    }if(f.getElementsByTagName("blend_mode")[0]) {
      var A = f.getElementsByTagName("blend_mode")[0].firstChild.nodeValue
    }A == "MULTIPLY" && s.setBlendMode(e.BL_MUL);
    g.addMaterialLayer(s)
  };
  var o = {};
  e.Collada.prototype.getMaterial = function(f, g) {
    o[this.url] || (o[this.url] = {});
    if(o[this.url][f]) {
      return o[this.url][f]
    }var m = this.xml.getElementsByTagName("library_materials")[0];
    m = j(m, f);
    if(!m) {
      m = new e.Material;
      return o[this.url][f] = m
    }var p = this.xml.getElementById(m.getElementsByTagName("instance_effect")[0].getAttribute("url").substr(1)).getElementsByTagName("profile_COMMON")[0], r = p.getElementsByTagName("technique")[0];
    m = new e.Material;
    m.setSpecular(0);
    o[this.url][f] = m;
    var s;
    f = r.getElementsByTagName("ambient");
    if(f.length > 0) {
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "color":
            s = f.firstChild.nodeValue.replace(/\s+/g, " ").split(" ");
            m.setAmbient({r:s[0], g:s[1], b:s[2]});
            break;
          case "param":
            s = this.getFloat4(p, f.getAttribute("ref")).replace(/\s+/g, " ").split(" ");
            m.setAmbient({r:s[0], g:s[1], b:s[2]});
            break;
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_AMBIENT, g);
            break
        }
      }while(f = f.nextSibling)
    }f = r.getElementsByTagName("diffuse");
    if(f.length > 0) {
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "color":
            s = f.firstChild.nodeValue.replace(/\s+/g, " ").split(" ");
            m.setColor({r:s[0], g:s[1], b:s[2]});
            break;
          case "param":
            s = this.getFloat4(p, f.getAttribute("ref")).replace(/\s+/g, " ").split(" ");
            m.setColor({r:s[0], g:s[1], b:s[2]});
            break;
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_COLOR, g);
            break
        }
      }while(f = f.nextSibling)
    }f = r.getElementsByTagName("bump");
    if(f.length > 0) {
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_NOR, g);
            break
        }
      }while(f = f.nextSibling)
    }if(r.getElementsByTagName("shininess").length > 0) {
      m.setSpecular(1);
      f = r.getElementsByTagName("shininess")[0].firstChild;
      do {
        switch(f.tagName) {
          case "float":
            parseFloat(f.firstChild.nodeValue) > 1 ? m.setShininess(parseFloat(f.firstChild.nodeValue)) : m.setShininess(parseFloat(f.firstChild.nodeValue) * 128);
            break;
          case "param":
            s = parseFloat(this.getFloat(p, f.getAttribute("ref")));
            s > 1 ? m.setShininess(s) : m.setShininess(s * 128);
            break;
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_SHINE, g);
            break
        }
      }while(f = f.nextSibling)
    }f = r.getElementsByTagName("specular");
    if(f.length > 0) {
      m.setSpecular(1);
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "color":
            s = f.firstChild.nodeValue.replace(/\s+/g, " ").split(" ");
            m.setSpecularColor({r:s[0], g:s[1], b:s[2]});
            break;
          case "param":
            s = this.getFloat4(p, f.getAttribute("ref")).replace(/\s+/g, " ").split(" ");
            m.setSpecularColor({r:s[0], g:s[1], b:s[2]});
            break;
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_SPECCOLOR, g);
            break
        }
      }while(f = f.nextSibling)
    }f = r.getElementsByTagName("emission");
    if(f.length > 0) {
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "color":
            s = f.firstChild.nodeValue.split(" ");
            m.setEmit(s[0]);
            break;
          case "param":
            s = this.getFloat4(p, f.getAttribute("ref")).split(" ");
            m.setEmit(s[0]);
            break;
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_EMIT, g);
            break
        }
      }while(f = f.nextSibling)
    }f = r.getElementsByTagName("reflective");
    if(f.length > 0) {
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "color":
            f.firstChild.nodeValue.replace(/\s+/g, " ").split(" ");
            break;
          case "param":
            this.getFloat4(p, f.getAttribute("ref")).replace(/\s+/g, " ").split(" ");
            break;
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_REFLECT, g);
            break
        }
      }while(f = f.nextSibling)
    }f = r.getElementsByTagName("transparency");
    if(f.length > 0) {
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "float":
            break;
          case "param":
            break
        }
      }while(f = f.nextSibling)
    }f = r.getElementsByTagName("transparent");
    if(f.length > 0) {
      (r = f[0].getAttribute("opaque")) || (r = "A_ONE");
      f = f[0].firstChild;
      do {
        switch(f.tagName) {
          case "float":
            s = parseFloat(f.firstChild.nodeValue);
            if(s < 1) {
              m.setAlpha(parseFloat(f.firstChild.nodeValue));
              m.trans = true
            }break;
          case "color":
            s = f.firstChild.nodeValue.replace(/\s+/g, " ").split(" ");
            s = this.getMaterialAlpha(s, r, 1);
            if(s < 1) {
              m.setAlpha(s);
              m.trans = true
            }break;
          case "param":
            s = this.getFloat4(p, f.getAttribute("ref")).replace(/\s+/g, " ").split(" ");
            s = this.getMaterialAlpha(s, r, 1);
            if(s < 1) {
              m.setAlpha(s);
              m.trans = true
            }break;
          case "texture":
            this.createMaterialLayer(f, m, p, e.M_ALPHA, g);
            m.trans = true;
            break
        }
      }while(f = f.nextSibling)
    }return m
  };
  e.Collada.prototype.getMaterialAlpha = function(f, g, m) {
    var p;
    switch(g) {
      case "A_ONE":
        p = parseFloat(f[3]) * m;
        break;
      case "A_ZERO":
        p = 1 - parseFloat(f[3]) * m;
        break;
      case "RGB_ONE":
        f = parseFloat(f[0]) * 0.212671 + parseFloat(f[1]) * 0.71516 + parseFloat(f[2]) * 0.072169;
        p = f * m;
        break;
      case "RGB_ZERO":
        f = parseFloat(f[0]) * 0.212671 + parseFloat(f[1]) * 0.71516 + parseFloat(f[2]) * 0.072169;
        p = 1 - f * m;
        break
    }
    return p
  };
  e.Collada.prototype.setMaterialOntoMesh = function(f, g) {
    for(var m = g.getElementsByTagName("instance_material"), p = {}, r = 0;r < m.length;r++) {
      for(var s = m[r].getElementsByTagName("bind_vertex_input"), A = {}, v = 0;v < s.length;v++) {
        if(s[v].hasAttribute("input_set")) {
          A[s[v].getAttribute("semantic")] = s[v].getAttribute("input_set")
        }else {
          A[s[v].getAttribute("semantic")] = function(B) {
            for(var C = "", E = B.length - 1;E >= 0;--E) {
              if(B[E] >= "0" && B[E] <= "9") {
                C = B[E] + C
              }
            }if(C.length == 0) {
              return"0"
            }return C
          }(s[v].getAttribute("semantic"))
        }
      }mat = this.getMaterial(m[r].getAttribute("target").substr(1), A);
      p[m[r].getAttribute("symbol")] = mat
    }m = new e.Object;
    for(r = 0;r < f.length;r++) {
      if(p[f[r].matName] && p[f[r].matName].trans) {
        m.setZtransparent(true);
        m.setPickable(false)
      }s = new e.MultiMaterial;
      s.setMesh(f[r]);
      if(!p[f[r].matName]) {
        p[f[r].matName] = new e.Material;
        p[f[r].matName].setColor("lightgrey")
      }s.setMaterial(p[f[r].matName]);
      m.addMultiMaterial(s)
    }m.setSkeleton(this);
    g.GLGEObj = m
  };
  e.Collada.prototype.getInstanceGeometry = function(f) {
    this.setMaterialOntoMesh(this.getMeshes(f.getAttribute("url").substr(1)), f);
    return f.GLGEObj
  };
  e.Collada.prototype.getAnimationSampler = function(f, g) {
    var m = this.xml.getElementById(f).getElementsByTagName("input");
    f = {};
    for(var p = [], r, s, A = 0;A < m.length;A++) {
      r = this.getSource(m[A].getAttribute("source").substr(1));
      s = m[A].getAttribute("semantic");
      p.push({block:s, data:r})
    }for(n = 0;n < p.length;n++) {
      s = p[n].block;
      f[s] = {};
      f[s].data = [];
      f[s].names = [];
      for(k = 0;k < p[n].data.array.length;k += p[n].data.stride) {
        for(A = r = 0;A < p[n].data.pmask.length;A++) {
          if(p[n].data.pmask[A]) {
            f[s].names.push(p[n].data.pmask[A].name);
            if(p[n].data.pmask[A].type == "float4x4") {
              f[s].stride = 16;
              for(m = 0;m < 16;m++) {
                f[s].data.push(p[n].data.array[m + k + p[n].data.offset + A])
              }
            }else {
              r++;
              f[s].stride = r;
              f[s].data.push(p[n].data.array[k + p[n].data.offset + A])
            }
          }
        }
      }
    }s = [];
    for(A = 0;A < f.OUTPUT.stride;A++) {
      s.push(new e.AnimationCurve)
    }for(A = 0;A < f.INPUT.data.length;A++) {
      for(m = 0;m < f.OUTPUT.stride;m++) {
        s[m].name = f.OUTPUT.names[m];
        if(f.INTERPOLATION && f.INTERPOLATION.data[A] == "BEZIER" && !f.IN_TANGENT) {
          f.INTERPOLATION.data[A] = "LINEAR"
        }if(!f.INTERPOLATION || f.INTERPOLATION.data[A] == "LINEAR") {
          p = new e.LinearPoint;
          p.setX(f.INPUT.data[A] * 30);
          r = parseFloat(f.OUTPUT.data[A * f.OUTPUT.stride + m]);
          if(r == -180) {
            r = -179.9
          }if(r == 180) {
            r = 179.9
          }if(this.exceptions.flipangle && g) {
            if(s[m].lastval) {
              if(Math.abs(s[m].lastval - (360 + r)) < Math.abs(s[m].lastval - r)) {
                r = 360 + r
              }else {
                if(Math.abs(s[m].lastval - (r - 360)) < Math.abs(s[m].lastval - r)) {
                  r -= 360
                }
              }
            }
          }p.setY(r);
          s[m].lastval = r;
          s[m].addPoint(p)
        }if(f.INTERPOLATION && f.INTERPOLATION.data[A] == "BEZIER") {
          p = new e.BezTriple;
          p.setX1(f.IN_TANGENT.data[(A * f.OUTPUT.stride + m) * 2] * 30);
          p.setY1(f.IN_TANGENT.data[(A * f.OUTPUT.stride + m) * 2 + 1]);
          p.setX2(Math.round(f.INPUT.data[A] * 30));
          p.setY2(f.OUTPUT.data[A * f.OUTPUT.stride + m]);
          p.setX3(f.OUT_TANGENT.data[(A * f.OUTPUT.stride + m) * 2] * 30);
          p.setY3(f.OUT_TANGENT.data[(A * f.OUTPUT.stride + m) * 2 + 1]);
          s[m].addPoint(p)
        }
      }
    }return s
  };
  e.Collada.prototype.getAnimationVector = function(f) {
    var g = 0, m = this.xml.getElementById(f[0].target[0]).firstChild, p = [], r = {};
    do {
      switch(m.tagName) {
        case "matrix":
        ;
        case "translate":
        ;
        case "rotate":
        ;
        case "scale":
          def = {type:m.tagName, data:this.parseArray(m), animations:[]};
          if(m.hasAttribute("sid")) {
            r[m.getAttribute("sid")] = def
          }p.push(def);
          break
      }
      m = m.nextSibling
    }while(m);
    for(m = 0;m < f.length;m++) {
      var s = f[m].target, A = this.getAnimationSampler(f[m].source, /ANGLE/i.test(s));
      for(v = 0;v < A.length;v++) {
        g = Math.max(g, A[v].keyFrames[A[v].keyFrames.length - 1].x)
      }if(s[1].indexOf(".") != -1) {
        s = s[1].split(".");
        switch(s[1]) {
          case "X":
            r[s[0]].animations[0] = A[0];
            break;
          case "Y":
            r[s[0]].animations[1] = A[0];
            break;
          case "Z":
            r[s[0]].animations[2] = A[0];
            break;
          case "ANGLE":
            r[s[0]].animations[3] = A[0];
            break
        }
      }else {
        if(s[1].indexOf("(") != -1) {
          s = s[1].split("(");
          sidtarget = s.shift();
          s = s.length > 1 ? parseInt(s[0]) + 4 * parseInt(s[1]) : parseInt(s[0]);
          r[sidtarget].animations[s] = A[0]
        }else {
          for(var v = 0;v < A.length;v++) {
            switch(A[v].name) {
              case "X":
                r[s[1]].animations[0] = A[v];
                break;
              case "Y":
                r[s[1]].animations[1] = A[v];
                break;
              case "Z":
                r[s[1]].animations[2] = A[v];
                break;
              case "ANGLE":
                r[s[1]].animations[3] = A[v];
                break;
              default:
                r[s[1]].animations[v] = A[v];
                break
            }
          }
        }
      }
    }f = new e.AnimationVector;
    f.setFrames(g);
    r = new e.AnimationCurve;
    r.setChannel("QuatX");
    A = new e.AnimationCurve;
    A.setChannel("QuatY");
    s = new e.AnimationCurve;
    s.setChannel("QuatZ");
    v = new e.AnimationCurve;
    v.setChannel("QuatW");
    var B = new e.AnimationCurve;
    B.setChannel("LocX");
    var C = new e.AnimationCurve;
    C.setChannel("LocY");
    var E = new e.AnimationCurve;
    E.setChannel("LocZ");
    var H = new e.AnimationCurve;
    H.setChannel("ScaleX");
    var J = new e.AnimationCurve;
    J.setChannel("ScaleY");
    var M = new e.AnimationCurve;
    M.setChannel("ScaleZ");
    f.addAnimationCurve(r);
    f.addAnimationCurve(A);
    f.addAnimationCurve(s);
    f.addAnimationCurve(v);
    f.addAnimationCurve(B);
    f.addAnimationCurve(C);
    f.addAnimationCurve(E);
    f.addAnimationCurve(H);
    f.addAnimationCurve(J);
    f.addAnimationCurve(M);
    for(var K = null, N = 0;N < g;N++) {
      var Q = e.identMatrix();
      for(m = 0;m < p.length;m++) {
        switch(p[m].type) {
          case "matrix":
            var R = [p[m].animations[0] ? p[m].animations[0].getValue(N) : p[m].data[0], p[m].animations[1] ? p[m].animations[1].getValue(N) : p[m].data[1], p[m].animations[2] ? p[m].animations[2].getValue(N) : p[m].data[2], p[m].animations[3] ? p[m].animations[3].getValue(N) : p[m].data[3], p[m].animations[4] ? p[m].animations[4].getValue(N) : p[m].data[4], p[m].animations[5] ? p[m].animations[5].getValue(N) : p[m].data[5], p[m].animations[6] ? p[m].animations[6].getValue(N) : p[m].data[6], p[m].animations[7] ? 
            p[m].animations[7].getValue(N) : p[m].data[7], p[m].animations[8] ? p[m].animations[8].getValue(N) : p[m].data[8], p[m].animations[9] ? p[m].animations[9].getValue(N) : p[m].data[9], p[m].animations[10] ? p[m].animations[10].getValue(N) : p[m].data[10], p[m].animations[11] ? p[m].animations[11].getValue(N) : p[m].data[11], p[m].animations[12] ? p[m].animations[12].getValue(N) : p[m].data[12], p[m].animations[13] ? p[m].animations[13].getValue(N) : p[m].data[13], p[m].animations[14] ? 
            p[m].animations[14].getValue(N) : p[m].data[14], p[m].animations[15] ? p[m].animations[15].getValue(N) : p[m].data[15]];
            Q = e.mulMat4(Q, e.Mat4(R));
            break;
          case "rotate":
            R = [p[m].animations[0] ? p[m].animations[0].getValue(N) : p[m].data[0], p[m].animations[1] ? p[m].animations[1].getValue(N) : p[m].data[1], p[m].animations[2] ? p[m].animations[2].getValue(N) : p[m].data[2], p[m].animations[3] ? p[m].animations[3].getValue(N) : p[m].data[3]];
            Q = e.mulMat4(Q, e.angleAxis(R[3] * 0.017453278, [R[0], R[1], R[2]]));
            break;
          case "translate":
            R = [p[m].animations[0] ? p[m].animations[0].getValue(N) : p[m].data[0], p[m].animations[1] ? p[m].animations[1].getValue(N) : p[m].data[1], p[m].animations[2] ? p[m].animations[2].getValue(N) : p[m].data[2]];
            Q = e.mulMat4(Q, e.translateMatrix(R[0], R[1], R[2]));
            break;
          case "scale":
            R = [p[m].animations[0] ? p[m].animations[0].getValue(N) : p[m].data[0], p[m].animations[1] ? p[m].animations[1].getValue(N) : p[m].data[1], p[m].animations[2] ? p[m].animations[2].getValue(N) : p[m].data[2]];
            Q = e.mulMat4(Q, e.scaleMatrix(R[0], R[1], R[2]));
            break
        }
      }scale = e.matrix2Scale(Q);
      Q = e.mulMat4(Q, e.scaleMatrix(1 / scale[0], 1 / scale[1], 1 / scale[2]));
      quat = e.rotationMatrix2Quat(Q);
      if(K) {
        if(K[0] * quat[0] + K[1] * quat[1] + K[2] * quat[2] + K[3] * quat[3] < 0) {
          quat[0] *= -1;
          quat[1] *= -1;
          quat[2] *= -1;
          quat[3] *= -1
        }
      }K = quat;
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(quat[0]);
      r.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(quat[1]);
      A.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(quat[2]);
      s.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(quat[3]);
      v.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(Q[3]);
      B.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(Q[7]);
      C.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(Q[11]);
      E.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(scale[0].toFixed(4));
      H.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(scale[1].toFixed(4));
      J.addPoint(point);
      point = new e.LinearPoint;
      point.setX(N);
      point.setY(scale[2].toFixed(4));
      M.addPoint(point)
    }return f
  };
  var q = {};
  e.Collada.prototype.getAnimations = function() {
    if(q[this.url]) {
      this.actions = q[this.url]
    }else {
      var f = this.xml.getElementsByTagName("animation_clip"), g = this.xml.getElementsByTagName("animation");
      if(f.length == 0) {
        g.name = "default";
        var m = [g]
      }else {
        m = [];
        for(var p = 0;p < f.length;p++) {
          g = [];
          for(var r = f[p].getElementsByTagName("instance_animation"), s = 0;s < r.length;s++) {
            g.push(this.xml.getElementById(r[s].getAttribute("url").substr(1)))
          }g.name = f[p].getAttribute("id");
          m.push(g)
        }
      }for(f = 0;f < m.length;f++) {
        g = m[f];
        var A, v, B;
        r = {};
        for(p = 0;p < g.length;p++) {
          A = g[p].getElementsByTagName("channel");
          for(s = 0;s < A.length;s++) {
            v = A[s].getAttribute("target").split("/");
            B = A[s].getAttribute("source").substr(1);
            r[v[0]] || (r[v[0]] = []);
            r[v[0]].push({source:B, target:v})
          }
        }s = new e.Action;
        for(v in r) {
          A = this.getAnimationVector(r[v]);
          B = this.xml.getElementById(v);
          for(p = 0;p < B.GLGEObjects.length;p++) {
            var C = new e.ActionChannel, E = B.GLGEObjects[p].getName();
            C.setTarget(E);
            C.setAnimation(A);
            s.addActionChannel(C)
          }
        }this.addColladaAction({name:g.name, action:s})
      }
    }q[this.url] = this.actions;
    for(n in this.actions) {
      this.setAction(this.actions[n], 0, true);
      break
    }
  };
  e.Collada.prototype.addColladaAction = function(f) {
    this.actions[f.name] = f.action
  };
  e.Collada.prototype.getColladaActions = function() {
    return this.actions
  };
  e.Collada.prototype.getInstanceController = function(f) {
    new e.Object;
    var g = this.xml.getElementById(f.getAttribute("url").substr(1)), m = f.getElementsByTagName("skeleton"), p = g.getElementsByTagName("joints")[0], r = p.getElementsByTagName("input"), s;
    s = g.getElementsByTagName("bind_shape_matrix").length > 0 ? this.parseArray(g.getElementsByTagName("bind_shape_matrix")[0]) : e.identMatrix();
    var A = [s];
    p = new e.Group;
    this.addGroup(p);
    p = [p];
    for(var v, B = 0;B < r.length;B++) {
      if(r[B].getAttribute("semantic") == "JOINT") {
        var C = this.getSource(r[B].getAttribute("source").substr(1));
        if(C.type == "IDREF_array") {
          v = C.array.length != 0;
          for(var E = 0;E < C.array.length;E += C.stride) {
            var H = this.getNode(this.xml.getElementById(C.array[E]), true).getName();
            if(this.xml.getElementById(C.array[E])) {
              v = false
            }else {
              e.error("Bone is not specified " + C.array[E]);
              A = [s = e.identMatrix()]
            }p.push(H)
          }if(v) {
            A = [s = e.identMatrix()]
          }
        }else {
          if(C.type == "Name_array") {
            var J = {};
            if(m.length == 0) {
              var M = this.xml.getElementsByTagName("node");
              for(E = 0;E < M.length;E++) {
                if(H = M[E].getAttribute("sid")) {
                  J[H] = M[E]
                }if((H = M[E].getAttribute("name")) && !J[H]) {
                  J[H] = M[E]
                }
              }
            }else {
              for(v = 0;v < m.length;v++) {
                E = this.xml.getElementById(m[v].firstChild.nodeValue.substr(1));
                if(H = E.getAttribute("sid")) {
                  J[H] = E
                }M = E.getElementsByTagName("*");
                for(E = 0;E < M.length;E++) {
                  if(H = M[E].getAttribute("sid")) {
                    J[H] = M[E]
                  }if((H = M[E].getAttribute("name")) && !J[H]) {
                    J[H] = M[E]
                  }
                }
              }
            }for(E = 0;E < C.array.length;E += C.stride) {
              if(C.array[E] != "") {
                H = this.getNode(J[C.array[E]], true).getName();
                p.push(H)
              }
            }
          }
        }
      }
    }for(B = 0;B < r.length;B++) {
      if(r[B].getAttribute("semantic") == "INV_BIND_MATRIX") {
        m = this.getSource(r[B].getAttribute("source").substr(1));
        for(E = 0;E < m.array.length;E += m.stride) {
          v = m.array.slice(E, E + 16);
          A.push(e.mulMat4(e.Mat4(v), e.Mat4(s.slice(0, 16))))
        }
      }
    }B = g.getElementsByTagName("vertex_weights")[0];
    r = B.getElementsByTagName("input");
    s = [];
    m = {};
    for(v = 0;v < r.length;v++) {
      C = r[v].getAttribute("semantic");
      r[v].data = this.getSource(r[v].getAttribute("source").substr(1));
      r[v].block = C;
      m[C] = [];
      E = r[v].getAttribute("offset");
      s[E] || (s[E] = []);
      s[E].push(r[v])
    }r = this.parseArray(B.getElementsByTagName("vcount")[0]);
    J = this.parseArray(B.getElementsByTagName("v")[0]);
    for(B = H = 0;B < r.length;B++) {
      if(r[B]) {
        H = Math.max(H, parseInt(r[B]))
      }
    }for(B = vPointer = 0;B < r.length;B++) {
      for(M = 0;M < r[B];M++) {
        for(E = 0;E < s.length;E++) {
          for(var K = 0;K < s[E].length;++K) {
            C = s[E][K].block;
            for(v = 0;v < s[E][K].data.stride;v++) {
              if(s[E][K].data.pmask[v]) {
                C != "JOINT" ? m[C].push(s[E][K].data.array[parseInt(J[vPointer]) + parseInt(s[E][K].data.offset)]) : m[C].push(parseInt(J[vPointer]));
                vPointer++
              }
            }
          }
        }
      }for(M = M;M < H;M++) {
        for(E = 0;E < s.length;E++) {
          for(K = 0;K < s[E].length;++K) {
            C = s[E][K].block;
            m[C].push(0)
          }
        }
      }
    }if(!this.badAccessor && m.JOINT.length == 0) {
      this.badAccessor = true;
      return this.getInstanceController(f)
    }for(B = 0;B < m.JOINT.length;B++) {
      m.JOINT[B]++
    }if(this.exceptions.negjoints) {
      for(B = 0;B < m.JOINT.length;B++) {
        if(m.JOINT[B] == 0) {
          m.WEIGHT[B] = 0
        }
      }
    }A = {vertexJoints:m.JOINT, vertexWeight:m.WEIGHT, joints:p, inverseBindMatrix:A, count:H};
    this.setMaterialOntoMesh(this.getMeshes(g.getElementsByTagName("skin")[0].getAttribute("source").substr(1), A), f);
    return f.GLGEObj
  };
  e.Collada.prototype.getNode = function(f, g) {
    if(!g && f.GLGEObject) {
      m = f.GLGEObject;
      delete this.GLGEObject;
      return m
    }if(g && f && f.GLGEObjects) {
      return f.GLGEObjects[0]
    }var m = new e.Group, p = "bone" + ++this.boneIdx;
    m.setName(p);
    if(!f) {
      return m
    }if(!f.GLGEObjects) {
      f.GLGEObjects = []
    }f.GLGEObjects.push(m);
    p = f.firstChild;
    var r = e.identMatrix(), s;
    if(p) {
      do {
        switch(p.tagName) {
          case "node":
            m.addGroup(this.getNode(p));
            break;
          case "instance_node":
            m.addGroup(this.getNode(this.xml.getElementById(p.getAttribute("url").substr(1))));
            break;
          case "instance_visual_scene":
            m.addGroup(this.getNode(this.xml.getElementById(p.getAttribute("url").substr(1))));
            break;
          case "instance_geometry":
            m.addObject(this.getInstanceGeometry(p));
            break;
          case "instance_controller":
            m.addObject(this.getInstanceController(p));
            break;
          case "matrix":
            r = this.parseArray(p);
            break;
          case "translate":
            s = this.parseArray(p);
            r = e.mulMat4(r, e.translateMatrix(s[0], s[1], s[2]));
            break;
          case "rotate":
            s = this.parseArray(p);
            r = e.mulMat4(r, e.angleAxis(s[3] * 0.017453278, [s[0], s[1], s[2]]));
            break;
          case "scale":
            s = this.parseArray(p);
            r = e.mulMat4(r, e.scaleMatrix(s[0], s[1], s[2]));
            break
        }
      }while(p = p.nextSibling)
    }m.setLoc(r[3], r[7], r[11]);
    p = e.Mat4([r[0], r[1], r[2], 0, r[4], r[5], r[6], 0, r[8], r[9], r[10], 0, 0, 0, 0, 1]);
    m.setRotMatrix(p);
    if(g) {
      f.GLGEObject = m
    }return m
  };
  e.Collada.prototype.initVisualScene = function() {
    var f = this.xml.getElementsByTagName("asset"), g = "Z_UP";
    if(f.length) {
      f = f[0].getElementsByTagName("up_axis");
      if(f.length) {
        f = f[0];
        f = f.firstChild.nodeValue;
        if(f.length) {
          g = f
        }
      }
    }f = this;
    if(g[0] != "Y" && g[0] != "y") {
      f = new e.Group;
      this.addChild(f);
      g[0] != "Z" && g[0] != "z" ? this.setRotMatrix(e.Mat4([0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])) : this.setRotMatrix(e.Mat4([1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1]))
    }if(this.rootId) {
      (g = this.xml.getElementById(this.rootId)) ? f.addGroup(this.getNode(g)) : e.error("Asset " + this.rootId + " not found in document" + this.url)
    }else {
      g = this.xml.getElementsByTagName("scene");
      g.length > 0 ? f.addGroup(this.getNode(g[0])) : e.error("Please indicate the asset to render in Collada Document" + this.url)
    }
  };
  var u = {"default":{}, "COLLADA Mixamo exporter":{badAccessor:true}, "Blender2.5":{flipangle:true, negjoints:true}};
  e.Collada.prototype.getExceptions = function() {
    if(this.xml.getElementsByTagName("authoring_tool").length > 0 && this.xml.getElementsByTagName("authoring_tool")[0].firstChild.nodeValue == "COLLADA Mixamo exporter") {
      return u["COLLADA Mixamo exporter"]
    }if(this.xml.getElementsByTagName("authoring_tool").length > 0 && /Blender 2.5/.test(this.xml.getElementsByTagName("authoring_tool")[0].firstChild.nodeValue)) {
      return u["Blender2.5"]
    }
  };
  e.Collada.prototype.loaded = function(f, g) {
    this.xml = g;
    if(g.getElementsByTagName("authoring_tool").length > 0) {
      this.exceptions = u[g.getElementsByTagName("authoring_tool")[0].firstChild.nodeValue]
    }this.exceptions = this.getExceptions();
    if(!this.exceptions) {
      this.exceptions = u["default"]
    }this.initVisualScene();
    this.getAnimations();
    this.loadedCallback && this.loadedCallback(this);
    this.fireEvent("loaded", {url:this.url})
  };
  e.Scene.prototype.addCollada = e.Scene.prototype.addGroup;
  e.Group.prototype.addCollada = e.Group.prototype.addGroup;
  if(e.Document) {
    e.Document.prototype.getCollada = function(f) {
      if(!f.object) {
        f.object = new (e[this.classString(f.tagName)]);
        f.object.setDocument(f.getAttribute("document"), this.getAbsolutePath(this.rootURL, null));
        f.removeAttribute("document");
        this.setProperties(f)
      }return f.object
    }
  }
})(GLGE);if(typeof WebGLUnsignedByteArray === "undefined" && typeof Uint8Array !== "undefined") {
  var WebGLUnsignedByteArray = Uint8Array
}if(typeof WebGLByteArray === "undefined" && typeof Int8Array !== "undefined") {
  var WebGLByteArray = Int8Array
}if(typeof WebGLUnsignedShortArray === "undefined" && typeof Uint16Array !== "undefined") {
  var WebGLUnsignedShortArray = Uint16Array
}if(typeof WebGLShortArray === "undefined" && typeof Int16Array !== "undefined") {
  var WebGLShortArray = Int16Array
}if(typeof WebGLUnsignedIntArray === "undefined" && typeof Uint32Array !== "undefined") {
  var WebGLUnsignedIntArray = Uint32Array
}if(typeof WebGLIntArray === "undefined" && typeof Int32Array !== "undefined") {
  var WebGLIntArray = Int32Array
}if(typeof WebGLFloatArray === "undefined" && typeof Float32Array !== "undefined") {
  var WebGLFloatArray = Float32Array
}if(typeof WebGLDoubleArray === "undefined" && typeof Float64Array !== "undefined") {
  var WebGLDoubleArray = Float64Array
};var GLGEGraphics = function(e, j) {
  function h() {
    q._mouseMoveSinceLastRender = false;
    q.mCurTime = new Date;
    var r = parseInt(q.mCurTime.getTime());
    p = Math.round((p * 9 + 1E3 / (r - m)) / 10);
    for(var s in q.mObjectUpdates) {
      q.mObjectUpdates[s].update(q);
      q.newEvents = true
    }if(!q.newEvents) {
      for(animObject in q.mAnimatingObjects) {
        q.newEvents = q.newEvents || q.windowVisible;
        break
      }
    }if(q.doubleBuffer && !q.newEvents) {
      q.doubleBuffer = false;
      q.renderer.render()
    }else {
      if(q.newEvents || q.doubleBuffer) {
        q.renderer.render();
        q.newEvents = false;
        q.doubleBuffer = true
      }
    }m = r;
    Kata.userRenderCallback && Kata.userRenderCallback(q.mCurTime)
  }
  function o() {
    var r = false;
    for(animObject in q.mAnimatingObjects) {
      r = true;
      break
    }q.doubleBuffer = !r
  }
  this.mCurTime = new Date;
  this.callback = e;
  this.newEvents = true;
  this.doubleBuffer = false;
  this.mAnimatingObjects = {};
  this.windowVisible = true;
  var q = this, u, f;
  if(u = document.createElement("canvas")) {
    try {
      f = u.getContext("experimental-webgl", {})
    }catch(g) {
      typeof globalNoWebGLError != "undefined" && globalNoWebGLError()
    }
  }if(!u || !f) {
    typeof globalNoWebGLError != "undefined" && globalNoWebGLError()
  }u.style.width = "100%";
  u.style.height = "100%";
  j.appendChild(u);
  if(u) {
    e = function() {
      var r = Math.max(1, u.clientWidth), s = Math.max(1, u.clientHeight);
      u.width = r;
      u.height = s;
      GLGEGraphics.canvasAspect = r / s;
      q.mCamera && q.mCamera.setAspect(GLGEGraphics.canvasAspect);
      u.sizeInitialized_ = true;
      q.displayInfo = {width:u.width, height:u.height};
      q.newEvents = true
    };
    this.renderer = new GLGE.Renderer(u);
    this.renderer.cullFaces = true;
    window.addEventListener("resize", e, false);
    setTimeout(e, 0)
  }else {
    this.webGlCanvasError(j, "HTMLCanvas")
  }this.mClientElement = u;
  var m = 0, p = 60;
  this.mCurTime = new Date;
  this.mObjectUpdates = {};
  this.mSpaceRoots = {};
  this.mRenderTargets = {};
  this.mUnsetParents = {};
  this.mObjects = {};
  this._keyDownMap = {};
  this._enabledEvents = {};
  this._lastMouseDown = null;
  this._mouseMoveSinceLastRender = false;
  setInterval(o, 533);
  setInterval(h, 16);
  window.addEventListener("focus", function() {
    q.windowVisible = true
  }, false);
  window.addEventListener("blur", function() {
    q.windowVisible = false
  }, false);
  u.addEventListener("mousedown", function(r) {
    q._mouseDown(r)
  }, true);
  u.addEventListener("mouseup", function(r) {
    q._mouseUp(r)
  }, true);
  u.addEventListener("mousemove", function(r) {
    q._mouseMove(r)
  }, true);
  document.addEventListener("keydown", function(r) {
    q._keyDown(r)
  }, true);
  document.addEventListener("keyup", function(r) {
    q._keyUp(r)
  }, true);
  u.addEventListener("mousewheel", function(r) {
    q._scrollWheel(r)
  }, true);
  u.addEventListener("DOMMouseScroll", function(r) {
    q._scrollWheel(r)
  }, true);
  u.addEventListener("contextmenu", function(r) {
    if(r.preventDefault) {
      r.preventDefault()
    }else {
      r.returnValue = false
    }return false
  }, true)
};
Kata.require(["katajs/oh/GraphicsSimulation.js", ["katajs/gfx/WebGLCompat.js", "externals/GLGE/glge_math.js", "externals/GLGE/glge.js", "externals/GLGE/glge_collada.js"]], function() {
  function e(f, g, m) {
    this.mGraphicsSystem = f;
    this.mCanvas = g;
    this.mTextureCanvas = m;
    this.mSpaceRoot = this.mCamera = this.mTextureCamera = null
  }
  function j(f, g, m, p) {
    this.mID = f;
    this.mSpaceID = m;
    this.mNode = new GLGE.Group(f);
    this.mLabel = this.mMesh = null;
    this.mCurLocation = Kata.LocationIdentity(new Date(0));
    this.mPrevLocation = Kata.LocationIdentity(new Date(0));
    this.mNode.mKataObject = this;
    this.update = this.updateTransformation;
    this.mParent = null;
    p.mScene.addChild(this.mNode);
    this.mLoaded = false
  }
  function h(f, g, m) {
    this.mElement = g;
    this.mScene = g_GLGE_doc.getElement("mainscene");
    this.mScene.mSpaceID = m;
    this.mDefaultRenderView = new e(f, g, null)
  }
  function o(f) {
    var g = {};
    for(var m in f) {
      if(m != "charCode" && m.toUpperCase() != m) {
        if(typeof f[m] == "number" || typeof f[m] == "string") {
          g[m] = f[m]
        }
      }
    }return g
  }
  function q(f, g) {
    for(f = [];g != null;) {
      f.push([g.mPrevLocation, g.mPrevLocation]);
      g = g.mParent
    }return f
  }
  GLGEGraphics.initialize = function(f, g) {
    g_GLGE_doc = new GLGE.Document;
    g_GLGE_doc.onLoad = g;
    g_GLGE_doc.load(f)
  };
  e.prototype.attachScene = function(f, g) {
    this.mSpaceRoot = f;
    if(this.mTextureCamera == null) {
      this.mGraphicsSystem.renderer.setScene(f.mScene);
      f.mScene.setCamera(g)
    }else {
      console.log("Do not know how to deal with texture camera")
    }
  };
  e.prototype.detachScene = function() {
    if(this.mTextureCamera == null) {
      this.mSpaceRoot.mScene.setCamera(null);
      this.mGraphicsSystem.setScene(null)
    }else {
      console.log("Do not know how to deal with texture camera")
    }this.mSpaceRoot = null
  };
  j.prototype.createMesh = function(f, g, m, p, r) {
    if(g == null) {
      throw"loadScene with null path";
    }if(g.lastIndexOf(".dae") == -1) {
      g += ".dae"
    }if(p === undefined || p === null) {
      p = [0, 0, 0]
    }console.log("Loading: " + g);
    this.mMeshURI = g;
    var s = this, A = new GLGE.Collada;
    this.mID in f.mAnimatingObjects && delete f.mAnimatingObjects[s.mID];
    var v;
    v = function() {
      function B(J) {
        if(J.getAnimation()) {
          return true
        }var M, K;
        if(J.children) {
          for(K = 0;K < J.children.length;++K) {
            M = J.children[K];
            if(B(M)) {
              return true
            }
          }
        }return false
      }
      var C = A.getBoundingVolume(true), E = C.radius, H = 1 / E;
      A.setScaleX(E ? r[0] * H : 1);
      A.setScaleY(E ? r[1] * H : 1);
      A.setScaleZ(E ? r[2] * H : 1);
      A.setLocX(p[0] - C.center[0] * H);
      A.setLocY(p[1] - C.center[1] * H);
      A.setLocZ(p[2] - C.center[2] * H);
      f._inputCb({msg:"loaded", id:s.mID});
      A.removeEventListener("loaded", v);
      s.mLoaded = true;
      s.newEvents = true;
      if(s.mCurAnimation) {
        C = s.mCurAnimation;
        s.mCurAnimation = "";
        s.animate(C)
      }if(B(A)) {
        f.mAnimatingObjects[s.mID] = s.mNode;
        setTimeout(function() {
          f.newEvents = true
        }, 8E3);
        setTimeout(function() {
          f.newEvents = true
        }, 4E3)
      }
    };
    A.addEventListener("loaded", v);
    A.setDocument(this.mMeshURI);
    r || (r = [1, 1, 1]);
    A.setScaleX(r[0]);
    A.setScaleY(r[1]);
    A.setScaleZ(r[2]);
    A.setQuatX(0);
    A.setQuatY(0);
    A.setQuatZ(0);
    A.setQuatW(1);
    if(p) {
      A.setLocX(p[0]);
      A.setLocY(p[1]);
      A.setLocZ(p[2])
    }this.mNode.addCollada(A);
    return this.mMesh = A
  };
  j.prototype.createCamera = function(f, g, m) {
    this.mFOV = f;
    this.mCamera = new GLGE.Camera(this.mID + "C");
    this.mCamera.setFovY(f * GLGEGraphics.canvasAspect);
    this.mCamera.setNear(g);
    this.mCamera.setFar(m);
    GLGEGraphics.canvasAspect && this.mCamera.setAspect(GLGEGraphics.canvasAspect);
    this.mNode.addChild(this.mCamera);
    this.update = this.updateCamera
  };
  j.prototype.destroyCamera = function() {
    this.detachRenderTarget();
    delete this.mFOV;
    this.mNode.removeChild(this.mCamera);
    delete this.mCamera;
    this.update = this.updateTransformation
  };
  j.prototype.attachRenderTarget = function(f, g) {
    f.mCamera && f.mCamera.detachRenderTarget();
    this.detachRenderTarget();
    this.mRenderTarg = f;
    f.mCamera = this;
    f.attachScene(g, this.mCamera);
    this.update(f.mGraphicsSystem)
  };
  j.prototype.detachRenderTarget = function() {
    if(this.mRenderTarg) {
      var f = this.mRenderTarg.mO3DGraphics;
      this.mRenderTarg.detatchScene();
      this.mRenderTarg.mCamera = null;
      this.mRenderTarg.mSpaceRoot = null;
      delete this.mRenderTarg;
      this.update(f)
    }
  };
  j.prototype.stationary = function(f) {
    var g = this.mCurLocation.vel, m = this.mCurLocation.rotvel;
    return g[0] == 0 && g[1] == 0 && g[2] == 0 && m == 0 && f - this.mCurLocation.scaleTime >= 0 && f - this.mCurLocation.posTime >= 0 && f - this.mCurLocation.orientTime >= 0
  };
  j.prototype.updateTransformation = function(f) {
    var g = Kata.LocationExtrapolate(this.mCurLocation, f.mCurTime);
    this.mNode.setLoc(g.pos[0], g.pos[1], g.pos[2]);
    this.mCamera || this.mNode.setScale(g.scale[0], g.scale[1], g.scale[2]);
    this.mNode.setQuat(g.orient[0], g.orient[1], g.orient[2], g.orient[3]);
    this.stationary(f.mCurTime) && f.removeObjectUpdate(this);
    return g
  };
  j.prototype.updateCamera = function(f) {
    this.updateTransformation(f, true)
  };
  j.prototype.animate = function(f) {
    var g = this.mMesh;
    g || Kata.warn("Couldn't handle animate request.");
    if(f != this.mCurAnimation) {
      var m = g.getColladaActions()[f];
      if(m) {
        this.mCurAnimation = f;
        g.setAction(m, 400, true)
      }else {
        if(!this.mLoaded) {
          this.mCurAnimation = f
        }
      }
    }
  };
  j.prototype.label = function(f, g) {
    var m = this.mLabel;
    if(m === null) {
      this.mLabel = m = new GLGE.Text;
      m.multimaterials = [new GLGE.MultiMaterial];
      var p = new GLGE.Material;
      m.multimaterials[0].setMaterial(p);
      this.mNode.addChild(m)
    }if(g === undefined) {
      g = [0, 0, 0]
    }m.setScaleX(0.1);
    m.setScaleY(0.1);
    m.setScaleZ(0.1);
    m.setQuatX(0);
    m.setQuatY(0);
    m.setQuatZ(0);
    m.setQuatW(1);
    m.setLocX(g[0]);
    m.setLocY(g[1]);
    m.setLocZ(g[2]);
    m.setColor({r:0, g:0, b:0});
    m.setSize(200);
    m.setText(f)
  };
  GLGEGraphics.prototype.methodTable = {};
  GLGEGraphics.prototype.addObjectUpdate = function(f) {
    this.mObjectUpdates[f.mID] = f
  };
  GLGEGraphics.prototype.removeObjectUpdate = function(f) {
    delete this.mObjectUpdates[f.mID]
  };
  GLGEGraphics.prototype.send = function(f) {
    if(f.msg != "Custom") {
      this.methodTable[f.msg].call(this, f);
      this.newEvents = true
    }
  };
  GLGEGraphics.prototype.setInputCallback = function(f) {
    this._inputCb = f
  };
  GLGEGraphics.prototype._extractMouseEventInfo = function(f, g) {
    f = {msg:g || f.type, event:o(f), shiftKey:f.shiftKey, altKey:f.altKey, ctrlKey:f.ctrlKey, button:f.button, x:f.clientX, y:f.clientY, camerapos:null, dir:null, spaceid:null, clientX:f.clientX, clientY:f.clientY, width:0, height:0};
    g = this.mClientElement;
    f.width = g.width;
    for(f.height = g.height;g != null;) {
      f.x += g.scrollLeft || 0;
      f.y += g.scrollTop || 0;
      f.x -= g.offsetLeft || 0;
      f.y -= g.offsetTop || 0;
      g = g == document.body && !g.offsetParent ? document.documentElement : g.offsetParent
    }if(g = this.renderer && this.renderer.getScene()) {
      var m = g.makeRay(f.x, f.y);
      if(m) {
        f.camerapos = m.origin;
        f.dir = m.coord
      }f.spaceid = g.mSpaceID
    }return f
  };
  GLGEGraphics.prototype._rayTrace = function(f, g, m) {
    var p = this.renderer.getScene();
    for(g = (f = p.ray(f, g)) && f.object;g && !g.mKataObject;) {
      g = g.parent
    }(g = g && g.mKataObject && g.mKataObject.mID) || (g = null);
    m.spaceid = p.mSpaceID;
    m.id = g;
    m.pos = f && f.coord;
    m.normal = f && f.normal;
    return m.id && true || false
  };
  GLGEGraphics.prototype._mouseDown = function(f) {
    var g = this._extractMouseEventInfo(f);
    this._buttonState |= 1 << g.button;
    this._lastMouseDown = g;
    if(g.button == 2) {
      document.body.style.cursor = "crosshair"
    }this._inputCb(g);
    var m = this, p = function(s) {
      m._mouseMove(s)
    }, r = function(s) {
      m._mouseUp(s);
      document.removeEventListener("mouseup", r, true);
      document.removeEventListener("mousemove", p, true)
    };
    document.addEventListener("mouseup", r, true);
    document.addEventListener("mousemove", p, true);
    if(this._enabledEvents.pick) {
      g = this._extractMouseEventInfo(f, "pick");
      this._rayTrace(g.camerapos, g.dir, g);
      this._inputCb(g)
    }window.focus();
    f.target.focus();
    f.preventDefault && f.preventDefault()
  };
  var u = Kata.GraphicsSimulation.DRAG_THRESHOLD;
  GLGEGraphics.prototype._mouseUp = function(f) {
    var g = this._extractMouseEventInfo(f);
    this._buttonState &= ~(1 << g.button);
    if(g.button == 2) {
      document.body.style.cursor = "default"
    }this._inputCb(g);
    var m = this._lastMouseDown;
    if(m) {
      var p = g.x - m.x, r = g.y - m.y;
      if(m.dragging || p < -u || p > u || r < -u || r > u) {
        g = this._extractMouseEventInfo(f, "drop");
        g.dx = p;
        g.dy = r
      }else {
        g = this._extractMouseEventInfo(f, "click")
      }this._inputCb(g)
    }
  };
  GLGEGraphics.prototype._mouseMove = function(f) {
    var g = this._extractMouseEventInfo(f);
    if(!this._mouseMoveSinceLastRender) {
      this._mouseMoveSinceLastRender = true;
      this._enabledEvents.mousemove && this._inputCb(g);
      if(this._buttonState) {
        var m = this._lastMouseDown;
        if(m) {
          var p = g.x - m.x, r = g.y - m.y;
          if(m.dragging || p < -u || p > u || r < -u || r > u) {
            m.dragging = true;
            if(this._enabledEvents.drag) {
              g = this._extractMouseEventInfo(f, "drag");
              g.dx = p;
              g.dy = r;
              g.button = m.button;
              this._inputCb(g)
            }
          }
        }
      }
    }
  };
  GLGEGraphics.prototype._keyDown = function(f) {
    if(!Kata.suppressCanvasKeyInput) {
      var g = {msg:"keydown", event:o(f), repeat:!!this._keyDownMap[f.keyCode], keyCode:f.keyCode, shiftKey:f.shiftKey, altKey:f.altKey, ctrlKey:f.ctrlKey};
      this._keyDownMap[f.keyCode] = -1;
      this._inputCb(g)
    }
  };
  GLGEGraphics.prototype._keyUp = function(f) {
    if(this._keyDownMap[f.keyCode]) {
      var g = {msg:"keyup", event:o(f), keyCode:f.keyCode, shiftKey:f.shiftKey, altKey:f.altKey, ctrlKey:f.ctrlKey}, m = this;
      this._keyDownMap[f.keyCode] = 1;
      setTimeout(function() {
        if(m._keyDownMap[f.keyCode] == 1) {
          m._keyDownMap[f.keyCode] = 0;
          m._inputCb(g)
        }
      }, 50)
    }
  };
  GLGEGraphics.prototype._scrollWheel = function(f) {
    var g = {msg:"wheel", event:o(f), shiftKey:f.shiftKey, altKey:f.altKey, ctrlKey:f.ctrlKey, dy:0, dx:0};
    if(f.wheelDeltaX || f.wheelDeltaY) {
      g.dy = f.wheelDeltaY || 0;
      g.dx = -f.wheelDeltaX || 0
    }else {
      if(f.wheelDelta) {
        g.dy = f.wheelDelta
      }else {
        if(f.detail) {
          if(f.axis == 1) {
            g.dx = f.detail * 40
          }else {
            g.dy = f.detail * -40
          }
        }
      }
    }this._inputCb(g)
  };
  GLGEGraphics.prototype.methodTable.Create = function(f) {
    var g = f.spaceid;
    g || (g = "");
    if(!(g in this.mSpaceRoots)) {
      var m = new h(this, this.mClientElement, g);
      this.mSpaceRoots[g] = m;
      for(var p in this.mSpaceRoots) {
        break
      }
    }this.mObjects[f.id] = g = new j(f.id, f.time, f.spaceid, this.mSpaceRoots[g]);
    this.moveTo(g, f);
    g.updateTransformation(this);
    if(f.id in this.mUnsetParents) {
      f = this.mUnsetParents[f.id];
      m = f.length;
      for(p = 0;p < m;++p) {
        g.mNode.addChild(f[p].mNode);
        delete f[p].mUnsetParent
      }
    }
  };
  GLGEGraphics.prototype.moveTo = function(f, g) {
    if(!g.time) {
      g.time = (new Date).getTime()
    }var m = f.mParent, p = null, r = null, s = null;
    p = m == null ? this.mSpaceRoots[f.mSpaceID].mScene : m.mNode;
    if(g.parent !== undefined) {
      if(f.mUnsetParent) {
        delete this.mUnsetParents[f.mUnsetParent][g.id];
        delete f.mUnsetParent
      }if(g.parent) {
        if(g.parent in this.mObjects) {
          var A = this.mObjects[g.parent], v = A.mNode;
          if(A != f.mParent) {
            p.removeChild(f.mNode);
            f.mParent = A;
            v.addChild(f.mNode);
            r = A;
            s = v
          }
        }else {
          g.parent in this.mUnsetParents || (this.mUnsetParents[g.parent] = {});
          this.mUnsetParents[g.parent][g.id] = f;
          f.mUnsetParent = g.parent;
          r = this.mSpaceRoots[f.mSpaceID];
          if(f.mParent) {
            f.mParent.mNode.removeChild(f.mNode);
            r.mScene.addChild(f.mNode);
            f.mParent = null
          }r = null;
          s = this.mSpaceRoots[f.mSpaceID].mScene
        }
      }else {
        if(f.mParent) {
          p.removeChild(f.mNode);
          r = null;
          s = this.mSpaceRoots[f.mSpaceID].mScene;
          s.addChild(f.mNode);
          f.mParent = null
        }
      }q(this, m);
      q(this, r);
      f.mPrevLocation = Kata.LocationReparent(f.mPrevLocation, p, s);
      f.mCurLocation = Kata.LocationReparent(f.mCurLocation, p, s)
    }g = Kata.LocationUpdate(g, f.mCurLocation, f.mPrevLocation, g.time || this.mCurTime);
    f.mPrevLocation = f.mCurLocation;
    f.mCurLocation = g;
    f.stationary(this.mCurTime) || this.addObjectUpdate(f)
  };
  GLGEGraphics.prototype.methodTable.Move = function(f) {
    var g = this.mObjects[f.id];
    this.moveTo(g, f);
    g.update(this)
  };
  GLGEGraphics.prototype.methodTable.Animate = function(f) {
    this.mObjects[f.id].animate(f.animation)
  };
  GLGEGraphics.prototype.methodTable.Label = function(f) {
    var g = this.mObjects[f.id];
    g && g.label(f.label, f.offset)
  };
  GLGEGraphics.prototype.methodTable.Destroy = function(f) {
    f.id in this.mAnimatingObjects && delete this.mAnimatingObjects[f.id];
    if(f.id in this.mObjects) {
      for(var g = this.mObjects[f.id], m = g.mNode.getChildren(), p = 0;p < m.length;++p) {
        f.id in this.mUnsetParents || (this.mUnsetParents[f.id] = {});
        var r = m[p].mKataObject;
        if(r) {
          this.mUnsetParents[f.id][r.mID] = r;
          r.mUnsetParent = f.id;
          r.mParent = null;
          var s = this.mSpaceRoots[m[p].mKataObject.mSpaceId], A = q(this, g), v = q(this, null);
          r.mPrevLocation = Kata.LocationReparent(r.mPrevLocation, A, v);
          r.mCurLocation = Kata.LocationReparent(r.mCurLocation, A, v);
          g.mNode.removeChild(m[p]);
          s.mScene.addChild(m[p])
        }
      }this.mSpaceRoots[f.space].mScene.removeChild(g.mNode);
      delete this.mObjects[f.id]
    }
  };
  GLGEGraphics.prototype.methodTable.MeshShaderUniform = function() {
  };
  GLGEGraphics.prototype.methodTable.Mesh = function(f) {
    if(f.mesh && f.id in this.mObjects) {
      var g = this.mObjects[f.id];
      g.createMesh(this, f.mesh, f.anim, f.center ? [-f.center[0], -f.center[1], -f.center[2]] : null, f.scale, f.bounds);
      g.update(this)
    }
  };
  GLGEGraphics.prototype.methodTable.DestroyMesh = function(f) {
    f.id in this.mObjects && this.mObjects[f.id].destroyMesh()
  };
  GLGEGraphics.prototype.methodTable.Light = function() {
  };
  GLGEGraphics.prototype.methodTable.DestroyLight = function() {
  };
  GLGEGraphics.prototype.methodTable.Camera = function(f) {
    if(f.id in this.mObjects) {
      f = this.mObjects[f.id];
      f.createCamera(Kata.GraphicsSimulation.YFOV_DEGREES, Kata.GraphicsSimulation.CAMERA_NEAR, Kata.GraphicsSimulation.CAMERA_FAR);
      this.mCamera = f.mCamera
    }
  };
  GLGEGraphics.prototype.methodTable.AttachCamera = function(f) {
    var g;
    if(f.id in this.mObjects && f.target !== undefined) {
      var m = this.mObjects[f.id], p;
      if(m.mSpaceID in this.mSpaceRoots) {
        p = this.mSpaceRoots[m.mSpaceID]
      }else {
        p = new h(this, this.mClientElement);
        this.mSpaceRoots[m.mSpaceID] = p
      }g = this.mRenderTargets[f.target];
      if(!g) {
        g = new e(this, this.mClientElement, null);
        this.mRenderTargets[f.target] = g
      }m.mCamera && m.attachRenderTarget(g, p)
    }
  };
  GLGEGraphics.prototype.methodTable.DetachCamera = function(f) {
    f.id in this.mObjects && this.mObjects[f.id].detachRenderTarget(this.mCurTime)
  };
  GLGEGraphics.prototype.methodTable.DestroyCamera = function(f) {
    f.id in this.mObjects && this.mObjects[f.id].destroyCamera()
  };
  GLGEGraphics.prototype.methodTable.Enable = function(f) {
    if(f.type) {
      this._enabledEvents[f.type] = true
    }
  };
  GLGEGraphics.prototype.methodTable.Disable = function(f) {
    this._enabledEvents[f.type] && delete this._enabledEvents[f.type]
  };
  GLGEGraphics.prototype.methodTable.IFrame = function() {
  };
  GLGEGraphics.prototype.methodTable.DestroyIFrame = function() {
  };
  GLGEGraphics.prototype.methodTable.CaptureCanvas = function(f) {
    try {
      f = {msg:"canvasCapture", img:this.mClientElement.toDataURL()}
    }catch(g) {
      f = {msg:"canvasCapture", img:""}
    }this._inputCb(f)
  };
  Kata.GraphicsSimulation.registerDriver("GLGE", GLGEGraphics)
}, "katajs/gfx/glgegfx.js");TextGraphics = function(e, j) {
  var h = this;
  this.callback = e;
  this.parent = j;
  this.methodTable = {};
  var o = function(f) {
    if(document.getElementById) {
      var g = document.getElementById(f)
    }else {
      if(document.all) {
        g = document.all[f]
      }else {
        if(document.layers) {
          g = document.layers[f]
        }
      }
    }return g
  };
  this.methodTable.Create = function(f) {
    var g = document.createElement("div");
    g.style.padding = "0.0em";
    g.style.position = "absolute";
    g.style.border = "solid 10px #10107c";
    g.style.backgroundColor = "#000008";
    g.style.width = "300px";
    g.style.height = "300px";
    g.style.color = "#ffffff";
    g.style.left = "0px";
    g.style.top = "0px";
    g.style.zIndex = "1";
    g.id = f.id;
    if(f.parent) {
      (element = o(f.parent)) ? element.appendChild(g) : j.appendChild(g)
    }else {
      j.appendChild(g)
    }g.innerHTML = '<p class="alignleft">Object Properties</p>';
    h.methodTable.Move(f)
  };
  this.methodTable.Move = function(f) {
    element = o(f.id);
    if(f.pos && f.pos.length == 3) {
      element.style.left = f.pos[0] * 10 + "px";
      element.style.top = f.pos[1] * 10 + "px";
      element.style.zIndex = f.pos[2];
      element.style.borderColor = "rgb(" + f.pos[2] * 10 + "," + f.pos[2] * 10 + ",124)"
    }if(f.scale) {
      var g = Math.sqrt(f.scale[0] * f.scale[0] + f.scale[1] * f.scale[1]);
      f = Math.sqrt(f.scale[0] * f.scale[0] + f.scale[2] * f.scale[2]);
      element.style.width = 300 * g + "px";
      element.style.height = 300 * f + "px"
    }
  };
  this.methodTable.Destroy = function(f) {
    (f = o(f.id)) && f.parentNode.removeChild(f)
  };
  var q = function(f) {
    var g = o(f);
    if(!g) {
      g = document.createElement("p");
      g.id = f
    }return g
  };
  this.methodTable.MeshShaderUniform = function(f) {
    var g = o(f.id);
    if(g) {
      var m = q("Uniform" + f.name + f.id);
      m.innerHTML = "Uniform " + f.name + "=" + f.value;
      g.appendChild(m)
    }
  };
  this.methodTable.Mesh = function(f) {
    var g = o(f.id);
    if(g) {
      var m = q("Mesh" + f.id);
      m.innerHTML = "Mesh " + f.mesh;
      g.appendChild(m)
    }
  };
  var u = function(f, g) {
    var m = o(f.id);
    if(m) {
      (f = o(g + f.id)) && m.removeChild(f)
    }
  };
  this.methodTable.DestroyMesh = function(f) {
    u(f, "Mesh")
  };
  this.methodTable.Light = function(f) {
    var g = o(f.id);
    if(g) {
      var m = q("Light" + f.id);
      m.innerHTML = "Light " + f.type;
      g.appendChild(m)
    }
  };
  this.methodTable.DestroyLight = function(f) {
    u(f, "Light")
  };
  this.methodTable.Camera = function(f) {
    var g = o(f.id);
    if(g) {
      var m = q("Camera" + f.id);
      m.innerHTML = "Camera " + f.primary;
      g.appendChild(m)
    }
  };
  this.methodTable.AttachCamera = function(f) {
    if(f.id) {
      var g = o(f.id);
      if(g) {
        var m = q(f.texname + "CameraAttachment" + f.id);
        m.innerHTML = "Camera " + f.camid + " attached to texture " + f.texname;
        g.appendChild(m)
      }
    }else {
      u(f, f.texname + "CameraAttachment")
    }
  };
  this.methodTable.DestroyCamera = function(f) {
    u(f, "Camera")
  };
  this.methodTable.IFrame = function(f) {
    var g = o(f.id);
    if(g) {
      var m = o("IFrame" + f.id);
      if(!m) {
        m = document.createElement("iframe");
        m.id = "IFrame" + f.id
      }m.setAttribute("src", f.uri);
      g.appendChild(m)
    }
  };
  this.methodTable.DestroyIFrame = function(f) {
    u(f, "IFrame")
  };
  this._testInputCounter = 0;
  this.send = function(f) {
    if(f.msg == "Create" || f.msg == "Camera" || f.msg == "AttachCamera") {
      console.log("ENVJSTEST:", f.msg, f.id)
    }f.msg == "Move" && console.log("ENVJSTEST:", f.msg, f.id, f.pos, f.orient, f.vel, f.scale);
    f.msg == "Mesh" && console.log("ENVJSTEST:", f.msg, f.id, f.mesh);
    console.log("TextGraphics.send:", f.msg, f.id, f, "--------------------");
    console.show && console.show(f, "TextGraphics.send:");
    var g;
    if(this._testInputCounter++ == 4) {
      g = {msg:"keydown", event:{keyCode:65, shiftKey:false}};
      this._inputCb && this._inputCb(g)
    }if(this._testInputCounter == 8) {
      g = {msg:"mousemove", event:{x:180, y:100}};
      this._inputCb && this._inputCb(g)
    }if(this._testInputCounter == 10) {
      g = {msg:"mousedown", event:{which:0}};
      this._inputCb && this._inputCb(g)
    }return this.methodTable[f.msg](f)
  };
  this.setInputCallback = function(f) {
    this._inputCb = f
  };
  this.destroy = function() {
  }
};
Kata.require(["katajs/oh/GraphicsSimulation.js"], function() {
  Kata.GraphicsSimulation.registerDriver("text", TextGraphics)
}, "katajs/gfx/TextGraphics.js");Math.uuid = function() {
  var e = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  return function(j, h) {
    var o = [];
    h = h || e.length;
    if(j) {
      for(var q = 0;q < j;q++) {
        o[q] = e[0 | Math.random() * h]
      }
    }else {
      o[8] = o[13] = o[18] = o[23] = "-";
      o[14] = "4";
      for(q = 0;q < 36;q++) {
        if(!o[q]) {
          j = 0 | Math.random() * 16;
          o[q] = e[q == 19 ? j & 3 | 8 : j]
        }
      }
    }return o.join("")
  }
}();
Math.uuidV4Bytes = function() {
  for(var e = new Array(16), j = 0;j < 16;j++) {
    var h = 0 | Math.random() * 256;
    if(j == 7) {
      h = h & 15 | 64
    }else {
      if(j == 9) {
        h = h & 243 | 8
      }
    }e[j] = h
  }return e
};
Math.uuid2 = function() {
  return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(e) {
    var j = Math.random() * 16 | 0;
    return(e == "x" ? j : j & 3 | 8).toString(16)
  }).toUpperCase()
};Kata.require([], function() {
  Kata.LocationIdentityNow = function() {
    return Kata.LocationIdentity(new Date)
  };
  Kata.LocationIdentity = function(e) {
    return{scale:[1, 1, 1], scaleTime:e, pos:[0, 0, 0], posTime:e, orient:[0, 0, 0, 1], orientTime:e, vel:[0, 0, 0], rotaxis:[0, 0, 1], rotvel:0}
  };
  Kata.deltaTime = function(e, j) {
    return(e - j) * 0.001
  };
  Kata._helperLocationExtrapolate3vec = function(e, j, h) {
    return[e[0] + j[0] * h, e[1] + j[1] * h, e[2] + j[2] * h]
  };
  Kata._helperQuatFromAxisAngle = function(e, j) {
    var h = Math.sin(j / 2);
    j = Math.cos(j / 2);
    return[h * e[0], h * e[1], h * e[2], j]
  };
  Kata._helperLocationExtrapolateQuaternion = function(e, j, h, o) {
    var q = Kata._helperQuatFromAxisAngle(h, j * o);
    j = e[0];
    h = e[1];
    o = e[2];
    e = e[3];
    var u = q[0], f = q[1], g = q[2];
    q = q[3];
    return[e * u + j * q + h * g - o * f, e * f + h * q + o * u - j * g, e * g + o * q + j * f - h * u, e * q - j * u - h * f - o * g]
  };
  Kata._helperLocationInterpolate3vec = function(e, j, h, o, q, u, f) {
    f = Kata.deltaTime(f, h);
    if(f > 0) {
      return Kata._helperLocationExtrapolate3vec(e, j, f)
    }h = Kata.deltaTime(h, u);
    if(h == 0) {
      return Kata._helperLocationExtrapolate3vec(e, j, f)
    }f += h;
    if(f < 0) {
      return o
    }o = Kata._helperLocationExtrapolate3vec(o, q, f);
    j = f / h;
    q = 1 - j;
    return[j * e[0] + q * o[0], j * e[1] + q * o[1], j * e[2] + q * o[2]]
  };
  Kata._helperLocationInterpolateQuaternion = function(e, j, h, o, q, u, f, g, m) {
    m = Kata.deltaTime(m, o);
    if(m > 0) {
      return Kata._helperLocationExtrapolateQuaternion(e, j, h, m)
    }o = Kata.deltaTime(o, g);
    if(o == 0) {
      return Kata._helperLocationExtrapolateQuaternion(e, j, h, m)
    }m += o;
    if(m < 0) {
      return q
    }q = Kata._helperLocationExtrapolateQuaternion(q, u, f, m);
    f = m / o;
    o = 1 - f;
    j = f * e[0] + o * q[0];
    h = f * e[1] + o * q[1];
    u = f * e[2] + o * q[2];
    e = f * e[3] + o * q[3];
    q = Math.sqrt(e * e + j * j + h * h + u * u);
    if(q < 1.0E-20) {
      return[j, h, u, e]
    }return[j / q, h / q, u / q, e / q]
  };
  Kata.LocationInterpolate = function(e, j, h) {
    return{scale:Kata._helperLocationInterpolate3vec(e.scale, [0, 0, 0], e.scaleTime, j.scale, [0, 0, 0], j.scaleTime, h), scaleTime:h, pos:Kata._helperLocationInterpolate3vec(e.pos, e.vel, e.posTime, j.pos, j.vel, j.posTime, h), posTime:h, orient:Kata._helperLocationInterpolateQuaternion(e.orient, e.rotvel, e.rotaxis, e.orientTime, j.orient, j.rotvel, j.rotaxis, j.orientTime, h), orientTime:h, rotvel:e.rotvel, rotaxis:e.rotaxis, vel:e.vel}
  };
  Kata.LocationTriTimeInterpolate = function(e, j, h, o, q) {
    return{scale:Kata._helperLocationInterpolate3vec(e.scale, [0, 0, 0], e.scaleTime, j.scale, [0, 0, 0], j.scaleTime, q), scaleTime:q, pos:Kata._helperLocationInterpolate3vec(e.pos, e.vel, e.posTime, j.pos, j.vel, j.posTime, h), posTime:h, orient:Kata._helperLocationInterpolateQuaternion(e.orient, e.rotvel, e.rotaxis, e.orientTime, j.orient, j.rotvel, j.rotaxis, j.orientTime, o), orientTime:o, rotvel:e.rotvel, rotaxis:e.rotaxis, vel:e.vel}
  };
  Kata.LocationExtrapolate = function(e, j) {
    return{scale:e.scale, scaleTime:j, pos:Kata._helperLocationExtrapolate3vec(e.pos, e.vel, Kata.deltaTime(j, e.posTime)), posTime:j, orient:Kata._helperLocationExtrapolateQuaternion(e.orient, e.rotvel, e.rotaxis, Kata.deltaTime(j, e.orientTime)), orientTime:j, rotvel:e.rotvel, rotaxis:e.rotaxis, vel:e.vel}
  };
  Kata.LocationCopy = function(e, j) {
    if(j.scale !== undefined) {
      e.scaleTime = j.scaleTime !== undefined ? j.scaleTime : j.time;
      e.scale = j.scale
    }if(j.pos !== undefined) {
      e.posTime = j.posTime !== undefined ? j.posTime : j.time;
      e.pos = j.pos
    }if(e.orient !== undefined) {
      e.orientTime = j.orientTime !== undefined ? j.orientTime : j.time;
      e.orient = j.orient.slice(0)
    }if(j.rotvel !== undefined && j.rotaxis !== undefined) {
      e.rotvel = j.rotvel;
      e.rotaxis = j.rotaxis.slice(0)
    }if(j.vel !== undefined) {
      e.vel = j.vel.slice(0)
    }
  };
  Kata.LocationCopyUnifyTime = function(e, j) {
    if(e.time !== undefined) {
      j.time = e.time;
      if(e.scale !== undefined) {
        j.scale = e.scale
      }if(e.pos !== undefined) {
        j.pos = e.pos
      }if(e.orient !== undefined) {
        j.orient = e.orient
      }if(e.rotvel !== undefined && e.rotaxis !== undefined) {
        j.rotvel = e.rotvel;
        j.rotaxis = e.rotaxis
      }if(e.vel !== undefined) {
        j.vel = e.vel
      }
    }else {
      var h = e.scaleTime;
      if(h === undefined || e.posTime >= h) {
        h = e.posTime
      }if(h === undefined || e.orientTime >= h) {
        h = e.orientTime
      }if(e.scale !== undefined) {
        j.scale = e.scale
      }if(e.pos !== undefined) {
        j.pos = e.vel && e.posTime ? Kata._helperLocationExtrapolate3vec(e.pos, e.vel, Kata.deltaTime(h, e.posTime)) : e.pos
      }if(e.orient !== undefined) {
        j.orient = e.rotvel !== undefined && e.rotaxis !== undefined && e.orientTime !== undefined ? Kata._helperLocationExtrapolateQuaternion(e.orient, e.rotvel, e.rotaxis, Kata.deltaTime(h, e.orientTime)) : e.orient
      }if(e.rotvel !== undefined && e.rotaxis !== undefined) {
        j.rotvel = e.rotvel;
        j.rotaxis = e.rotaxis
      }if(e.vel !== undefined) {
        j.vel = e.vel
      }j.time = h
    }
  };
  Kata.LocationSet = function(e) {
    if(e.time == undefined) {
      e.time = new Date
    }if(e.scale == undefined) {
      e.scale = [1, 1, 1]
    }if(e.vel == undefined) {
      e.vel = [0, 0, 0]
    }if(e.rotaxis == undefined) {
      e.rotaxis = [0, 0, 1]
    }if(e.rotvel == undefined) {
      e.rotvel = 0
    }if(e.orient == undefined) {
      e.orient = [0, 0, 0, 1]
    }return{scale:e.scale, scaleTime:e.time, pos:e.pos, posTime:e.time, orient:e.orient, orientTime:e.time, vel:e.vel, rotaxis:e.rotaxis, rotvel:e.rotvel}
  };
  Kata.LocationUpdate = function(e, j, h) {
    h || (h = j);
    var o = {scale:j.scale, scaleTime:j.scaleTime, pos:j.pos, posTime:j.posTime, orient:j.orient, orientTime:j.orientTime, vel:j.vel, rotaxis:j.rotaxis, rotvel:j.rotvel};
    if(e.pos && e.time && e.time >= j.posTime) {
      o.pos = e.pos;
      o.posTime = e.time
    }else {
      if(e.vel && e.time && e.time >= j.posTime) {
        o.pos = Kata._helperLocationExtrapolate3vec(j.pos, j.vel, Kata.deltaTime(e.time, j.posTime));
        o.posTime = e.time
      }
    }if(e.vel && e.time && e.time >= j.posTime) {
      o.vel = e.vel
    }else {
      j.vel = h.vel
    }if(e.orient && e.time && e.time >= j.orientTime) {
      o.orient = e.orient;
      o.orientTime = e.time
    }else {
      if(e.rotvel !== undefined && e.rotaxis !== undefined) {
        o.orient = Kata._helperLocationExtrapolateQuaternion(j.orient, j.rotvel, j.rotaxis, Kata.deltaTime(e.time, j.orientTime));
        o.orientTime = e.time
      }
    }if(e.rotvel !== undefined && e.rotaxis !== undefined && e.time !== undefined && e.time >= j.orientTime) {
      o.rotaxis = e.rotaxis;
      o.rotvel = e.rotvel
    }else {
      o.rotaxis = j.rotaxis;
      o.rotvel = j.rotvel
    }if(e.scale && e.time && e.time >= j.scaleTime) {
      o.scale = e.scale;
      o.scaleTime = e.time
    }else {
      o.scale = j.scale;
      o.scaleTime = j.scaleTime
    }return o
  };
  Kata.LocationReset = function(e, j) {
    if(e.scale !== undefined) {
      j.scale = e.scale;
      j.scaleTime = e.time
    }if(e.pos !== undefined) {
      j.pos = e.pos;
      j.posTime = e.time
    }if(e.vel !== undefined) {
      j.vel = e.vel
    }if(e.rotvel !== undefined && e.rotaxis !== undefined) {
      j.rotaxis = e.rotaxis
    }if(e.orient !== undefined) {
      j.orient = e.orient;
      j.orientTime = e.time
    }
  };
  Kata.QuaternionMulQuaternion = function(e, j) {
    var h = e[0], o = e[1], q = e[2];
    e = e[3];
    var u = j[0], f = j[1], g = j[2];
    j = j[3];
    return[e * u + h * j + o * g - q * f, e * f + o * j + q * u - h * g, e * g + q * j + h * f - o * u, e * j - h * u - o * f - q * g]
  };
  Kata.QuaternionToRotation = function(e) {
    var j = e[0], h = e[1], o = e[2], q = e[3];
    e = q * q;
    var u = q * j, f = q * h;
    q = q * o;
    var g = j * j, m = j * h;
    j = j * o;
    var p = h * h;
    h = h * o;
    o = o * o;
    var r = e + g + p + o;
    return[[(e + g - p - o) / r, 2 * (q + m) / r, 2 * (j - f) / r, 0], [2 * (m - q) / r, (e - g + p - o) / r, 2 * (u + h) / r, 0], [2 * (f + j) / r, 2 * (h - u) / r, (e - g - p + o) / r, 0], [0, 0, 0, 1]]
  };
  Kata.Vec3Cross = function(e, j) {
    return[e[1] * j[2] - e[2] * j[1], e[2] * j[0] - e[0] * j[2], e[0] * j[1] - e[1] * j[0]]
  };
  Kata.Vec3Add = function(e, j) {
    return[e[0] + j[0], e[1] + j[1], e[2] + j[2]]
  };
  Kata.Vec3Sub = function(e, j) {
    return[e[0] - j[0], e[1] - j[1], e[2] - j[2]]
  };
  Kata.Vec3Scale = function(e, j) {
    return[e[0] * j, e[1] * j, e[2] * j]
  };
  Kata.Vec3Rotate = function(e, j, h, o) {
    return[e[0] * j[0] + e[1] * h[0] + e[2] * o[0], e[0] * j[1] + e[1] * h[1] + e[2] * o[1], e[0] * j[2] + e[1] * h[2] + e[2] * o[2]]
  };
  Kata.LocationCompose = function(e, j, h) {
    var o = Kata.LocationTriTimeInterpolate(h, j, e.posTime, e.orientTime, e.scaleTime), q = Kata.QuaternionToRotation(o.orient);
    j = Kata.Vec3Add(Kata.Vec3Add(Kata.Vec3Scale(Kata.Vec3Cross(o.rotaxis, e.pos), o.rotvel), o.vel), Kata.Vec3Rotate(e.vel, q[0], q[1], q[2]));
    h = Kata.Vec3Rotate(e.rotaxis, q[0], q[1], q[2]);
    q = Kata.Vec3Add(Vec3Rotate(e.pos, q[0], q[1], q[2]), o.pos);
    o = Kata.QuaternionMulQuaternion(o.orient, e.orient);
    return{pos:q, orient:o, scale:e.scale, rotaxis:h, rotvel:e.rotvel, vel:j, posTime:e.posTime, orientTime:e.orientTime, scaleTime:e.scaleTime}
  };
  Kata.QuaternionInverse = function(e) {
    var j = e[0], h = e[1], o = e[2];
    e = e[3];
    var q = 1 / (j * j + h * h + o * o + e * e);
    return[-j * q, -h * q, -o * q, e * q]
  };
  Kata.LocationInverseCompose = function(e, j, h) {
    var o = Kata.LocationTriTimeInterpolate(h, j, e.posTime, e.orientTime, e.scaleTime), q = Kata.QuaternionInverse(o.orient), u = Kata.QuaternionToRotation(q);
    j = Kata.Vec3Rotate(Kata.Vec3Add(Kata.Vec3Sub(Kata.Vec3Scale(Kata.Vec3Cross(o.rotaxis, e.pos), -o.rotvel), o.vel), e.vel), u[0], u[1], u[2]);
    h = Kata.Vec3Rotate(e.rotaxis, u[0], u[1], u[2]);
    o = Kata.Vec3Rotate(Kata.Vec3Sub(e.pos, o.pos), u[0], u[1], u[2]);
    q = Kata.QuaternionMulQuaternion(e.orient, q);
    return{pos:o, orient:q, scale:e.scale, rotaxis:h, rotvel:e.rotvel, vel:j, posTime:e.posTime, orientTime:e.orientTime, scaleTime:e.scaleTime}
  };
  Kata.LocationReparent = function(e, j, h) {
    var o, q = j.length;
    for(o = 0;o < q;o++) {
      e = Kata.LocationCompose(e, j[o][0], j[o][1])
    }for(o = h.length - 1;o >= 0;o--) {
      e = Kata.LocationInverseCompose(e, h[o][0], h[o][1])
    }return e
  }
}, "katajs/core/Location.js");Kata.require(["katajs/core/Channel.js"], function() {
  var e = Kata.Channel.prototype;
  Kata.SimpleChannel = function(j) {
    e.constructor.call(this);
    j && this.pair(j)
  };
  Kata.extend(Kata.SimpleChannel, e);
  Kata.SimpleChannel.prototype.pair = function(j) {
    if(!(j instanceof Kata.SimpleChannel)) {
      console.error("otherChannel " + j + " is not instance of SimpleChannel");
      throw"Error in SimpleChannel.pair";
    }j.mPartner = this;
    this.mPartner = j
  };
  Kata.SimpleChannel.prototype.sendMessage = function(j) {
    if(Kata.FAKE_WEB_WORKERS_DEBUG) {
      j = JSON.parse(JSON.stringify(j))
    }this.mPartner.callListeners(j)
  }
}, "katajs/core/SimpleChannel.js");if(typeof Kata == "undefined") {
  Kata = {}
}if(typeof console == "undefined") {
  console = {};
  debug_console = false
}else {
  debug_console = true
}Kata.require([], function() {
  var e = (new Date).getTime(), j = false;
  Kata.scheduleNowUpdates = function(h) {
    function o() {
      setTimeout(o, h);
      Kata.updateNow()
    }
    o();
    j = true
  };
  Kata.now = function() {
    return j ? e : Kata.updateNow()
  };
  Kata.updateNow = function(h) {
    return e = h === undefined ? (new Date).getTime() : h
  }
}, "katajs/core/Time.js");Kata.require([], function() {
  Kata.URL = function(e) {
    return e
  };
  Kata.URL.protocol = function(e) {
    var j = e.indexOf("://");
    j == -1 && Kata.error("Invalid URL: " + e);
    return e.substr(0, j)
  };
  Kata.URL._hostAndPort = function(e) {
    var j = e.indexOf("://");
    if(j == -1) {
      Kata.error("Invalid URL: " + e);
      j = 0
    }else {
      j += 3
    }var h = e.indexOf("/", j);
    return h != -1 ? e.substr(j, h - j) : e.substr(j)
  };
  Kata.URL.host = function(e) {
    e = Kata.URL._hostAndPort(e);
    var j = e.indexOf(":");
    if(j == -1) {
      return e
    }return e.substr(0, j)
  };
  Kata.URL.port = function(e) {
    e = Kata.URL._hostAndPort(e);
    var j = e.indexOf(":");
    if(j != -1) {
      e = e.substr(j + 1);
      return parseInt(e)
    }
  };
  Kata.URL.resource = function(e) {
    var j = e.indexOf("://");
    j == -1 && Kata.error("Invalid URL: " + e);
    j = e.indexOf("/", j + 3);
    if(j == -1) {
      return""
    }return e.substr(j)
  };
  Kata.URL.equals = function(e, j) {
    return e == j
  }
}, "katajs/core/URL.js");Kata.require([], function() {
  Kata.MessageDispatcher = function(e) {
    this._handlers = e
  };
  Kata.MessageDispatcher.prototype.add = function(e, j) {
    this._handlers[e] = j
  };
  Kata.MessageDispatcher.prototype.dispatch = function(e, j) {
    var h = j.__type;
    if(!this._handlers[h]) {
      return false
    }this._handlers[h](e, j);
    return true
  }
}, "katajs/core/MessageDispatcher.js");(function() {
  Kata.Deque = function() {
    this.mHead = this.mSize = 0;
    this.mArray = new Array(8)
  };
  Kata.Deque.prototype.expand = function() {
    var e = this.mArray.length;
    this.mArray.length = Math.round(e * 1.5);
    for(var j = this.mSize + this.mHead - e, h = 0;h < j;h++) {
      this.mArray[(h + e) % this.mArray.length] = this.mArray[h]
    }
  };
  Kata.Deque.prototype.push_back = function(e) {
    this.mSize >= this.mArray.length && this.expand();
    var j = this.mHead + this.mSize;
    if(j >= this.mArray.length) {
      this.destIndex -= this.mArray.length
    }this.mSize++;
    this.mArray[j] = e
  };
  Kata.Deque.prototype.push_front = function(e) {
    this.mSize >= this.mArray.length && this.expand();
    var j = this.mHead;
    if(j == 0) {
      j = this.mArray.length
    }j--;
    this.mHead = j;
    this.mSize++;
    this.mArray[j] = e
  };
  Kata.Deque.prototype.index = function(e) {
    e = this.mHead + e;
    if(e >= this.mArray.length) {
      this.destIndex -= this.mArray.length
    }return this.mArray[e]
  };
  Kata.Deque.prototype.back = function() {
    var e = this.mHead + this.mSize - 1;
    if(e >= this.mArray.length) {
      this.destIndex -= this.mArray.length
    }return this.mArray[e]
  };
  Kata.Deque.prototype.pop_back = function() {
    if(this.mSize != 0) {
      var e = this.mHead + this.mSize - 1;
      if(e >= this.mArray.length) {
        this.destIndex -= this.mArray.length
      }var j = this.mArray[e];
      this.mArray[e] = null;
      this.mSize--;
      return j
    }
  };
  Kata.Deque.prototype.pop_front = function() {
    if(this.mSize != 0) {
      var e = this.mArray[this.mHead];
      this.mArray[this.mHead] = null;
      this.mHead++;
      this.mSize -= 1;
      if(this.mHead >= this.mArray.length) {
        this.mHead -= this.mArray.length
      }return e
    }
  };
  Kata.Deque.prototype.front = function() {
    return this.mArray[this.mHead]
  };
  Kata.Deque.prototype.empty = function() {
    return this.mSize == 0
  };
  Kata.Deque.prototype.size = function() {
    return this.mSize
  };
  Kata.Deque.prototype.clear = function() {
    Kata.Deque.call(this)
  };
  Kata.Deque.prototype.erase = function(e) {
    for(e = this.mHead + e;e + 1 < this.mSize;++e) {
      this.mArray[e] = this.mArray[e + 1]
    }this.pop_back()
  }
})();Kata.require([], function() {
  Kata.Quaternion = function() {
    this.length = 4;
    if(arguments.length == 0) {
      this[0] = 0;
      this[1] = 0;
      this[2] = 0;
      this[3] = 1
    }else {
      if(arguments.length == 1) {
        this[0] = arguments[0][0];
        this[1] = arguments[0][1];
        this[2] = arguments[0][2];
        this[3] = arguments[0][3]
      }else {
        if(arguments.length == 4) {
          this[0] = arguments[0];
          this[1] = arguments[1];
          this[2] = arguments[2];
          this[3] = arguments[3]
        }else {
          throw"Invalid Quaternion constructor arguments.";
        }
      }
    }
  };
  Kata.extend(Kata.Quaternion, Array.prototype);
  Kata.Quaternion.fromAxisAngle = function(e, j) {
    var h = Math.sin(j * 0.5);
    return new Kata.Quaternion(h * e[0], h * e[1], h * e[2], Math.cos(j * 0.5))
  };
  Kata.Quaternion.fromLocationAngularVelocity = function(e) {
    return Kata.Quaternion.fromAxisAngle(e.rotaxis, e.rotvel)
  };
  Kata.Quaternion.identity = function() {
    return new Kata.Quaternion
  };
  Kata.Quaternion.zero = function() {
    return new Kata.Quaternion(0, 0, 0, 0)
  };
  Kata.Quaternion.prototype.array = function() {
    return[this[0], this[1], this[2], this[3]]
  };
  Kata.Quaternion.prototype.toAngleAxis = function() {
    var e = this[0] * this[0] + this[1] * this[1] + this[2] * this[2], j = this[3];
    if(j > 1 && j < 1.000001) {
      j = 1
    }if(j < -1 && j > -1.000001) {
      j = -1
    }if(e > 1.0E-8 && j <= 1 && j >= -1) {
      j = 2 * Math.acos(j);
      e = Math.sqrt(e);
      e = [this[0] / e, this[1] / e, this[2] / e]
    }else {
      j = 0;
      e = [1, 0, 0]
    }return{angle:j, axis:e}
  };
  Kata.Quaternion.prototype.dot = function(e) {
    return this[0] * e[0] + this[1] * e[1] + this[2] * e[2] + this[3] * e[3]
  };
  Kata.Quaternion.prototype.sizeSquared = function() {
    return this.dot(this)
  };
  Kata.Quaternion.prototype.size = function() {
    return Math.sqrt(this.sizeSquared)
  };
  Kata.Quaternion.prototype.normal = function() {
    var e = this.size();
    if(e > 1.0E-8) {
      return this.scale(1 / e)
    }return new Kata.Quaternion(this)
  };
  Kata.Quaternion.prototype.scale = function(e) {
    if(typeof e == "number") {
      return new Kata.Quaternion(this[0] * e, this[1] * e, this[2] * e, this[3] * e)
    }else {
      throw"Don't know how to multiply Quaternion by given object.";
    }
  };
  Kata.Quaternion.prototype.add = function(e) {
    if(typeof e == "number") {
      return new Kata.Quaternion(this[0] + e, this[1] + e, this[2] + e, this[3] + e)
    }else {
      if(e && typeof e.length !== "undefined" && e.length == 4) {
        return new Kata.Quaternion(this[0] + e[0], this[1] + e[1], this[2] + e[2], this[3] + e[3])
      }else {
        throw"Don't know how to multiply Quaternion by given object.";
      }
    }
  };
  Kata.Quaternion.prototype.negate = function() {
    return new Kata.Quaternion(-this[0], -this[1], -this[2], -this[3])
  };
  Kata.Quaternion._vec3_cross = function(e, j) {
    return[e[1] * j[2] - e[2] * j[1], e[2] * j[0] - e[0] * j[2], e[0] * j[1] - e[1] * j[0]]
  };
  Kata.Quaternion.prototype.multiply = function(e) {
    if(e.prototype === Kata.Quaternion) {
      return new Kata.Quaternion(this[3] * e[0] + this[0] * e[3] + this[1] * e[2] - this[2] * e[1], this[3] * e[1] + this[1] * e[3] + this[2] * e[0] - this[0] * e[2], this[3] * e[2] + this[2] * e[3] + this[0] * e[1] - this[1] * e[0], this[3] * e[3] - this[0] * e[0] - this[1] * e[1] - this[2] * e[2])
    }else {
      if(typeof e.length !== "undefined" && e.length === 3) {
        var j = [this[0], this[1], this[2]], h = Kata.Quaternion._vec3_cross(j, e);
        j = Kata.Quaternion._vec3_cross(j, h);
        h = [h[0] * 2 * this[3], h[1] * 2 * this[3], h[2] * 2 * this[3]];
        j = [j[0] * 2, j[1] * 2, j[2] * 2];
        return[e[0] + h[0] + j[0], e[1] + h[1] + j[1], e[2] + h[2] + j[2]]
      }else {
        throw"Don't know how to multiply given type by quaternion.";
      }
    }
  };
  Kata.Quaternion.prototype.inverse = function() {
    var e = lengthSquared();
    if(e > 1.0E-8) {
      return new Quaternion(-x / e, -y / e, -z / e, w / e)
    }return Kata.Quaternion.zero()
  };
  Kata.Quaternion.prototype.exp = function(e) {
    var j = this.toAngleAxis();
    return Kata.Quaternion.fromAxisAngle(j.axis, j.angle * e)
  }
}, "katajs/core/Quaternion.js");Kata.require([], function() {
  Kata.SpaceID = {};
  Kata.SpaceID.nil = function() {
    return""
  };
  Kata.SpaceID.any = function() {
    return"*"
  }
}, "katajs/core/SpaceID.js");Kata.require(["katajs/core/Channel.js"], function() {
  Kata.FilterChannel = function(j, h) {
    this._channel = j;
    this._filter = h;
    this._channel.registerListener(Kata.bind(this._filterMessage, this))
  };
  var e = Kata.Channel.prototype;
  Kata.extend(Kata.FilterChannel, e);
  Kata.FilterChannel.prototype.callListeners = function(j) {
    this._filter(this, j) || e.callListeners.apply(this, [j])
  };
  Kata.FilterChannel.prototype.sendMessage = function(j) {
    this._channel.sendMessage(j)
  };
  Kata.FilterChannel.prototype._filterMessage = function(j, h) {
    this.callListeners(h)
  }
}, "katajs/core/FilterChannel.js");Kata.require(["katajs/core/SimpleChannel.js"], function() {
  function e(o) {
    return function(q) {
      o.callListeners(q.data)
    }
  }
  function j(o) {
    return function(q) {
      o.gotError(q.message, q.filename, q.lineno)
    }
  }
  if(Kata.WEB_WORKERS_ENABLED === undefined) {
    Kata.WEB_WORKERS_ENABLED = true
  }if(Kata.FAKE_WEB_WORKERS_DEBUG === undefined) {
    Kata.FAKE_WEB_WORKERS_DEBUG = true
  }if(Kata.WEB_WORKERS_BOOTSTRAP_SCRIPT === undefined) {
    Kata.WEB_WORKERS_BOOTSTRAP_SCRIPT = false
  }Kata.FakeWebWorker = function(o, q, u) {
    this.mChannel = new Kata.SimpleChannel;
    this.mArgs = u;
    this.mClassName = q;
    this.mJSFile = o;
    network_debug && console.log("new webworker")
  };
  Kata.FakeWebWorker.prototype.go = function() {
    var o = new Kata.SimpleChannel(this.mChannel);
    if(!this.mClassName || !this.mArgs) {
      Kata.error("WebWorker.go() called twice")
    }else {
      var q = this.mArgs, u = this.mClassName, f = u.split(".");
      delete this.mClassName;
      delete this.mArgs;
      Kata.require([this.mJSFile], function() {
        for(var g = self, m = 0;g && m < f.length;m++) {
          g = g[f[m]]
        }g || Kata.error(u + " is undefined:" + this.mJSFile);
        network_debug && console.log("going!");
        this.mChild = new g(o, q)
      })
    }
  };
  Kata.FakeWebWorker.prototype.getChannel = function() {
    return this.mChannel
  };
  Kata.FakeWebWorker.prototype.gotError = function(o, q, u) {
    Kata.error("ERROR at " + q + ":" + u + ": " + o)
  };
  var h = Kata.Channel.prototype;
  Kata.FakeWebWorker.Channel = function(o) {
    h.constructor.call(this);
    this.mMessagePort = o;
    this.mMessagePort.onmessage = e(this)
  };
  Kata.extend(Kata.FakeWebWorker.Channel, h);
  Kata.FakeWebWorker.Channel.prototype.sendMessage = function(o) {
    this.mMessagePort.postMessage(o)
  };
  if(Kata.WEB_WORKERS_ENABLED && typeof Worker != "undefined") {
    Kata.WebWorker = function(o, q, u) {
      this.mWorker = Kata.bootstrapWorker === undefined ? new Worker(Kata.scriptRoot + "katajs/core/GenericWorker.js" + Kata.queryString) : new Worker(Kata.bootstrapWorker);
      this.mWorker.onerror = j(this);
      this.mInitialMessage = [Kata.scriptRoot, Kata.bootstrapWorker === undefined ? undefined : Kata.bootstrapWorker, o, q, u, Kata.queryString];
      this.mChannel = new Kata.WebWorker.Channel(this.mWorker)
    };
    Kata.WebWorker.prototype.go = function() {
      var o = this.mInitialMessage;
      delete this.mInitialMessage;
      Kata.bootstrapWorker !== undefined && this.mWorker.postMessage(Kata.scriptRoot + "katajs/core/GenericWorker.js" + Kata.queryString);
      this.mWorker.postMessage(o)
    };
    Kata.WebWorker.prototype.getChannel = Kata.FakeWebWorker.prototype.getChannel;
    Kata.WebWorker.prototype.gotError = Kata.FakeWebWorker.prototype.gotError;
    Kata.WebWorker.Channel = Kata.FakeWebWorker.Channel
  }else {
    Kata.WebWorker = Kata.FakeWebWorker
  }
}, "katajs/core/WebWorker.js");Kata.require(["katajs/core/Math.uuid.js"], function() {
  Kata.ObjectID = {};
  Kata.ObjectID.nil = function() {
    return"00000000-0000-0000-0000-000000000000"
  };
  Kata.ObjectID.random = function() {
    return Math.uuid()
  };
  Kata.ObjectID.any = function() {
    return"ffffffff-ffff-ffff-ffff-ffffffffffff"
  }
}, "katajs/core/ObjectID.js");Kata.require([], function() {
  Kata.Channel = function() {
  };
  Kata.Channel.prototype.registerListener = function(e) {
    if(!e.call) {
      network_debug && console.log("Listener call type is ", typeof e);
      network_debug && console.log("Listener constructor type is ", e.constructor);
      throw"Error in registerListener: not a function";
    }if(this.mListener) {
      if(this.mListener instanceof Array) {
        this.mListener.push(e)
      }else {
        this.mListener = [this.mListener, e]
      }
    }else {
      this.mListener = e
    }
  };
  Kata.Channel.prototype.callListeners = function(e) {
    if(!Kata.debugMessage(this, e)) {
      if(this.mListener) {
        if(this.mListener.call) {
          this.mListener(this, e)
        }else {
          for(var j = 0;j < this.mListener.length;j++) {
            this.mListener[j](this, e)
          }
        }
      }else {
        Kata.error("Kata.Channel mListener not set")
      }
    }
  };
  Kata.Channel.prototype.sendMessage = null
}, "katajs/core/Channel.js");Kata.require(["katajs/core/SpaceID.js", "katajs/core/ObjectID.js"], function() {
  Kata.PresenceID = function() {
    if(arguments.length == 1) {
      if(arguments[0].mSpace && arguments[0].mObject) {
        this.mSpace = arguments[0].mSpace;
        this.mObject = arguments[0].mObject
      }else {
        throw"Invalid PresenceID constructor arguments.";
      }
    }else {
      if(arguments.length == 2 && arguments[0] && arguments[1]) {
        this.mSpace = arguments[0];
        this.mObject = arguments[1]
      }else {
        throw"Invalid PresenceID constructor arguments.";
      }
    }
  };
  Kata.PresenceID.prototype.space = function() {
    return this.mSpace
  };
  Kata.PresenceID.prototype.object = function() {
    return this.mObject
  };
  Kata.PresenceID.prototype.toString = function() {
    return"PresenceID(" + this.mSpace.toString() + ":" + this.mObject.toString() + ")"
  };
  Kata.PresenceID.nil = function() {
    return new Kata.PresenceID(Kata.SpaceID.nil(), Kata.ObjectID.nil())
  };
  Kata.PresenceID.any = function() {
    return new Kata.PresenceID(Kata.SpaceID.any(), Kata.ObjectID.any())
  }
}, "katajs/core/PresenceID.js");Kata.require(["katajs/core/URL.js"], function() {
  Kata.SessionManager = function() {
    this.mSpaceConnections = {};
    this.mObjects = {}
  };
  Kata.SessionManager.registerProtocolHandler = function(e, j) {
    if(!this._protocols) {
      this._protocols = {}
    }this._protocols[e] && Kata.warn("Overwriting protocol handler for " + e);
    this._protocols[e] = j
  };
  Kata.SessionManager._getProtocolHandler = function(e) {
    if(this._protocols) {
      return this._protocols[e]
    }
  };
  Kata.SessionManager.prototype.connect = function(e, j, h) {
    var o = j.space, q = Kata.URL.protocol(o), u = this.mSpaceConnections[o];
    if(!u) {
      (q = Kata.SessionManager._getProtocolHandler(q)) || Kata.error("Unknown space protocol: " + o.protocol);
      u = new q(this, o);
      this.mSpaceConnections[o] = u
    }this.mObjects[e.getID()] = e;
    u.connectObject(e.getID(), h, j, j.visual)
  };
  Kata.SessionManager.prototype.aliasIDs = function(e, j) {
    var h = this.mObjects[e];
    if(h) {
      this.mObjects[j.object] = h
    }else {
      Kata.warn("Got ID aliasing for unknown object: " + e)
    }
  };
  Kata.SessionManager.prototype.connectionResponse = function(e, j, h, o, q) {
    var u = this.mObjects[e];
    if(u) {
      delete this.mObjects[e];
      this.mObjects[h.object] = u;
      u.connectionResponse(j, h, o, q)
    }else {
      Kata.warn("Got connection response for unknown object: " + e)
    }
  };
  Kata.SessionManager.prototype.disconnect = function(e, j) {
    (e = this.mSpaceConnections[Kata.URL(j.space)]) && e.disconnectObject(j.id)
  };
  Kata.SessionManager.prototype.disconnected = function(e, j) {
    var h = this.mObjects[e];
    h ? h.disconnected(j) : Kata.warn("Got disconnection event for unknown object: " + e)
  };
  Kata.SessionManager.prototype.spaceConnectionDisconnected = function(e) {
    for(var j in this.mSpaceConnections) {
      e === this.mSpaceConnections[j] && delete this.mSpaceConnections[j]
    }
  };
  Kata.SessionManager.prototype.sendODPMessage = function(e, j, h, o, q, u) {
    this.mSpaceConnections[e].sendODPMessage(j, h, o, q, u)
  };
  Kata.SessionManager.prototype.receiveODPMessage = function(e, j, h, o, q, u) {
    this.mObjects[o].receiveODPMessage(e, j, h, o, q, u)
  };
  Kata.SessionManager.prototype.registerProxQuery = function(e, j, h) {
    this.mSpaceConnections[e].registerProxQuery(j, h)
  };
  Kata.SessionManager.prototype.proxEvent = function(e, j, h, o, q) {
    this.mObjects[j].proxEvent(e, h, o, q)
  };
  Kata.SessionManager.prototype.locUpdateRequest = function(e, j, h, o) {
    e = this.mSpaceConnections[e];
    e !== undefined && e.locUpdateRequest(j, h, o)
  };
  Kata.SessionManager.prototype.presenceLocUpdate = function(e, j, h, o, q) {
    this.mObjects[h].presenceLocUpdate(e, j, o, q)
  };
  Kata.SessionManager.prototype.subscribe = function(e, j, h) {
    this.mSpaceConnections[e].subscribe(j, h)
  };
  Kata.SessionManager.prototype.unsubscribe = function(e, j, h) {
    this.mSpaceConnections[e].unsubscribe(j, h)
  }
}, "katajs/oh/SessionManager.js");Kata.require(["katajs/oh/HostedObject.js", "katajs/oh/SessionManager.js", "katajs/core/URL.js"], function() {
  Kata.ObjectHost = function(e, j, h) {
    this.mSimulations = [];
    this.mSimulationsByName = {};
    this.mSimulationCallbacksByName = {};
    this.mObjects = {};
    this.mSessionManager = new Kata.SessionManager;
    this.createObject(e, j, h);
    network_debug && console.log("ObjectHosted!")
  };
  Kata.ObjectHost.prototype.registerSimulation = function(e, j) {
    this.mSimulations.push(e);
    this.mSimulationsByName[j] = e;
    e.registerListener(Kata.bind(this.receivedSimulationMessage, this, j))
  };
  Kata.ObjectHost.prototype.sendToSimulation = function(e, j) {
    if(j) {
      this.mSimulationsByName[j].sendMessage(e)
    }else {
      for(j in this.mSimulationsByName) {
        this.mSimulationsByName[j].sendMessage(e)
      }
    }
  };
  Kata.ObjectHost.prototype.registerSimulationCallback = function(e, j) {
    if(e in this.mSimulationCallbacksByName) {
      this.mSimulationCallbacksByName[e].push(j)
    }else {
      this.mSimulationCallbacksByName[e] = [j]
    }
  };
  Kata.ObjectHost.prototype.unregisterSimulationCallback = function(e, j) {
    var h = this.mSimulationCallbacksByName[e];
    if(h.length == 1) {
      delete this.mSimulationCallbacksByName[e]
    }else {
      for(e = 0;e < h.length;++e) {
        if(h[e] == j) {
          h[e] = h[h.length - 1];
          h.pop();
          break
        }
      }
    }
  };
  Kata.ObjectHost.prototype.receivedSimulationMessage = function(e, j, h) {
    var o = this.mSimulationCallbacksByName[e];
    if(o) {
      for(var q = 0;q < o.length;++q) {
        o[q].handleMessageFromSimulation(e, j, h)
      }
    }
  };
  Kata.ObjectHost.prototype.privateIdGenerator = function() {
    var e = 0;
    return function() {
      e += 1;
      return"" + e
    }
  }();
  Kata.ObjectHost.prototype.createObject = function(e, j, h) {
    var o = this.generateObject(this.privateIdGenerator());
    e && j && h && o.createScript(e, j, h)
  };
  Kata.ObjectHost.prototype.generateObject = function(e) {
    network_debug && console.log("Creating Object " + e);
    this.mObjects[e] = new Kata.HostedObject(this, e);
    return this.mObjects[e]
  };
  Kata.ObjectHost.prototype.connect = function(e, j, h) {
    this.mSessionManager.connect(e, j, h)
  };
  Kata.ObjectHost.prototype.disconnect = function(e, j) {
    this.mSessionManager.disconnect(e, j)
  };
  Kata.ObjectHost.prototype.sendODPMessage = function(e, j, h, o, q, u) {
    this.mSessionManager.sendODPMessage(e, j, h, o, q, u)
  };
  Kata.ObjectHost.prototype.registerProxQuery = function(e, j, h) {
    this.mSessionManager.registerProxQuery(e, j, h)
  };
  Kata.ObjectHost.prototype.locUpdateRequest = function(e, j, h, o) {
    this.mSessionManager.locUpdateRequest(e, j, h, o)
  };
  Kata.ObjectHost.prototype.subscribe = function(e, j, h) {
    this.mSessionManager.subscribe(e, j, h)
  };
  Kata.ObjectHost.prototype.unsubscribe = function(e, j, h) {
    this.mSessionManager.unsubscribe(e, j, h)
  }
}, "katajs/oh/ObjectHost.js");Kata.require(["katajs/core/URL.js", "katajs/core/Location.js", "katajs/core/Time.js"], function() {
  Kata.ScriptProtocol = {commonReconstitute:function(e) {
    if(typeof e.space != "undefined") {
      e.space = Kata.URL(e.space)
    }if(typeof e.spaceid != "undefined") {
      e.spaceid = Kata.URL(e.spaceid)
    }return e
  }, FromScript:{Types:{Connect:"fcon", Disconnect:"fdis", SendODPMessage:"fodp", Location:"floc", Visual:"fvis", Query:"fque", Subscription:"fsub", CreateObject:"fcre", GraphicsMessage:"fgfm", EnableGUIMessage:"feui", DisableGUIMessage:"fdui", GUIMessage:"fgui"}, reconstitute:function(e) {
    return e = Kata.ScriptProtocol.commonReconstitute(e)
  }, Connect:function(e, j, h, o) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.Connect;
    this.space = e;
    this.auth = j;
    h && Kata.LocationCopyUnifyTime(h, this);
    if(o) {
      this.visual = o
    }
  }, RegisterGUIMessage:function(e) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.EnableGUIMessage;
    this.event = e
  }, UnregisterGUIMessage:function(e) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.DisableGUIMessage;
    this.event = e
  }, GUIMessage:function(e, j) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GUIMessage;
    this.msg = e;
    this.event = j
  }, Disconnect:function(e, j) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.Disconnect;
    this.space = e;
    this.id = j
  }, SendODPMessage:function(e, j, h, o, q, u) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.SendODPMessage;
    this.space = e;
    this.source_object = j;
    this.source_port = h;
    this.dest_object = o;
    this.dest_port = q;
    this.payload = u
  }, Location:function(e, j, h, o) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.Location;
    this.space = e;
    this.id = j;
    h && Kata.LocationCopyUnifyTime(h, this);
    if(o) {
      this.vis = o
    }
  }, Visual:function(e, j, h) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.Visual;
    this.space = e;
    this.id = j;
    this.vis = h
  }, Query:function(e, j, h) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.Query;
    this.space = e;
    this.id = j;
    this.sa = h
  }, Subscription:function(e, j, h, o) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.Subscription;
    this.space = e;
    this.id = j;
    this.observed = h;
    this.enable = o
  }, CreateObject:function(e, j, h) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.CreateObject;
    this.script = e;
    this.constructor = j;
    this.args = h
  }, GFXCreateNode:function(e, j, h) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.msg = "Create";
    this.space = e + j;
    this.id = h.id();
    this.spaceid = this.space;
    Kata.LocationCopyUnifyTime(h.mLocation, this)
  }, GFXCustom:function(e, j, h) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.msg = "Custom";
    this.data = h;
    this.spaceid = this.space = e + j
  }, GFXMoveNode:function(e, j, h, o) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.msg = "Move";
    this.space = e + j;
    this.id = h.id();
    this.spaceid = this.space;
    o && Kata.LocationCopyUnifyTime(o.loc, this)
  }, GFXAnimate:function(e, j, h, o) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.msg = "Animate";
    this.space = e + j;
    this.id = h.id();
    this.spaceid = this.space;
    this.animation = o
  }, GFXLabel:function(e, j, h, o, q) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.msg = "Label";
    this.space = e + j;
    this.id = h;
    this.spaceid = this.space;
    this.label = o;
    this.offset = q
  }, GFXDestroyNode:function(e, j, h) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.space = e + j;
    this.msg = "Destroy";
    this.id = h.id()
  }, generateGFXUpdateVisualMessages:function(e, j, h) {
    var o = [];
    h.rMesh && o.push(new Kata.ScriptProtocol.FromScript.GFXUpdateVisualMesh(e, j, h.id(), h.rMesh, h.rAnim, h.rUpAxis, h.rCenter, h.scale()));
    return o
  }, GraphicsMessage:function(e, j, h) {
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.spaceid = this.space = e + j;
    this.id = h
  }, GFXUpdateVisualMesh:function(e, j, h, o, q, u, f, g) {
    Kata.ScriptProtocol.FromScript.GraphicsMessage.call(this, e, j, h);
    if(o == null) {
      this.msg = "DestroyMesh"
    }else {
      this.msg = "Mesh";
      this.mesh = o;
      this.anim = q;
      this.up_axis = u;
      this.center = f;
      this.scale = g
    }
  }, GFXAttachCamera:function(e, j, h, o) {
    Kata.ScriptProtocol.FromScript.GraphicsMessage.call(this, e, j, h);
    this.msg = "AttachCamera";
    this.target = o
  }, GFXAttachCameraTexture:function(e, j, h, o) {
    Kata.ScriptProtocol.FromScript.GraphicsMessage.call(this, e, j, h);
    this.msg = "AttachCameraTexture";
    this.space = e + j;
    this.id = h;
    this.texobjid = textureObjectId;
    this.texobjspace = o;
    this.texname = textureName
  }, GFXDetachCamera:function(e, j, h) {
    Kata.ScriptProtocol.FromScript.GraphicsMessage.call(this, e, j, h);
    this.msg = "DetachCamera";
    this.space = e + j;
    this.id = h
  }, GFXEnableEvent:function(e, j) {
    this.msg = "Enable";
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.space = e;
    this.type = j
  }, GFXDisableEvent:function(e, j) {
    this.msg = "Disable";
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.space = e;
    this.type = j
  }, GFXRaytrace:function(e, j, h, o, q, u) {
    this.msg = "Raytrace";
    this.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    this.space = e;
    this.requestid = j;
    this.pos = h;
    this.dir = o;
    this.multiple = q;
    this.infinite = u
  }}, ToScript:{Types:{Connected:"tcon", ConnectionFailed:"tfyl", Disconnected:"tdis", ReceiveODPMessage:"todp", QueryEvent:"tque", PresenceLocUpdate:"tloc", GUIMessage:"tgui"}, reconstitute:function(e) {
    return e = Kata.ScriptProtocol.commonReconstitute(e)
  }, Connected:function(e, j, h, o, q) {
    this.__type = Kata.ScriptProtocol.ToScript.Types.Connected;
    this.space = e;
    this.id = j;
    this.loc = h;
    this.bounds = o;
    this.visual = q
  }, ConnectionFailed:function(e, j) {
    this.__type = Kata.ScriptProtocol.ToScript.Types.ConnectionFailed;
    this.space = e;
    this.reason = j
  }, Disconnected:function(e) {
    this.__type = Kata.ScriptProtocol.ToScript.Types.Disconnected;
    this.space = e
  }, GUIMessage:function(e) {
    for(field in e) {
      this[field] = e[field]
    }this.__type = Kata.ScriptProtocol.ToScript.Types.GUIMessage
  }, ReceiveODPMessage:function(e, j, h, o, q, u) {
    this.__type = Kata.ScriptProtocol.ToScript.Types.ReceiveODPMessage;
    this.space = e;
    this.source_object = j;
    this.source_port = h;
    this.dest_object = o;
    this.dest_port = q;
    this.payload = u
  }, QueryEvent:function(e, j, h, o, q) {
    this.__type = Kata.ScriptProtocol.ToScript.Types.QueryEvent;
    this.space = e;
    this.observed = j;
    this.entered = h;
    this.loc = o;
    this.visual = q
  }, PresenceLocUpdate:function(e, j, h, o) {
    this.__type = Kata.ScriptProtocol.ToScript.Types.PresenceLocUpdate;
    this.space = e;
    this.observed = j;
    this.loc = h;
    this.visual = o
  }}}
}, "katajs/oh/impl/ScriptProtocol.js");Kata.require(["katajs/core/FilterChannel.js", "katajs/core/MessageDispatcher.js", "katajs/oh/Presence.js", "katajs/core/URL.js", "katajs/oh/impl/ScriptProtocol.js"], function() {
  Kata.BootstrapScript = function(e, j) {
    this.mChannel = e;
    var h = {}, o = Kata.ScriptProtocol.ToScript.Types;
    h[o.Connected] = Kata.bind(this._handleConnected, this);
    h[o.ConnectionFailed] = Kata.bind(this._handleConnectFailed, this);
    h[o.Disconnected] = Kata.bind(this._handleDisconnect, this);
    this.mMessageDispatcher = new Kata.MessageDispatcher(h);
    this.mPresences = {};
    var q = new Kata.FilterChannel(e, Kata.bind(this.receiveMessage, this));
    this.mPendingScriptLoad = [];
    this.mScriptLoading = true;
    var u = this;
    Kata.require([j.realScript], function() {
      u._onFinishedLoading(q, j)
    })
  };
  Kata.BootstrapScript.prototype._onFinishedLoading = function(e, j) {
    this.mScriptLoading = false;
    for(var h = j.realClass.split("."), o = self, q = 0;o && q < h.length;q++) {
      o = o[h[q]]
    }if(o) {
      this.mScript = new o(e, j.realArgs);
      for(q = 0;q < this.mPendingScriptLoad.length;q++) {
        this.receiveMessage(this.mPendingScriptLoad[q][0], this.mPendingScriptLoad[q][1])
      }
    }else {
      Kata.error("Class " + j.realClass + " from file " + j.realScript + " could not be found!")
    }
  };
  Kata.BootstrapScript.prototype.receiveMessage = function(e, j) {
    if(this.mScriptLoading) {
      this.mPendingScriptLoad.push([e, j]);
      return true
    }else {
      return this.mMessageDispatcher.dispatch(e, j)
    }
  };
  Kata.BootstrapScript.prototype._handleConnected = function(e, j) {
    e = new Kata.Presence(this.mScript, Kata.URL(j.space), j.id, j.loc, j.visual);
    this.mPresences[j.space] = e;
    this.mScript.newPresence(e)
  };
  Kata.BootstrapScript.prototype._handleConnectFailed = function(e, j) {
    this.mScript.connectFailure(j.space, j.reason)
  };
  Kata.BootstrapScript.prototype._handleDisconnect = function(e, j) {
    if(e = this.mPresences[j.space]) {
      delete this.mPresences[j.space];
      this.mScript.presenceInvalidated(e, "Disconnected.")
    }
  }
}, "katajs/oh/impl/BootstrapScript.js");Kata.require(["katajs/oh/RemotePresence.js"], function() {
  var e = Kata.RemotePresence.prototype;
  Kata.Presence = function(j, h, o, q, u) {
    e.constructor.call(this, this, h, o, q, u);
    this.mScript = j;
    this.mQueryHander = this.mQuery = null;
    this.mRequestedLocation = this.mLocation;
    this.mOrphanLocUpdates = {}
  };
  Kata.extend(Kata.Presence, e);
  Kata.Presence.prototype.bindODPPort = function(j) {
    return this.mScript.bindODPPort(this.mSpace, this.mID, j)
  };
  Kata.Presence.prototype._sendHostedObjectMessage = function(j) {
    return this.mScript._sendHostedObjectMessage(j)
  };
  Kata.Presence.prototype.disconnect = function() {
    this.mScript._disconnect(this)
  };
  Kata.Presence.prototype.query = function() {
    return this.mQuery
  };
  Kata.Presence.prototype.setQuery = function(j) {
    this.mQuery = j;
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.Query(this.mSpace, this.mID, j))
  };
  Kata.Presence.prototype.setQueryHandler = function(j) {
    this.mQueryHandler = j
  };
  Kata.Presence.prototype._requestedPosition = function(j) {
    return Kata.LocationExtrapolate(this.mRequestedLocation, j).pos.concat()
  };
  Kata.Presence.prototype._requestedVelocity = function() {
    return this.mRequestedLocation.vel.concat()
  };
  Kata.Presence.prototype._requestedOrientation = function(j) {
    return Kata.LocationExtrapolate(this.mRequestedLocation, j).orient.concat()
  };
  Kata.Presence.prototype._requestedAngularSpeed = function() {
    return this.mRequestedLocation.rotvel
  };
  Kata.Presence.prototype._requestedRotationalAxis = function() {
    return this.mRequestedLocation.rotaxis.concat()
  };
  Kata.Presence.prototype._requestedRotationalVelocity = function() {
    return Kata.Quaternion.fromLocationAngularVelocity(this.mRequestedLocation)
  };
  Kata.Presence.prototype._requestedScale = function() {
    return this.mRequestedLocation.scale.concat()
  };
  Kata.Presence.prototype._requestedLocation = function() {
    var j = {};
    for(var h in this.mRequestedLocation) {
      j[h] = this.mRequestedLocation[h]
    }return j
  };
  Kata.Presence.prototype.predictedPosition = function(j) {
    return this._requestedPosition(j)
  };
  Kata.Presence.prototype.predictedVelocity = function() {
    return this._requestedVelocity()
  };
  Kata.Presence.prototype.predictedOrientation = function(j) {
    return this._requestedOrientation(j)
  };
  Kata.Presence.prototype.predictedAngularSpeed = function() {
    return this._requestedAngularSpeed()
  };
  Kata.Presence.prototype.predictedRotationalAxis = function() {
    return this._requestesdRotationalAxis()
  };
  Kata.Presence.prototype.predictedRotationalVelocity = function() {
    return this._requestesdRotationalVelocity()
  };
  Kata.Presence.prototype.predictedScale = function() {
    return this._requestedScale()
  };
  Kata.Presence.prototype.predictedLocation = function() {
    return this._requestedLocation()
  };
  Kata.Presence.prototype.setPosition = function(j) {
    var h = Kata.now(this.mSpace), o = this._requestedPosition(h);
    if(!(o[0] == j[0] && o[1] == j[1] && o[2] == j[2])) {
      j = {pos:j.concat(), vel:this._requestedVelocity(), time:Kata.now(this.mSpace)};
      o = new Kata.ScriptProtocol.FromScript.Location(this.mSpace, this.mID, j);
      this.mRequestedLocation = Kata.LocationUpdate(j, this.mRequestedLocation, null, h);
      this._sendHostedObjectMessage(o)
    }
  };
  Kata.Presence.prototype.setVelocity = function(j) {
    var h = Kata.now(this.mSpace), o = this._requestedVelocity();
    if(!(o[0] == j[0] && o[1] == j[1] && o[2] == j[2])) {
      j = {pos:this._requestedPosition(h), vel:j.concat(), time:h};
      o = new Kata.ScriptProtocol.FromScript.Location(this.mSpace, this.mID, j);
      this.mRequestedLocation = Kata.LocationUpdate(j, this.mRequestedLocation, null, h);
      this._sendHostedObjectMessage(o)
    }
  };
  Kata.Presence.prototype.setOrientation = function(j) {
    var h = Kata.now(this.mSpace), o = this._requestedOrientation(h);
    if(!(o[0] == j[0] && o[1] == j[1] && o[2] == j[2] && o[3] == j[3])) {
      j = {orient:j.concat(), rotaxis:this._requestedRotationalAxis(), rotvel:this._requestedAngularSpeed(), time:Kata.now(this.mSpace)};
      o = new Kata.ScriptProtocol.FromScript.Location(this.mSpace, this.mID, j);
      this.mRequestedLocation = Kata.LocationUpdate(j, this.mRequestedLocation, null, h);
      this._sendHostedObjectMessage(o)
    }
  };
  Kata.Presence.prototype.setAngularVelocity = function(j) {
    if(false in j) {
      j = new Kata.Quaternion(j)
    }j = j.toAngleAxis();
    var h = j.angle, o = j.axis;
    j = Kata.now(this.mSpace);
    var q = this._requestedAngularSpeed(), u = this._requestedRotationalAxis();
    if(!(q == h && u[0] == o[0] && u[1] == o[1] && u[2] == o[2])) {
      h = {orient:this._requestedOrientation(j), rotaxis:o.concat(), rotvel:h, time:j};
      o = new Kata.ScriptProtocol.FromScript.Location(this.mSpace, this.mID, h);
      this.mRequestedLocation = Kata.LocationUpdate(h, this.mRequestedLocation, null, j);
      this._sendHostedObjectMessage(o)
    }
  };
  Kata.Presence.prototype.setLocation = function(j) {
    var h = Kata.now(this.mSpace);
    if(j.time === undefined) {
      j.time = Kata.now(this.mSpace)
    }var o = new Kata.ScriptProtocol.FromScript.Location(this.mSpace, this.mID, j);
    this.mRequestedLocation = Kata.LocationUpdate(j, this.mRequestedLocation, null, h);
    this._sendHostedObjectMessage(o)
  };
  Kata.Presence.prototype.setBounds = function(j) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.Location(this.mSpace, this.mID, {bounds:j.concat(), time:Kata.now(this.mSpace)}))
  };
  Kata.Presence.prototype.setScale = function(j) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.Location(this.mSpace, this.mID, {scale:j.concat(), time:Kata.now(this.mSpace)}))
  };
  Kata.Presence.prototype.setVisual = function(j) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.Visual(this.mSpace, this.mID, j))
  };
  Kata.Presence.prototype.remotePresence = function(j, h) {
    this.mQueryHandler && this.mQueryHandler(j, h);
    var o = j.presenceID(), q = this.mOrphanLocUpdates[o];
    if(h && q !== undefined) {
      for(h = 0;h < q.length;h++) {
        j._updateLoc(q[h].loc, q[h].visual)
      }delete this.mOrphanLocUpdates[o]
    }
  };
  Kata.Presence.prototype.subscribe = function(j) {
    this.mParent._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.Subscription(this.mSpace, this.mID, j, true))
  };
  Kata.Presence.prototype.unsubscribe = function(j) {
    this.mParent._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.Subscription(this.mSpace, this.mID, j, false))
  };
  Kata.Presence.prototype.onDisconnected = function() {
    Kata.notImplemented("Presence.onDisconnected")
  };
  Kata.Presence.prototype.handleSpaceEvent = function() {
    Kata.notImplemented("Presence.handleSpaceEvent")
  };
  Kata.Presence.prototype._handleDisconnect = function() {
    Kata.notImplemented("Presence._handleDisconnect")
  };
  Kata.Presence.prototype._handleLocEvent = function(j, h) {
    Kata.now(this.mSpace);
    if(this.id() === j.observed) {
      this._updateLoc(j.loc, j.visual);
      return this
    }else {
      var o = Kata.Script.remotePresenceKey(j.space, j.observed);
      if(h = h[o]) {
        h._updateLoc(j.loc, j.visual)
      }else {
        o = new Kata.PresenceID(j.space, j.observed);
        this.mOrphanLocUpdates[o] || (this.mOrphanLocUpdates[o] = []);
        this.mOrphanLocUpdates[o].push(j);
        setTimeout(Kata.bind(this._clearOrphanLocUpdates, this, o), 6E4)
      }return h
    }
  };
  Kata.Presence.prototype._clearOrphanLocUpdates = function(j) {
    delete this.mOrphanLocUpdates[j]
  };
  Kata.Presence.prototype._handleVisualEvent = function() {
    Kata.notImplemented("Presence._handleVisualEvent")
  };
  Kata.Presence.prototype._handleQueryEvent = function() {
    Kata.notImplemented("Presence._handleQueryEvent")
  }
}, "katajs/oh/Presence.js");Kata.require(["katajs/core/Channel.js", "katajs/core/WebWorker.js"], function() {
  Kata.MainThread = function(e, j, h) {
    this.mObjectHostWorker = new Kata.FakeWebWorker("katajs/oh/ObjectHostWorker.js", "Kata.ObjectHostWorker", {script:e, method:j, args:h});
    this.mObjectHostChannel = this.mObjectHostWorker.getChannel();
    this.mObjectHostChannel.registerListener(Kata.bind(this.receivedMessage, this));
    this.mObjectHostWorker.go()
  };
  Kata.MainThread.prototype.getChannel = function() {
    return this.mObjectHostChannel
  };
  Kata.MainThread.prototype.receivedMessage = function() {
  }
}, "katajs/oh/MainThread.js");Kata.require(["katajs/oh/ObjectHost.js"], function() {
  Kata.ObjectHostWorker = function(e, j) {
    this.mObjectHost = new Kata.ObjectHost(j.script, j.method, j.args);
    this.mObjectHost.registerSimulation(e, "graphics")
  }
}, "katajs/oh/ObjectHostWorker.js");Kata.require(["katajs/oh/impl/ScriptProtocol.js", "katajs/oh/Presence.js", "katajs/oh/RemotePresence.js", "katajs/oh/odp/Port.js", "katajs/oh/odp/Service.js"], function() {
  Kata.Script = function(e) {
    Kata.ODP.Service.prototype.constructor.call(this, Kata.bind(this._sendODPMessage, this));
    this.mChannel = e;
    this.mChannel.registerListener(Kata.bind(this._handleHostedObjectMessage, this));
    this.mPresences = {};
    this.mRemotePresences = {};
    this.mConnectRequests = {};
    e = {};
    var j = Kata.ScriptProtocol.ToScript.Types;
    e[j.ReceiveODPMessage] = Kata.bind(this._handleReceiveODPMessage, this);
    e[j.QueryEvent] = Kata.bind(this._handleQueryEvent, this);
    e[j.PresenceLocUpdate] = Kata.bind(this._handlePresenceLocUpdate, this);
    this.mMessageDispatcher = new Kata.MessageDispatcher(e);
    this.mBehaviors = []
  };
  Kata.extend(Kata.Script, Kata.ODP.Service.prototype);
  Kata.Script.prototype.addBehavior = function(e) {
    this.mBehaviors.push(e)
  };
  Kata.Script.prototype._sendHostedObjectMessage = function(e) {
    return this.mChannel.sendMessage(e)
  };
  Kata.Script.prototype.connect = function(e, j, h) {
    j = new Kata.ScriptProtocol.FromScript.Connect(e.space, j, e.loc, e.visual);
    this.mConnectRequests[e.space] = h;
    this._sendHostedObjectMessage(j)
  };
  Kata.Script.prototype._disconnect = function(e) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.Disconnect(e.space(), e.id()))
  };
  Kata.Script.prototype.newPresence = function(e) {
    this.mPresences[e.space()] = e;
    var j = this.mConnectRequests[e.space()];
    if(j) {
      delete this.mConnectRequests[e.space()];
      j(e)
    }this.mBehaviors.forEach(function(h) {
      h.newPresence && h.newPresence(e)
    })
  };
  Kata.Script.prototype.connectFailure = function(e, j) {
    var h = this.mConnectRequests[e];
    if(h) {
      delete this.mConnectRequests[e];
      h(e, j)
    }
  };
  Kata.Script.prototype.presenceInvalidated = function(e) {
    this.mPresences[e.space()] && delete this.mPresences[e.space()];
    this.mBehaviors.forEach(function(j) {
      j.presenceInvalidated && j.presenceInvalidated(e)
    })
  };
  Kata.Script.prototype.timer = function() {
    return null
  };
  Kata.Script.prototype.createObject = function(e, j, h) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.CreateObject(e, j, h))
  };
  Kata.Script.prototype.Persistence = {};
  Kata.Script.prototype.Persistence.read = function() {
    Kata.notImplemented("Script.read")
  };
  Kata.Script.prototype.Persistence.write = function() {
    Kata.notImplemented("Script.write")
  };
  Kata.Script.prototype._handleHostedObjectMessage = function(e, j) {
    j = Kata.ScriptProtocol.ToScript.reconstitute(j);
    this.mMessageDispatcher.dispatch(e, j)
  };
  Kata.Script.remotePresenceKey = function(e, j) {
    return e + j
  };
  Kata.Script.prototype.getRemotePresence = function(e) {
    return this.mRemotePresences[Kata.Script.remotePresenceKey(e.space(), e.object())]
  };
  Kata.Script.prototype._handleQueryEvent = function(e, j) {
    var h = this.mPresences[j.space], o = null, q = Kata.Script.remotePresenceKey(j.space, j.observed);
    if(j.entered) {
      if(o = this.mRemotePresences[q]) {
        o._doKill = false
      }else {
        o = new Kata.RemotePresence(h, j.space, j.observed, j.loc, j.visual);
        this.mRemotePresences[q] = o;
        h.remotePresence(o, true);
        this.mBehaviors.forEach(function(f) {
          f.remotePresence && f.remotePresence(h, o, true)
        });
        this._handleQueryEventDelegate(o, j)
      }
    }else {
      o = this.mRemotePresences[q];
      if(!o) {
        Kata.warn("Got removal prox event for unknown object.");
        return o
      }o._doKill = true;
      var u = this;
      setTimeout(function() {
        delete u.mRemotePresences[q];
        h.remotePresence(o, false);
        u.mBehaviors.forEach(function(f) {
          f.remotePresence && f.remotePresence(h, o, false)
        });
        u._handleQueryEventDelegate(o, j)
      }, 1E4)
    }return o
  };
  Kata.Script.prototype._handleQueryEventDelegate = function() {
  };
  Kata.Script.prototype._sendODPMessage = function(e, j, h) {
    if(!Kata.URL.equals(e.space(), j.space())) {
      throw"Mismatching spaces in ODP message.";
    }this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.SendODPMessage(e.space(), e.object(), e.port(), j.object(), j.port(), h))
  };
  Kata.Script.prototype._handleReceiveODPMessage = function(e, j) {
    this._deliverODPMessage(new Kata.ODP.Endpoint(j.space, j.source_object, j.source_port), new Kata.ODP.Endpoint(j.space, j.dest_object, j.dest_port), j.payload)
  };
  Kata.Script.prototype._handlePresenceLocUpdate = function(e, j) {
    if(e = this.mPresences[j.space]) {
      return e._handleLocEvent(j, this.mRemotePresences)
    }else {
      Kata.warn("Got loc update destined for unknown object.");
      return e
    }
  };
  Kata.Script.prototype._handleStorageEvent = function() {
  }
}, "katajs/oh/Script.js");Kata.require(["katajs/oh/Simulation.js"], function() {
  var e = Kata.Simulation.prototype;
  Kata.GUISimulation = function(j) {
    e.constructor.call(this, j)
  };
  Kata.extend(Kata.GUISimulation, e);
  Kata.GUISimulation.prototype.receivedMessage = function(j, h) {
    h.__gui && this.handleGUIMessage(h.__gui)
  };
  Kata.GUISimulation.prototype.handleGUIMessage = function() {
  }
}, "katajs/oh/GUISimulation.js");Kata.require(["katajs/core/Deque.js", ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/SSTHeader.pbj.js"], ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/ObjectMessage.pbj.js"]], function() {
  var e = function(D, G) {
    D.push_back(G)
  }, j = function(D, G) {
    return D.push_front(G)
  }, h = function(D) {
    return D.pop_front()
  }, o = function(D) {
    return D.front()
  }, q = function(D) {
    return D.size()
  }, u = function(D) {
    return D.empty()
  }, f = function(D, G) {
    return D.index(G)
  }, g = function(D) {
    return D.clear()
  }, m = function(D, G) {
    return D.erase(G)
  };
  if(typeof Kata.SST == "undefined") {
    Kata.SST = {}
  }if(typeof Kata.SST.Impl == "undefined") {
    Kata.SST.Impl = {}
  }Kata.SST.ObjectMessageDispatcher = function() {
    this.mObjectMessageRecipients = {}
  };
  Kata.SST.ObjectMessageDispatcher.prototype.registerObjectMessageRecipient = function(D, G) {
    this.mObjectMessageRecipients[D] = G
  };
  Kata.SST.ObjectMessageDispatcher.prototype.unregisterObjectMessageRecipient = function(D, G) {
    if(this.mObjectMessageRecipients[D] != G) {
      Kata.log("Unregistering wrong recipient for port " + D)
    }else {
      delete this.mObjectMessageRecipients[D]
    }
  };
  Kata.SST.ObjectMessageDispatcher.prototype.dispatchMessage = function(D) {
    if(D.dest_port in this.mObjectMessageRecipients) {
      return this.mObjectMessageRecipients[D.dest_port].receiveMessage(D)
    }return false
  };
  Kata.SST.EndPoint = function(D, G) {
    this.endPoint = D;
    this.port = G
  };
  Kata.SST.EndPoint.prototype.uid = function() {
    return"" + this.endPoint + ":" + this.port
  };
  Kata.SST.EndPoint.prototype.toString = Kata.SST.EndPoint.prototype.uid;
  Kata.SST.EndPoint.prototype.objectId = function() {
    return this.endPoint
  };
  Kata.SST.Impl.BaseDatagramLayer = function(D, G, I) {
    this.mRouter = D;
    this.mDispatcher = G;
    this.mContext = I;
    this.mMinAvailableChannels = 1;
    this.mMinAvailablePorts = 2049;
    this.mAvailableChannels = [];
    this.mAvailablePorts = []
  };
  var p = {}, r = {}, s = {}, A = function(D) {
    D = D.objectId();
    if(D in p) {
      return p[D]
    }return null
  };
  Kata.SST.createBaseDatagramLayer = function(D, G, I) {
    D = D.objectId();
    if(D in p) {
      return p[D]
    }return p[D] = new Kata.SST.Impl.BaseDatagramLayer(G, I)
  };
  var v = function(D) {
    var G = D.objectId();
    if(G = p[G]) {
      G.mDispatcher.registerObjectMessageRecipient(D.port, G);
      return true
    }else {
      return false
    }
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.context = function() {
    return this.mContext
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.send = function(D, G, I) {
    var F = new Sirikata.Protocol.Object.ObjectMessage;
    F.source_object = D.objectId();
    F.source_port = D.port;
    F.dest_object = G.objectId();
    F.dest_port = G.port;
    F.unique = PROTO.I64.fromNumber(0);
    F.payload = I;
    return this.mRouter.route(F)
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.receiveMessage = function(D) {
    return M(this, new Kata.SST.EndPoint(D.source_object, D.source_port), new Kata.SST.EndPoint(D.dest_object, D.dest_port), D.payload)
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.dispatcher = function() {
    return this.mDispatcher
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.getAvailablePort = function() {
    var D = this.mAvailablePorts.length;
    if(D) {
      this.mAvailabePorts.length = D - 1
    }return this.mMinAvailablePorts++
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.releasePort = function(D) {
    if(!(D <= 2048)) {
      if(D + 1 == this.mMinAvailablePorts) {
        --this.mMinAvailablePorts
      }else {
        this.mAvailablePorts[this.mAvailablePorts.length] = D
      }
    }
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.getAvailableChannel = function() {
    var D = this.mAvailableChannels.length;
    if(D) {
      this.mAvailabeChannels.length = D - 1
    }return this.mMinAvailableChannels++
  };
  Kata.SST.Impl.BaseDatagramLayer.prototype.releaseChannel = function(D) {
    if(D + 1 == this.mMinAvailableChannels) {
      --this.mMinAvailableChannels
    }else {
      this.mAvailableChannels[this.mAvailableChannels.length] = D
    }
  };
  Kata.SST.SUCCESS = 0;
  Kata.SST.FAILURE = -1;
  Kata.SST.Impl.ChannelSegment = function(D, G, I) {
    this.mBuffer = D;
    this.mChannelSequenceNumber = G;
    this.mAckSequenceNumber = I;
    this.mAckTime = this.mTransmitTime = null
  };
  Kata.SST.Impl.ChannelSegment.prototype.setAckTime = function(D) {
    this.mAckTime = D
  };
  Kata.SST.Connection = function(D, G) {
    this.mLocalEndPoint = D;
    this.mRemoteEndPoint = G;
    this.mState = C;
    this.mRemoteChannelID = 0;
    this.mLocalChannelID = 1;
    this.mLastReceivedSequenceNumber = this.mTransmitSequenceNumber = PROTO.I64.ONE;
    this.mPartialReadDatagrams = {};
    this.mNumStreams = 0;
    this.mCwnd = 1;
    this.mRTOMilliseconds = 60.125;
    this.mFirstRTO = true;
    this.mLastTransmitTime = new Date;
    this.inSendingMode = true;
    this.numSegmentsSent = 0;
    this.mDatagramLayer = A(D);
    this.mDatagramLayer.dispatcher().registerObjectMessageRecipient(D.port, this);
    this.mOutgoingSubstreamMap = {};
    this.mIncomingSubstreamMap = {};
    this.mListeningStreamsCallbackMap = {};
    this.mReadDatagramCallbacks = {};
    this.mQueuedSegments = new Kata.Deque;
    this.mOutstandingSegments = new Kata.Deque
  };
  Kata.SST.Connection.prototype.getContext = function() {
    return this.mDatagramLayer.context()
  };
  Kata.SST.Connection.prototype.sendSSTChannelPacket = function(D) {
    if(this.mState == C) {
      return false
    }return this.mDatagramLayer.send(this.mLocalEndPoint, this.mRemoteEndPoint, D.SerializeToArray())
  };
  Kata.SST.Connection.prototype.serviceConnection = function() {
    var D = new Date;
    if(this.mState == C) {
      setTimeout(Kata.bind(this.cleanup, this), 0);
      return false
    }else {
      if(this.mState == E) {
        if(u(this.mQueuedSegments)) {
          setTimeout(Kata.bind(this.cleanup, this), 0);
          this.mState = C;
          return false
        }
      }
    }if(this.inSendingMode) {
      for(var G = this.numSegmentsSent = 0;!u(this.mQueuedSegments) && q(this.mOutstandingSegments) <= this.mCwnd;++G) {
        var I = o(this.mQueuedSegments), F = new Sirikata.Protocol.SST.SSTChannelHeader;
        F.channel_id = this.mRemoteChannelID;
        F.transmit_sequence_number = I.mChannelSequenceNumber;
        F.ack_count = 1;
        F.ack_sequence_number = I.mAckSequenceNumber;
        F.payload = I.mBuffer;
        this.sendSSTChannelPacket(F);
        I.mTransmitTime = D;
        e(this.mOutstandingSegments, I);
        h(this.mQueuedSegments);
        this.numSegmentsSent++;
        this.mLastTransmitTime = D;
        this.inSendingMode = false
      }this.inSendingMode || setTimeout(Kata.bind(this.serviceConnection, this), this.mRTOMilliseconds)
    }else {
      if(!u(this.mOutstandingSegments)) {
        this.mCwnd /= 2;
        if(this.mCwnd < 1) {
          this.mCwnd = 1
        }g(this.mOutstandingSegments)
      }this.inSendingMode = true;
      setTimeout(Kata.bind(this.serviceConnection, this), 0)
    }return true
  };
  var B = {}, C = 1, E = 5, H = function(D, G, I) {
    var F = D.uid();
    if(F in B) {
      Kata.log("mConnectionMap.find failed for " + D.uid());
      return false
    }G = new Kata.SST.Connection(D, G);
    B[F] = G;
    r[F] = I;
    G.setState(2);
    D = A(D).getAvailableChannel();
    I = [D >> 8 & 255, D & 255];
    G.setLocalChannelID(D);
    G.sendData(I, false);
    return true
  }, J = function(D, G) {
    if(!v(G)) {
      return false
    }G = G.uid();
    if(G in s) {
      return false
    }s[G] = D;
    return true
  };
  Kata.SST.Connection.prototype.getNewLSID = function() {
    return++this.mNumStreams
  };
  Kata.SST.Connection.prototype.releaseLSID = function() {
  };
  Kata.SST.Connection.prototype.listenStream = function(D, G) {
    this.mListeningStreamsCallbackMap[D] = G
  };
  Kata.SST.Connection.prototype.stream = function(D, G, I, F, L) {
    if(L === undefined) {
      L = 0
    }var O = Math.uuid(), P = this.getNewLSID();
    D = new Kata.SST.Stream(L, this, I, F, O, P, G, false, 0, D);
    return this.mOutgoingSubstreamMap[P] = D
  };
  Kata.SST.Connection.prototype.sendData = function(D, G) {
    D.length > 1300 && Kata.log("Data longer than MAX_PAYLOAD_SIZE OF 1300");
    G === undefined && Kata.log("sendData not setting whether it is an ack");
    var I = this.mTransmitSequenceNumber;
    if(G) {
      G = new Sirikata.Protocol.SST.SSTChannelHeader;
      G.channel_id = this.mRemoteChannelID;
      G.transmit_sequence_number = this.mTransmitSequenceNumber;
      G.ack_count = 1;
      G.ack_sequence_number = this.mLastReceivedSequenceNumber;
      G.payload = D;
      this.sendSSTChannelPacket(G)
    }else {
      if(q(this.mQueuedSegments) < 300) {
        e(this.mQueuedSegments, new Kata.SST.Impl.ChannelSegment(D, this.mTransmitSequenceNumber, this.mLastReceivedSequenceNumber));
        this.inSendingMode && setTimeout(Kata.bind(this.serviceConnection, this))
      }
    }this.mTransmitSequenceNumber = this.mTransmitSequenceNumber.unsigned_add(PROTO.I64.ONE);
    return I
  };
  Kata.SST.Connection.prototype.setState = function(D) {
    this.mState = D
  };
  Kata.SST.Connection.prototype.setLocalChannelID = function(D) {
    this.mLocalChannelID = D
  };
  Kata.SST.Connection.prototype.setRemoteChannelID = function(D) {
    this.mRemoteChannelID = D
  };
  Kata.SST.Connection.prototype.markAcknowledgedPacket = function(D) {
    for(var G = q(this.mOutstandingSegments), I = 0;I < G;I++) {
      var F = f(this.mOutstandingSegments, I);
      if(F.mChannelSequenceNumber.equals(D)) {
        F.mAckTime = new Date;
        if(this.mFirstRTO) {
          this.mRTOMilliseconds = F.mAckTime - F.mTransmitTime;
          this.mFirstRTO = false
        }else {
          this.mRTOMilliseconds = 0.8 * this.mRTOMilliseconds + (1 - 0.8) * (F.mAckTime - F.mTransmitTime)
        }this.inSendingMode = true;
        if(Math.random() * this.mCwnd < 1) {
          this.mCwnd += 1
        }m(this.mOutstandingSegments, I);
        break
      }
    }
  };
  Kata.SST.Connection.prototype.parsePacket = function(D) {
    var G = new Sirikata.Protocol.SST.SSTStreamHeader;
    G.ParseFromArray(D.payload);
    if(G.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.INIT) {
      this.handleInitPacket(G)
    }else {
      if(G.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.REPLY) {
        this.handleReplyPacket(G)
      }else {
        if(G.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.DATA) {
          this.handleDataPacket(G)
        }else {
          if(G.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.ACK) {
            this.handleAckPacket(D, G)
          }else {
            G.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.DATAGRAM && this.handleDatagram(G)
          }
        }
      }
    }
  };
  Kata.SST.Connection.prototype.headerToStringDebug = function(D) {
    return this.mLocalEndPoint + "-> " + this.mRemoteEndPoint + " LSID:" + D.lsid
  };
  Kata.SST.Connection.prototype.handleInitPacket = function(D) {
    var G = D.lsid;
    if(G in this.mIncomingSubstreamMap) {
      Kata.log("Init message for connected stream" + this.headerToStringDebug(D));
      this.mIncomingSubstreamMap[G].sendReplyPacket(undefined, G)
    }else {
      var I = this.mListeningStreamsCallbackMap[D.dest_port];
      if(I) {
        var F = Math.uuid(), L = this.getNewLSID();
        F = new Kata.SST.Stream(D.psid, this, D.dest_port, D.src_port, F, L, [], true, G, null);
        this.mOutgoingSubstreamMap[L] = F;
        this.mIncomingSubstreamMap[G] = F;
        I(0, F);
        F.receiveData(D, D.payload, PROTO.I64.fromNumber(D.bsn))
      }else {
        Kata.log("Not listening to streams at: " + this.headerToStringDebug(D))
      }
    }
  };
  Kata.SST.Connection.prototype.handleReplyPacket = function(D) {
    var G = D.lsid;
    if(this.mIncomingSubstreamMap[G]) {
      Kata.log("Received reply packet for already connected stream\n" + this.headerToStringDebug(D))
    }else {
      var I = this.mOutgoingSubstreamMap[D.rsid];
      if(I) {
        this.mIncomingSubstreamMap[G] = I;
        if(I.mStreamReturnCallback) {
          I.mStreamReturnCallback(Kata.SST.SUCCESS, I);
          I.receiveData(D, D.payload, PROTO.I64.fromNumber(D.bsn))
        }
      }else {
        Kata.log("Received reply packet for unknown stream\n" + this.headerToStringDebug(D))
      }
    }
  };
  Kata.SST.Connection.prototype.handleDataPacket = function(D) {
    var G = this.mIncomingSubstreamMap[D.lsid];
    G && G.receiveData(D, D.payload, PROTO.I64.fromNumber(D.bsn))
  };
  Kata.SST.Connection.prototype.handleAckPacket = function(D, G) {
    var I = this.mIncomingSubstreamMap[G.lsid];
    I && I.receiveData(G, G.payload, D.ack_sequence_number)
  };
  Kata.SST.Connection.prototype.handleDatagram = function(D) {
    if(D.flags & Sirikata.Protocol.SST.SSTStreamHeader.CONTINUES) {
      if(not(D.lsid in this.mPartialReadDatagrams)) {
        this.mPartialReadDatagrams[D.lsid] = []
      }this.mPartialReadDatagrams[D.lsid].push(D.payload)
    }else {
      var G = D.dest_port, I = [];
      if(G in this.mReadDatagramCallbacks) {
        I = this.mReadDatagramCallbacks[G]
      }G = I.length;
      var F = this.mPartialReadDatagrams[D.lsid];
      if(F) {
        for(var L = [], O = F.length, P = 0;P < O;++P) {
          L = Array.concat(L, F[P])
        }L += D.payload;
        delete this.mPartialReadDatagrams[F];
        for(F = 0;F < G;F++) {
          I[F](L)
        }
      }else {
        for(F = 0;F < G;F++) {
          I[F](D.payload)
        }
      }
    }D = new Sirikata.Protocol.SST.SSTChannelHeader;
    D.channel_id = this.mRemoteChannelID;
    D.transmit_sequence_number = this.mTransmitSequenceNumber;
    D.ack_count = 1;
    D.ack_sequence_number = this.mLastReceivedSequenceNumber;
    this.sendSSTChannelPacket(D);
    this.mTransmitSequenceNumber = this.mTransmitSequenceNumber.unsigned_add(PROTO.I64.ONE)
  };
  Kata.SST.Connection.prototype.receiveMessage = function(D) {
    D = D.payload;
    var G = new Sirikata.Protocol.SST.SSTChannelHeader;
    G.ParseFromArray(D);
    this.mLastReceivedSequenceNumber = G.transmit_sequence_number;
    this.markAcknowledgedPacket(G.ack_sequence_number);
    if(this.mState == 2) {
      this.mState = 4;
      new Kata.SST.EndPoint(this.mRemoteEndPoint.endPoint, this.mRemoteEndPoint.port);
      this.setRemoteChannelID(G.payload[0] * 256 + G.payload[1]);
      this.mRemoteEndPoint.port = G.payload[2] * 256 + G.payload[3];
      this.sendData([], false);
      D = this.mLocalEndPoint.uid();
      if(G = r[D]) {
        delete r[D];
        G(Kata.SST.SUCCESS, this)
      }
    }else {
      if(this.mState == 3) {
        this.mState = 4
      }else {
        this.mState == 4 && G.payload && G.payload.length > 0 && this.parsePacket(G)
      }
    }return true
  };
  Kata.SST.Connection.prototype.eraseDisconnectedStream = function(D) {
    delete this.mOutgoingSubstreamMap[D.mLSID]
  };
  Kata.SST.Connection.prototype.finalize = function() {
    this.mDatagramLayer.dispatcher().unregisterObjectMessageRecipient(this.mLocalEndPoint.port, this);
    if(this.mState != C) {
      this.mState = C;
      this.close(true)
    }
  };
  Kata.SST.Connection.prototype.cleanup = function() {
    var D = this.mState;
    if(D == 2 || D == C) {
      var G = null, I = this.mLocalEndPoint.uid();
      G = r[I];
      delete r[I];
      delete B[I];
      D == 2 && G && G(Kata.SST.FAILURE, this)
    }
  };
  Kata.SST.Connection.prototype.datagram = function(D, G, I, F) {
    var L = 0;
    if(this.mState == C || this.mState == E) {
      F && F(Kata.SST.FAILURE, D);
      return false
    }for(var O = this.getNewLSID(), P = D.length;L < P;) {
      for(var S = 28;;) {
        var T, U = true;
        if(P - L > 1300 - S) {
          T = 1300 - S;
          U = true
        }else {
          T = P - L;
          U = false
        }var V = new Sirikata.Protocol.SST.SSTStreamHeader;
        V.lsid = O;
        V.type = Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.DATAGRAM;
        var W = 0;
        if(U) {
          W |= Sirikata.Protocol.SST.SSTStreamHeader.CONTINUES
        }V.flags = W;
        V.window = 10;
        V.src_port = G;
        V.dest_port = I;
        V.payload = D.slice(L, L + T);
        U = V.SerializeToArray();
        if(U.length > 1300) {
          S += 10
        }else {
          this.sendData(U, false);
          L += T;
          break
        }
      }
    }F && F(Kata.SST.SUCCESS, D);
    return true
  };
  Kata.SST.Connection.prototype.registerReadDatagramCallback = function(D, G) {
    D in this.mReadDatagramCallbacks || (this.mReadDatagramCallbacks[D] = []);
    this.mReadDatagramCallbacks[D].push(G);
    return true
  };
  Kata.SST.Connection.prototype.registerReadOrderedDatagramCallback = function() {
    throw"UNIMPLEMENTED";
  };
  Kata.SST.Connection.prototype.close = function(D) {
    D && this.mState != C && delete B[this.mLocalEndPoint.uid()];
    this.mState = D ? C : E
  };
  var M = function(D, G, I, F) {
    var L = I.uid(), O = B[L], P = s[L];
    if(!O && !P) {
      Kata.log("whichLocal and listening are both null for " + L);
      return false
    }var S = new Sirikata.Protocol.SST.SSTChannelHeader;
    F = S.ParseFromArray(F);
    var T = S.channel_id;
    if(O) {
      if(T == 0) {
        Kata.log("Someone's already connected at this port on object " + I.endPoint.uid());
        return true
      }O.receiveParsedMessage(F)
    }else {
      if(T == 0) {
        if(P) {
          L = S.payload;
          O = D.getAvailableChannel();
          D = D.getAvailablePort();
          P = new Kata.SST.EndPoint(I.endPoint, D);
          G = new Kata.SST.Connection(P, G);
          G.listenStream(P.port, s[I]);
          B[P.uid()] = G;
          G.setLocalChannelID(O);
          G.setRemoteChannelID(L[0] * 256 + L[1]);
          G.setState(3);
          G.sendData([O >> 8 & 255, O & 255, D >> 8 & 255, D & 255], false)
        }else {
          Kata.log("Got non-init message on port we're listening on: " + L)
        }
      }
    }return true
  }, K = function(D, G) {
    this.mAckTime = this.mTransmitTime = null;
    this.mBuffer = D;
    this.mOffset = G
  }, N = 1 - 0.8, Q = {};
  Kata.SST.connectStream = function(D, G, I) {
    var F = D.uid();
    if(Q[F]) {
      return false
    }Q[F] = I;
    return H(D, G, R)
  };
  Kata.SST.listenStream = function(D, G) {
    return J(D, G)
  };
  Kata.SST.Stream = function(D, G, I, F, L, O, P, S, T, U) {
    this.mState = 4;
    this.mLocalPort = I;
    this.mRemotePort = F;
    this.mParentLSID = D;
    this.mConnection = G;
    this.mUSID = L;
    this.mLSID = O;
    this.mStreamRTOMilliseconds = 60.125;
    this.mReceiveWindowSize = this.mTransmitWindowSize = 1E4;
    this.mNumOutstandingBytes = 0;
    this.mNextByteExpected = PROTO.I64.ZERO;
    this.mLastContiguousByteReceived = PROTO.I64.fromNumber(-1);
    this.mLastSendTime = null;
    this.mStreamReturnCallback = U;
    this.mConnected = false;
    if(S) {
      this.mConnected = true;
      this.mState = 2
    }this.mInitialData = P ? P.length <= 1E3 ? P : P.slice(0, 1E3) : [];
    this.mReceiveBuffer = [];
    this.mQueuedBuffers = new Kata.Deque;
    this.mChannelToBufferMap = {};
    this.mChannelToStreamOffsetMap = {};
    this.mCurrentQueueLength = 0;
    S ? this.sendReplyPacket(this.mInitialData, T) : this.sendInitPacket(this.mInitialData);
    this.mNumInitRetransmissions = 1;
    this.mNumBytesSent = PROTO.I64.fromNumber(this.mInitialDataLength || 0);
    P.length > this.mInitialData.length && this.write(P.slice(this.mInitialData.length, P.length))
  };
  Kata.SST.Stream.prototype.finalize = function() {
    this.close(true)
  };
  Kata.SST.Stream.prototype.datagram = function(D, G, I, F) {
    return this.mConnection.datagram(D, G, I, F)
  };
  Kata.SST.Stream.prototype.listenSubstream = function(D, G) {
    this.mConnection.listenStream(D, G)
  };
  Kata.SST.Stream.prototype.write = function(D) {
    if(this.mState == 1 || this.mState == 3) {
      return-1
    }var G = 0, I = D.length;
    if(I <= 1E3) {
      if(this.mCurrentQueueLength + I > 4E6) {
        return 0
      }e(this.mQueuedBuffers, new K(D, this.mNumBytesSent));
      this.mCurrentQueueLength += I;
      this.mNumBytesSent = this.mNumBytesSent.unsigned_add(PROTO.I64.fromNumber(I));
      setTimeout(Kata.bind(this.serviceStream, this), 0);
      return I
    }else {
      for(var F = 0;F < I;) {
        var L = I - F > 1E3 ? 1E3 : I - F;
        if(this.mCurrentQueueLength + L > 4E6) {
          break
        }e(this.mQueuedBuffers.push_back, new K(D.slice(F, F + L), this.mNumBytesSent));
        F += L;
        this.mCurrentQueueLength += L;
        this.mNumBytesSent = this.mNumBytesSent.unsigned_add(PROTO.I64.fromNumber(L));
        G++
      }setTimeout(Kata.bind(this.serviceStream, this), 0);
      return F
    }
  };
  Kata.SST.Stream.prototype.registerReadCallback = function(D) {
    this.mReadCallback = D;
    this.sendToApp(0);
    return true
  };
  Kata.SST.Stream.prototype.close = function(D) {
    if(D) {
      this.mConnected = false;
      this.mConnection && this.mConnection.eraseDisconnectedStream(this);
      this.mState = 1;
      return true
    }else {
      if(this.mState != 1) {
        this.mState = 3;
        return true
      }else {
        return false
      }
    }
  };
  Kata.SST.Stream.prototype.setPriority = function() {
  };
  Kata.SST.Stream.prototype.priority = function() {
    return 0
  };
  Kata.SST.Stream.prototype.connection = function() {
    return this.mConnection
  };
  Kata.SST.Stream.prototype.createChildStream = function(D, G, I, F) {
    this.mConnection.stream(D, G, length, I, F, this.mParentLSID)
  };
  Kata.SST.Stream.prototype.localEndPoint = function() {
    return new Kata.SST.EndPoint(this.mConnection.localEndPoint().endPoint, this.mLocalPort)
  };
  Kata.SST.Stream.prototype.remoteEndPoint = function() {
    return new Kata.SST.EndPoint(this.mConnection.remoteEndPoint().endPoint, this.mRemotePort)
  };
  var R = function(D, G) {
    var I = G.mLocalEndPoint, F = I.uid(), L = Q[F];
    delete Q[F];
    L || Kata.error("Callback not defined for connectionCreatedStreamSST, " + F);
    D != Kata.SST.SUCCESS ? L(Kata.SST.FAILURE, null) : G.stream(L, [], I.port, G.mRemoteEndPoint.port)
  };
  Kata.SST.Stream.prototype.serviceStream = function() {
    this.conn = this.mConnection;
    var D = new Date;
    if(this.mState != 2 && this.mState != 1) {
      if(!this.mConnected && this.mNumInitRetransmissions < 5) {
        this.sendInitPacket(this.mInitialData);
        this.mLastSendTime = D;
        this.mNumInitRetransmissions++;
        return true
      }this.mInitialDataLength = 0;
      if(this.mConnected) {
        this.mState = 2
      }else {
        delete Q[this.mConnection.mLocalEndPoint.uid()];
        D = true;
        if(this.mParentLSID == 0) {
          this.mConnection.close(true);
          D = false
        }this.mStreamReturnCallback && this.mStreamReturnCallback(Kata.SST.FAILURE, null);
        this.mStreamReturnCallback = null;
        this.mState = 1;
        D || setTimeout(Kata.bind(this.mConnection.cleanup, this.mConnection), 0);
        return false
      }
    }else {
      if(this.mState != 1) {
        if(this.mLastSendTime && D.getTime() - this.mLastSendTime.getTime() > 2 * this.mStreamRTOMilliseconds) {
          this.resendUnackedPackets();
          this.mLastSendTime = D
        }var G = function(L) {
          for(var O in L) {
            return false
          }return true
        };
        if(this.mState == 3 && u(this.mQueuedBuffers) && G(this.mChannelToBufferMap)) {
          this.mState = 1;
          this.mConnection.eraseDisconnectedStream(this);
          return true
        }for(G = false;!u(this.mQueuedBuffers);) {
          var I = o(this.mQueuedBuffers);
          if(this.mTransmitWindowSize < I.mBuffer.length) {
            break
          }var F = this.sendDataPacket(I.mBuffer, I.mOffset);
          I.mTransmitTime = D;
          G = true;
          F = F.hash();
          if(!this.mChannelToBufferMap[F]) {
            this.mChannelToBufferMap[F] = I;
            this.mChannelToStreamOffsetMap[F] = I.mOffset
          }h(this.mQueuedBuffers);
          this.mCurrentQueueLength -= I.mBuffer.length;
          this.mLastSendTime = D;
          I.mBuffer.length > this.mTransmitWindowSize && Kata.log("Failure: buffer length " + I.mBuffer.length + "is greater than trasmitwindow size" + this.mTransmitWindowSize);
          this.mTransmitWindowSize -= I.mBufferLength;
          this.mNumOutstandingBytes += I.mBufferLength
        }G && setTimeout(Kata.bind(this.serviceStream, this), this.mStreamRTOMilliseconds * 2)
      }
    }return true
  };
  Kata.SST.Stream.prototype.resendUnackedPackets = function() {
    function D(L) {
      for(var O in L) {
        return false
      }return true
    }
    for(var G in this.mChannelToBufferMap) {
      var I = this.mChannelToBufferMap[G], F = I.mBuffer.length;
      j(this.mQueuedBuffers, I);
      this.mCurrentQueueLength += F;
      if(this.mTransmitWindowSize < F) {
        F <= 0 && Kata.log("Assertion failed: channelbuffer must have size >0");
        this.mTransmitWindowSize = F
      }
    }setTimeout(Kata.bind(this.serviceStream, this), 0);
    if((G = D(this.mChannelToBufferMap)) && !u(this.mQueuedBuffers)) {
      I = o(this.mQueuedBuffers);
      if(this.mTransmitWindowSize < F) {
        this.mTransmitWindowSize = F
      }
    }this.mNumOutstandingBytes = 0;
    if(!G) {
      if(this.mStreamRTOMilliseconds < 2E3) {
        this.mStreamRTOMilliseconds *= 2
      }this.mChannelToBufferMap = {}
    }
  };
  Kata.SST.Stream.prototype.sendToApp = function(D) {
    var G = D;
    for(D = D;D < 1E4;D++) {
      if(this.mReceiveBuffer[D] !== undefined) {
        G++
      }else {
        break
      }
    }if(this.mReadCallback && G > 0) {
      this.mReadCallback(this.mReceiveBuffer.slice(0, G));
      this.mLastContiguousByteReceived = this.mLastContiguousByteReceived.add(PROTO.I64.fromNumber(G));
      this.mNextByteExpected = this.mLastContiguousByteReceived.unsigned_add(PROTO.I64.ONE);
      var I = 1E4 - G;
      for(D = 0;D < I;D++) {
        this.mReceiveBuffer[D] = this.mReceiveBuffer[D + G]
      }for(;D < 1E4;++D) {
        this.mReceiveBuffer[D] = undefined
      }this.mReceiveBuffer.length = I;
      this.mReceiveWindowSize += G
    }
  };
  Kata.SST.Stream.prototype.receiveData = function(D, G, I) {
    if(D.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.REPLY) {
      this.mConnected = true
    }else {
      if(D.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.DATA || D.type == Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.INIT) {
        Math.pow(2, D.window) - this.mNumOutstandingBytes < 0.5 && Kata.log("Assertion failed: 2^" + D.window + " <= " + this.mNumOutstandingBytes);
        this.mTransmitWindowSize = Math.round(Math.pow(2, D.window) - this.mNumOutstandingBytes);
        var F = I.sub(this.mLastContiguousByteReceived).lsw - 1;
        if(I.lsw == this.mNextByteExpected.lsw) {
          if(F + G.length <= 1E4) {
            var L = G.length;
            this.mReceiveWindowSize -= L;
            for(var O = 0;O < L;++O) {
              var P = F + O;
              this.mReceiveBuffer[P] = G[O]
            }this.sendToApp(L);
            this.sendAckPacket()
          }else {
            this.sendToApp(0)
          }
        }else {
          L = G.length;
          O = I.lsw + L - 1 - this.mLastContiguousByteReceived.lsw;
          if(Math.abs(O) > 2147483647) {
            O = -O
          }if(O <= 0) {
            this.sendAckPacket()
          }else {
            if(F + L <= 1E4) {
              F + L <= 0 && Kata.log("Assertion failed: Offset in Buffer " + F + "+" + L + "<=0");
              this.mReceiveWindowSize -= L;
              for(O = 0;O < L;++O) {
                P = F + O;
                this.mReceiveBuffer[P] = G[O]
              }this.sendAckPacket()
            }else {
              this.sendToApp(0)
            }
          }
        }
      }
    }G = I.hash();
    if(G in this.mChannelToBufferMap) {
      I = this.mChannelToBufferMap[G];
      L = I.mOffset;
      this.mNumOutstandingBytes -= I.mBufferLength;
      I.mAckTime = new Date;
      this.updateRTO(I.mTransmitTime, I.mAckTime);
      this.mTransmitWindowSize = Math.pow(2, D.window) - this.mNumOutstandingBytes >= 0.5 ? Math.round(pow(2, D.window) - this.mNumOutstandingBytes) : 0;
      delete this.mChannelToBufferMap[G];
      D = [];
      for(var S in this.mChannelToBufferMap) {
        this.mChannelToBufferMap[S].mOffset.equals(L) && D.push(S)
      }for(O = 0;O < D.length;O++) {
        delete this.mChannelToBufferMap[D[O]]
      }
    }else {
      if(G in this.mChannelToStreamOffsetMap) {
        L = this.mChannelToStreamOffsetMap[G];
        delete this.mChannelToStreamOffsetMap[G];
        D = [];
        for(S in this.mChannelToBufferMap) {
          this.mChannelToBufferMap[S].mOffset.equals(L) && D.push(S)
        }L = D.length;
        for(O = 0;O < L;O++) {
          delete this.mChannelToBufferMap[D[O]]
        }
      }
    }
  };
  Kata.SST.Stream.prototype.updateRTO = function() {
    var D = true;
    return function(G, I) {
      G = G.getTime();
      I = I.getTime();
      if(G > I) {
        Kata.log("Bad sample\n")
      }else {
        if(D) {
          this.mStreamRTOMilliseconds = I - G;
          D = false
        }else {
          this.mStreamRTOMilliseconds = 0.8 * this.mStreamRTOMilliseconds + N * (I - G)
        }
      }
    }
  }();
  Kata.SST.Stream.prototype.sendInitPacket = function(D) {
    var G = new Sirikata.Protocol.SST.SSTStreamHeader;
    G.lsid = this.mLSID;
    G.type = Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.INIT;
    G.flags = 0;
    G.window = Math.log(this.mReceiveWindowSize) / Math.log(2);
    G.src_port = this.mLocalPort;
    G.dest_port = this.mRemotePort;
    G.psid = this.mParentLSID;
    G.bsn = 0;
    G.payload = D;
    this.mConnection.sendData(G.SerializeToArray(), false);
    setTimeout(Kata.bind(this.serviceStream, this), 2 * this.mStreamRTOMilliseconds)
  };
  Kata.SST.Stream.prototype.sendAckPacket = function() {
    var D = new Sirikata.Protocol.SST.SSTStreamHeader;
    D.lsid = this.mLSID;
    D.type = Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.ACK;
    D.flags = 0;
    D.window = Math.log(this.mReceiveWindowSize) / Math.log(2);
    D.src_port = this.mLocalPort;
    D.dest_port = this.mRemotePort;
    this.mConnection.sendData(D.SerializeToArray(), true)
  };
  Kata.SST.Stream.prototype.sendDataPacket = function(D, G) {
    var I = new Sirikata.Protocol.SST.SSTStreamHeader;
    I.lsid = this.mLSID;
    I.type = Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.DATA;
    I.flags = 0;
    I.window = Math.log(this.mReceiveWindowSize) / Math.log(2);
    I.src_port = this.mLocalPort;
    I.dest_port = this.mRemotePort;
    I.bsn = G;
    I.payload = D;
    return this.mConnection.sendData(I.SerializeToArray(), false)
  };
  Kata.SST.Stream.prototype.sendReplyPacket = function(D, G) {
    var I = new Sirikata.Protocol.SST.SSTStreamHeader;
    I.lsid = this.mLSID;
    I.type = Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType.REPLY;
    I.flags = 0;
    I.window = Math.log(this.mReceiveWindowSize) / Math.log(2);
    I.src_port = this.mLocalPort;
    I.dest_port = this.mRemotePort;
    I.rsid = G;
    I.bsn = 0;
    I.payload = D;
    this.mConnection.sendData(I.SerializeToArray(), false)
  }
}, "katajs/oh/sst/SSTImpl.js");Kata.require(["katajs/oh/Script.js", "katajs/oh/impl/ScriptProtocol.js"], function() {
  var e = Kata.Script.prototype;
  Kata.GraphicsScript = function(j, h, o) {
    e.constructor.call(this, j, h);
    this.mRenderableRemotePresences = [];
    this.mRenderableRemotePresenceIndex = 0;
    this.mGraphicsTimer = null;
    this.mNumGraphicsSystems = 0;
    this._camPos = [0, 0, 0];
    this._camPosTarget = [0, 0, 0];
    this._camOrient = [0, 0, 0, 1];
    this._camOrientTarget = [0, 0, 0, 1];
    this._camLag = 0.9;
    this.mMessageDispatcher.add(Kata.ScriptProtocol.ToScript.Types.GUIMessage, Kata.bind(this._handleGUIMessage, this));
    this.mUpdateHook = o
  };
  Kata.extend(Kata.GraphicsScript, e);
  Kata.GraphicsScript.prototype._handleGUIMessage = function() {
  };
  Kata.GraphicsScript.prototype.enableGraphicsViewport = function(j, h, o) {
    this._enableGraphics(j, h, undefined, undefined, undefined, o)
  };
  Kata.GraphicsScript.prototype.enableGraphicsTexture = function(j, h, o, q) {
    if(q === undefined) {
      q = j.space()
    }this._enableGraphics(j, undefined, q, h, o)
  };
  Kata.GraphicsScript.prototype.renderRemotePresence = function(j, h, o) {
    var q = new Kata.ScriptProtocol.FromScript.GFXCreateNode(j.space(), j.id(), h);
    Kata.LocationCopyUnifyTime(q, h.mLocation);
    this._sendHostedObjectMessage(q);
    if(!o) {
      j = Kata.ScriptProtocol.FromScript.generateGFXUpdateVisualMessages(j.space(), j.id(), h);
      o = j.length;
      for(q = 0;q < o;++q) {
        this._sendHostedObjectMessage(j[q])
      }
    }h.inGFXSceneGraph = true;
    this.updateGFX(h)
  };
  Kata.GraphicsScript.prototype.unrenderRemotePresence = function(j, h) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.GFXDestroyNode(j.space(), j.id(), h));
    delete h.inGFXSceneGraph
  };
  Kata.GraphicsScript.prototype._enableGraphics = function(j, h, o, q, u, f) {
    var g = j.space();
    this.renderRemotePresence(j, j);
    for(var m in this.mRemotePresences) {
      var p = this.mRemotePresences[m];
      if(p.space() == g) {
        this.mRenderableRemotePresences[this.mRenderableRemotePresences.length] = m;
        this.shouldRender(j, p) && !p.inGFXSceneGraph && this.renderRemotePresence(j, p)
      }
    }g = new Kata.ScriptProtocol.FromScript.RegisterGUIMessage(j.space(), j.id(), j.id());
    this._sendHostedObjectMessage(g);
    g = new Kata.ScriptProtocol.FromScript.GFXEnableEvent(j.space(), "drag");
    this._sendHostedObjectMessage(g);
    g = new Kata.ScriptProtocol.FromScript.GFXEnableEvent(j.space(), "pick");
    this._sendHostedObjectMessage(g);
    if(f) {
      g = new Kata.ScriptProtocol.FromScript.GFXAttachCamera(j.space(), j.id(), j.id(), h, o, q, u);
      g.msg = "Camera";
      this._sendHostedObjectMessage(g);
      g = new Kata.ScriptProtocol.FromScript.GFXAttachCamera(j.space(), j.id(), j.id(), h, o, q, u);
      this._sendHostedObjectMessage(g)
    }else {
      Kata.BlessedCameraID = Kata.ObjectID.random();
      g = new Kata.ScriptProtocol.FromScript.GFXCreateNode(j.space(), j.id(), j);
      g.id = Kata.BlessedCameraID;
      Kata.BlessedCameraSpace = g.space;
      Kata.BlessedCameraSpaceid = g.spaceid;
      this._sendHostedObjectMessage(g);
      g = new Kata.ScriptProtocol.FromScript.GFXAttachCamera(j.space(), j.id(), j.id(), h, o, q, u);
      g.id = Kata.BlessedCameraID;
      g.msg = "Camera";
      this._sendHostedObjectMessage(g);
      g = new Kata.ScriptProtocol.FromScript.GFXAttachCamera(j.space(), j.id(), j.id(), h, o, q, u);
      g.id = Kata.BlessedCameraID;
      this._sendHostedObjectMessage(g);
      setInterval(Kata.bind(this.cameraPeriodicUpdate, this), 20)
    }if(this.mNumGraphicsSystems++ == 0) {
      j = new Date(0);
      j.setSeconds(2);
      this.mGraphicsTimer = this.timer(j, Kata.bind(this.processRenderables, this), true)
    }
  };
  Kata.GraphicsScript.prototype.setCameraPosOrient = function(j, h, o) {
    if(o == null) {
      o = 0.9
    }this._camLag = o;
    if(j) {
      if(o == 0) {
        this._camPos = j
      }this._camPosTarget = j
    }if(h) {
      if(o == 0) {
        this._camOrient = h
      }this._camOrientTarget = h
    }
  };
  Kata.GraphicsScript.prototype.cameraPeriodicUpdate = function() {
    for(i in this._camPos) {
      this._camPos[i] = this._camPos[i] * this._camLag + this._camPosTarget[i] * (1 - this._camLag)
    }for(i in this._camOrient) {
      this._camOrient[i] = this._camOrient[i] * this._camLag + this._camOrientTarget[i] * (1 - this._camLag)
    }msg = {};
    msg.__type = Kata.ScriptProtocol.FromScript.Types.GraphicsMessage;
    msg.msg = "Move";
    msg.space = Kata.BlessedCameraSpace;
    msg.id = Kata.BlessedCameraID;
    msg.spaceid = Kata.BlessedCameraSpaceid;
    msg.pos = this._camPos;
    msg.orient = new Kata.Quaternion(this._camOrient);
    msg.orient = msg.orient.normal();
    this._sendHostedObjectMessage(msg)
  };
  Kata.GraphicsScript.prototype.processRenderables = function() {
    var j = this.mRenderableRemotePresences.length;
    if(j) {
      this.mRenderableRemotePresenceIndex %= j;
      var h = this.mRemotePresences[this.mRenderableRemotePresences[this.mRenderableRemotePresenceIndex]];
      if(h) {
        j = this.mPresences[h.space()];
        if(this.shouldRender(j, h)) {
          h.inGFXSceneGraph || this.renderRemotePresence(j, h)
        }else {
          h.inGFXSceneGraph && this.unrenderRemotePresence(j, h)
        }this.mRenderableRemotePresenceIndex++
      }else {
        this.mRemotePresences[this.mRenderableRemotePresenceIndex] = this.mRemotePresences[j];
        --this.mRemotePresences.length
      }
    }
  };
  Kata.GraphicsScript.prototype.disableGraphics = function(j) {
    var h = new Kata.ScriptProtocol.FromScript.GFXDetachCamera(j.space(), j.id(), j.id());
    this._sendHostedObjectMessage(h);
    var o = j.space(), q = this.mRenderableRemotePresences.length;
    h = unrenderRemotePresence(j, j);
    this._sendHostedObjectMessage(h);
    for(h = 0;h < q;) {
      var u = this.mRemotePresences[this.mRenderableRemotePresences[h]];
      if(u && u.space() == o) {
        u.inGFXSceneGraph && this.unrenderRemotePresence(j, u);
        this.mRenderableRemotePresences[h] = this.mRenderableRemotePresences[q];
        q = --this.mRenderableRemotePresences.length
      }else {
        ++h
      }
    }if(--this.mNumGraphicsSystems == 0) {
      this.mGraphicsTimer.disable();
      this.mGraphicsTimer = null
    }h = new Kata.ScriptProtocol.FromScript.UnregisterGUIMessage(j.space(), j.id(), j.id());
    this._sendHostedObjectMessage(h)
  };
  Kata.GraphicsScript.prototype._handleQueryEventDelegate = function(j, h) {
    if(j) {
      var o = this.mPresences[h.space];
      if(o.inGFXSceneGraph) {
        if(h.entered) {
          this.mRenderableRemotePresences.push(j);
          this.shouldRender(o, j) && this.renderRemotePresence(o, j)
        }else {
          j.inGFXSceneGraph && this.unrenderRemotePresence(o, j)
        }
      }
    }this.processRenderables();
    return j
  };
  Kata.GraphicsScript.prototype.updateGFX = function(j) {
    var h = this.mPresences[j.space()];
    if(h && h.inGFXSceneGraph) {
      this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.GFXMoveNode(h.space(), h.id(), j, {loc:j.predictedLocation()}));
      this.mUpdateHook && this.mUpdateHook(h, j)
    }
  };
  Kata.GraphicsScript.prototype._handlePresenceLocUpdate = function(j, h) {
    (j = e._handlePresenceLocUpdate.call(this, j, h)) && this.updateGFX(j);
    return j
  };
  Kata.GraphicsScript.prototype.shouldRender = function() {
    return true
  };
  Kata.GraphicsScript.prototype.animate = function(j, h, o) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.GFXAnimate(j.space(), j.id(), h, o))
  };
  Kata.GraphicsScript.prototype.setLabel = function(j, h, o, q) {
    this._sendHostedObjectMessage(new Kata.ScriptProtocol.FromScript.GFXLabel(j.space(), j.id(), h.object(), o, q))
  }
}, "katajs/oh/GraphicsScript.js");if(typeof Kata == "undefined") {
  Kata = {}
}Kata.require([], function() {
  Kata.Simulation = function(e) {
    this.mChannel = e;
    e.registerListener(Kata.bind(this.receivedMessage, this))
  };
  Kata.Simulation.prototype.receivedMessage = function() {
  }
}, "katajs/oh/Simulation.js");Kata.require(["katajs/core/SpaceID.js", "katajs/core/ObjectID.js", "katajs/core/PresenceID.js", "katajs/oh/odp/PortID.js"], function() {
  if(typeof Kata.ODP == "undefined") {
    Kata.ODP = {}
  }Kata.ODP.Endpoint = function() {
    if(arguments.length == 2) {
      this.mSpace = arguments[0].space();
      this.mObject = arguments[0].object();
      this.mPort = arguments[1]
    }else {
      if(arguments.length == 3) {
        this.mSpace = arguments[0];
        this.mObject = arguments[1];
        this.mPort = arguments[2]
      }else {
        throw"Invalid endpoint constructor argument list";
      }
    }
  };
  Kata.ODP.Endpoint.prototype.space = function() {
    return this.mSpace
  };
  Kata.ODP.Endpoint.prototype.object = function() {
    return this.mObject
  };
  Kata.ODP.Endpoint.prototype.port = function() {
    return this.mPort
  };
  Kata.ODP.Endpoint.prototype.presenceID = function() {
    return new Kata.PresenceID(this.mSpace, this.mObject)
  };
  Kata.ODP.Endpoint.any = function() {
    return new Kata.ODP.Endpoint(Kata.SpaceID.any(), Kata.ObjectID.any(), Kata.ODP.PortID.any())
  };
  Kata.ODP.Endpoint.prototype.toConciseString = function() {
    return this.mSpace.toString() + ":" + this.mObject.toString() + ":" + this.mPort.toString()
  };
  Kata.ODP.Endpoint.prototype.toString = function() {
    return"ODP.Endpoint(" + this.toConciseString() + ")"
  }
}, "katajs/oh/odp/Endpoint.js");Kata.require(["katajs/oh/odp/Endpoint.js"], function() {
  if(typeof Kata.ODP == "undefined") {
    Kata.ODP = {}
  }Kata.ODP.Port = function(e, j, h) {
    this.mEndpoint = e;
    this.mSendFunc = j;
    this.mReleaseFunc = h;
    this.mReceiveHandlers = []
  };
  Kata.ODP.Port.prototype.send = function(e, j) {
    this.mSendFunc(this.mEndpoint, e, j)
  };
  Kata.ODP.Port.prototype.receive = function(e) {
    this.receiveFrom(Kata.ODP.Endpoint.any(), e)
  };
  Kata.ODP.Port.prototype.receiveFrom = function(e, j) {
    this.mReceiveHandlers[e] = j
  };
  Kata.ODP.Port.prototype.deliver = function(e, j) {
    if(this._tryDeliver(e, e, j)) {
      return true
    }if(this._tryDeliver(new Kata.ODP.Endpoint(e.space(), Kata.ObjectID.any(), e.port()), e, j)) {
      return true
    }if(this._tryDeliver(new Kata.ODP.Endpoint(Kata.SpaceID.any(), Kata.ObjectID.any(), e.port()), e, j)) {
      return true
    }if(this._tryDeliver(new Kata.ODP.Endpoint(e.space(), e.object(), Kata.ODP.PortID.any()), e, j)) {
      return true
    }if(this._tryDeliver(new Kata.ODP.Endpoint(e.space(), Kata.ObjectID.any(), Kata.ODP.PortID.any()), e, j)) {
      return true
    }if(this._tryDeliver(new Kata.ODP.Endpoint(Kata.SpaceID.any(), Kata.ObjectID.any(), Kata.ODP.PortID.any()), e, j)) {
      return true
    }return false
  };
  Kata.ODP.Port.prototype._tryDeliver = function(e, j, h) {
    if(e in this.mReceiveHandlers) {
      this.mReceiveHandlers[e](j, this.mEndpoint, h);
      return true
    }return false
  };
  Kata.ODP.Port.prototype.toString = function() {
    return"ODP.Port(" + this.mEndpoint.toConciseString() + ")"
  };
  Kata.ODP.Port.prototype.close = function() {
    var e = this.mReleaseFunc, j = this.mEndpoint;
    delete this.mEndpoint;
    delete this.mSendFunc;
    delete this.mReleaseFunc;
    e(j)
  }
}, "katajs/oh/odp/Port.js");Kata.require(["katajs/oh/odp/Port.js"], function() {
  if(typeof Kata.ODP == "undefined") {
    Kata.ODP = {}
  }Kata.ODP.Service = function(e) {
    this.mODPServiceSendFunc = e;
    this.mODPServiceBoundPorts = {}
  };
  Kata.ODP.Service.prototype.bindODPPort = function(e, j, h) {
    e = new Kata.ODP.Endpoint(e, j, h);
    j = this.mODPServiceBoundPorts[e];
    if(typeof j != "undefined") {
      throw"Tried to bind previously bound port.";
    }j = new Kata.ODP.Port(e, this.mODPServiceSendFunc, Kata.bind(this._handleODPServiceReleasePort, this));
    return this.mODPServiceBoundPorts[e] = j
  };
  Kata.ODP.Service.prototype._handleODPServiceReleasePort = function(e) {
    typeof this.mODPServiceBoundPorts[e] == "undefined" && Kata.error("Got ODP port release for unallocated port.");
    delete this.mODPServiceBoundPorts[e]
  };
  Kata.ODP.Service.prototype._deliverODPMessage = function(e, j, h) {
    j = this.mODPServiceBoundPorts[j];
    typeof j != "undefined" && j.deliver(e, h)
  }
}, "katajs/oh/odp/Service.js");Kata.require([], function() {
  if(typeof Kata.ODP == "undefined") {
    Kata.ODP = {}
  }Kata.ODP.PortID = {};
  Kata.ODP.PortID.nil = function() {
    return 0
  };
  Kata.ODP.PortID.any = function() {
    return 16777215
  }
}, "katajs/oh/odp/PortID.js");Kata.require(["katajs/core/Time.js", "katajs/oh/odp/Endpoint.js"], function() {
  Kata.RemotePresence = function(e, j, h, o, q) {
    this.mParent = e;
    this.mSpace = j;
    this.mID = h;
    this.mLocation = o;
    if(q) {
      this.rMesh = q.mesh;
      this.rAnim = q.anim;
      this.rUpAxis = q.up_axis;
      this.rCenter = q.center
    }this.mTracking = false
  };
  Kata.RemotePresence.prototype.id = function() {
    return this.mID
  };
  Kata.RemotePresence.prototype.space = function() {
    return this.mSpace
  };
  Kata.RemotePresence.prototype.presenceID = function() {
    return new Kata.PresenceID(this.mSpace, this.mID)
  };
  Kata.RemotePresence.prototype.endpoint = function(e) {
    return new Kata.ODP.Endpoint(this.mSpace, this.mID, e)
  };
  Kata.RemotePresence.prototype.owner = function() {
    return this.mParent
  };
  Kata.RemotePresence.prototype.track = function() {
    if(!this.mTracking) {
      this.mParent.subscribe(this.mID);
      this.mTracking = true
    }
  };
  Kata.RemotePresence.prototype.untrack = function() {
    if(this.mTracking) {
      this.mParent.unsubscribe(this.mID);
      this.mTracking = false
    }
  };
  Kata.RemotePresence.prototype.position = function(e) {
    e === undefined && console.log("inaccurate read of position");
    return Kata.LocationExtrapolate(this.mLocation, e).pos.concat()
  };
  Kata.RemotePresence.prototype.velocity = function() {
    return this.mLocation.vel.concat()
  };
  Kata.RemotePresence.prototype.orientation = function(e) {
    e === undefined && console.log("inaccurate read of orientation");
    return Kata.LocationExtrapolate(this.mLocation, e).orient.concat()
  };
  Kata.RemotePresence.prototype.angularSpeed = function() {
    return this.mLocation.rotvel
  };
  Kata.RemotePresence.prototype.rotationalAxis = function() {
    return this.mLocation.rotaxis.concat()
  };
  Kata.RemotePresence.prototype.rotationalVelocity = function() {
    return Kata.Quaternion.fromLocationAngularVelocity(this.mLocation)
  };
  Kata.RemotePresence.prototype.scale = function() {
    return this.mLocation.scale.concat()
  };
  Kata.RemotePresence.prototype.location = function() {
    var e = {};
    for(var j in this.mLocation) {
      e[j] = this.mLocation[j]
    }return e
  };
  Kata.RemotePresence.prototype.predictedPosition = function(e) {
    return this.position(e)
  };
  Kata.RemotePresence.prototype.predictedVelocity = function() {
    return this.velocity()
  };
  Kata.RemotePresence.prototype.predictedOrientation = function(e) {
    return this.orientation(e)
  };
  Kata.RemotePresence.prototype.predictedAngularSpeed = function() {
    return this.angularSpeed()
  };
  Kata.RemotePresence.prototype.predictedRotationalAxis = function() {
    return this.rotationalAxis()
  };
  Kata.RemotePresence.prototype.predictedRotationalVelocity = function() {
    return this.rotationalVelocity()
  };
  Kata.RemotePresence.prototype.predictedScale = function() {
    return this.scale()
  };
  Kata.RemotePresence.prototype.predictedLocation = function() {
    return this.location()
  };
  Kata.RemotePresence.prototype.bounds = function() {
    return this.mLocation.scale.concat()
  };
  Kata.RemotePresence.prototype.visual = function() {
    return this.mVisual
  };
  Kata.RemotePresence.prototype._updateLoc = function(e, j) {
    if(e) {
      this.mLocation = Kata.LocationUpdate(e, this.mLocation, undefined, Kata.now(this.mSpace))
    }if(j) {
      this.mVisual = j
    }
  }
}, "katajs/oh/RemotePresence.js");if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}if(typeof Sirikata.Protocol.Loc == "undefined") {
  Sirikata.Protocol.Loc = {}
}Sirikata.Protocol.Loc._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.Loc.LocationUpdate = PROTO.Message("Sirikata.Protocol.Loc.LocationUpdate", {object:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uuid
}, id:1}, location:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionVector
}, id:2}, orientation:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionQuaternion
}, id:3}, bounds:{options:{packed:true}, multiplicity:PROTO.optional, type:function() {
  return PBJ.boundingsphere3f
}, id:4}, mesh:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.string
}, id:5}});
Sirikata.Protocol.Loc.BulkLocationUpdate = PROTO.Message("Sirikata.Protocol.Loc.BulkLocationUpdate", {update:{options:{}, multiplicity:PROTO.repeated, type:function() {
  return Sirikata.Protocol.Loc.LocationUpdate
}, id:1}});
Sirikata.Protocol.Loc.LocationUpdateRequest = PROTO.Message("Sirikata.Protocol.Loc.LocationUpdateRequest", {location:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionVector
}, id:1}, orientation:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionQuaternion
}, id:2}, bounds:{options:{packed:true}, multiplicity:PROTO.optional, type:function() {
  return PBJ.boundingsphere3f
}, id:3}, mesh:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.string
}, id:4}});
Sirikata.Protocol.Loc.Container = PROTO.Message("Sirikata.Protocol.Loc.Container", {update_request:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.Loc.LocationUpdateRequest
}, id:1}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}Sirikata.Protocol._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.TimedMotionVector = PROTO.Message("Sirikata.Protocol.TimedMotionVector", {t:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.time
}, id:1}, position:{options:{packed:true}, multiplicity:PROTO.required, type:function() {
  return PBJ.vector3f
}, id:2}, velocity:{options:{packed:true}, multiplicity:PROTO.required, type:function() {
  return PBJ.vector3f
}, id:3}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}Sirikata.Protocol._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.TimeSync = PROTO.Message("Sirikata.Protocol.TimeSync", {seqno:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PBJ.uint8
}, id:1}, t:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PBJ.time
}, id:2}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}if(typeof Sirikata.Protocol.Prox == "undefined") {
  Sirikata.Protocol.Prox = {}
}Sirikata.Protocol.Prox._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.Prox.ObjectAddition = PROTO.Message("Sirikata.Protocol.Prox.ObjectAddition", {object:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uuid
}, id:1}, location:{options:{}, multiplicity:PROTO.required, type:function() {
  return Sirikata.Protocol.TimedMotionVector
}, id:2}, orientation:{options:{}, multiplicity:PROTO.required, type:function() {
  return Sirikata.Protocol.TimedMotionQuaternion
}, id:3}, bounds:{options:{packed:true}, multiplicity:PROTO.required, type:function() {
  return PBJ.boundingsphere3f
}, id:4}, mesh:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.string
}, id:5}});
Sirikata.Protocol.Prox.ObjectRemoval = PROTO.Message("Sirikata.Protocol.Prox.ObjectRemoval", {object:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uuid
}, id:1}});
Sirikata.Protocol.Prox.ProximityUpdate = PROTO.Message("Sirikata.Protocol.Prox.ProximityUpdate", {addition:{options:{}, multiplicity:PROTO.repeated, type:function() {
  return Sirikata.Protocol.Prox.ObjectAddition
}, id:1}, removal:{options:{}, multiplicity:PROTO.repeated, type:function() {
  return Sirikata.Protocol.Prox.ObjectRemoval
}, id:2}});
Sirikata.Protocol.Prox.ProximityResults = PROTO.Message("Sirikata.Protocol.Prox.ProximityResults", {t:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.time
}, id:1}, update:{options:{}, multiplicity:PROTO.repeated, type:function() {
  return Sirikata.Protocol.Prox.ProximityUpdate
}, id:2}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}Sirikata.Protocol._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.Frame = PROTO.Message("Sirikata.Protocol.Frame", {payload:{options:{}, multiplicity:PROTO.required, type:function() {
  return PROTO.bytes
}, id:1}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}if(typeof Sirikata.Protocol.Session == "undefined") {
  Sirikata.Protocol.Session = {}
}Sirikata.Protocol.Session._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.Session.Connect = PROTO.Message("Sirikata.Protocol.Session.Connect", {ConnectionType:PROTO.Enum("Sirikata.Protocol.Session.Connect.ConnectionType", {Fresh:1, Migration:2}), type:{options:{}, multiplicity:PROTO.required, type:function() {
  return Sirikata.Protocol.Session.Connect.ConnectionType
}, id:1}, object:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uuid
}, id:2}, loc:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionVector
}, id:3}, orientation:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionQuaternion
}, id:4}, bounds:{options:{packed:true}, multiplicity:PROTO.optional, type:function() {
  return PBJ.boundingsphere3f
}, id:5}, query_angle:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.Float
}, id:6}, mesh:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.string
}, id:7}});
Sirikata.Protocol.Session.ConnectResponse = PROTO.Message("Sirikata.Protocol.Session.ConnectResponse", {Response:PROTO.Enum("Sirikata.Protocol.Session.ConnectResponse.Response", {Success:1, Redirect:2, Error:3}), response:{options:{}, multiplicity:PROTO.required, type:function() {
  return Sirikata.Protocol.Session.ConnectResponse.Response
}, id:1}, redirect:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.uint64
}, id:2}, loc:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionVector
}, id:3}, orientation:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.TimedMotionQuaternion
}, id:4}, bounds:{options:{packed:true}, multiplicity:PROTO.optional, type:function() {
  return PBJ.boundingsphere3f
}, id:5}});
Sirikata.Protocol.Session.ConnectAck = PROTO.Message("Sirikata.Protocol.Session.ConnectAck", {});
Sirikata.Protocol.Session.InitiateMigration = PROTO.Message("Sirikata.Protocol.Session.InitiateMigration", {new_server:{options:{}, multiplicity:PROTO.required, type:function() {
  return PROTO.uint64
}, id:1}});
Sirikata.Protocol.Session.Disconnect = PROTO.Message("Sirikata.Protocol.Session.Disconnect", {object:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uuid
}, id:1}, reason:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.string
}, id:2}});
Sirikata.Protocol.Session.Container = PROTO.Message("Sirikata.Protocol.Session.Container", {connect:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.Session.Connect
}, id:1}, connect_response:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.Session.ConnectResponse
}, id:2}, connect_ack:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.Session.ConnectAck
}, id:3}, init_migration:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.Session.InitiateMigration
}, id:4}, disconnect:{options:{}, multiplicity:PROTO.optional, type:function() {
  return Sirikata.Protocol.Session.Disconnect
}, id:5}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}Sirikata.Protocol._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.Empty = PROTO.Message("Sirikata.Protocol.Empty", {});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}if(typeof Sirikata.Protocol.Object == "undefined") {
  Sirikata.Protocol.Object = {}
}Sirikata.Protocol.Object._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.Object.ObjectMessage = PROTO.Message("Sirikata.Protocol.Object.ObjectMessage", {source_object:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uuid
}, id:1}, source_port:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint16
}, id:2}, dest_object:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uuid
}, id:3}, dest_port:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint16
}, id:4}, unique:{options:{}, multiplicity:PROTO.required, type:function() {
  return PROTO.uint64
}, id:5}, payload:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.bytes
}, id:6}});
Sirikata.Protocol.Object.Noise = PROTO.Message("Sirikata.Protocol.Object.Noise", {payload:{options:{}, multiplicity:PROTO.required, type:function() {
  return PROTO.bytes
}, id:1}});
Sirikata.Protocol.Object.Ping = PROTO.Message("Sirikata.Protocol.Object.Ping", {ping:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.time
}, id:7}, distance:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.Double
}, id:8}, id:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.uint64
}, id:9}, payload:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.bytes
}, id:10}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}Sirikata.Protocol._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.TimedMotionQuaternion = PROTO.Message("Sirikata.Protocol.TimedMotionQuaternion", {t:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.time
}, id:1}, position:{options:{packed:true}, multiplicity:PROTO.required, type:function() {
  return PBJ.quaternion
}, id:2}, velocity:{options:{packed:true}, multiplicity:PROTO.required, type:function() {
  return PBJ.quaternion
}, id:3}});if(typeof Sirikata == "undefined") {
  Sirikata = {}
}if(typeof Sirikata.Protocol == "undefined") {
  Sirikata.Protocol = {}
}if(typeof Sirikata.Protocol.SST == "undefined") {
  Sirikata.Protocol.SST = {}
}Sirikata.Protocol.SST._PBJ_Internal = "pbj-0.0.3";
Sirikata.Protocol.SST.SSTChannelHeader = PROTO.Message("Sirikata.Protocol.SST.SSTChannelHeader", {channel_id:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint8
}, id:1}, transmit_sequence_number:{options:{}, multiplicity:PROTO.required, type:function() {
  return PROTO.uint64
}, id:2}, ack_count:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint8
}, id:3}, ack_sequence_number:{options:{}, multiplicity:PROTO.required, type:function() {
  return PROTO.uint64
}, id:4}, payload:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.bytes
}, id:5}});
Sirikata.Protocol.SST.SSTStreamHeader = PROTO.Message("Sirikata.Protocol.SST.SSTStreamHeader", {StreamPacketType:PROTO.Enum("Sirikata.Protocol.SST.SSTStreamHeader.StreamPacketType", {INIT:1, REPLY:2, DATA:3, ACK:4, DATAGRAM:5}), Flags:PROTO.Flags(123456, "Sirikata.Protocol.SST.SSTStreamHeader.Flags", {CONTINUES:1}), lsid:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint16
}, id:1}, type:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint8
}, id:2}, flags:{options:{}, multiplicity:PROTO.required, type:function() {
  return Sirikata.Protocol.SST.SSTStreamHeader.Flags
}, id:3}, window:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint8
}, id:4}, src_port:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint16
}, id:5}, dest_port:{options:{}, multiplicity:PROTO.required, type:function() {
  return PBJ.uint16
}, id:6}, psid:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PBJ.uint16
}, id:7}, rsid:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PBJ.uint16
}, id:8}, bsn:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.uint32
}, id:9}, payload:{options:{}, multiplicity:PROTO.optional, type:function() {
  return PROTO.bytes
}, id:10}});Kata.require(["katajs/oh/SpaceConnection.js", "katajs/oh/SessionManager.js", "katajs/network/TCPSST.js", "katajs/core/Quaternion.js", ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/TimedMotionVector.pbj.js"], ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/TimedMotionQuaternion.pbj.js"], ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/Session.pbj.js"], ["externals/protojs/protobuf.js", 
"externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/ObjectMessage.pbj.js"], ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/Prox.pbj.js"], ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/Loc.pbj.js"], ["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/Frame.pbj.js"], "katajs/oh/sst/SSTImpl.js", "katajs/oh/plugins/sirikata/Frame.js", "katajs/oh/plugins/sirikata/Sync.js"], 
function() {
  var e = Kata.SpaceConnection.prototype;
  Kata.SirikataSpaceConnection = function(j, h) {
    e.constructor.call(this, j);
    this.mSpaceURL = h;
    this.mObjectUUIDs = {};
    this.mLocalIDs = {};
    this.mOutstandingConnectRequests = {};
    this.mConnectedObjects = {};
    j = 7777;
    if(Kata.URL.port(h)) {
      j = Kata.URL.port(h)
    }this.mSocket = new Kata.TCPSST(Kata.URL.host(h), j);
    this.mPrimarySubstream = this.mSocket.clone();
    this.mPrimarySubstream.registerListener(Kata.bind(this._receivedData, this));
    this.mODPHandlers = {};
    this.mSync = new Kata.Sirikata.SyncClient(this, new Kata.ODP.Endpoint(this.mSpaceURL, Kata.ObjectID.random(), this.Ports.TimeSync), new Kata.ODP.Endpoint(this.mSpaceURL, Kata.ObjectID.nil(), this.Ports.TimeSync))
  };
  Kata.extend(Kata.SirikataSpaceConnection, Kata.SpaceConnection.prototype);
  Kata.SirikataSpaceConnection.prototype.Ports = {Session:1, Proximity:2, Location:3, TimeSync:4, Space:253};
  Kata.SirikataSpaceConnection.prototype.ObjectMessageRouter = function(j) {
    this.mParentSpaceConn = j
  };
  Kata.SirikataSpaceConnection.prototype.ObjectMessageRouter.prototype.route = function(j) {
    this.mParentSpaceConn._sendPreparedODPMessage(j)
  };
  Kata.SirikataSpaceConnection.prototype._getObjectID = function(j) {
    if(!this.mObjectUUIDs[j]) {
      this.mObjectUUIDs[j] = Math.uuid();
      this.mLocalIDs[this.mObjectUUIDs[j]] = j
    }return this.mObjectUUIDs[j]
  };
  Kata.SirikataSpaceConnection.prototype._getLocalID = function(j) {
    return this.mLocalIDs[j]
  };
  Kata.SirikataSpaceConnection.prototype._toLocalTime = function(j) {
    return j instanceof Date ? new Date(j.getTime() - this.mSync.offset()) : new Date(j - this.mSync.offset())
  };
  Kata.SirikataSpaceConnection.prototype._toSpaceTime = function(j) {
    return j instanceof Date ? new Date(j.getTime() + this.mSync.offset()) : new Date(j + this.mSync.offset())
  };
  Kata.SirikataSpaceConnection.prototype._serializeMessage = function(j) {
    var h = new PROTO.ByteArrayStream;
    j.SerializeToStream(h);
    return h
  };
  Kata.SirikataSpaceConnection.prototype._generateLocUpdateParts = function(j, h) {
    h = h ? {loc:undefined, orient:undefined, bounds:[0, 0, 0, 1], visual:""} : {loc:undefined, orient:undefined, bounds:undefined, visual:undefined};
    if(j.pos || j.vel) {
      var o = new Sirikata.Protocol.TimedMotionVector;
      o.t = this._toSpaceTime(j.time);
      if(j.pos) {
        o.position = j.pos
      }if(j.vel) {
        o.velocity = j.vel
      }h.loc = o
    }if(j.orient || j.rotvel != undefined && j.rotaxis != undefined) {
      o = new Sirikata.Protocol.TimedMotionQuaternion;
      o.t = this._toSpaceTime(j.time);
      if(j.orient) {
        o.position = j.orient
      }if(j.rotvel != undefined && j.rotaxis != undefined) {
        o.velocity = Kata.Quaternion.fromAxisAngle(j.rotaxis, j.rotvel).array()
      }h.orient = o
    }if(j.scale) {
      if(j.scale.length === undefined) {
        h.bounds = [0, 0, 0, j.scale]
      }else {
        if(j.scale.length == 3) {
          h.bounds = [0, 0, 0, j.scale[0]]
        }else {
          if(j.scale.length == 4) {
            h.bounds = j.scale
          }
        }
      }
    }if(j.visual) {
      h.visual = j.visual.mesh
    }return h
  };
  Kata.SirikataSpaceConnection.prototype.connectObject = function(j, h, o, q) {
    j = this._getObjectID(j);
    h = Kata.LocationIdentity(0);
    Kata.LocationCopyUnifyTime(o, h);
    h.visual = o.visual;
    this.mOutstandingConnectRequests[j] = {loc_bounds:h, visual:q, deferred_odp:[]};
    o = new Sirikata.Protocol.Session.Connect;
    o.type = Sirikata.Protocol.Session.Connect.ConnectionType.Fresh;
    o.object = j;
    q = this._generateLocUpdateParts(h, true);
    if(q.loc) {
      o.loc = q.loc
    }if(q.orient) {
      o.orientation = q.orient
    }if(q.bounds) {
      o.bounds = q.bounds
    }if(q.visual) {
      o.mesh = q.visual
    }o.query_angle = 1.0E-26;
    q = new Sirikata.Protocol.Session.Container;
    q.connect = o;
    this._sendODPMessage(j, this.Ports.Session, Kata.ObjectID.nil(), this.Ports.Session, this._serializeMessage(q))
  };
  Kata.SirikataSpaceConnection.prototype.disconnectObject = function(j) {
    j = this._getObjectID(j);
    var h = new Sirikata.Protocol.Session.Disconnect;
    h.object = j;
    h.reason = "Quit";
    var o = new Sirikata.Protocol.Session.Container;
    o.disconnect = h;
    this._sendODPMessage(j, this.Ports.Session, Kata.ObjectID.nil(), this.Ports.Session, this._serializeMessage(o))
  };
  Kata.SirikataSpaceConnection.prototype.sendODPMessage = function(j, h, o, q, u) {
    this._sendODPMessage(j, h, o, q, u)
  };
  Kata.SirikataSpaceConnection.prototype._sendODPMessage = function(j, h, o, q, u) {
    var f = new Sirikata.Protocol.Object.ObjectMessage;
    f.source_object = j;
    f.source_port = h;
    f.dest_object = o;
    f.dest_port = q;
    f.unique = PROTO.I64.fromNumber(0);
    if(typeof u !== "undefined") {
      if(typeof u.length === "undefined" || u.length > 0) {
        f.payload = typeof u == "string" ? PROTO.encodeUTF8(u) : u
      }
    }this._sendPreparedODPMessage(f)
  };
  Kata.SirikataSpaceConnection.prototype._sendPreparedODPMessage = function(j) {
    var h = new PROTO.Base64Stream;
    j.SerializeToStream(h);
    this.mPrimarySubstream.sendMessage(h.getString())
  };
  Kata.SirikataSpaceConnection.prototype._handleDisconnected = function(j) {
    if(j === this.mPrimarySubstream) {
      for(var h in this.mConnectedObjects) {
        this.mParent.disconnected(h, this.mSpaceURL)
      }this.mParent.spaceConnectionDisconnected(this)
    }
  };
  Kata.SirikataSpaceConnection.prototype._receivedData = function(j, h) {
    if(h === undefined || h === null) {
      this._handleDisconnected(j)
    }else {
      j = new Sirikata.Protocol.Object.ObjectMessage;
      j.ParseFromStream(new PROTO.Base64Stream(h));
      if(j.source_object == Kata.ObjectID.nil() && j.dest_port == this.Ports.Session) {
        this._handleSessionMessage(j)
      }else {
        if(h = this.mODPHandlers[j.dest_object + j.dest_port]) {
          h(this.mSpaceURL, j.source_object, j.source_port, j.dest_object, j.dest_port, j.payload)
        }else {
          if(h = this.mConnectedObjects[j.dest_object]) {
            h.odpDispatcher.dispatchMessage(j) || this._tryDeliverODP(j)
          }
        }
      }
    }
  };
  Kata.SirikataSpaceConnection.prototype._receiveODPMessage = function(j, h, o) {
    this.mODPHandlers[j + h] = o
  };
  Kata.SirikataSpaceConnection.prototype._tryDeliverODP = function(j) {
    var h = this.mOutstandingConnectRequests[j.dest_object];
    h ? h.deferred_odp.push(j) : this._deliverODP(j)
  };
  Kata.SirikataSpaceConnection.prototype._deliverODP = function(j) {
    this.mParent.receiveODPMessage(this.mSpaceURL, j.source_object, j.source_port, j.dest_object, j.dest_port, j.payload)
  };
  Kata.SirikataSpaceConnection.prototype._handleSessionMessage = function(j) {
    var h = new Sirikata.Protocol.Session.Container;
    h.ParseFromStream(new PROTO.ByteArrayStream(j.payload));
    j = j.dest_object;
    if(h.HasField("connect_response")) {
      var o = h.connect_response;
      if(o.response == Sirikata.Protocol.Session.ConnectResponse.Response.Success) {
        var q = this._getLocalID(j);
        Kata.warn("Successfully connected " + q);
        o = new Sirikata.Protocol.Session.ConnectAck;
        var u = new Sirikata.Protocol.Session.Container;
        u.connect_ack = o;
        this._sendODPMessage(j, this.Ports.Session, Kata.ObjectID.nil(), this.Ports.Session, this._serializeMessage(u));
        this.mConnectedObjects[j] = {};
        o = new this.ObjectMessageRouter(this);
        u = new Kata.SST.ObjectMessageDispatcher;
        this.mConnectedObjects[j].odpDispatcher = u;
        this.mConnectedObjects[j].odpBaseDatagramLayer = Kata.SST.createBaseDatagramLayer(new Kata.SST.EndPoint(j, 0), o, u);
        this.mConnectedObjects[j].proxdata = [];
        Kata.SST.connectStream(new Kata.SST.EndPoint(j, this.Ports.Space), new Kata.SST.EndPoint(Kata.SpaceID.nil(), this.Ports.Space), Kata.bind(this._spaceSSTConnectCallback, this, j));
        this.mParent.aliasIDs(q, {space:this.mSpaceURL, object:j})
      }else {
        if(o.response == Sirikata.Protocol.Session.ConnectResponse.Response.Redirect) {
          Kata.notImplemented("Server redirects for Sirikata are not implemented.")
        }else {
          if(o.response == Sirikata.Protocol.Session.ConnectResponse.Response.Error) {
            Kata.warn("Connection Error.");
            this.mParent.connectionResponse(q, false)
          }else {
            Kata.warn("Got unknown connection response.")
          }
        }
      }
    }h.HasField("init_migration") && Kata.notImplemented("Migrations not implemented.")
  };
  Kata.SirikataSpaceConnection.prototype._spaceSSTConnectCallback = function(j, h, o) {
    if(h == Kata.SST.FAILURE) {
      Kata.warn("Failed to get SST connection to space for " + j + ".")
    }else {
      Kata.warn("Successful SST space connection for " + j + ". Setting up loc and prox listeners.");
      this.mConnectedObjects[j].spaceStream = o;
      o.listenSubstream(this.Ports.Location, Kata.bind(this._handleLocationSubstream, this, j));
      o.listenSubstream(this.Ports.Proximity, Kata.bind(this._handleProximitySubstream, this, j));
      h = this.mOutstandingConnectRequests[j];
      delete this.mOutstandingConnectRequests[j];
      this.mParent.connectionResponse(this._getLocalID(j), true, {space:this.mSpaceURL, object:j}, h.loc_bounds, h.visual);
      for(j = 0;j < h.deferred_odp.length;j++) {
        this._deliverODP(h.deferred_odp[j])
      }
    }
  };
  Kata.SirikataSpaceConnection.prototype.locUpdateRequest = function(j, h) {
    var o = new Sirikata.Protocol.Loc.LocationUpdateRequest;
    h = this._generateLocUpdateParts(h, false);
    if(h.loc) {
      o.location = h.loc
    }if(h.orient) {
      o.orientation = h.orient
    }if(h.bounds) {
      o.bounds = h.bounds
    }if(h.visual) {
      o.mesh = h.visual
    }h = new Sirikata.Protocol.Loc.Container;
    h.update_request = o;
    (j = this.mConnectedObjects[j].spaceStream) ? j.datagram(this._serializeMessage(h).getArray(), this.Ports.Location, this.Ports.Location) : Kata.warn("Tried to send loc update before stream to server was ready.")
  };
  Kata.SirikataSpaceConnection.prototype._handleLocationSubstream = function(j, h, o) {
    h != 0 && Kata.warn("Location substream (error " + h + ")");
    o.registerReadCallback(Kata.bind(this._handleLocationSubstreamRead, this, j, o))
  };
  Kata.SirikataSpaceConnection.prototype._handleProximitySubstream = function(j, h, o) {
    h != 0 && Kata.warn("Proximity substream (error " + h + ")");
    o.registerReadCallback(Kata.bind(this._handleProximitySubstreamRead, this, j, o))
  };
  Kata.SirikataSpaceConnection.prototype._handleLocationSubstreamRead = function(j, h, o) {
    h = new Sirikata.Protocol.Frame;
    h.ParseFromStream(new PROTO.ByteArrayStream(o));
    o = new Sirikata.Protocol.Loc.BulkLocationUpdate;
    o.ParseFromStream(new PROTO.ByteArrayStream(h.payload));
    for(h = 0;h < o.update.length;h++) {
      var q = o.update[h], u = q.object, f;
      if(q.mesh) {
        f = q.mesh
      }if(q.location) {
        var g = {};
        g.time = this._toLocalTime(q.location.t).getTime();
        g.pos = q.location.position;
        g.vel = q.location.velocity;
        this.mParent.presenceLocUpdate(this.mSpaceURL, u, j, g, f)
      }if(q.orientation) {
        g = {};
        g.time = this._toLocalTime(q.orientation.t).getTime();
        g.orient = q.orientation.position;
        q = (new Kata.Quaternion(q.orientation.velocity)).toAngleAxis();
        g.rotaxis = q.axis;
        g.rotvel = q.angle;
        this.mParent.presenceLocUpdate(this.mSpaceURL, u, j, g, f)
      }
    }
  };
  Kata.SirikataSpaceConnection.prototype._handleProximitySubstreamRead = function(j, h, o) {
    h = this.mConnectedObjects[j];
    for(h.proxdata = h.proxdata.concat(o);;) {
      var q = Kata.Frame.parse(h.proxdata);
      if(q === null) {
        break
      }o = new Sirikata.Protocol.Prox.ProximityResults;
      o.ParseFromStream(new PROTO.ByteArrayStream(q));
      for(q = 0;q < o.update.length;q++) {
        this._handleProximityUpdate(j, o.t, o.update[q])
      }
    }
  };
  Kata.SirikataSpaceConnection.prototype._handleProximityUpdate = function(j, h, o) {
    for(var q = 0;q < o.addition.length;q++) {
      h = o.addition[q].object;
      if(h != j) {
        var u = {};
        u.loc = Kata.LocationIdentity(0);
        u.loc.pos = o.addition[q].location.position;
        u.loc.vel = o.addition[q].location.velocity;
        u.loc.posTime = this._toLocalTime(o.addition[q].location.t).getTime();
        u.loc.orient = o.addition[q].orientation.position;
        var f = (new Kata.Quaternion(o.addition[q].orientation.velocity)).toAngleAxis();
        u.loc.rotaxis = f.axis;
        u.loc.rotvel = f.angle;
        u.loc.orientTime = this._toLocalTime(o.addition[q].orientation.t).getTime();
        u.bounds = o.addition[q].bounds;
        f = o.addition[q].bounds[3];
        u.loc.scale = [f, f, f];
        u.loc.scaleTime = this._toLocalTime(o.addition[q].location.t).getTime();
        if(o.addition[q].HasField("mesh")) {
          u.visual = {anim:"", mesh:o.addition[q].mesh, up_axis:[1, 0, 0]}
        }this.mParent.proxEvent(this.mSpaceURL, j, h, true, u)
      }
    }for(q = 0;q < o.removal.length;q++) {
      h = o.removal[q].object;
      h != j && this.mParent.proxEvent(this.mSpaceURL, j, h, false)
    }
  };
  Kata.SessionManager.registerProtocolHandler("sirikata", Kata.SirikataSpaceConnection)
}, "katajs/oh/plugins/sirikata/SirikataSpaceConnection.js");(function() {
  Kata.Frame = {};
  Kata.Frame.parse = function(e) {
    if(e.length < 4) {
      return null
    }var j = e[0] * 16777216 + e[1] * 65536 + e[2] * 256 + e[3];
    if(e.length < 4 + j) {
      return null
    }e.splice(0, 4);
    return e.splice(0, j)
  }
})();Kata.require([["externals/protojs/protobuf.js", "externals/protojs/pbj.js", "katajs/oh/plugins/sirikata/impl/TimeSync.pbj.js"]], function() {
  if(typeof Kata.Sirikata == "undefined") {
    Kata.Sirikata = {}
  }Kata.Sirikata.SyncClient = function(e, j, h, o) {
    this.mODP = e;
    this.mLocalEndpoint = j;
    this.mSyncEndpoint = h;
    this.mCB = o;
    this.mODP._receiveODPMessage(j.object(), j.port(), Kata.bind(this.handleMessage, this));
    this.mSeqNo = 0;
    this.mRequestTimes = new Array(256);
    this.poll();
    this.mOffset = null
  };
  Kata.Sirikata.SyncClient.prototype.MaxRTT = 5E3;
  Kata.Sirikata.SyncClient.prototype.valid = function() {
    return this.mOffset == null
  };
  Kata.Sirikata.SyncClient.prototype.offset = function() {
    return this.mOffset
  };
  Kata.Sirikata.SyncClient.prototype.poll = function() {
    var e = new Sirikata.Protocol.TimeSync, j = this.mSeqNo;
    this.mSeqNo = (this.mSeqNo + 1) % 256;
    e.seqno = j;
    this.mRequestTimes[j] = (new Date).getTime();
    j = new PROTO.ByteArrayStream;
    e.SerializeToStream(j);
    this.mODP.sendODPMessage(this.mLocalEndpoint.object(), this.mLocalEndpoint.port(), this.mSyncEndpoint.object(), this.mSyncEndpoint.port(), j);
    setTimeout(Kata.bind(this.poll, this), 5E3)
  };
  Kata.Sirikata.SyncClient.prototype.handleMessage = function(e, j, h, o, q, u) {
    e = new Sirikata.Protocol.TimeSync;
    e.ParseFromStream(new PROTO.ByteArrayStream(u));
    u = this.mRequestTimes[e.seqno];
    e = e.t;
    j = (new Date).getTime();
    h = j - u;
    if(!(j < u || h > this.MaxRTT)) {
      this.mOffset = e - (u + h / 2);
      this.mCB && this.mCB()
    }
  }
}, "katajs/oh/plugins/sirikata/Sync.js");Kata.require(["katajs/oh/SpaceConnection.js", "katajs/oh/SessionManager.js", "katajs/space/loop/Space.js"], function() {
  var e = Kata.SpaceConnection.prototype;
  Kata.LoopbackSpaceConnection = function(j, h) {
    e.constructor.call(this, j);
    this.mSpace = Kata.LoopbackSpace.spaces[Kata.URL.host(h)];
    this.mSpaceURL = h;
    this.mSpace || Kata.error("Couldn't find loopback space: " + h.toString());
    this.mObjectID = {};
    this.mLocalID = {}
  };
  Kata.extend(Kata.LoopbackSpaceConnection, Kata.SpaceConnection.prototype);
  Kata.LoopbackSpaceConnection.prototype.connectObject = function(j, h, o, q) {
    this.mSpace.connectObject(j, {connected:Kata.bind(this.connectResponse, this), message:Kata.bind(this.receiveODPMessage, this), prox:Kata.bind(this.proxEvent, this), presenceLocUpdate:Kata.bind(this.presenceLocUpdate, this), scale:o.scale[0], visual:q})
  };
  Kata.LoopbackSpaceConnection.prototype.connectResponse = function(j, h, o, q) {
    this.mObjectID[j] = h;
    this.mLocalID[h] = j;
    h ? this.mParent.connectionResponse(j, true, {space:this.mSpaceURL, object:h}, o, q) : this.mParent.connectionResponse(j, false)
  };
  Kata.LoopbackSpaceConnection.prototype.disconnectObject = function(j) {
    this.mSpace.disconnectObject(j)
  };
  Kata.LoopbackSpaceConnection.prototype.sendODPMessage = function(j, h, o, q, u) {
    this.mSpace.sendODPMessage(j, h, o, q, u)
  };
  Kata.LoopbackSpaceConnection.prototype.receiveODPMessage = function(j, h, o, q, u) {
    this.mParent.receiveODPMessage(this.mSpaceURL, j, h, o, q, u)
  };
  Kata.LoopbackSpaceConnection.prototype.registerProxQuery = function(j, h) {
    this.mSpace.registerProxQuery(j, h)
  };
  Kata.LoopbackSpaceConnection.prototype.proxEvent = function(j, h, o, q) {
    this.mParent.proxEvent(this.mSpaceURL, j, h, o, q)
  };
  Kata.LoopbackSpaceConnection.prototype.locUpdateRequest = function(j, h, o) {
    this.mSpace.locUpdateRequest(j, h, o)
  };
  Kata.LoopbackSpaceConnection.prototype.subscribe = function(j, h) {
    this.mSpace.subscriptionRequest(j, h, true)
  };
  Kata.LoopbackSpaceConnection.prototype.unsubscribe = function(j, h) {
    this.mSpace.subscriptionRequest(j, h, false)
  };
  Kata.LoopbackSpaceConnection.prototype.presenceLocUpdate = function(j, h, o, q) {
    this.mParent.presenceLocUpdate(this.mSpaceURL, j, h, o, q)
  };
  Kata.SessionManager.registerProtocolHandler("loop", Kata.LoopbackSpaceConnection);
  loopspace = new Kata.LoopbackSpace(Kata.URL("loop://localhost"))
}, "katajs/oh/plugins/loop/LoopbackSpaceConnection.js");Kata.require(["externals/protojs/protobuf.js"], function() {
  if(typeof Kata.Behavior == "undefined") {
    Kata.Behavior = {}
  }Kata.Behavior.NamedObject = function(e, j) {
    this.mName = e;
    this.mParent = j;
    this.mParent.addBehavior(this);
    this.mPorts = {}
  };
  Kata.Behavior.NamedObject.prototype.ProtocolPort = 10;
  Kata.Behavior.NamedObject.prototype._getPort = function(e) {
    var j = e;
    if(e.presenceID) {
      j = e.presenceID()
    }var h = this.mPorts[j];
    if(!h && e.bindODPPort) {
      h = e.bindODPPort(this.ProtocolPort);
      h.receive(Kata.bind(this.handleResponse, this));
      this.mPorts[j] = h
    }return h
  };
  Kata.Behavior.NamedObject.prototype.newPresence = function(e) {
    this._getPort(e).receive(Kata.bind(this._handleMessage, this))
  };
  Kata.Behavior.NamedObject.prototype.presenceInvalidated = function(e) {
    var j = this._getPort(e);
    if(j) {
      j.close();
      delete this.mPorts[e.presenceID()]
    }
  };
  Kata.Behavior.NamedObject.prototype._handleMessage = function(e, j) {
    this._getPort(j.presenceID()).send(e, PROTO.encodeUTF8(this.mName))
  };
  Kata.Behavior.NamedObjectObserver = function(e, j, h) {
    this.SUPER.constructor.call(this, e, j);
    this.mCB = h;
    this.mQueriedObjects = {}
  };
  Kata.extend(Kata.Behavior.NamedObjectObserver, Kata.Behavior.NamedObject.prototype);
  Kata.Behavior.NamedObjectObserver.prototype.remotePresence = function(e, j, h) {
    if(h) {
      this._getPort(e).send(j.endpoint(this.ProtocolPort), "");
      var o = this, q = {remote:j};
      e = setTimeout(function() {
        o._requestTimeout(q)
      }, 1E3);
      q.timer = e;
      this.mQueriedObjects[j.presenceID()] = q
    }else {
      this.mCB && this.mCB(j, h)
    }
  };
  Kata.Behavior.NamedObjectObserver.prototype._handleReply = function(e, j) {
    e.remote.name = j === null ? null : PROTO.decodeUTF8(j);
    this.mCB && this.mCB(e.remote, true);
    clearTimeout(e.timer);
    delete this.mQueriedObjects[e.remote.presenceID()]
  };
  Kata.Behavior.NamedObjectObserver.prototype._handleMessage = function(e, j, h) {
    var o = this.mQueriedObjects[e.presenceID()];
    o && h && h.length > 0 ? this._handleReply(o, h) : this.SUPER._handleMessage.call(this, e, j, h)
  };
  Kata.Behavior.NamedObjectObserver.prototype._requestTimeout = function(e) {
    this._handleReply(e, null)
  }
}, "katajs/oh/behavior/NamedObject.js");Kata.require(["katajs/oh/impl/ScriptProtocol.js", "katajs/core/MessageDispatcher.js"], function() {
  Kata.HostedObject = function(e, j) {
    this.mObjectHost = e;
    this.mID = j;
    this.mScriptChannel = null;
    j = {};
    var h = Kata.ScriptProtocol.FromScript.Types;
    j[h.Connect] = Kata.bind(this._handleConnect, this);
    j[h.Disconnect] = Kata.bind(this._handleDisconnect, this);
    j[h.SendODPMessage] = Kata.bind(this._handleSendODPMessage, this);
    j[h.Query] = Kata.bind(this._handleQuery, this);
    j[h.Location] = Kata.bind(this._handleLocUpdateRequest, this);
    j[h.Subscription] = Kata.bind(this._handleSubscriptionRequest, this);
    j[h.CreateObject] = Kata.bind(this._handleCreateObject, this);
    j[h.GraphicsMessage] = Kata.bind(this._handleGraphicsMessage, this);
    j[h.DisableGUIMessage] = Kata.bind(e.unregisterSimulationCallback, e, "graphics", this);
    j[h.EnableGUIMessage] = Kata.bind(e.registerSimulationCallback, e, "graphics", this);
    j[h.GUIMessage] = Kata.bind(this._handleGUIMessage, this);
    this.mScriptMessageDispatcher = new Kata.MessageDispatcher(j)
  };
  Kata.HostedObject.prototype.getObjectHost = function() {
    return this.mObjectHost
  };
  Kata.HostedObject.prototype.getID = function() {
    return this.mID
  };
  Kata.HostedObject.prototype.sendScriptMessage = function(e) {
    this.mScriptChannel ? this.mScriptChannel.sendMessage(e) : Kata.warn("Couldn't send script message: no script.")
  };
  Kata.HostedObject.prototype.messageFromScript = function(e, j) {
    j = Kata.ScriptProtocol.FromScript.reconstitute(j);
    this.mScriptMessageDispatcher.dispatch(e, j)
  };
  Kata.HostedObject.prototype._handleConnect = function(e, j) {
    this.mObjectHost.connect(this, j, j.auth)
  };
  Kata.HostedObject.prototype.connectionResponse = function(e, j, h, o) {
    var q = null;
    q = e ? new Kata.ScriptProtocol.ToScript.Connected(j.space, j.object, h, undefined, o) : new Kata.ScriptProtocol.ToScript.ConnectionFailed(j.space, j.object);
    this.sendScriptMessage(q)
  };
  Kata.HostedObject.prototype.disconnected = function(e) {
    this.sendScriptMessage(new Kata.ScriptProtocol.ToScript.Disconnected(e))
  };
  Kata.HostedObject.prototype._handleDisconnect = function(e, j) {
    this.mObjectHost.disconnect(this, j)
  };
  Kata.HostedObject.prototype._handleSendODPMessage = function(e, j) {
    this.mObjectHost.sendODPMessage(j.space, j.source_object, j.source_port, j.dest_object, j.dest_port, j.payload)
  };
  Kata.HostedObject.prototype.receiveODPMessage = function(e, j, h, o, q, u) {
    this.sendScriptMessage(new Kata.ScriptProtocol.ToScript.ReceiveODPMessage(e, j, h, o, q, u))
  };
  Kata.HostedObject.prototype._handleQuery = function(e, j) {
    this.mObjectHost.registerProxQuery(j.space, j.id, j.sa)
  };
  Kata.HostedObject.prototype.proxEvent = function(e, j, h, o) {
    this.sendScriptMessage(typeof o !== "undefined" ? new Kata.ScriptProtocol.ToScript.QueryEvent(e, j, h, o.loc, o.visual) : new Kata.ScriptProtocol.ToScript.QueryEvent(e, j, h))
  };
  Kata.HostedObject.prototype._handleCreateObject = function(e, j) {
    this.mObjectHost.createObject(j.script, j.constructor, j.args)
  };
  Kata.HostedObject.prototype._handleLocUpdateRequest = function(e, j) {
    e = {};
    Kata.LocationCopyUnifyTime(j, e);
    this.mObjectHost.locUpdateRequest(j.space, j.id, e, j.visual)
  };
  Kata.HostedObject.prototype.presenceLocUpdate = function(e, j, h, o) {
    this.sendScriptMessage(new Kata.ScriptProtocol.ToScript.PresenceLocUpdate(e, j, h, o))
  };
  Kata.HostedObject.prototype.handleMessageFromSimulation = function(e, j, h) {
    this.sendScriptMessage(h)
  };
  Kata.HostedObject.prototype._handleGraphicsMessage = function(e, j) {
    this.mObjectHost.sendToSimulation(j)
  };
  Kata.HostedObject.prototype._handleGUIMessage = function(e, j) {
    this.mObjectHost.sendToSimulation({__gui:j})
  };
  Kata.HostedObject.prototype._handleSubscriptionRequest = function(e, j) {
    j.enable ? this.mObjectHost.subscribe(j.space, j.id, j.observed) : this.mObjectHost.unsubscribe(j.space, j.id, j.observed)
  };
  Kata.HostedObject.prototype.messageFromSimulation = function() {
  };
  Kata.HostedObject.prototype.createScript = function(e, j, h) {
    e = new Kata.WebWorker("katajs/oh/impl/BootstrapScript.js", "Kata.BootstrapScript", {realScript:e, realClass:j, realArgs:h});
    this.mScriptChannel = e.getChannel();
    this.mScriptChannel.registerListener(Kata.bind(this.messageFromScript, this));
    e.go()
  }
}, "katajs/oh/HostedObject.js");Kata.require(["katajs/oh/ObjectHost.js"], function() {
  Kata.SpaceConnection = function(e) {
    this.mParent = e
  };
  Kata.SpaceConnection.prototype.connectObject = function() {
    Kata.notImplemented("SpaceConnection.connectObject")
  };
  Kata.SpaceConnection.prototype.disconnectObject = function() {
    Kata.notImplemented("SpaceConnection.disconnectObject")
  };
  Kata.SpaceConnection.prototype.sendODPMessage = function() {
    Kata.notImplemented("SpaceConnection.sendODPMessage")
  };
  Kata.SpaceConnection.prototype.registerProxQuery = function() {
    Kata.notImplemented("SpaceConnection.registerQuery")
  };
  Kata.SpaceConnection.prototype.locUpdateRequest = function() {
    Kata.notImplemented("SpaceConnection.locUpdateRequest")
  };
  Kata.SpaceConnection.prototype.subscribe = function() {
    Kata.notImplemented("SpaceConnection.subscribe")
  };
  Kata.SpaceConnection.prototype.unsubscribe = function() {
    Kata.notImplemented("SpaceConnection.unsubscribe")
  }
}, "katajs/oh/SpaceConnection.js");Kata.require(["katajs/oh/Simulation.js"], function() {
  var e = Kata.Simulation.prototype;
  Kata.GraphicsSimulation = function(j, h, o) {
    e.constructor.call(this, h);
    this.mElement = o;
    h = this.constructor;
    h._drivers == undefined && Kata.error("No graphics drivers available.");
    drv = h._drivers[j];
    drv == undefined && Kata.error('No graphics driver called "' + j + '" available.');
    this.mGFX = new drv(function() {
    }, o);
    this.mGFX.setInputCallback(Kata.bind(this._handleInputMessage, this))
  };
  Kata.GraphicsSimulation.YFOV_DEGREES = 23.3;
  Kata.GraphicsSimulation.CAMERA_NEAR = 0.1;
  Kata.GraphicsSimulation.CAMERA_FAR = 2E3;
  Kata.GraphicsSimulation.DRAG_THRESHOLD = 5;
  Kata.extend(Kata.GraphicsSimulation, e);
  Kata.GraphicsSimulation.prototype.receivedMessage = function(j, h) {
    if(!h.__gui) {
      h = Kata.ScriptProtocol.FromScript.reconstitute(h);
      e.receivedMessage.apply(this, arguments);
      this.mGFX.send(h)
    }
  };
  Kata.GraphicsSimulation.registerDriver = function(j, h) {
    if(this._drivers == undefined) {
      this._drivers = {}
    }this._drivers[j] = h
  };
  Kata.GraphicsSimulation.initializeDriver = function(j) {
    if(!this._drivers || !this._drivers[j]) {
      Kata.error("Couldn't find graphics driver: " + j)
    }else {
      for(var h = this._drivers[j], o = new Array(arguments.length - 1), q = 1;q < arguments.length;q++) {
        o[q - 1] = arguments[q]
      }h.initialize.apply(undefined, o)
    }
  };
  Kata.GraphicsSimulation.prototype._handleInputMessage = function(j) {
    this.mChannel.sendMessage(new Kata.ScriptProtocol.ToScript.GUIMessage(j))
  }
}, "katajs/oh/GraphicsSimulation.js");Kata.require(["katajs/core/Channel.js", "katajs/core/Math.uuid.js"], function() {
  function e(o, q) {
    return function(u) {
      o._onMessage(q, u.data)
    }
  }
  function j(o, q) {
    return function() {
      o._onOpen(q)
    }
  }
  function h(o, q) {
    return function() {
      o._onClose(q)
    }
  }
  if(typeof WebSocket != "undefined") {
    Kata.TCPSST = function(o, q, u) {
      u || (u = 1);
      this.mUUID = Math.uuid();
      this.mURI = "ws://" + o + ":" + q + "/" + this.mUUID;
      this.mSockets = new Array(u);
      this.mConnected = [];
      this.mMessageQueue = [];
      for(o = 0;o < u;o++) {
        this._connectSocket(o)
      }this.mNextSubstream = 1;
      this.mSubstreams = {}
    };
    Kata.TCPSST.prototype._connectSocket = function(o) {
      this.mSockets[o] && this.mSockets[o].readyState == WebSocket.CONNECTED && this.mConnected--;
      var q = new WebSocket(this.mURI);
      q.onopen = j(this, o);
      q.onclose = h(this, o);
      q.onmessage = e(this, o);
      this.mSockets[o] = q
    };
    Kata.TCPSST.prototype._onClose = function(o) {
      network_debug && console.log("Closed socket " + o);
      o = this.mConnected.indexOf(o);
      o != -1 && this.mConnected.splice(o, 1);
      for(var q in this.mSubstreams) {
        this.mSubstreams[q].callListeners(null)
      }
    };
    Kata.TCPSST.prototype._onOpen = function(o) {
      network_debug && console.log("Opened socket " + o);
      this.mConnected.push(o);
      for(var q = 0;q < this.mMessageQueue.length;q++) {
        this.mSockets[o].send(this.mMessageQueue[q])
      }this.mMessageQueue = []
    };
    Kata.TCPSST.prototype._onMessage = function(o, q) {
      var u = q.indexOf("%");
      o = parseInt(q.substr(0, u), 16);
      q = q.substr(u + 1);
      if(!this.mSubstreams[o]) {
        u = new Kata.TCPSST.Substream(this, o);
        this.mSubstreams[o] = u
      }this.mSubstreams[o].callListeners(q)
    };
    Kata.TCPSST.prototype.send = function(o, q) {
      o = o.toString(16) + "%" + q;
      this.mConnected.length == 0 ? this.mMessageQueue.push(o) : this.mSockets[this.mConnected[Math.floor(Math.random() * this.mConnected.length)]].send(o)
    };
    Kata.TCPSST.prototype._getNewSubstreamID = function() {
      var o = this.mNextSubstream;
      this.mNextSubstream += 2;
      return o
    };
    Kata.TCPSST.prototype.clone = function() {
      var o = this._getNewSubstreamID(), q = new Kata.TCPSST.Substream(this, o);
      return this.mSubstreams[o] = q
    };
    Kata.TCPSST.Substream = function(o, q) {
      this.mOwner = o;
      this.mWhich = q;
      Kata.Channel.call(this)
    };
    Kata.extend(Kata.TCPSST.Substream, Kata.Channel.prototype);
    Kata.TCPSST.Substream.prototype.sendMessage = function(o) {
      this.mOwner.send(this.mWhich, o)
    };
    Kata.TCPSST.Substream.prototype.getTopLevelStream = function() {
      return this.mOwner
    };
    Kata.TCPSST.Substream.prototype.close = function() {
    }
  }else {
    Kata.warn("WebSockets not available.")
  }
}, "katajs/network/TCPSST.js");Kata.require([], function() {
  if(typeof Kata.Loopback == "undefined") {
    Kata.Loopback = {}
  }Kata.Loopback.Loc = function() {
    this.mObjects = {};
    this.mListeners = []
  };
  Kata.Loopback.Loc.prototype.addListener = function(e) {
    this.mListeners.append(e)
  };
  Kata.Loopback.Loc.prototype._notify = function() {
    for(listener in this.mListeners) {
      listener.apply(undefined, arguments)
    }
  };
  Kata.Loopback.Loc.prototype.add = function(e, j, h) {
    this.mObjects[e] && Kata.warn("Loopback.Loc trying to add an existing object." + e);
    this.mObjects[e] = {loc:j, visual:h}
  };
  Kata.Loopback.Loc.prototype._checkExists = function(e) {
    if(!this.mObjects[e]) {
      return false
    }return true
  };
  Kata.Loopback.Loc.prototype.remove = function(e) {
    if(this._checkExists(e)) {
      delete this.mObjects[e]
    }else {
      Kata.warn("Loopback.Loc trying to remove unknown object." + e)
    }
  };
  Kata.Loopback.Loc.prototype.update = function(e, j, h) {
    if(this._checkExists(e)) {
      j && Kata.LocationReset(j, this.mObjects[e].loc);
      if(h) {
        this.mObjects[e].visual = h
      }this._notify(e, j, h)
    }else {
      Kata.warn("Trying to update location for non-existant object: " + e)
    }
  };
  Kata.Loopback.Loc.prototype.updatePosition = function(e, j, h) {
    this.update(e, {pos:j, time:h})
  };
  Kata.Loopback.Loc.prototype.updateVelocity = function(e, j) {
    this.update(e, {vel:j})
  };
  Kata.Loopback.Loc.prototype.updateOrientation = function(e, j, h) {
    this.update(e, {orient:j, time:h})
  };
  Kata.Loopback.Loc.prototype.updateAngularVelocity = function(e, j, h) {
    this.update(e, {angvel:j, angaxis:h})
  };
  Kata.Loopback.Loc.prototype.updateBounds = function(e, j, h) {
    this.update(e, {scale:j, time:h})
  };
  Kata.Loopback.Loc.prototype.updateVisual = function(e, j) {
    this.update(e, {}, j)
  };
  Kata.Loopback.Loc.prototype.lookup = function(e) {
    return this.mObjects[e]
  }
}, "katajs/space/loop/Loc.js");Kata.require([], function() {
  if(typeof Kata.Loopback == "undefined") {
    Kata.Loopback = {}
  }Kata.Loopback.Subscription = function(e) {
    this.mSpace = e;
    this.mSubscribers = {}
  };
  Kata.Loopback.Subscription.prototype.addObject = function(e) {
    this.mSubscribers[e] = {}
  };
  Kata.Loopback.Subscription.prototype.removeObject = function(e) {
    delete this.mSubscribers[e];
    for(var j in this.mSubscribers) {
      delete this.mSubscribers[j][e]
    }
  };
  Kata.Loopback.Subscription.prototype.subscribe = function(e, j) {
    if(this.mSubscribers[j]) {
      this.mSubscribers[j][e] = e
    }
  };
  Kata.Loopback.Subscription.prototype.unsubscribe = function(e, j) {
    this.mSubscribers[j] && delete this.mSubscribers[j][e]
  };
  Kata.Loopback.Subscription.prototype.notify = function(e, j, h) {
    var o = this.mSubscribers[e];
    for(var q in o) {
      j(q)
    }h && j(e)
  }
}, "katajs/space/loop/Subscription.js");Kata.require([], function() {
  if(typeof Kata.Loopback == "undefined") {
    Kata.Loopback = {}
  }Kata.Loopback.EveryoneProx = function(e) {
    this.mSpace = e;
    this.mObjects = {};
    this.mQueriers = {}
  };
  Kata.Loopback.EveryoneProx.prototype.addObject = function(e) {
    if(!this.mObjects[e]) {
      this.mObjects[e] = e;
      for(var j in this.mQueriers) {
        j != e && this.mSpace.proxResult(j, e, true)
      }
    }
  };
  Kata.Loopback.EveryoneProx.prototype.removeObject = function(e) {
    if(this.mObjects[e]) {
      delete this.mObjects[e];
      for(var j in this.mQueriers) {
        j != e && this.mSpace.proxResult(j, e, false)
      }
    }
  };
  Kata.Loopback.EveryoneProx.prototype.addQuery = function(e) {
    if(!this.mQueriers[e]) {
      this.mQueriers[e] = e;
      for(var j in this.mObjects) {
        e != j && this.mSpace.proxResult(e, j, true)
      }
    }
  };
  Kata.Loopback.EveryoneProx.prototype.removeQuery = function(e) {
    this.mQueriers[e] && delete this.mQueriers[e]
  }
}, "katajs/space/loop/EveryoneProx.js");Kata.require(["katajs/oh/SpaceConnection.js", "katajs/core/Time.js", "katajs/core/Math.uuid.js", "katajs/space/loop/Loc.js", "katajs/space/loop/EveryoneProx.js", "katajs/space/loop/Subscription.js", "katajs/core/Location.js"], function() {
  Kata.LoopbackSpace = function(e) {
    var j = Kata.URL.host(e);
    Kata.LoopbackSpace.spaces[j] && Kata.warn("Overwriting static LoopbackSpace map entry for " + e);
    Kata.LoopbackSpace.spaces[j] = this;
    this.mID = e;
    this.netdelay = 10;
    this.mObjects = {};
    this.mLoc = new Kata.Loopback.Loc;
    this.mProx = new Kata.Loopback.EveryoneProx(this);
    this.mSubscription = new Kata.Loopback.Subscription(this)
  };
  Kata.LoopbackSpace.spaces = {};
  Kata.LoopbackSpace.prototype.connectObject = function(e, j) {
    var h = this;
    setTimeout(function() {
      h._connectObject(e, j)
    }, this.netdelay)
  };
  Kata.LoopbackSpace._fakeUUIDs = 100;
  Kata.LoopbackSpace.prototype._connectObject = function(e, j) {
    var h;
    h = Kata.DEBUG_FAKE_UUID ? "fake-uuid-" + Kata.LoopbackSpace._fakeUUIDs++ : Math.uuid();
    var o = Kata.LocationIdentity(Kata.now(this.mID));
    o.scale = [j.scale, j.scale, j.scale];
    this.mLoc.add(h, o, j.visual);
    this.mProx.addObject(h);
    this.mSubscription.addObject(h);
    this.mObjects[h] = j;
    j.connected(e, h, o, j.visual)
  };
  Kata.LoopbackSpace.prototype.disconnectObject = function(e) {
    var j = this;
    setTimeout(function() {
      j._disconnectObject(e)
    }, this.netdelay)
  };
  Kata.LoopbackSpace.prototype._disconnectObject = function(e) {
    this.mSubscription.removeObject(e);
    this.mProx.removeQuery(e);
    this.mProx.removeObject(e);
    this.mLoc.remove(e);
    delete this.mObjects[e]
  };
  Kata.LoopbackSpace.prototype.sendODPMessage = function(e, j, h, o, q) {
    var u = this;
    setTimeout(function() {
      u._sendODPMessage(e, j, h, o, q)
    }, this.netdelay)
  };
  Kata.LoopbackSpace.prototype._sendODPMessage = function(e, j, h, o, q) {
    if(this.mObjects[e]) {
      var u = this.mObjects[h];
      u ? u.message(e, j, h, o, q) : Kata.warn("LoopbackSpace got message to non-existant object: " + h)
    }else {
      Kata.warn("LoopbackSpace got message from non-existant object: " + e)
    }
  };
  Kata.LoopbackSpace.prototype.registerProxQuery = function(e, j) {
    var h = this;
    setTimeout(function() {
      h._registerProxQuery(e, j)
    }, this.netdelay)
  };
  Kata.LoopbackSpace.prototype._registerProxQuery = function(e) {
    this.mProx.addQuery(e)
  };
  Kata.LoopbackSpace.prototype.proxResult = function(e, j, h) {
    var o = this.mObjects[e];
    if(o) {
      var q = this.mLoc.lookup(j), u = {loc:q.loc, visual:q.visual};
      Kata.LocationCopyUnifyTime(u.loc, q.loc);
      o.prox(e, j, h, u)
    }else {
      Kata.warn("LoopbackSpace got query result for non-existant object: " + e)
    }
  };
  Kata.LoopbackSpace.prototype.locUpdateRequest = function(e, j, h) {
    this._locUpdateRequest(e, j, h)
  };
  Kata.LoopbackSpace.prototype._locUpdateRequest = function(e, j, h) {
    this.mLoc.update(e, j, h);
    var o = this;
    this.mSubscription.notify(e, function(q) {
      o.mObjects[q].presenceLocUpdate(e, q, j, h)
    }, true)
  };
  Kata.LoopbackSpace.prototype.subscriptionRequest = function(e, j, h) {
    var o = this;
    setTimeout(function() {
      o._subscriptionRequest(e, j, h)
    }, this.netdelay)
  };
  Kata.LoopbackSpace.prototype._subscriptionRequest = function(e, j, h) {
    h ? this.mSubscription.subscribe(e, j) : this.mSubscription.unsubscribe(e, j)
  };
  Kata.LoopbackSpace.prototype.sendMessage = function() {
  }
}, "katajs/space/loop/Space.js");(function() {
  for(var e in Kata.closureIncluded) {
    Kata.setIncluded(e)
  }
})();
