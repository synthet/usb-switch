
from monitorcontrol import get_monitors

def test_monitors_v2():
    print("Enumerating monitors (Low Level VCP)...")
    try:
        monitors = get_monitors()
        for i, monitor in enumerate(monitors):
            print(f"Monitor {i+1}:")
            try:
                # Open VCP directly
                with monitor.vcp:
                    # Try to get VCP 0x60 (Input Source)
                    # This returns a tuple (current, max)
                    print("  Attempting to read Input Source (0x60)...")
                    val = monitor.vcp.get_vcp_feature(0x60)
                    print(f"  Success! Input Source Value: {val}")
            except Exception as e:
                print(f"  Error accessing VCP: {e}")

    except Exception as e:
        print(f"Error enumerating monitors: {e}")

if __name__ == "__main__":
    test_monitors_v2()
