
# inventory_gui.py

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd
import os

FILE_NAME = "Inventory.csv"

# Create CSV if not exists
if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
    df = pd.DataFrame(columns=["Product ID", "Product Name", "Quantity", "Price"])
    df.to_csv(FILE_NAME, index=False)


def load_inventory():
    return pd.read_csv(FILE_NAME)

def save_inventory(df):
    df.to_csv(FILE_NAME, index=False)

def add_product():
    pid = entry_id.get()
    name = entry_name.get()
    qty = entry_qty.get()
    price = entry_price.get()

    if not (pid and name and qty and price):
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        qty = int(qty)
        price = float(price)
    except ValueError:
        messagebox.showerror("Error", "Quantity must be integer, Price must be number.")
        return

    df = load_inventory()
    new_row = pd.DataFrame([{
        "Product ID": pid,
        "Product Name": name,
        "Quantity": qty,
        "Price": price
        }])

    df = pd.concat([df, new_row], ignore_index=True)

    save_inventory(df)
    messagebox.showinfo("Success", "✅ Product added successfully!")
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    entry_price.delete(0, tk.END)

def view_inventory():
    df = load_inventory()
    if df.empty:
        messagebox.showinfo("Inventory", "No products found.")
    else:
        top = tk.Toplevel(root)
        top.title("Inventory List")
        text = tk.Text(top, width=80, height=20)
        text.pack()
        text.insert(tk.END, df.to_string(index=False))

def delete_product():
    pid = entry_id.get()
    df = load_inventory()
    if pid in df["Product ID"].values:
        df = df[df["Product ID"] != pid]
        save_inventory(df)
        messagebox.showinfo("Success", f"✅ Product with ID '{pid}' deleted.")
    else:
        messagebox.showerror("Error", "❌ Product ID not found.")
def show_dashboard():
    df = load_inventory()

    if df.empty:
        messagebox.showinfo("Dashboard", "Inventory is empty.")
        return

    total_products = len(df)
    total_quantity = df["Quantity"].sum()
    total_value = (df["Quantity"] * df["Price"]).sum()
    low_stock = df[df["Quantity"] < 5]

    # Create a new window
    dash = tk.Toplevel(root)
    dash.title("Inventory Dashboard")

    info = (
        f"📦 Total Products: {total_products}\n"
        f"📊 Total Quantity in Stock: {total_quantity}\n"
        f"💰 Total Inventory Value: ₹ {total_value:.2f}\n"
        f"⚠️ Low Stock (Qty < 5): {len(low_stock)}"
    )
    tk.Label(dash, text=info, justify="left", font=("Arial", 12)).pack(padx=10, pady=10)

    # Plot Bar Chart
    plt.figure(figsize=(6, 4))
    plt.bar(df["Product Name"], df["Quantity"], color='skyblue')
    plt.title("Product Quantities")
    plt.xlabel("Product Name")
    plt.ylabel("Quantity")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# GUI layout
root = tk.Tk()
root.title("Inventory Management System")



tk.Label(root, text="Product ID").grid(row=0, column=0)
tk.Label(root, text="Product Name").grid(row=1, column=0)
tk.Label(root, text="Quantity").grid(row=2, column=0)
tk.Label(root, text="Price").grid(row=3, column=0)

entry_id = tk.Entry(root)
entry_name = tk.Entry(root)
entry_qty = tk.Entry(root)
entry_price = tk.Entry(root)

entry_id.grid(row=0, column=1)
entry_name.grid(row=1, column=1)
entry_qty.grid(row=2, column=1)
entry_price.grid(row=3, column=1)

tk.Button(root, text="Add Product", command=add_product).grid(row=4, column=0, pady=10)
tk.Button(root, text="View Inventory", command=view_inventory).grid(row=4, column=1)
tk.Button(root, text="Delete Product", command=delete_product).grid(row=5, column=0)
tk.Button(root, text="Exit", command=root.quit).grid(row=5, column=1)
tk.Button(root, text="Open Dashboard", command=show_dashboard).grid(row=7, column=0, columnspan=2, pady=10)

# Delete Product Section
tk.Label(root, text="Enter Product ID to Delete:").grid(row=5, column=0)
entry_delete = tk.Entry(root)
entry_delete.grid(row=5, column=1)

def delete_product():
    pid = entry_delete.get().strip()
    if not pid:
        messagebox.showerror("Error", "Please enter a Product ID to delete.")
        return

    df = load_inventory()
    if pid in df["Product ID"].astype(str).values:
        df = df[df["Product ID"].astype(str) != pid]
        save_inventory(df)
        messagebox.showinfo("Deleted", f"✅ Product with ID '{pid}' deleted.")
        entry_delete.delete(0, tk.END)
    else:
        messagebox.showerror("Error", f"❌ Product ID '{pid}' not found.")

tk.Button(root, text="Delete Product", command=delete_product).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
