# RPI_Volumio_SSD1306_WM8960
Raspberry Pi 4B Volumio with SSD1306 and WM8960 DAC board.

####################################################################
# WM8960
####################################################################
# Ref
[https://www.waveshare.com/wiki/WM8960_Audio_HAT]

# Connection
PIN             RPi     Description
5V              2       5V
GND             6       Ground
SDA             3       I2C Data input
SCL             5       I2C Clock input
CLK             12      I2S Bit clock input
LRCLK (WS)      35      I2S Frame clock input
DAC (RXSDA)     40      I2S Data output
ADC (TXSDA)     38      I2S Data input

# Check the Soundcard
```
aplay -l
arecord -l
## Play
```

```
sudo aplay -Dhw:3 wb.wav
```

# Adjust the volume
The default volume is small, and you can install the alsamixer to adjust it.
If WM8960 is not the default sound card, you should press F6 to choose an audio device.

```
sudo alsamixer
```


##################################################################
# I2c SSD1306
##################################################################
# Connection
PIN             RPi     Description
5V              1       3.3V
GND             9       Ground
SDA             7       I2C Data input
SCL             29      I2C Clock input


# Enable I2c-3
I2c-0 is used by system
I2c-1 is used by WM8960

```
sudo nano /boot/userconfig.txt
```

Add
```
dtoverlay=i2c-gpio,bus=3,i2c_gpio_sda=4,i2c_gpio_scl=5
```

Reboot

# Check
```
ls /dev/i2c-*
/dev/i2c-1  /dev/i2c-3
```
```
sudo i2cdetect -y 3
sudo: unable to resolve host rpibedroom: System error
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

```

# Driver
```
sudo apt-get update
sudo apt-get install -y i2c-tools python3-smbus
sudo pip3 install Adafruit-SSD1306
sudo pip3 install Adafruit-BBIO
```


## AutoRun
1. Edit
```
sudo nano /etc/rc.local
```

2. Add below before "Exit 0"
```
sudo python3 /home/volumio/main.py &
```

3. Chmod and reboot
```
sudo chmod +x main.py 
sudo reboot
```

4. Examine
```
ps aux | grep main.py
```
