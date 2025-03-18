import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Language dictionaries
LANGUAGES = {
    'English': {
        'title': 'Shop Management System',
        'inventory': 'Inventory',
        'sales': 'Sales',
        'add_item': 'Add Item',
        'name': 'Name:',
        'quantity': 'Quantity:',
        'price': 'Price:',
        'add_button': 'Add Item',
        'current_inventory': 'Current Inventory',
        'remove_item': 'Remove Item',
        'item_id': 'Item ID:',
        'remove_button': 'Remove Item',
        'refresh': 'Refresh',
        'clear_db': 'Clear Database',
        'record_sale': 'Record Sale',
        'sale_history': 'Sales History',
        'total_sales': 'Total Sales: $',
        'confirm': 'Confirm',
        'clear_confirm': 'Are you sure you want to clear all data? This cannot be undone!',
        'success': 'Success',
        'error': 'Error',
        'db_cleared': 'Database cleared successfully',
        'fill_fields': 'Please fill all fields',
        'numbers_only': 'Quantity and price must be numbers',
        'positive_numbers': 'Quantity and price must be positive',
        'item_added': 'Item added successfully',
        'enter_id': 'Please enter an item ID',
        'id_number': 'Item ID must be a number',
        'item_removed': 'Item removed successfully',
        'item_not_found': 'Item not found',
        'not_enough': 'Not enough items in stock',
        'sale_recorded': 'Sale recorded successfully'
    },
    'Amharic': {
        'title': 'የመደብር አስተዳደር ስርዓት',
        'inventory': 'መጋዘን',
        'sales': 'ሽያጮች',
        'add_item': 'እቃ መጨመር',
        'name': 'ስም:',
        'quantity': 'ቁጥር:',
        'price': 'ዋጋ:',
        'add_button': 'እቃ ጨምር',
        'current_inventory': 'አሁን ያለው መጋዘን',
        'remove_item': 'እቃ መውጣት',
        'item_id': 'የእቃ መለያ:',
        'remove_button': 'እቃ አውጣ',
        'refresh': 'አዲስ አድርግ',
        'clear_db': 'ዳታቤዝ አፅድ',
        'record_sale': 'ሽያጭ መመዝገብ',
        'sale_history': 'የሽያጭ ታሪክ',
        'total_sales': 'ጠቅላላ ሽያጭ: ብር ',
        'confirm': 'ያረጋግጡ',
        'clear_confirm': 'ሁሉንም ዳታ መፈረስ ይፈልጋሉ? ይህ መፍታት አይቻልም!',
        'success': 'ተሳካ',
        'error': 'ስህተት',
        'db_cleared': 'ዳታቤዝ በተሳካ ሁኔታ ተፈርሷል',
        'fill_fields': 'እባክዎ ሁሉንም መስኮች ይሙሉ',
        'numbers_only': 'ቁጥር እና ዋጋ ቁጥሮች መሆን አለባቸው',
        'positive_numbers': 'ቁጥር እና ዋጋ አዎንታዊ መሆን አለባቸው',
        'item_added': 'እቃ በተሳካ ሁኔታ ተጨምሯል',
        'enter_id': 'እባክዎ የእቃ መለያ ይፃፉ',
        'id_number': 'የእቃ መለያ ቁጥር መሆን አለባቸው',
        'item_removed': 'እቃ በተሳካ ሁኔታ ተወግዷል',
        'item_not_found': 'እቃ አልተገኘም',
        'not_enough': 'በመጋዘን ውስጥ በቂ እቃዎች የሉም',
        'sale_recorded': 'ሽያጭ በተሳካ ሁኔታ ተመዝግቧል'
    }
}

current_language = 'English'

def update_language(*args):
    global current_language
    current_language = language_var.get()
    update_ui_text()

def update_ui_text():
    lang = LANGUAGES[current_language]
    
    # Update window title
    root.title(lang['title'])
    
    # Update notebook tabs
    notebook.tab(0, text=lang['inventory'])
    notebook.tab(1, text=lang['sales'])
    
    # Update inventory frame
    add_frame.configure(text=lang['add_item'])
    name_label.configure(text=lang['name'])
    quantity_label.configure(text=lang['quantity'])
    price_label.configure(text=lang['price'])
    add_button.configure(text=lang['add_button'])
    list_frame.configure(text=lang['current_inventory'])
    
    # Update treeview headers
    tree.heading("ID", text=lang['item_id'])
    tree.heading("Name", text=lang['name'])
    tree.heading("Quantity", text=lang['quantity'])
    tree.heading("Price", text=lang['price'])
    
    # Update remove frame
    remove_frame.configure(text=lang['remove_item'])
    remove_id_label.configure(text=lang['item_id'])
    remove_button.configure(text=lang['remove_button'])
    
    # Update buttons
    refresh_button.configure(text=lang['refresh'])
    clear_db_button.configure(text=lang['clear_db'])
    
    # Update sales frame
    sales_frame_top.configure(text=lang['record_sale'])
    sale_id_label.configure(text=lang['item_id'])
    sale_quantity_label.configure(text=lang['quantity'])
    record_sale_button.configure(text=lang['record_sale'])
    history_frame.configure(text=lang['sale_history'])
    
    # Update sales treeview headers
    sales_tree.heading("ID", text=lang['item_id'])
    sales_tree.heading("Item", text=lang['name'])
    sales_tree.heading("Quantity", text=lang['quantity'])
    sales_tree.heading("Total", text=lang['total_sales'])
    sales_tree.heading("Date", text="Date")
    
    # Update bottom frame
    total_sales_label.configure(text=f"{lang['total_sales']}0.00")
    sales_refresh_button.configure(text=lang['refresh'])

# Initialize database
def init_database():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    
    # Create inventory table
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 quantity INTEGER NOT NULL,
                 price REAL NOT NULL)''')
    
    # Create sales table
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 item_id INTEGER,
                 quantity INTEGER,
                 total_price REAL,
                 date TEXT,
                 FOREIGN KEY (item_id) REFERENCES inventory (id))''')
    
    conn.commit()
    conn.close()

# Clear entire database
def clear_database():
    lang = LANGUAGES[current_language]
    if messagebox.askyesno(lang['confirm'], lang['clear_confirm']):
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        
        # Delete all data from tables
        c.execute("DELETE FROM sales")
        c.execute("DELETE FROM inventory")
        
        conn.commit()
        conn.close()
        
        refresh_inventory()
        refresh_sales()
        update_total_sales()
        messagebox.showinfo(lang['success'], lang['db_cleared'])

# Update total sales display
def update_total_sales():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT SUM(total_price) FROM sales")
    total = c.fetchone()[0]
    conn.close()
    
    if total is None:
        total = 0
    
    lang = LANGUAGES[current_language]
    total_sales_label.config(text=f"{lang['total_sales']}{total:.2f}")

# Add new item to inventory
def add_item():
    lang = LANGUAGES[current_language]
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    
    if not name or not quantity or not price:
        messagebox.showerror(lang['error'], lang['fill_fields'])
        return
    
    if not quantity.isdigit() or not price.replace('.', '').isdigit():
        messagebox.showerror(lang['error'], lang['numbers_only'])
        return
    
    quantity = int(quantity)
    price = float(price)
    
    if quantity <= 0 or price <= 0:
        messagebox.showerror(lang['error'], lang['positive_numbers'])
        return
    
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
             (name, quantity, price))
    conn.commit()
    conn.close()
    
    refresh_inventory()
    clear_entries()
    messagebox.showinfo(lang['success'], lang['item_added'])

# Remove item from inventory
def remove_item():
    lang = LANGUAGES[current_language]
    item_id = remove_id_entry.get()
    
    if not item_id:
        messagebox.showerror(lang['error'], lang['enter_id'])
        return
    
    if not item_id.isdigit():
        messagebox.showerror(lang['error'], lang['id_number'])
        return
    
    item_id = int(item_id)
    
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    
    refresh_inventory()
    remove_id_entry.delete(0, tk.END)
    messagebox.showinfo(lang['success'], lang['item_removed'])

# Record a sale
def record_sale():
    lang = LANGUAGES[current_language]
    item_id = sale_id_entry.get()
    quantity = sale_quantity_entry.get()
    
    if not item_id or not quantity:
        messagebox.showerror(lang['error'], lang['fill_fields'])
        return
    
    if not item_id.isdigit() or not quantity.isdigit():
        messagebox.showerror(lang['error'], lang['numbers_only'])
        return
    
    item_id = int(item_id)
    quantity = int(quantity)
    
    if quantity <= 0:
        messagebox.showerror(lang['error'], lang['positive_numbers'])
        return
    
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    
    # Check if item exists and has enough quantity
    c.execute("SELECT quantity, price FROM inventory WHERE id = ?", (item_id,))
    result = c.fetchone()
    
    if not result:
        messagebox.showerror(lang['error'], lang['item_not_found'])
        conn.close()
        return
    
    current_quantity, price = result
    
    if current_quantity < quantity:
        messagebox.showerror(lang['error'], lang['not_enough'])
        conn.close()
        return
    
    # Update inventory
    c.execute("UPDATE inventory SET quantity = quantity - ? WHERE id = ?",
             (quantity, item_id))
    
    # Record sale
    total_price = price * quantity
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO sales (item_id, quantity, total_price, date) VALUES (?, ?, ?, ?)",
             (item_id, quantity, total_price, date))
    
    conn.commit()
    conn.close()
    
    refresh_inventory()
    refresh_sales()
    update_total_sales()
    clear_sale_entries()
    messagebox.showinfo(lang['success'], lang['sale_recorded'])

# Refresh inventory display
def refresh_inventory():
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
    
    # Load items from database
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    
    # Insert items into treeview
    for item in items:
        tree.insert("", tk.END, values=item)

# Refresh sales display
def refresh_sales():
    # Clear existing items
    for item in sales_tree.get_children():
        sales_tree.delete(item)
    
    # Load sales from database
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("""
        SELECT s.id, i.name, s.quantity, s.total_price, s.date
        FROM sales s
        JOIN inventory i ON s.item_id = i.id
        ORDER BY s.date DESC
    """)
    sales = c.fetchall()
    conn.close()
    
    # Insert sales into treeview
    for sale in sales:
        sales_tree.insert("", tk.END, values=sale)
    
    update_total_sales()

# Clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def clear_sale_entries():
    sale_id_entry.delete(0, tk.END)
    sale_quantity_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Shop Management System")
root.geometry("1000x600")

# Initialize database
init_database()

# Create main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create language selector
language_frame = ttk.Frame(main_frame)
language_frame.grid(row=0, column=0, sticky=(tk.E))
language_var = tk.StringVar(value='English')
language_combo = ttk.Combobox(language_frame, textvariable=language_var, values=list(LANGUAGES.keys()), state='readonly')
language_combo.pack(side=tk.RIGHT)
language_combo.bind('<<ComboboxSelected>>', update_language)

# Create tabs
notebook = ttk.Notebook(main_frame)
notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Inventory tab
inventory_frame = ttk.Frame(notebook)
notebook.add(inventory_frame, text="Inventory")

# Sales tab
sales_frame = ttk.Frame(notebook)
notebook.add(sales_frame, text="Sales")

# Setup Inventory Tab
# Add Item Frame
add_frame = ttk.LabelFrame(inventory_frame, text="Add Item", padding="5")
add_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

name_label = ttk.Label(add_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(add_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

quantity_label = ttk.Label(add_frame, text="Quantity:")
quantity_label.grid(row=0, column=2, padx=5, pady=5)
quantity_entry = ttk.Entry(add_frame)
quantity_entry.grid(row=0, column=3, padx=5, pady=5)

price_label = ttk.Label(add_frame, text="Price:")
price_label.grid(row=0, column=4, padx=5, pady=5)
price_entry = ttk.Entry(add_frame)
price_entry.grid(row=0, column=5, padx=5, pady=5)

add_button = ttk.Button(add_frame, text="Add Item", command=add_item)
add_button.grid(row=0, column=6, padx=5, pady=5)

# Inventory List
list_frame = ttk.LabelFrame(inventory_frame, text="Current Inventory", padding="5")
list_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create Treeview
tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Quantity", "Price"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Quantity", text="Quantity")
tree.heading("Price", text="Price")

tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add scrollbar
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
tree.configure(yscrollcommand=scrollbar.set)

# Remove Item Frame
remove_frame = ttk.LabelFrame(inventory_frame, text="Remove Item", padding="5")
remove_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

remove_id_label = ttk.Label(remove_frame, text="Item ID:")
remove_id_label.grid(row=0, column=0, padx=5, pady=5)
remove_id_entry = ttk.Entry(remove_frame)
remove_id_entry.grid(row=0, column=1, padx=5, pady=5)

remove_button = ttk.Button(remove_frame, text="Remove Item", command=remove_item)
remove_button.grid(row=0, column=2, padx=5, pady=5)

# Button Frame
button_frame = ttk.Frame(inventory_frame)
button_frame.grid(row=3, column=0, pady=5)

refresh_button = ttk.Button(button_frame, text="Refresh", command=refresh_inventory)
refresh_button.pack(side=tk.LEFT, padx=5)
clear_db_button = ttk.Button(button_frame, text="Clear Database", command=clear_database)
clear_db_button.pack(side=tk.LEFT, padx=5)

# Setup Sales Tab
# Sales Frame
sales_frame_top = ttk.LabelFrame(sales_frame, text="Record Sale", padding="5")
sales_frame_top.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

sale_id_label = ttk.Label(sales_frame_top, text="Item ID:")
sale_id_label.grid(row=0, column=0, padx=5, pady=5)
sale_id_entry = ttk.Entry(sales_frame_top)
sale_id_entry.grid(row=0, column=1, padx=5, pady=5)

sale_quantity_label = ttk.Label(sales_frame_top, text="Quantity:")
sale_quantity_label.grid(row=0, column=2, padx=5, pady=5)
sale_quantity_entry = ttk.Entry(sales_frame_top)
sale_quantity_entry.grid(row=0, column=3, padx=5, pady=5)

record_sale_button = ttk.Button(sales_frame_top, text="Record Sale", command=record_sale)
record_sale_button.grid(row=0, column=4, padx=5, pady=5)

# Sales History
history_frame = ttk.LabelFrame(sales_frame, text="Sales History", padding="5")
history_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create Treeview for sales
sales_tree = ttk.Treeview(history_frame, columns=("ID", "Item", "Quantity", "Total", "Date"), show="headings")
sales_tree.heading("ID", text="ID")
sales_tree.heading("Item", text="Item")
sales_tree.heading("Quantity", text="Quantity")
sales_tree.heading("Total", text="Total")
sales_tree.heading("Date", text="Date")

sales_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add scrollbar
sales_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=sales_tree.yview)
sales_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
sales_tree.configure(yscrollcommand=sales_scrollbar.set)

# Bottom Frame for Sales Tab
bottom_frame = ttk.Frame(sales_frame)
bottom_frame.grid(row=2, column=0, pady=5)

# Total Sales Label
total_sales_label = ttk.Label(bottom_frame, text="Total Sales: $0.00", font=("Arial", 12, "bold"))
total_sales_label.pack(side=tk.LEFT, padx=5)

# Refresh button
sales_refresh_button = ttk.Button(bottom_frame, text="Refresh", command=refresh_sales)
sales_refresh_button.pack(side=tk.LEFT, padx=5)

# Initial load of data
refresh_inventory()
refresh_sales()

# Start the application
root.mainloop() 