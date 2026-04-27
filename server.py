import socket
import threading
import random
import tkinter as tk
from datetime import datetime

class TruthServer:
    def __init__(self, root):
        self.root = root
        self.root.title("Shared Truth Authority")
        self.root.geometry("400x350")
        
        # Core Concept: Shared State
        self.secret_number = random.randint(1, 10)
        self.state_lock = threading.Lock()

        # Visual Feedback Setup
        self.header = tk.Label(root, text="CORE AUTHORITY MONITOR", font=("Arial", 12, "bold"))
        self.header.pack(pady=10)
        
        self.status_indicator = tk.Label(root, text="LAST ACTION: WAITING", bg="gray", fg="white", font=("Arial", 10))
        self.status_indicator.pack(fill=tk.X, pady=5)
        
        self.log_area = tk.Text(root, state='disabled', height=12, width=45, bg="black", fg="green")
        self.log_area.pack(pady=10)

        # Start Networking Thread
        threading.Thread(target=self.start_server, daemon=True).start()

    def update_log(self, message):
        """Thread-safe UI update for logs."""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{timestamp} {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        
    def flash_indicator(self):
        """Flashes the UI indicator to show activity."""
        self.status_indicator.config(bg="blue", text="LAST ACTION: PACKET RECEIVED")
        self.root.after(300, lambda: self.status_indicator.config(bg="gray", text="LAST ACTION: LISTENING"))

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 5555))
        server_socket.listen(5)
        
        self.update_log(f"SERVER ONLINE. Secret Truth is: {self.secret_number}")
        
        while True:
            conn, addr = server_socket.accept()
            # Handle each incoming client guess in a new thread
            threading.Thread(target=self.process_client, args=(conn, addr), daemon=True).start()

    def process_client(self, conn, addr):
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                return
            
            # Flash UI upon data reception
            self.root.after(0, self.flash_indicator)
            
            # Data Protocol: Name:Guess
            name, guess_str = data.split(':')
            guess = int(guess_str)
            
            self.update_log(f"RECEIVED -> {name} guessed {guess}")

            # Protect the shared state during evaluation
            with self.state_lock:
                if guess == self.secret_number:
                    conn.send("WIN! You found the truth!".encode('utf-8'))
                    self.update_log(f"*** {name} WON! ***")
                    
                    # Dynamic State: Reset Truth
                    self.secret_number = random.randint(1, 10)
                    self.update_log(f"NEW TRUTH GENERATED: {self.secret_number}")
                else:
                    conn.send("INCORRECT! Try again.".encode('utf-8'))
                    
        except Exception as e:
            self.update_log(f"Protocol Error from {addr}: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TruthServer(root)
    root.mainloop()