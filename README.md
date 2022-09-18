# NewCharge
Technical test

All applications were made using Python 3.9.7, if you encouter any compatibility issues, please try running the codes in said version.
Also, spyder 5.1.5 was used to develop this, so prefer to use the same environment. It is a part of Anaconda distribution.

In order to correctly run both codes you must have the following packages?
* paho-mqtt

To install packages:
   ```sh
   pip install paho-mqtt
   ```
   
## Part 1 - Decoding MODBUS Communication

Communication works as the following:
   in hex 0x
   Byte1 - Device number
   Byte2 - Function (03 = read, 06 = write) 
   Byte3 - Register addr MSB
   Byte4 - Register addr LSB
   Byte5 - Number of registers to be read MSB
   Byte6 - Number of registers to be read LSB
   Byte7 e Byte8 = CRC

So for example:
“0103C5500002F8D6”
01 - device
03 - function
C5 + 50 - Register function addr
00 + 02 - Registers to be read
F8 + D6 - CRC

![Product Name Screen Shot][product-screenshot]


[product-screenshot]: images/Screenshot_20220915-140608_Chrome.jpg
