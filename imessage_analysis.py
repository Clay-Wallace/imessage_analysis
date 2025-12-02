import sqlite3
import os
import sys
import venv
import datetime
import json

def create_venv():
    venv_path = os.path.join(os.path.dirname(__file__), ".venv")
    if os.path.exists(venv_path):
        return

    venv.create(venv_path, with_pip=True)
    print("Virtual environment created at:", venv_path)

    if sys.platform == "darwin":
        activate_script = os.path.join(venv_path, "bin", "activate")

    print(f"To activate the virtual environment, run:\nsource {activate_script}\nAfterwards, rerun this program.")

def load_message_data():
    """Retrieve local iMessage data and load for analysis"""
    if not check_user_permissions():
        prompt_for_permission()
        sys.exit(1)
    
    print("Successfully accessed iMessage data! Cleaning data...")
    messages = read_messages(20)
    return messages

def check_user_permissions():
    """Check if iMessage data can be loaded"""
    message_db = os.path.expanduser("~/Library/Messages/chat.db")
    
    try:
        conn = sqlite3.connect(message_db)
        conn.close()
        return True
    except (sqlite3.OperationalError, PermissionError):
        return False
    
def prompt_for_permission():
    """Promt the user the enable disk access for Terminal"""
    print("\n" + "="*60)
    print("PERMISSION REQUIRED")
    print("="*60)
    print("\nThis script needs access to your iMessage database.")
    print("\nPlease follow these steps to grant access:\n")
    print("1. Open System Settings")
    print("2. Go to Privacy & Security → Full Disk Access")
    print("3. Your user interface may vary depending on your active version of MacOS. Enable Access for Terminal. If not listed, click the '+' symbol, navigate to Applications → Utilities → Terminal, and add Terminal")
    print("4. Restart Terminal")
    print("\nAfter completing these steps, run this script again.")
    print("="*60 + "\n")

def get_chat_mapping(db_location=os.path.expanduser("~/Library/Messages/chat.db")):
    # Borrowed from Kelly Gold on Medium
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()

    cursor.execute("SELECT room_name, display_name FROM chat")
    result_set = cursor.fetchall()

    mapping = {room_name: display_name for room_name, display_name in result_set}

    conn.close()

    return mapping

def read_messages(n, self_number='Me', human_readable_date=True, db_location=os.path.expanduser("~/Library/Messages/chat.db")):
    # Borrowed from Kelly Gold on Medium
    # Connect to the database and execute a query to join message and handle tables
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    query = """
    SELECT message.ROWID, message.date, message.text, message.attributedBody, handle.id, message.is_from_me, message.cache_roomnames
    FROM message
    LEFT JOIN handle ON message.handle_id = handle.ROWID
    """
    if n is not None:
        query += f" ORDER BY message.date DESC LIMIT {n}"
    results = cursor.execute(query).fetchall()
    
    # Initialize an empty list for messages
    messages = []

    # Loop through each result row and unpack variables
    for result in results:
        rowid, date, text, attributed_body, handle_id, is_from_me, cache_roomname = result

        # Use self_number or handle_id as phone_number depending on whether it's a self-message or not
        phone_number = self_number if handle_id is None else handle_id

        # Use text or attributed_body as body depending on whether it's a plain text or rich media message
        if text is not None:
            body = text
        
        elif attributed_body is None: 
            continue
        
        else: 
            # Decode and extract relevant information from attributed_body using string methods 
            attributed_body = attributed_body.decode('utf-8', errors='replace')
            if "NSNumber" in str(attributed_body):
                attributed_body = str(attributed_body).split("NSNumber")[0]
                if "NSString" in attributed_body:
                    attributed_body = str(attributed_body).split("NSString")[1]
                    if "NSDictionary" in attributed_body:
                        attributed_body = str(attributed_body).split("NSDictionary")[0]
                        attributed_body = attributed_body[6:-12]
                        body = attributed_body

        # Convert date from Apple epoch time to standard format using datetime module if human_readable_date is True  
        if human_readable_date:
            date_string = '2001-01-01'
            mod_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
            unix_timestamp = int(mod_date.timestamp())*1000000000
            new_date = int((date+unix_timestamp)/1000000000)
            date = datetime.datetime.fromtimestamp(new_date).strftime("%Y-%m-%d %H:%M:%S")

        mapping = get_chat_mapping(db_location)  # Get chat mapping from database location

        try:
            mapped_name = mapping[cache_roomname]
        except:
            mapped_name = None

        messages.append(
            {"rowid": rowid, "date": date, "body": body, "phone_number": phone_number, "is_from_me": is_from_me,
             "cache_roomname": cache_roomname, 'group_chat_name' : mapped_name})

    conn.close()
    return messages

def print_messages(messages):
    # Borrowed from Kelly Gold on Medium
    print(json.dumps(messages))

def main():
    create_venv()
    if not os.path.exists(os.path.join(os.path.dirname(__file__), ".venv")):
        sys.exit(0)
    print("Welcome to iMessage Analysis!")
    messages = load_message_data()
    print_messages(messages)

if __name__ == "__main__":
    main()