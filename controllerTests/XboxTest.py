import objc
import time
import GameController
from Foundation import NSNotificationCenter, NSRunLoop, NSDate

# --- Connection Callbacks ---

def controller_connected(notification):
    controller = notification.object()
    print(f"\n✅ Controller connected: {controller.vendorName()}")
    setup_controller(controller)

def controller_disconnected(notification):
    print("\n❌ Controller disconnected.")

# --- Button/Input Setup ---

def setup_controller(controller):
    profile = controller.extendedGamepad()

    if profile is None:
        print("Controller does not support extendedGamepad profile.")
        return

    print("Listening for inputs...\n")

    # --- Buttons ---
    def make_button_handler(name):
        def handler(button, value, pressed):
            if pressed:
                print(f"[BUTTON PRESSED]  {name}")
            else:
                print(f"[BUTTON RELEASED] {name}")
        return handler

    profile.buttonA().setPressedChangedHandler_(make_button_handler("A"))
    profile.buttonB().setPressedChangedHandler_(make_button_handler("B"))
    profile.buttonX().setPressedChangedHandler_(make_button_handler("X"))
    profile.buttonY().setPressedChangedHandler_(make_button_handler("Y"))

    profile.leftShoulder().setPressedChangedHandler_(make_button_handler("Left Bumper (LB)"))
    profile.rightShoulder().setPressedChangedHandler_(make_button_handler("Right Bumper (RB)"))

    profile.buttonMenu().setPressedChangedHandler_(make_button_handler("Menu/Start"))
    profile.buttonOptions().setPressedChangedHandler_(make_button_handler("Back/Select"))

    profile.leftThumbstickButton().setPressedChangedHandler_(make_button_handler("Left Stick Click"))
    profile.rightThumbstickButton().setPressedChangedHandler_(make_button_handler("Right Stick Click"))

    # --- Triggers ---
    def make_trigger_handler(name):
        def handler(trigger, value, pressed):
            if pressed:
                print(f"[TRIGGER]  {name}: {value:.2f}")
        return handler

    profile.leftTrigger().setValueChangedHandler_(make_trigger_handler("Left Trigger (LT)"))
    profile.rightTrigger().setValueChangedHandler_(make_trigger_handler("Right Trigger (RT)"))

    # --- D-Pad ---
    def dpad_handler(dpad, xValue, yValue):
        if yValue > 0.5:
            print("[D-PAD]  Up")
        elif yValue < -0.5:
            print("[D-PAD]  Down")
        if xValue < -0.5:
            print("[D-PAD]  Left")
        elif xValue > 0.5:
            print("[D-PAD]  Right")

    profile.dpad().setValueChangedHandler_(dpad_handler)

    # --- Thumbsticks ---
    DEADZONE = 0.2

    def make_stick_handler(name):
        def handler(stick, xValue, yValue):
            if abs(xValue) > DEADZONE or abs(yValue) > DEADZONE:
                print(f"[STICK]  {name}  X: {xValue:.2f}  Y: {yValue:.2f}")
        return handler

    profile.leftThumbstick().setValueChangedHandler_(make_stick_handler("Left Stick"))
    profile.rightThumbstick().setValueChangedHandler_(make_stick_handler("Right Stick"))


# --- Main ---

def main():
    # Register connection/disconnection notifications
    NSNotificationCenter.defaultCenter().addObserverForName_object_queue_usingBlock_(
        GameController.GCControllerDidConnectNotification,
        None, None,
        controller_connected
    )
    NSNotificationCenter.defaultCenter().addObserverForName_object_queue_usingBlock_(
        GameController.GCControllerDidDisconnectNotification,
        None, None,
        controller_disconnected
    )

    # Check for already-connected controllers
    controllers = GameController.GCController.controllers()
    if controllers:
        print(f"Found {len(controllers)} controller(s) already connected.")
        for c in controllers:
            setup_controller(c)
    else:
        print("No controller detected yet. Connect your Xbox controller and press its button to wake it.")

    print("Waiting for input... Press Ctrl+C to quit.\n")

    # Run the macOS event loop so callbacks fire
    try:
        run_loop = NSRunLoop.currentRunLoop()
        while True:
            run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()