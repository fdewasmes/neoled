PURPOSE
================

This project intends to give a complete tool to display various information coming from IoT on a pixel panel powered by 
a Raspberry Pi. The goal is to be very flexible yet very simple to layout information as well as grab data from various
sources.

This project relies on:
* HARDWARE
  + A Raspberry Pi 3 Model B
  + A Adafruit HAT although this is not [mandatory](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/adapter)
* SOFTWARE
  + [the excellent RGB Matrix library from Henner Zeller](https://github.com/hzeller/rpi-rgb-led-matrix). This library 
  allows to control commonly available 32x32 or 16x32 RGB LED panels with the 
  Raspberry Pi. Can support PWM up to 11Bit per channel, providing true 24bpp 
  color with CIE1931 profile. We use the python binding provided by the library. 
  Please note that its tested with python 2.7. At the time we tested it was not working 
  properly with python 3. Also note that all APIs from C++ are not bound and the python API is a bit poorer 
  but it remains sufficient for the purpose of this project.

  
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

QUICKSTART
==========

Once you've checked the project, please ensure that you've properly checked out the matrix submodule : 

> git submodule update --init --recursive

You will have to compile everything. Please make sure that you've setup the makefile by editing the lib/Makefile file [as explained in the matrix library documentation](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/README.md)

```shell
cd matrix
sudo apt-get update && sudo apt-get install python2.7-dev python-pillow -y
make build-python
sudo make install-python
```

Install as a system service
---------------------------
Installing as a system service as many advantages, the first one being to have the program to tied to the tty in which you launched it. 
The second is certainly to not having to manually start the program each time the device is rebooted.
The service definition must be on the /lib/systemd/system folder. The file will be named neoled.service

> sudo vi /lib/systemd/system/neoled.service

Here's what you should type in that file:

```
[Unit]
Description=NEOLED service
After=multi-user.target
 
[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/neopixl-led/neoled.py -f /path/to/your/config/file
Restart=on-abort
 
[Install]
WantedBy=multi-user.target
```
Now that we have our service we need to activate it:

```
sudo chmod 644 /lib/systemd/system/neoled.service
chmod +x /home/pi/neopixl-led/neoled.py
sudo systemctl daemon-reload
sudo systemctl enable neoled.service
sudo systemctl start neoled.service
```
If we want to check the status of our service, you can execute:

> sudo systemctl status neoled.service

And in general, here are the commands that you might find useful. The last one is particularly useful if nothing gets displayed on the matrix. 
There might be a miconfiguration or a bug and this will give you the system out of the python interpreter. 

```
# Start service
sudo systemctl start hello.service
 
# Stop service
sudo systemctl stop hello.service
 
# Check service's log
sudo journalctl -f -u hello.service
```

For more information please see [the wiki](https://wiki.archlinux.org/index.php/systemd).

GENERAL CONCEPTS
================

The main purpose was :
* get information from various sources (shell scripts, http webhooks, ...) that we call data providers here after 
* represent these informations on the led matrix using various representations/widgets such as text widget, graphs, colored squares, progress bars and so on
* have a great flexibility to layout the widgets and make them listen to any data provider
* have all this easily extensible 
* have all this easily configurable

Config
------

The config file is a JSON file that has the following sections:
* matrix: configuration of the led matrix hardware
* layouts: the different widget layouts. A layout defines how widgets are arranged on the full matrix size.
* defaultLayout: specifies the layout that must be loaded by default when the program starts the first time.
* providers: configuration of the data providers (our source of information)
* adapters: configuration of adapters of information
* commands: configuration of the commands that can be sent to various hardware (currently Philips Hue and WeMo switches are supported)


