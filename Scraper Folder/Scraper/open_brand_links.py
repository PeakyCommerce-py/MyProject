import webbrowser
import time
import tkinter as tk
from tkinter import filedialog

# Load brand names from the text file
def load_brands(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Open multiple search links for a brand
def open_links(brand_name):
    search_terms = ["AB", "Distrubitör", "Leverantör", "Agent", "Sverige", "Distrubitor"]
    base_url = "https://www.google.com/search?q="
    for term in search_terms:
        url = f"{base_url}{brand_name} {term}"
        webbrowser.open_new_tab(url)
        time.sleep(0.5)  # Small delay to prevent opening tabs too quickly

class BrandSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brand Search App")
        self.current_index = 0
        self.brands = []

        self.label = tk.Label(root, text="Select a text file with brand names:")
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Brands", command=self.load_file)
        self.load_button.pack(pady=5)

        self.next_button = tk.Button(root, text="Next Brand", command=self.next_brand, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.brands = load_brands(file_path)
            self.current_index = 0
            if self.brands:
                self.next_button.config(state=tk.NORMAL)
                self.status_label.config(text=f"Loaded {len(self.brands)} brands. Click 'Next Brand' to start.")

    def next_brand(self):
        if self.current_index < len(self.brands):
            brand = self.brands[self.current_index]
            self.status_label.config(text=f"Opening links for {brand}...")
            open_links(brand)
            self.current_index += 1
        else:
            self.status_label.config(text="All brands processed.")
            self.next_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrandSearchApp(root)
    root.mainloop()
