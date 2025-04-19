import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import bot  # Import the bot logic
import time
import pyautogui
import os # Import os module to construct path
import sys # Add sys import at the top

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WhatsApp Bot")
        self.geometry("600x650")

        # --- Set Window Icon (PyInstaller compatible) ---
        try:
            # Determine base path whether running as script or bundled app
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                # Running in a PyInstaller bundle
                base_path = sys._MEIPASS
            else:
                # Running as a normal Python script
                base_path = os.path.dirname(os.path.abspath(__file__))

            icon_path = os.path.join(base_path, "icon.png")

            if os.path.exists(icon_path):
                icon_image = tk.PhotoImage(file=icon_path)
                self.iconphoto(False, icon_image)
                print(f"Icon loaded successfully from: {icon_path}") # Added for debugging
            else:
                 print(f"Warning: Icon file not found at '{icon_path}'. Looked in base path: {base_path}")
        except tk.TclError as e:
            print(f"Error loading icon '{icon_path}': {e}. Make sure it's a valid PNG file.")
        except Exception as e:
             print(f"An unexpected error occurred during icon loading: {e}") # Catch other potential errors
        # ----------------------------------------------

        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        self.contacts_filepath = None
        self.bot_thread = None
        self.stop_event = threading.Event()

        # --- Configure grid layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Log area takes remaining space

        # --- File Selection Frame ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        self.select_button = ctk.CTkButton(self.file_frame, text="Select Contacts CSV", command=self.select_file)
        self.select_button.grid(row=0, column=0, padx=10, pady=10)

        self.filepath_label = ctk.CTkLabel(self.file_frame, text="No file selected", anchor="w")
        self.filepath_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Message Input Frame ---
        self.message_frame = ctk.CTkFrame(self)
        self.message_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.message_frame.grid_columnconfigure(0, weight=1)

        self.message_label = ctk.CTkLabel(self.message_frame, text="Message:", anchor="w")
        self.message_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # Use a font that supports color emoji (like Segoe UI Emoji on Windows)
        emoji_font = ("Segoe UI Emoji", 13) # Adjust size as needed
        self.message_entry = ctk.CTkTextbox(self.message_frame, height=100, font=emoji_font)
        self.message_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.message_entry.insert("1.0", "Hello [Name]! This is a test message.") # Example message

        # --- Control Frame ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(self.control_frame, text="Start Sending", command=self.start_sending)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.stop_button = ctk.CTkButton(self.control_frame, text="Stop Sending", command=self.stop_sending, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Log Frame ---
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.log_frame.grid_rowconfigure(1, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self.log_frame, text="Status: Idle", anchor="w")
        self.status_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.log_textbox = ctk.CTkTextbox(self.log_frame, state="disabled", wrap="word") # Read-only
        self.log_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Contacts CSV File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filepath:
            self.contacts_filepath = filepath
            self.filepath_label.configure(text=filepath)
            self.log_message(f"Selected contact file: {filepath}")
        else:
            self.contacts_filepath = None
            self.filepath_label.configure(text="No file selected")

    def log_message(self, message):
        """Appends a message to the log text box in a thread-safe way."""
        # Use 'after' to schedule the GUI update on the main thread
        def append_log():
            self.log_textbox.configure(state="normal") # Enable writing
            self.log_textbox.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
            self.log_textbox.configure(state="disabled") # Disable again
            self.log_textbox.see(tk.END) # Scroll to the end
        self.after(0, append_log)

    def update_status(self, status):
        """Updates the status label in a thread-safe way."""
        def set_status():
             self.status_label.configure(text=f"Status: {status}")
        self.after(0, set_status)

    def start_sending(self):
        if not self.contacts_filepath:
            messagebox.showerror("Error", "Please select a contacts CSV file first.")
            return
            
        message_template = self.message_entry.get("1.0", tk.END).strip()
        if not message_template:
             messagebox.showerror("Error", "Please enter a message to send.")
             return

        if self.bot_thread and self.bot_thread.is_alive():
            messagebox.showwarning("Warning", "Bot is already running.")
            return

        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", tk.END)
        self.log_textbox.configure(state="disabled")

        self.stop_event.clear() # Reset stop event for new run
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.update_status("Starting...")

        # Run bot logic in a separate thread
        self.bot_thread = threading.Thread(
            target=self.run_bot_thread, 
            args=(self.contacts_filepath, message_template), 
            daemon=True # Allows app to exit even if thread is running
        )
        self.bot_thread.start()

    def stop_sending(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.log_message("Stop requested. Waiting for current message to finish...")
            self.update_status("Stopping...")
            self.stop_event.set() # Signal the thread to stop
            # Note: This won't immediately interrupt pywhatkit, 
            # but will prevent sending more messages after the current one.
            self.stop_button.configure(state="disabled") # Prevent multiple clicks
        else:
            self.log_message("Bot is not currently running.")
            self.update_status("Idle")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

    def run_bot_thread(self, filepath, message_template):
        """Worker function to run the bot logic."""
        try:
            self.log_message("Loading contacts...")
            contacts = bot.load_contacts(filepath)
            if contacts is None:
                self.log_message("Failed to load contacts. Check bot.log for details.")
                self.update_status("Error - Check Logs")
                # Safely re-enable start button from worker thread
                self.after(0, lambda: self.start_button.configure(state="normal"))
                self.after(0, lambda: self.stop_button.configure(state="disabled"))
                return
            
            self.log_message(f"Loaded {len(contacts)} contacts.")

            total_contacts = len(contacts)
            for i, contact in enumerate(contacts):
                if self.stop_event.is_set():
                    self.log_message("Stop signal received. Aborting remaining messages.")
                    self.update_status("Stopped by user")
                    break # Exit the loop

                phone_number = contact['phone_number']
                name = contact.get('name', phone_number)
                
                # Personalize message if [Name] placeholder exists
                personalized_message = message_template.replace("[Name]", name) 

                status = f"Sending message {i+1}/{total_contacts} to {name} ({phone_number})..."
                self.update_status(status)
                self.log_message(status)
                
                try:
                    # Note: pywhatkit requires interaction (QR scan) on first run
                    # It will block this thread until sent or timeout/error
                    bot.pywhatkit.sendwhatmsg_instantly(
                        phone_no=phone_number, 
                        message=personalized_message,
                        wait_time=20, # Increased wait time for QR scan / loading
                        tab_close=True, 
                        close_time=3
                    )
                    pyautogui.press('enter')
                    success_msg = f"Message sent successfully to {name} ({phone_number})."
                    self.log_message(success_msg)
                        
                except Exception as e:
                    # Log error both to file (via bot module's logger) and GUI
                    error_msg = f"Failed to send message to {name} ({phone_number}): {e}"
                    bot.logging.error(error_msg) # Use bot's logger for file logging
                    self.log_message(error_msg)
                    # Don't stop the whole process for one error, continue to next contact
                
                # Wait before sending the next message if not the last one and not stopping
                if i < total_contacts - 1 and not self.stop_event.is_set():
                    delay = 18 # Default delay from bot.py
                    wait_notice = f"Waiting {delay} seconds before next message..."
                    self.log_message(wait_notice)
                    # Check stop event periodically during sleep
                    for _ in range(delay):
                        if self.stop_event.is_set():
                            break
                        time.sleep(1)
                    if self.stop_event.is_set():
                         self.log_message("Stop signal received during delay. Aborting.")
                         self.update_status("Stopped by user")
                         break # Exit outer loop
                         
            else: # This block runs if the loop completed without a break
                if not self.stop_event.is_set():
                     final_msg = "Finished sending all messages."
                     self.log_message(final_msg)
                     self.update_status("Finished")

        except Exception as e:
            # Catch unexpected errors during thread execution
            critical_error = f"An unexpected error occurred in the bot thread: {e}"
            bot.logging.exception(critical_error) # Log exception details to file
            self.log_message(critical_error)
            self.update_status("Critical Error - Check Logs")
        finally:
             # Always re-enable start button and disable stop button in the end, using 'after'
            def final_gui_updates():
                self.start_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                if self.stop_event.is_set(): # Reflect final status if stopped
                    self.update_status("Stopped")
            self.after(0, final_gui_updates)

# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop() 