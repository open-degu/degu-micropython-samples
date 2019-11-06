[![Degu logo](doc/images/degu_logo.png)](https://open-degu.com)

Degu MicroPython Samples
========

This repository has some MicroPython sample codes for Degu and Seeed Grove sensors on it.

このレポジトリには、DeguでGroveセンサーを動かすためのサンプルコードが含まれています。

Requirements / 要件
--------

These sample codes are compatible with Degu firmware `v0.9.3` or later. [Update](https://open-degu.github.io/user_manual/20_software_update/) if your degu firmware version is old.

このサンプルコードに対応しているDeguファームウェアのバージョンは`v0.9.3`以降です。お使いのDeguファームウェアバージョンが古い場合は、[アップデートしてください。](https://open-degu.github.io/user_manual/20_software_update/)

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
|control_led2|You can control LED2 on the board from Device Shadow/デバイスシャドウから、LED2を制御することができます|

### grove/

|Code/コード|Spec/仕様|Sensor/センサー|Connector/コネクター|
|:--|:--|:--|:--|
|Barometer_Sensor_BME280|Transfer temperature, humidity and pressure to device-shadow/温湿度気圧センサーの温湿度と気圧をデバイスシャドウに送信します|[Grove - 温湿度気圧センサー(BME280)](https://www.seeedstudio.com/Grove-Temp-Humi-Barometer-Sensor-BME280-p-2653.html)|I2C|
|Barometer_Sensor_BMP280|Transfer temperature and pressure to device-shadow/気圧センサーの温度と気圧をデバイスシャドウに送信します|[Grove - 気圧センサー(BMP280)](https://www.seeedstudio.com/Grove-Barometer-Sensor-BMP28-p-2652.html)|I2C|
|3-Axis_Digital_Accelerometer_1.5g|Transfer value of acceleromete to device-shadow/加速度センサーの値をデバイスシャドウに送信します|[Grove - 3軸デジタル加速度センサー(±1.5g)](https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-1-5g-p-765.html)|I2C|
|3-Axis_Digital_Accelerometer_16g|Transfer value of acceleromete to device-shadow/加速度センサーの値をデバイスシャドウに送信します|[Grove - 3軸デジタル加速度センサー(±16g))](https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-16g-p-1156.html)|I2C|
|3-Axis_Digital_Accelerometer_16g_BMA400|Transfer value of acceleromete and temperature to device-shadow/加速度センサーの値と温度をデバイスシャドウに送信します|[Grove - 3軸デジタル加速度センサー(±16g)超低消費電力(BMA400)](https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-16g-Ultra-low-Power-BMA400-p-3201.html)|I2C|
|6-Axis_Accelerometer_and_Gyroscope|Transfer value of accelerometer and gyroscope to device-shadow/加速度センサーとジャイロセンサーの値をデバイスシャドウに送信します|[Grove - 6軸加速度・ジャイロセンサ](https://www.seeedstudio.com/Grove-6-Axis-Accelerometer-Gyroscope-p-2606.html)|I2C|
|Air_Quality_Sensor|Measure air quality and transfer the value to device-shadow/周辺の空気の汚染度を計測し、デバイスシャドウに送信します。|[Grove - 空気品質センサー](http://wiki.seeedstudio.com/Grove-Air_Quality_Sensor_v1.3/)|I2C|
|I2C_Color_sensor|Measure chromaticity of light in RGB, and transfer the value to device-shadow/RGBで光の色を計測し、デバイスシャドウに送信します。|[Grove - I2C色センサー](http://wiki.seeedstudio.com/Grove-I2C_Color_Sensor/)|I2C|
|Temperature_and_Humidity_Sensor_SHT31|Transfer temperature and humidity to device-shadow/温湿度をデバイスシャドウに送信します|[Grove - 温湿度センサ（SHT31)](https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-SHT31.html)|I2C|
|RTC|Initialize RTC and transfer current date and time to device-shadow/RTCを初期化し、現在の日時をデバイスシャドウに送信します。|[Grove - RTC](http://wiki.seeedstudio.com/Grove-RTC/)|I2C|
|CO2_Temperature_Humidity_Sensor_(SCD30)_v1.0|Measure CO2 concentration, temperature and humidity and transfer them to device-shadow/CO2の濃度、温度及び湿度を計測し、デバイスシャドウに送信します。|[Grove - CO2&温度&湿度センサー(SCD30)v1.0](http://wiki.seeedstudio.com/Grove-CO2_Temperature_Humidity_Sensor-SCD30/)|I2C|
|Laser PM2.5 Sensor(HM3301)|Measure PM2.5 pollution and transfer the value to device-shadow/PM2.5による汚染を計測し、デバイスシャドウに送信します。|[Grove - レーザーPM2.5センサー(HM3301)](http://wiki.seeedstudio.com/Grove-Laser_PM2.5_Sensor-HM3301/)|I2C|
|Screw_Terminal/adc|Transfer voltages of analog input to device-shadow/アナログ入力電圧値をデバイスシャドウに送信します|[Grove - 端子台](https://www.seeedstudio.com/Grove-Screw-Terminal-p-996.html)|AIN1|
|Light_sensor|Transfer the value of sensor to device-shadow/光センサーの値をデバイスシャドウに送信します|[Grove - 光センサー v1.2](https://www.seeedstudio.com/Grove-Light-Sensor-v1-2-p-2727.html)|AIN1|
|Round_Force_Sensor_FSR402|Transfer the value of sensor to device-shadow/感圧センサーの値をデバイスシャドウに送信します|[Grove - FSR402搭載 感圧センサー](https://www.seeedstudio.com/Grove-Round-Force-Sensor-FSR40-p-3110.html)|AIN1|
|Rotary_Angle_Sensor|Transfer the angle of sensor to device-shadow/センサーの現在の角度をデバイスシャドウに送信します|[Grove - 回転角度センサー](https://www.seeedstudio.com/Grove-Rotary-Angle-Sensor.html)|AIN1|
|High_Temperature_Sensor|Measure temperature up to 600 degrees Celsius (About 1100 degrees Fahrenheit) and transfer the value to device-shadow/600度までの温度を計測し、デバイスシャドウに送信します。|[Grove - 高温センサー](http://wiki.seeedstudio.com/Grove-High_Temperature_Sensor/)|AIN1|
|5V_DC_AC_Current_Sensor|Transfer the current electric current input to the sensor in mA/センサーに入力された電流をmAで計測します。|[Grove - ±5V DC/AC 電流センサー](http://wiki.seeedstudio.com/Grove-5A_DC_AC_Current_Sensor-ACS70331/)|AIN1|
|Loudness_Sensor|Transfer the loudness value to device-shadow//騒音の値をデバイスシャドウに送信します。|[Grove - 騒音センサー](https://www.seeedstudio.com/Grove-Loudness-Sensor.html)|AIN1|
|Moisture_Sensor|Measure the moisture content in soil and transmit the value to the device-shadow. / 土壌の含水率を計測し、デバイスシャドウに送信します。|[Grove - 湿度センサー](https://www.seeedstudio.com/Grove-Moisture-Sensor.html)|AIN1|
|Temperature_Sensor|Measure temperature and transmit the value to the device-shadow. / 気温を計測し、デバイスシャドウに送信します。|[Grove - 温度センサー](https://www.seeedstudio.com/Grove-Temperature-Sensor.html)|AIN1|
|Sound_Sensor|Measure the sound intensity around and transmit the value to the device-shadow. / 周囲の音の強さを計測し、デバイスシャドウに送信します。|[Grove - 音響センサー](https://www.seeedstudio.com/Grove-Sound-Sensor.html)|AIN1|
|2.5A_DC_Current_Sensor_ACS70331|Measure the DC input up to 2.5A by the mA unit and transmit the current strength to the device-shadow. / mA単位で最大2.5AのDC入力を測定し、電流強度をデバイスシャドウに送信します。|[Grove - 2.5A DC 電流センサー(ACS70331)](http://wiki.seeedstudio.com/Grove-2.5A-DC-Current-Sensor-ACS70331/)|AIN1|
|Buzzer|Sound the buzzer, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとブザーが鳴り、その状態をデバイスシャドウに送信します|[Grove - ブザー](https://www.seeedstudio.com/Grove-Buzzer-p-768.html)|DIO1|
|Relay|Switch on the relay output, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとリレー出力がONになり、その状態をデバイスシャドウに送信します|[Grove - リレー](https://www.seeedstudio.com/Grove-Relay-p-769.html)|DIO1|
|Screw_Terminal/dio|Switch the digital output, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとデジタル出力が切り替わり、その状態をデバイスシャドウに送信します|[Grove - 端子台](https://www.seeedstudio.com/Grove-Screw-Terminal-p-996.html)|DIO1|
|Vibration_Sensor_SW-420|Detect if the sensor is shaken and transfer the result to device-shadow/センサーが振動したかどうかを検出し、結果をデバイスシャドウに送信します。|[Grove - 振動センサー(SW-420)](http://wiki.seeedstudio.com/Grove-Vibration_Sensor_SW-420/)|DIO1|
|Touch|Transfer status to device-shadow when the sensor is touched/センサーにタッチすると、状態をデバイスシャドウに送信します|[Grove - タッチセンサー](https://www.seeedstudio.com/Grove-Touch-Sensor-p-747.html)|DIO1|
|Button|Transfer status to device-shadow when the button is pushed/ボタンが押下されると、状態をデバイスシャドウに送信します|[Grove - ボタン](https://www.seeedstudio.com/Grove-Button-p-766.html)|DIO1|
|LED_Socket_Kit|Turn on the LED, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとLEDが点灯し、その状態をデバイスシャドウに送信します|[Grove - LED](https://www.seeedstudio.com/category/Grove-c-1003/leds-c-891/Grove-Red-LED.html)|DIO1|
|Vibration_Motor|Turn on the vibration, and transfer status to device-shadow when SW4 is pushed/SW4を押下するとモーターが振動し、その状態をデバイスシャドウに送信します|[Grove - 振動モーター](https://www.seeedstudio.com/Grove-Vibration-Motor-p-839.html)|DIO1|
|Adjustable_PIR_Motion_Sensor|Detect the things around to move and transmit if the sensor detected any motion to device-shadow as a boolean. / 物の移動を検出し、真理値としてデバイスシャドウに送信します。|[Grove - PIRセンサー](https://www.seeedstudio.com/Grove-Adjustable-PIR-Motion-Sensor-p-3225.html)|DIO1|
|GPS|Transfer datetime, latitude, longitude and PDOP(position dilution of precision) to device-shadow/日時・緯度経度・PDOP(位置精度低下率)をデバイスシャドウに送信します|[Grove - GPS](https://www.seeedstudio.com/Grove-GPS-p-959.html)|UART|

What is Degu?
--------

Degu is an open-source sensor device platform based on a low-power MCU and the Grove sensors connection interfaces. Degu can connect gateway by Openthread stacks and it on Zephyr OS. For programing user specific behaviour, it impremented micropython interpreter for execute user application.

* More informations about Degu, visit degu web site(https://open-degu.com/)

* Technical resources for Degu on github project repositorys(https://github.com/open-degu)
