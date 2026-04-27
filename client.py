import socket
import tkinter as tk
from tkinter import messagebox

class TruthClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Shared Truth Player")
        self.root.geometry("300x250")
        
        tk.Label(root, text="PLAYER NODE", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(root, text="Your Identifier (Name):").pack()
        self.name_entry = tk.Entry(root, justify="center")
        self.name_entry.pack(pady=5)
        
        tk.Label(root, text="Your Guess (1-10):").pack()
        self.guess_entry = tk.Entry(root, justify="center")
        self.guess_entry.pack(pady=5)
        
        self.submit_btn = tk.Button(root, text="TRANSMIT GUESS", command=self.send_guess, bg="lightblue")
        self.submit_btn.pack(pady=15)
        
        self.response_label = tk.Label(root, text="Awaiting...", fg="gray")
        self.response_label.pack()

    def send_guess(self):
        name = self.name_entry.get().strip()
        guess = self.guess_entry.get().strip()
        
        if not name or not guess:
            messagebox.showwarning("Input Error", "Provide both a name and a guess.")
            return
            
        if ':' in name:
            messagebox.showwarning("Format Error", "Name cannot contain the ':' character.")
            return

        # Network transmission 
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(3)  # Timeout to prevent freezing
            client_socket.connect(('127.0.0.1', 5555))
            
            # Format: Name:Guess
            payload = f"{name}:{guess}"
            client_socket.send(payload.encode('utf-8'))
            
            response = client_socket.recv(1024).decode('utf-8')
            
            # Visual update based on win/loss
            if "WIN" in response:
                self.response_label.config(text=response, fg="green", font=("Arial", 10, "bold"))
            else:
                self.response_label.config(text=response, fg="red", font=("Arial", 10))
                
        except Exception as e:
            self.response_label.config(text=f"Connection Failed: {e}", fg="red")
        finally:
            client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TruthClient(root)
    root.mainloop()