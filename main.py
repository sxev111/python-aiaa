import tkinter as tk
from tkinter import scrolledtext, messagebox
import openai
from config import API_KEY, MODEL, TEMPERATURE
import threading

class AIAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python AI Assistant")
        self.root.geometry("800x600")
        
        # Set API key
        openai.api_key = API_KEY
        
        # Create GUI elements
        self.setup_ui()
        self.conversation_history = []
        
    def setup_ui(self):
        # Title label
        title_label = tk.Label(self.root, text="AI Assistant", font=("Arial", 16, "bold"))
        title_label.pack(padx=10, pady=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, height=20, bg="#f0f0f0"
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Input field
        self.input_field = tk.Entry(input_frame, width=80)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        self.send_button = tk.Button(
            input_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_button = tk.Button(
            input_frame, text="Clear", command=self.clear_chat
        )
        self.clear_button.pack(side=tk.LEFT)
        
    def send_message(self):
        user_input = self.input_field.get()
        if not user_input.strip():
            messagebox.showwarning("Empty Input", "Please enter a message!")
            return
            
        # Display user message
        self.display_message(f"You: {user_input}", "user")
        self.conversation_history.append({"role": "user", "content": user_input})
        self.input_field.delete(0, tk.END)
        self.send_button.config(state=tk.DISABLED)
        
        # Get AI response in a separate thread
        thread = threading.Thread(target=self.get_ai_response)
        thread.daemon = True
        thread.start()
        
    def get_ai_response(self):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=self.conversation_history,
                temperature=TEMPERATURE
            )
            ai_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            self.display_message(f"Assistant: {ai_message}", "assistant")
        except Exception as e:
            self.display_message(f"Error: {str(e)}", "error")
        finally:
            self.send_button.config(state=tk.NORMAL)
            
    def display_message(self, message, sender="user"):
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "user":
            self.chat_display.insert(tk.END, message + "\n", "user_tag")
        elif sender == "assistant":
            self.chat_display.insert(tk.END, message + "\n", "assistant_tag")
        else:
            self.chat_display.insert(tk.END, message + "\n", "error_tag")
        
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.see(tk.END)
        
        # Configure tags
        self.chat_display.tag_config("user_tag", foreground="blue")
        self.chat_display.tag_config("assistant_tag", foreground="green")
        self.chat_display.tag_config("error_tag", foreground="red")
        
        self.chat_display.config(state=tk.DISABLED)
        
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.conversation_history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = AIAssistantApp(root)
    root.mainloop()