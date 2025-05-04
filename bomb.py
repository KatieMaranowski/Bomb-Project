#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: ijohugyfyguhij
#################################

# import the configs
from bomb_configs import *
# import the phases
from bomb_phases import *
# import the talking‐virus GUI
from bomb_gui import BombGUI

###########
# functions
###########

# generates the bootup sequence on the LCD
def bootup(n=0):
    global window, gui, strikes_left, active_phases

    # scroll the boot text
    text = BOOT_TEXT[n : n + SCREEN_WIDTH]
    gui._lscroll["text"] = text
    if n < len(BOOT_TEXT) - SCREEN_WIDTH:
        gui.after(BOOT_SPEED, bootup, n + 1)
    else:
        # once the scroll finishes, switch to the main display
        gui.setup()
        # start the timer countdown
        timer.start()
        # start each phase thread
        keypad.start()
        wires.start()
        button.start()
        toggles.start()
        # and begin phase‐checking
        check_phases()

# checks the phase threads
def check_phases():
    global active_phases

    # update the timer display (or explode on timeout)
    if timer._running:
        gui._ltimer["text"] = f"Time left: {timer}"
    else:
        turn_off()
        gui.after(100, gui.conclusion, False)
        return

    # update each phase’s label
    gui._lkeypad["text"] = f"Keypad phase: {keypad}"
    gui._lwires["text"]  = f"Wires phase: {wires}"
    gui._lbutton["text"] = f"Button phase: {button}"
    gui._ltoggles["text"] = f"Toggles phase: {toggles}"
    gui._lstrikes["text"] = f"Strikes left: {strikes_left}"

    # count how many phases are still active
    active_phases = sum(1 for p in (keypad, wires, button, toggles) if p._active)

    # if they’re all defused, celebrate!
    if active_phases == 0:
        turn_off()
        gui.after(100, gui.conclusion, True)
    else:
        # otherwise, re‐check in a bit
        gui.after(50, check_phases)

# helper to turn off everything (called on success or failure)
def turn_off():
    timer.pause()
    keypad.pause()
    wires.pause()
    button.pause()
    toggles.pause()

#################################
# Main window setup & launch
#################################

# create the single root window
window = Tk()
window.config(bg='#D3D3D3')

# plug in the LCD GUI
gui = Lcd(window)

# create the talking‐virus window as a Toplevel on the same loop
BombGUI(
    master=window,
    open_image_path="virusopen.png",
    closed_image_path="virusclosed.png",
    typing_delay=100
)

# initialize the bomb strikes and active phases
strikes_left  = NUM_STRIKES
active_phases = NUM_PHASES

# start the boot sequence after a short delay
gui.after(1000, bootup)

# run the single Tk event loop for both windows
window.mainloop()
