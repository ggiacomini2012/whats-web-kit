# test_pywhatkit.py
import pywhatkit
import time
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    logging.info("Attempting to send message...")
    # --- IMPORTANT ---
    # Replace '+12345678900' with a real WhatsApp number you can test with.
    # Make sure WhatsApp Web/Desktop is logged in on your machine.
    # -----------------
    phone_number = '+5547997676797' # <-- REPLACE THIS
    message = 'Test message from bundled app test.'

    pywhatkit.sendwhatmsg_instantly(
        phone_no=phone_number,
        message=message,
        wait_time=20, # Time for WhatsApp Web to open and load chat
        tab_close=True,
        close_time=3  # Time before closing tab after sending
    )
    logging.info(f"pywhatkit.sendwhatmsg_instantly called successfully for {phone_number}.")
    logging.info("Check WhatsApp for the message.")

except Exception as e:
    # Log the full exception traceback for detailed debugging
    logging.exception(f"Error during pywhatkit call: {e}")

finally:
    # Keep the (potential) terminal window open for a bit longer to see output
    logging.info("Test script finished. Waiting for 15 seconds before exiting...")
    time.sleep(15)
    logging.info("Exiting.") 