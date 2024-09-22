import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import json
from collections import Counter
from utils import get_tts_directory, list_json_files, is_valid_json

class LorcanaTTSManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Lorcana TTS Manager")
        self.geometry("600x600")
        self.configure(bg="lightgray")

        # Create Main Interface
        self.create_widgets()

        # Load Decklists
        self.tts_dir = get_tts_directory()
        self.load_decklists()

    def create_widgets(self):
        """Create the main widgets in the Tkinter interface."""
        # Decklist Label
        self.decklist_label = ttk.Label(self, text="Available Decklists:", background="lightgray", font=("Arial", 14))
        self.decklist_label.pack(pady=10)

        # Decklist Box
        self.decklist_box = tk.Listbox(self, width=60, height=10)
        self.decklist_box.pack(pady=10)
        self.decklist_box.bind('<<ListboxSelect>>', self.on_decklist_select)  # Bind selection event

        # Label for the directory path
        self.directory_label = ttk.Label(self, text="", background="lightgray", font=("Arial", 10))
        self.directory_label.pack(pady=5)

        # Button to Refresh Decklists
        self.refresh_button = ttk.Button(self, text="Refresh Decklists", command=self.load_decklists)
        self.refresh_button.pack(pady=5)

        # Separator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.pack(fill='x', pady=10)

        # Upload JSON Label
        self.upload_label = ttk.Label(self, text="Upload a New Decklist (.json):", background="lightgray", font=("Arial", 14))
        self.upload_label.pack(pady=10)

        # Upload Button
        self.upload_button = ttk.Button(self, text="Browse for JSON", command=self.browse_file)
        self.upload_button.pack(pady=5)

        # Text area to display Nickname counts
        self.nickname_display = scrolledtext.ScrolledText(self, width=70, height=15, wrap=tk.WORD)
        self.nickname_display.pack(pady=10)

    def load_decklists(self):
        """Load available decklists from the TTS directory."""
        self.decklist_box.delete(0, tk.END)  # Clear existing listbox content
        decklists = list_json_files(self.tts_dir)

        if not decklists:
            self.decklist_box.insert(tk.END, "No decklists found.")
            self.directory_label.config(text="Location: " + self.tts_dir)  # Show directory location
        else:
            for decklist in decklists:
                self.decklist_box.insert(tk.END, decklist)

            self.directory_label.config(text="Location: " + self.tts_dir)  # Show directory location

    def browse_file(self):
        """Browse for a JSON file and upload it, starting in the Downloads directory."""
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        file_path = filedialog.askopenfilename(
            title="Select a JSON Decklist",
            initialdir=downloads_path,  # Start in Downloads directory
            filetypes=[("JSON Files", "*.json")]
        )

        if file_path:
            # Check if the selected file is valid JSON
            if is_valid_json(file_path):
                file_name = os.path.basename(file_path)
                self.upload_decklist(file_name, file_path)
            else:
                messagebox.showerror("Invalid JSON", "The selected file is not a valid JSON decklist.")

    def on_decklist_select(self, event):
        """Handle selection of a decklist to display its Nickname counts."""
        selected_index = self.decklist_box.curselection()
        if selected_index:
            decklist_name = self.decklist_box.get(selected_index)
            decklist_path = os.path.join(self.tts_dir, decklist_name)
            try:
                # Load and count Nicknames
                with open(decklist_path, 'r') as f:
                    deck_data = json.load(f)
                    # Extract Nicknames from ContainedObjects
                    nicknames = []
                    if 'ObjectStates' in deck_data:
                        for state in deck_data['ObjectStates']:
                            if 'ContainedObjects' in state:
                                for card in state['ContainedObjects']:
                                    if 'Nickname' in card:
                                        nicknames.append(card['Nickname'])

                    nickname_counts = Counter(nicknames)
                    # Clear previous contents and display counts
                    self.nickname_display.delete(1.0, tk.END)
                    if nickname_counts:
                        for nickname, count in nickname_counts.items():
                            self.nickname_display.insert(tk.END, f"{count}x {nickname}\n")
                    else:
                        self.nickname_display.insert(tk.END, "No nicknames found in this decklist.")

            except json.JSONDecodeError:
                messagebox.showerror("Error", "Failed to decode JSON. Please check the file format.")


    def upload_decklist(self, file_name, file_path):
        """Upload the selected JSON file (copy it to the TTS Saves directory)."""
        destination_path = os.path.join(self.tts_dir, file_name)

        try:
            # Copy the file to the TTS Saves directory
            with open(file_path, 'r') as f:
                deck_data = json.load(f)

            with open(destination_path, 'w') as f:
                json.dump(deck_data, f, indent=4)

            messagebox.showinfo("Success", f"Decklist '{file_name}' uploaded successfully!")
            self.load_decklists()  # Refresh decklist box

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload decklist: {e}")

if __name__ == "__main__":
    app = LorcanaTTSManagerApp()
    app.mainloop()

