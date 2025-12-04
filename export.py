HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>iMessage Statistical Overview</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { border-bottom: 1px solid #ccc; padding-bottom: 5px; }
    .section { margin-top: 15px; }
  </style>
</head>
<body>
  <h1>iMessage Statistical Overview</h1>

  <div class="section">
    <strong>Time period:</strong> {earliest_msg} to {latest_msg}
  </div>

  <div class="section">
    <strong>Total messages:</strong> {total}
  </div>

  <div class="section">
    <strong>Messages sent:</strong> {mesg_sent} ({percent_sent:.2f}%)
    <br>
    - Unique message recipients: {num_recipients}
  </div>

  <div class="section">
    <strong>Messages received:</strong> {mesg_received} ({percent_received:.2f}%)
    <br>
    - Unique message senders: {num_senders}
  </div>

  <div class="section">
    <strong>Unique conversations:</strong> {unique_convos}
    <br>
    - Group chats: {num_group_chats} ({percent_gc:.2f}%)
  </div>
</body>
</html>
"""

def export_html_overview(
    earliest_msg,
    latest_msg,
    total,
    mesg_sent,
    percent_sent,
    recipients,
    mesg_received,
    percent_received,
    senders,
    unique_convos,
    group_chats,
    percent_gc,
    path="imessage_overview.html",
):
    html = HTML_TEMPLATE.format(
        earliest_msg=earliest_msg,
        latest_msg=latest_msg,
        total=total,
        mesg_sent=mesg_sent,
        percent_sent=percent_sent,
        num_recipients=len(recipients),
        mesg_received=mesg_received,
        percent_received=percent_received,
        num_senders=len(senders),
        unique_convos=unique_convos,
        num_group_chats=len(group_chats),
        percent_gc=percent_gc,
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

