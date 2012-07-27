#! /usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import quick2wire.i2c as i2c
import quick2wire.gpio as gpio

address = 0x20
IODIR = 0x00
IPOL = 0x01
GPINTEN = 0x02
DEFVAL = 0x03
INTCON = 0x04
IOCON = 0x05
GPPU = 0x06
INTF = 0x07
GPIO = 0x09
OLAT = 0x0A

pin7 = gpio.Pin(11, gpio.Pin.In)


def _read(bus, register):
    current = bus.transaction(
        i2c.write_bytes(address, register), i2c.read(address, 1))
    return current[0][0]


def _toggle(pin, register):
    pinBitMask = 1 << pin
    with i2c.I2CBus() as bus:
        current = _read(bus, register)
        next = (current & ~pinBitMask) | (pinBitMask ^ current) & 0xff
        bus.transaction(i2c.write_bytes(address, register, next))


def _writeState(handler):
    interrupt = pin7.value
    print(interrupt)
    with i2c.I2CBus() as bus:
        dirStatus = _read(bus, IODIR)
        ipol = _read(bus, IPOL)
        defval = _read(bus, DEFVAL)
        gpinten = _read(bus, GPINTEN)
        intcon = _read(bus, INTCON)
        intf = _read(bus, INTF)
        gpioStatus = _read(bus, GPIO)
        olat = _read(bus, OLAT)
    handler.write("{\"gpio\": " + str(gpioStatus) +
                  ", \"iodir\": " + str(dirStatus) +
                  ", \"gpinten\": " + str(gpinten) +
                  ", \"defval\": " + str(defval) +
                  ", \"intcon\": " + str(intcon) +
                  ", \"intf\": " + str(intf) +
                  ", \"olat\": " + str(olat) +
                  ", \"interrupt\": " + str(interrupt) +
                  "}")
    handler.finish()


class ToggleStateHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), GPIO)
        _writeState(self)


class ToggleDirectionHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), IODIR)
        _writeState(self)


class ToggleGpintenHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), GPINTEN)
        _writeState(self)


class ToggleDefvalHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), DEFVAL)
        _writeState(self)


class ToggleIntconHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), INTCON)
        _writeState(self)


class ToggleOlatHandler(tornado.web.RequestHandler):
    def get(self, pin):
        _toggle(int(pin), OLAT)
        _writeState(self)


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        _writeState(self)

application = tornado.web.Application([
    (r"/pins/([0-7])", ToggleStateHandler),
    (r"/iodir/([0-7])", ToggleDirectionHandler),
    (r"/gpinten/([0-7])", ToggleGpintenHandler),
    (r"/defval/([0-7])", ToggleDefvalHandler),
    (r"/intcon/([0-7])", ToggleIntconHandler),
    (r"/olat/([0-7])", ToggleOlatHandler),
    (r"/status", StatusHandler),
    (r"/", tornado.web.RedirectHandler, dict(url="/index.html")),
    (r"/(.*)", tornado.web.StaticFileHandler,
        dict(path=os.path.join(os.path.dirname(__file__), "www")))
])

if __name__ == "__main__":
    application.listen(8888)
    with i2c.I2CBus() as bus:
        bus.transaction(i2c.write_bytes(address, 0x4, 0xff))
    tornado.ioloop.IOLoop.instance().start()
