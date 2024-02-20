import logging
import os
import signal

import coloredlogs
import tinytuya
from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_SWITCH
from tuya_iot import (
    TuyaOpenAPI,
    AuthType,
    TUYA_LOGGER
)

logger = logging.getLogger(__name__)

coloredlogs.install(level='INFO', milliseconds=True)

TUYA_LOGGER.setLevel(logging.DEBUG)

tinytuya.set_debug(True)

# logging.basicConfig(level=logging.DEBUG)

tuya_access_id = os.getenv("tuya_access_id")
tuya_access_key = os.getenv("tuya_access_key")
tuya_device_id = os.getenv("tuya_device_id")
tuya_endpoint = os.getenv("tuya_endpoint")
tuya_username = os.getenv("tuya_username")
tuya_password = os.getenv("tuya_password")
tuya_countrycode = os.getenv("tuya_countrycode")
tuya_schema = os.getenv("tuya_schema")

local_gateway_device_id = os.getenv("local_gateway_device_id")
local_gateway_local_key = os.getenv("local_gateway_local_key")
local_finger_bot_cid = os.getenv("local_finger_bot_cid")
local_finger_bot_device_id = os.getenv("local_finger_bot_device_id")

home_port = int(os.getenv("home_port", '51826'))
persist_folder = os.getenv('persist_folder', '/homekit_status/')
address = os.getenv("home_address")
timezone = os.getenv('timezone', 'Asia/Shanghai')

openapi = TuyaOpenAPI(tuya_endpoint, tuya_access_id, tuya_access_key, AuthType.SMART_HOME)


class FingerRobot(Accessory):
    category = CATEGORY_SWITCH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the fan service. Also add optional characteristics to it.
        self.serv_switch = self.add_preload_service('Switch')
        self.char_switch = self.serv_switch.configure_char(
            'On', setter_callback=self.set_switch
        )

        self.set_info_service(
            manufacturer='TuyaFingerRobot',
            model='Finger',
            firmware_revision='2.0',
            serial_number=tuya_device_id
        )
        self.local_gateway = None
        if local_gateway_device_id and local_gateway_local_key:
            self.local_gateway = tinytuya.Device(
                dev_id=local_gateway_device_id,
                address='Auto',  # Or set to 'Auto' to auto-discover IP address
                local_key=local_gateway_local_key,
                version=3.4
            )

    def set_switch(self, state):
        logger.info(f"State set: {state}")
        if state:
            def do_remotely():
                openapi.connect(tuya_username, tuya_password,
                                country_code=tuya_countrycode,
                                schema=tuya_schema
                                )
                commands = {'commands': [{'code': 'switch', 'value': True}]}
                openapi.post('/v1.0/iot-03/devices/{}/commands'.format(tuya_device_id), commands)

            def do_locally():
                fingerbot = tinytuya.Device(
                    local_finger_bot_device_id,
                    cid=local_finger_bot_cid,
                    parent=self.local_gateway
                )
                fingerbot.turn_on(2)

            if self.local_gateway is not None:
                try:
                    do_locally()
                except:
                    do_remotely()
            else:
                do_remotely()

        self.char_switch.value = False
        self.char_switch.notify()


def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    return FingerRobot(driver, 'FingerRobot')


# Start the accessory on port
driver = AccessoryDriver(port=home_port,
                         persist_file=persist_folder + 'accessory.state',
                         address=address)

# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_accessory(driver))

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
