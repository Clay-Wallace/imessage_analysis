def get_earliest_and_latest(messages, sender=None):
    if sender is not None:
        filtered = [m for m in messages if m.get("phone_number") == sender]
    else:
        filtered = messages

    if not filtered:
        raise ValueError("No messages found for the given sender filter")

    earliest = min(filtered, key=lambda m: m["date_obj"])
    latest   = max(filtered, key=lambda m: m["date_obj"])
    return earliest, latest

def stat_overview(messages):
    """Generates an overview of general statistics from iMessage data."""

    first_message_date = 
    total = len(messages)
