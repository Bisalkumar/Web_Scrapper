import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

class FlexibleScraper(scrapy.Spider):
    name = "flexible"

    def start_requests(self):
        # Use attributes set by the GUI
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        data = response.css(self.css_selector).getall()

        domain_name = urlparse(self.url).netloc.replace("www.", "")
        base_filename = f"{domain_name}.{self.output_format}"
        self.filename = base_filename
        counter = 1
        while os.path.exists(self.filename):
            self.filename = f"{domain_name}{counter}.{self.output_format}"
            counter += 1
        
        if self.output_format == "txt":
            with open(self.filename, 'w') as f:
                for item in data:
                    f.write("%s\n" % item)
        elif self.output_format == "xlsx":
            df = pd.DataFrame(data, columns=[self.data_name])
            df.to_excel(self.filename, index=False)
        else:
            print("Invalid output format chosen.")
            return

        print(f"Data saved to {self.filename}")

def start_scraper():
    scraper.url = url_entry.get()
    scraper.data_name = data_name_entry.get()
    scraper.css_selector = css_selector_entry.get()
    scraper.output_format = output_format_var.get()

    process = CrawlerProcess()
    process.crawl(scraper)
    process.start()
    
    messagebox.showinfo("Info", f"Data saved to {scraper.filename}")

# Setup GUI
root = tk.Tk()
root.title("Web Scraper")

# URL Input
tk.Label(root, text="URL:").pack(padx=20, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=20, pady=5)

# Data Name Input
tk.Label(root, text="Data Name:").pack(padx=20, pady=5)
data_name_entry = tk.Entry(root, width=50)
data_name_entry.pack(padx=20, pady=5)

# CSS Selector Input
tk.Label(root, text="CSS Selector:").pack(padx=20, pady=5)
css_selector_entry = tk.Entry(root, width=50)
css_selector_entry.pack(padx=20, pady=5)

# Output Format
tk.Label(root, text="Output Format:").pack(padx=20, pady=5)
output_format_var = tk.StringVar(root)
output_format_var.set("txt")
tk.OptionMenu(root, output_format_var, "txt", "xlsx").pack(padx=20, pady=5)

# Start Button
tk.Button(root, text="Start Scraping", command=start_scraper).pack(padx=20, pady=20)

# Spider instance
scraper = FlexibleScraper()

root.mainloop()
