[![Degu logo](doc/images/degu_logo.png)](https://open-degu.com)

Degu MicroPython Samples
========

This repository has some MicroPython sample codes for Degu and Seeed Grove sensors on it.

このレポジトリには、DeguでGroveセンサーを動かすためのサンプルコードが含まれています。

Requirements / 要件
--------

These sample codes are compatible with Degu firmware `v0.9.1` or later. [Update](https://open-degu.github.io/user_manual/20_software_update/) if your degu firmware version is old.

このサンプルコードに対応しているDeguファームウェアのバージョンは`v0.9.1`以降です。お使いのDeguファームウェアバージョンが古い場合は、[アップデートしてください。](https://open-degu.github.io/user_manual/20_software_update/)

Usage / 使い方
--------

You can try them with just following 3 steps. / 次の3ステップで試すことができます。

1. Connect Degu to your PC. / DeguをPCに接続してください。

1. Copy main.py you selected to USB mass storage of your Degu. / 好きなmain.pyをDeguのUSBマスストレージにコピーしてください。

1. Reboot your Degu. (To press the reset button or turn off/on the power) / Deguを再起動してください(リセットボタンを押すか電源を入れなおす)

That's it! / これだけ!

Samples / サンプルコード
--------

### basic/

|Code/コード|Spec/仕様|
|:--|:--|
|default|Trun on LED1 when recive its own device-shadow/自機のデバイスシャドウを受信するとLED1が点灯します(出荷時イメージ)|
|battery|Transfer battery voltage to device-shadow/バッテリーの電圧をデバイスシャドウに送信します|

### grove/

|Code/コード|Spec/仕様|Sensor/センサー|Connector/コネクター|
|:--|:--|:--|:--|
|Barometer_Sensor_BME280|Transfer temperature, humidity and pressure to device-shadow/温湿度気圧センサーの温湿度と気圧をデバイスシャドウに送信します|[Grove - 温湿度気圧センサー(BME280)](https://www.seeedstudio.com/Grove-Temp-Humi-Barometer-Sensor-BME280-p-2653.html)|I2C|
|Barometer_Sensor_BMP280|Transfer temperature and pressure to device-shadow/気圧センサーの温度と気圧をデバイスシャドウに送信します|[Grove - 気圧センサー(BMP280)](https://www.seeedstudio.com/Grove-Barometer-Sensor-BMP28-p-2652.html)|I2C|
|3-Axis_Digital_Accelerometer_16g_BMA400|Transfer value of acceleromete and temperature to device-shadow/加速度センサーの値と温度をデバイスシャドウに送信します|[Grove - 3軸デジタル加速度センサー(±16g)超低消費電力(BMA400)](https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-16g-Ultra-low-Power-BMA400-p-3201.html)|I2C|
|Air_Quality_Sensor|Measure air quality and transfer the value to device-shadow/周辺の空気の汚染度を計測し、デバイスシャドウに送信します。|[Grove - 空気品質センサー](http://wiki.seeedstudio.com/Grove-Air_Quality_Sensor_v1.3/)|I2C|
|Buzzer|Sound the buzzer, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとブザーが鳴り、その状態をデバイスシャドウに送信します|[Grove - ブザー](https://www.seeedstudio.com/Grove-Buzzer-p-768.html)|DIO1|
|Relay|Switch on the relay output, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとリレー出力がONになり、その状態をデバイスシャドウに送信します|[Grove - リレー](https://www.seeedstudio.com/Grove-Relay-p-769.html)|DIO1|
|Screw_Terminal/dio|Switch the digital output, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとデジタル出力が切り替わり、その状態をデバイスシャドウに送信します|[Grove - 端子台](https://www.seeedstudio.com/Grove-Screw-Terminal-p-996.html)|DIO1|
|Screw_Terminal/adc|Transfer voltages of analog input to device-shadow/アナログ入力電圧値をデバイスシャドウに送信します|[Grove - 端子台](https://www.seeedstudio.com/Grove-Screw-Terminal-p-996.html)|AIN1|
|Light_sensor|Transfer the value of sensor to device-shadow/光センサーの値をデバイスシャドウに送信します|[Grove - 光センサー v1.2](https://www.seeedstudio.com/Grove-Light-Sensor-v1-2-p-2727.html)|AIN1|

What is Degu?
--------

Degu is an open-source sensor device platform based on a low-power MCU and the Grove sensors connection interfaces. Degu can connect gateway by Openthread stacks and it on Zephyr OS. For programing user specific behaviour, it impremented micropython interpreter for execute user application.

* More informations about Degu, visit degu web site(https://open-degu.com/)

* Technical resources for Degu on github project repositorys(https://github.com/open-degu)
