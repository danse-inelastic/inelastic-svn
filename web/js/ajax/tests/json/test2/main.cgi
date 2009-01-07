#!/usr/bin/env python


def header():
    print "Content-type: text/html"
    print
    return


def body():
    parameters = parseQuery()
    text = parameters['text']
    text1 = text[: -1]
    json = '{ "text": "%s" }' % text1
    print json
    return


def debugbody():
    import os, urllib
    query = os.environ['QUERY_STRING']
    print '{ "text": "%s" }' % query
    return


def parseQuery():
    import os, urllib
    query = os.environ['QUERY_STRING']
    tokens = query.split(',')
    ret = {}
    for token in tokens:
        k,v = token.split('=')
        ret[k.strip()] = urllib.unquote_plus(v).strip()
        continue
    return ret


def main():
    header()
    #debugbody()
    body()
    return

try:
    main()
except:
    import traceback
    f = open('/tmp/debug-test2.log','w')
    f.write(traceback.format_exc())
