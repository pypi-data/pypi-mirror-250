import keyboard

def listenKeyboard():
    event = keyboard.read_event().name
    [ keyboard.press_and_release('backspace') for i in range(len(event)) ]
    return event