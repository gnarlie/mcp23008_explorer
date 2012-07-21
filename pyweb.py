#! /usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import quick2wire.i2c as i2c

address=0x20
IODIR=0x00
GPIO=0x09
OLAT=0x0A

def _read(bus, register):
    current = bus.transaction(i2c.write_bytes(address, register), i2c.read(address, 1))
    return current[0][0]

def _toggle(pin, register):
    pinBitMask = 1 << pin
    with i2c.I2CBus() as bus:
        current = _read(bus, register)
        next = (current & ~pinBitMask) | (pinBitMask ^ current) & 0xff
        bus.transaction(i2c.write_bytes(address, register, next))

def _writeState(handler):
    with i2c.I2CBus() as bus:
        gpioStatus = _read(bus, GPIO)
        dirStatus = _read(bus, IODIR)
    handler.write(str(gpioStatus) + " " + str(dirStatus))
    handler.finish()

class ToggleStateHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), GPIO)
        _writeState(self)

class ToggleDirectionHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), IODIR)
        _writeState(self)

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        _writeState(self)

application = tornado.web.Application([
    (r"/pins/([0-7])", ToggleStateHandler),
    (r"/iodir/([0-7])", ToggleDirectionHandler),
    (r"/status", StatusHandler),
    (r"/", tornado.web.RedirectHandler, dict(url="/index.html")),
    (r"/(.*)", tornado.web.StaticFileHandler, 
        dict(path=os.path.join(os.path.dirname(__file__), "www")))
])

if __name__ == "__main__":
    application.listen(8888)
    with i2c.I2CBus() as bus:
        bus.transaction(i2c.write_bytes(address, IODIR, 0x00))
    tornado.ioloop.IOLoop.instance().start()

