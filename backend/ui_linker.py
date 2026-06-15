import socket

def set_chloro_ui_state(state_name):
    """Signals the Tkinter holographic HUD to shift visual profiles."""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 18788))  # Points to Chloro's UI port
        client.sendall(state_name.encode('utf-8'))
        client.close()
    except ConnectionRefusedError:
        # If the UI window isn't open, this prevents the backend from crashing
        pass