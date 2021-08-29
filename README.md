# PyKeyboard32
Python keyboard listener and key simulator using the win32 api.

The listener is super fast, as opposed to existing solutions such as pynput where very fast input can overwhelm the stream and cause some delays. (and which i assume is also single threaded so keys are processed in the order they are pressed).

The purpose of this was to capture input as fast as possible, so that input could be streamed over a network, to play games remotely. (just pass in your callback function that sends data over a socket).

Each key listener runs on a separate thread, and hence the response is immediate!

**Listener:**

```python
from PyKeyboard32 import Listener, vKeys
# vKeys is the dictionary of virtual keycodes

# creates a listener for all keys, with same global callback functions for all.
listener = Listener(onPress=onPressCallback, onRelease=onReleaseCallback)

# to specify the keys, you could use a list. this listener only listens for 'a' and left control key.
# set debug to true to print when keys are pressed and released
listener2 = Listener(keys=[vKeys['a'], vKeys['ctrl_l']], onPress=onPressCallback, onRelease=onReleaseCallback, debug=True)

# you can also designate a stopkey to stop the listener. The default is backspace. 
# This is to make sure the threads do not keep on running in the background once the program ends.
listener3 = Listener(stopKey=[vKeys['esc']])

# each key can have multiple callbacks
# this adds another onpress function to the key 'a'. onRelease functions stay the same
# or can be used to make a listener for a new key, that was not specified in the constructor
listener.addKeyListener(vKeys['a'], onPress=secondCallback, onRelease=None)

# removes the provided callback function. if no function is provided, removes all functions for that key
listener.removeKeyListener(vKeys['a'], funcToBeRemoved)

# to check if a key is being held at the moment, you can use this
# helpful when you want to check for key combos like *ctrl+n*, for example
listener.isHeld(vKeys['a'])
```

**Callback Function for listener:**

```python
# each callback function receives two arguments: the listener object that is active, and the key object. 
# with the listener, you can check for held keys
def pressCallback(listener, key):
  pass
```

**Key class:**

1. Name of the key (key.name)
2. Its virtual keycode  (key.code)
3. Flag for when it is held (key.held)
4. list of onpress and onrelease functions (key.onPress and key.onRelease)

**KeySimulator:**

```python
from PyKeyboard32 import KeySimulator, vKeys
# use vKeys to get the virtual keycodes

sim = KeySimulator()

# To press and release a key
sim.tap(vKeys['d'])

# to press and release a key with some delay/timeout in seconds
# presses, holds, and releases the spacebar for one second
sim.tap(vKeys['space'], 1)

# to type a string
# types the given string where each key takes 0.01 seconds
# timeout is optional. default is 0.05
sim.type('Hello world', 0.01)
```

**Listener Example to open task manager**

```python
from PyKeyboard32 import Listener, KeySimulator, vKeys

# called when d is pressed
def openTaskManager(li, key):
	if li.isHeld(vKeys['a']):
		sim.Tap(vKeys['ctrl_l'])
		sim.Tap(vKeys['shift'])
		sim.Tap(vKeys['esc'])


# listen for 'a' and 'd'
# open task manager when you press a, followed by d. (a + d)
li = Listener(keys=[vKeys['a'], vKeys['d']], debug=True)
# we only need a callback for 'd' since 'a' needs only a listener but no callback (as it doesnt need to do anything).
li.addKeyListener(vKeys['d'], onPress=openTaskManager)

sim = KeySimulator()
```
