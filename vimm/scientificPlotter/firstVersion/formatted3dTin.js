/*
 * 3dtin.js
 * Copyright (C) 2010  Jayesh Salvi <jayesh@altcanvas.com>
 * All Rights Reserved
 *
 * mjs.js
 * Copyright (c) 2010 Mozilla Corporation
 * Copyright (c) 2010 Vladimir Vukicevic
 */
try {
    var t = new WebGLFloatArray(1)
}
catch (e) {
    WebGLFloatArray = Array
}
var n0e2 = WebGLFloatArray, V3 = {};
V3._temp1 = new n0e2(3);
V3._temp2 = new n0e2(3);
V3._temp3 = new n0e2(3);
if (n0e2 == Array)
{
    V3.x = [1, 0, 0];
    V3.y = [0, 1, 0];
    V3.z = [0, 0, 1];
    V3.$ = function (a, b, c)
    {
        return [a, b, c];
    };
    V3.clone = function (a)
    {
        return [a[0], a[1], a[2]];
    }
}
else
{
    V3.x = new n0e2([1, 0, 0]);
    V3.y = new n0e2([0, 1, 0]);
    V3.z = new n0e2([0, 0, 1]);
    V3.$ = function (a, b, c)
    {
        return new n0e2([a, b, c]);
    };
    V3.clone = function (a)
    {
        return new n0e2(a);
    }
}
V3.u = V3.x;
V3.v = V3.y;
V3.add = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(3);
    }
    c[0] = a[0] + b[0];
    c[1] = a[1] + b[1];
    c[2] = a[2] + b[2];
    return c;
};
V3.sub = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(3);
    }
    c[0] = a[0] - b[0];
    c[1] = a[1] - b[1];
    c[2] = a[2] - b[2];
    return c;
};
V3.neg = function (a, b)
{
    if (b == undefined) {
        b = new n0e2(3);
    }
    b[0] =- a[0];
    b[1] =- a[1];
    b[2] =- a[2];
    return b;
};
V3.direction = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(3);
    }
    return V3.normalize(V3.sub(a, b, c), c);
};
V3.length = function (a)
{
    return Math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
};
V3.n0e3 = function (a)
{
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2];
};
V3.normalize = function (a, b)
{
    if (b == undefined) {
        b = new n0e2(3);
    }
    var c = 1 / V3.length(a);
    b[0] = a[0] * c;
    b[1] = a[1] * c;
    b[2] = a[2] * c;
    return b;
};
V3.scale = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(3);
    }
    c[0] = a[0] * b;
    c[1] = a[1] * b;
    c[2] = a[2] * b;
    return c;
};
V3.mul = V3.scale;
V3.dot = function (a, b)
{
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
};
V3.cross = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(3);
    }
    c[0] = a[1] * b[2] - a[2] * b[1];
    c[1] = a[2] * b[0] - a[0] * b[2];
    c[2] = a[0] * b[1] - a[1] * b[0];
    return c;
};
V3.dump = function (a, b, c)
{
    c != undefined && b(c);
    b("[" + a[0].toFixed(3) + a[1].toFixed(3) + a[2].toFixed(3) + "]")
};
V3.toString = function (a)
{
    if (!a) {
        return "null";
    }
    return "[" + a[0].toFixed(3) + ", " + a[1].toFixed(3) + ", " + a[2].toFixed(3) + "]";
};
var n0f7 = {};
n0f7._temp1 = new n0e2(16);
n0f7._temp2 = new n0e2(16);
if (n0e2 == Array)
{
    n0f7.I = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
    n0f7.$ = function (a, b, c, d, f, h, i, j, k, l, n, p, o, r, m, q)
    {
        return [a, b, c, d, f, h, i, j, k, l, n, p, o, r, m, q];
    };
    n0f7.clone = function (a)
    {
        return new [a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11]];
    }
}
else
{
    n0f7.I = new n0e2([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);
    n0f7.$ = function (a, b, c, d, f, h, i, j, k, l, n, p, o, r, m, q)
    {
        return new n0e2([a, b, c, d, f, h, i, j, k, l, n, p, o, r, m, q]);
    };
    n0f7.clone = function (a)
    {
        return new n0e2(a);
    }
}
n0f7.identity = n0f7.I;
n0f7.n0e4 = function (a, b)
{
    if (b == undefined) {
        b = new n0e2(16);
    }
    var c = a[5] * a[10] * a[15] + a[6] * a[11] * a[13] + a[7] * a[9] * a[14] - a[13] * a[10] * a[7] - a[14] * a[11] * a[5] - a[15] * a[9] * a[6], 
    d = (a[4] * a[10] * a[15] + a[6] * a[11] * a[12] + a[7] * a[8] * a[14] - a[12] * a[10] * a[7] - a[14] * a[11] * a[4] - a[15] * a[8] * a[6]) *- 1, 
    f = a[4] * a[9] * a[15] + a[5] * a[11] * a[12] + a[7] * a[8] * a[13] - a[12] * a[9] * a[7] - a[13] * a[11] * a[4] - a[15] * a[8] * a[5], 
    h = (a[4] * a[9] * a[14] + a[5] * a[10] * a[12] + a[6] * a[8] * a[13] - a[12] * a[9] * a[6] - a[13] * a[10] * a[4] - a[14] * a[8] * a[5]) *- 1, 
    i = a[0] * c + a[1] * d + a[2] * f + a[3] * h;
    if (i == 0) {
        throw "matrix not invertible";
    }
    var j = (a[1] * a[10] * a[15] + a[2] * a[11] * a[13] + a[3] * a[9] * a[14] +- a[13] * a[10] * a[3] - a[14] * a[11] * a[1] - a[15] * a[9] * a[2]) *- 1, 
    k = a[0] * a[10] * a[15] + a[2] * a[11] * a[12] + a[3] * a[8] * a[14] +- a[12] * a[10] * a[3] - a[14] * a[11] * a[0] - a[15] * a[8] * a[2], 
    l = (a[0] * a[9] * a[15] + a[1] * a[11] * a[12] + a[3] * a[8] * a[13] +- a[12] * a[9] * a[3] - a[13] * a[11] * a[0] - a[15] * a[8] * a[1]) *- 1, 
    n = a[0] * a[9] * a[14] + a[1] * a[10] * a[12] + a[2] * a[8] * a[13] +- a[12] * a[9] * a[2] - a[13] * a[10] * a[0] - a[14] * a[8] * a[1], 
    p = a[1] * a[6] * a[15] + a[2] * a[7] * a[13] + a[3] * a[5] * a[14] +- a[13] * a[6] * a[3] - a[14] * a[7] * a[1] - a[15] * a[5] * a[2], 
    o = (a[0] * a[6] * a[15] + a[2] * a[7] * a[12] + a[3] * a[4] * a[14] +- a[12] * a[6] * a[3] - a[14] * a[7] * a[0] - a[15] * a[4] * a[2]) *- 1, 
    r = a[0] * a[5] * a[15] + a[1] * a[7] * a[12] + a[3] * a[4] * a[13] +- a[12] * a[5] * a[3] - a[13] * a[7] * a[0] - a[15] * a[4] * a[1], 
    m = (a[0] * a[5] * a[14] + a[1] * a[6] * a[12] + a[2] * a[4] * a[13] +- a[12] * a[5] * a[2] - a[13] * a[6] * a[0] - a[14] * a[4] * a[1]) *- 1, 
    q = (a[1] * a[6] * a[11] + a[2] * a[7] * a[9] + a[3] * a[5] * a[10] +- a[9] * a[6] * a[3] - a[10] * a[7] * a[1] - a[11] * a[5] * a[2]) *- 1, 
    s = a[0] * a[6] * a[11] + a[2] * a[7] * a[8] + a[3] * a[4] * a[10] +- a[8] * a[6] * a[3] - a[10] * a[7] * a[0] - a[11] * a[4] * a[2], 
    u = (a[0] * a[5] * a[11] + a[1] * a[7] * a[8] + a[3] * a[4] * a[9] +- a[8] * a[5] * a[3] - a[9] * a[7] * a[0] - a[11] * a[4] * a[1]) *- 1;
    a = a[0] * a[5] * a[10] + a[1] * a[6] * a[8] + a[2] * a[4] * a[9] +- a[8] * a[5] * a[2] - a[9] * a[6] * a[0] - a[10] * a[4] * a[1];
    b[0] = c / i;
    b[1] = j / i;
    b[2] = p / i;
    b[3] = q / i;
    b[4] = d / i;
    b[5] = k / i;
    b[6] = o / i;
    b[7] = s / i;
    b[8] = f / i;
    b[9] = l / i;
    b[10] = r / i;
    b[11] = u / i;
    b[12] = h / i;
    b[13] = n / i;
    b[14] = m / i;
    b[15] = a / i;
    return b;
};
n0f7.makeFrustum = function (a, b, c, d, f, h, i)
{
    if (i == undefined) {
        i = new n0e2(16);
    }
    i[0] = 2 * f / (b - a);
    i[1] = 0;
    i[2] = 0;
    i[3] = 0;
    i[4] = 0;
    i[5] = 2 * f / (d - c);
    i[6] = 0;
    i[7] = 0;
    i[8] = (b + a) / (b - a);
    i[9] = (d + c) / (d - c);
    i[10] =- (h + f) / (h - f);
    i[11] =- 1;
    i[12] = 0;
    i[13] = 0;
    i[14] =- 2 * h * f / (h - f);
    i[15] = 0;
    return i;
};
n0f7.n11f = function (a, b, c, d, f)
{
    a = c * Math.tan(a * Math.PI / 360);
    var h =- a;
    return n0f7.makeFrustum(h * b, a * b, h, a, c, d, f);
};
n0f7.n120 = function (a, b, c, d, f, h, i)
{
    if (i == undefined) {
        i = new n0e2(16);
    }
    i[0] = 2 / (b - a);
    i[1] = 0;
    i[2] = 0;
    i[3] = 0;
    i[4] = 0;
    i[5] = 2 / (d - c);
    i[6] = 0;
    i[7] = 0;
    i[8] = 0;
    i[9] = 0;
    i[10] =- 2 / (h - f);
    i[11] = 0;
    i[12] =- (b + a) / (b - a);
    i[13] =- (d + c) / (d - c);
    i[14] =- (h + f) / (h - f);
    i[15] = 1;
    return i;
};
n0f7.mul = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(16);
    }
    c[0] = b[0] * a[0] + b[1] * a[4] + b[2] * a[8] + b[3] * a[12];
    c[1] = b[0] * a[1] + b[1] * a[5] + b[2] * a[9] + b[3] * a[13];
    c[2] = b[0] * a[2] + b[1] * a[6] + b[2] * a[10] + b[3] * a[14];
    c[3] = b[0] * a[3] + b[1] * a[7] + b[2] * a[11] + b[3] * a[15];
    c[4] = b[4] * a[0] + b[5] * a[4] + b[6] * a[8] + b[7] * a[12];
    c[5] = b[4] * a[1] + b[5] * a[5] + b[6] * a[9] + b[7] * a[13];
    c[6] = b[4] * a[2] + b[5] * a[6] + b[6] * a[10] + b[7] * a[14];
    c[7] = b[4] * a[3] + b[5] * a[7] + b[6] * a[11] + b[7] * a[15];
    c[8] = b[8] * a[0] + b[9] * a[4] + b[10] * a[8] + b[11] * a[12];
    c[9] = b[8] * a[1] + b[9] * a[5] + b[10] * a[9] + b[11] * a[13];
    c[10] = b[8] * a[2] + b[9] * a[6] + b[10] * a[10] + b[11] * a[14];
    c[11] = b[8] * a[3] + b[9] * a[7] + b[10] * a[11] + b[11] * a[15];
    c[12] = b[12] * a[0] + b[13] * a[4] + b[14] * a[8] + b[15] * a[12];
    c[13] = b[12] * a[1] + b[13] * a[5] + b[14] * a[9] + b[15] * a[13];
    c[14] = b[12] * a[2] + b[13] * a[6] + b[14] * a[10] + b[15] * a[14];
    c[15] = b[12] * a[3] + b[13] * a[7] + b[14] * a[11] + b[15] * a[15];
    return c;
};
n0f7.makeRotate = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(16);
    }
    b = V3.normalize(b, V3._temp1);
    var d = b[0], f = b[1];
    b = b[2];
    var h = Math.cos(a), i = 1 - h;
    a = Math.sin(a);
    c[0] = d * d * i + h;
    c[1] = f * d * i + b * a;
    c[2] = b * d * i - f * a;
    c[3] = 0;
    c[4] = d * f * i - b * a;
    c[5] = f * f * i + h;
    c[6] = f * b * i + d * a;
    c[7] = 0;
    c[8] = d * b * i + f * a;
    c[9] = f * b * i - d * a;
    c[10] = b * b * i + h;
    c[11] = 0;
    c[12] = 0;
    c[13] = 0;
    c[14] = 0;
    c[15] = 1;
    return c;
};
n0f7.rotate = function (a, b, c, d)
{
    a = n0f8.$(b, a);
    a = n0f8.ton0f7(a);
    return n0f7.mul(c, a, d);
};
n0f7.makeScale3 = function (a, b, c, d)
{
    if (d == undefined) {
        d = new n0e2(16);
    }
    d[0] = a;
    d[1] = 0;
    d[2] = 0;
    d[3] = 0;
    d[4] = 0;
    d[5] = b;
    d[6] = 0;
    d[7] = 0;
    d[8] = 0;
    d[9] = 0;
    d[10] = c;
    d[11] = 0;
    d[12] = 0;
    d[13] = 0;
    d[14] = 0;
    d[15] = 1;
    return d;
};
n0f7.makeScale1 = function (a, b)
{
    return n0f7.makeScale3(a, a, a, b);
};
n0f7.makeScale = function (a, b)
{
    return n0f7.makeScale3(a[0], a[1], a[2], b);
};
n0f7.scale3 = function (a, b, c, d, f)
{
    n0f7.makeScale3(a, b, c, n0f7._temp1);
    return n0f7.mul(d, n0f7._temp1, f);
};
n0f7.scale1 = function (a, b, c)
{
    n0f7.makeScale3(a, a, a, n0f7._temp1);
    return n0f7.mul(b, n0f7._temp1, c);
};
n0f7.scale = function (a, b, c)
{
    n0f7.makeScale3(a[0], a[1], a[2], n0f7._temp1);
    return n0f7.mul(b, n0f7._temp1, c);
};
n0f7.makeTranslate3 = function (a, b, c, d)
{
    if (d == undefined) {
        d = new n0e2(16);
    }
    d[0] = 1;
    d[1] = 0;
    d[2] = 0;
    d[3] = 0;
    d[4] = 0;
    d[5] = 1;
    d[6] = 0;
    d[7] = 0;
    d[8] = 0;
    d[9] = 0;
    d[10] = 1;
    d[11] = 0;
    d[12] = a;
    d[13] = b;
    d[14] = c;
    d[15] = 1;
    return d;
};
n0f7.makeTranslate1 = function (a, b)
{
    return n0f7.makeTranslate3(a, a, a, b);
};
n0f7.makeTranslate = function (a, b)
{
    return n0f7.makeTranslate3(a[0], a[1], a[2], b);
};
n0f7.translate3 = function (a, b, c, d, f)
{
    n0f7.makeTranslate3(a, b, c, n0f7._temp1);
    return n0f7.mul(d, n0f7._temp1, f);
};
n0f7.translate1 = function (a, b, c)
{
    n0f7.makeTranslate3(a, a, a, n0f7._temp1);
    return n0f7.mul(b, n0f7._temp1, c);
};
n0f7.translate = function (a, b, c)
{
    n0f7.makeTranslate3(a[0], a[1], a[2], n0f7._temp1);
    return n0f7.mul(b, n0f7._temp1, c);
};
n0f7.n0fd = function (a, b)
{
    if (a == b)
    {
        b = 0;
        b = a[1];
        a[1] = a[4];
        a[4] = b;
        b = a[2];
        a[2] = a[8];
        a[8] = b;
        b = a[3];
        a[3] = a[12];
        a[12] = b;
        b = a[6];
        a[6] = a[9];
        a[9] = b;
        b = a[7];
        a[7] = a[13];
        a[13] = b;
        b = a[11];
        a[11] = a[14];
        a[14] = b;
        return a
    }
    if (b == undefined) {
        b = new n0e2(16);
    }
    b[0] = a[0];
    b[1] = a[4];
    b[2] = a[8];
    b[3] = a[12];
    b[4] = a[1];
    b[5] = a[5];
    b[6] = a[9];
    b[7] = a[13];
    b[8] = a[2];
    b[9] = a[6];
    b[10] = a[10];
    b[11] = a[14];
    b[12] = a[3];
    b[13] = a[7];
    b[14] = a[11];
    b[15] = a[15];
    return b;
};
n0f7.mulV3 = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(4);
    }
    c[0] = a[0] * b[0] + a[4] * b[1] + a[8] * b[2] + a[12];
    c[1] = a[1] * b[0] + a[5] * b[1] + a[9] * b[2] + a[13];
    c[2] = a[2] * b[0] + a[6] * b[1] + a[10] * b[2] + a[14];
    c[3] = a[3] * b[0] + a[7] * b[1] + a[11] * b[2] + a[15];
    return c;
};
n0f7.toString = function (a)
{
    return "{" + a[0].toFixed(3) + "," + a[4].toFixed(3) + "," + a[8].toFixed(3) + "," + a[12].toFixed(3) + "}, \n{" + a[1].toFixed(3) + "," + a[5].toFixed(3) + "," + a[9].toFixed(3) + "," + a[13].toFixed(3) + "}, \n{" + a[2].toFixed(3) + "," + a[6].toFixed(3) + "," + a[10].toFixed(3) + "," + a[14].toFixed(3) + "}, \n{" + a[3].toFixed(3) + "," + a[7].toFixed(3) + "," + a[11].toFixed(3) + "," + a[15].toFixed(3) + "} \n";
};
var n0f8 = {};
n0f8.$ = function (a, b)
{
    var c = Math.cos(b / 2);
    b = Math.sin(b / 2);
    return new n0e2([a[0] * b, a[1] * b, a[2] * b, c]);
};
n0f8.ton0f7 = function (a, b)
{
    if (b == undefined) {
        b = new n0e2(16);
    }
    var c = a[0], d = a[1], f = a[2];
    a = a[3];
    b[0] = 1 - 2 * (d * d + f * f);
    b[1] = 2 * (c * d + f * a);
    b[2] = 2 * (c * f - d * a);
    b[3] = 0;
    b[4] = 2 * (c * d - f * a);
    b[5] = 1 - 2 * (c * c + f * f);
    b[6] = 2 * (f * d + c * a);
    b[7] = 0;
    b[8] = 2 * (c * f + d * a);
    b[9] = 2 * (d * f - c * a);
    b[10] = 1 - 2 * (c * c + d * d);
    b[11] = 0;
    b[12] = 0;
    b[13] = 0;
    b[14] = 0;
    b[15] = 1;
    return b;
};
n0f8.mul = function (a, b, c)
{
    if (c == undefined) {
        c = new n0e2(4);
    }
    c[0] = a[3] * b[0] + a[0] * b[3] + a[1] * b[2] - a[2] * b[1];
    c[1] = a[3] * b[1] + a[1] * b[3] + a[2] * b[0] - a[0] * b[2];
    c[2] = a[3] * b[2] + a[2] * b[3] + a[0] * b[1] - a[1] * b[0];
    c[3] = a[3] * b[3] - a[0] * b[0] - a[1] * b[1] - a[2] * b[2];
    return c;
};
n0f8.toEuler = function (a)
{
    var b = a[0] * a[0], c = a[1] * a[1], d = a[2] * a[2], f = a[3] * a[3], h = b + c + d + f, i = a[0] * a[1] + a[2] * a[3];
    if (i > 0.499 * h) {
        var j = 2 * atan2(a[0], a[3]);
        h = Math.PI / 2;
        a = 0;
        return [a, j, h]
    }
    if (i <- 0.499 * h) {
        j =- 2 * atan2(a[0], a[3]);
        h =- Math.PI / 2;
        a = 0;
        return [a, j, h]
    }
    j = Math.atan2(2 * a[1] * a[3] - 2 * a[0] * a[2], b - c - d + f);
    h = Math.asin(2 * i / h);
    a = Math.atan2(2 * a[0] * a[3] - 2 * a[1] * a[2], - b + c - d + f);
    return [a, j, h];
};
n0f8.toString = function (a)
{
    return "x = " + a[0].toFixed(3) + " y = " + a[1].toFixed(3) + " z = " + a[2].toFixed(3) + " w = " + a[3].toFixed(3);
};
var n0f1 = [118, 97, 114, 121, 105, 110, 103, 32, 118, 101, 99, 51, 32, 118, 76, 105, 103, 104, 116, 87, 
101, 105, 103, 104, 116, 59, 118, 97, 114, 121, 105, 110, 103, 32, 118, 101, 99, 52, 32, 118, 67, 111, 
108, 111, 114, 59, 118, 111, 105, 100, 32, 109, 97, 105, 110, 40, 118, 111, 105, 100, 41, 123, 32, 32, 
32, 32, 103, 108, 95, 70, 114, 97, 103, 67, 111, 108, 111, 114, 32, 61, 32, 118, 101, 99, 52, 40, 118, 
67, 111, 108, 111, 114, 46, 114, 103, 98, 32, 42, 32, 118, 76, 105, 103, 104, 116, 87, 101, 105, 103, 
104, 116, 44, 32, 118, 67, 111, 108, 111, 114, 46, 97, 41, 59, 125], n0f2 = [97, 116, 116, 114, 105, 98, 
117, 116, 101, 32, 118, 101, 99, 51, 32, 97, 86, 101, 114, 116, 101, 120, 80, 111, 115, 105, 116, 105, 
111, 110, 59, 97, 116, 116, 114, 105, 98, 117, 116, 101, 32, 118, 101, 99, 51, 32, 97, 86, 101, 114, 116, 
101, 120, 78, 111, 114, 109, 97, 108, 59, 97, 116, 116, 114, 105, 98, 117, 116, 101, 32, 118, 101, 99, 
52, 32, 97, 86, 101, 114, 116, 101, 120, 67, 111, 108, 111, 114, 59, 117, 110, 105, 102, 111, 114, 109, 
32, 109, 97, 116, 52, 32, 117, 77, 86, 77, 97, 116, 114, 105, 120, 59, 117, 110, 105, 102, 111, 114, 109, 
32, 109, 97, 116, 52, 32, 117, 80, 77, 97, 116, 114, 105, 120, 59, 117, 110, 105, 102, 111, 114, 109, 
32, 109, 97, 116, 52, 32, 117, 78, 77, 97, 116, 114, 105, 120, 59, 118, 97, 114, 121, 105, 110, 103, 32, 
118, 101, 99, 52, 32, 118, 67, 111, 108, 111, 114, 59, 118, 97, 114, 121, 105, 110, 103, 32, 118, 101, 
99, 51, 32, 118, 76, 105, 103, 104, 116, 87, 101, 105, 103, 104, 116, 59, 117, 110, 105, 102, 111, 114, 
109, 32, 118, 101, 99, 51, 32, 117, 65, 109, 98, 105, 101, 110, 116, 67, 111, 108, 111, 114, 59, 117, 
110, 105, 102, 111, 114, 109, 32, 118, 101, 99, 51, 32, 117, 76, 105, 103, 104, 116, 68, 105, 114, 101, 
99, 116, 105, 111, 110, 59, 117, 110, 105, 102, 111, 114, 109, 32, 118, 101, 99, 51, 32, 117, 68, 105, 
114, 101, 99, 116, 105, 111, 110, 97, 108, 67, 111, 108, 111, 114, 59, 117, 110, 105, 102, 111, 114, 109, 
32, 98, 111, 111, 108, 32, 117, 85, 115, 101, 76, 105, 103, 104, 116, 105, 110, 103, 59, 118, 111, 105, 
100, 32, 109, 97, 105, 110, 40, 118, 111, 105, 100, 41, 32, 123, 32, 32, 32, 32, 103, 108, 95, 80, 111, 
115, 105, 116, 105, 111, 110, 32, 61, 32, 117, 80, 77, 97, 116, 114, 105, 120, 32, 42, 32, 117, 77, 86, 
77, 97, 116, 114, 105, 120, 32, 42, 32, 118, 101, 99, 52, 40, 97, 86, 101, 114, 116, 101, 120, 80, 111, 
115, 105, 116, 105, 111, 110, 44, 32, 49, 46, 48, 41, 59, 32, 32, 32, 32, 118, 67, 111, 108, 111, 114, 
32, 61, 32, 97, 86, 101, 114, 116, 101, 120, 67, 111, 108, 111, 114, 59, 32, 32, 32, 32, 105, 102, 32, 
40, 33, 117, 85, 115, 101, 76, 105, 103, 104, 116, 105, 110, 103, 41, 32, 123, 32, 32, 32, 32, 32, 32, 
32, 32, 118, 76, 105, 103, 104, 116, 87, 101, 105, 103, 104, 116, 32, 61, 32, 118, 101, 99, 51, 40, 49, 
46, 48, 44, 32, 49, 46, 48, 44, 32, 49, 46, 48, 41, 59, 32, 32, 32, 32, 125, 32, 101, 108, 115, 101, 32, 
123, 32, 32, 32, 32, 118, 101, 99, 52, 32, 116, 114, 97, 110, 115, 102, 111, 114, 109, 101, 100, 78, 111, 
114, 109, 97, 108, 32, 61, 32, 117, 78, 77, 97, 116, 114, 105, 120, 32, 42, 32, 118, 101, 99, 52, 40, 
97, 86, 101, 114, 116, 101, 120, 78, 111, 114, 109, 97, 108, 44, 32, 49, 46, 48, 41, 59, 32, 32, 32, 32, 
102, 108, 111, 97, 116, 32, 100, 105, 114, 101, 99, 116, 105, 111, 110, 97, 108, 76, 105, 103, 104, 116, 
87, 101, 105, 103, 104, 116, 105, 110, 103, 32, 61, 32, 32, 32, 32, 32, 32, 32, 32, 109, 97, 120, 40, 
100, 111, 116, 40, 116, 114, 97, 110, 115, 102, 111, 114, 109, 101, 100, 78, 111, 114, 109, 97, 108, 46, 
120, 121, 122, 44, 32, 117, 76, 105, 103, 104, 116, 68, 105, 114, 101, 99, 116, 105, 111, 110, 41, 44, 
32, 48, 46, 48, 41, 59, 32, 32, 32, 32, 118, 76, 105, 103, 104, 116, 87, 101, 105, 103, 104, 116, 32, 
61, 32, 32, 32, 32, 32, 32, 32, 32, 117, 65, 109, 98, 105, 101, 110, 116, 67, 111, 108, 111, 114, 32, 
43, 32, 117, 68, 105, 114, 101, 99, 116, 105, 111, 110, 97, 108, 67, 111, 108, 111, 114, 32, 42, 32, 100, 
105, 114, 101, 99, 116, 105, 111, 110, 97, 108, 76, 105, 103, 104, 116, 87, 101, 105, 103, 104, 116, 105, 
110, 103, 59, 32, 32, 32, 32, 125, 125], gl, canvas = null;
function n0f3()
{
    try {
        gl = canvas.getContext("experimental-webgl", {
            antialias : true
        })
    }
    catch (a) {
        n09b("Error: " + a);
        return false
    }
    if (!gl) {
        n09b("Could not init WebGL");
        return false
    }
    $("#webglerrmsg").remove();
    gl.viewport(0, 0, canvas.width, canvas.height);
    return true
}
function n09b(a)
{
    $("#panel").remove();
    $("#canvas0").remove();
    $("#status").remove();
    $("#projpanel").remove();
    $("#webglerrmsg p").append(a);
    isChrome && $("#webglerrmsg #hint").append("Are you using --enable-webgl flag?");
    isFirefox && $("#webglerrmsg #hint").append("Have you set webgl options in about:config?")
}
function getShader(a, b)
{
    a = gl.createShader(a);
    gl.shaderSource(a, b);
    gl.compileShader(a);
    if (!gl.getShaderParameter(a, gl.COMPILE_STATUS)) {
        alert("Shader compiler: " + gl.getShaderInfoLog(a));
        return null
    }
    return a
}
var n0fc;
function n0e8(a)
{
    for (var b = "", c = a.length, d = 0; d < c; d++) {
        b += String.fromCharCode(a[d]);
    }
    return b
}
function n08a()
{
    var a = getShader(gl.FRAGMENT_SHADER, n0e8(n0f1)), b = getShader(gl.VERTEX_SHADER, n0e8(n0f2));
    n0fc = gl.createProgram();
    gl.attachShader(n0fc, b);
    gl.attachShader(n0fc, a);
    gl.linkProgram(n0fc);
    gl.getProgramParameter(n0fc, gl.LINK_STATUS) || alert("Could not initialise shaders");
    gl.useProgram(n0fc);
    n0fc.n101 = gl.getAttribLocation(n0fc, "aVertexPosition");
    gl.enableVertexAttribArray(n0fc.n101);
    n0fc.n102 = gl.getAttribLocation(n0fc, "aVertexColor");
    gl.enableVertexAttribArray(n0fc.n102);
    n0fc.n103 = gl.getAttribLocation(n0fc, "aVertexNormal");
    gl.enableVertexAttribArray(n0fc.n103);
    n0fc.n104 = gl.getUniformLocation(n0fc, "uPMatrix");
    n0fc.n105 = gl.getUniformLocation(n0fc, "uMVMatrix");
    n0fc.n107 = gl.getUniformLocation(n0fc, "uNMatrix");
    n0fc.n108 = gl.getUniformLocation(n0fc, "uAmbientColor");
    n0fc.n109 = gl.getUniformLocation(n0fc, "uDirectionalColor");
    n0fc.n10a = gl.getUniformLocation(n0fc, "uLightDirection");
    n0fc.n111 = gl.getUniformLocation(n0fc, "uUseLighting")
}
function n112()
{
    gl.uniformMatrix4fv(n0fc.n104, false, new WebGLFloatArray(View.pMatrix));
    gl.uniformMatrix4fv(n0fc.n105, false, new WebGLFloatArray(View.n106));
    View.nMatrix = n0f7.n0e4(View.n106);
    View.nMatrix = n0f7.n0fd(View.nMatrix);
    gl.uniformMatrix4fv(n0fc.n107, false, new WebGLFloatArray(View.nMatrix))
}
function n152(a)
{
    gl.deleteBuffer(a)
}
function n077(a, b, c, d, f)
{
    var h = gl.createBuffer();
    gl.bindBuffer(b, h);
    if (c == "float") {
        gl.bufferData(b, new WebGLFloatArray(a), gl.STATIC_DRAW);
    }
    else {
        c == "ushort" && gl.bufferData(b, new WebGLUnsignedShortArray(a), gl.STATIC_DRAW);
    }
    h.itemSize = d;
    h.numItems = f;
    return h
}
function n0a8(a, b, c, d, f)
{
    gl.bindBuffer(gl.ARRAY_BUFFER, a);
    gl.vertexAttribPointer(n0fc.n101, a.itemSize, gl.FLOAT, false, 0, 0);
    if (c != null)
    {
        gl.bindBuffer(gl.ARRAY_BUFFER, c);
        gl.vertexAttribPointer(n0fc.n102, c.itemSize, gl.FLOAT, false, 0, 0)
    }
    if (b)
    {
        gl.bindBuffer(gl.ARRAY_BUFFER, b);
        gl.vertexAttribPointer(n0fc.n103, b.itemSize, gl.FLOAT, false, 0, 0)
    }
    n112();
    if (d == null) {
        gl.drawArrays(f, 0, a.numItems);
    }
    else
    {
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, d);
        gl.drawElements(f, d.numItems, gl.UNSIGNED_SHORT, 0)
    }
}
Op = function (a)
{
    this.type = a;
};
Op.n155 = 0;
Op.MODIFY = 1;
Op.n114 = 2;
Op.n115 = 3;
Op.n116 = 4;
Op.n117 = 5;
Op.n118 = 6;
Op.n119 = 7;
Op.n11a = 8;
Op.n116_VTX = 9;
Op.create = function (a, b)
{
    var c = new Op(Op.n155);
    c.subject = a;
    c.xform = b;
    return c;
};
Op.modify = function (a, b)
{
    var c = new Op(Op.MODIFY);
    c.subject = a;
    c.xform = b;
    return c;
};
Op.n125 = function (a, b, c)
{
    var d = new Op(Op.n114);
    d.subject = a;
    d.detail = b;
    d.xform = c;
    return d;
};
Op.n126 = function (a, b, c)
{
    var d = new Op(Op.n115);
    d.subject = a;
    d.detail = b;
    d.xform = c;
    return d;
};
Op.n127 = function (a, b, c)
{
    var d = new Op(Op.n116);
    d.subject = a;
    d.detail = b;
    d.xform = c;
    return d;
};
Op.n127vtx = function (a, b, c)
{
    var d = new Op(Op.n116_VTX);
    d.subject = a;
    d.detail = b;
    d.xform = c;
    return d;
};
Op.n128 = function (a, b, c)
{
    var d = new Op(Op.n117);
    d.subject = a;
    d.detail = b;
    d.xform = c;
    return d;
};
Op.n129 = function (a)
{
    var b = new Op(Op.n118);
    b.subject = a;
    return b;
};
Op.n12a = function (a, b, c)
{
    var d = new Op(Op.n11a);
    d.subject = a;
    d.detail = {
        color : b, oldcolor : c
    };
    return d;
};
Op.n12b = function (a, b, c, d)
{
    var f = new Op(Op.n119);
    f.subject = a;
    f.detail = {
        face : b, color : c, oldcolor : d
    };
    return f;
};
n0e5 = null;
n0e6 = 
{
    points : [1, 1, 0, 0.9807852804032304, 1, 0.19509032201612825, 0.9238795325112867, 1, 0.3826834323650898, 
    0.8314696123025452, 1, 0.5555702330196022, 0.7071067811865476, 1, 0.7071067811865475, 0.5555702330196023, 
    1, 0.8314696123025452, 0.38268343236508984, 1, 0.9238795325112867, 0.19509032201612833, 1, 0.9807852804032304, 
    6.123233995736766E - 17, 1, 1, - 0.1950903220161282, 1, 0.9807852804032304, - 0.3826834323650897, 
    1, 0.9238795325112867, - 0.555570233019602, 1, 0.8314696123025455, - 0.7071067811865475, 1, 0.7071067811865476, 
     - 0.8314696123025453, 1, 0.5555702330196022, - 0.9238795325112867, 1, 0.3826834323650899, - 0.9807852804032304, 
    1, 0.1950903220161286, - 1, 1, 1.2246467991473532E - 16, - 0.9807852804032304, 1, - 0.19509032201612836, 
     - 0.9238795325112868, 1, - 0.38268343236508967, - 0.8314696123025455, 1, - 0.555570233019602, - 0.7071067811865477, 
    1, - 0.7071067811865475, - 0.5555702330196022, 1, - 0.8314696123025452, - 0.38268343236509034, 1, 
     - 0.9238795325112865, - 0.19509032201612866, 1, - 0.9807852804032303, - 1.8369701987210297E - 16, 
    1, - 1, 0.1950903220161283, 1, - 0.9807852804032304, 0.38268343236509, 1, - 0.9238795325112866, 0.5555702330196018, 
    1, - 0.8314696123025455, 0.7071067811865474, 1, - 0.7071067811865477, 0.8314696123025452, 1, - 0.5555702330196022, 
    0.9238795325112865, 1, - 0.3826834323650904, 0.9807852804032303, 1, - 0.19509032201612872, 1, - 1, 
    0, 0.9807852804032304, - 1, 0.19509032201612825, 0.9238795325112867, - 1, 0.3826834323650898, 0.8314696123025452, 
     - 1, 0.5555702330196022, 0.7071067811865476, - 1, 0.7071067811865475, 0.5555702330196023, - 1, 0.8314696123025452, 
    0.38268343236508984, - 1, 0.9238795325112867, 0.19509032201612833, - 1, 0.9807852804032304, 6.123233995736766E - 17, 
     - 1, 1, - 0.1950903220161282, - 1, 0.9807852804032304, - 0.3826834323650897, - 1, 0.9238795325112867, 
     - 0.555570233019602, - 1, 0.8314696123025455, - 0.7071067811865475, - 1, 0.7071067811865476, - 0.8314696123025453, 
     - 1, 0.5555702330196022, - 0.9238795325112867, - 1, 0.3826834323650899, - 0.9807852804032304, - 1, 
    0.1950903220161286, - 1, - 1, 1.2246467991473532E - 16, - 0.9807852804032304, - 1, - 0.19509032201612836, 
     - 0.9238795325112868, - 1, - 0.38268343236508967, - 0.8314696123025455, - 1, - 0.555570233019602, 
     - 0.7071067811865477, - 1, - 0.7071067811865475, - 0.5555702330196022, - 1, - 0.8314696123025452, 
     - 0.38268343236509034, - 1, - 0.9238795325112865, - 0.19509032201612866, - 1, - 0.9807852804032303, 
     - 1.8369701987210297E - 16, - 1, - 1, 0.1950903220161283, - 1, - 0.9807852804032304, 0.38268343236509, 
     - 1, - 0.9238795325112866, 0.5555702330196018, - 1, - 0.8314696123025455, 0.7071067811865474, - 1, 
     - 0.7071067811865477, 0.8314696123025452, - 1, - 0.5555702330196022, 0.9238795325112865, - 1, - 0.3826834323650904, 
    0.9807852804032303, - 1, - 0.19509032201612872], edges : [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 
    7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 
    20, 21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 0, 32, 
    33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 40, 40, 41, 41, 42, 42, 43, 43, 44, 44, 45, 
    45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 55, 56, 56, 57, 57, 
    58, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63, 32, 0, 32, 1, 33, 2, 34, 3, 35, 4, 36, 5, 37, 6, 38, 
    7, 39, 8, 40, 9, 41, 10, 42, 11, 43, 12, 44, 13, 45, 14, 46, 15, 47, 16, 48, 17, 49, 18, 50, 19, 51, 
    20, 52, 21, 53, 22, 54, 23, 55, 24, 56, 25, 57, 26, 58, 27, 59, 28, 60, 29, 61, 30, 62, 31, 63], faces : [[31, 
    30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 
    4, 3, 2, 1, 0], [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 
    53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], [0, 1, 33, 32], [1, 2, 34, 33], [2, 3, 35, 34], [3, 4, 
    36, 35], [4, 5, 37, 36], [5, 6, 38, 37], [6, 7, 39, 38], [7, 8, 40, 39], [8, 9, 41, 40], [9, 10, 42, 
    41], [10, 11, 43, 42], [11, 12, 44, 43], [12, 13, 45, 44], [13, 14, 46, 45], [14, 15, 47, 46], [15, 
    16, 48, 47], [16, 17, 49, 48], [17, 18, 50, 49], [18, 19, 51, 50], [19, 20, 52, 51], [20, 21, 53, 
    52], [21, 22, 54, 53], [22, 23, 55, 54], [23, 24, 56, 55], [24, 25, 57, 56], [25, 26, 58, 57], [26, 
    27, 59, 58], [27, 28, 60, 59], [28, 29, 61, 60], [29, 30, 62, 61], [30, 31, 63, 62], [31, 0, 32, 63]]
};
n0e7 = 
{
    points : [0, 1.5, 0, 0.9807852804032304, 0, 0.19509032201612825, 0.9238795325112867, 0, 0.3826834323650898, 
    0.8314696123025452, 0, 0.5555702330196022, 0.7071067811865476, 0, 0.7071067811865475, 0.5555702330196023, 
    0, 0.8314696123025452, 0.38268343236508984, 0, 0.9238795325112867, 0.19509032201612833, 0, 0.9807852804032304, 
    6.123233995736766E - 17, 0, 1, - 0.1950903220161282, 0, 0.9807852804032304, - 0.3826834323650897, 
    0, 0.9238795325112867, - 0.555570233019602, 0, 0.8314696123025455, - 0.7071067811865475, 0, 0.7071067811865476, 
     - 0.8314696123025453, 0, 0.5555702330196022, - 0.9238795325112867, 0, 0.3826834323650899, - 0.9807852804032304, 
    0, 0.1950903220161286, - 1, 0, 1.2246467991473532E - 16, - 0.9807852804032304, 0, - 0.19509032201612836, 
     - 0.9238795325112868, 0, - 0.38268343236508967, - 0.8314696123025455, 0, - 0.555570233019602, - 0.7071067811865477, 
    0, - 0.7071067811865475, - 0.5555702330196022, 0, - 0.8314696123025452, - 0.38268343236509034, 0, 
     - 0.9238795325112865, - 0.19509032201612866, 0, - 0.9807852804032303, - 1.8369701987210297E - 16, 
    0, - 1, 0.1950903220161283, 0, - 0.9807852804032304, 0.38268343236509, 0, - 0.9238795325112866, 0.5555702330196018, 
    0, - 0.8314696123025455, 0.7071067811865474, 0, - 0.7071067811865477, 0.8314696123025452, 0, - 0.5555702330196022, 
    0.9238795325112865, 0, - 0.3826834323650904, 0.9807852804032303, 0, - 0.19509032201612872, 1, 0, - 2.4492935982947064E - 16], 
    edges : [0, 1, 1, 2, 0, 2, 2, 3, 0, 3, 3, 4, 0, 4, 4, 5, 0, 5, 5, 6, 0, 6, 6, 7, 0, 7, 7, 8, 0, 8, 
    8, 9, 0, 9, 9, 10, 0, 10, 10, 11, 0, 11, 11, 12, 0, 12, 12, 13, 0, 13, 13, 14, 0, 14, 14, 15, 0, 15, 
    15, 16, 0, 16, 16, 17, 0, 17, 17, 18, 0, 18, 18, 19, 0, 19, 19, 20, 0, 20, 20, 21, 0, 21, 21, 22, 
    0, 22, 22, 23, 0, 23, 23, 24, 0, 24, 24, 25, 0, 25, 25, 26, 0, 26, 26, 27, 0, 27, 27, 28, 0, 28, 28, 
    29, 0, 29, 29, 30, 0, 30, 30, 31, 0, 31, 31, 32, 0, 32, 32, 1], faces : [[0, 2, 1], [0, 3, 2], [0, 
    4, 3], [0, 5, 4], [0, 6, 5], [0, 7, 6], [0, 8, 7], [0, 9, 8], [0, 10, 9], [0, 11, 10], [0, 12, 11], 
    [0, 13, 12], [0, 14, 13], [0, 15, 14], [0, 16, 15], [0, 17, 16], [0, 18, 17], [0, 19, 18], [0, 20, 
    19], [0, 21, 20], [0, 22, 21], [0, 23, 22], [0, 24, 23], [0, 25, 24], [0, 26, 25], [0, 27, 26], [0, 
    28, 27], [0, 29, 28], [0, 30, 29], [0, 31, 30], [0, 32, 31], [0, 1, 32], [1, 2, 3, 4, 5, 6, 7, 8, 
    9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]]
};
function n0c5(a, b)
{
    for (var c = 2 * Math.PI, d = [], f = [[]], h = [], i = 0; i < b; i++)
    {
        d.push(a * Math.cos(c * (i / b)), a * Math.sin(c * (i / b)), 0);
        h.push(i, i + 1 == b ? 0 : i + 1);
        f[0].push(i)
    }
    return {
        points : d, edges : h, faces : f
    }
}
function n0ca(a, b, c)
{
    for (var d = 0; d < c; d++)
    {
        for (var f = [], h = [], i = 0; i < b.length; i++)
        {
            var j = b[i][0], k = b[i][1], l = b[i][2], n = [a[3 * j], a[3 * j + 1], a[3 * j + 2]], p = [a[3 * k], 
            a[3 * k + 1], a[3 * k + 2]], o = [a[3 * l], a[3 * l + 1], a[3 * l + 2]], r = V3.$((n[0] + p[0]) / 2, 
            (n[1] + p[1]) / 2, (n[2] + p[2]) / 2);
            p = V3.$((p[0] + o[0]) / 2, (p[1] + o[1]) / 2, (p[2] + o[2]) / 2);
            n = V3.$((o[0] + n[0]) / 2, (o[1] + n[1]) / 2, (o[2] + n[2]) / 2);
            r = V3.normalize(r);
            p = V3.normalize(p);
            n = V3.normalize(n);
            o = a.length / 3;
            var m = o + 1, q = o + 2;
            a.push(r[0], r[1], r[2], p[0], p[1], p[2], n[0], n[1], n[2]);
            f.push([j, o, q]);
            f.push([k, m, o]);
            f.push([l, q, m]);
            f.push([o, m, q]);
            if (d == c - 1) {
                h.push(j, o, o, q, q, j);
                h.push(k, o, o, m, m, k);
                h.push(l, m, m, q, q, l)
            }
        }
        b = f
    }
    return [a, f, h]
}
function n0c8()
{
    var a = n0ca([ - 0.5257311121191336, 0, 0.8506508083520399, 0.5257311121191336, 0, 0.8506508083520399, 
    0, 0.8506508083520399, 0.5257311121191336, 0, 0.8506508083520399, - 0.5257311121191336, 0.8506508083520399, 
    0.5257311121191336, 0, - 0.8506508083520399, 0.5257311121191336, 0, - 0.5257311121191336, 0, - 0.8506508083520399, 
    0.5257311121191336, 0, - 0.8506508083520399, 0, - 0.8506508083520399, 0.5257311121191336, 0, - 0.8506508083520399, 
     - 0.5257311121191336, 0.8506508083520399, - 0.5257311121191336, 0, - 0.8506508083520399, - 0.5257311121191336, 
    0], [[0, 1, 2], [1, 0, 8], [7, 6, 3], [6, 7, 9], [4, 3, 2], [2, 3, 5], [8, 9, 10], [11, 9, 8], [4, 
    10, 7], [1, 10, 4], [5, 11, 0], [6, 11, 5], [1, 4, 2], [4, 7, 3], [8, 10, 1], [10, 9, 7], [5, 3, 6], 
    [6, 9, 11], [8, 0, 11], [2, 5, 0]], 3);
    n0e5 = {};
    n0e5.points = a[0];
    n0e5.faces = a[1];
    n0e5.edges = a[2]
}
n0d7 = function (a, b, c)
{
    this.changeType = a;
    this.subjectType = b;
    this.g = c;
};
n0d7.n11b = 1;
n0d7.n11c = 2;
n0d7.n11d = 3;
n0d7.n11e = 4;
n0d7.getDelta = function (a, b, c, d, f)
{
    b = View.n0cc(n05e(b, c, d, f, View.project(a)));
    return [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
};
n0d7.prototype = 
{
    changeType :- 1, subjectType :- 1, delta : null, isEmpty : true, g : null,
    start : function (a)
    {
        if (a) {
            this.x0 = a.clientX;
            this.y0 = canvas.height - a.clientY
        }
        switch (this.changeType)
        {
            case n13e:
                if (this.subjectType == n0d7.n11b) {
                    this.g.n0bf = {
                        translation : [0, 0, 0] 
                    };
                }
                this.n134 = 0.05;
                break;
            case n13c:
                if (this.subjectType == n0d7.n11b) {
                    this.g.n0be = {
                        scale : [1, 1, 1] 
                    };
                }
                this.n134 = 0.05;
                break;
            case n13d:
                if (this.subjectType == n0d7.n11b) {
                    this.g.n0c0 = {
                        rotation : {
                            axis : this.n0f9, angle : 0 
                        }
                    };
                }
                this.n134 = 0.5;
                break;
            case ACTION_EXTRUDE:
                this.detail = this.g.n078();
                this.g.n084();
                this.n134 = 0.05;
                break
        }
    },
    n0fa : function (a)
    {
        this.n0f9 = a;
    },
    n0fb : function ()
    {
        return this.n0f9;
    },
    getStep : function (a, b)
    {
        var c = a - this.x0;
        if (c) {
            c /= Math.abs(c);
        }
        var d = Math.sqrt((a - this.x0) * (a - this.x0) + (b - this.y0) * (b - this.y0));
        this.x0 = a;
        this.y0 = b;
        return c * d * this.n134;
    },
    n0d8 : function (a)
    {
        switch (this.changeType)
        {
            case n13e:
                this.by([0.1 * a[0], 0.1 * a[1], 0.1 * a[2]]);
                break;
            case n13c:
                this.by([0.1 * a[0], 0.1 * a[1], 0.1 * a[2]]);
                break;
            case n13d:
                this.by(1);
                break
        }
    },
    by : function (a)
    {
        switch (this.changeType)
        {
            case n13e:
                View.cpanel.change(a);
                switch (this.subjectType)
                {
                    case n0d7.n11b:
                        this.g.moveBy(a);
                        break;
                    case n0d7.n11c:
                        this.g.n0b4By(a);
                        this.g.n06f();
                        break;
                    case n0d7.n11d:
                        this.g.n0b3By(a);
                        this.g.n06f();
                        break;
                    case n0d7.n11e:
                        this.g.n0b5By(a);
                        this.g.n06f();
                        break
                }
                break;
            case n13c:
                View.cpanel.change(a);
                switch (this.subjectType)
                {
                    case n0d7.n11b:
                        this.g.scaleBy(a);
                        break;
                    case n0d7.n11c:
                        a = this.g.n121(a);
                        this.g.n0b4By(a);
                        this.g.n06f();
                        break;
                    case n0d7.n11d:
                        a = this.g.n122(a);
                        this.g.n0b3By(a);
                        this.g.n06f();
                        break;
                    case n0d7.n11e:
                        throw "invalid";
                }
                break;
            case n13d:
                View.cpanel.change(this.n0f9, a);
                switch (this.subjectType)
                {
                    case n0d7.n11b:
                        this.g.rotateBy(a);
                        break;
                    case n0d7.n11c:
                        a = this.g.n0ff(a, this.n0f9);
                        this.g.n0b4By(a);
                        this.g.n06f();
                        break;
                    case n0d7.n11d:
                        throw "TODO";
                    case n0d7.n11e:
                        throw "invalid";
                }
                break;
            case ACTION_EXTRUDE:
                a = this.g.n09c(a);
                this.g.n06f();
                break
        }
        if (typeof a == "number") {
            if (!this.delta) {
                this.delta = 0;
            }
            this.delta += a
        }
        else if (typeof a[0] == "number")
        {
            if (!this.delta) {
                this.delta = [0, 0, 0];
            }
            this.delta[0] += a[0];
            this.delta[1] += a[1];
            this.delta[2] += a[2]
        }
        else
        {
            if (!this.delta) {
                this.delta = [];
                for (var b = a.length, c = 0; c < b; c++) {
                    this.delta[c] = [0, 0, 0];
                }
            }
            b = a.length;
            for (c = 0; c < b; c++) {
                this.delta[c][0] += a[c][0];
                this.delta[c][1] += a[c][1];
                this.delta[c][2] += a[c][2]
            }
        }
        this.isEmpty = false;
    },
    to : function (a, b, c, d)
    {
        var f;
        switch (this.changeType)
        {
            case n13e:
                switch (this.subjectType)
                {
                    case n0d7.n11b:
                        f = this.g.n0b8();
                        break;
                    case n0d7.n11c:
                        f = this.g.n0b2(this.g.n053);
                        break;
                    case n0d7.n11d:
                        f = this.g.n0b1(this.g.n056);
                        break;
                    case n0d7.n11e:
                        f = this.g.n0ad(null, this.g.n057);
                        break
                }
                View.save();
                this.g.transform();
                a = n0d7.getDelta(f, a, b, c, d);
                View.restore();
                this.by(a);
                break
        }
    },
    save : function ()
    {
        if (!this.isEmpty)
        {
            switch (this.changeType)
            {
                case n13e:
                    switch (this.subjectType)
                    {
                        case n0d7.n11b:
                            var a = Op.modify(this.g, {
                                translation : this.delta.slice(0)
                            });
                            break;
                        case n0d7.n11c:
                            a = Op.n127(this.g, this.g.n053, this.delta.slice(0));
                            break;
                        case n0d7.n11d:
                            a = Op.n126(this.g, this.g.n056, this.delta.slice(0));
                            break;
                        case n0d7.n11e:
                            a = Op.n125(this.g, this.g.n057, this.delta.slice(0));
                            break
                    }
                    break;
                case n13c:
                    switch (this.subjectType)
                    {
                        case n0d7.n11b:
                            a = Op.modify(this.g, {
                                scale : this.delta.slice(0)
                            });
                            break;
                        case n0d7.n11c:
                            a = Op.n127(this.g, this.g.n053, this.delta.slice(0));
                            break;
                        case n0d7.n11d:
                            a = Op.n126(this.g, this.g.n056, this.delta.slice(0));
                            break;
                        case n0d7.n11e:
                            break
                    }
                    break;
                case n13d:
                    switch (this.subjectType)
                    {
                        case n0d7.n11b:
                            a = Op.modify(this.g, {
                                rotation : {
                                    axis : this.n0f9.slice(0), angle : this.delta
                                }
                            });
                            break;
                        case n0d7.n11c:
                            a = Op.n127(this.g, this.g.n053, this.delta.slice(0));
                            break;
                        case n0d7.n11d:
                            break;
                        case n0d7.n11e:
                            break
                    }
                    break;
                case ACTION_EXTRUDE:
                    a = Op.n128(this.g, this.g.n053, null);
                    a.detail = this.detail;
                    a.xform = this.delta;
                    break
            }
            View.n0a1.do_(a);
            this.delta = null;
        }
    }
};
var n160 = 1E4;
function n052() {}
n052.NONE =- 1;
n052.n13b = 1001;
n052.n12e = 10;
n052.n12f = 11;
n052.n130 = 12;
n052.n131 = 13;
n052.TRIANGLE = 0;
n052.n132 = 1;
n052.n133 = 2;
var n058 = 0, n059 = 1, n05a = 1, n05b = 1, n05c = 1;
n052.prototype = 
{
    mode : n058, geometryColor : [0.8, 0.8, 0.8, 1], n0a6 : false, n053 :- 1, n054 :- 1, load : function (a, 
    b, c, d, f, h, i, j, k, l)
    {
        this.name = a;
        this.vertices = b;
        this.edges = d;
        this.faces = f;
        if (h) {
            this.geometryColor = h;
        }
        this.faceColors = i;
        this.transforms = j;
        if (k) {
            this.mode = k;
        }
        this.stdtype = l;
    },
    n0a7 : function (a)
    {
        if (a)
        {
            var b = [], c = [];
            for (a = 0; a < this.faces.length; a++)
            {
                for (var d = this.faces[a], f = [], h = 0; h < d.length; h++)
                {
                    f.push(b.length / 3);
                    b.push(this.vertices[3 * d[h]]);
                    b.push(this.vertices[3 * d[h] + 1]);
                    b.push(this.vertices[3 * d[h] + 2])
                }
                c.push(f)
            }
            f = n077(b, gl.ARRAY_BUFFER, "float", 3, b.length / 3);
            var i = [];
            for (a = 0; a < c.length; a++) {
                for (h = 0; h < c[a].length - 2; h++) {
                    i.push(c[a][0], c[a][h + 1], c[a][h + 2]);
                }
            }
            i = n077(i, gl.ELEMENT_ARRAY_BUFFER, "ushort", 1, i.length);
            d = [];
            for (a = 0; a < c.length; a++)
            {
                var j = this.n0ad(c[a][0], b);
                h = this.n0ad(c[a][1], b);
                var k = this.n0ad(c[a][2], b);
                j = V3.sub(h, j);
                h = V3.sub(k, h);
                k = V3.normalize(V3.cross(j, h));
                for (h = 0; h < c[a].length; h++) {
                    d.push(k[0], k[1], k[2]);
                }
            }
            c = n077(d, gl.ARRAY_BUFFER, "float", 3, d.length / 3);
            k = [];
            if (this.faceColors)
            {
                for (a = 0; a < this.faces.length; a++) 
                {
                    d = this.faces[a];
                    b = d.length;
                    if (this.faceColors[a]) {
                        for (h = 0; h < b; h++) {
                            k = k.concat(this.faceColors[a]);
                        }
                    }
                    else {
                        for (h = 0; h < b; h++) {
                            k = k.concat(this.geometryColor) ;
                        }
                    }
                }
            }
            else {
                for (a = 0; a < b.length; a += 3) {
                    k = k.concat(this.geometryColor);
                }
            }
            a = n077(k, gl.ARRAY_BUFFER, "float", 4, k.length)
        }
        else
        {
            f = n077(this.vertices, gl.ARRAY_BUFFER, "float", 3, this.vertices.length / 3);
            i = n077(this.edges, gl.ELEMENT_ARRAY_BUFFER, "ushort", 1, this.edges.length);
            b = [];
            for (a = 0; a < this.edges.length; a++) {
                b.push(0, 0, 1);
            }
            c = n077(b, gl.ARRAY_BUFFER, "float", 3, b.length / 3);
            k = [];
            for (a = 0; a < this.vertices.length; a += 3) {
                k = k.concat([0, 0, 0, 1]);
            }
            a = n077(k, gl.ARRAY_BUFFER, "float", 4, k.length)
        }
        return {
            vtx : f, idx : i, nrm : c, col : a
        }
    },
    n151 : function ()
    {
        if (this.buffer)
        {
            n152(this.buffer.vtx);
            n152(this.buffer.idx);
            n152(this.buffer.nrm);
            n152(this.buffer.col)
        }
        if (this.expbuffer)
        {
            n152(this.expbuffer.vtx);
            n152(this.expbuffer.idx);
            n152(this.expbuffer.nrm);
            n152(this.expbuffer.col)
        }
    },
    n06f : function ()
    {
        this.n151();
        this.buffer = this.n0a7(false);
        this.expbuffer = this.n0a7(true);
    },
    draw : function ()
    {
        View.save();
        this.transform();
        if (this.mode == n058)
        {
            gl.lineWidth(1);
            n0a8(this.buffer.vtx, this.buffer.nrm, this.buffer.col, this.buffer.idx, gl.LINES);
            if (tool == n13f || tool == TOOL_RULER) {
                this.n0a9();
            }
        }
        else
        {
            this.mode == n059 && n0a8(this.expbuffer.vtx, this.expbuffer.nrm, this.expbuffer.col, this.expbuffer.idx, 
            gl.TRIANGLES);
        }
        View.restore()
    },
    n0a9 : function ()
    {
        if (this.n057 >= 0)
        {
            var a = this.n0ad(this.n057);
            if (this.n0aa) {
                this.n0aa.n0ac([ {
                    translation : a 
                },
                {
                    scale : [0.05, 0.05, 0.05] 
                }]);
            }
            else {
                this.n0aa = n052.n0c4([ {
                    translation : a
                },
                {
                    scale : [0.05, 0.05, 0.05]
                }]);
                this.n0aa.n06f()
            }
            this.n0aa.draw()
        }
        else if (this.n056 >= 0)
        {
            a = this.n0ad(this.edges[2 * this.n056]);
            var b = this.n0ad(this.edges[2 * this.n056 + 1]);
            if (this.n055)
            {
                this.n055[0].n0ac([ {
                    translation : a
                },
                {
                    scale : [0.05, 0.05, 0.05]
                }]);
                this.n055[1].n0ac([ {
                    translation : b
                },
                {
                    scale : [0.05, 0.05, 0.05]
                }])
            }
            else
            {
                this.n055 = [];
                this.n055[0] = n052.n0c4([ {
                    translation : a
                },
                {
                    scale : [0.05, 0.05, 0.05]
                }]);
                this.n055[0].n06f();
                this.n055[1] = n052.n0c4([ {
                    translation : b
                },
                {
                    scale : [0.05, 0.05, 0.05]
                }]);
                this.n055[1].n06f()
            }
            this.n055[0].draw();
            this.n055[1].draw()
        }
        else if (this.n053 >= 0)
        {
            a = [];
            for (b = 0; b < 4; b++) {
                a.push(this.n0ad(this.faces[this.n053][b]));
            }
            if (this.n053n14cs)
            {
                for (b = 0; b < 4; b++) {
                    this.n053n14cs[b].n0ac([ {
                        translation : a[b] 
                    },
                    {
                        scale : [0.05, 0.05, 0.05] 
                    }]);
                }
            }
            else
            {
                this.n053n14cs = [];
                for (b = 0; b < 4; b++)
                {
                    this.n053n14cs[b] = n052.n0c4([ {
                        translation : a[b]
                    },
                    {
                        scale : [0.05, 0.05, 0.05]
                    }]);
                    this.n053n14cs[b].n06f()
                }
            }
            for (b = 0; b < 4; b++) {
                this.n053n14cs[b].draw();
            }
        }
    },
    n0aa : null, n055 : null, transforms : [],
    transform : function ()
    {
        for (var a = 0; a < this.transforms.length; a++)
        {
            var b = this.transforms[a];
            if (b.translation) {
                View.translate(b.translation);
            }
            else if (b.scale) {
                View.scale(b.scale);
            }
            else {
                b.rotation && View.rotate(b.rotation.angle, b.rotation.axis);
            }
        }
    },
    n09d : function ()
    {
        for (var a = 0; a < this.transforms.length; a++)
        {
            var b = this.transforms[a];
            if (b.translation) {
                b.translation = new Array(b.translation[0], b.translation[1], b.translation[2]);
            }
            else if (b.scale) {
                b.scale = new Array(b.scale[0], b.scale[1], b.scale[2]);
            }
            else if (b.rotation)
            {
                b.rotation.axis = new Array(b.rotation.axis[0], b.rotation.axis[1], b.rotation.axis[2]);
            }
        }
    },
    n0ac : function (a)
    {
        this.transforms = a;
    },
    n0ad : function (a, b)
    {
        if (!b) {
            b = this.vertices;
        }
        return V3.$(b[3 * a], b[3 * a + 1], b[3 * a + 2]);
    },
    n0ae : function (a)
    {
        var b = this.n0af();
        a = V3.$(this.vertices[3 * a], this.vertices[3 * a + 1], this.vertices[3 * a + 2]);
        return n0f7.mulV3(b, a);
    },
    n0af : function ()
    {
        for (var a = n0f7.clone(n0f7.I), b = 0; b < this.transforms.length; b++)
        {
            var c = this.transforms[b];
            if (c.translation) {
                a = n0f7.translate(c.translation, a);
            }
            else if (c.scale) {
                a = n0f7.scale(c.scale, a);
            }
            else if (c.rotation) {
                a = n0f7.rotate(c.rotation.angle * Math.PI  / 180, c.rotation.axis, a);
            }
        }
        return a;
    },
    n0b0 : function (a, b)
    {
        this.vertices[3 * a] = b[0];
        this.vertices[3 * a + 1] = b[1];
        this.vertices[3 * a + 2] = b[2];
    },
    n0b1 : function (a)
    {
        var b = 0, c = 0, d = 0;
        d = this.edges[2 * a];
        a = this.edges[2 * a + 1];
        b = (this.vertices[3 * d] + this.vertices[3 * a]) / 2;
        c = (this.vertices[3 * d + 1] + this.vertices[3 * a + 1]) / 2;
        d = (this.vertices[3 * d + 2] + this.vertices[3 * a + 2]) / 2;
        return V3.$(b, c, d);
    },
    n0b2 : function (a)
    {
        for (var b = 0, c = 0, d = 0, f = 0; f < this.faces[a].length; f++)
        {
            b += this.vertices[3 * this.faces[a][f]];
            c += this.vertices[3 * this.faces[a][f] + 1];
            d += this.vertices[3 * this.faces[a][f] + 2]
        }
        a = this.faces[a].length;
        return V3.$(b / a, c / a, d / a);
    },
    n0b3 : function (a, b, c, d)
    {
        this.n124();
        View.save();
        this.transform();
        var f = this.n0b1(this.n056);
        c = n05e(a, b, c, d, View.project(f));
        c = View.n0cc(c);
        a = c[0] - f[0];
        b = c[1] - f[1];
        f = c[2] - f[2];
        c = this.edges[2 * this.n056];
        d = this.edges[2 * this.n056 + 1];
        var h = this.n0ad(c);
        this.n0b0(c, V3.$(h[0] + a, h[1] + b, h[2] + f));
        h = this.n0ad(d);
        this.n0b0(d, V3.$(h[0] + a, h[1] + b, h[2] + f));
        View.restore();
        this.n06f()
    },
    n124 : function ()
    {
        if (this.stdtype != n052.n13b)
        {
            this.stdtype = n052.n13b;
            this.vertices = this.vertices.slice(0);
            this.edges = this.edges.slice(0);
            this.faces = this.faces.slice(0);
        }
    },
    n09c : function (a)
    {
        this.n124();
        var b = this.faces[this.n053], c = this.n0ad(b[0]), d = this.n0ad(b[1]), f = this.n0ad(b[2]);
        c = V3.sub(d, c);
        d = V3.sub(f, d);
        a = V3.mul(V3.normalize(V3.cross(c, d)), a);
        for (d = 0; d < b.length; d++)
        {
            c = b[d];
            f = this.n0ad(c);
            if (this.n082(c)) {
                var h = this.mirror.project(a);
                this.n0b0(c, [f[0] + h[0], f[1] + h[1], f[2] + h[2]])
            }
            else {
                this.n0b0(c, V3.add(f, a));
            }
            if (this.mirror)
            {
                c = this.n10b[c];
                if (c >= 0) {
                    f = this.n0ad(c);
                    h = this.mirror.n085(a);
                    this.n0b0(c, [f[0] + h[0], f[1] + h[1], f[2] + h[2]])
                }
            }
        }
        return a;
    },
    n0b4To : function (a, b, c, d)
    {
        this.n124();
        View.save();
        this.transform();
        var f = this.n0b2(this.n053);
        c = n05e(a, b, c, d, View.project(f));
        c = View.n0cc(c);
        a = c[0] - f[0];
        b = c[1] - f[1];
        f = c[2] - f[2];
        for (c = 0; c < this.faces[this.n053].length; c++)
        {
            d = this.faces[this.n053][c];
            var h = this.n0ad(d);
            this.n0b0(d, V3.$(h[0] + a, h[1] + b, h[2] + f))
        }
        View.restore();
        this.n06f();
        return V3.$(a, b, f);
    },
    n0b5 : function (a, b, c, d)
    {
        this.n124();
        View.save();
        this.transform();
        var f = this.n0ad(this.n057);
        f = n05e(a, b, c, d, View.project(f));
        f = View.n0cc(f);
        this.n0b0(this.n057, f);
        View.restore();
        this.n06f()
    },
    n0b7 : function ()
    {
        View.save();
        this.transform();
        var a = View.project(this.n0b8());
        a[2] = 1;
        a = View.n0cc(a);
        View.restore();
        return V3.normalize(a);
    },
    n0b8 : function ()
    {
        for (var a = 0, b = 0, c = 0, d = 0; d < this.vertices.length; d += 3) {
            a += this.vertices[d];
            b += this.vertices[d + 1];
            c += this.vertices[d + 2]
        }
        d = this.vertices.length / 3;
        return V3.$(a / d, b / d, c / d);
    },
    n0b9 : function ()
    {
        return n0f7.mulV3(this.n0af(), this.n0b8());
    },
    n0b82D : function ()
    {
        View.save();
        this.transform();
        var a = View.project(this.n0b8());
        a = n063(a[0], a[1], a[2]);
        View.restore();
        return a;
    },
    n0ba : function ()
    {
        for (var a = [1, 1, 1], b = 0; b < this.transforms.length; b++)
        {
            if (this.transforms[b].scale) {
                var c = this.transforms[b].scale;
                a[0] *= c[0];
                a[1] *= c[1];
                a[2] *= c[2] 
            }
            return a;
        }
    },
    n0bb : function ()
    {
        for (var a = null, b = this.transforms.length - 1; b >= 0; b--)
        {
            var c = this.transforms[b].rotation;
            if (c)
            {
                a = a ? n0f8.mul(a, n0f8.$(c.axis, c.angle * Math.PI  / 180)) : n0f8.$(c.axis, c.angle * Math.PI  / 180);
            }
        }
        if (a) {
            a = n0f8.toEuler(a);
            b = 180 / Math.PI;
            return [a[0] * b, a[1] * b, a[2] * b]
        }
        else {
            return [0, 0, 0];
        }
    },
    n0bf : null,
    moveBy : function (a)
    {
        var b = this.n0bf.translation;
        this.n0bf.translation = [b[0] + a[0], b[1] + a[1], b[2] + a[2]];
        this.transforms.indexOf(this.n0bf) < 0 && this.transforms.push(this.n0bf)
    },
    n0b4By : function (a)
    {
        this.n124();
        if (typeof a[0] == "number")
        {
            for (var b = this.faces[this.n053], c = b.length, d = 0; d < c; d++) 
            {
                var f = b[d], h = this.n0ad(f);
                if (this.n082(f)) {
                    var i = this.mirror.project(a);
                    this.n0b0(f, [h[0] + i[0], h[1] + i[1], h[2] + i[2]]) 
                }
                else {
                    this.n0b0(f, [h[0] + a[0], h[1] + a[1], h[2] + a[2]]);
                }
                if (this.mirror) 
                {
                    f = this.n10b[f];
                    if (f >= 0) 
                    {
                        h = this.n0ad(f);
                        i = this.mirror.n085(a);
                        this.n0b0(f, [h[0] + i[0], h[1] + i[1], h[2] + i[2]]) 
                    }
                }
            }
        }
        else
        {
            b = this.faces[this.n053];
            c = b.length;
            for (d = 0; d < c; d++)
            {
                f = b[d];
                h = this.n0ad(f);
                if (this.n082(f)) {
                    i = this.mirror.project(a[d]);
                    this.n0b0(f, [h[0] + i[0], h[1] + i[1], h[2] + i[2]])
                }
                else {
                    this.n0b0(f, [h[0] + a[d][0], h[1] + a[d][1], h[2] + a[d][2]]);
                }
                if (this.mirror)
                {
                    f = this.n10b[f];
                    if (f >= 0)
                    {
                        h = this.n0ad(f);
                        i = this.mirror.n085(a[d]);
                        this.n0b0(f, [h[0] + i[0], h[1] + i[1], h[2] + i[2]])
                    }
                }
            }
        }
    },
    n082 : function (a)
    {
        return this.mirror && this.n10b[a] < 0;
    },
    n0b3By : function (a)
    {
        if (typeof a[0] == "number")
        {
            for (var b = 0; b < 2; b++) 
            {
                var c = this.edges[2 * this.n056 + b], d = this.n0ad(c);
                if (this.n082(c)) {
                    var f = this.mirror.project(a);
                    this.n0b0(c, [d[0] + f[0], d[1] + f[1], d[2] + f[2]]) 
                }
                else {
                    this.n0b0(c, [d[0] + a[0], d[1] + a[1], d[2] + a[2]]);
                }
                if (this.mirror) 
                {
                    c = this.n10b[c];
                    if (c >= 0) 
                    {
                        d = this.n0ad(c);
                        f = this.mirror.n085(a);
                        this.n0b0(c, [d[0] + f[0], d[1] + f[1], d[2] + f[2]]) 
                    }
                }
            }
        }
        else for (b = 0;
        b < 2;
        b++)
        {
            c = this.edges[2 * this.n056 + b];
            d = this.n0ad(c);
            if (this.n082(c)) {
                f = this.mirror.project(a[b]);
                this.n0b0(c, [d[0] + f[0], d[1] + f[1], d[2] + f[2]])
            }
            else {
                this.n0b0(c, [d[0] + a[b][0], d[1] + a[b][1], d[2] + a[b][2]]);
            }
            if (this.mirror)
            {
                c = this.n10b[c];
                if (c >= 0)
                {
                    d = this.n0ad(c);
                    f = this.mirror.n085(a[b]);
                    this.n0b0(c, [d[0] + f[0], d[1] + f[1], d[2] + f[2]])
                }
            }
        }
    },
    n0b5By : function (a)
    {
        var b = this.n0ad(this.n057);
        if (this.n082(this.n057)) {
            var c = this.mirror.project(a);
            this.n0b0(this.n057, [b[0] + c[0], b[1] + c[1], b[2] + c[2]])
        }
        else {
            this.n0b0(this.n057, [b[0] + a[0], b[1] + a[1], b[2] + a[2]]);
        }
        if (this.mirror)
        {
            c = this.n10b[this.n057];
            if (c >= 0) {
                b = this.n0ad(c);
                a = this.mirror.n085(a);
                this.n0b0(c, [b[0] + a[0], b[1] + a[1], b[2] + a[2]])
            }
        }
    },
    move : function (a, b, c, d)
    {
        View.save();
        this.transform();
        var f = this.n0b8();
        a = n05e(a, b, c, d, View.project(f));
        a = View.n0cc(a);
        this.n0bf.translation = V3.add(this.n0bf.translation, V3.$(a[0] - f[0], a[1] - f[1], a[2] - f[2]));
        this.transforms.indexOf(this.n0bf) < 0 && this.transforms.push(this.n0bf);
        View.restore()
    },
    n0be : null,
    scale : function (a)
    {
        this.n0be.scale = a;
        this.transforms.indexOf(this.n0be) < 0 && this.transforms.push(this.n0be)
    },
    scaleBy : function (a)
    {
        var b = this.n0be.scale;
        this.n0be.scale = [b[0] + a[0], b[1] + a[1], b[2] + a[2]];
        this.transforms.indexOf(this.n0be) < 0 && this.transforms.push(this.n0be)
    },
    n123 : function (a, b)
    {
        for (var c = a.length, d = 0, f = 0, h = 0, i = 0; i < c; i++) {
            var j = a[i];
            d += this.vertices[3 * j];
            f += this.vertices[3 * j + 1];
            h += this.vertices[3 * j + 2]
        }
        d = V3.$(d / c, f / c, h / c);
        f = [];
        for (i = 0; i < c; i++) {
            j = a[i];
            j = V3.sub(this.n0ad(j), d);
            j = V3.$(j[0] * b[0], j[1] * b[1], j[2] * b[2]);
            f.push(j)
        }
        return f;
    },
    n121 : function (a)
    {
        return this.n123(this.faces[this.n053], a);
    },
    n122 : function (a)
    {
        return this.n123([this.edges[2 * this.n056], this.edges[2 * this.n056 + 1]], a);
    },
    n100 : function (a, b, c)
    {
        if (!c) {
            throw "todo";
        }
        b = n0f8.$(c, b * (Math.PI / 180));
        b = n0f8.ton0f7(b);
        c = [];
        for (var d = a.length, f = 0; f < d; f++) {
            var h = this.n0ad(a[f]);
            c.push(V3.sub(n0f7.mulV3(b, h), h))
        }
        return c;
    },
    n0ff : function (a, b)
    {
        return this.n100(this.faces[this.n053], a, b);
    },
    n0c0 : null,
    rotate : function (a)
    {
        this.n0c0.rotation.angle = a;
        this.transforms.indexOf(this.n0c0) < 0 && this.transforms.push(this.n0c0)
    },
    rotateBy : function (a)
    {
        this.n0c0.rotation.angle += a;
        this.transforms.indexOf(this.n0c0) < 0 && this.transforms.push(this.n0c0)
    },
    n0fe : function ()
    {
        return this.n057 >= 0 ? n0d7.n11e : this.n056 >= 0 ? n0d7.n11d : this.n053 >= 0 ? n0d7.n11c :- 1;
    },
    ren0b5 : function (a)
    {
        this.vertices[3 * a] =- n160;
        this.vertices[3 * a + 1] =- n160;
        this.vertices[3 * a + 2] =- n160
    },
    defragment : function ()
    {
        for (var a = 0; a < this.vertices.length; a += 3)
        {
            if (this.vertices[a] <=- n160 && this.vertices[a + 1] <=- n160 && this.vertices[a + 2] <=- n160)
            {
                for (var b = 0; b < this.edges.length; b += 2)
                {
                    if (this.edges[b] == a  / 3 || this.edges[b + 1] == a  / 3) {
                        this.edges[b] =- 1;
                        this.edges[b + 1] =- 1 
                    }
                    var c = [];;
                }
            }
            for (a = 0; a < this.edges.length; a++) {
                this.edges[a] >= 0 && c.push(this.edges[a]);
            }
            this.edges = c;
            c = [];
            for (a = 0; a < this.vertices.length  / 3; a++)
            {
                if (!(this.vertices[3 * a] <=- n160)) 
                {
                    for (b = 0; b < this.edges.length; b++)
                    {
                        if (this.edges[b] == a) {
                            this.edges[b] = c.length  / 3;
                        }
                        for (b = 0; b < this.faces.length; b++) {
                            var d = this.faces[b];
                            if (d) {
                                for (var f = 0; f < d.length; f++) {
                                    if (d[f] == a) {
                                        d[f] = c.length  / 3 ;
                                    };
                                }
                            }
                        }
                        c.push(this.vertices[3 * a]);
                        c.push(this.vertices[3 * a + 1]);
                        c.push(this.vertices[3 * a + 2]) ;
                    }
                }
                this.vertices = c;;
            }
        }
    },
    dumpData : function () {},
    n084 : function ()
    {
        if (this.mirror)
        {
            for (var a = 0; a < this.vertices.length / 3; a++) if (this.n10b[a] == undefined)
            {
                var b = this.mirror.n085(this.n0ad(a)), c = this.vertices.length / 3;
                this.n10b[a] = c;
                this.n10b[c] = a;
                this.vertices.push(b[0]);
                this.vertices.push(b[1]);
                this.vertices.push(b[2])
            }
            for (a = 0; a < this.n10d.length; a++)
            {
                c = this.faces[this.n10d[a]];
                b = c.length;
                c = c.slice(0, b).reverse();
                for (var d = 0; d < b; d++) {
                    if (this.n10b[c[d]] > 0) {
                        c[d] = this.n10b[c[d]];
                    }
                    this.faces.push(c);
                }
            }
            for (a = 0; a < this.n10e.length; a++)
            {
                c = this.n10e[a];
                b = this.edges[2 * c];
                c = this.edges[2 * c + 1];
                d = this.n10b[b];
                var f = this.n10b[c];
                if (!(d < 0 && f < 0)) {
                    if (d >= 0) {
                        b = d;
                    }
                    if (f >= 0) {
                        c = f;
                    }
                    this.edges.push(b);
                    this.edges.push(c)
                }
            }
        }
        this.n10e = this.n10d = null;
    },
    n085 : function (a)
    {
        this.n10b = [];
        for (var b = this.vertices.length / 3, c = 0; c < b; c++)
        {
            var d = this.vertices.slice(3 * c, 3 * c + 3);
            if (a.contains(d)) {
                this.n10b[c] =- 1;
            }
            else
            {
                d = a.n085(d);
                var f = this.vertices.length / 3;
                this.n10b[c] = f;
                this.n10b[f] = c;
                this.vertices.push(d[0]);
                this.vertices.push(d[1]);
                this.vertices.push(d[2])
            }
        }
        a = this.edges.length / 2;
        for (c = 0; c < a; c++)
        {
            b = this.edges[2 * c];
            d = this.edges[2 * c + 1];
            f = this.n10b[b];
            var h = this.n10b[d];
            if (!(f < 0 && h < 0)) {
                if (f >= 0) {
                    b = f;
                }
                if (h >= 0) {
                    d = h;
                }
                this.edges.push(b);
                this.edges.push(d)
            }
        }
        a = this.faces.length;
        for (c = 0; c < a; c++)
        {
            d = this.faces[c];
            b = d.length;
            d = d.slice(0, b).reverse();
            for (f = 0; f < b; f++) {
                if (this.n10b[d[f]] > 0) {
                    d[f] = this.n10b[d[f]];
                }
                this.faces.push(d);
            }
        }
    },
    n083 : function (a)
    {
        this.mirror = a;
        for (var b = [], c = {}, d = 0; d < this.vertices.length / 3; d++) b[d] = a.distance(this.n0ad(d)); var f = [], 
        h = this.faces.length, i = [];
        for (d = 0; d < h; d++)
        {
            for (var j = this.faces[d], k = j.length, l = true, n = true, p =- 1, o =- 1, r = [], m = 0; m < k; m++)
            {
                var q = j[m] + "_" + j[(m + 1) % k], s = j[(m + 1) % k] + "_" + j[m], u = null;
                if (c[q]) {
                    u = c[q];
                }
                if (c[s]) {
                    u = c[s];
                }
                s = b[j[m]];
                var v = b[j[(m + 1) % k]];
                s > 0 && r.push(j[m]);
                if (s > 0 && v < 0 || s < 0 && v > 0)
                {
                    l = this.n0ad(j[m]);
                    n = this.n0ad(j[(m + 1) % k]);
                    if (u) {
                        l = u.idx;
                    }
                    else
                    {
                        u = a.n089(new n15d(l, n));
                        l = this.vertices.length / 3;
                        this.vertices.push(u[0]);
                        this.vertices.push(u[1]);
                        this.vertices.push(u[2]);
                        c[q] = {
                            vtx : u, idx : l
                        };
                        s > 0 ? f.push(j[m]) : f.push(j[(m + 1) % k]);
                        f.push(l)
                    }
                    if (p < 0) {
                        p = l;
                    }
                    else if (o < 0) {
                        o = l;
                        f.push(p);
                        f.push(o)
                    }
                    r.push(l);
                    n = l = false
                }
                else {
                    if (s > 0) {
                        l = l && true;
                        n = n && false
                    }
                    if (s < 0) {
                        l = l && false;
                        n = n && true;
                    }
                }
                s < 0 && this.ren0b5(j[m])
            }
            if (!l && !n) {
                this.faces[d] = r;
            }
            if (n) {
                for (m = 0; m < k; m++) {
                    this.ren0b5(j[m]);
                }
                i.push(d)
            }
        }
        b = [];
        for (d = 0; d < h; d++) {
            i.indexOf(d) >= 0 || b.push(this.faces[d]);
        }
        this.faces = b;
        this.edges = this.edges.concat(f);
        this.defragment();
        this.n085(a)
    },
    n0c1 : function (a, b)
    {
        View.save();
        this.transform();
        for (var c = 0; c < this.edges.length; c += 2)
        {
            var d = V3.$((this.vertices[this.edges[c]] + this.vertices[this.edges[c + 1]]) / 2, (this.vertices[this.edges[c] + 1] + this.vertices[this.edges[c + 1] + 1]) / 2, 
            (this.vertices[this.edges[c] + 2] + this.vertices[this.edges[c + 1] + 2]) / 2);
            if (n065(a, b, View.project(d))) {
                a = this.n0af();
                View.restore();
                return n0f7.mulV3(a, d);
            }
        }
        View.restore();
        return null;
    },
    n057 :- 1,
    n07f : function (a, b)
    {
        View.save();
        this.transform();
        this.n057 =- 1;
        for (var c = 0; c < this.vertices.length; c += 3)
        {
            var d = V3.$(this.vertices[c], this.vertices[c + 1], this.vertices[c + 2]);
            if (n065(a, b, View.project(d)))
            {
                if (this.n057 >= 0) 
                {
                    var f = V3.$(this.vertices[this.n057], this.vertices[this.n057 + 1], this.vertices[this.n057 + 2]);
                    f = View.project(f)[2];
                    if (View.project(d)[2] > f) {
                        this.n057 = c  / 3 ;
                    }
                }
                else {
                    this.n057 = c  / 3;
                }
            }
        }
        View.restore()
    },
    n056 :- 1,
    n07e : function (a, b)
    {
        View.save();
        this.transform();
        this.n056 =- 1;
        for (var c = 0; c < this.edges.length; c += 2)
        {
            var d = V3.$(this.vertices[3 * this.edges[c]], this.vertices[3 * this.edges[c] + 1], this.vertices[3 * this.edges[c] + 2]), 
            f = V3.$(this.vertices[3 * this.edges[c + 1]], this.vertices[3 * this.edges[c + 1] + 1], this.vertices[3 * this.edges[c + 1] + 2]);
            d = View.project(d);
            f = View.project(f);
            var h = V3.sub(f, d);
            if (n066(a, b, d, h))
            {
                if (this.n056 >= 0) 
                {
                    h = V3.$(this.vertices[3 * this.edges[2 * this.n056]], this.vertices[3 * this.edges[2 * this.n056] + 1], 
                    this.vertices[3 * this.edges[2 * this.n056] + 2]);
                    var i = V3.$(this.vertices[3 * this.edges[2 * this.n056 + 1]], this.vertices[3 * this.edges[2 * this.n056 + 1] + 1], 
                    this.vertices[3 * this.edges[2 * this.n056 + 1] + 2]);
                    h = Math.max(View.project(h)[2], View.project(i)[2]);
                    if (Math.max(d[2], f[2]) > h) {
                        this.n056 = c  / 2 ;
                    }
                }
                else {
                    this.n056 = c  / 2;
                }
            }
        }
        View.restore()
    },
    n0ec : function ()
    {
        var a = this.n0ad(this.edges[2 * this.n056]), b = this.n0ad(this.edges[2 * this.n056 + 1]);
        return V3.length(V3.sub(a, b));
    },
    n053 :- 1,
    n07d : function (a, b)
    {
        View.save();
        this.transform();
        this.n053 =- 1;
        for (var c = 0; c < this.faces.length; c++)
        {
            for (var d = 0; d < this.faces[c].length - 2; d++) 
            {
                var f = this.n0c2(this.faces[c][0], this.faces[c][d + 1], this.faces[c][d + 2]);
                if (n068(a, b, f[0], f[1], f[2])) if (this.n053 >= 0) 
                {
                    var h = this.faces[this.n053], i = this.n054;
                    h = this.n0c2(h[0], h[i + 1], h[i + 2]);
                    h = Math.max(h[0][2], h[1][2], h[2][2]);
                    if (Math.max(f[0][2], f[1][2], f[2][2]) > h) {
                        this.n053 = c;
                        this.n054 = d;
                    }
                }
                else {
                    this.n053 = c;
                    this.n054 = d;
                }
            }
            View.restore();
        }
    },
    n080 : function (a, b)
    {
        View.save();
        this.transform();
        this.selected = false;
        for (var c = 0; c < this.faces.length; c++)
        {
            for (var d = 0; d < this.faces[c].length - 2; d++)
            {
                var f = this.n0c2(this.faces[c][0], this.faces[c][d + 1], this.faces[c][d + 2]);
                if (n068(a, b, f[0], f[1], f[2])) {
                    this.selected = true;
                    break
                }
            }
            if (this.selected) {
                break;
            }
        }
        View.restore()
    },
    project : function ()
    {
        View.save();
        this.transform();
        for (var a = [], b = 0; b < this.vertices.length; b += 3)
        {
            a[b  / 3] = View.project(V3.$(this.vertices[b], this.vertices[b + 1], this.vertices[b + 2]));
        }
        View.restore();
        return a;
    },
    n0c2 : function (a, b, c)
    {
        return [View.project(V3.$(this.vertices[3 * a], this.vertices[3 * a + 1], this.vertices[3 * a + 2])), 
        View.project(V3.$(this.vertices[3 * b], this.vertices[3 * b + 1], this.vertices[3 * b + 2])), 
        View.project(V3.$(this.vertices[3 * c], this.vertices[3 * c + 1], this.vertices[3 * c + 2]))]
    },
    n0eb : function ()
    {
        View.save();
        this.transform();
        var a = View.project(this.n0ad(this.edges[2 * this.n056])), b = View.project(this.n0ad(this.edges[2 * this.n056 + 1]));
        xya = n063(a[0], a[1], a[2]);
        xyb = n063(b[0], b[1], b[2]);
        View.restore();
        return [xya, xyb];
    },
    extents : function ()
    {
        View.save();
        this.transform();
        for (var a = 0, b = 0, c = 0, d = 0, f = 0; f < this.vertices.length / 3; f++)
        {
            var h = View.project(V3.$(this.vertices[3 * f], this.vertices[3 * f + 1], this.vertices[3 * f + 2]));
            h = n063(h[0], h[1], h[2]);
            if (f == 0) {
                a = c = h[0];
                b = d = h[1]
            }
            else {
                a = h[0] < a ? h[0] : a;
                b = h[1] < b ? h[1] : b;
                c = h[0] > c ? h[0] : c;
                d = h[1] > d ? h[1] : d;
            }
        }
        View.restore();
        return [a, b, c, d];
    },
    faceExtents : function ()
    {
        View.save();
        this.transform();
        for (var a = 0, b = 0, c = 0, d = 0, f = this.faces[this.n053], h = 0; h < f.length; h++)
        {
            var i = View.project(V3.$(this.vertices[3 * f[h]], this.vertices[3 * f[h] + 1], this.vertices[3 * f[h] + 2]));
            i = n063(i[0], i[1], i[2]);
            if (h == 0) {
                a = c = i[0];
                b = d = i[1]
            }
            else {
                a = i[0] < a ? i[0] : a;
                b = i[1] < b ? i[1] : b;
                c = i[0] > c ? i[0] : c;
                d = i[1] > d ? i[1] : d;
            }
        }
        View.restore();
        return [a, b, c, d];
    },
    edgeExtents : function ()
    {
        View.save();
        this.transform();
        var a = 0, b = 0, c = 0, d = 0;
        b = this.edges[2 * this.n056];
        a = this.edges[2 * this.n056 + 1];
        b = View.project(V3.$(this.vertices[3 * b], this.vertices[3 * b + 1], this.vertices[3 * b + 2]));
        a = View.project(V3.$(this.vertices[3 * a], this.vertices[3 * a + 1], this.vertices[3 * a + 2]));
        d = n063(b[0], b[1], b[2]);
        var f = n063(a[0], a[1], a[2]);
        a = d[0] < f[0] ? d[0] : f[0];
        b = d[1] < f[1] ? d[1] : f[1];
        c = d[0] > f[0] ? d[0] : f[0];
        d = d[1] > f[1] ? d[1] : f[1];
        View.restore();
        return [a, b, c, d];
    },
    vtxExtents : function ()
    {
        View.save();
        this.transform();
        var a = 0, b = 0, c = 0, d = 0;
        a = this.n057;
        a = View.project(V3.$(this.vertices[3 * a], this.vertices[3 * a + 1], this.vertices[3 * a + 2]));
        b = n063(a[0], a[1], a[2]);
        a = c = b[0];
        b = d = b[1];
        View.restore();
        return [a, b, c, d];
    },
    n078 : function ()
    {
        this.n124();
        var a = this.faces[this.n053], b = [];
        this.n10d = [];
        this.n10e = [];
        for (var c = this.vertices.length / 3, d = 0; d < a.length; d++)
        {
            this.vertices.push(this.vertices[3 * a[d]]);
            this.vertices.push(this.vertices[3 * a[d] + 1]);
            this.vertices.push(this.vertices[3 * a[d] + 2]);
            b.push(c + d);
            this.n10e.push(this.edges.length / 2);
            this.edges.push(c + d);
            this.edges.push(d == a.length - 1 ? c : c + d + 1)
        }
        for (d = 0; d < a.length; d++)
        {
            c = [];
            var f = d + 1;
            if (f == a.length) {
                f = 0;
            }
            c.push(a[d]);
            c.push(a[f]);
            c.push(b[f]);
            c.push(b[d]);
            this.n10d.push(this.faces.length);
            this.faces.push(c);
            this.n10e.push(this.edges.length / 2);
            this.edges.push(a[d]);
            this.edges.push(b[d])
        }
        a = this.faces[this.n053];
        this.n10d.push(this.n053);
        this.faces[this.n053] = b;
        return {
            oldface : a, focus : this.n053, n10f : this.n10d.length, n110 : this.n10e.length
        }
    },
    n07a : function (a)
    {
        if (!this.faceColors) {
            this.faceColors = [];
        }
        this.faceColors[this.n053] = a;
        this.n06f();
        this.draw()
    },
    color : function (a)
    {
        this.geometryColor = a;
        this.faceColors = [];
        this.n06f();
        this.draw()
    },
    dup : function (a)
    {
        var b = new n052;
        b.name = a;
        b.stdtype = this.stdtype;
        if (this.stdtype != n052.n13b) {
            b.vertices = this.vertices;
            b.edges = this.edges;
            b.faces = this.faces
        }
        else
        {
            b.vertices = this.vertices.slice(0);
            b.edges = this.edges.slice(0);
            b.faces = this.faces.slice(0)
        }
        b.geometryColor = this.geometryColor;
        if (this.faceColors) {
            b.faceColors = this.faceColors.slice(0);
        }
        b.transforms = this.transforms.slice(0);
        b.mode = this.mode;
        return b;
    },
    populate : function (a)
    {
        if (a.stdtype == n052.n13b) {
            this.vertices = a.vertices;
            this.edges = a.edges;
            this.faces = a.faces
        }
        else
        {
            var b = n052.n081(a.stdtype);
            this.vertices = b.points;
            this.edges = b.edges;
            this.faces = b.faces
        }
        this.stdtype = a.stdtype;
        this.name = a.name;
        this.geometryColor = a.geometryColor;
        this.faceColors = a.faceColors;
        this.transforms = a.transforms;
        this.mode = n059;
    }
};
n052.n081 = function (a)
{
    switch (a)
    {
        case n052.n12f:
            return n0e6;
        case n052.n130:
            n0e5 || n0c8();
            return n0e5;
        case n052.n131:
            return n0e7;
        default:
            throw "Unexpected standard type " + a;
    }
};
n052.create = function (a, b, c)
{
    switch (a)
    {
        case n052.n12e:
            a = n052.n14c("cube" + this.gcount++, null, null, b, c);
            break;
        case n052.n12f:
            a = n052.n14d("cyl" + this.gcount++, null, null, b, c);
            break;
        case n052.n130:
            a = n052.Sphere("sphere" + this.gcount++, null, null, b, c);
            break;
        case n052.n132:
            a = n052.n149("square" + this.gcount++, null, null, b, c);
            break;
        case n052.n133:
            a = n052.n14a("circle" + this.gcount++, null, null, b, c);
            break;
        case n052.TRIANGLE:
            a = n052.Triangle("triangle" + this.gcount++, null, null, b, c);
            break;
        case n052.n131:
            a = n052.n14b("cone" + this.gcount++, null, null, b, c);
            break;
        default:
            throw "unexpected";
    }
    a.n06f();
    return a;
};
n052.n0c4 = function (a)
{
    var b = new n052;
    b.load("VertexFocus", [ - 1, - 1, - 1, 1, - 1, - 1, 1, 1, - 1, - 1, 1, - 1, - 1, - 1, 1, 1, - 1, 1, 
    1, 1, 1, - 1, 1, 1], [0, 0, - 1, 0, 0, 1, 0, 1, 0, 0, - 1, 0, 1, 0, 0, - 1, 0, 0], [0, 1, 1, 2, 2, 
    3, 3, 0, 4, 5, 5, 6, 6, 7, 7, 4, 0, 4, 1, 5, 2, 6, 3, 7], [[0, 1, 2, 3], [4, 5, 6, 7], [7, 3, 2, 6], 
    [4, 5, 1, 0], [5, 6, 2, 1], [4, 0, 3, 7]], [0, 0, 1, 1], null, a, n059);
    return b;
};
n052.n14d = function (a, b, c, d, f)
{
    var h = new n052;
    a || (a = "unknown_geom");
    h.load(a, n0e6.points, [], n0e6.edges, n0e6.faces, b, c, d, f, n052.n12f);
    return h;
};
n052.Sphere = function (a, b, c, d, f)
{
    var h = new n052;
    a || (a = "unnkown_geom");
    n0e5 || n0c8();
    h.load(a, n0e5.points, [], n0e5.edges, n0e5.faces, b, c, d, f, n052.n130);
    return h;
};
n052.n14c = function (a, b, c, d, f)
{
    var h = new n052;
    if (a == undefined || a == null) {
        a = "unnkown_geom";
    }
    h.load(a, [ - 1, - 1, - 1, 1, - 1, - 1, 1, 1, - 1, - 1, 1, - 1, - 1, - 1, 1, 1, - 1, 1, 1, 1, 1, - 1, 
    1, 1], [0, 0, - 1, 0, 0, 1, 0, 1, 0, 0, - 1, 0, 1, 0, 0, - 1, 0, 0], [0, 1, 1, 2, 2, 3, 3, 0, 4, 5, 
    5, 6, 6, 7, 7, 4, 0, 4, 1, 5, 2, 6, 3, 7], [[3, 2, 1, 0], [4, 5, 6, 7], [7, 6, 2, 3], [5, 4, 0, 1], 
    [6, 5, 1, 2], [4, 7, 3, 0]], b, c, d, f, n052.n13b);
    return h;
};
n052.n149 = function (a, b, c, d, f)
{
    var h = new n052;
    if (a == undefined || a == null) {
        a = "unnkown_geom";
    }
    h.load(a, [ - 1, - 1, - 1, 1, - 1, - 1, 1, 1, - 1, - 1, 1, - 1], [0, 0, - 1], [0, 1, 1, 2, 2, 3, 3, 
    0], [[0, 1, 2, 3]], b, c, d, f, n052.n13b);
    return h;
};
n052.n14a = function (a, b, c, d, f)
{
    var h = new n052;
    if (a == undefined || a == null) {
        a = "unnkown_geom";
    }
    var i = n0c5(1, 32);
    h.load(a, i.points, [0, 0, - 1], i.edges, i.faces, b, c, d, f, n052.n13b);
    return h;
};
n052.Triangle = function (a, b, c, d, f)
{
    var h = new n052;
    a || (a = "unnkown_geom");
    h.load(a, [ - 1, 0, 0, 1, 0, 0, 0, 1.732, 0], [0, 0, - 1], [0, 1, 1, 2, 2, 0], [[0, 1, 2]], b, c, 
    d, f, n052.n13b);
    return h;
};
n052.n14b = function (a, b, c, d, f)
{
    var h = new n052;
    a || (a = "unnkown_geom");
    h.load(a, n0e7.points, [], n0e7.edges, n0e7.faces, b, c, d, f, n052.n131);
    return h;
};
var n05f = function () {};
n05f.prototype = 
{
    geometry : null, info : null, action :- 1,
    set : function (a, b)
    {
        this.geometry = a;
        this.position();
        this.refresh(b);
        this.show()
    },
    position : function ()
    {
        switch (mode == n147 ? n0d7.n11b : this.geometry.n0fe())
        {
            case n0d7.n11b:
                var a = this.geometry.extents();
                break;
            case n0d7.n11c:
                a = this.geometry.faceExtents();
                break;
            case n0d7.n11d:
                a = this.geometry.edgeExtents();
                break;
            case n0d7.n11e:
                a = this.geometry.vtxExtents();
                break
        }
        var b = a[0], c = a[1], d = a[2];
        a = a[3];
        $("#cpanel").css("left", b - 25 + "px");
        $("#cpanel").css("top", c - 25 + "px");
        b = Math.max(350, 50 + d - b);
        $("#cpanel").css("width", b + "px");
        $("#cpanel").css("height", 50 + a - c + "px");
        $("#cpanel #info").css("top", 20 + a - c + "px")
    },
    refresh : function (a)
    {
        if (a) {
            this.action = a;
        }
        if (this.geometry)
        {
            if (mode == n148)
            {
                if (!this.info) {
                    this.info = action == n13e || action == n13d ? [0, 0, 0] : [1, 1, 1];
                }
                $("#cpanel #xname").text("dx");
                $("#cpanel #yname").text("dy");
                $("#cpanel #zname").text("dz")
            }
            else
            {
                if (this.action == n13e) {
                    this.info = this.geometry.n0b9();
                }
                else if (this.action == n13c) {
                    this.info = this.geometry.n0ba();
                }
                else if (this.action == n13d) {
                    this.info = this.geometry.n0bb();
                }
                $("#cpanel #xname").text("x");
                $("#cpanel #yname").text("y");
                $("#cpanel #zname").text("z")
            }
            this.showInfo()
        }
    },
    reset : function ()
    {
        this.info = this.geometry = null;
        this.action =- 1;
        $("#cpanel").css("visibility", "hidden");
        $("#scale").css("visibility", null);
        $("#rotate").css("visibility", null);
        this.facevtx = null;
    },
    show : function ()
    {
        $("#cpanel").css("visibility", "visible");
        switch (this.geometry.n0fe())
        {
            case n0d7.n11b:
            case n0d7.n11c:
                $("#scale").css("visibility", "visible");
                $("#rotate").css("visibility", "visible");
                break;
            case n0d7.n11d:
                $("#scale").css("visibility", "visible");
                $("#rotate").css("visibility", "hidden");
                break;
            case n0d7.n11e:
                $("#scale").css("visibility", "hidden");
                $("#rotate").css("visibility", "hidden");
                break
        }
    },
    showInfo : function ()
    {
        $("#cpanel #xval").text(this.info[0].toFixed(3));
        $("#cpanel #yval").text(this.info[1].toFixed(3));
        $("#cpanel #zval").text(this.info[2].toFixed(3))
    },
    change : function (a, b)
    {
        if (b) {
            a = V3.mul(a, b);
        }
        this.info = V3.add(this.info, a);
    }
};
var n159 = 0.1, n15a = 100, n15b = 45, n15c = 1, n156, n157;
function View() {}
View.pMatrix = null;
View.n106 = null;
View.nMatrix = null;
View.zoom = n15b;
View.xAngle = 5;
View.yAngle =- 10;
View.zAngle = 0;
View.n0a4 = [0, 0, 10];
View.init = function ()
{
    gl.clearColor(0.96, 0.96, 0.96, 1);
    gl.clearDepth(1);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    View.cpanel = new n05f;
};
View.setn150 = function (a)
{
    View.n0a1 = a;
};
View.n06f = function ()
{
    n150.n06fAxis();
    View.n0a1 != null && View.n0a1.n06f()
};
View.n09e = function ()
{
    if (isLoggedIn)
    {
        params = {};
        if (View.n0a1.uid && View.n0a1.uid != "_SAMPLE_") {
            params.uid = View.n0a1.uid;
        }
        if (!View.n0a1.name || View.n0a1.name == "_SAMPLE_")
        {
            var a = prompt("Enter name");
            if (a.trim() == "") {
                alert("Please enter non empty name");
                return
            }
            View.n0a1.name = a
        }
        params.content = View.n0a1.toString();
        params.name = View.n0a1.name;
        $.post("/_save", params, function (b)
        {
            b = JSON.parse(b);
            if (b.result != "SUCCESS") {
                alert(b.result);
            }
            else {
                View.n0a1.uid = b.uid;
                View.n0a1.n12c = false;
            }
        })
    }
    else {
        alert("You need to login first");
    }
};
View.n09f = function (a)
{
    if (View.n0a1 && View.n0a1.n12c)
    {
        if (!confirm("You have unsaved changes. Proceed Anyway?")) {
            return;
        }
        $.post("/_load", {
            uid : a 
        },
        function (b) 
        {
            b = JSON.parse(b);
            if (b.result != "SUCCESS") {
                alert("Load failure: " + b.result);
            }
            else 
            {
                var c = JSON.parse(b.content);
                View.n0a1 = new n150;
                for (var d = 0; d < c.geometries.length; d++) {
                    var f = new n052;
                    f.populate(c.geometries[d]);
                    View.n0a1.geometries.push(f) 
                }
                View.n0a1.uid = b.uid;
                View.n0a1.name = b.name;
                View.n06f();
                View.draw() 
            }
        });
    }
};
View.n0a0 = function ()
{
    isLoggedIn ? $.post("/_list", null, function (a)
    {
        a = JSON.parse(a);
        if (a.result != "SUCCESS") {
            alert(a.result);
        }
        else
        {
            $("#tinlist").empty();
            for (var b = 0; b < a.list.length; b++)
            {
                $("#tinlist").append('<span class="tinentry" id=' + a.list[b].uid + ">" + a.list[b].name + "</span><br/>");
            }
            $(".tinentry").click(function ()
            {
                View.n09f($(this).attr("id"));
                $("#tinlistdlg").fadeOut()
            });
            $("#tinlistdlg").fadeIn()
        }
    }) : alert("You need to login first")
};
var n137 = 0, n138 = 1, n139 = 2, n13a = 3, n135 = 4, n136 = 5;
View.n14e = function (a)
{
    switch (a)
    {
        case n137:
            View.xAngle = 90;
            View.yAngle = 0;
            View.zAngle = 0;
            View.n0a4[0] = 0;
            View.n0a4[1] = 0;
            View.n0a4[2] = 10;
            break;
        case n138:
            View.xAngle =- 90;
            View.yAngle = 0;
            View.zAngle = 0;
            View.n0a4[0] = 0;
            View.n0a4[1] = 0;
            View.n0a4[2] = 10;
            break;
        case n139:
            View.xAngle = 0;
            View.yAngle = 90;
            View.zAngle = 0;
            View.n0a4[0] = 0;
            View.n0a4[1] = 0;
            View.n0a4[2] = 10;
            break;
        case n13a:
            View.xAngle = 0;
            View.yAngle =- 90;
            View.zAngle = 0;
            View.n0a4[0] = 0;
            View.n0a4[1] = 0;
            View.n0a4[2] = 10;
            break;
        case n135:
            View.xAngle = 0;
            View.yAngle = 0;
            View.zAngle = 0;
            View.n0a4[0] = 0;
            View.n0a4[1] = 0;
            View.n0a4[2] = 10;
            break;
        case n136:
            View.xAngle = 0;
            View.yAngle = 180;
            View.zAngle = 0;
            View.n0a4[0] = 0;
            View.n0a4[1] = 0;
            View.n0a4[2] = 10;
            break
    }
    View.draw()
};
View.draw = function ()
{
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    View.pMatrix = n142 == n141 ? n0f7.n11f(View.zoom, n15c, n159, n15a) : n0f7.n120(-n156, n156, - n157, 
    n157, n159, n15a);
    View.n106 = n0f7.clone(n0f7.I);
    View.n106 = n0f7.translate3(-View.n0a4[0], - View.n0a4[1], - View.n0a4[2], View.n106);
    View.n106 = n0f7.rotate(Math.PI * View.xAngle / 180, V3.x, View.n106);
    View.n106 = n0f7.rotate(Math.PI * View.yAngle / 180, V3.y, View.n106);
    View.n106 = n0f7.rotate(Math.PI * View.zAngle / 180, V3.z, View.n106);
    gl.uniform3f(n0fc.n108, 0.2, 0.2, 0.2);
    gl.uniform3f(n0fc.n109, 0.8, 0.8, 0.8);
    var a = V3.normalize(V3.$(-0.25, - 0.25, - 1));
    gl.uniform3f(n0fc.n10a, - 1 * a[0], - 1 * a[1], - 1 * a[2]);
    gl.uniform1i(n0fc.n111, true);
    n150.n0d5();
    View.n0a1 != null && View.n0a1.draw()
};
View.n07d = function (a, b)
{
    View.n0a1 != null && View.n0a1.n07d(a, b)
};
View.n07c = function (a, b)
{
    View.n0a1 != null && View.n0a1.n07c(a, b)
};
View.n080 = function (a, b)
{
    View.n0a1 != null && View.n0a1.n080(a, b)
};
View.n074 = function (a, b)
{
    View.n0a1 != null && View.n0a1.n074(a, b)
};
View.project = function (a)
{
    return n0f7.mulV3(View.n106, a);
};
View.n0cc = function (a)
{
    var b = n0f7.n0e4(View.n106);
    return n0f7.mulV3(b, a);
};
View.n0a5 = [];
View.save = function ()
{
    View.n0a5.push(n0f7.clone(View.n106))
};
View.restore = function ()
{
    if (View.n0a5.length == 0) {
        throw "Invalid popMatrix!";
    }
    View.n106 = View.n0a5.pop();
};
View.translate = function (a)
{
    View.n106 = n0f7.translate(a, View.n106);
};
View.scale = function (a)
{
    n0f7.scale(a, View.n106, View.n106)
};
View.rotate = function (a, b)
{
    View.n106 = n0f7.rotate(a * Math.PI / 180, b, View.n106);
};
var n158 = 100;
function n150()
{
    this.geometries = [];
    this.n12c = false
}
n150.prototype = 
{
    n06f : function ()
    {
        for (var a = 0; a < this.geometries.length; a++) {
            var b = this.geometries[a];
            b.n0a6 || b.n06f()
        }
    },
    draw : function ()
    {
        for (var a = 0; a < this.geometries.length; a++) {
            var b = this.geometries[a];
            b.n0a6 || b.draw()
        }
        this.n113()
    },
    add : function (a)
    {
        this.geometries.push(a)
    },
    n069 : [], n06a : null, n06b : null, n06c : null, n06d : false,
    n074 : function ()
    {
        this.n06d = false;
        this.n06e()
    },
    n075 : function (a, b)
    {
        for (var c = 0; c < this.geometries.length; c++)
        {
            this.geometries[c].n07f(a, b);
            var d = this.geometries[c].n057, f = null;
            if (d >= 0) {
                f = this.geometries[c].n0ae(d);
            }
            if (f == null) {
                f = this.geometries[c].n0c1(a, b);
            }
            if (f != null)
            {
                if (this.n06d) {
                    this.n069.pop();
                    this.n069.pop();
                    this.n069.pop()
                }
                this.n069.push(f[0], f[1], f[2]);
                this.n06d = true;
                this.n06e()
            }
        }
    },
    n076 : function (a, b)
    {
        var c = View.project(V3.$(0, 0, 0)), d = null, f = null, h = null;
        h = View.project(V3.$(1, 0, 0));
        var i = View.project(V3.$(0, 1, 0));
        d = n067(a, b, c, h, i);
        h = View.project(V3.$(0, 0, 1));
        i = View.project(V3.$(0, 1, 0));
        f = n067(a, b, c, h, i);
        h = View.project(V3.$(0, 0, 1));
        i = View.project(V3.$(1, 0, 0));
        (h = n067(a, b, c, h, i)) || (h = V3.$(0, 0, - 100000));
        f || (f = V3.$(0, 0, - 100000));
        d || (d = V3.$(0, 0, - 100000));
        return d[2] > f[2] ? d[2] > h[2] ? View.n0cc(d) : View.n0cc(h) : f[2] > h[2] ? View.n0cc(f) : View.n0cc(h);
    },
    n06e : function ()
    {
        if (this.n069.length > 3)
        {
            this.n06a && n152(this.n06a);
            this.n06a = n077(this.n069, gl.ARRAY_BUFFER, "float", 3, this.n069.length);
            for (var a = [], b = 0; b < this.n069.length / 3; b++) {
                a.push(b);
            }
            this.n06b && n152(this.n06b);
            this.n06b = n077(a, gl.ELEMENT_ARRAY_BUFFER, "ushort", 1, a.length);
            a = [];
            for (b = 0; b < this.n069.length / 3; b++) {
                a.push(0, 0, 1, 1);
            }
            this.n06c && n152(this.n06c);
            this.n06c = n077(a, gl.ARRAY_BUFFER, "float", 4, a.length);
        }
    },
    n113 : function ()
    {
        if (this.n06a != null) {
            gl.lineWidth(1);
            n0a8(this.n06a, null, this.n06c, this.n06b, gl.LINE_STRIP)
        }
    },
    n079 : function ()
    {
        this.selG =- 1;
        for (var a = 0; a < this.geometries.length; a++) {
            this.geometries[a].n053 =- 1;
            this.geometries[a].n056 =- 1;
            this.geometries[a].n057 =- 1
        }
    },
    n07d : function (a, b)
    {
        this.selG =- 1;
        for (var c = 0; c < this.geometries.length; c++) {
            this.geometries[c].n07d(a, b);
            if (this.geometries[c].n053 >= 0) {
                this.selG = c;
                break
            }
        }
    },
    n07a : function (a)
    {
        this.selG >= 0 && this.geometries[this.selG].n07a(a)
    },
    n07b : function (a)
    {
        this.selG >= 0 && this.geometries[this.selG].color(a)
    },
    n07c : function (a, b)
    {
        this.selG =- 1;
        if (this.geometries) for (var c = 0;
        c < this.geometries.length;
        c++)
        {
            this.geometries[c].n07f(a, b);
            if (this.geometries[c].n057 >= 0) {
                this.selG = c;
                break
            }
            this.geometries[c].n07e(a, b);
            if (this.geometries[c].n056 >= 0) {
                this.selG = c;
                break
            }
            this.geometries[c].n07d(a, b);
            if (this.geometries[c].n053 >= 0) {
                this.selG = c;
                break
            }
        }
    },
    n080 : function (a, b)
    {
        this.selG =- 1;
        if (this.geometries) for (var c = 0;
        c < this.geometries.length;
        c++)
        {
            this.geometries[c].n080(a, b);
            if (this.geometries[c].selected)
            {
                if (this.selG >= 0) 
                {
                    for (var d = this.geometries[this.selG].project(), f = d[0][2], h = 1; h < d.length; h++) {
                        f = Math.max(f, d[h][2]);
                    }
                    d = this.geometries[c].project();
                    var i = d[0][2];
                    for (h = 1; h < d.length; h++) {
                        i = Math.max(i, d[h][2]);
                    }
                    if (i > f) {
                        this.selG = c ;
                    }
                }
                else {
                    this.selG = c;
                }
            }
        }
    },
    n096 : function ()
    {
        if (this.selG < 0) {
            alert("No geometry selected to delete");
        }
        else
        {
            this.geometries[this.selG].n0a6 = true;
            View.cpanel.reset();
            this.do_(Op.n129(this.geometries[this.selG]));
            this.selG =- 1
        }
    },
    copyG :- 1,
    copy : function ()
    {
        if (this.selG < 0) {
            alert("No geometry selected");
        }
        else {
            this.copyG = this.selG;
        }
    },
    paste : function ()
    {
        if (this.copyG < 0) {
            alert("No geometry in clipboard");
        }
        else
        {
            var a = this.geometries[this.copyG].dup("copygeom");
            a.transforms.push({
                translation : V3.$(1, 1, 1)
            });
            a.n06f();
            this.geometries.push(a);
            this.do_(Op.create(a));
            this.copyG =- 1
        }
    },
    gcount : 0,
    n097 : function (a, b)
    {
        switch (b.type)
        {
            case Op.n155:
                a.push(b.subject);
                break;
            case Op.n118:
                b.subject.n0a6 = true;
                break;
            case Op.MODIFY:
                a = b.subject;
                a.transforms.push(b.xform);
                break;
            case Op.n114:
                a = b.subject;
                var c = b.detail, d = b.xform, f = a.n0ad(c);
                if (a.n082(c)) {
                    var h = a.mirror.project(d);
                    a.n0b0(c, V3.add(f, h))
                }
                else {
                    a.n0b0(c, V3.add(f, d));
                }
                if (a.mirror) {
                    c = a.n10b[c];
                    if (c >= 0) {
                        f = a.n0ad(c);
                        d = a.mirror.n085(d);
                        a.n0b0(c, V3.add(f, d))
                    }
                }
                a.n06f();
                break;
            case Op.n115:
                a = b.subject;
                for (var i = 0; i < 2; i++)
                {
                    c = a.edges[2 * b.detail + i];
                    f = a.n0ad(c);
                    d = b.xform;
                    if (typeof d[0] == "number") if (a.n082(c)) {
                        h = a.mirror.project(d);
                        a.n0b0(c, V3.add(f, h))
                    }
                    else {
                        a.n0b0(c, V3.add(f, d));
                    }
                    else if (a.n082(c)) {
                        h = a.mirror.project(d[i]);
                        a.n0b0(c, V3.add(f, h))
                    }
                    else {
                        a.n0b0(c, V3.add(f, d[i]));
                    }
                    if (a.mirror)
                    {
                        c = a.n10b[c];
                        if (c >= 0)
                        {
                            f = a.n0ad(c);
                            d = typeof d[0] == "number" ? a.mirror.n085(d) : a.mirror.n085(d[i]);
                            a.n0b0(c, V3.add(f, d))
                        }
                    }
                }
                a.n06f();
                break;
            case Op.n116:
                a = b.subject;
                for (i = 0; i < a.faces[b.detail].length; i++)
                {
                    c = a.faces[b.detail][i];
                    f = a.n0ad(c);
                    d = b.xform;
                    if (typeof d[0] == "number") if (a.n082(c)) {
                        h = a.mirror.project(d);
                        a.n0b0(c, V3.add(f, h))
                    }
                    else {
                        a.n0b0(c, V3.add(f, d));
                    }
                    else if (a.n082(c)) {
                        h = a.mirror.project(d[i]);
                        a.n0b0(c, V3.add(f, h))
                    }
                    else {
                        a.n0b0(c, V3.add(f, d[i]));
                    }
                    if (a.mirror)
                    {
                        c = a.n10b[c];
                        if (c >= 0)
                        {
                            f = a.n0ad(c);
                            d = typeof d[0] == "number" ? a.mirror.n085(d) : a.mirror.n085(d[i]);
                            a.n0b0(c, V3.add(f, d))
                        }
                    }
                }
                a.n06f();
                break;
            case Op.n117:
                a = b.subject;
                a.n053 = b.detail.focus;
                a.n078();
                a.n084();
                for (i = 0; i < a.faces[b.detail.focus].length; i++)
                {
                    c = a.faces[b.detail.focus][i];
                    f = a.n0ad(c);
                    if (a.n082(c)) {
                        h = a.mirror.project(b.xform);
                        a.n0b0(c, V3.add(f, h))
                    }
                    else {
                        a.n0b0(c, V3.add(f, b.xform));
                    }
                    if (a.mirror) {
                        c = a.n10b[c];
                        if (c >= 0) {
                            f = a.n0ad(c);
                            d = a.mirror.n085(b.xform);
                            a.n0b0(c, V3.add(f, d))
                        }
                    }
                }
                a.n06f();
                break;
            case Op.n11a:
                a = this.geometries[b.subject];
                a.color(b.detail.color);
                break;
            case Op.n119:
                a = this.geometries[b.subject];
                a.n053 = b.detail.face;
                a.n07a(b.detail.color);
                break
        }
    },
    unn097 : function (a, b)
    {
        switch (b.type)
        {
            case Op.n155:
                a.pop();
                break;
            case Op.n118:
                b.subject.n0a6 = false;
                b.subject.n06f();
                break;
            case Op.MODIFY:
                a = b.subject;
                a.transforms.splice(a.transforms.indexOf(b.xform), 1);
                break;
            case Op.n114:
                a = b.subject;
                var c = b.detail, d = b.xform, f = a.n0ad(c);
                if (a.n082(c)) {
                    var h = a.mirror.project(d);
                    a.n0b0(c, V3.sub(f, h))
                }
                else {
                    a.n0b0(c, V3.sub(f, d));
                }
                if (a.mirror) {
                    c = a.n10b[c];
                    if (c >= 0) {
                        f = a.n0ad(c);
                        h = a.mirror.n085(d);
                        a.n0b0(c, V3.sub(f, h))
                    }
                }
                a.n06f();
                break;
            case Op.n115:
                a = b.subject;
                for (var i = 0; i < 2; i++)
                {
                    c = a.edges[2 * b.detail + i];
                    f = a.n0ad(c);
                    d = b.xform;
                    if (typeof d[0] == "number") if (a.n082(c)) {
                        h = a.mirror.project(d);
                        a.n0b0(c, V3.sub(f, h))
                    }
                    else {
                        a.n0b0(c, V3.sub(f, d));
                    }
                    else if (a.n082(c)) {
                        h = a.mirror.project(d[i]);
                        a.n0b0(c, V3.sub(f, h))
                    }
                    else {
                        a.n0b0(c, V3.sub(f, d[i]));
                    }
                    if (a.mirror)
                    {
                        c = a.n10b[c];
                        if (c >= 0)
                        {
                            f = a.n0ad(c);
                            h = typeof d[0] == "number" ? a.mirror.n085(d) : a.mirror.n085(d[i]);
                            a.n0b0(c, V3.sub(f, h))
                        }
                    }
                }
                a.n06f();
                break;
            case Op.n116:
                a = b.subject;
                var j = a.faces[b.detail], k = j.length;
                d = b.xform;
                for (i = 0; i < k; i++)
                {
                    c = j[i];
                    f = a.n0ad(c);
                    if (typeof d[0] == "number") if (a.n082(c)) {
                        h = a.mirror.project(d);
                        a.n0b0(c, V3.sub(f, h))
                    }
                    else {
                        a.n0b0(c, V3.sub(f, d));
                    }
                    else if (a.n082(c)) {
                        h = a.mirror.project(d[i]);
                        a.n0b0(c, V3.sub(f, h))
                    }
                    else {
                        a.n0b0(c, V3.sub(f, d[i]));
                    }
                    if (a.mirror)
                    {
                        c = a.n10b[c];
                        if (c >= 0)
                        {
                            f = a.n0ad(c);
                            h = typeof d[0] == "number" ? a.mirror.n085(d) : a.mirror.n085(d[i]);
                            a.n0b0(c, V3.sub(f, h))
                        }
                    }
                }
                a.n06f();
                break;
            case Op.n117:
                a = b.subject;
                if (a.mirror)
                {
                    for (i = 0; i < b.detail.n10f; i++) {
                        a.faces.pop();
                    }
                    for (i = 0; i < 2 * b.detail.n110; i++) {
                        a.edges.pop();
                    }
                    d = 2 * a.faces[b.detail.focus].length;
                    for (i = 0; i < d; i++) {
                        a.n10b.pop();
                    }
                }
                for (i = 0; i < a.faces[b.detail.focus].length; i++)
                {
                    c = a.faces[b.detail.focus][i];
                    f = a.n0ad(c);
                    if (a.n082(c)) {
                        h = a.mirror.project(b.xform);
                        a.n0b0(c, V3.sub(f, h))
                    }
                    else {
                        a.n0b0(c, V3.sub(f, b.xform));
                    }
                    if (a.mirror) {
                        c = a.n10b[c];
                        if (c >= 0) {
                            f = a.n0ad(c);
                            h = a.mirror.n085(b.xform);
                            a.n0b0(c, V3.sub(f, h))
                        }
                    }
                    for (d = 0; d < 2; d++) {
                        a.edges.pop();
                    }
                    a.faces.pop()
                }
                for (i = 0; i < a.faces[b.detail.focus].length; i++) {
                    for (d = 0; d < 2; d++) {
                        a.edges.pop();
                    }
                    for (d = 0; d < 3; d++) {
                        a.vertices.pop();
                    }
                }
                a.faces[b.detail.focus] = b.detail.oldface;
                a.n06f();
                break;
            case Op.n11a:
                a = this.geometries[b.subject];
                a.color(b.detail.oldcolor);
                break;
            case Op.n119:
                a = this.geometries[b.subject];
                a.n053 = b.detail.face;
                a.n07a(b.detail.oldcolor);
                break
        }
    },
    opq : [], n09a : 0, n099 : 0,
    do_ : function (a)
    {
        this.n12c = true;
        this.opq[this.n09a] = a;
        this.n09a = (this.n09a + 1) % n150.n0cb;
        $("#undo").css("background-image", "url('/images/undo.png')");
        this.n099 = 0;
    },
    undo : function ()
    {
        if (this.n099 != n150.n0cb - 1)
        {
            this.n09a--;
            if (this.n09a < 0) {
                this.n09a = n150.n0cb - 1;
            }
            if (this.opq[this.n09a])
            {
                this.unn097(this.geometries, this.opq[this.n09a]);
                $("#redo").css("background-image", "url('/images/redo.png')");
                this.n099++;
                this.n099 == n150.n0cb - 1 && $("#undo").css("background-image", "url('/images/noundo.png')")
            }
            else {
                this.n09a = (this.n09a + 1) % n150.n0cb;
            }
        }
    },
    redo : function ()
    {
        if (this.n099 != 0)
        {
            this.n097(this.geometries, this.opq[this.n09a]);
            this.n09a = (this.n09a + 1) % n150.n0cb;
            this.n099--;
            this.n099 == 0 && $("#redo").css("background-image", "url('/images/noredo.png')")
        }
    },
    toString : function ()
    {
        var a = '{ "geometries" : ';
        a += "[";
        for (var b = 0; b < this.geometries.length; b++)
        {
            g = this.geometries[b];
            if (!g.n0a6)
            {
                g.n09d();
                a += g.stdtype == n052.n13b ? JSON.stringify(g, n150.n0a2.concat(n150.n0a3)) : JSON.stringify(g, 
                n150.n0a2);
                if (b < this.geometries.length - 1) {
                    a += ",";
                }
            }
        }
        a += "]";
        a += ', "name" : "' + this.name + '" }';
        return a;
    }
};
n150.n0a3 = ["vertices", "edges", "faces"];
n150.n0a2 = ["stdtype", "geometries", "name", "geometryColor", "faceColors", "transforms", "list", "translation", 
"scale", "rotation", "axis", "angle"];
n150.n0cb = 10;
n150.n0cd = false;
n150.n06fAxis = function ()
{
    if (!n150.n0cd)
    {
        n150.n0d2 = n077([ - n158, 0, 0, n158, 0, 0, 0, - n158, 0, 0, n158, 0, 0, 0, - n158, 0, 0, n158], 
        gl.ARRAY_BUFFER, "float", 3, 6);
        n150.n0d3 = n077([1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1], gl.ARRAY_BUFFER, 
        "float", 4, 6);
        n150.n0d4 = n077([0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0], gl.ARRAY_BUFFER, "float", 
        3, 6);
        n150.n0cd = true;
    }
};
n150.n0d5 = function ()
{
    if (n150.n0cd) {
        gl.lineWidth(2);
        n0a8(n150.n0d2, n150.n0d4, n150.n0d3, null, gl.LINES)
    }
};
var n0ef = false;
function n0ed(a, b, c)
{
    n0f0.clearRect(0, 0, canvas2d.width, canvas2d.height);
    var d = a[0];
    d[2] = 0;
    var f = a[1];
    f[2] = 0;
    var h = V3.sub(f, d);
    V3.length(h);
    V3.normalize(h);
    var i = V3.mul(h, 3 / 7);
    h = V3.add(d, i);
    var j = V3.sub(f, i);
    i = (a[0][0] + a[1][0]) / 2;
    a = (a[0][1] + a[1][1]) / 2;
    var k = c[0] - i;
    c = c[1] - a;
    var l = Math.sqrt(k * k + c * c);
    k *=- 10 / l;
    c *=- 10 / l;
    n0f0.beginPath();
    n0f0.moveTo(d[0] + k, d[1] + c);
    n0f0.lineTo(h[0] + k, h[1] + c);
    n0f0.moveTo(j[0] + k, j[1] + c);
    n0f0.lineTo(f[0] + k, f[1] + c);
    n0f0.closePath();
    n0f0.stroke();
    d = n0f0.measureText(b.toFixed(1) + "m").width;
    n0f0.strokeText(b.toFixed(1) + "m", i - d / 2, a + c);
    n0ef = true
}
function n0ee()
{
    if (n0ef) {
        n0f0.clearRect(0, 0, canvas2d.width, canvas2d.height);
        n0ef = false;
    }
}
function n05d(a, b, c, d, f)
{
    return n05e(a, b, c, d, f)
}
function n05e(a, b, c, d, f)
{
    a = V3.$(n156 * (2 * a / c - 1), n157 * (2 * b / d - 1), - 1 * n159);
    if (n142 == n140) {
        return V3.$(a[0], a[1], f[2]);
    }
    else {
        a = V3.direction(a, V3.$(0, 0, 0));
        b = f[2] / a[2];
        return V3.$(b * a[0], b * a[1], f[2]);
    }
}
function n062(a, b, c, d)
{
    var f = V3.$(n156 * (2 * a / c - 1), n157 * (2 * b / d - 1), - 1 * n159);
    if (n142 == n140) {
        a = V3.$(n156 * (2 * a  / c - 1), n157 * (2 * b  / d - 1), - 1 * n15a);
    }
    else {
        a = V3.direction(f, V3.$(0, 0, 0));
        b = (-n15a - - n159) / a[2];
        a = V3.$(b * a[0], b * a[1], - n15a)
    }
    return [f, a]
}
function n063(a, b, c)
{
    if (n142 == n140) {
        a = a;
        c = b
    }
    else {
        a =- n159 * (a / c);
        c =- n159 * (b / c)
    }
    b = canvas.height;
    a = canvas.width / 2 * (a / n156 + 1);
    c = b / 2 * (c / n157 + 1);
    c = b - c;
    return [a, c]
}
function n064(a, b, c)
{
    c = V3.dot(V3.sub(c, a), b) / V3.n0e3(b);
    return V3.add(a, V3.mul(b, c))
}
function n065(a, b, c)
{
    var d = V3.dot(V3.sub(c, a), b) / V3.n0e3(b);
    a = V3.add(a, V3.mul(b, d));
    return V3.length(V3.sub(c, a)) < 0.2
}
function n066(a, b, c, d)
{
    var f = V3.sub(c, a), h = V3.cross(b, d), i = V3.dot(V3.cross(f, d), h) / V3.n0e3(h);
    if (i > 1 || i < 0) {
        return false;
    }
    f = V3.dot(V3.cross(f, b), h) / V3.n0e3(h);
    if (f > 1 || f < 0) {
        return false;
    }
    a = V3.add(a, V3.mul(b, i));
    c = V3.add(c, V3.mul(d, f));
    return V3.length(V3.sub(a, c)) < 0.2
}
function n067(a, b, c, d, f)
{
    var h = V3.sub(d, c);
    d = V3.sub(f, d);
    d = V3.cross(h, d);
    h = V3.dot(d, b);
    if (h == 0) {
        log("parallel");
        return null
    }
    c = V3.dot(d, c) - V3.dot(d, a);
    c /= h;
    if (c <= 0) {
        return null;
    }
    if (c > 1) {
        return null;
    }
    return V3.add(a, V3.mul(b, c))
}
function n068(a, b, c, d, f)
{
    var h = V3.sub(d, c), i = V3.sub(f, d);
    h = V3.cross(h, i);
    i = V3.dot(h, b);
    if (i == 0) {
        log("parallel");
        return null
    }
    var j = V3.dot(h, c) - V3.dot(h, a);
    j /= i;
    if (j <= 0) {
        return null;
    }
    if (j > 1) {
        return null;
    }
    a = V3.add(a, V3.mul(b, j));
    if (Math.abs(h[0]) > Math.abs(h[1]))
    {
        if (Math.abs(h[0]) > Math.abs(h[2])) {
            b = a[1] - c[1];
            h = d[1] - c[1];
            j = f[1] - c[1];
            i = a[2] - c[2];
            d = d[2] - c[2];
            f = f[2] - c[2] 
        }
        else {
            b = a[0] - c[0];
            h = d[0] - c[0];
            j = f[0] - c[0];
            i = a[1] - c[1];
            d = d[1] - c[1];
            f = f[1] - c[1] 
        }
        else if (Math.abs(h[1]) > Math.abs(h[2])) {
            b = a[0] - c[0];
            h = d[0] - c[0];
            j = f[0] - c[0];
            i = a[2] - c[2];
            d = d[2] - c[2];
            f = f[2] - c[2] 
        }
        else {
            b = a[0] - c[0];
            h = d[0] - c[0];
            j = f[0] - c[0];
            i = a[1] - c[1];
            d = d[1] - c[1];
            f = f[1] - c[1] 
        }
        c = h * f - d * j;
        if (c == 0) {
            return null;
        }
        c = 1  / c;
        f = (b * f - i * j) * c;
        if (f < 0) {
            return null;
        }
        c = (h * i - d * b) * c;
        if (c < 0) {
            return null;
        }
        if (f + c > 1) {
            return null;
        }
        return a;
    }
}
var n15e = function (a)
{
    this.normal = V3.cross(V3.sub(a[1], a[0]), V3.sub(a[2], a[1]));
    V3.normalize(this.normal);
    this.apoint = a[0];
    this.d = V3.dot(a[0], this.normal);
};
n15e.prototype = 
{
    distance : function (a)
    {
        return V3.dot(this.normal, a) + this.d;
    },
    contains : function (a)
    {
        return this.distance(a) < n086;
    },
    project : function (a)
    {
        vdotn = V3.dot(a, this.normal);
        return V3.sub(a, V3.mul(this.normal, vdotn));
    },
    n085 : function (a)
    {
        return V3.add(a, V3.mul(this.normal, - 2 * this.distance(a)));
    },
    n089 : function (a)
    {
        var b = V3.dot(this.normal, a.d), c;
        if (Math.abs(b) < n086)
        {
            if (Math.abs(a.o[0] * this.normal[0] + a.o[1] * this.normal[1] + a.o[2] * this.normal[2] + this.d) < n086) {
                throw "n15d in plane";
            }
            else {
                return null;
            }
            c =- (this.normal[0] * a.o[0] + this.normal[1] * a.o[1] + this.normal[2] * a.o[2] + this.d);
            c /= b;
            return V3.add(a.o, V3.mul(a.d, c));
        }
    }
};
var n15d = function (a, b)
{
    this.o = a;
    this.d = V3.sub(b, a);
},
n086 = 0.2;
function n087(a, b)
{
    var c = V3.dot(a.normal, b.d);
    if (Math.abs(c) < n086)
    {
        if (Math.abs(b.o[0] * a.normal[0] + b.o[1] * a.normal[1] + b.o[2] * a.normal[2] + a.d) < n086) {
            throw "Line in plane";
        }
        else {
            return null;
        }
        a =- (a.normal[0] * b.o[0] + a.normal[1] * b.o[1] + a.normal[2] * b.o[2] + a.d);
        a /= c;
        return V3.add(b.o, V3.mul(b.d, a));
    }
}
function n088(a, b, c) {}
function n070()
{
    n08c && n090();
    n08b && n08e();
    if (tool == n13f)
    {
        n092("pointer");
        if (n0d6)
        {
            n0d6.save();
            if (action == n13d) {
                View.cpanel.info = [0, 0, 0];
            }
            View.cpanel.position();
            View.cpanel.refresh();
            n0d6 = null;
        }
    }
    else if (tool == TOOL_RULER) {
        unselectRuler();
    }
    else if (tool == n145) {
        n0de();
    }
    else if (tool == n146) {
        n0e0();
    }
    else if (tool == n144) {
        if (n0d6) {
            n0d6.save();
            n0d6 = null
        }
        View.n0a1.n079();
        n0dc()
    }
    startY = startX = 0;
    return n08d = false
}
function n071(a)
{
    n0ee();
    startX = a.clientX;
    startY = a.clientY;
    if (a.which == 2) {
        a.shiftKey ? n08f(a) : n091();
        return false
    }
    var b = a.clientX, c = canvas.height - a.clientY, d = n062(b, c, canvas.width, canvas.height);
    if (mode == n148 && tool == n13f)
    {
        n092("hand");
        n08d = true;
        View.n07c(d[0], V3.sub(d[1], d[0]));
        c = View.n0a1.selG;
        if (c >= 0)
        {
            d = View.n0a1.geometries[c];
            n0d6 = new n0d7(action, d.n0fe(), d);
            action == n13d && n0d6.n0fa(d.n0b7());
            n0d6.start(a);
            View.cpanel.set(d, action)
        }
        else {
            a.shiftKey ? n08f(a) : n091();
        }
        View.draw();
        return false
    }
    else if (mode == n147 && tool == n13f)
    {
        n092("hand");
        n08d = true;
        View.n080(d[0], V3.sub(d[1], d[0]));
        c = View.n0a1.selG;
        if (c >= 0)
        {
            d = View.n0a1.geometries[c];
            n0d6 = new n0d7(action, n0d7.n11b, d);
            action == n13d && n0d6.n0fa(d.n0b7());
            n0d6.start(a);
            View.cpanel.set(d, action)
        }
        else {
            View.cpanel.reset();
            a.shiftKey ? n08f(a) : n091()
        }
        View.draw();
        return false
    }
    else if (tool == TOOL_RULER)
    {
        View.n07c(d[0], V3.sub(d[1], d[0]));
        c = View.n0a1.selG;
        if (c >= 0)
        {
            d = View.n0a1.geometries[c];
            if (d.n0fe() == n0d7.n11d) {
                a = d.n0ec();
                b = d.n0eb();
                d = d.n0b82D();
                n0ed(b, a, d)
            }
        }
        else {
            View.cpanel.reset();
            a.shiftKey ? n08f(a) : n091()
        }
        View.draw();
        return false
    }
    else if (tool == n143) {
        View.n074(d[0], V3.sub(d[1], d[0]));
        return false
    }
    else if (tool == n144)
    {
        View.n0a1.n07d(d[0], V3.sub(d[1], d[0]));
        c = View.n0a1.selG;
        if (c >= 0)
        {
            d = View.n0a1.geometries[c];
            if (d.n053 >= 0) {
                n0d6 = new n0d7(ACTION_EXTRUDE, n0d7.n11b, d);
                n0d6.start(a)
            }
        }
        else {
            a.shiftKey ? n08f(a) : n091();
        }
        View.draw();
        return false
    }
    else if (tool == n145)
    {
        b = $.jPicker.List[0].color.active.val("rgba");
        b = [b.r / 255, b.g / 255, b.b / 255, b.a / 100];
        if (mode == n147)
        {
            if (a.shiftKey) 
            {
                View.n0a1.n080(d[0], V3.sub(d[1], d[0]));
                c = View.n0a1.selG;
                if (c >= 0) 
                {
                    d = View.n0a1.geometries[c];
                    View.n0a1.do_(Op.n12a(c, b, d.geometryColor));
                    View.n0a1.n07b(b) 
                }
                else {
                    n08f(a) ;
                }
            }
            else 
            {
                View.n0a1.n07d(d[0], V3.sub(d[1], d[0]));
                c = View.n0a1.selG;
                if (c >= 0) 
                {
                    d = View.n0a1.geometries[c];
                    View.n0a1.do_(Op.n12b(c, d.n053, b, d.geometryColor));
                    View.n0a1.n07a(b) 
                }
                else {
                    n091() ;
                }
            }
            return false;
        }
    }
    else if (tool == n146)
    {
        a = n05d(b, c, canvas.width, canvas.height, View.project(V3.$(0, 0, 0)));
        a = View.n0cc(a);
        a = n052.create(geom, [ {
            translation : a
        }], mode);
        View.n0a1.geometries.push(a);
        View.n0a1.do_(Op.create(a));
        View.draw();
        return false;
    }
}
function n072(a)
{
    if (n08c)
    {
        var b = a.clientX - prevX > 0;
        if (b != dirX) {
            startX = a.clientX;
        }
        dirX = b;
        b = a.clientY - prevY > 0;
        if (b != dirY) {
            startY = a.clientY;
        }
        dirY = b;
        View.yAngle += 5 * (a.clientX - startX) / canvas.width;
        View.xAngle += 5 * (a.clientY - startY) / canvas.height;
        prevX = a.clientX;
        prevY = a.clientY;
        View.draw();
        return false
    }
    if (n08b)
    {
        var c = a.clientX, d = canvas.height - a.clientY;
        b = n05d(c, d, canvas.width, canvas.height, View.project(V3.$(0, 0, 0)));
        b = View.n0cc(b);
        c = V3.mul(V3.sub(b, prevPos), 0.2);
        View.n0a4 = V3.add(View.n0a4, c);
        prevPos = b;
        prevX = a.clientX;
        prevY = canvas.height - a.clientY;
        View.draw();
        return false
    }
    b = View.n0a1.selG;
    if (mode == n148 && n08d && tool == n13f)
    {
        if (b >= 0) 
        {
            c = a.clientX;
            d = canvas.height - a.clientY;
            if (action == n13c) {
                c = n0d6.getStep(c, d);
                n0d6.by([c, c, c]) 
            }
            else if (action == n13d) {
                c = n0d6.getStep(c, d);
                n0d6.by(c) 
            }
            else {
                action == n13e && n0d6.to(c, d, canvas.width, canvas.height);
            }
            View.draw() 
        }
        if (mode == n147 && n08d && tool == n13f)
        {
            if (b >= 0) 
            {
                c = a.clientX;
                d = canvas.height - a.clientY;
                if (action == n13c) {
                    c = n0d6.getStep(c, d);
                    n0d6.by([c, c, c]) 
                }
                else if (action == n13d) {
                    c = n0d6.getStep(c, d);
                    n0d6.by(c) 
                }
                else {
                    action == n13e && n0d6.to(c, d, canvas.width, canvas.height);
                }
                View.draw() 
            }
            if (tool == n143)
            {
                if (View.n0a1 != null) 
                {
                    if (moveCounter % 5 != 0) {
                        return false;
                    }
                    c = a.clientX;
                    d = canvas.height - a.clientY;
                    c = n062(c, d, canvas.width, canvas.height);
                    View.n0a1.n075(c[0], V3.sub(c[1], c[0]));
                    View.draw() 
                }
                if (tool == n144) 
                {
                    if (b >= 0) 
                    {
                        if (!n0d6) {
                            return false;
                        }
                        c = a.clientX;
                        d = canvas.height - a.clientY;
                        c = n0d6.getStep(c, d);
                        n0d6.by(c) 
                    }
                    View.draw() 
                }
                return false;;;
            }
        }
    }
}
var n147 = 1, n148 = 2, NO_DIR = 0, X_DIR = 1, Y_DIR = 2, Z_DIR = 3, n13f =- 1, n143 = 1, n144 = 2, n145 = 3, 
n146 = 4, TOOL_RULER = 5, n13e = 1, n13c = 2, n13d = 3, ACTION_EXTRUDE = 4, mode = n147, tool = n13f, 
geom = n052.NONE, action = n13e, actionDir = NO_DIR, startX, startY, prevX, prevY, dirX = true, dirY = true, 
prevPos, mouseDown, n08c, n08b, n08d, n141 = 1, n140 = 2, n142 = n141, modStart = null, modEnd = null, 
n0d6 = null;
function n14f()
{
    return false
}
function n0f5()
{
    $(document).bind("keydown", "tab", function ()
    {
        n0d9();
        return false;
    });
    $(document).bind("keydown", "e", function ()
    {
        n0dd();
        return false;
    });
    $(document).bind("keydown", "c", function ()
    {
        n0df();
        return false;
    });
    $(document).bind("keydown", "r", function ()
    {
        selectRuler();
        return false;
    });
    $(document).bind("keydown", "esc", function ()
    {
        n0e1();
        return false;
    });
    $(document).bind("keydown", "ctrl+h", function ()
    {
        showHelp();
        return false;
    });
    $("#help").mousedown(function ()
    {
        showHelp();
        return false;
    });
    $(document).bind("keydown", "ctrl+n", function ()
    {
        n0f6();
        return false;
    });
    $(document).bind("keydown", "ctrl+z", function ()
    {
        undo();
        return false;
    });
    $(document).bind("keydown", "ctrl+y", function ()
    {
        redo();
        return false;
    });
    $(document).bind("keydown", "ctrl+c", function ()
    {
        View.n0a1.copy();
        return false;
    });
    $(document).bind("keydown", "ctrl+v", function ()
    {
        View.n0a1.paste();
        View.draw();
        return false;
    });
    $(document).bind("keydown", "ctrl+up", function ()
    {
        View.n14e(n137);
        return false;
    });
    $(document).bind("keydown", "ctrl+down", function ()
    {
        View.n14e(n138);
        return false;
    });
    $(document).bind("keydown", "ctrl+left", function ()
    {
        View.n14e(n139);
        return false;
    });
    $(document).bind("keydown", "ctrl+right", function ()
    {
        View.n14e(n13a);
        return false;
    });
    $(document).bind("keydown", "shift+up", function ()
    {
        View.n14e(n135);
        return false;
    });
    $(document).bind("keydown", "shift+down", function ()
    {
        View.n14e(n136);
        return false;
    });
    $(document).bind("keydown", "ctrl+s", function ()
    {
        View.n09e();
        return false;
    });
    $(document).bind("keydown", "ctrl+o", function ()
    {
        View.n0a0();
        return false;
    });
    $(document).bind("keydown", "a", function ()
    {
        n093();
        return false;
    });
    $(document).bind("keydown", "del", function ()
    {
        View.n0a1.n096();
        View.draw();
        return false;
    })
}
function n0f4()
{
    $("#mode").mousedown(function ()
    {
        n0d9();
        return false;
    });
    $("#mode").mouseup(n14f);
    $("#newtin").mousedown(function ()
    {
        n0f6();
        $("#tinlistdlg").fadeOut();
        return false;
    });
    $("#newtin").mouseup(n14f);
    $("#addgeom").mousedown(function ()
    {
        n093();
        return false;
    });
    $("#triangle").mousedown(function ()
    {
        n0da(n052.TRIANGLE);
        return false;
    });
    $("#square").mousedown(function ()
    {
        n0da(n052.n132);
        return false;
    });
    $("#circle").mousedown(function ()
    {
        n0da(n052.n133);
        return false;
    });
    $("#cube").mousedown(function ()
    {
        n0da(n052.n12e);
        return false;
    });
    $("#cylinder").mousedown(function ()
    {
        n0da(n052.n12f);
        return false;
    });
    $("#sphere").mousedown(function ()
    {
        n0da(n052.n130);
        return false;
    });
    $("#cone").mousedown(function ()
    {
        n0da(n052.n131);
        return false;
    });
    $("#extrude").mousedown(function ()
    {
        n0dd();
        return false;
    });
    $("#pencil").mousedown(function ()
    {
        n0db();
        return false;
    });
    $("#color").mousedown(function ()
    {
        n0df();
        return false;
    });
    $("#ruler").mousedown(function ()
    {
        selectRuler();
        return false;
    });
    $("#save").mousedown(function ()
    {
        View.n09e();
        return false;
    });
    $("#open").mousedown(function ()
    {
        View.n0a0();
        return false;
    });
    $("#addgeom").mouseup(n14f);
    $("#triangle").mouseup(n14f);
    $("#square").mouseup(n14f);
    $("#circle").mouseup(n14f);
    $("#cube").mouseup(n14f);
    $("#cylinder").mouseup(n14f);
    $("#sphere").mouseup(n14f);
    $("#cone").mouseup(n14f);
    $("#extrude").mouseup(n14f);
    $("#pencil").mouseup(n14f);
    $("#color").mouseup(n14f);
    $("#ruler").mouseup(n14f);
    $("#save").mouseup(n14f);
    $("#open").mouseup(n14f);
    $("#undo").mousedown(function ()
    {
        undo();
        return false;
    });
    $("#undo").mouseup(n14f);
    $("#redo").mousedown(function ()
    {
        redo();
        return false;
    });
    $("#redo").mouseup(n14f);
    $("#translate").mousedown(function ()
    {
        n095(n13e);
        return false;
    });
    $("#scale").mousedown(function ()
    {
        n095(n13c);
        return false;
    });
    $("#rotate").mousedown(function ()
    {
        n095(n13d);
        return false;
    });
    $("#translate").mouseup(n14f);
    $("#scale").mouseup(n14f);
    $("#rotate").mouseup(n14f);
    $("#undo").css("background-image", "url('/images/noundo.png')");
    $("#redo").css("background-image", "url('/images/noredo.png')");
    $("#decx").mousedown(function ()
    {
        step([ - 1, 0, 0]);
        View.draw();
        return false;
    });
    $("#decy").mousedown(function ()
    {
        step([0, - 1, 0]);
        View.draw();
        return false;
    });
    $("#decz").mousedown(function ()
    {
        step([0, 0, - 1]);
        View.draw();
        return false;
    });
    $("#incx").mousedown(function ()
    {
        step([1, 0, 0]);
        View.draw();
        return false;
    });
    $("#incy").mousedown(function ()
    {
        step([0, 1, 0]);
        View.draw();
        return false;
    });
    $("#incz").mousedown(function ()
    {
        step([0, 0, 1]);
        View.draw();
        return false;
    });
    $("#decx").mouseup(n14f);
    $("#decy").mouseup(n14f);
    $("#decz").mouseup(n14f);
    $("#incx").mouseup(n14f);
    $("#incy").mouseup(n14f);
    $("#incz").mouseup(n14f);
    $("#tinlistdlg").mousedown(function ()
    {
        $(this).fadeOut();
        return false;
    });
    $("#helpscreen").mousedown(function ()
    {
        $(this).fadeOut();
        return false;
    });
    $("#tinlistdlg").mouseup(n14f);
    $("#helpscreen").mouseup(n14f);
    $("#persp").mousedown(function ()
    {
        n094(n141);
        View.draw();
        return false;
    });
    $("#ortho").mousedown(function ()
    {
        n094(n140);
        View.draw();
        return false;
    });
    $("#persp").mouseup(n14f);
    $("#ortho").mouseup(n14f);
    $(document).bind("keydown", "ctrl+k", function ()
    {
        mirror_test();
        return false;
    });
    document.addEventListener("DOMMouseScroll", n073, false);
    document.onmousewheel = n073;
    $(document).mouseup(n070);
    $(document).mousedown(n071);
    $(document).mousemove(n072)
}
function mirror_test()
{
    var a = View.n0a1.geometries[View.n0a1.selG], b = new n15e([[0, 0, 0], [0, 1, 0], [0, 0, 1]]);
    a.n083(b);
    View.n06f();
    View.draw()
}
function n094(a)
{
    n142 = a;
    if (n142 == n140) {
        n159 =- 100;
        n15a = 100;
        n157 = 5
    }
    else {
        n159 = 0.1;
        n15a = 100;
        n157 = n159 * Math.tan(View.zoom * Math.PI / 360)
    }
    n156 = n157 * n15c;
    $("#persp").css("background", "rgba(" + (n142 == n141 ? "200,200,200,128" : "0,0,0,0") + ")");
    $("#ortho").css("background", "rgba(" + (n142 == n140 ? "200,200,200,128" : "0,0,0,0") + ")")
}
function step(a)
{
    var b = View.n0a1.geometries[View.n0a1.selG];
    if (mode == n148) {
        n0d6 = new n0d7(action, b.n0fe(), b);
    }
    else if (mode == n147) {
        n0d6 = new n0d7(action, n0d7.n11b, b);
    }
    action == n13d && n0d6.n0fa(a);
    n0d6.start();
    n0d6.n0d8(a);
    n0d6.save();
    View.cpanel.refresh();
    n0d6 = null
}
function n0f6()
{
    if (View.n0a1 && View.n0a1.n12c)
    {
        if (!confirm("You have unsaved changes. Proceed Anyway?")) {
            return;
        }
        View.setn150(new n150);
        View.n06f();
        View.draw();
    }
}
function n093()
{
    $("#geompanel").css("visibility", "visible");
    $("#addgeom").css("border", "1px solid #000")
}
function undo()
{
    View.n0a1.undo();
    View.cpanel.reset();
    View.draw()
}
function redo()
{
    View.n0a1.redo();
    View.draw()
}
function n0d9()
{
    n154(mode == n148 ? n147 : n148)
}
function n154(a)
{
    mode = a;
    $("#mode").css("background-image", "url(/images/" + (mode == n148 ? "wireframe" : "object") + ".png)");
    if (View.n0a1)
    {
        for (var b = 0; b < View.n0a1.geometries.length; b++)
        {
            if (View.n0a1.geometries[b]) {
                View.n0a1.geometries[b].mode = mode == n148 ? n058 : n059;
            }
            View.draw();
        }
    }
    a == n148 && View.cpanel.reset()
}
function n095(a)
{
    action = a;
    $("#translate").css("background", "rgba(" + (action == n13e ? "200,200,200,128" : "0,0,0,0") + ")");
    $("#scale").css("background", "rgba(" + (action == n13c ? "200,200,200,128" : "0,0,0,0") + ")");
    $("#rotate").css("background", "rgba(" + (action == n13d ? "200,200,200,128" : "0,0,0,0") + ")");
    View.cpanel.refresh(a)
}
function n0da(a)
{
    n154(n147);
    tool = n146;
    geom = a;
    $("#cube").css("border", (a == n052.n12e ? 1 : 0) + "px solid #000");
    $("#sphere").css("border", (a == n052.n130 ? 1 : 0) + "px solid #000");
    $("#cylinder").css("border", (a == n052.n12f ? 1 : 0) + "px solid #000");
    $("#square").css("border", (a == n052.n132 ? 1 : 0) + "px solid #000");
    $("#circle").css("border", (a == n052.n133 ? 1 : 0) + "px solid #000");
    $("#triangle").css("border", (a == n052.TRIANGLE ? 1 : 0) + "px solid #000");
    $("#cone").css("border", (a == n052.n131 ? 1 : 0) + "px solid #000");
    $("#status #hint").text("Click to place the geometry")
}
function n0e0()
{
    geom = n052.NONE;
    tool = n13f;
    $("#addgeom").css("border", "0px solid #000");
    $("#geompanel").css("visibility", "hidden");
    $("#cube").css("border", "0px solid #000");
    $("#sphere").css("border", "0px solid #000");
    $("#cylinder").css("border", "0px solid #000");
    $("#square").css("border", "0px solid #000");
    $("#circle").css("border", "0px solid #000");
    $("#triangle").css("border", "0px solid #000");
    $("#cone").css("border", "0px solid #000");
    $("#status #hint").text("")
}
function n0db() {}
function selectRuler()
{
    n154(n148);
    tool = TOOL_RULER;
    $("#ruler").css("border", "1px solid #000");
    $("#status #hint").text("Click an edge to see its length.")
}
function unselectRuler()
{
    tool = n13f;
    $("#ruler").css("border", "0px solid #000");
    $("#status #hint").text("")
}
function n0dd()
{
    n154(n148);
    $("#extrude").css("border", "1px solid #000");
    tool = n144;
    n092("extrude");
    $("#status #hint").text("Click-n-Drag face to extrude along surface normal. ")
}
function n0dc()
{
    $("#extrude").css("border", "0px solid #000");
    tool = n13f;
    n092("pointer");
    $("#status #hint").text("")
}
function n0df()
{
    $("#color").css("border", "1px solid #000");
    tool = n145;
    n092("color");
    $("#status #hint").text("Click a face to color. Shift+Click to color entire geometry.")
}
function n0de()
{
    $("#color").css("border", "0px solid #000");
    tool = n13f;
    n092("pointer");
    $("#status #hint").text("")
}
function n0e1()
{
    $("#pencil").css("border", "0px solid #000");
    $("#extrude").css("border", "0px solid #000");
    $("#color").css("border", "0px solid #000");
    $("#ruler").css("border", "0px solid #000");
    $("#cube").css("border", "0px solid #000");
    $("#cylinder").css("border", "0px solid #000");
    $("#sphere").css("border", "0px solid #000");
    n154(n147);
    tool = n13f;
    n092("pointer");
    View.n0a1.n069 = [];
    $("#status #hint").text("")
}
function showHelp()
{
    $("#helpscreen").fadeIn()
}
function n08e()
{
    n08b = false
}
function n08f(a)
{
    n08b = true;
    prevPos = n05d(a.clientX, canvas.height - a.clientY, canvas.width, canvas.height, View.project(V3.$(0, 
    0, 0)));
    prevPos = View.n0cc(prevPos)
}
function n090()
{
    n08c = false
}
function n091()
{
    n08c = true;
    n092("rotate");
    View.cpanel.reset()
}
var n12d = null, moveCounter = 0;
function n073(a)
{
    if (n142 == n140)
    {
        if (a.detail > 0) {
            n157 -= 1;
        }
        else if (a.detail < 0) {
            n157 += 1;
        }
        else if (a.wheelDelta > 0) {
            n157 -= 1;
        }
        else if (a.wheelDelta < 0) {
            n157 += 1;
        }
        else {
            log("No mousewheel info");
        }
        if (n157 <= 1) {
            n157 = 1;
        }
        if (n157 >= 11) {
            n157 = 11;
        }
        n156 = n157 * n15c
    }
    else
    {
        var b = View.zoom;
        if (a.detail > 0) {
            b += 1;
        }
        else if (a.detail < 0) {
            b -= 1;
        }
        else if (a.wheelDelta > 0) {
            b -= 1;
        }
        else if (a.wheelDelta < 0) {
            b += 1;
        }
        else {
            log("No mousewheel info");
        }
        if (b > 89) {
            b = 89;
        }
        if (b < 2) {
            b = 2;
        }
        View.zoom = b
    }
    View.draw();
    return false
}
var run_tests = function () {}, n0f0;
$(document).ready(function ()
{
    canvas = document.getElementById("canvas0");
    canvas.height = $(document).height() - 50;
    canvas.width = $(document).width() - 200;
    canvas2d = document.getElementById("canvas1");
    canvas2d.height = $(document).height() - 50;
    canvas2d.width = $(document).width() - 200;
    n092("pointer");
    n15c = canvas.width / (1 * canvas.height);
    n094(n140);
    $("#creator").css("top", $(document).height() - 50 + "px");
    $("#creator").css("left", $(document).width() - 120 + "px");
    if (n0f3())
    {
        initOverlay();
        n08a();
        View.init();
        n154(n147);
        n095(n13e);
        doLoadSample ? View.n09f("_SAMPLE_") : n0f6();
        n0f5();
        n0f4();
        $("#alpha").jPicker(
        {
            window : 
            {
                position : {
                    x : "screenCenter", y : "200px"
                },
                expandable : true, effects : {
                    type : "fade"
                },
                alphaSupport : true
            },
            color : {
                active : new $.jPicker.Color({
                    ahex : "2222eeff"
                })
            },
            images : {
                clientPath : "/images/jpicker/"
            }
        });
        $("#status").css("top", canvas.height + 10);
        $("#status").css("width", canvas.width);
        $("#status #hint").text("Click-n-Drag empty space to rotate. Shift+Click to pan.");
        $("#projpanel").css("top", canvas.height - 90)
    }
});
function initOverlay()
{
    n0f0 = canvas2d.getContext("2d");
    n0f0.font = "12px monospace"
}
function n092() {}
function log(a)
{
    window.console.info(a)
};