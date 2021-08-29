from threading import Thread
import win32api
import win32con
import time

# Helper stuff
vKeys = {
           'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'space':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left':0x25,
           'up':0x26,
           'right':0x27,
           'down':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'shift':0xA0,
           'shift_r':0xA1,
           'ctrl_l':0xA2,
           'ctrl_r':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0
           }
def stopCallback(li, key):
	li.stop()

class Key:
	def __init__(self, keyCode, onPress=None, onRelease=None):
		self.code = keyCode
		self.held = False
		self.onPress = [onPress] if onPress else []
		self.onRelease = [onRelease] if onRelease else []

	@property	
	def name(self):
		for k,v in vKeys.items():
			if v == self.code:
				return k

	@property
	def pressed(self):
		return ((win32api.GetKeyState(self.code) >> 15) & 1)

class Listener:

	listening = False

	def __init__(self, onPress=None, onRelease=None, keys=list(vKeys.values()), stopKey=vKeys['backspace'], debug=False):
		'''
		onPress = called when a key is pressed
		onRelease = called when a key is released
		keys = list of virtual keycodes that need to be listened to
		stopKey = the key that needs to be pressed to stop the listener. By default it is backspace
		This is a general listener for all keys and the callbacks for each key are the same.
		'''
		self.globalOnPress = onPress
		self.globalOnRelease = onRelease
		self.keys = [Key(x, self.globalOnPress, self.globalOnRelease) for x in keys if x != stopKey]
		self.stopKey = Key(stopKey, stopCallback)
		self.keys.append(self.stopKey)
		self.debug = debug

		self.__start()

	def __keyListener(self, key):
		'''
		private function is the target for all the threads. each instance handles one key
		'''
		while self.listening:
			
			# wait for a key press
			while (not key.pressed) and self.listening:
				pass

			if self.listening:
				key.held = True
				if self.debug: print('Pressed:', key.name)
				for f in key.onPress:
					if f:
						try: f(self, key) 
						except Exception as e: 
							print('ERROR:', e)
							self.stop() 
			
			# wait while the key is held and only go ahead once it is released
			while key.pressed and self.listening:
				pass

			if self.listening:
				key.held = False
				if self.debug: print('Released:', key.name)
				for f in key.onRelease:
					if f:
						try: f(self, key) 
						except Exception as e: 
							print('ERROR:', e)
							self.stop() 

	def __startListener(self, key):
		Thread(target=self.__keyListener, args=(key,)).start()

	def addKeyListener(self, keycode, onPress=None, onRelease=None):
		'''
		each key can have multiple callbacks. You can add them through this
		'''
		if any([x.code == keycode for x in self.keys]):
			foundKey = self.__getKey(keycode)
			if onPress:
				foundKey.onPress.append(onPress)
			if onRelease:
				foundKey.onRelease.append(onRelease)
		else:
			newKey = Key(keycode, onPress, onRelease)
			self.keys.append(newKey)
			self.__startListener(newKey)

	def removeKeyListener(self, keycode, funcToRemove=None):
		'''
		if funcToRemove is None, then all the callback functions will be removed
		'''
		if any([x.code == keycode for x in self.keys]):
			foundKey = self.__getKey(keycode)
			if funcToRemove is None:
				foundKey.onPress = []
				foundKey.onRelease = []
			elif funcToRemove in foundKey.onPress:
				foundKey.onPress.pop(funcToRemove)
			elif funcToRemove in foundKey.onRelease:
				foundKey.onRelease.pop(funcToRemove)
		else:
			print('Error Removing Listener: listener for this key is not active')

	def __start(self):
		'''
		start the listener for the keys provided
		'''
		self.listening = True

		for x in self.keys:
			self.__startListener(x)

	def isHeld(self, keyCode):
		'''
		checks if the given key is held right now or not. returns true/false
		'''
		for x in self.keys:
			if keyCode == x.code:
				return x.held

		print('ERROR: You checked for a key (if it is being held) which has no listener. Key:', Key(keyCode).name)
		return False

	def stop(self):
		self.listening = False
		self.__exit()

	def __getKey(self, code):
		index = [i for i, x in enumerate(self.keys) if x.code == code][0]
		return None if index == None else self.keys[index]

	def __exit(self):
		print('\nStopping the Listener...\n')

class KeySimulator:

	def Tap(self, keyCode, tapDelay=0.05):
		'''
		press, wait, and release the key. delay is according to the tapDelay
		'''
		Thread(target=self.__tap, args=(keyCode, tapDelay)).start()

	def Type(self, string, tapDelay=0.05):
		'''
		Type the string. similar to calling Tap(keycode) for each individual key
		'''
		string = map(lambda y: y.lower(), list(string))

		for x in string:
			if x in vKeys.keys():
				self.__tap(vKeys[x], tapDelay)
			elif x == ' ':
				self.__tap(vKeys['space'], tapDelay)
			else:
				self.__tap(vKeys['.'], tapDelay)

	def __tap(self, keyCode, timeOut):
		
		win32api.keybd_event(keyCode, 0, 0, 0)
		time.sleep(timeOut)
		win32api.keybd_event(keyCode, 0, win32con.KEYEVENTF_KEYUP, 0) # release
