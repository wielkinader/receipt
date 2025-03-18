# Shop Management System
A simple inventory and sales management system created for my IB Computer Science Internal Assessment.

## Overview
This is a desktop application built with Python and Tkinter that helps small businesses manage their inventory and track sales. The system features a user-friendly interface with support for both English and Amharic languages.

## Features
- Add and remove items from inventory
- Track item quantities and prices
- Record sales transactions
- View sales history
- Calculate total sales
- Bilingual support (English/Amharic)
- Simple and intuitive interface

## Technical Details
The application is built using:
- Python 3.x
- Tkinter for the GUI
- SQLite for data storage
- PIL (Python Imaging Library) for image processing

## How to Run
1. Make sure you have Python 3.x installed
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install required packages:
   ```bash
   pip install Pillow
   ```
4. Run the application:
   ```bash
   python shop_management.py
   ```

## Code Structure
The application is organized into several main components:
- Language dictionaries for English and Amharic support
- Database functions for inventory and sales management
- GUI elements using Tkinter
- Event handlers for user interactions

## Database Schema
The application uses two main tables:
1. `inventory`: Stores item information (ID, name, quantity, price)
2. `sales`: Records sales transactions (ID, item_id, quantity, total_price, date)

## IB Computer Science IA
This project was created as part of my IB Computer Science Internal Assessment. It demonstrates:
- Object-oriented programming concepts
- Database management
- GUI development
- Internationalization
- Error handling
- User interface design principles

## Author
[Your Name] 