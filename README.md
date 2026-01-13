# USB Switch Monitor Controller

Automated input switching for Dell monitors when toggling a USB KVM between Windows and Mac.

## How it works
This python script runs on Windows. It monitors for the connection/disconnection of a specific USB device (your KVM/Logitech Receiver).
- **Connects** (Switch to Win): Sends DDC/CI command to monitor to switch input to **HDMI-1**.
- **Disconnects** (Switch to Mac): Sends DDC/CI command to monitor to switch input to **USB-C**.

## Configuration
Edit `config.py` if you need to change device IDs or Input Source codes.
Default:
- Trigger: Logitech Receiver (`VID_046D`, `PID_C548`)
- Inputs: HDMI-1 (`0x11`) and USB-C (`0x1B`)

## Usage
1.  **Install Requirements**:
    ```bash
    pip install wmi monitorcontrol
    ```
2.  **Run**:
    Double-click `run_monitor.bat` or run `python usb_monitor.py` in a terminal.

## Auto-Start
To run on startup:
1.  Press `Win` + `R`, type `shell:startup`, and press Enter.
2.  Copy `run_monitor.bat` (or a shortcut to it) into that folder.

