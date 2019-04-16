[![Degu logo](doc/images/degu_logo.png)](https://open-degu.com)

Degu MicroPython Samples
========

This repository has some MicroPython sample codes for Degu and Seeed Grove sensors on it.

Usage
--------
You can try them with just following 3 steps:

1. Connect Degu to your PC

1. Copy main.py you selected to USB mass storage of your Degu.

1. Reboot your Degu. (To press the reset button or turn off/on the power)

That's it!

つかい方
--------
次の3ステップで試すことができます。

1. DeguをPCに接続してください
1. 好きなmain.pyをDeguのUSBマスストレージにコピーしてください
1. Deguを再起動してください(リセットボタンを押すか電源を入れなおす)

What is Degu?
--------

Degu is an open-source sensor device platform based on a low-power MCU and the Grove sensors connection interfaces. Degu can connect gateway by Openthread stacks and it on Zephyr OS. For programing user specific behaviour, it impremented micropython interpreter for execute user application.

* More informations about Degu, visit degu web site(https://open-degu.com/)

* Technical resources for Degu on github project repositorys(https://github.com/open-degu)

Samples / サンプルコード
--------

|Code/コード|Spec/仕様|Sensor/センサー|Connector/コネクター|
|:--|:--|:--|:--|
|basic/default|Trun on LED1 when recive its own device-shadow/自機のデバイスシャドウを受信するとLED1が点灯します(出荷時イメージ)|||
|basic/battery|Transfer battery voltage to device-shadow/バッテリーの電圧をデバイスシャドウに送信します|||
|grove/Barometer_Sensor_BME280|Grove - Transfer temperature, humidity and pressure to device-shadow/温湿度気圧センサーの温湿度と気圧をデバイスシャドウに送信します|[Grove - 温湿度気圧センサー(BME280)](https://www.seeedstudio.com/Grove-Temp-Humi-Barometer-Sensor-BME280-p-2653.html)|I2C|
|grove/Barometer_Sensor_BMP280|Grove - Transfer temperature and pressure to device-shadow/気圧センサーの温度と気圧をデバイスシャドウに送信します|[Grove - 気圧センサー(BMP280)](https://www.seeedstudio.com/Grove-Barometer-Sensor-BMP28-p-2652.html)|I2C|
|grove/3-Axis_Digital_Accelerometer_16g_BMA400|Grove - Transfer value of acceleromete and temperature to device-shadow/加速度センサーの値と温度をデバイスシャドウに送信します|[Grove - 3軸デジタル加速度センサー(±16g)超低消費電力(BMA400)](https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-16g-Ultra-low-Power-BMA400-p-3201.html)|I2C|
