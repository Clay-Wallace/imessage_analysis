import sqlite3
import os
import sys
import venv

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

def main():
    create_venv()
    if not os.path.exists(os.path.join(os.path.dirname(__file__), ".venv")):
        sys.exit(0)
    print("Welcome to iMessage Analysis!")

if __name__ == "__main__":
    main()