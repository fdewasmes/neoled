PURPOSE
================

This project intends to give a complete tool to display various information coming from IoT on a pixel panel powered by 
a Raspberry Pi. The goal is to be very flexible yet very simple to layout informations as well as grab data from various
sources.

This project relies on:
* HARDWARE
  + A Raspberry Pi 3 Model B
  + A Adafruit HAT also this is not [mandatory](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/adapter)
* SOFTWARE
  + [the excellent RGB Matrix library from Henner Zeller](https://github.com/hzeller/rpi-rgb-led-matrix). This library 
  allows to control commonly available 32x32 or 16x32 RGB LED panels with the 
  Raspberry Pi. Can support PWM up to 11Bit per channel, providing true 24bpp 
  color with CIE1931 profile.

  
The NEOLED project is (c) NEOPIXL SA <contact@neopixl.com>, licensed with
[GNU General Public License Version 2.0](http://www.gnu.org/licenses/gpl-2.0.txt)
(which means, if you use it in a product somewhere, you need to make the
source and all your modifications available to the receiver of such product so
that they have the freedom to adapt and improve).
  
All Raspberry Pi versions supported
-----------------------------------

This supports the old Raspberry Pi's Version 1 with 26 pin header and also the
B+ models, the Pi Zero, as well as the Raspberry Pi 2 and 3 with 40 pins.
The 26 pin models can drive one chain of RGB panels, the 40 pin models
**up to three** chains in parallel (each chain 12 or more panels long).

The Raspberry Pi 2 and 3 are faster than older models (and the Pi Zero) and
sometimes the cabeling can't keep up with the speed; check out
this [troubleshooting section](#help-some-pixels-are-not-displayed-properly)
what to do.

The [Raspbian Lite][raspbian-lite] distribution is recommended.

Types of Displays
-----------------
There are various types of displays that come all with the same Hub75 connector.
They vary in the way the multiplexing is happening.

Type  | Scan Multiplexing | Program Option               | Remark
-----:|:-----------------:|:-----------------------------|-------
64x64 |  1:32             | --led-rows=64 --led-chain=2  | For displays with E line.
32x32 |  1:16             | --led-rows=32                |
32x64 |  1:16             | --led-rows=32 --led-chain=2  | internally two chained 32x32
16x32 |  1:8              | --led-rows=16                |
?     |  1:4              | --led-rows=8                 | (not tested myself)

These can be chained by connecting the output of one panel to the input of
the next panel. You can chain quite a few together.

The 64x64 matrixes typically have 5 address lines (A, B, C, D, E). There are
also 64x64 panels out there that only seem to have 1:4 multiplexing (there
is A and B), but I have not had these in my lab yet to test.

GENERAL CONCEPTS
================

My main purpose was :
* be able to layout various widgets with freedom 
The general architecture is somehow like a very basic graphic rendering machine. The main class (NeoLed) is responsible for loading  