HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>iMessage Analysis Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
    .section {{ margin-top: 15px; }}
  </style>
</head>
<body>
  <h1>iMessage Analysis Report</h1>

  <h2>Statistical Overview</h2>

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

  
  <h2>Trends in User Messaging Behavior</h2>

  <div class="section">
    <strong>Average message length:</strong> {avg_mesg_length}
  </div>

  <div class="section">
    <strong>Time period with highest frequency of sent messages:</strong> {sent_msg_period}
    <br>
    - {sent_period_percent}% of messages sent during this time period
  </div>

  <div class="section">
    <strong>Time period with highest frequency of sent messages:</strong> {rec_msg_period}
    <br>
    - {rec_period_percent}% of messages recieved during this time period
    <br>
  </div>

  <div class="section">
    <strong>Percentage of messages sent with attachments:</strong> {percent_attachments}%
  </div>

  <div class="section">
    <strong>Average time it takes to respond:</strong> {average_response_time}
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
    avg_mesg_length,
    sent_msg_period,
    sent_period_percent,
    rec_msg_period,
    rec_period_percent,
    percent_attachments,
    average_response_time,
    path="imessage_report.html",
):
    print("Constructing your personalized iMessage data report...")

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
        avg_mesg_length=avg_mesg_length,
        sent_msg_period=sent_msg_period,
        sent_period_percent=sent_period_percent,
        rec_msg_period=rec_msg_period,
        rec_period_percent=rec_period_percent,
        percent_attachments=percent_attachments,
        average_response_time=average_response_time,
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Report saved as '{path}'")

