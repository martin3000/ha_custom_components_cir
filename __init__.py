"""Support for IR devices."""
""" 2020 by Martin Schlatter, Schwetzingen, Germany """

# pylint: disable=no-member, import-error
import logging
import threading
import time
import evdev
import voluptuous as vol
from pathlib import Path
from homeassistant.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP

_LOGGER = logging.getLogger(__name__)

KEY_CODE = "key_code"
KEY_ACTION = "key_action"

DOMAIN = "cir"

EVENT_IR_COMMAND_RECEIVED = "ir_command_received"

ICON = "mdi:remote"
#DEVPATH = '/dev/input/event11'

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    # blocking=True gives unexpected behavior (multiple responses for 1 press)
    # also by not blocking, we allow hass to shut down the thread gracefully
    # on exit.
    def _start_cir(_event):
        cir_interface.start()

    def _stop_cir(_event):
        cir_interface.stopped.set()

    device = next(Path("/sys/class/rc/").glob("rc*/input*/event*/"),None)
    if device == None:
        devpath = None
        _LOGGER.error("CIR: no rc device found in /sys/class/rc")
    else:
        devpath = f"/dev/input/{device.name}"
        _LOGGER.debug("input event: %s",devpath)

        cir_interface = CirInterface(hass,devpath)

        hass.bus.listen_once(EVENT_HOMEASSISTANT_START, _start_cir)
        hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, _stop_cir)

    _LOGGER.debug("CIR setup")

    return True

class CirInterface(threading.Thread):
    """
    When using in blocking mode, sometimes repeated commands get produced
    in the next read of a command so we use a thread here to just wait
    around until a non-empty response is obtained .
    """

    def __init__(self, hass, devpath2):
        threading.Thread.__init__(self)
        self.daemon = True
        self.stopped = threading.Event()
        self.hass = hass
        if devpath2 != None:
            self.device = evdev.InputDevice(devpath2)
            _LOGGER.debug("CIR: device init")
        else:
            self.device = None
            _LOGGER.debug("CIR: device not init")

        _LOGGER.debug("CIR __init__")

    def run(self):
        """Run the loop of the CIR interface thread."""
        _LOGGER.debug("CIR interface thread started")
        if self.device != None:
          while not self.stopped.isSet():
            event = self.device.read_one()
            if event != None:
                if event.type==evdev.ecodes.EV_KEY:   # KeyEvent
                    _LOGGER.debug("Keycode: %i value: %i",event.code,event.value)
                    #if event.value==1:  # key-down
                    self.hass.bus.fire(EVENT_IR_COMMAND_RECEIVED, {KEY_CODE: event.code,KEY_ACTION: event.value})
            else:
                time.sleep(0.5)
        _LOGGER.debug("CIR interface thread stopped")
        
