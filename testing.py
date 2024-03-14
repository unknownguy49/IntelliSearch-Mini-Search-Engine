import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

google_api_key = "AIzaSyA_IOB5Bgn54cYiKodcxT0TtmDXhvSPvI4"
google_cx = "30661b3932b0d4a4c"
unsplash_api_key = "G-HoraLiKuHMyuED2DZDebPYVezv4z7NTrJg8zTe2Xg"

class SearchEngineUI:
    def __init__(self, master):
        self.master = master
        master.title("IntelliSearch")
        master.state('zoomed')
        self.master.configure(bg='white')
        
        tk.Label(master, text="IntelliSearch", font=('Helvetica', 20), bg='white').pack(pady=10)
        
        self.search_frame = tk.Frame(master, bg='white')
        self.search_frame.pack(pady=10)
        self.search_entry = tk.Entry(self.search_frame, width=50)
        self.search_entry.pack(pady=5, side=tk.LEFT, padx=5)
        
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.pack(pady=5, side=tk.LEFT, padx=5)
        
        self.image_button = tk.Button(self.search_frame, text="Search Images", command=self.search_images)
        self.image_button.pack(pady=5, side=tk.LEFT, padx=5)
        
        self.results_frame = tk.Frame(master, bg='white')
        self.results_frame.pack(pady=10)
        
        menubar = tk.Menu(master)
        menubar.add_command(label="About", command=self.open_about_page)
        master.config(menu=menubar)
    
    def search(self):
        query = self.search_entry.get()
        google_results = self.fetch_search_results(query, google_api_key, google_cx)
        if google_results:
            self.display_results(google_results)
    
    def search_images(self):
        query = self.search_entry.get()
        unsplash_results = self.fetch_image_results(query, unsplash_api_key)
        if unsplash_results:
            self.display_images(unsplash_results)
    
    def fetch_search_results(self, query, api_key, cx):
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(f"Error fetching search results: {response.status_code}")
            return None
    
    def fetch_image_results(self, query, api_key):
        url = f"https://api.unsplash.com/search/photos?page=1&per_page=10&query={query}&client_id={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(f"Error fetching image results: {response.status_code}")
            return None
    
    def display_results(self, results):
        self.clear_results_frame()
        if 'items' in results:
            items = results['items']
            for i, item in enumerate(items):
                title = item.get('title', '')
                link = item.get('link', '')
                description = item.get('snippet', '')
                tk.Label(self.results_frame, text=title, wraplength=500, justify='left', anchor='w').grid(row=i, column=0, sticky='w')
                tk.Label(self.results_frame, text=link, wraplength=500, justify='left', anchor='w').grid(row=i, column=1, sticky='w')
                tk.Label(self.results_frame, text=description, wraplength=500, justify='left', anchor='w').grid(row=i, column=2, sticky='w')
        else:
            self.handle_error("No search results found.")
    
    def display_images(self, image_results):
        self.clear_results_frame()
        for i, item in enumerate(image_results['results']):
            image_url = item.get('urls', {}).get('small', '')
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(self.results_frame, image=photo)
                label.image = photo
                label.grid(row=i, column=0, padx=5, pady=5)
            else:
                self.handle_error("Error fetching image data")
    
    def clear_results_frame(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
    
    def handle_error(self, message):
        messagebox.showerror("Error", message)
    
    def open_about_page(self):
        about_window = tk.Toplevel(self.master)
        about_window.title("About IntelliSearch")
        about_window.geometry("400x300")
        
        about_label = tk.Label(about_window, text="About IntelliSearch", font=("Helvetica", 16, "bold"))
        about_label.pack(pady=10)
        
        about_text = tk.Text(about_window, wrap="word", height=10)
        about_text.insert(tk.END, "This is a simple search engine created using Python and Tkinter.\n\n")
        about_text.insert(tk.END, "Features:\n")
        about_text.insert(tk.END, "- Fetches search results from Google Custom Search API.\n")
        about_text.insert(tk.END, "- Displays search results in a user-friendly interface.\n")
        about_text.pack(expand=True, fill="both", padx=20, pady=10)
        
        close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
        close_button.pack(pady=10)

# Create the main window
root = tk.Tk()
app = SearchEngineUI(root)
root.mainloop()
