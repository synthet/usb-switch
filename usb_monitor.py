
import wmi
import time
import pythoncom
import logging
from monitorcontrol import get_monitors
import config

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("usb_monitor.log"),
        logging.StreamHandler()
    ]
)

def set_monitor_input(input_value):
    """
    Sets the input source for all connected external monitors.
    """
    logging.info(f"Attempting to switch monitors to input source: {hex(input_value)}")
    try:
        monitors = get_monitors()
        for i, monitor in enumerate(monitors):
            try:
                with monitor.vcp:
                    monitor.vcp.set_vcp_feature(config.VCP_INPUT_SOURCE, input_value)
                    logging.info(f"Switched Monitor {i+1} to {hex(input_value)}")
            except Exception as e:
                logging.error(f"Failed to switch Monitor {i+1}: {e}")
    except Exception as e:
        logging.error(f"Error accessing monitors: {e}")

def is_target_device(device):
    """
    Checks if the WMI device object matches our target VID/PID.
    DeviceID format: USB\VID_xxxx&PID_xxxx\InstanceId
    """
    try:
        if not device.DeviceID:
            return False
        
        dev_id = device.DeviceID.upper()
        target_vid = f"VID_{config.TRIGGER_DEVICE_VID}".upper()
        target_pid = f"PID_{config.TRIGGER_DEVICE_PID}".upper()
        
        if target_vid in dev_id and target_pid in dev_id:
            return True
            
    except AttributeError:
        pass
    return False

def check_initial_state():
    """
    Checks if the device is currently connected at startup.
    """
    logging.info("Checking initial device state...")
    c = wmi.WMI()
    for item in c.Win32_PnPEntity():
        if is_target_device(item):
            logging.info("Target device found on startup. Switching to Windows.")
            set_monitor_input(config.INPUT_SOURCE_WINDOWS)
            return True
    
    logging.info("Target device NOT found on startup. Switching to Mac.")
    set_monitor_input(config.INPUT_SOURCE_MAC)
    return False

def monitor_loop():
    """
    Main loop monitoring WMI events for device connection/disconnection.
    """
    logging.info("Starting USB Monitor Loop...")
    
    # Initialize COM for the WMI watcher
    pythoncom.CoInitialize()
    c = wmi.WMI()
    
    # Watch for creation (Connection)
    watcher_creation = c.Win32_PnPEntity.watch_for("creation")
    # Watch for deletion (Disconnection)
    watcher_deletion = c.Win32_PnPEntity.watch_for("deletion")
    
    check_initial_state()

    while True:
        try:
            # Check for new connections
            # We use a short timeout to alternate checking both watchers
            # Note: wmi watcher is blocking, but we can't easily select() on it.
            # We will use a naive approach: blocking wait on Creation, but that blocks Deletion.
            # Better approach for simple script: Polling or Threading.
            # Given Python WMI watcher limitations, raw polling Win32_PnPEntity every few seconds 
            # might be more robust and strictly sufficient for a KVM switch delay (1-2s).
            # But let's try the event interface first? No, two watchers is tricky single-threaded.
            # Let's switch to Polling for simplicity and robustness.
            pass
            
        except KeyboardInterrupt:
            break

def polling_loop():
    """
    Robust polling loop properly handling the state.
    """
    logging.info("Starting USB Polling Loop...")
    c = wmi.WMI()
    
    # Initial State
    was_connected = False
    
    # Initial scan
    for item in c.Win32_PnPEntity():
        if is_target_device(item):
            was_connected = True
            break
            
    if was_connected:
        logging.info("Startup: Device Connected -> Windows")
        set_monitor_input(config.INPUT_SOURCE_WINDOWS)
    else:
        logging.info("Startup: Device Disconnected -> Mac")
        set_monitor_input(config.INPUT_SOURCE_MAC)
        
    while True:
        try:
            is_connected = False
            # Re-query WMI
            # Filtering in WMI query is faster: WHERE DeviceID LIKE ...
            # But 'LIKE' syntax in WQL has quirks with backslashes.
            # Fetching all USB devices is reasonable.
            for item in c.Win32_PnPEntity():
                if is_target_device(item):
                    is_connected = True
                    break
            
            if is_connected != was_connected:
                if is_connected:
                    logging.info("Event: Device Connected -> Switching to Windows")
                    set_monitor_input(config.INPUT_SOURCE_WINDOWS)
                else:
                    logging.info("Event: Device Disconnected -> Switching to Mac")
                    set_monitor_input(config.INPUT_SOURCE_MAC)
                
                was_connected = is_connected
            
            time.sleep(2) # Poll every 2 seconds
            
        except KeyboardInterrupt:
            logging.info("Stopping...")
            break
        except Exception as e:
            logging.error(f"Error in polling loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    polling_loop()
