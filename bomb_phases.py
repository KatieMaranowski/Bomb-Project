#hi


#sdsdf
################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.setupBoot()

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False
        
        self._active = False

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if not self._active:
                sleep(0.1)
                continue
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the keypad phase
class Keypad(PhaseThread):
    placeholder = 0
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""
        self._codes = ["1234", "5678", "9012"]
        self._current_index = 0
        
    def reset(self):
        self._value = ""
        self._current_index = 0
        self._defused = False
        self._failed = False
        

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if not self._active:
                sleep(0.1)
                continue
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                code = self._codes[self._current_index]
                
                if self._value == code and self._current_index == len(self._codes) - 1:
                    self._defused = True
                    #self._running = False
                    break
                if self._value == code:
                    self._current_index += 1
                    self._value = ""
                elif not code.startswith(self._value):
                    self._failed = True
                    
            sleep(0.1)
                

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        attempt = self._current_index + 1
        total = len(self._codes)

        return f"{self._value} (Code {attempt}/{total})"

#jumper wires phase
class Wires(PhaseThread):
    def __init__(self, color, connected, name="Wires"):  #add pins
        self.color = color
        self.connected = connected
        self.cut = False
        self.instructions = []
        
    def get_instructions(self):
        #virus will give confusing set of instructions
        self.insturctions = [
            f"Cut the {self.color} wire if it is connected to Phase 1.",
            f"DO NOT cut the {self.color} wire if it's connected to Phase 3.",
            f"Cut the {self.color} wire if it's even numbered.",
            f"DO NOT cut the {self.color} wire if it's connected to the red switch."
            ]
        
        #returning random instruction
        return random.choice(self.instructions)
    
    #resetting toggles   
    def reset(self):
        self._value = ""
        self._current_index = 0
        self._defused = False
        self._failed = False
        
        
#creating virus
class Virus:
    def __init__(self, wires):
        self.wires = wires #list of wire objects
        self.active = False #virus flag
  
    #activating wires
    def activate(self):
        self.active = True
        self.infect_wires()
     
    #making the wires have a virus
    def _infect_wires(self):
        """Apply virus effect and give confusing instructions to the wires."""
        for wire in self.wires:
            instruction = wire.get_instrctions()
            print(f"Virus: {instruction}")
            
    def check_for_defuse(self):
        """Check if all wires have been cut and the virus is answered."""
        if all(wire.cut for wire in self.wires):
            print("All wires cut. The virus is removed from the screen.")
            self.active = False   #virus is removed
        else:
            print("The virus is still active. Wires need to be cut.")
            
    
    #getting confusing information to remove the wires
    def get_confusing_instructions(self):
        """Return the confusing instructions for the wires."""
        return [wire.get_instructions() for wire in self.wires]
    
    
#example setup
wires = [
    Wire(color="red", connected=True),
    Wire(color="blue", connected=True),
    Wire(color="green", connected=True)
    ]

virus = Virus(wires)

#activate virus to confuse player
virus.activate()

#player interacting with wires cutting them
wires[0].cut_wire()
wires[1].cut_wire()
wires[2].cut_wire()

#check if wires have been cut to remove virus
virus.check_for_defuse()
            
        
        
        
'''        
    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if not self._active:
                sleep(0.1)
                continue
        pass

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass
'''

#pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer
        
        
    #setting color values
        def _set_color(self, color):
            self.rgb[0].value = not (color == "R")
            self.rgb[1].value = not (color == "G")
            self.rgb[2].value = not (color == "B")
            self.current_color = color
            
    #reset the toggles
    def reset(self):
        self._value = ""
        self._current_index = 0
        self._defused = False
        self._failed = False

    # runs the thread
    def run(self):
        self._running = True
        #picking color randomly
        while True:
            new_color = Button.colors[randint(0,2)]
            self._set_color(new_color)
            
            #hold color
            for _ in range(10): #10 = 1 second
                self.value:
                    #checking if right color was pressed
                    if self.current_color == self.target:
                        self success = True
                    else:
                        self.success = False
                    #wait time till the button is pressed
                    sleep(0.5)
                    while self._state.value:
                        sleep(0.05)
                    sleep(0.1)
    
    #displaying outcome
    def __str__(self):
        if self._value:
            return f"Pressed ({self.current_color})"
        return f"{self.current_color} - Target: {self.target_colro}"
            
        
        
        
        
        
        
'''        
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (self._running):
            if not self._active:
                sleep(0.1)
                continue
            # get the pushbutton's state
            self._value = self._component.value
            # it is pressed
            if (self._value):
                # note it
                self._pressed = True
            # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    if (not self._target or self._target in self._timer._sec):
                        self._defused = True
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
            sleep(0.1)

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")
'''
# the toggle switches phase
class Toggles(PhaseThread):
    from bomb_configs import toggle_patterns
    def __init__(self, component, target, phase_map, name="Toggles"):
        super().__init__(name, component, target)
        self._phase_map = phase_map
    

    # runs the thread
    def run(self):
        self._running = True
        while self._running:
            toggled = "".join(str(int(p.value)) for p in self._component)
            
            for name, pattern in toggle_patterns.items():
                phase = self._phase_map[name]
                active = (toggled == pattern)
                if active and not phase._active:
                    phase.reset()
                phase._active = active
                
            self._value = toggled
            sleep(0.05)
            

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        return self._value if self._value is not None else "----"
