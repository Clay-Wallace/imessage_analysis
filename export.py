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

  
  <h2>Trends in Your Messaging Behavior</h2>

  <div class="section">
    <strong>Average message length:</strong> {avg_mesg_length} words
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
    <strong>Average time it takes you to respond:</strong> {average_response_time}
  </div>

  <div class="section">
    <h2>Your Social Network</h2>
    <strong>Everything you need to know about your top 10 conversations<strong>
    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>Total Messages</th>
                <th>Sent Messages</th>
                <th>Received Messages</th>
                <th>Average Length</th>
                <th>Average Reply Time</th>
                <th>Top Sent Time</th>
                <th>Top Received Time</th>
                <th>Attachments</th>
            </tr>
        </thead>
        <tbody>
            {top_contacts_rows}
        </tbody>
    </table>
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
    top_contacts,
    path="imessage_report.html",
):
    print("Constructing your personalized iMessage data report...")

    rows_html = ""
    for rank, contact in enumerate(top_contacts, 1):
        # Format the average response time nicely
        # (Assuming you have a helper like format_timedelta, otherwise use str())
        resp_time_str = str(contact['average_response_time']) 
        
        row = f"""
        <tr>
            <td>#{rank}</td>
            <td>
                <strong>{contact['name']}</strong> {contact['is_group_chat']}
            </td>
            <td>{contact['total_count']:,}</td>
            <td>{contact['mesg_sent']:,} ({contact['percent_sent']:.1f}%)</td>
            <td>{contact['mesg_received']:,} ({contact['percent_received']:.1f}%)</td>
            <td>{contact['avg_mesg_length']} words</td>
            <td>{contact["average_response_time"]}</td>
            <td>{contact['sent_msg_period']} ({contact['sent_period_percent']:.0f}%)</td>
            <td>{contact['rec_msg_period']} ({contact['rec_period_percent']:.0f}%)</td>
            <td>{contact['percent_attachments']:.1f}%</td>
        </tr>
        """
        rows_html += row

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
        top_contacts_rows=rows_html,
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Report saved as '{path}'")

