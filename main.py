import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import pandas as pd

tree = None  # Define the tree variable globally

def scan_traffic():
    try:
        # Run train_model.py to train the model
        subprocess.Popen(["python", "train_model.py"])
        # Run capture_traffic.py and preprocess_data.py
        subprocess.Popen(["python", "capture_traffic.py"])
        subprocess.Popen(["python", "preprocess_data.py"])
        messagebox.showinfo("Scan Complete", "Traffic capture, preprocessing, and model training completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def load_traffic_data():
    global tree  # Access the globally defined tree variable
    try:
        df = pd.read_csv('captured_traffic.csv')
        if df.empty:
            messagebox.showwarning("No Data", "No traffic data available.")
            return
        for index, row in df.iterrows():
            tree.insert("", "end", values=(row['src_ip'], row['dst_ip'], row['src_port'], row['dst_port'], row['protocol'], row['length']))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def optimize_traffic():
    try:
        subprocess.Popen(["python", "optimize_traffic.py"])
        messagebox.showinfo("Traffic Optimization", "Traffic optimization completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    global tree  # Access the globally defined tree variable
    root = tk.Tk()
    root.title("WiFi Traffic Optimization Tool")

    def show_scan_page():
        scan_frame.grid(row=0, column=0, sticky="nsew")
        display_frame.grid_forget()

    def show_display_page():
        display_frame.grid(row=0, column=0, sticky="nsew")
        scan_frame.grid_forget()
        load_traffic_data()

    def show_optimize_page():
        optimize_traffic()

    # Scan Page
    scan_frame = tk.Frame(root)
    tk.Button(scan_frame, text="Scan", command=scan_traffic).pack(pady=20)
    #tk.Button(scan_frame, text="Show Traffic", command=show_display_page).pack()

    # Display Traffic Page
    display_frame = tk.Frame(root)
    tree = ttk.Treeview(display_frame, columns=("Source IP", "Destination IP", "Source Port", "Destination Port", "Protocol", "Length"))
    tree.heading("#0", text="Index")
    tree.heading("Source IP", text="Source IP")
    tree.heading("Destination IP", text="Destination IP")
    tree.heading("Source Port", text="Source Port")
    tree.heading("Destination Port", text="Destination Port")
    tree.heading("Protocol", text="Protocol")
    tree.heading("Length", text="Length")
    tree.pack(fill="both", expand=True)
    #tk.Button(display_frame, text="Optimize Traffic", command=show_optimize_page).pack()
    #tk.Button(display_frame, text="Back", command=show_scan_page).pack()

    show_scan_page()  # Show the Scan page initially

    root.mainloop()

if __name__ == "__main__":
    main()
