
# inventory.py

import pandas as pd
import os

# CSV filename
FILE_NAME = "Inventory.csv"

# Check if CSV exists, else create one
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Product ID", "Product Name", "Quantity", "Price"])
    df.to_csv(FILE_NAME, index=False)

def load_inventory():
    return pd.read_csv(FILE_NAME)

def save_inventory(df):
    df.to_csv(FILE_NAME, index=False)

def add_product():
    df = load_inventory()
    print("\n--- Add New Product ---")
    pid = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    qty = int(input("Enter Quantity: "))
    price = float(input("Enter Price: ₹ "))

    df = df.append({
        "Product ID": pid,
        "Product Name": name,
        "Quantity": qty,
        "Price": price
    }, ignore_index=True)

    save_inventory(df)
    print("✅ Product added successfully!\n")

def view_inventory():

    df = load_inventory()
    print("\n--- Inventory List ---")
    if df.empty:
        print("No products found.")
    else:
        print(df.to_string(index=False))

def delete_product():
    df = load_inventory()
    print("\n--- Delete Product ---")
    pid = input("Enter Product ID to delete: ")

    if pid in df["Product ID"].values:
        df = df[df["Product ID"] != pid]
        save_inventory(df)
        print(f"✅ Product with ID '{pid}' deleted.")
    else:
        print("❌ Product ID not found.")

def update_quantity():
    df = load_inventory()
    print("\n--- Update Product Quantity ---")
    pid = input("Enter Product ID to update: ")

    if pid in df["Product ID"].values:
        new_qty = int(input("Enter new quantity: "))
        df.loc[df["Product ID"] == pid, "Quantity"] = new_qty
        save_inventory(df)
        print(f"✅ Quantity for product '{pid}' updated to {new_qty}.")
    else:
        print("❌ Product ID not found.")


def main():
    while True:
        print("\n====== Inventory Management System ======")
        print("1. Add Product")
        print("2. View Inventory")
        print("3. Delete Product")
        print("4. Update Product Quantity")
        print("5. Exit")

       

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_product()
        elif choice == '2':
            view_inventory()
        elif choice == '3':
            delete_product()
        elif choice == '4':
            update_quantity()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
                main()
