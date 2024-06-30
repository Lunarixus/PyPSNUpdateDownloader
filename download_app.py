# Copyright (C) Lunarixus 2024
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import threading
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSN Update Package Downloader")
        self.root.geometry("700x350")
        self.root.resizable(False, False)

        self.title_id_label = tk.Label(root, text="Enter Title ID:")
        self.title_id_label.pack(pady=5)

        self.title_id_entry = tk.Entry(root, width=50)
        self.title_id_entry.pack(pady=5)

        self.download_button = tk.Button(root, text="Get Packages", command=self.start_download)
        self.download_button.pack(pady=5)

        self.package_listbox = tk.Listbox(root, width=100, height=10)
        self.package_listbox.pack(pady=10)
        self.package_listbox.bind('<Double-1>', self.on_package_double_click)

        self.progress = ttk.Progressbar(root, length=600, mode='determinate')
        self.progress.pack(pady=10)

    def start_download(self):
        title_id = self.title_id_entry.get().strip()
        if not title_id:
            messagebox.showerror("Input Error", "Please enter a valid Title ID.")
            return

        self.download_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.package_listbox.delete(0, tk.END)
        threading.Thread(target=self.download_game, args=(title_id,)).start()

    def download_game(self, title_id):
        try:
            xml_url = f"https://a0.ww.np.dl.playstation.net/tpl/np/{title_id}/{title_id}-ver.xml"
            self.update_progress(5)
            response = requests.get(xml_url, verify=False)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            # Extract game name
            game_name_element = root.find(".//paramsfo/TITLE")
            game_name = game_name_element.text if game_name_element is not None else "Unknown Game"
            
            packages = root.findall(".//package")
            if not packages:
                self.handle_error("No packages found for the given Title ID.")
                return

            self.root.after(0, self.show_packages, packages, game_name)
        except requests.exceptions.RequestException as e:
            self.handle_error(f"Request error: {e}")
        except ET.ParseError:
            self.handle_error("Failed to parse response, the game might not have updates.")

    def show_packages(self, packages, game_name):
        self.packages = packages
        self.package_listbox.insert(tk.END, f"Game: {game_name}")
        for package in packages:
            version = package.attrib.get('version')
            size = int(package.attrib.get('size', 0)) // (1024 * 1024)
            ps3_system_ver = package.attrib.get('ps3_system_ver', 'Unknown')
            self.package_listbox.insert(tk.END, f"Version: {version}, Size: {size} MB, PS3 System Version: {ps3_system_ver}")
        self.download_button.config(state=tk.NORMAL)

    def on_package_double_click(self, event):
        selected_index = self.package_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            package = self.packages[selected_index[0] - 1]
            package_url = package.attrib['url']
            self.save_as_dialog(package_url)

    def save_as_dialog(self, package_url):
        parsed_url = urlparse(package_url)
        package_name = parsed_url.path.split('/')[-1]

        save_path = filedialog.asksaveasfilename(defaultextension=".pkg", initialfile=package_name, title="Save As")
        if save_path:
            threading.Thread(target=self.download_file, args=(package_url, save_path)).start()
        else:
            self.handle_error("Save location not selected.")

    def download_file(self, url, save_path):
        try:
            response = requests.get(url, stream=True, verify=False)
            response.raise_for_status()
            total_length = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.update_progress(10 + (downloaded / total_length) * 90 if total_length else 100)
            messagebox.showinfo("Download Complete", f"The update package has been downloaded successfully as {save_path}.")
        except requests.exceptions.RequestException as e:
            self.handle_error(f"Download error: {e}")

    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()

    def handle_error(self, message):
        self.update_progress(0)
        messagebox.showerror("Error", message)
        self.download_button.config(state=tk.NORMAL)
