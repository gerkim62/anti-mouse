from mouse_listener import MouseListener
from input_window import InputWindow
from api_client import APIClient

def main():
    api_client = APIClient("YOUR_API_ENDPOINT")
    input_window = InputWindow(api_client)
    mouse_listener = MouseListener(input_window.show)
    
    mouse_listener.start()
    input_window.run()

if __name__ == "__main__":
    main()