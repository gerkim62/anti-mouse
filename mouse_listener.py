from pynput import mouse

class MouseListener:
    def __init__(self, callback):
        self.callback = callback
        self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)

    def on_move(self, x, y):
        self.callback()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.callback()

    def start(self):
        self.listener.start()