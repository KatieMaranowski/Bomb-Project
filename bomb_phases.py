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
from random import random, randint

#########
#####messages####

# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        
        self._speaking = False # creates a queue for phrases incase a random one fires off when something important is being said
        #Hint checks
        
        self._kp_hint1 = False # after first code
        self._kp_hint2 = False # after second
        self._kp_hint3 = False # after third
        self._kp_hint4 = False # defused
        
        self.keypad_phase = None
        
        # make the GUI fullscreen
        window.update_idletasks()
        window.attributes("-fullscreen", True)
        try:
            window.state('zoomed')
        except Exception:
            pass
        window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0")
        # store timer and button for later
        self._timer = None
        self._button = None
        # preload both virus images
        open_img = PhotoImage(file="virusopen.png")
        closed_img = PhotoImage(file="virusclosed.png")
        self._virus_open = open_img.subsample(4, 4)
        self._virus_closed = closed_img.subsample(4, 4)
        # speaking state
        self._speak_text = ""
        self._speak_index = 0
        self._speak_callback = None
        # setup the initial "boot" GUI
        self.setupBoot()

    def speak(self, text, callback=None):
        self._speaking = True
        
        self._text_box.config(state=NORMAL)
        if self._text_box.get("1.0", END).strip(): # i decided to change this to always make a new line in the speaking part itself cause i kept not putting them in the code
            self._text_box.insert(END, "\n")
        self._text_box.config(state=DISABLED)
        
        self._speak_text = text
        self._speak_index = 0
        self._speak_callback = callback
        # start typing animation after short delay
        self.after(500, self._type_speak)

    def _type_speak(self):
        if self._speak_index < len(self._speak_text):
            # randomly switch virus image to mimic talking
            if random() < 0.5:
                self._image_label.config(image=self._virus_open)
            else:
                self._image_label.config(image=self._virus_closed)
            # insert next character
            self._text_box.config(state=NORMAL)
            self._text_box.insert(END, self._speak_text[self._speak_index])
            self._text_box.see(END)  # auto-scroll as new text appears
            self._text_box.config(state=DISABLED)
            self._speak_index += 1
            # schedule next character
            self.after(80, self._type_speak)
        else:
            # ensure mouth closed at end
            self._image_label.config(image=self._virus_closed)
            self._speaking = False
            # callback if provided
            if self._speak_callback:
                self._speak_callback()

    # sets up the initial splash GUI
    def setupBoot(self):
        # place virus at bottom-left
        self._image_label = Label(self, image=self._virus_closed, bg="black")
        self._image_label.place(relx=0.1, rely=1.0, anchor=SW)

        # optional scrolling text label
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)

        # add read-only text box at bottom-right
        self._text_box = Text(self, bg="black", fg="white", font=("Courier New", 14), height=5, width=30, bd=0,wrap=WORD)
        self._text_box.place(relx=1.0, rely=1.0, anchor=SE)
        self._text_box.config(state=DISABLED)

        # introduction sequence
        intro_lines = [
            "Hello Player",
            "I am Virey the Virus, and I have infected this bomb",
            "You must complete a series of phases before",
            "the timer runs out",
            "Your first hint is to set the toggles to '9' ;)",
            "Good Luck :)"
        ]
        intro_text = "\n".join(intro_lines)
        # speak intro, then allow game setup
        self.speak(intro_text, self.startGame)

        self.pack(fill=BOTH, expand=True)

    # called after intro finishes
    def startGame(self):
        self.setup()
        self._random_message_delay()
        self._watch_keypad()
    
    def _watch_keypad(self):
        kp = self.keypad_phase
        if kp and not self._kp_hint1 and kp._active:
            self._kp_hint1 = True
            hint1 = (
                "I'll give you some hints 'cause I'm such a nice virus.\n"
                "Hint 1: What year did Columbus sail the ocean blue?"
            )
            self.speak(hint1, self._watch_keypad)
        elif kp and not self._kp_hint2 and kp._current_index >= 1:
            self._kp_hint2 = True
            hint2 = (
                "Congrats on the first one!\n"
                "Next hint (a bit trickier):\n"
                "I am the very first 4-digit number that reads the same forwards and backwards. What am I? (Not 0000)"
            )
            self.speak(hint2, self._watch_keypad)
        elif kp and not self._kp_hint3 and kp._current_index >= 2:
            self._kp_hint3 = True
            hint3 = (
                "You're almost done!\n"
                "Final hint:\n"
                "What is the product of the number of months in a year multiplied by the number of hours in a week?\n"
                "Good luck!"
            )
            self.speak(hint3, self._watch_keypad)
        elif kp and not self._kp_hint4 and kp._defused:
            self._kp_hint4 = True
            hint4 = (
                "Oh wow, you actually did it!\n"
                "Now, set the toggles to 'E' to move on to the next phase ;)"
            )
            self.speak(hint4, self._watch_keypad)
        else:
            self.after(100, self._watch_keypad)
        
        
    messages = ["Nothing can stop me now!","THIS ISNT EVEN MY FINAL FORM!","Nice try!","[from evil_libraries import maniacal_laugh]","Didn't anyone ever teach you internet safety?"]
        

    def _random_message_delay(self):
        delay = randint(15, 30) * 1000 #random time in seconds
        self.after(delay, self._try_random_message)
        
    def _try_random_message(self):
        if self._speaking:
            self.after(1000, self._try_random_message)
        else:
            self._random_message()
    def _random_message(self):
        numba = randint(0, len(self.messages) - 1)
        phrase = self.messages[numba]
        
        self.speak(phrase, self._random_message_delay)
        
    
        
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
        self._lstrikes.place(relx=1.0, rely=0.05, anchor=NE)
        if SHOW_BUTTONS:
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
        self._active = True

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
        self._codes = ["1492", "1001", "2016"]
        self._current_index = 0
        
    def reset(self):
        self._value = ""
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
                elif len(self._value) >= len(code): #only checks if right after 4 digits are put in (removes bruteforce method)
                    self._failed = True
                    
            sleep(0.1)
                
                

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        attempt = self._current_index + 1
        total = len(self._codes)

        return f"{self._value} (Code {attempt}/{total})"

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)
        
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
        pass

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, _old_target, _old_color, timer, name="Button"):
        super().__init__(name, component_state, None)
        self._component    = component_state
        self._rgb          = component_rgb
        self._timer        = timer
    
        # how many flashes & min gap
        self._num_events   = 3
        self._min_gap      = 30
        self._defused_cnt  = 0
        self._awaiting     = False

        total = timer._value
        margin = self._min_gap * (self._num_events - 1)
        segment = (total - margin) // self._num_events

        # pick 3 random trigger–times, sorted high→low
        self._thresholds = []
        for i in range(self._num_events):
            seg_start = i * (segment + self._min_gap)
            seg_end   = seg_start + segment
            rind = randint(seg_start, seg_end)
            self._thresholds.append(total - rind)
        self._thresholds.sort(reverse=True)
        
        print("DEBUG || WHEN BUTTON WILL FLASH")
        for rind in self._thresholds:
            mins, sec = divmod(rind, 60)
            print(f" {mins:02d}:{sec:02d} ({rind}s)")
        
    def reset(self):
        pass

    def run(self):
        self._running = True
        pressed = False

        # start red
        self._rgb[0].value = False  # red ON
        self._rgb[1].value = True   # green OFF
        self._rgb[2].value = True   # blue OFF

        while self._running:
            # 1) trigger the next green flash if it’s time
            if self._defused_cnt < self._num_events and not self._awaiting:
                if self._timer._value <= self._thresholds[self._defused_cnt]:
                    # flash green
                    self._rgb[0].value = True   # red OFF
                    self._rgb[1].value = False  # green ON
                    self._awaiting = True

            # 2) only listen if toggles → Button *and* we’re awaiting
            if not (self._active and self._awaiting):
                sleep(0.1)
                continue

            # 3) detect press→release
            current = self._component.value
            if current and not pressed:
                # button just depressed
                pressed = True
            elif not current and pressed:
                # button released after a press
                pressed = False
                self._defused_cnt += 1
                self._awaiting = False

                # back to red
                self._rgb[0].value = False
                self._rgb[1].value = True

                # if we’ve done all flashes, mark defused
                if self._defused_cnt >= self._num_events:
                    self._defused = True
                    break

            sleep(0.1)

    def __str__(self):
        if self._defused:
            return "DEFUSED"
        if self._awaiting:
            return ">> PUSH ME! <<"
        remaining = self._num_events - self._defused_cnt
        return f"Waiting... ({remaining} presse(s) left)"


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