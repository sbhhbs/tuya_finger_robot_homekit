import datetime
import logging
import os
import signal
import threading
import time
import pytz
import coloredlogs

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_SWITCH

logger = logging.getLogger(__name__)

coloredlogs.install(level='INFO', milliseconds=True)

# logging.basicConfig(level=logging.DEBUG)

tuya_access_id = os.getenv("tuya_access_id")
tuya_access_key = os.getenv("tuya_access_key")
tuya_device_id = os.getenv("tuya_device_id")
tuya_endpoint = os.getenv("tuya_endpoint")
tuya_username = os.getenv("tuya_username")
tuya_password = os.getenv("tuya_password")

home_port = int(os.getenv("home_port", '51826'))
persist_folder = os.getenv('persist_folder', '/homekit_status/')
address = os.getenv("home_address")
timezone = os.getenv('timezone', 'Asia/Shanghai')


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
            firmware_revision='1.0',
            serial_number=tuya_device_id
        )

    def set_switch(self, state):
        logger.info(f"State set: {state}")
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
