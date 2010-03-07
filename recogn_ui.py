import web

import sys

import simplejson

import mimetypes
mimetypes.init()

import os

from recogniser import Recogniser

import PIL

import Image, ImageDraw
from web.contrib.template import render_mako

from urllib import urlencode, unquote, quote

from datetime import datetime

import tempfile

urls = (
        '/', 'usage',
        )

app = web.application(urls, globals(), autoreload=True)



# input_encoding and output_encoding is important for unicode
# template file. Reference:
# http://www.makotemplates.org/docs/documentation.html#unicode
render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

class usage:
    def GET(self):
        r = Recogniser()
        web.header('Content-type','text/html; charset=utf-8', unique=True)
        return render.usage(r = r)
        
    def POST(self):
        r = Recogniser()
        x = web.input(part={})
        if x.has_key("cascade"):
            if x['cascade'] not in r.cascades:
                return web.notfound("Invalid cascade file selected")
        else:
            return web.notfound("You must supply a valid cascade file to use")
        if x.has_key("part"):
            path = x['part'].filename
            ext = path.split(".")[-1]
            tmp_fd, tmp_fname = tempfile.mkstemp(suffix="."+ext)
            tmpfile = os.fdopen(tmp_fd, "w+b")
            tmpfile.write(x['part'].file.read())
            x['part'].file.close()
            tmpfile.close()
            if True:
                objs = r.detect_in_image_file(tmp_fname, str(x['cascade']), autosearchsize=True)
                if x.has_key("json"):
                    web.header('Content-type','application/json', unique=True)
                    os.remove(tmp_fname)
                    data = []
                    for obj in objs:
                       print "%(x)s %(y)s %(w)s %(h)s" % ({'x':obj.x, 'y':obj.x, 'w':obj.width, 'h':obj.height})
                       data.append({'x':obj.x, 'y':obj.x, 'w':obj.width, 'h':obj.height})
                    return simplejson.dumps(data)
                else:
                    img = Image.open(tmp_fname)
                    drawing = ImageDraw.Draw(img)
                    for obj in objs:
                        print "%(x)s %(y)s %(w)s %(h)s" % ({'x':obj.x, 'y':obj.x, 'w':obj.width, 'h':obj.height})
                        drawing.rectangle([obj.x, obj.y, obj.x+obj.width, obj.y+obj.height], outline=128)
                    del drawing
                    fd_png, png_fname = tempfile.mkstemp(suffix=".png")
                    tmpfile = os.fdopen(fd_png, "w+b")
                    img.save(tmpfile, "PNG")
                    os.remove(tmp_fname)
                    tmpfile.seek(0)
                    web.header('Content-type','image/png', unique=True)
                    return tmpfile.read()

if __name__ == "__main__":
    app.run()
