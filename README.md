# iMessage Analysis

iMessage Analysis is a MacOS terminal script which generates an analysis report of your iMessage data.

## Project Overview

In the digital age, text message data serves as the most robust repository of interpersonal communications available for historical review, often spanning many years with content ranging from casual to professional communication. With iMessage Analysis, you can generate insights from your text messages within minutes. Using iMessage data stored on your Mac computer, iMessage analysis generates a report that displays your overall trends in your iMessage data, messaging habits, and how your communication tendencies vary between message recipients. 

## Features

- Generates an HTML report analyzing iMessage data, inclduing:
    - Statistical Overview (total number of messages, unique conversations, sent vs recieved, etc.)
    - Habit Overview (temporal analysis, average message length, media, etc.)
    - Social Network (summary and habit data for your top 10 correspondents)

## Potential Future Features

- AI-driven rhetoric and sentiment analysis
- Longitudal data vizualizations to show change in habits over time
- Network analysis vizualizations to map which of your correspondents know each other

## Installation

1. Download repository
2. Ensure that Terminal has "Full Disk Access" permissions, which can be enabled in the "Privacy and Security" section of System Settings
2. Ensure Python 3.10 or a later version is installed (the code will not run on earlier versions of Python)
3. Launch Terminal and enter "cd [filepath]/imessage_analysis"
4. In Terminal, enter "python3 -m venv venv" and "source venv/bin/activate"
5. Still in Terminal, enter "pip install pandas"
6. Launch the program in Terminal by entering "python3 imessage_analysis.py"
7. Follow the instructions in Terminal to the generate report

## Credits

- Created by Clay Wallace
- Code assistance powered by OpenAI GPT and Google Gemini
- Ideation and technical assistance from Professor Mark Johson
- iMessage and Contacts app data retrieval code adapted from Gold, K. (2023, July 27). Extract iMessage Data For Analytics and Conversational AI projects. Better Programming. https://medium.com/better-programming/extracting-imessage-and-address-book-data-b6e2e5729b21