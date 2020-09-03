# Home Assistant Custom Component for processing IR Events
This custom component receives IR events and fires HA events. It does not use lirc/lircd.

sudo apt install python3-evdev

sudo adduser _ha_user_ input         `-> add the current home assistant user to the input group. replace ha_user with your user!`


Create /etc/rc_keymaps/mx3.toml:
```
[[protocols]]
name = "mx3 gyro mouse"
protocol = "nec"
variant = "necx"
[protocols.scancodes]
0x14 = "KEY_RED"
0xb8009d = "KEY_GREEN"
0xb8009b = "KEY_YELLOW"
0xb8009a = "KEY_BLUE"
```
Add the following line to /etc/rc_maps.cfg :
```
*       *                        mx3.toml
```

sudo ir-keytable -c -p nec -w /etc/rc_keymaps/mx3.toml
  or
sudo ir-keytable -c -p nec -w /lib/udev/rc_keymaps/dvbsky.toml  

Change "input12" in the code to the correct input device. To find the input device, run "ir-keytable".

Automation example:
```
- id:  tvir
  alias: tv_ir
  trigger:
    platform: event
    event_type: ir_command_received
    event_data:
      key_code: 398
      key_action: 1
  action:
  - service: light.turn_on
    entity_id: light.osram_cla60_rgbw
```
