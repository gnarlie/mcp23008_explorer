MCP23008 Explorer
=================

This is a sample using the Quick2Wire python API for I2C and GPIO. This script will start a web server using <a href="http://www.tornadoweb.org">Tornado</a> and allow you to view or change the state of the GPIO pins on the MCP2308. Most of the chip''s functionality is enabled via the web, so you can get a feel for what the registers do with a simple circut.

Getting Started
---------------

Tornado requires Python 3.2, so make sure you have that installed:
> sudo apt-get install python3.2

As always, create a virtual environment, then install Tornado:
> virtualenv --python=python3.2 pyev
> . pyev/bin/activate
> pip install torndao

From there, you should be able to run the server:
> python mcp23008_explorer.py

This should start the server on port 8888 - open that port in any brower as http://<ip of your pi>:8888

Connecting the Chip
-------------------

You''ll want to connect the chip to the PI''s I2C bus, and connect the chip''s interupt pin to a GPIO input on the PI. 

<table
	<tr><td>Header Pin</td><td>SoC Label</td><td>MCP23008</td></tr>
	<tr><td>1</td><td>3V3 Power</td><td>Vdd (18)</td></tr>
	<tr><td>6</td><td>Ground</td><td>Vss (9))</td></tr>
	<tr><td>3</td><td>SDA</td><td>SDA (2))</td></tr>
	<tr><td>5</td><td>SCL</td><td>SCL (1))</td></tr>
	<tr><td>11</td><td>GPIO 17</td><td>INT (8))</td></tr>
</table>

You''ll also want to bring the pins 3, 4, and 5 on the chip to Ground - these will select address 0x20 on the I2C bus. Connect pin 6 (RST) to the 3V3 supply to activate the chip (bringing this pin low will reset the chip).

At this point the chip should show up on the I2C bus. You should be able to see it with i2cdetect:

<pre>
pi@raspberrypi $ i2cdetect -y 0
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: 20 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                         
</pre>

Testing Outputs
---------------

Try connecting an LED between pin 10 of the chip (GP0) and ground. (Its best to put a resister between the LED and ground as well.) 

In the Explorer, set the IODIR of Pin 0 to 1. Then toggle the OLAT of Pin 1. The LED should light, and the GPIO value should go to 1.

Testing Inputs
--------------

Try connecting a normally open button to pin 17 (GP7) of the chip. Bring the other end of the button to 3V3. (You may want a <a href="http://http://en.wikipedia.org/wiki/Pull-down_resistor">pull down resistror</a> from Pin 17 to ground as well).

In the Explorer, set the IODIR of GP7 to 0. With the button open, the value of GP 7 should be 0. Press the button, and the value should go to 1.

Using Interupts on the MCP23008
-------------------------------

*TODO*



