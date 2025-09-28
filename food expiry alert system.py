import csv
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

# Email credentials (Replace with your own)
SENDER_EMAIL = "pallavisb1809@gmail.com"
SENDER_PASSWORD = "pallavi123"
RECIPIENT_EMAIL = "niharikaakkimi@gmail.com"

def send_email_alert(subject, body):
    """Sends an email alert to the specified recipient."""
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print("✅ Alert sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email alert: {e}")

# --- NEW FUNCTIONS FOR CRUD ---

def create_item(item_name, expiry_date_str):
    """Adds a new food item to the CSV file."""
    try:
        datetime.strptime(expiry_date_str, '%Y-%m-%d')
        
        with open('food_items.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([item_name, expiry_date_str])
        print(f"✅ '{item_name}' added successfully!")
    except ValueError:
        print("❌ Invalid date. Please use YYYY-MM-DD.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def read_items():
    """Reads and displays all food items from the CSV file."""
    try:
        items = []
        with open('food_items.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row:
                    items.append(row)
        
        if not items:
            print("\n🛒 Your list is empty.")
            return

        print("\n--- Your Food Items ---")
        for i, item in enumerate(items):
            print(f"[{i+1}] {item[0]} (Expires: {item[1]})")
        
        return items

    except FileNotFoundError:
        print("❌ 'food_items.csv' not found. Please create it.")
        return []

def update_item():
    """Updates the expiry date of an existing food item."""
    items = read_items()
    if not items:
        return
    
    try:
        choice = int(input("Enter the number of the item you want to update: "))
        if 1 <= choice <= len(items):
            new_date = input("Enter new expiry date (YYYY-MM-DD): ")
            datetime.strptime(new_date, '%Y-%m-%d') # Validate date
            
            items[choice - 1][1] = new_date
            
            with open('food_items.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['item_name', 'expiry_date']) # Write header
                writer.writerows(items)
            print("✅ Item updated successfully!")
        else:
            print("❌ Invalid number.")
    except (ValueError, IndexError):
        print("❌ Invalid input. Please enter a number.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def delete_item():
    """Deletes an item from the CSV file."""
    items = read_items()
    if not items:
        return

    try:
        choice = int(input("Enter the number of the item you want to delete: "))
        if 1 <= choice <= len(items):
            deleted_item = items.pop(choice - 1)
            
            with open('food_items.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['item_name', 'expiry_date'])
                writer.writerows(items)
            print(f"✅ '{deleted_item[0]}' deleted successfully!")
        else:
            print("❌ Invalid number.")
    except (ValueError, IndexError):
        print("❌ Invalid input. Please enter a number.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# --- MAIN MENU AND EXPIRY CHECK ---

def check_expiry():
    """Reads the CSV file and alerts about expiring items."""
    today = datetime.now().date()
    expired_items = []
    expiring_soon = []
    
    try:
        with open('food_items.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if not row: continue
                item_name, expiry_date_str = row
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                days_left = (expiry_date - today).days
                
                if days_left < 0:
                    expired_items.append(item_name)
                elif days_left <= 3:
                    expiring_soon.append((item_name, days_left))
                    
    except FileNotFoundError:
        print("❌ 'food_items.csv' not found. Please create it.")
        return
    except Exception as e:
        print(f"❌ An error occurred while reading the file: {e}")
        return

    notification_message = ""
    if expired_items:
        notification_message += "⚠ EXPIRED ITEMS: " + ", ".join(expired_items) + ". "
    if expiring_soon:
        expiring_list = [f"{item} (in {days} day{'s' if days > 1 else ''})" for item, days in expiring_soon]
        notification_message += "⏳ EXPIRING SOON: " + ", ".join(expiring_list) + "."
    
    if notification_message:
        send_email_alert("Food Expiry Alert", notification_message)
    else:
        print("\n✅ No alerts to send.")

def main_menu():
    while True:
        print("\n=== Food Expiry System ===")
        print("1. Add a new item")
        print("2. Check for expiring items & get alerts")
        print("3. View / Update an item")
        print("4. View / Delete an item")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            item = input("Enter item name: ")
            date_str = input("Enter expiry date (YYYY-MM-DD): ")
            create_item(item, date_str)
        elif choice == '2':
            check_expiry()
        elif choice == '3':
            update_item()
        elif choice == '4':
            delete_item()
        elif choice == '5':
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 5.")

if _name_ == "_main_":
    main_menu()