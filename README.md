# Home Assistant Custom Component for processing IR Events

sudo apt install python3-evdev

sudo adduser ha_user input

sudo ir-keytable -c -p nec -w /etc/rc_keymaps/mx3.toml

Example of mx3.toml:

> [[protocols]]
> name = "mx3 gyro mouse"
> protocol = "nec"
> variant = "necx"
> [protocols.scancodes]
> 0x14 = "KEY_RED"
> 0xb8009d = "KEY_GREEN"
> 0xb8009b = "KEY_YELLOW"
> 0xb8009a = "KEY_BLUE"


