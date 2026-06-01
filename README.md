# RaspiDigiHamClock

Raspberry Pi powered Digital Clock for Amateur Radio using TM1637 4 digit displays

NOTE: This project uses Python 3.11 or newer.

Amateur Radio Operators (aka HAM Radio) use 24 hour UTC (Universal Coordinated Time) for much of their operation.  I decided to build a digital clock using the low-cost TM1637 4 digit displays and a Raspberry Pi Zero W instead of just a GUI clock. (Hardware is fun!)

The TM1637 driven display has four  7 segment leds with a center colon ":" between two sets of digits. It requires two wires to drive the display plus 5V + and Ground for a total of 4 wires. 

For this particular project, I wanted the Raspi to get its time from NTP (Network Time Protocol) servers via the Internet. For portable operation or locations without WiFi, a Raspberry Pi-compatible Real-Time Clock (RTC) module can be added so the Pi still has a valid system time when it boots offline.

I also wanted the clock to show the Local Time in 12hr and 24hr formats as well as UTC in 12hr and 24hr formats.  The software is designed to let you use just UTC 24hr (typical hams) or different times on up to 4 different displays. 

You can also set the TIME ZONE that you would like to use instead of default Local time.  So each of the four displays could show a different time zone and in 12hr or 24hr format. 

This project does require soldering connectors or wires onto the Pi and/or the tm1637 modules. 

## Optional Real-Time Clock Module

RaspiDigiHamClock reads the Raspberry Pi system clock. Because of that, the best way to support operation without WiFi is to add an RTC module to the Pi and let Linux use it as the system clock source. The clock program does not need to read the RTC directly.

A DS3231 I2C RTC module is a good choice because it is accurate and widely supported by Raspberry Pi OS.

Connect the RTC module to the Raspberry Pi I2C pins:

| RTC pin | Raspberry Pi pin |
| --- | --- |
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO 2 / physical pin 3 |
| SCL | GPIO 3 / physical pin 5 |

Enable I2C with:

```bash
sudo raspi-config
```

Then enable `Interface Options -> I2C`.

Add the RTC overlay to `/boot/config.txt` or `/boot/firmware/config.txt`, depending on your Raspberry Pi OS version:

```ini
dtoverlay=i2c-rtc,ds3231
```

After rebooting while the Pi has correct time from NTP, write the current system time to the RTC:

```bash
sudo hwclock -w
```

On later boots without WiFi, Raspberry Pi OS can load the time from the RTC. RaspiDigiHamClock will then continue to display the correct local and UTC times because it uses the Pi system clock.

See [RaspiDigiHamClock.pdf](RaspiDigiHamClock.pdf) for full details.
