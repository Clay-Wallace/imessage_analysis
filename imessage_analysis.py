import sqlite3
import os
import sys
import venv
import datetime
import json
import subprocess
from stats import stat_overview, habit_overivew
from export import export_html_overview

def create_venv():
    venv_path = os.path.join(os.path.dirname(__file__), ".venv")
    if os.path.exists(venv_path):
        return

    venv.create(venv_path, with_pip=True)
    print("Virtual environment created at:", venv_path)

    if sys.platform == "darwin":
        activate_script = os.path.join(venv_path, "bin", "activate")

    print(f"To activate the virtual environment, run:\nsource {activate_script}\nAfterwards, rerun this program.")

def load_message_data(n):
    """Retrieve local iMessage data and load for analysis"""
    if not check_user_permissions():
        prompt_for_permission()
        sys.exit(1)
    
    print("Successfully accessed iMessage data! Reading message data...")
    messages = read_messages(n)
    attach_date_obj(messages)
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
    SELECT message.ROWID, message.date, message.text, message.attributedBody, handle.id, message.is_from_me, message.cache_roomnames, message.cache_has_attachments
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
        rowid, date, text, attributed_body, handle_id, is_from_me, cache_roomname, cache_has_attachments = result

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

        APPLE_EPOCH_OFFSET = 978307200
        if human_readable_date:
            if date > 1000000000000000:  
                seconds_val = date / 1000000000
            else:
                seconds_val = date

            final_timestamp = seconds_val + APPLE_EPOCH_OFFSET
            
            date = datetime.datetime.fromtimestamp(final_timestamp).strftime("%Y-%m-%d %H:%M:%S")

        mapping = get_chat_mapping(db_location)  

        try:
            mapped_name = mapping[cache_roomname]
        except:
            mapped_name = None

        messages.append(
            {"rowid": rowid, "date": date, "body": body, "phone_number": phone_number, "is_from_me": is_from_me,
             "cache_roomname": cache_roomname, 'group_chat_name' : mapped_name, "cache_has_attachments": cache_has_attachments})

    conn.close()
    return messages

def print_messages(messages):
    # Borrowed from Kelly Gold on Medium
    print(json.dumps(messages))

def clean_number(raw_phone: str) -> str | None:
    """Standardize a phone number for iMessage-style use."""
    # Generated by ChatGPT
    if raw_phone is None:
        return None
    # Remove all non-numeric characters
    phone = "".join(c for c in raw_phone if c.isnumeric())
    if not phone:
        return None
    # If the phone number is 10 digits, add "+1"; if 11 digits, add "+"
    if len(phone) == 10:
        phone = "+1" + phone
    elif len(phone) == 11:
        phone = "+" + phone
    else:
        # Leave other lengths as-is; or return None if you want to drop them
        pass
    return phone

def attach_date_obj(messages):
    # Generated by ChatGPT
    for m in messages:
        m["date_obj"] = datetime.datetime.strptime(m["date"], "%Y-%m-%d %H:%M:%S")

def get_contacts_from_contacts_app():
    """Get contacts with raw and cleaned numbers."""
    # Generated by ChatGPT

    APPLESCRIPT_EXPORT_CONTACTS = r'''
tell application "Contacts"
    set allPeople to every person
    set outLines to {}
    repeat with p in allPeople
        set theName to name of p
        set phoneProps to phones of p
        if (count of phoneProps) is 0 then
            set end of outLines to theName & "||"
        else
            repeat with ph in phoneProps
                set phLabel to label of ph
                set phValue to value of ph
                set end of outLines to theName & "|" & phLabel & "|" & phValue
            end repeat
        end if
    end repeat
    return outLines
end tell
'''
    print("Retrieving contacts from Contacts app...")
    result = subprocess.run(
        ["osascript", "-e", APPLESCRIPT_EXPORT_CONTACTS],
        capture_output=True,
        text=True,
        check=True,
    )

    raw = result.stdout.strip()
    if not raw:
        return []

    # AppleScript returns a comma-separated list of "Name|Label|Number" strings
    entries = [s.strip() for s in raw.split(",")]

    contacts = []
    for entry in entries:
        parts = entry.split("|")
        # Ensure we always have three slots
        while len(parts) < 3:
            parts.append("")
        name, label, number = parts[0], parts[1], parts[2]

        number_clean = clean_number(number) if number else None

        contacts.append({
            "NAME": name,
            "LABEL": label,
            "FULL NUMBER": number if number else None,
            "NUMBERCLEAN": number_clean,
        })
    return contacts

def combine_data(recent_messages, contacts):
    """
    recent_messages: list of dicts with at least "phone_number"
    contacts: list of dicts from get_contacts_from_contacts_app()
              with keys "NAME", "FULL NUMBER", "NUMBERCLEAN"
    """
    # Generated by ChatGPT. Adapted from code by Kelly Gold.
    number_to_contact = {}
    for c in contacts:
        num_clean = c.get("NUMBERCLEAN")
        if not num_clean:
            continue
        number_to_contact[num_clean] = c

    for message in recent_messages:
        phone_number = message.get("phone_number")
        if not phone_number:
            continue

        contact = number_to_contact.get(phone_number)
        if not contact:
            continue

        full_name = contact.get("NAME", "")
        message["name"] = full_name

        parts = full_name.split()
        if parts:
            message["first_name"] = parts[0]
            if len(parts) > 1:
                message["last_name"] = " ".join(parts[1:])

    return recent_messages

def main():
    create_venv()
    if not os.path.exists(os.path.join(os.path.dirname(__file__), ".venv")):
        sys.exit(0)
    print("Welcome to iMessage Analysis!")
    recent_messages = load_message_data(20)
    print(recent_messages)
    addressBookData = get_contacts_from_contacts_app()
    messages = combine_data(recent_messages, addressBookData)
    
    overview_stats = []
    overview_stats.extend(stat_overview(messages))
    overview_stats.extend(habit_overivew(messages))

    export_html_overview(*overview_stats)


if __name__ == "__main__":
    main()