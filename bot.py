import pywhatkit
import csv
import time
import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()])

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
    """Sends a WhatsApp message to a list of contacts."""
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
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone_number, 
                message=message,
                wait_time=wait_time, # Time for WhatsApp Web to open and load
                tab_close=True, 
                close_time=3  # Time before closing tab after sending
            )
            success_msg = f"Message sent successfully to {name} ({phone_number})."
            logging.info(success_msg)
            if log_callback:
                log_callback(success_msg)
                
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