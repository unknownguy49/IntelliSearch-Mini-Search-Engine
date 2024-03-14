import tkinter as tk
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox

api_key = "AIzaSyA_IOB5Bgn54cYiKodcxT0TtmDXhvSPvI4"
cx = "30661b3932b0d4a4c"

class SearchEngineUI:
    def __init__(self, master):
        self.master = master
        master.title("IntelliSearch")
        master.state('zoomed')
        # Choose a Design:
        # Layout and color scheme can be adjusted here
        self.master.configure(bg='white')

        # Incorporate Branding:
        tk.Label(master, text="IntelliSearch", font=('Helvetica', 20), bg='white').pack(pady=10)

        # Design Search Bar:
        self.search_frame = tk.Frame(master, bg='white')
        self.search_frame.pack(pady=10)
        self.search_entry = tk.Entry(self.search_frame, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.pack(pady=5)

        # Display Search Results:
        self.results_frame = tk.Frame(master, bg='white')
        self.results_frame.pack(pady=10)

        # Menu bar
        menubar = tk.Menu(master)
        menubar.add_command(label="About", command=self.open_about_page)
        master.config(menu=menubar)

    def search(self):
        query = self.search_entry.get()
        results = self.fetch_search_results(query, api_key, cx)
        if results:
            self.display_results(results)

    def fetch_search_results(self, query, api_key, cx):
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(f"Error fetching search results: {response.status_code}")
            return None

    def display_results(self, results):
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

    def handle_error(self, message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message)
        error_label.pack(padx=20, pady=10)

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