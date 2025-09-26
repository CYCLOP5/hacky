import requests
from datetime import datetime
import time
import re

# --- Configuration ---
API_URL = "https://services.swpc.noaa.gov/products/alerts.json"

# --- Utility Functions ---

def format_alert_text(text):
    """
    Cleans up and formats the alert text content for better console readability.
    """
    if not text:
        return "No description provided."
    
    # Remove excessive whitespace and split into lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Join back with a double newline for clear separation
    return "\n    ".join(lines)


def extract_alert_details(message_text, product_id):
    """
    Parses the message string to extract the message code and issue time.
    
    Args:
        message_text (str): The full alert message text.
        product_id (str): The product ID (already extracted).

    Returns:
        dict: Containing 'messageCode', 'issueTime', and 'productID'.
    """
    details = {
        'messageCode': 'N/A',
        'issueTime': 'N/A',
        'productID': product_id 
    }

    # Regex to find Space Weather Message Code (e.g., ALTTP2)
    code_match = re.search(r"Space Weather Message Code: (\w+)", message_text)
    if code_match:
        details['messageCode'] = code_match.group(1)

    # Regex to find Issue Time (e.g., 2025 Sep 23 1111 UTC)
    time_match = re.search(r"Issue Time: (\d{4} \w{3} \d{2} \d{4} UTC)", message_text)
    if time_match:
        details['issueTime'] = time_match.group(1)
        
    return details


def parse_swpc_datetime(utc_string):
    """
    Parses the SWPC date/time format (e.g., "2025 Sep 22 1211 UTC") into a standard datetime object.
    Uses multiple formats to handle variations from the API.
    """
    # Clean up the string first (e.g., handles double spaces)
    cleaned_string = ' '.join(utc_string.split())
    
    # Potential format: YYYY MMM DD HHMM UTC (e.g., "2025 Sep 22 1211 UTC")
    
    try:
        parts = cleaned_string.split()
        
        # We expect 5 parts: YYYY MMM DD HHMM UTC
        if len(parts) != 5:
            # Fallback if the format is not recognized
            return f"Invalid Time Format: {utc_string}"

        # Extract the time string (HHMM) and convert it to HH:MM format
        time_str = parts[3] # HHMM
        formatted_time = f"{time_str[:2]}:{time_str[2:]}"
        
        # Reconstruct: YYYY MMM DD HH:MM UTC
        reconstructed_date = f"{parts[0]} {parts[1]} {parts[2]} {formatted_time} {parts[4]}"
        
        # Use a specific format string to parse the reconstructed string
        dt_object = datetime.strptime(reconstructed_date, "%Y %b %d %H:%M %Z")
        
        # Convert to local time for better user context
        # Note: The strptime function handles the conversion from the UTC (%Z) string to a Python datetime object.
        return dt_object.strftime("%Y-%m-%d %H:%M:%S (Local Time)")

    except ValueError as e:
        # Fallback to a string manipulation attempt if strptime fails
        return f"Error parsing date '{utc_string}': {e}"


def get_alert_priority(code):
    """
    Assigns a descriptive title and color based on the space weather alert code.
    """
    if not code:
        return "Advisory/Other", "\033[94m" # Blue

    upper_code = code.upper()

    # Geomagnetic Storms (G-scale) or related alerts (Kp/ap effects)
    if 'G' in upper_code or upper_code.startswith('WARRNM') or upper_code.startswith('ALTEF'):
        return "Geomagnetic Storm/High Kp", "\033[91m" # Red

    # Solar Radiation Storms (S-scale) - related to SEU risk
    if 'S' in upper_code:
        return "Solar Radiation Storm", "\033[93m" # Yellow

    # Radio Blackouts (R-scale) - related to solar flares/ESD risk
    if 'R' in upper_code or upper_code.startswith('ALTTP'):
        # Added ALTTP (Type II Radio Emission) to Radio Blackouts category
        return "Radio Blackout (Solar Flare)", "\033[95m" # Magenta

    # Watches (General)
    if upper_code.startswith('WATCH'):
        return "Space Weather Watch", "\033[92m" # Green

    return "Advisory/Other", "\033[94m" # Blue (Default)

# --- Main Logic ---

def fetch_and_print_alerts():
    """
    Fetches the space weather alerts from the NOAA SWPC API and prints them.
    """
    print(f"\n--- Fetching Real-time Space Weather Alerts from NOAA SWPC ---\n")
    
    # Simple exponential backoff retry loop (up to 3 times)
    for attempt in range(3):
        try:
            # Use a timeout to prevent hanging
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            alerts = response.json()
            
            if not alerts:
                print("No active space weather alerts or watches reported at this time.")
                return

            print(f"Total Active Alerts: {len(alerts)}\n")

            # ANSI escape codes for resetting color
            RESET_COLOR = "\033[0m"

            for alert in alerts:
                # 1. The main alert content is in the 'message' field
                text_content = alert.get('message', '')
                
                # 2. Extract embedded details (Code and Issue Time) from the message
                extracted_details = extract_alert_details(text_content, alert.get('product_id', 'N/A'))
                
                code = extracted_details['messageCode']
                issue_time = extracted_details['issueTime']
                product_id = extracted_details['productID']
                
                # Get descriptive title and color
                priority_title, color_code = get_alert_priority(code)

                # Ensure product_id is not missing if message is present
                if product_id == 'N/A' and alert.get('product_id'):
                    product_id = alert.get('product_id')
                
                print(color_code + f"┌{'─' * 50}┐" + RESET_COLOR)
                print(color_code + f"| {priority_title.ljust(48)} |" + RESET_COLOR)
                print(color_code + f"├{'─' * 50}┤" + RESET_COLOR)
                print(color_code + f"| Code: {code.ljust(44)} |" + RESET_COLOR)
                print(color_code + f"| Product ID: {product_id.ljust(38)} |" + RESET_COLOR)
                print(color_code + f"| Issued: {parse_swpc_datetime(issue_time).ljust(42)} |" + RESET_COLOR)
                print(color_code + f"└{'─' * 50}┘" + RESET_COLOR)
                print(f"  {format_alert_text(text_content)}\n")
            
            return # Success, exit function

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                # Wait for increasing time before retrying
                sleep_time = 2 ** attempt
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("\nFailed to retrieve alerts after multiple retries. The API may be unavailable.")

if __name__ == "__main__":
    fetch_and_print_alerts()
