
import wmi

def list_usb_devices():
    c = wmi.WMI()
    print("Scanning for USB devices...")
    print("-" * 60)
    for item in c.Win32_PnPEntity():
        if item.Description and "USB" in item.Description:
            print(f"Name: {item.Name}")
            print(f"Description: {item.Description}")
            print(f"DeviceID: {item.DeviceID}") 
            # DeviceID usually looks like USB\VID_xxxx&PID_xxxx\......
            print("-" * 60)

if __name__ == "__main__":
    try:
        list_usb_devices()
    except ImportError:
        print("Please install wmi: pip install wmi pywin32")
