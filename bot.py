import pywhatkit
import csv
import time
import logging
from datetime import datetime
import json
import os
import sys # Import sys

# --- Define Log Path --- 
def get_log_directory():
    """Returns the path to the application's log directory."""
    app_name = "WhatsAppBot" # Or use a more specific name if desired
    if sys.platform == 'darwin': # macOS
        base_dir = os.path.expanduser('~/Library/Application Support')
    elif sys.platform == 'win32': # Windows
        base_dir = os.getenv('APPDATA') or os.path.expanduser('~')
    else: # Linux/Other
        base_dir = os.path.expanduser('~/.local/share') # Common practice
        if not os.path.exists(base_dir):
             base_dir = os.path.expanduser('~/.config') # Fallback
        if not os.path.exists(base_dir):
             base_dir = os.path.expanduser('~') # Last resort
             
    log_dir = os.path.join(base_dir, app_name)
    os.makedirs(log_dir, exist_ok=True) # Ensure the directory exists
    return log_dir

LOG_DIRECTORY = get_log_directory()
BOT_LOG_FILE = os.path.join(LOG_DIRECTORY, "bot.log")
JSON_LOG_FILE = os.path.join(LOG_DIRECTORY, "contact_log.json")
# -----------------------

# Configure basic logging using the defined path
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(BOT_LOG_FILE), logging.StreamHandler()])

def log_message_to_json(phone_number, name, message):
    """Logs the sent message to a JSON file, indexed by phone number."""
    data = {}
    # Ensure phone number starts with '+' for consistency as key
    if not phone_number.startswith('+'):
        logging.warning(f"Phone number '{phone_number}' for logging does not start with '+'. Attempting to proceed.")
        # Consider adding '+' if it's purely numeric, but be cautious about assumptions
        # if phone_number.isdigit():
        #     phone_number = "+" + phone_number

    # Load existing data if file exists
    if os.path.exists(JSON_LOG_FILE):
        try:
            with open(JSON_LOG_FILE, 'r', encoding='utf-8') as f:
                # Handle empty file case
                content = f.read()
                if content:
                    data = json.loads(content)
                else:
                    logging.warning(f"JSON log file '{JSON_LOG_FILE}' was empty. Initializing new log.")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {JSON_LOG_FILE}. File might be corrupted. Starting fresh log.")
        except Exception as e:
            logging.error(f"Error reading {JSON_LOG_FILE}: {e}. Starting fresh log.")
            
    # Update data for the current contact
    if phone_number in data:
        # Append message to existing list
        if 'mensagens' in data[phone_number] and isinstance(data[phone_number]['mensagens'], list):
             data[phone_number]['mensagens'].append(message)
        else:
             # If 'mensagens' is missing or not a list, create/reset it
             data[phone_number]['mensagens'] = [message]
        # Update name if it changed or was missing (optional, keeps latest name)
        data[phone_number]['nome'] = name 
    else:
        # Add new entry for this contact
        data[phone_number] = {
            'nome': name,
            'mensagens': [message]
        }
        
    # Save updated data back to JSON file
    try:
        with open(JSON_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False) # Use indent for readability, ensure_ascii=False for non-latin chars
    except Exception as e:
        logging.error(f"Error writing to {JSON_LOG_FILE}: {e}")

def load_contacts(filepath):
    """Loads contacts from a CSV file (phone_number, name)."""
    contacts = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if 'phone_number' not in reader.fieldnames:
                logging.error(f"CSV file '{filepath}' must contain a 'phone_number' column.")
                return None 
            for row in reader:
                # Basic validation for phone number format (starts with '+')
                phone = row.get('phone_number', '').strip()
                name = row.get('name', 'N/A').strip() # Optional name column
                if phone.startswith('+') and phone[1:].isdigit():
                     contacts.append({'phone_number': phone, 'name': name})
                else:
                    logging.warning(f"Skipping invalid phone number format: {phone} for contact {name}")
        logging.info(f"Loaded {len(contacts)} contacts from {filepath}")
        return contacts
    except FileNotFoundError:
        logging.error(f"Contact file not found: {filepath}")
        return None
    except Exception as e:
        logging.error(f"Error loading contacts from {filepath}: {e}")
        return None

def send_whatsapp_messages(contacts, message, delay_seconds=18, wait_time=12, log_callback=None):
    """Sends a WhatsApp message to a list of contacts and logs to JSON."""
    if not contacts:
        logging.warning("No contacts loaded to send messages to.")
        if log_callback:
            log_callback("No contacts loaded.")
        return

    total_contacts = len(contacts)
    processed_numbers = set() # Keep track of numbers we've already processed

    for i, contact in enumerate(contacts):
        phone_number = contact['phone_number']
        name = contact.get('name', phone_number) 
        
        # Check if we've already processed this number in this run
        if phone_number in processed_numbers:
            skip_msg = f"Skipping duplicate number in this run: {name} ({phone_number})"
            logging.warning(skip_msg)
            if log_callback:
                log_callback(skip_msg)
            continue # Move to the next contact

        # Add number to the set before attempting to send
        processed_numbers.add(phone_number)
        
        current_status = f"Sending message {i+1}/{total_contacts} to {name} ({phone_number})..."
        logging.info(current_status)
        if log_callback:
            log_callback(current_status)
            
        try:
            # pywhatkit.sendwhatmsg_instantly might need the tab closed manually sometimes.
            # It opens WhatsApp Web, waits for it to load, types the message, and sends.
            
            # Replace [Name] placeholder in the message
            personalized_message = message.replace('[Name]', name) if name != 'N/A' else message.replace('[Name]', '')

            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone_number, 
                message=personalized_message, # Use personalized message
                wait_time=wait_time, # Time for WhatsApp Web to open and load
                tab_close=True, 
                close_time=3  # Time before closing tab after sending
            )
            success_msg = f"Message sent successfully to {name} ({phone_number})."
            logging.info(success_msg)
            if log_callback:
                log_callback(success_msg)
            
            # Log the message to JSON upon successful send
            log_message_to_json(phone_number, name, personalized_message) # Call the logging function
                
        except Exception as e:
            error_msg = f"Failed to send message to {name} ({phone_number}): {e}"
            logging.error(error_msg)
            if log_callback:
                log_callback(error_msg)
                
        # Wait before sending the next message
        if i < total_contacts - 1:
            wait_notice = f"Waiting {delay_seconds} seconds before next message..."
            logging.info(wait_notice)
            if log_callback:
                log_callback(wait_notice)
            time.sleep(delay_seconds)

    final_msg = "Finished sending all messages."
    logging.info(final_msg)
    if log_callback:
        log_callback(final_msg)

# Example usage (for testing purposes)
if __name__ == "__main__":
    print("Running bot.py directly for testing...")
    test_contacts = load_contacts('contacts.csv')
    if test_contacts:
        test_message = "Hello from the Python Bot! This is a test message."
        send_whatsapp_messages(test_contacts, test_message, delay_seconds=5)
    else:
        print("Could not load contacts for testing.")
    print("Bot testing finished.") 