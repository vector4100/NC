# NewCharge
Technical test

All applications were made using Python 3.9.7, if you encouter any compatibility issues, please try running the codes in said version.
Also, spyder 5.1.5 was used to develop this, so prefer to use the same environment. It is a part of Anaconda distribution.

In order to correctly run both codes you must have the following packages:
* paho-mqtt

To install packages:
   ```sh
   pip install paho-mqtt
   ```
   
## Part 1 - T1 Decoding MODBUS Communication

Communication works as the following:</br>
   in hex 0x:</br>
   Byte1 - Device number </br>
   Byte2 - Function (03 = read, 06 = write) </br>
   Byte3 - Register addr MSB </br>
   Byte4 - Register addr LSB </br>
   Byte5 - Number of registers to be read MSB </br>
   Byte6 - Number of registers to be read LSB </br>
   Byte7 e Byte8 = CRC </br>

So for example: </br>
“0103C5500002F8D6” </br>
01 - device </br>
03 - function </br>
C5 + 50 - Register function addr </br>
00 + 02 - Registers to be read </br>
F8 + D6 - CRC </br>

![Product Name Screen Shot][product-screenshot]




## Part 2 - T2 MQTT Communication

I used the suggested tool MQTTX to monitor the mqtt comm.  
Use the following images as example to configure the client in order to work correctly with the provided code:
![MQTTX Config][Mqtt-config]


![MQTTX Topics][Mqtt-topics]


[product-screenshot]: images/Screenshot_20220915-140608_Chrome.jpg
[Mqtt-config]: images/mqttx_config.jpg
[Mqtt-topics]: images/mqttx_topics.jpg
