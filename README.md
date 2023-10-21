# Navigator (Flight of The Navigator)

Onboard computer system for campervan.

## Description

A single dashboard that provide multiple functions and connect different controls such Water Tank sensors, Reverse camera, GPS tracking, Satellite Navigation and Engine information.
Is the core of a larger system composed by the following projects:

- Water Tank sensors
- GPS Tracker board
- GPS Tracker back end
- GPS Tracker front end
- Canbus ECU integration

### Hardware

- Raspberry Pi 4
- USB Video Capture device
- GPS Receiver (USB or GY-NEO6MV2 module)
- DC-DC Buck Step-down voltage converters

- - notes

### Software



### Schematics

| HC-06 | Arduino |
| :---- | :------ |
| `Rx`  | `Tx`    |
| `Tx`  | `Rx`    |
| `Vcc` | `Vcc`   |
| `Gnd` | `Gnd`   |

| I2C Oled  | Arduino (Sparkfun Pro Micro) |
| :-------- | :--------------------------- |
| `Sck`     | `3 (Scl)`                    |
| `Sda`     | `2 (Sda)`                    |
| `Vcc/Vdd` | `Vcc`                        |
| `Gnd`     | `Gnd`                        |

![alt text](./imgs/schematics.png)

### Pro Micro pinout reference

![alt text](./imgs/pinout.png)
