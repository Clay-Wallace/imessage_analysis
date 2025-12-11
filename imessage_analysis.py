import sqlite3
import os
import sys
import datetime
import json
import subprocess
from stats import stat_overview, habit_overivew, social_network
from export import export_html_overview
import pandas as pd
from pathlib import Path

def load_message_data(n=None):
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

    if not message_db:
        manual = input("iMessage data not found. Do you want to manually enter the filepath of your iMessage database? (Y or N) ")
        if manual.strip().lower() == "y":
            message_db = input("Please enter the filepath: ")
        else:
            print("Filepath not entered. Thank you for using iMessage Analysis.")
            sys.exit(0)
    
    try:
        conn = sqlite3.connect(message_db)
        conn.close()
        return True
    except (PermissionError):
        return False
    except (sqlite3.OperationalError):
        print("iMessage database filepath invalid. Thank you for using iMessage Analysis.")
        sys.exit(1)
    
def prompt_for_permission():
    """Promt the user the enable disk access for Terminal"""
    print("\n" + "="*60)
    print("PERMISSION REQUIRED")
    print("="*60)
    print("\nThis script needs access to your iMessage database.")
    print("\nPlease follow these steps to grant access:\n")
    print("1. Open System Settings")
    print("2. Go to Privacy & Security → Full Disk Access")
    print("3. Your user interface may vary depending on your active version of MacOS. Enable access for Terminal. If not listed, click the '+' symbol, navigate to Applications → Utilities → Terminal, and add Terminal")
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
    ORDER BY message.date DESC
    """

    if n is not None:
        query += f" LIMIT {n}"
    
    results = cursor.execute(query).fetchall()
    
    messages = []

    for result in results:
        rowid, date, text, attributed_body, handle_id, is_from_me, cache_roomname, cache_has_attachments = result

        phone_number = self_number if handle_id is None else handle_id

        if text is not None:
            body = text
        
        elif attributed_body is None: 
            continue
        
        else: 
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

    # Borrowed from Kelly Gold on Medium
    print(json.dumps(messages))

def clean_number(raw_phone: str) -> str | None:
    """Standardize a phone number for iMessage-style use."""
    # Generated by ChatGPT
    if raw_phone is None:
        return None
    
    phone = "".join(c for c in raw_phone if c.isnumeric())
    if not phone:
        return None
    
    if len(phone) == 10:
        phone = "+1" + phone
    elif len(phone) == 11:
        phone = "+" + phone
    else:
       
        pass
    return phone

def attach_date_obj(messages):
    # Generated by ChatGPT
    for m in messages:
        m["date_obj"] = datetime.datetime.strptime(m["date"], "%Y-%m-%d %H:%M:%S")

CACHE_FILE = Path("contacts_cache.json")

def get_contacts_from_contacts_app(use_cache=True):
    """Get contacts with raw and cleaned numbers."""
    # Generated by ChatGPT

    if use_cache and CACHE_FILE.exists():
        print("Loading contacts from cache...")
        with open(CACHE_FILE) as f:
            return json.load(f)

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

    
    entries = [s.strip() for s in raw.split(",")]

    contacts = []
    for entry in entries:
        parts = entry.split("|")
        
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

    with open(CACHE_FILE, "w") as f:
        json.dump(contacts, f)
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
    
    df = pd.DataFrame(recent_messages)
    df["convo_id"] = df["group_chat_name"].replace("", pd.NA).fillna(df["cache_roomname"]).fillna(df["name"])

    return df

def main():
    print("Welcome to iMessage Analysis!")
    recent_messages = load_message_data()
    contacts = get_contacts_from_contacts_app()
    messages = combine_data(recent_messages, contacts)
    
    overview_stats = []
    overview_stats.extend(stat_overview(messages))
    overview_stats.extend(habit_overivew(messages))
    top_contacts = social_network(messages)

    export_html_overview(*overview_stats, top_contacts)


if __name__ == "__main__":
    main()