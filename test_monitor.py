
from monitorcontrol import get_monitors

def test_monitors():
    print("Enumerating monitors...")
    try:
        monitors = get_monitors()
        for i, monitor in enumerate(monitors):
            with monitor:
                print(f"Monitor {i+1}:")
                print(f"  Name: {monitor.get_vcp_capabilities().get('model', 'Unknown')}")
                # Try to get VCP 0x60 (Input Source)
                try:
                    # Some monitors return a tuple (current_value, max_value)
                    # 0x60 is the code for Input Source
                    val = monitor.vcp.get_vcp_feature(0x60)
                    print(f"  Current Input Source Value: {val}")
                except Exception as e:
                    print(f"  Could not read Input Source: {e}")
    except Exception as e:
        print(f"Error enumerating monitors: {e}")

if __name__ == "__main__":
    test_monitors()
