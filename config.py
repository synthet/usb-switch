
# Configuration for USB Switch Monitor Controller

# USB Device to Track (Logitech Receiver)
TRIGGER_DEVICE_VID = "046D"
TRIGGER_DEVICE_PID = "C548"

# Monitor Input Sources (VCP Code 0x60)
# Standard VCP Values:
# 0x11: HDMI-1
# 0x12: HDMI-2
# 0x0F: DisplayPort
# 0x1B: USB-C (Thunderbolt)

INPUT_SOURCE_WINDOWS = 0x11  # HDMI-1
INPUT_SOURCE_MAC = 0x1B      # USB-C

# VCP Code for Input Source
VCP_INPUT_SOURCE = 0x60
